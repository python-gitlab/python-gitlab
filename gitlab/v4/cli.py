#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2013-2017 Gauvain Pocentek <gauvain@pocentek.net>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import argparse
import operator
import sys
from typing import Any, Dict, List, Optional, Type, TYPE_CHECKING, Union

import gitlab
import gitlab.base
import gitlab.v4.objects
from gitlab import cli


class GitlabCLI:
    def __init__(
        self, gl: gitlab.Gitlab, what: str, action: str, args: Dict[str, str]
    ) -> None:
        self.cls: Type[gitlab.base.RESTObject] = cli.what_to_cls(
            what, namespace=gitlab.v4.objects
        )
        self.cls_name = self.cls.__name__
        self.what = what.replace("-", "_")
        self.action = action.lower()
        self.gl = gl
        self.args = args
        self.parent_args: Dict[str, Any] = {}
        self.mgr_cls: Union[
            Type[gitlab.mixins.CreateMixin],
            Type[gitlab.mixins.DeleteMixin],
            Type[gitlab.mixins.GetMixin],
            Type[gitlab.mixins.GetWithoutIdMixin],
            Type[gitlab.mixins.ListMixin],
            Type[gitlab.mixins.UpdateMixin],
        ] = getattr(gitlab.v4.objects, f"{self.cls.__name__}Manager")
        # We could do something smart, like splitting the manager name to find
        # parents, build the chain of managers to get to the final object.
        # Instead we do something ugly and efficient: interpolate variables in
        # the class _path attribute, and replace the value with the result.
        if TYPE_CHECKING:
            assert self.mgr_cls._path is not None

        self._process_from_parent_attrs()

        self.mgr_cls._path = self.mgr_cls._path.format(**self.parent_args)
        self.mgr = self.mgr_cls(gl)

        if self.mgr_cls._types:
            for attr_name, type_cls in self.mgr_cls._types.items():
                if attr_name in self.args.keys():
                    obj = type_cls()
                    obj.set_from_cli(self.args[attr_name])
                    self.args[attr_name] = obj.get()

    def _process_from_parent_attrs(self) -> None:
        """Items in the path need to be url-encoded. There is a 1:1 mapping from
        mgr_cls._from_parent_attrs <--> mgr_cls._path. Those values must be url-encoded
        as they may contain a slash '/'."""
        for key in self.mgr_cls._from_parent_attrs:
            if key not in self.args:
                continue

            self.parent_args[key] = gitlab.utils.EncodedId(self.args[key])
            # If we don't delete it then it will be added to the URL as a query-string
            del self.args[key]

    def run(self) -> Any:
        # Check for a method that matches object + action
        method = f"do_{self.what}_{self.action}"
        if hasattr(self, method):
            return getattr(self, method)()

        # Fallback to standard actions (get, list, create, ...)
        method = f"do_{self.action}"
        if hasattr(self, method):
            return getattr(self, method)()

        # Finally try to find custom methods
        return self.do_custom()

    def do_custom(self) -> Any:
        class_instance: Union[gitlab.base.RESTManager, gitlab.base.RESTObject]
        in_obj = cli.custom_actions[self.cls_name][self.action][2]

        # Get the object (lazy), then act
        if in_obj:
            data = {}
            if self.mgr._from_parent_attrs:
                for k in self.mgr._from_parent_attrs:
                    data[k] = self.parent_args[k]
            if not issubclass(self.cls, gitlab.mixins.GetWithoutIdMixin):
                if TYPE_CHECKING:
                    assert isinstance(self.cls._id_attr, str)
                data[self.cls._id_attr] = self.args.pop(self.cls._id_attr)
            class_instance = self.cls(self.mgr, data)
        else:
            class_instance = self.mgr

        method_name = self.action.replace("-", "_")
        return getattr(class_instance, method_name)(**self.args)

    def do_project_export_download(self) -> None:
        try:
            project = self.gl.projects.get(self.parent_args["project_id"], lazy=True)
            export_status = project.exports.get()
            if TYPE_CHECKING:
                assert export_status is not None
            data = export_status.download()
            if TYPE_CHECKING:
                assert data is not None
            sys.stdout.buffer.write(data)

        except Exception as e:  # pragma: no cover, cli.die is unit-tested
            cli.die("Impossible to download the export", e)

    def do_create(self) -> gitlab.base.RESTObject:
        if TYPE_CHECKING:
            assert isinstance(self.mgr, gitlab.mixins.CreateMixin)
        try:
            result = self.mgr.create(self.args)
        except Exception as e:  # pragma: no cover, cli.die is unit-tested
            cli.die("Impossible to create object", e)
        return result

    def do_list(
        self,
    ) -> Union[gitlab.base.RESTObjectList, List[gitlab.base.RESTObject]]:
        if TYPE_CHECKING:
            assert isinstance(self.mgr, gitlab.mixins.ListMixin)
        try:
            result = self.mgr.list(**self.args)
        except Exception as e:  # pragma: no cover, cli.die is unit-tested
            cli.die("Impossible to list objects", e)
        return result

    def do_get(self) -> Optional[gitlab.base.RESTObject]:
        if isinstance(self.mgr, gitlab.mixins.GetWithoutIdMixin):
            try:
                result = self.mgr.get(id=None, **self.args)
            except Exception as e:  # pragma: no cover, cli.die is unit-tested
                cli.die("Impossible to get object", e)
            return result

        if TYPE_CHECKING:
            assert isinstance(self.mgr, gitlab.mixins.GetMixin)
            assert isinstance(self.cls._id_attr, str)

        id = self.args.pop(self.cls._id_attr)
        try:
            result = self.mgr.get(id, lazy=False, **self.args)
        except Exception as e:  # pragma: no cover, cli.die is unit-tested
            cli.die("Impossible to get object", e)
        return result

    def do_delete(self) -> None:
        if TYPE_CHECKING:
            assert isinstance(self.mgr, gitlab.mixins.DeleteMixin)
            assert isinstance(self.cls._id_attr, str)
        id = self.args.pop(self.cls._id_attr)
        try:
            self.mgr.delete(id, **self.args)
        except Exception as e:  # pragma: no cover, cli.die is unit-tested
            cli.die("Impossible to destroy object", e)

    def do_update(self) -> Dict[str, Any]:
        if TYPE_CHECKING:
            assert isinstance(self.mgr, gitlab.mixins.UpdateMixin)
        if issubclass(self.mgr_cls, gitlab.mixins.GetWithoutIdMixin):
            id = None
        else:
            if TYPE_CHECKING:
                assert isinstance(self.cls._id_attr, str)
            id = self.args.pop(self.cls._id_attr)

        try:
            result = self.mgr.update(id, self.args)
        except Exception as e:  # pragma: no cover, cli.die is unit-tested
            cli.die("Impossible to update object", e)
        return result


def _populate_sub_parser_by_class(
    cls: Type[gitlab.base.RESTObject], sub_parser: argparse._SubParsersAction
) -> None:
    mgr_cls_name = f"{cls.__name__}Manager"
    mgr_cls = getattr(gitlab.v4.objects, mgr_cls_name)

    action_parsers: Dict[str, argparse.ArgumentParser] = {}
    for action_name in ["list", "get", "create", "update", "delete"]:
        if not hasattr(mgr_cls, action_name):
            continue

        sub_parser_action = sub_parser.add_parser(
            action_name, conflict_handler="resolve"
        )
        action_parsers[action_name] = sub_parser_action
        sub_parser_action.add_argument("--sudo", required=False)
        if mgr_cls._from_parent_attrs:
            for x in mgr_cls._from_parent_attrs:
                sub_parser_action.add_argument(
                    f"--{x.replace('_', '-')}", required=True
                )

        if action_name == "list":
            for x in mgr_cls._list_filters:
                sub_parser_action.add_argument(
                    f"--{x.replace('_', '-')}", required=False
                )

            sub_parser_action.add_argument("--page", required=False, type=int)
            sub_parser_action.add_argument("--per-page", required=False, type=int)
            sub_parser_action.add_argument("--all", required=False, action="store_true")

        if action_name == "delete":
            if cls._id_attr is not None:
                id_attr = cls._id_attr.replace("_", "-")
                sub_parser_action.add_argument(f"--{id_attr}", required=True)

        if action_name == "get":
            if not issubclass(cls, gitlab.mixins.GetWithoutIdMixin):
                if cls._id_attr is not None:
                    id_attr = cls._id_attr.replace("_", "-")
                    sub_parser_action.add_argument(f"--{id_attr}", required=True)

            for x in mgr_cls._optional_get_attrs:
                sub_parser_action.add_argument(
                    f"--{x.replace('_', '-')}", required=False
                )

        if action_name == "create":
            for x in mgr_cls._create_attrs.required:
                sub_parser_action.add_argument(
                    f"--{x.replace('_', '-')}", required=True
                )
            for x in mgr_cls._create_attrs.optional:
                sub_parser_action.add_argument(
                    f"--{x.replace('_', '-')}", required=False
                )

        if action_name == "update":
            if cls._id_attr is not None:
                id_attr = cls._id_attr.replace("_", "-")
                sub_parser_action.add_argument(f"--{id_attr}", required=True)

            for x in mgr_cls._update_attrs.required:
                if x != cls._id_attr:
                    sub_parser_action.add_argument(
                        f"--{x.replace('_', '-')}", required=True
                    )

            for x in mgr_cls._update_attrs.optional:
                if x != cls._id_attr:
                    sub_parser_action.add_argument(
                        f"--{x.replace('_', '-')}", required=False
                    )

    if cls.__name__ in cli.custom_actions:
        name = cls.__name__
        for action_name in cli.custom_actions[name]:
            # NOTE(jlvillal): If we put a function for the `default` value of
            # the `get` it will always get called, which will break things.
            sub_parser_action = action_parsers.get(action_name)
            if sub_parser_action is None:
                sub_parser_action = sub_parser.add_parser(action_name)
            # Get the attributes for URL/path construction
            if mgr_cls._from_parent_attrs:
                for x in mgr_cls._from_parent_attrs:
                    sub_parser_action.add_argument(
                        f"--{x.replace('_', '-')}", required=True
                    )
                sub_parser_action.add_argument("--sudo", required=False)

            # We need to get the object somehow
            if not issubclass(cls, gitlab.mixins.GetWithoutIdMixin):
                if cls._id_attr is not None:
                    id_attr = cls._id_attr.replace("_", "-")
                    sub_parser_action.add_argument(f"--{id_attr}", required=True)

            required, optional, dummy = cli.custom_actions[name][action_name]
            for x in required:
                if x != cls._id_attr:
                    sub_parser_action.add_argument(
                        f"--{x.replace('_', '-')}", required=True
                    )
            for x in optional:
                if x != cls._id_attr:
                    sub_parser_action.add_argument(
                        f"--{x.replace('_', '-')}", required=False
                    )

    if mgr_cls.__name__ in cli.custom_actions:
        name = mgr_cls.__name__
        for action_name in cli.custom_actions[name]:
            # NOTE(jlvillal): If we put a function for the `default` value of
            # the `get` it will always get called, which will break things.
            sub_parser_action = action_parsers.get(action_name)
            if sub_parser_action is None:
                sub_parser_action = sub_parser.add_parser(action_name)
            if mgr_cls._from_parent_attrs:
                for x in mgr_cls._from_parent_attrs:
                    sub_parser_action.add_argument(
                        f"--{x.replace('_', '-')}", required=True
                    )
                sub_parser_action.add_argument("--sudo", required=False)

            required, optional, dummy = cli.custom_actions[name][action_name]
            for x in required:
                if x != cls._id_attr:
                    sub_parser_action.add_argument(
                        f"--{x.replace('_', '-')}", required=True
                    )
            for x in optional:
                if x != cls._id_attr:
                    sub_parser_action.add_argument(
                        f"--{x.replace('_', '-')}", required=False
                    )


def extend_parser(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    subparsers = parser.add_subparsers(
        title="object", dest="what", help="Object to manipulate."
    )
    subparsers.required = True

    # populate argparse for all Gitlab Object
    classes = set()
    for cls in gitlab.v4.objects.__dict__.values():
        if not isinstance(cls, type):
            continue
        if issubclass(cls, gitlab.base.RESTManager):
            if cls._obj_cls is not None:
                classes.add(cls._obj_cls)

    for cls in sorted(classes, key=operator.attrgetter("__name__")):
        arg_name = cli.cls_to_what(cls)
        object_group = subparsers.add_parser(arg_name)

        object_subparsers = object_group.add_subparsers(
            title="action", dest="whaction", help="Action to execute."
        )
        _populate_sub_parser_by_class(cls, object_subparsers)
        object_subparsers.required = True

    return parser


def get_dict(
    obj: Union[str, gitlab.base.RESTObject], fields: List[str]
) -> Union[str, Dict[str, Any]]:
    if isinstance(obj, str):
        return obj

    if fields:
        return {k: v for k, v in obj.attributes.items() if k in fields}
    return obj.attributes


class JSONPrinter:
    def display(self, d: Union[str, Dict[str, Any]], **kwargs: Any) -> None:
        import json  # noqa

        print(json.dumps(d))

    def display_list(
        self,
        data: List[Union[str, gitlab.base.RESTObject]],
        fields: List[str],
        **kwargs: Any,
    ) -> None:
        import json  # noqa

        print(json.dumps([get_dict(obj, fields) for obj in data]))


class YAMLPrinter:
    def display(self, d: Union[str, Dict[str, Any]], **kwargs: Any) -> None:
        try:
            import yaml  # noqa

            print(yaml.safe_dump(d, default_flow_style=False))
        except ImportError:
            exit(
                "PyYaml is not installed.\n"
                "Install it with `pip install PyYaml` "
                "to use the yaml output feature"
            )

    def display_list(
        self,
        data: List[Union[str, gitlab.base.RESTObject]],
        fields: List[str],
        **kwargs: Any,
    ) -> None:
        try:
            import yaml  # noqa

            print(
                yaml.safe_dump(
                    [get_dict(obj, fields) for obj in data], default_flow_style=False
                )
            )
        except ImportError:
            exit(
                "PyYaml is not installed.\n"
                "Install it with `pip install PyYaml` "
                "to use the yaml output feature"
            )


class LegacyPrinter:
    def display(self, d: Union[str, Dict[str, Any]], **kwargs: Any) -> None:
        verbose = kwargs.get("verbose", False)
        padding = kwargs.get("padding", 0)
        obj: Optional[Union[Dict[str, Any], gitlab.base.RESTObject]] = kwargs.get("obj")
        if TYPE_CHECKING:
            assert obj is not None

        def display_dict(d: Dict[str, Any], padding: int) -> None:
            for k in sorted(d.keys()):
                v = d[k]
                if isinstance(v, dict):
                    print(f"{' ' * padding}{k.replace('_', '-')}:")
                    new_padding = padding + 2
                    self.display(v, verbose=True, padding=new_padding, obj=v)
                    continue
                print(f"{' ' * padding}{k.replace('_', '-')}: {v}")

        if verbose:
            if isinstance(obj, dict):
                display_dict(obj, padding)
                return

            # not a dict, we assume it's a RESTObject
            if obj._id_attr:
                id = getattr(obj, obj._id_attr, None)
                print(f"{obj._id_attr}: {id}")
            attrs = obj.attributes
            if obj._id_attr:
                attrs.pop(obj._id_attr)
            display_dict(attrs, padding)

        else:
            if TYPE_CHECKING:
                assert isinstance(obj, gitlab.base.RESTObject)
            if obj._id_attr:
                id = getattr(obj, obj._id_attr)
                print(f"{obj._id_attr.replace('_', '-')}: {id}")
            if obj._repr_attr:
                value = getattr(obj, obj._repr_attr, "None")
                value = value.replace("\r", "").replace("\n", " ")
                # If the attribute is a note (ProjectCommitComment) then we do
                # some modifications to fit everything on one line
                line = f"{obj._repr_attr}: {value}"
                # ellipsize long lines (comments)
                if len(line) > 79:
                    line = f"{line[:76]}..."
                print(line)

    def display_list(
        self,
        data: List[Union[str, gitlab.base.RESTObject]],
        fields: List[str],
        **kwargs: Any,
    ) -> None:
        verbose = kwargs.get("verbose", False)
        for obj in data:
            if isinstance(obj, gitlab.base.RESTObject):
                self.display(get_dict(obj, fields), verbose=verbose, obj=obj)
            else:
                print(obj)
            print("")


PRINTERS: Dict[
    str, Union[Type[JSONPrinter], Type[LegacyPrinter], Type[YAMLPrinter]]
] = {
    "json": JSONPrinter,
    "legacy": LegacyPrinter,
    "yaml": YAMLPrinter,
}


def run(
    gl: gitlab.Gitlab,
    what: str,
    action: str,
    args: Dict[str, Any],
    verbose: bool,
    output: str,
    fields: List[str],
) -> None:
    g_cli = GitlabCLI(gl=gl, what=what, action=action, args=args)
    data = g_cli.run()

    printer: Union[JSONPrinter, LegacyPrinter, YAMLPrinter] = PRINTERS[output]()

    if isinstance(data, dict):
        printer.display(data, verbose=True, obj=data)
    elif isinstance(data, list):
        printer.display_list(data, fields, verbose=verbose)
    elif isinstance(data, gitlab.base.RESTObject):
        printer.display(get_dict(data, fields), verbose=verbose, obj=data)
    elif isinstance(data, str):
        print(data)
    elif isinstance(data, bytes):
        sys.stdout.buffer.write(data)
    elif hasattr(data, "decode"):
        print(data.decode())

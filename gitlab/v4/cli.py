import argparse
import json
import operator
import sys
from typing import Any, Dict, List, Optional, Type, TYPE_CHECKING, Union

import gitlab
import gitlab.base
import gitlab.v4.objects
from gitlab import cli
from gitlab.exceptions import GitlabCiLintError


class GitlabCLI:
    def __init__(
        self,
        gl: gitlab.Gitlab,
        gitlab_resource: str,
        resource_action: str,
        args: Dict[str, str],
    ) -> None:
        self.cls: Type[gitlab.base.RESTObject] = cli.gitlab_resource_to_cls(
            gitlab_resource, namespace=gitlab.v4.objects
        )
        self.cls_name = self.cls.__name__
        self.gitlab_resource = gitlab_resource.replace("-", "_")
        self.resource_action = resource_action.lower()
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
        self.mgr._from_parent_attrs = self.parent_args
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
        # Check for a method that matches gitlab_resource + action
        method = f"do_{self.gitlab_resource}_{self.resource_action}"
        if hasattr(self, method):
            return getattr(self, method)()

        # Fallback to standard actions (get, list, create, ...)
        method = f"do_{self.resource_action}"
        if hasattr(self, method):
            return getattr(self, method)()

        # Finally try to find custom methods
        return self.do_custom()

    def do_custom(self) -> Any:
        class_instance: Union[gitlab.base.RESTManager, gitlab.base.RESTObject]
        in_obj = cli.custom_actions[self.cls_name][self.resource_action].in_object

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

        method_name = self.resource_action.replace("-", "_")
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
                assert isinstance(data, bytes)
            sys.stdout.buffer.write(data)

        except Exception as e:  # pragma: no cover, cli.die is unit-tested
            cli.die("Impossible to download the export", e)

    def do_validate(self) -> None:
        if TYPE_CHECKING:
            assert isinstance(self.mgr, gitlab.v4.objects.CiLintManager)
        try:
            self.mgr.validate(self.args)
        except GitlabCiLintError as e:  # pragma: no cover, cli.die is unit-tested
            cli.die("CI YAML Lint failed", e)
        except Exception as e:  # pragma: no cover, cli.die is unit-tested
            cli.die("Cannot validate CI YAML", e)

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
        message_details = gitlab.utils.WarnMessageData(
            message=(
                "Your query returned {len_items} of {total_items} items. To return all "
                "items use `--get-all`. To silence this warning use `--no-get-all`."
            ),
            show_caller=False,
        )

        try:
            result = self.mgr.list(**self.args, message_details=message_details)
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


# https://github.com/python/typeshed/issues/7539#issuecomment-1076581049
if TYPE_CHECKING:
    _SubparserType = argparse._SubParsersAction[argparse.ArgumentParser]
else:
    _SubparserType = Any


def _populate_sub_parser_by_class(
    cls: Type[gitlab.base.RESTObject],
    sub_parser: _SubparserType,
) -> None:
    mgr_cls_name = f"{cls.__name__}Manager"
    mgr_cls = getattr(gitlab.v4.objects, mgr_cls_name)

    action_parsers: Dict[str, argparse.ArgumentParser] = {}
    for action_name, help_text in [
        ("list", "List the GitLab resources"),
        ("get", "Get a GitLab resource"),
        ("create", "Create a GitLab resource"),
        ("update", "Update a GitLab resource"),
        ("delete", "Delete a GitLab resource"),
    ]:
        if not hasattr(mgr_cls, action_name):
            continue

        sub_parser_action = sub_parser.add_parser(
            action_name,
            conflict_handler="resolve",
            help=help_text,
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
            get_all_group = sub_parser_action.add_mutually_exclusive_group()
            get_all_group.add_argument(
                "--get-all",
                required=False,
                action="store_const",
                const=True,
                default=None,
                dest="get_all",
                help="Return all items from the server, without pagination.",
            )
            get_all_group.add_argument(
                "--no-get-all",
                required=False,
                action="store_const",
                const=False,
                default=None,
                dest="get_all",
                help="Don't return all items from the server.",
            )

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
            if mgr_cls._create_attrs.exclusive:
                group = sub_parser_action.add_mutually_exclusive_group()
                for x in mgr_cls._create_attrs.exclusive:
                    group.add_argument(f"--{x.replace('_', '-')}")

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

            if mgr_cls._update_attrs.exclusive:
                group = sub_parser_action.add_mutually_exclusive_group()
                for x in mgr_cls._update_attrs.exclusive:
                    group.add_argument(f"--{x.replace('_', '-')}")

    if cls.__name__ in cli.custom_actions:
        name = cls.__name__
        for action_name in cli.custom_actions[name]:
            custom_action = cli.custom_actions[name][action_name]
            # NOTE(jlvillal): If we put a function for the `default` value of
            # the `get` it will always get called, which will break things.
            action_parser = action_parsers.get(action_name)
            if action_parser is None:
                sub_parser_action = sub_parser.add_parser(
                    action_name, help=custom_action.help
                )
            else:
                sub_parser_action = action_parser
            # Get the attributes for URL/path construction
            if mgr_cls._from_parent_attrs:
                for x in mgr_cls._from_parent_attrs:
                    sub_parser_action.add_argument(
                        f"--{x.replace('_', '-')}", required=True
                    )
                sub_parser_action.add_argument("--sudo", required=False)

            # We need to get the object somehow
            if not issubclass(cls, gitlab.mixins.GetWithoutIdMixin):
                if cls._id_attr is not None and custom_action.requires_id:
                    id_attr = cls._id_attr.replace("_", "-")
                    sub_parser_action.add_argument(f"--{id_attr}", required=True)

            for x in custom_action.required:
                if x != cls._id_attr:
                    sub_parser_action.add_argument(
                        f"--{x.replace('_', '-')}", required=True
                    )
            for x in custom_action.optional:
                if x != cls._id_attr:
                    sub_parser_action.add_argument(
                        f"--{x.replace('_', '-')}", required=False
                    )

    if mgr_cls.__name__ in cli.custom_actions:
        name = mgr_cls.__name__
        for action_name in cli.custom_actions[name]:
            # NOTE(jlvillal): If we put a function for the `default` value of
            # the `get` it will always get called, which will break things.
            action_parser = action_parsers.get(action_name)
            if action_parser is None:
                sub_parser_action = sub_parser.add_parser(action_name)
            else:
                sub_parser_action = action_parser
            if mgr_cls._from_parent_attrs:
                for x in mgr_cls._from_parent_attrs:
                    sub_parser_action.add_argument(
                        f"--{x.replace('_', '-')}", required=True
                    )
                sub_parser_action.add_argument("--sudo", required=False)

            custom_action = cli.custom_actions[name][action_name]
            for x in custom_action.required:
                if x != cls._id_attr:
                    sub_parser_action.add_argument(
                        f"--{x.replace('_', '-')}", required=True
                    )
            for x in custom_action.optional:
                if x != cls._id_attr:
                    sub_parser_action.add_argument(
                        f"--{x.replace('_', '-')}", required=False
                    )


def extend_parser(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    subparsers = parser.add_subparsers(
        title="resource",
        dest="gitlab_resource",
        help="The GitLab resource to manipulate.",
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
        arg_name = cli.cls_to_gitlab_resource(cls)
        mgr_cls_name = f"{cls.__name__}Manager"
        mgr_cls = getattr(gitlab.v4.objects, mgr_cls_name)
        object_group = subparsers.add_parser(
            arg_name,
            help=f"API endpoint: {mgr_cls._path}",
        )

        object_subparsers = object_group.add_subparsers(
            title="action",
            dest="resource_action",
            help="Action to execute on the GitLab resource.",
        )
        _populate_sub_parser_by_class(cls, object_subparsers)
        object_subparsers.required = True

    return parser


def get_dict(
    obj: Union[str, Dict[str, Any], gitlab.base.RESTObject], fields: List[str]
) -> Union[str, Dict[str, Any]]:
    if not isinstance(obj, gitlab.base.RESTObject):
        return obj

    if fields:
        return {k: v for k, v in obj.attributes.items() if k in fields}
    return obj.attributes


class JSONPrinter:
    @staticmethod
    def display(d: Union[str, Dict[str, Any]], **_kwargs: Any) -> None:
        print(json.dumps(d))

    @staticmethod
    def display_list(
        data: List[Union[str, Dict[str, Any], gitlab.base.RESTObject]],
        fields: List[str],
        **_kwargs: Any,
    ) -> None:
        print(json.dumps([get_dict(obj, fields) for obj in data]))


class YAMLPrinter:
    @staticmethod
    def display(d: Union[str, Dict[str, Any]], **_kwargs: Any) -> None:
        try:
            import yaml  # noqa

            print(yaml.safe_dump(d, default_flow_style=False))
        except ImportError:
            sys.exit(
                "PyYaml is not installed.\n"
                "Install it with `pip install PyYaml` "
                "to use the yaml output feature"
            )

    @staticmethod
    def display_list(
        data: List[Union[str, Dict[str, Any], gitlab.base.RESTObject]],
        fields: List[str],
        **_kwargs: Any,
    ) -> None:
        try:
            import yaml  # noqa

            print(
                yaml.safe_dump(
                    [get_dict(obj, fields) for obj in data], default_flow_style=False
                )
            )
        except ImportError:
            sys.exit(
                "PyYaml is not installed.\n"
                "Install it with `pip install PyYaml` "
                "to use the yaml output feature"
            )


class LegacyPrinter:
    def display(self, _d: Union[str, Dict[str, Any]], **kwargs: Any) -> None:
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
            return

        lines = []

        if TYPE_CHECKING:
            assert isinstance(obj, gitlab.base.RESTObject)

        if obj._id_attr:
            id = getattr(obj, obj._id_attr)
            lines.append(f"{obj._id_attr.replace('_', '-')}: {id}")
        if obj._repr_attr:
            value = getattr(obj, obj._repr_attr, "None") or "None"
            value = value.replace("\r", "").replace("\n", " ")
            # If the attribute is a note (ProjectCommitComment) then we do
            # some modifications to fit everything on one line
            line = f"{obj._repr_attr}: {value}"
            # ellipsize long lines (comments)
            if len(line) > 79:
                line = f"{line[:76]}..."
            lines.append(line)

        if lines:
            print("\n".join(lines))
            return

        print(
            f"No default fields to show for {obj!r}. "
            f"Please use  '--verbose' or the JSON/YAML formatters."
        )

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
    gitlab_resource: str,
    resource_action: str,
    args: Dict[str, Any],
    verbose: bool,
    output: str,
    fields: List[str],
) -> None:
    g_cli = GitlabCLI(
        gl=gl,
        gitlab_resource=gitlab_resource,
        resource_action=resource_action,
        args=args,
    )
    data = g_cli.run()

    printer: Union[JSONPrinter, LegacyPrinter, YAMLPrinter] = PRINTERS[output]()

    if isinstance(data, dict):
        printer.display(data, verbose=True, obj=data)
    elif isinstance(data, list):
        printer.display_list(data, fields, verbose=verbose)
    elif isinstance(data, gitlab.base.RESTObjectList):
        printer.display_list(list(data), fields, verbose=verbose)
    elif isinstance(data, gitlab.base.RESTObject):
        printer.display(get_dict(data, fields), verbose=verbose, obj=data)
    elif isinstance(data, str):
        print(data)
    elif isinstance(data, bytes):
        sys.stdout.buffer.write(data)
    elif hasattr(data, "decode"):
        print(data.decode())

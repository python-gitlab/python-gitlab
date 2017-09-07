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

from __future__ import print_function
import inspect
import operator

import six

import gitlab
import gitlab.base
from gitlab import cli
import gitlab.v4.objects


class GitlabCLI(object):
    def __init__(self, gl, what, action, args):
        self.cls_name = cli.what_to_cls(what)
        self.cls = gitlab.v4.objects.__dict__[self.cls_name]
        self.what = what.replace('-', '_')
        self.action = action.lower()
        self.gl = gl
        self.args = args
        self.mgr_cls = getattr(gitlab.v4.objects,
                               self.cls.__name__ + 'Manager')
        # We could do something smart, like splitting the manager name to find
        # parents, build the chain of managers to get to the final object.
        # Instead we do something ugly and efficient: interpolate variables in
        # the class _path attribute, and replace the value with the result.
        self.mgr_cls._path = self.mgr_cls._path % self.args
        self.mgr = self.mgr_cls(gl)

    def __call__(self):
        method = 'do_%s' % self.action
        if hasattr(self, method):
            return getattr(self, method)()
        else:
            return self.do_custom()

    def do_custom(self):
        in_obj = cli.custom_actions[self.cls_name][self.action][2]

        # Get the object (lazy), then act
        if in_obj:
            data = {}
            if hasattr(self.mgr, '_from_parent_attrs'):
                for k in self.mgr._from_parent_attrs:
                    data[k] = self.args[k]
            if gitlab.mixins.GetWithoutIdMixin not in inspect.getmro(self.cls):
                data[self.cls._id_attr] = self.args.pop(self.cls._id_attr)
            o = self.cls(self.mgr, data)
            method_name = self.action.replace('-', '_')
            return getattr(o, method_name)(**self.args)
        else:
            return getattr(self.mgr, self.action)(**self.args)

    def do_create(self):
        try:
            return self.mgr.create(self.args)
        except Exception as e:
            cli.die("Impossible to create object", e)

    def do_list(self):
        try:
            return self.mgr.list(**self.args)
        except Exception as e:
            cli.die("Impossible to list objects", e)

    def do_get(self):
        id = None
        if gitlab.mixins.GetWithoutIdMixin not in inspect.getmro(self.cls):
            id = self.args.pop(self.cls._id_attr)

        try:
            return self.mgr.get(id, **self.args)
        except Exception as e:
            cli.die("Impossible to get object", e)

    def do_delete(self):
        id = self.args.pop(self.cls._id_attr)
        try:
            self.mgr.delete(id, **self.args)
        except Exception as e:
            cli.die("Impossible to destroy object", e)

    def do_update(self):
        id = self.args.pop(self.cls._id_attr)
        try:
            return self.mgr.update(id, self.args)
        except Exception as e:
            cli.die("Impossible to update object", e)


def _populate_sub_parser_by_class(cls, sub_parser):
    mgr_cls_name = cls.__name__ + 'Manager'
    mgr_cls = getattr(gitlab.v4.objects, mgr_cls_name)

    for action_name in ['list', 'get', 'create', 'update', 'delete']:
        if not hasattr(mgr_cls, action_name):
            continue

        sub_parser_action = sub_parser.add_parser(action_name)
        sub_parser_action.add_argument("--sudo", required=False)
        if hasattr(mgr_cls, '_from_parent_attrs'):
            [sub_parser_action.add_argument("--%s" % x.replace('_', '-'),
                                            required=True)
             for x in mgr_cls._from_parent_attrs]

        if action_name == "list":
            if hasattr(mgr_cls, '_list_filters'):
                [sub_parser_action.add_argument("--%s" % x.replace('_', '-'),
                                                required=False)
                 for x in mgr_cls._list_filters]

            sub_parser_action.add_argument("--page", required=False)
            sub_parser_action.add_argument("--per-page", required=False)
            sub_parser_action.add_argument("--all", required=False,
                                           action='store_true')

        if action_name == 'delete':
            id_attr = cls._id_attr.replace('_', '-')
            sub_parser_action.add_argument("--%s" % id_attr, required=True)

        if action_name == "get":
            if gitlab.mixins.GetWithoutIdMixin not in inspect.getmro(cls):
                if cls._id_attr is not None:
                    id_attr = cls._id_attr.replace('_', '-')
                    sub_parser_action.add_argument("--%s" % id_attr,
                                                   required=True)

            if hasattr(mgr_cls, '_optional_get_attrs'):
                [sub_parser_action.add_argument("--%s" % x.replace('_', '-'),
                                                required=False)
                 for x in mgr_cls._optional_get_attrs]

        if action_name == "create":
            if hasattr(mgr_cls, '_create_attrs'):
                [sub_parser_action.add_argument("--%s" % x.replace('_', '-'),
                                                required=True)
                 for x in mgr_cls._create_attrs[0] if x != cls._id_attr]

                [sub_parser_action.add_argument("--%s" % x.replace('_', '-'),
                                                required=False)
                 for x in mgr_cls._create_attrs[1] if x != cls._id_attr]

        if action_name == "update":
            if cls._id_attr is not None:
                id_attr = cls._id_attr.replace('_', '-')
                sub_parser_action.add_argument("--%s" % id_attr,
                                               required=True)

            if hasattr(mgr_cls, '_update_attrs'):
                [sub_parser_action.add_argument("--%s" % x.replace('_', '-'),
                                                required=True)
                 for x in mgr_cls._update_attrs[0] if x != cls._id_attr]

                [sub_parser_action.add_argument("--%s" % x.replace('_', '-'),
                                                required=False)
                 for x in mgr_cls._update_attrs[1] if x != cls._id_attr]

    if cls.__name__ in cli.custom_actions:
        name = cls.__name__
        for action_name in cli.custom_actions[name]:
            sub_parser_action = sub_parser.add_parser(action_name)
            # Get the attributes for URL/path construction
            if hasattr(mgr_cls, '_from_parent_attrs'):
                [sub_parser_action.add_argument("--%s" % x.replace('_', '-'),
                                                required=True)
                 for x in mgr_cls._from_parent_attrs]
                sub_parser_action.add_argument("--sudo", required=False)

            # We need to get the object somehow
            if gitlab.mixins.GetWithoutIdMixin not in inspect.getmro(cls):
                if cls._id_attr is not None:
                    id_attr = cls._id_attr.replace('_', '-')
                    sub_parser_action.add_argument("--%s" % id_attr,
                                                   required=True)

            required, optional, dummy = cli.custom_actions[name][action_name]
            [sub_parser_action.add_argument("--%s" % x.replace('_', '-'),
                                            required=True)
             for x in required if x != cls._id_attr]
            [sub_parser_action.add_argument("--%s" % x.replace('_', '-'),
                                            required=False)
             for x in optional if x != cls._id_attr]

    if mgr_cls.__name__ in cli.custom_actions:
        name = mgr_cls.__name__
        for action_name in cli.custom_actions[name]:
            sub_parser_action = sub_parser.add_parser(action_name)
            if hasattr(mgr_cls, '_from_parent_attrs'):
                [sub_parser_action.add_argument("--%s" % x.replace('_', '-'),
                                                required=True)
                 for x in mgr_cls._from_parent_attrs]
                sub_parser_action.add_argument("--sudo", required=False)

            required, optional, dummy = cli.custom_actions[name][action_name]
            [sub_parser_action.add_argument("--%s" % x.replace('_', '-'),
                                            required=True)
             for x in required if x != cls._id_attr]
            [sub_parser_action.add_argument("--%s" % x.replace('_', '-'),
                                            required=False)
             for x in optional if x != cls._id_attr]


def extend_parser(parser):
    subparsers = parser.add_subparsers(title='object', dest='what',
                                       help="Object to manipulate.")
    subparsers.required = True

    # populate argparse for all Gitlab Object
    classes = []
    for cls in gitlab.v4.objects.__dict__.values():
        try:
            if gitlab.base.RESTManager in inspect.getmro(cls):
                if cls._obj_cls is not None:
                    classes.append(cls._obj_cls)
        except AttributeError:
            pass
    classes.sort(key=operator.attrgetter("__name__"))

    for cls in classes:
        arg_name = cli.cls_to_what(cls)
        object_group = subparsers.add_parser(arg_name)

        object_subparsers = object_group.add_subparsers(
            dest='action', help="Action to execute.")
        _populate_sub_parser_by_class(cls, object_subparsers)
        object_subparsers.required = True

    return parser


class JSONPrinter(object):
    def display(self, d, **kwargs):
        import json  # noqa

        print(json.dumps(d))


class YAMLPrinter(object):
    def display(self, d, **kwargs):
        import yaml  # noqa

        print(yaml.safe_dump(d, default_flow_style=False))


class LegacyPrinter(object):
    def display(self, d, **kwargs):
        verbose = kwargs.get('verbose', False)
        padding = kwargs.get('padding', 0)
        obj = kwargs.get('obj')

        def display_dict(d, padding):
            for k in sorted(d.keys()):
                v = d[k]
                if isinstance(v, dict):
                    print('%s%s:' % (' ' * padding, k.replace('_', '-')))
                    new_padding = padding + 2
                    self.display(v, verbose=True, padding=new_padding, obj=v)
                    continue
                print('%s%s: %s' % (' ' * padding, k.replace('_', '-'), v))

        if verbose:
            if isinstance(obj, dict):
                display_dict(obj, padding)
                return

            # not a dict, we assume it's a RESTObject
            id = getattr(obj, obj._id_attr, None)
            print('%s: %s' % (obj._id_attr, id))
            attrs = obj.attributes
            attrs.pop(obj._id_attr)
            display_dict(attrs, padding)

        else:
            id = getattr(obj, obj._id_attr)
            print('%s: %s' % (obj._id_attr.replace('_', '-'), id))
            if hasattr(obj, '_short_print_attr'):
                value = getattr(obj, obj._short_print_attr)
                print('%s: %s' % (obj._short_print_attr, value))


PRINTERS = {
    'json': JSONPrinter,
    'legacy': LegacyPrinter,
    'yaml': YAMLPrinter,
}


def run(gl, what, action, args, verbose, output, fields):
    g_cli = GitlabCLI(gl, what, action, args)
    ret_val = g_cli()

    printer = PRINTERS[output]()

    def get_dict(obj):
        if fields:
            return {k: v for k, v in obj.attributes.items()
                    if k in fields}
        return obj.attributes

    if isinstance(ret_val, dict):
        printer.display(ret_val, verbose=True, obj=ret_val)
    elif isinstance(ret_val, list):
        for obj in ret_val:
            if isinstance(obj, gitlab.base.RESTObject):
                printer.display(get_dict(obj), verbose=verbose, obj=obj)
            else:
                print(obj)
            print('')
    elif isinstance(ret_val, gitlab.base.RESTObject):
        printer.display(get_dict(ret_val), verbose=verbose, obj=ret_val)
    elif isinstance(ret_val, six.string_types):
        print(ret_val)

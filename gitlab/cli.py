#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2013-2015 Gauvain Pocentek <gauvain@pocentek.net>
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
from __future__ import division
from __future__ import absolute_import
import argparse
import inspect
import operator
import re
import sys

import gitlab

camel_re = re.compile('(.)([A-Z])')
LIST = 'list'
GET = 'get'
CREATE = 'create'
UPDATE = 'update'
DELETE = 'delete'
PROTECT = 'protect'
UNPROTECT = 'unprotect'
SEARCH = 'search'
OWNED = 'owned'
ALL = 'all'
ACTIONS = [LIST, GET, CREATE, UPDATE, DELETE]
EXTRA_ACTION = [PROTECT, UNPROTECT, SEARCH, OWNED, ALL]

extra_actions = {
    gitlab.ProjectBranch: {PROTECT: {'requiredAttrs': ['id', 'project-id']},
                           UNPROTECT: {'requiredAttrs': ['id', 'project-id']}},
    gitlab.Project: {SEARCH: {'requiredAttrs': ['query']},
                     OWNED: {'requiredAttrs': []},
                     ALL: {'requiredAttrs': []}},
    gitlab.Group: {SEARCH: {'requiredAttrs': ['query']}},
}


def _die(msg):
    sys.stderr.write(msg + "\n")
    sys.exit(1)


def _what_to_cls(what):
    return "".join([s.capitalize() for s in what.split("-")])


def _cls_to_what(cls):
    return camel_re.sub(r'\1-\2', cls.__name__).lower()


def _populate_sub_parser_by_class(cls, sub_parser):
    for action_name in ACTIONS:
        attr = 'can' + action_name.capitalize()
        if not getattr(cls, attr):
            continue
        sub_parser_action = sub_parser.add_parser(action_name)
        [sub_parser_action.add_argument("--%s" % x.replace('_', '-'),
                                        required=True)
         for x in cls.requiredUrlAttrs]
        sub_parser_action.add_argument("--sudo", required=False)

        if action_name == LIST:
            [sub_parser_action.add_argument("--%s" % x.replace('_', '-'),
                                            required=True)
             for x in cls.requiredListAttrs]
            sub_parser_action.add_argument("--page", required=False)
            sub_parser_action.add_argument("--per-page", required=False)

        elif action_name in [GET, DELETE]:
            if cls not in [gitlab.CurrentUser]:
                if cls.getRequiresId:
                    id_attr = cls.idAttr.replace('_', '-')
                    sub_parser_action.add_argument("--%s" % id_attr,
                                                   required=True)
                [sub_parser_action.add_argument("--%s" % x.replace('_', '-'),
                                                required=True)
                 for x in cls.requiredGetAttrs if x != cls.idAttr]

        elif action_name == CREATE:
            [sub_parser_action.add_argument("--%s" % x.replace('_', '-'),
                                            required=True)
             for x in cls.requiredCreateAttrs]
            [sub_parser_action.add_argument("--%s" % x.replace('_', '-'),
                                            required=False)
             for x in cls.optionalCreateAttrs]

        elif action_name == UPDATE:
            id_attr = cls.idAttr.replace('_', '-')
            sub_parser_action.add_argument("--%s" % id_attr,
                                           required=True)

            attrs = (cls.requiredUpdateAttrs
                     if (cls.requiredUpdateAttrs or cls.optionalUpdateAttrs)
                     else cls.requiredCreateAttrs)
            [sub_parser_action.add_argument("--%s" % x.replace('_', '-'),
                                            required=True)
             for x in attrs if x != cls.idAttr]

            attrs = (cls.optionalUpdateAttrs
                     if (cls.requiredUpdateAttrs or cls.optionalUpdateAttrs)
                     else cls.optionalCreateAttrs)
            [sub_parser_action.add_argument("--%s" % x.replace('_', '-'),
                                            required=False)
             for x in attrs]

    if cls in extra_actions:
        for action_name in sorted(extra_actions[cls]):
            sub_parser_action = sub_parser.add_parser(action_name)
            d = extra_actions[cls][action_name]
            [sub_parser_action.add_argument("--%s" % arg, required=True)
             for arg in d['requiredAttrs']]


def do_auth(gitlab_id, config_files):
    try:
        gl = gitlab.Gitlab.from_config(gitlab_id, config_files)
        gl.auth()
        return gl
    except Exception as e:
        _die(str(e))


def _get_id(cls, args):
    try:
        id = args.pop(cls.idAttr)
    except Exception:
        _die("Missing --%s argument" % cls.idAttr.replace('_', '-'))

    return id


def do_create(cls, gl, what, args):
    if not cls.canCreate:
        _die("%s objects can't be created" % what)

    try:
        o = cls.create(gl, args)
    except Exception as e:
        _die("Impossible to create object (%s)" % str(e))

    return o


def do_list(cls, gl, what, args):
    if not cls.canList:
        _die("%s objects can't be listed" % what)

    try:
        l = cls.list(gl, **args)
    except Exception as e:
        _die("Impossible to list objects (%s)" % str(e))

    return l


def do_get(cls, gl, what, args):
    if cls.canGet is False:
        _die("%s objects can't be retrieved" % what)

    id = None
    if cls not in [gitlab.CurrentUser] and cls.getRequiresId:
        id = _get_id(cls, args)

    try:
        o = cls.get(gl, id, **args)
    except Exception as e:
        _die("Impossible to get object (%s)" % str(e))

    return o


def do_delete(cls, gl, what, args):
    if not cls.canDelete:
        _die("%s objects can't be deleted" % what)

    id = args.pop(cls.idAttr)
    try:
        gl.delete(cls, id, **args)
    except Exception as e:
        _die("Impossible to destroy object (%s)" % str(e))


def do_update(cls, gl, what, args):
    if not cls.canUpdate:
        _die("%s objects can't be updated" % what)

    o = do_get(cls, gl, what, args)
    try:
        for k, v in args.items():
            o.__dict__[k] = v
        o.save()
    except Exception as e:
        _die("Impossible to update object (%s)" % str(e))

    return o


def do_group_search(gl, what, args):
    try:
        return gl.groups.search(args['query'])
    except Exception as e:
        _die("Impossible to search projects (%s)" % str(e))


def do_project_search(gl, what, args):
    try:
        return gl.projects.search(args['query'])
    except Exception as e:
        _die("Impossible to search projects (%s)" % str(e))


def do_project_all(gl, what, args):
    try:
        return gl.projects.all()
    except Exception as e:
        _die("Impossible to list all projects (%s)" % str(e))


def do_project_owned(gl, what, args):
    try:
        return gl.projects.owned()
    except Exception as e:
        _die("Impossible to list owned projects (%s)" % str(e))


def main():
    if "--version" in sys.argv:
        print(gitlab.__version__)
        exit(0)

    parser = argparse.ArgumentParser(
        description="GitLab API Command Line Interface")
    parser.add_argument("--version", help="Display the version.",
                        action="store_true")
    parser.add_argument("-v", "--verbose", "--fancy",
                        help="Verbose mode",
                        action="store_true")
    parser.add_argument("-c", "--config-file", action='append',
                        help=("Configuration file to use. Can be used "
                              "multiple times."))
    parser.add_argument("-g", "--gitlab",
                        help=("Which configuration section should "
                              "be used. If not defined, the default selection "
                              "will be used."),
                        required=False)

    subparsers = parser.add_subparsers(title='object', dest='what',
                                       help="Object to manipulate.")
    subparsers.required = True

    # populate argparse for all Gitlab Object
    classes = []
    for cls in gitlab.__dict__.values():
        try:
            if gitlab.GitlabObject in inspect.getmro(cls):
                classes.append(cls)
        except AttributeError:
            pass
    classes.sort(key=operator.attrgetter("__name__"))

    for cls in classes:
        arg_name = _cls_to_what(cls)
        object_group = subparsers.add_parser(arg_name)

        object_subparsers = object_group.add_subparsers(
            dest='action', help="Action to execute.")
        _populate_sub_parser_by_class(cls, object_subparsers)
        object_subparsers.required = True

    arg = parser.parse_args()
    args = arg.__dict__

    config_files = arg.config_file
    gitlab_id = arg.gitlab
    verbose = arg.verbose
    action = arg.action
    what = arg.what

    # Remove CLI behavior-related args
    args.pop("gitlab")
    args.pop("config_file")
    args.pop("verbose")
    args.pop("what")
    args.pop("action")

    cls = None
    try:
        cls = gitlab.__dict__[_what_to_cls(what)]
    except Exception:
        _die("Unknown object: %s" % what)

    gl = do_auth(gitlab_id, config_files)

    if action == CREATE or action == GET:
        o = globals()['do_%s' % action.lower()](cls, gl, what, args)
        o.display(verbose)

    elif action == LIST:
        for o in do_list(cls, gl, what, args):
            o.display(verbose)
            print("")

    elif action == DELETE or action == UPDATE:
        o = globals()['do_%s' % action.lower()](cls, gl, what, args)

    elif action == PROTECT or action == UNPROTECT:
        if cls != gitlab.ProjectBranch:
            _die("%s objects can't be protected" % what)

        o = do_get(cls, gl, what, args)
        getattr(o, action)()

    elif action == SEARCH:

        if cls == gitlab.Project:
            l = do_project_search(gl, what, args)
        elif cls == gitlab.Group:
            l = do_group_search(gl, what, args)
        else:
            _die("%s objects don't support this request" % what)

        for o in l:
            o.display(verbose)

    elif action == OWNED:
        if cls != gitlab.Project:
            _die("%s objects don't support this request" % what)

        for o in do_project_owned(gl, what, args):
            o.display(verbose)

    elif action == ALL:
        if cls != gitlab.Project:
            _die("%s objects don't support this request" % what)

        for o in do_project_all(gl, what, args):
            o.display(verbose)

    sys.exit(0)

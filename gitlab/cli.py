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
from __future__ import division
from __future__ import absolute_import
import argparse
import inspect
import operator
import re
import sys

import six

import gitlab

camel_re = re.compile('(.)([A-Z])')

EXTRA_ACTIONS = {
    gitlab.Group: {'search': {'required': ['query']}},
    gitlab.ProjectBranch: {'protect': {'required': ['id', 'project-id']},
                           'unprotect': {'required': ['id', 'project-id']}},
    gitlab.ProjectBuild: {'cancel': {'required': ['id', 'project-id']},
                          'retry': {'required': ['id', 'project-id']},
                          'artifacts': {'required': ['id', 'project-id']},
                          'trace': {'required': ['id', 'project-id']}},
    gitlab.ProjectCommit: {'diff': {'required': ['id', 'project-id']},
                           'blob': {'required': ['id', 'project-id',
                                                 'filepath']},
                           'builds': {'required': ['id', 'project-id']},
                           'cherrypick': {'required': ['id', 'project-id',
                                                       'branch']}},
    gitlab.ProjectIssue: {'subscribe': {'required': ['id', 'project-id']},
                          'unsubscribe': {'required': ['id', 'project-id']},
                          'move': {'required': ['id', 'project-id',
                                                'to-project-id']}},
    gitlab.ProjectMergeRequest: {
        'closes-issues': {'required': ['id', 'project-id']},
        'cancel': {'required': ['id', 'project-id']},
        'merge': {'required': ['id', 'project-id'],
                  'optional': ['merge-commit-message',
                               'should-remove-source-branch',
                               'merged-when-build-succeeds']}
    },
    gitlab.ProjectMilestone: {'issues': {'required': ['id', 'project-id']}},
    gitlab.Project: {'search': {'required': ['query']},
                     'owned': {},
                     'all': {'optional': [('all', bool)]},
                     'starred': {},
                     'star': {'required': ['id']},
                     'unstar': {'required': ['id']},
                     'archive': {'required': ['id']},
                     'unarchive': {'required': ['id']},
                     'share': {'required': ['id', 'group-id',
                                            'group-access']}},
    gitlab.User: {'block': {'required': ['id']},
                  'unblock': {'required': ['id']},
                  'search': {'required': ['query']},
                  'get-by-username': {'required': ['query']}},
}


def _die(msg, e=None):
    if e:
        msg = "%s (%s)" % (msg, e)
    sys.stderr.write(msg + "\n")
    sys.exit(1)


def _what_to_cls(what):
    return "".join([s.capitalize() for s in what.split("-")])


def _cls_to_what(cls):
    return camel_re.sub(r'\1-\2', cls.__name__).lower()


def do_auth(gitlab_id, config_files):
    try:
        gl = gitlab.Gitlab.from_config(gitlab_id, config_files)
        gl.auth()
        return gl
    except Exception as e:
        _die(str(e))


class GitlabCLI(object):
    def _get_id(self, cls, args):
        try:
            id = args.pop(cls.idAttr)
        except Exception:
            _die("Missing --%s argument" % cls.idAttr.replace('_', '-'))

        return id

    def do_create(self, cls, gl, what, args):
        if not cls.canCreate:
            _die("%s objects can't be created" % what)

        try:
            o = cls.create(gl, args)
        except Exception as e:
            _die("Impossible to create object", e)

        return o

    def do_list(self, cls, gl, what, args):
        if not cls.canList:
            _die("%s objects can't be listed" % what)

        try:
            l = cls.list(gl, **args)
        except Exception as e:
            _die("Impossible to list objects", e)

        return l

    def do_get(self, cls, gl, what, args):
        if cls.canGet is False:
            _die("%s objects can't be retrieved" % what)

        id = None
        if cls not in [gitlab.CurrentUser] and cls.getRequiresId:
            id = self._get_id(cls, args)

        try:
            o = cls.get(gl, id, **args)
        except Exception as e:
            _die("Impossible to get object", e)

        return o

    def do_delete(self, cls, gl, what, args):
        if not cls.canDelete:
            _die("%s objects can't be deleted" % what)

        id = args.pop(cls.idAttr)
        try:
            gl.delete(cls, id, **args)
        except Exception as e:
            _die("Impossible to destroy object", e)

    def do_update(self, cls, gl, what, args):
        if not cls.canUpdate:
            _die("%s objects can't be updated" % what)

        o = self.do_get(cls, gl, what, args)
        try:
            for k, v in args.items():
                o.__dict__[k] = v
            o.save()
        except Exception as e:
            _die("Impossible to update object", e)

        return o

    def do_group_search(self, cls, gl, what, args):
        try:
            return gl.groups.search(args['query'])
        except Exception as e:
            _die("Impossible to search projects", e)

    def do_project_search(self, cls, gl, what, args):
        try:
            return gl.projects.search(args['query'])
        except Exception as e:
            _die("Impossible to search projects", e)

    def do_project_all(self, cls, gl, what, args):
        try:
            return gl.projects.all(all=args.get('all', False))
        except Exception as e:
            _die("Impossible to list all projects", e)

    def do_project_starred(self, cls, gl, what, args):
        try:
            return gl.projects.starred()
        except Exception as e:
            _die("Impossible to list starred projects", e)

    def do_project_owned(self, cls, gl, what, args):
        try:
            return gl.projects.owned()
        except Exception as e:
            _die("Impossible to list owned projects", e)

    def do_project_star(self, cls, gl, what, args):
        try:
            o = self.do_get(cls, gl, what, args)
            o.star()
        except Exception as e:
            _die("Impossible to star project", e)

    def do_project_unstar(self, cls, gl, what, args):
        try:
            o = self.do_get(cls, gl, what, args)
            o.unstar()
        except Exception as e:
            _die("Impossible to unstar project", e)

    def do_project_archive(self, cls, gl, what, args):
        try:
            o = self.do_get(cls, gl, what, args)
            o.archive_()
        except Exception as e:
            _die("Impossible to archive project", e)

    def do_project_unarchive(self, cls, gl, what, args):
        try:
            o = self.do_get(cls, gl, what, args)
            o.unarchive_()
        except Exception as e:
            _die("Impossible to unarchive project", e)

    def do_project_share(self, cls, gl, what, args):
        try:
            o = self.do_get(cls, gl, what, args)
            o.share(args['group_id'], args['group_access'])
        except Exception as e:
            _die("Impossible to share project", e)

    def do_user_block(self, cls, gl, what, args):
        try:
            o = self.do_get(cls, gl, what, args)
            o.block()
        except Exception as e:
            _die("Impossible to block user", e)

    def do_user_unblock(self, cls, gl, what, args):
        try:
            o = self.do_get(cls, gl, what, args)
            o.unblock()
        except Exception as e:
            _die("Impossible to block user", e)

    def do_project_commit_diff(self, cls, gl, what, args):
        try:
            o = self.do_get(cls, gl, what, args)
            return [x['diff'] for x in o.diff()]
        except Exception as e:
            _die("Impossible to get commit diff", e)

    def do_project_commit_blob(self, cls, gl, what, args):
        try:
            o = self.do_get(cls, gl, what, args)
            return o.blob(args['filepath'])
        except Exception as e:
            _die("Impossible to get commit blob", e)

    def do_project_commit_builds(self, cls, gl, what, args):
        try:
            o = self.do_get(cls, gl, what, args)
            return o.builds()
        except Exception as e:
            _die("Impossible to get commit builds", e)

    def do_project_commit_cherrypick(self, cls, gl, what, args):
        try:
            o = self.do_get(cls, gl, what, args)
            o.cherry_pick(branch=args['branch'])
        except Exception as e:
            _die("Impossible to cherry-pick commit", e)

    def do_project_build_cancel(self, cls, gl, what, args):
        try:
            o = self.do_get(cls, gl, what, args)
            return o.cancel()
        except Exception as e:
            _die("Impossible to cancel project build", e)

    def do_project_build_retry(self, cls, gl, what, args):
        try:
            o = self.do_get(cls, gl, what, args)
            return o.retry()
        except Exception as e:
            _die("Impossible to retry project build", e)

    def do_project_build_artifacts(self, cls, gl, what, args):
        try:
            o = self.do_get(cls, gl, what, args)
            return o.artifacts()
        except Exception as e:
            _die("Impossible to get project build artifacts", e)

    def do_project_build_trace(self, cls, gl, what, args):
        try:
            o = self.do_get(cls, gl, what, args)
            return o.trace()
        except Exception as e:
            _die("Impossible to get project build trace", e)

    def do_project_issue_subscribe(self, cls, gl, what, args):
        try:
            o = self.do_get(cls, gl, what, args)
            o.subscribe()
        except Exception as e:
            _die("Impossible to subscribe to issue", e)

    def do_project_issue_unsubscribe(self, cls, gl, what, args):
        try:
            o = self.do_get(cls, gl, what, args)
            o.unsubscribe()
        except Exception as e:
            _die("Impossible to subscribe to issue", e)

    def do_project_issue_move(self, cls, gl, what, args):
        try:
            o = self.do_get(cls, gl, what, args)
            o.move(args['to_project_id'])
        except Exception as e:
            _die("Impossible to move issue", e)

    def do_project_merge_request_closesissues(self, cls, gl, what, args):
        try:
            o = self.do_get(cls, gl, what, args)
            return o.closes_issues()
        except Exception as e:
            _die("Impossible to list issues closed by merge request", e)

    def do_project_merge_request_cancel(self, cls, gl, what, args):
        try:
            o = self.do_get(cls, gl, what, args)
            return o.cancel_merge_when_build_succeeds()
        except Exception as e:
            _die("Impossible to cancel merge request", e)

    def do_project_merge_request_merge(self, cls, gl, what, args):
        try:
            o = self.do_get(cls, gl, what, args)
            should_remove = args.get('should_remove_source_branch', False)
            build_succeeds = args.get('merged_when_build_succeeds', False)
            return o.merge(
                merge_commit_message=args.get('merge_commit_message', ''),
                should_remove_source_branch=should_remove,
                merged_when_build_succeeds=build_succeeds)
        except Exception as e:
            _die("Impossible to validate merge request", e)

    def do_project_milestone_issues(self, cls, gl, what, args):
        try:
            o = self.do_get(cls, gl, what, args)
            return o.issues()
        except Exception as e:
            _die("Impossible to get milestone issues", e)

    def do_user_search(self, cls, gl, what, args):
        try:
            return gl.users.search(args['query'])
        except Exception as e:
            _die("Impossible to search users", e)

    def do_user_getbyusername(self, cls, gl, what, args):
        try:
            return gl.users.search(args['query'])
        except Exception as e:
            _die("Impossible to get user %s" % args['query'], e)


def _populate_sub_parser_by_class(cls, sub_parser):
    for action_name in ['list', 'get', 'create', 'update', 'delete']:
        attr = 'can' + action_name.capitalize()
        if not getattr(cls, attr):
            continue
        sub_parser_action = sub_parser.add_parser(action_name)
        [sub_parser_action.add_argument("--%s" % x.replace('_', '-'),
                                        required=True)
         for x in cls.requiredUrlAttrs]
        sub_parser_action.add_argument("--sudo", required=False)

        if action_name == "list":
            [sub_parser_action.add_argument("--%s" % x.replace('_', '-'),
                                            required=True)
             for x in cls.requiredListAttrs]
            sub_parser_action.add_argument("--page", required=False)
            sub_parser_action.add_argument("--per-page", required=False)
            sub_parser_action.add_argument("--all", required=False,
                                           action='store_true')

        if action_name in ["get", "delete"]:
            if cls not in [gitlab.CurrentUser]:
                if cls.getRequiresId:
                    id_attr = cls.idAttr.replace('_', '-')
                    sub_parser_action.add_argument("--%s" % id_attr,
                                                   required=True)
                [sub_parser_action.add_argument("--%s" % x.replace('_', '-'),
                                                required=True)
                 for x in cls.requiredGetAttrs if x != cls.idAttr]

        if action_name == "get":
            [sub_parser_action.add_argument("--%s" % x.replace('_', '-'),
                                            required=False)
             for x in cls.optionalGetAttrs]

        if action_name == "list":
            [sub_parser_action.add_argument("--%s" % x.replace('_', '-'),
                                            required=False)
             for x in cls.optionalListAttrs]

        if action_name == "create":
            [sub_parser_action.add_argument("--%s" % x.replace('_', '-'),
                                            required=True)
             for x in cls.requiredCreateAttrs]
            [sub_parser_action.add_argument("--%s" % x.replace('_', '-'),
                                            required=False)
             for x in cls.optionalCreateAttrs]

        if action_name == "update":
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

    if cls in EXTRA_ACTIONS:
        def _add_arg(parser, required, data):
            extra_args = {}
            if isinstance(data, tuple):
                if data[1] is bool:
                    extra_args = {'action': 'store_true'}
                data = data[0]

            parser.add_argument("--%s" % data, required=required, **extra_args)

        for action_name in sorted(EXTRA_ACTIONS[cls]):
            sub_parser_action = sub_parser.add_parser(action_name)
            d = EXTRA_ACTIONS[cls][action_name]
            [_add_arg(sub_parser_action, True, arg)
             for arg in d.get('required', [])]
            [_add_arg(sub_parser_action, False, arg)
             for arg in d.get('optional', [])]


def _build_parser(args=sys.argv[1:]):
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

    return parser


def _parse_args(args=sys.argv[1:]):
    parser = _build_parser()
    return parser.parse_args(args)


def main():
    if "--version" in sys.argv:
        print(gitlab.__version__)
        exit(0)

    arg = _parse_args()
    args = arg.__dict__

    config_files = arg.config_file
    gitlab_id = arg.gitlab
    verbose = arg.verbose
    action = arg.action
    what = arg.what

    # Remove CLI behavior-related args
    for item in ("gitlab", "config_file", "verbose", "what", "action",
                 "version"):
        args.pop(item)

    args = {k: v for k, v in args.items() if v is not None}

    cls = None
    try:
        cls = gitlab.__dict__[_what_to_cls(what)]
    except Exception:
        _die("Unknown object: %s" % what)

    gl = do_auth(gitlab_id, config_files)

    cli = GitlabCLI()
    method = None
    what = what.replace('-', '_')
    action = action.lower().replace('-', '')
    for test in ["do_%s_%s" % (what, action),
                 "do_%s" % action]:
        if hasattr(cli, test):
            method = test
            break

    if method is None:
        sys.stderr.write("Don't know how to deal with this!\n")
        sys.exit(1)

    ret_val = getattr(cli, method)(cls, gl, what, args)

    if isinstance(ret_val, list):
        for o in ret_val:
            if isinstance(o, gitlab.GitlabObject):
                o.display(verbose)
                print("")
            else:
                print(o)
    elif isinstance(ret_val, gitlab.GitlabObject):
        ret_val.display(verbose)
    elif isinstance(ret_val, six.string_types):
        print(ret_val)

    sys.exit(0)

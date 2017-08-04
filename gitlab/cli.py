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
from __future__ import absolute_import
import argparse
import importlib
import re
import sys

import gitlab.config

camel_re = re.compile('(.)([A-Z])')


def die(msg, e=None):
    if e:
        msg = "%s (%s)" % (msg, e)
    sys.stderr.write(msg + "\n")
    sys.exit(1)


def what_to_cls(what):
    return "".join([s.capitalize() for s in what.split("-")])


def cls_to_what(cls):
    return camel_re.sub(r'\1-\2', cls.__name__).lower()


def _get_base_parser():
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

    return parser


def _get_parser(cli_module):
    parser = _get_base_parser()
    return cli_module.extend_parser(parser)


def main():
    if "--version" in sys.argv:
        print(gitlab.__version__)
        exit(0)

    parser = _get_base_parser()
    (options, args) = parser.parse_known_args(sys.argv)

    config = gitlab.config.GitlabConfigParser(options.gitlab,
                                              options.config_file)
    cli_module = importlib.import_module('gitlab.v%s.cli' % config.api_version)
    parser = _get_parser(cli_module)
    args = parser.parse_args(sys.argv[1:])
    config_files = args.config_file
    gitlab_id = args.gitlab
    verbose = args.verbose
    action = args.action
    what = args.what

    args = args.__dict__
    # Remove CLI behavior-related args
    for item in ('gitlab', 'config_file', 'verbose', 'what', 'action',
                 'version'):
        args.pop(item)
    args = {k: v for k, v in args.items() if v is not None}

    try:
        gl = gitlab.Gitlab.from_config(gitlab_id, config_files)
        gl.auth()
    except Exception as e:
        die(str(e))

    cli_module.run(gl, what, action, args, verbose)

    sys.exit(0)

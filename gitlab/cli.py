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
import functools
import re
import sys
from typing import Any, Callable, Dict, Optional, Tuple, Union

import gitlab.config

camel_re = re.compile("(.)([A-Z])")

# custom_actions = {
#    cls: {
#        action: (mandatory_args, optional_args, in_obj),
#    },
# }
custom_actions: Dict[str, Dict[str, Tuple[Tuple[str, ...], Tuple[str, ...], bool]]] = {}


def register_custom_action(
    cls_names: Union[str, Tuple[str, ...]],
    mandatory: Tuple[str, ...] = tuple(),
    optional: Tuple[str, ...] = tuple(),
) -> Callable:
    def wrap(f: Callable) -> Callable:
        @functools.wraps(f)
        def wrapped_f(*args, **kwargs):
            return f(*args, **kwargs)

        # in_obj defines whether the method belongs to the obj or the manager
        in_obj = True
        if isinstance(cls_names, tuple):
            classes = cls_names
        else:
            classes = (cls_names,)

        for cls_name in classes:
            final_name = cls_name
            if cls_name.endswith("Manager"):
                final_name = cls_name.replace("Manager", "")
                in_obj = False
            if final_name not in custom_actions:
                custom_actions[final_name] = {}

            action = f.__name__.replace("_", "-")
            custom_actions[final_name][action] = (mandatory, optional, in_obj)

        return wrapped_f

    return wrap


def die(msg: str, e: Optional[Exception] = None) -> None:
    if e:
        msg = "%s (%s)" % (msg, e)
    sys.stderr.write(msg + "\n")
    sys.exit(1)


def what_to_cls(what: str) -> str:
    return "".join([s.capitalize() for s in what.split("-")])


def cls_to_what(cls: Any) -> str:
    return camel_re.sub(r"\1-\2", cls.__name__).lower()


def _get_base_parser(add_help: bool = True) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        add_help=add_help, description="GitLab API Command Line Interface"
    )
    parser.add_argument("--version", help="Display the version.", action="store_true")
    parser.add_argument(
        "-v",
        "--verbose",
        "--fancy",
        help="Verbose mode (legacy format only)",
        action="store_true",
    )
    parser.add_argument(
        "-d", "--debug", help="Debug mode (display HTTP requests)", action="store_true"
    )
    parser.add_argument(
        "-c",
        "--config-file",
        action="append",
        help="Configuration file to use. Can be used multiple times.",
    )
    parser.add_argument(
        "-g",
        "--gitlab",
        help=(
            "Which configuration section should "
            "be used. If not defined, the default selection "
            "will be used."
        ),
        required=False,
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Output format (v4 only): json|legacy|yaml",
        required=False,
        choices=["json", "legacy", "yaml"],
        default="legacy",
    )
    parser.add_argument(
        "-f",
        "--fields",
        help=(
            "Fields to display in the output (comma "
            "separated). Not used with legacy output"
        ),
        required=False,
    )

    return parser


def _get_parser(cli_module):
    parser = _get_base_parser()
    return cli_module.extend_parser(parser)


def _parse_value(v):
    if isinstance(v, str) and v.startswith("@"):
        # If the user-provided value starts with @, we try to read the file
        # path provided after @ as the real value. Exit on any error.
        try:
            with open(v[1:]) as fl:
                return fl.read()
        except Exception as e:
            sys.stderr.write("%s\n" % e)
            sys.exit(1)

    return v


def docs() -> argparse.ArgumentParser:
    """
    Provide a statically generated parser for sphinx only, so we don't need
    to provide dummy gitlab config for readthedocs.
    """
    if "sphinx" not in sys.modules:
        sys.exit("Docs parser is only intended for build_sphinx")

    parser = _get_base_parser(add_help=False)
    # NOTE: We must delay import of gitlab.v4.cli until now or
    # otherwise it will cause circular import errors
    import gitlab.v4.cli

    return _get_parser(gitlab.v4.cli)


def main():
    # NOTE: We must delay import of gitlab.v4.cli until now or
    # otherwise it will cause circular import errors
    import gitlab.v4.cli

    if "--version" in sys.argv:
        print(gitlab.__version__)
        sys.exit(0)

    parser = _get_base_parser(add_help=False)

    # This first parsing step is used to find the gitlab config to use, and
    # load the propermodule (v3 or v4) accordingly. At that point we don't have
    # any subparser setup
    (options, args) = parser.parse_known_args(sys.argv)
    try:
        config = gitlab.config.GitlabConfigParser(options.gitlab, options.config_file)
    except gitlab.config.ConfigError as e:
        if "--help" in sys.argv or "-h" in sys.argv:
            parser.print_help()
            sys.exit(0)
        sys.exit(e)
    # We only support v4 API at this time
    if config.api_version not in ("4",):
        raise ModuleNotFoundError(name="gitlab.v%s.cli" % config.api_version)

    # Now we build the entire set of subcommands and do the complete parsing
    parser = _get_parser(gitlab.v4.cli)
    try:
        import argcomplete  # type: ignore

        argcomplete.autocomplete(parser)
    except Exception:
        pass
    args = parser.parse_args(sys.argv[1:])

    config_files = args.config_file
    gitlab_id = args.gitlab
    verbose = args.verbose
    output = args.output
    fields = []
    if args.fields:
        fields = [x.strip() for x in args.fields.split(",")]
    debug = args.debug
    action = args.whaction
    what = args.what

    args = args.__dict__
    # Remove CLI behavior-related args
    for item in (
        "gitlab",
        "config_file",
        "verbose",
        "debug",
        "what",
        "whaction",
        "version",
        "output",
    ):
        args.pop(item)
    args = {k: _parse_value(v) for k, v in args.items() if v is not None}

    try:
        gl = gitlab.Gitlab.from_config(gitlab_id, config_files)
        if gl.private_token or gl.oauth_token or gl.job_token:
            gl.auth()
    except Exception as e:
        die(str(e))

    if debug:
        gl.enable_debug()

    gitlab.v4.cli.run(gl, what, action, args, verbose, output, fields)

    sys.exit(0)

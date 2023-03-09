import argparse
import functools
import os
import re
import sys
from types import ModuleType
from typing import (
    Any,
    Callable,
    cast,
    Dict,
    Optional,
    Tuple,
    Type,
    TYPE_CHECKING,
    TypeVar,
    Union,
)

from requests.structures import CaseInsensitiveDict

import gitlab.config
from gitlab.base import RESTObject

# This regex is based on:
# https://github.com/jpvanhal/inflection/blob/master/inflection/__init__.py
camel_upperlower_regex = re.compile(r"([A-Z]+)([A-Z][a-z])")
camel_lowerupper_regex = re.compile(r"([a-z\d])([A-Z])")

# custom_actions = {
#    cls: {
#        action: (mandatory_args, optional_args, in_obj),
#    },
# }
custom_actions: Dict[str, Dict[str, Tuple[Tuple[str, ...], Tuple[str, ...], bool]]] = {}


# For an explanation of how these type-hints work see:
# https://mypy.readthedocs.io/en/stable/generics.html#declaring-decorators
#
# The goal here is that functions which get decorated will retain their types.
__F = TypeVar("__F", bound=Callable[..., Any])


class VerticalHelpFormatter(argparse.HelpFormatter):
    def format_help(self) -> str:
        result = super().format_help()
        output = ""
        indent = self._indent_increment * " "
        for line in result.splitlines(keepends=True):
            # All of our resources are on one line and wrapped inside braces.
            # For example: {application,resource1,resource2}
            # We then put each resource on its own line to make it easier to read.
            if line.strip().startswith("{"):
                choices = line.strip().strip("{}").split(",")
                choices_str = f"\n{indent}".join(choices)
                line = f"{indent}{choices_str}\n"
            output += line
        return output


def register_custom_action(
    cls_names: Union[str, Tuple[str, ...]],
    mandatory: Tuple[str, ...] = (),
    optional: Tuple[str, ...] = (),
    custom_action: Optional[str] = None,
) -> Callable[[__F], __F]:
    def wrap(f: __F) -> __F:
        @functools.wraps(f)
        def wrapped_f(*args: Any, **kwargs: Any) -> Any:
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

            action = custom_action or f.__name__.replace("_", "-")
            custom_actions[final_name][action] = (mandatory, optional, in_obj)

        return cast(__F, wrapped_f)

    return wrap


def die(msg: str, e: Optional[Exception] = None) -> None:
    if e:
        msg = f"{msg} ({e})"
    sys.stderr.write(f"{msg}\n")
    sys.exit(1)


def gitlab_resource_to_cls(
    gitlab_resource: str, namespace: ModuleType
) -> Type[RESTObject]:
    classes = CaseInsensitiveDict(namespace.__dict__)
    lowercase_class = gitlab_resource.replace("-", "")
    class_type = classes[lowercase_class]
    if TYPE_CHECKING:
        assert isinstance(class_type, type)
        assert issubclass(class_type, RESTObject)
    return class_type


def cls_to_gitlab_resource(cls: RESTObject) -> str:
    dasherized_uppercase = camel_upperlower_regex.sub(r"\1-\2", cls.__name__)
    dasherized_lowercase = camel_lowerupper_regex.sub(r"\1-\2", dasherized_uppercase)
    return dasherized_lowercase.lower()


def _get_base_parser(add_help: bool = True) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        add_help=add_help,
        description="GitLab API Command Line Interface",
        formatter_class=VerticalHelpFormatter,
        allow_abbrev=False,
    )
    parser.add_argument("--version", help="Display the version.", action="store_true")
    parser.add_argument(
        "-v",
        "--verbose",
        "--fancy",
        help="Verbose mode (legacy format only) [env var: GITLAB_VERBOSE]",
        action="store_true",
        default=os.getenv("GITLAB_VERBOSE"),
    )
    parser.add_argument(
        "-d",
        "--debug",
        help="Debug mode (display HTTP requests) [env var: GITLAB_DEBUG]",
        action="store_true",
        default=os.getenv("GITLAB_DEBUG"),
    )
    parser.add_argument(
        "-c",
        "--config-file",
        action="append",
        help=(
            "Configuration file to use. Can be used multiple times. "
            "[env var: PYTHON_GITLAB_CFG]"
        ),
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
    parser.add_argument(
        "--server-url",
        help=("GitLab server URL [env var: GITLAB_URL]"),
        required=False,
        default=os.getenv("GITLAB_URL"),
    )
    parser.add_argument(
        "--ssl-verify",
        help=(
            "Whether SSL certificates should be validated. [env var: GITLAB_SSL_VERIFY]"
        ),
        required=False,
        default=os.getenv("GITLAB_SSL_VERIFY"),
    )
    parser.add_argument(
        "--timeout",
        help=(
            "Timeout to use for requests to the GitLab server. "
            "[env var: GITLAB_TIMEOUT]"
        ),
        required=False,
        type=int,
        default=os.getenv("GITLAB_TIMEOUT"),
    )
    parser.add_argument(
        "--api-version",
        help=("GitLab API version [env var: GITLAB_API_VERSION]"),
        required=False,
        default=os.getenv("GITLAB_API_VERSION"),
    )
    parser.add_argument(
        "--per-page",
        help=(
            "Number of entries to return per page in the response. "
            "[env var: GITLAB_PER_PAGE]"
        ),
        required=False,
        type=int,
        default=os.getenv("GITLAB_PER_PAGE"),
    )
    parser.add_argument(
        "--pagination",
        help=(
            "Whether to use keyset or offset pagination [env var: GITLAB_PAGINATION]"
        ),
        required=False,
        default=os.getenv("GITLAB_PAGINATION"),
    )
    parser.add_argument(
        "--order-by",
        help=("Set order_by globally [env var: GITLAB_ORDER_BY]"),
        required=False,
        default=os.getenv("GITLAB_ORDER_BY"),
    )
    parser.add_argument(
        "--user-agent",
        help=(
            "The user agent to send to GitLab with the HTTP request. "
            "[env var: GITLAB_USER_AGENT]"
        ),
        required=False,
        default=os.getenv("GITLAB_USER_AGENT"),
    )

    tokens = parser.add_mutually_exclusive_group()
    tokens.add_argument(
        "--private-token",
        help=("GitLab private access token [env var: GITLAB_PRIVATE_TOKEN]"),
        required=False,
        default=os.getenv("GITLAB_PRIVATE_TOKEN"),
    )
    tokens.add_argument(
        "--oauth-token",
        help=("GitLab OAuth token [env var: GITLAB_OAUTH_TOKEN]"),
        required=False,
        default=os.getenv("GITLAB_OAUTH_TOKEN"),
    )
    tokens.add_argument(
        "--job-token",
        help=("GitLab CI job token [env var: CI_JOB_TOKEN]"),
        required=False,
    )
    return parser


def _get_parser() -> argparse.ArgumentParser:
    # NOTE: We must delay import of gitlab.v4.cli until now or
    # otherwise it will cause circular import errors
    from gitlab.v4 import cli as v4_cli

    parser = _get_base_parser()
    return v4_cli.extend_parser(parser)


def _parse_value(v: Any) -> Any:
    if isinstance(v, str) and v.startswith("@@"):
        return v[1:]
    if isinstance(v, str) and v.startswith("@"):
        # If the user-provided value starts with @, we try to read the file
        # path provided after @ as the real value. Exit on any error.
        try:
            with open(v[1:], encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            sys.stderr.write(f"{e}\n")
            sys.exit(1)

    return v


def docs() -> argparse.ArgumentParser:  # pragma: no cover
    """
    Provide a statically generated parser for sphinx only, so we don't need
    to provide dummy gitlab config for readthedocs.
    """
    if "sphinx" not in sys.modules:
        sys.exit("Docs parser is only intended for build_sphinx")

    return _get_parser()


def main() -> None:
    if "--version" in sys.argv:
        print(gitlab.__version__)
        sys.exit(0)

    parser = _get_base_parser(add_help=False)

    # This first parsing step is used to find the gitlab config to use, and
    # load the propermodule (v3 or v4) accordingly. At that point we don't have
    # any subparser setup
    (options, _) = parser.parse_known_args(sys.argv)
    try:
        config = gitlab.config.GitlabConfigParser(options.gitlab, options.config_file)
    except gitlab.config.ConfigError as e:
        if "--help" in sys.argv or "-h" in sys.argv:
            parser.print_help()
            sys.exit(0)
        sys.exit(str(e))
    # We only support v4 API at this time
    if config.api_version not in ("4",):  # dead code # pragma: no cover
        raise ModuleNotFoundError(f"gitlab.v{config.api_version}.cli")

    # Now we build the entire set of subcommands and do the complete parsing
    parser = _get_parser()
    try:
        import argcomplete  # type: ignore

        argcomplete.autocomplete(parser)  # pragma: no cover
    except Exception:
        pass
    args = parser.parse_args()

    config_files = args.config_file
    gitlab_id = args.gitlab
    verbose = args.verbose
    output = args.output
    fields = []
    if args.fields:
        fields = [x.strip() for x in args.fields.split(",")]
    debug = args.debug
    gitlab_resource = args.gitlab_resource
    resource_action = args.resource_action

    args_dict = vars(args)
    # Remove CLI behavior-related args
    for item in (
        "gitlab",
        "config_file",
        "verbose",
        "debug",
        "gitlab_resource",
        "resource_action",
        "version",
        "output",
        "fields",
        "server_url",
        "ssl_verify",
        "timeout",
        "api_version",
        "pagination",
        "user_agent",
        "private_token",
        "oauth_token",
        "job_token",
    ):
        args_dict.pop(item)
    args_dict = {k: _parse_value(v) for k, v in args_dict.items() if v is not None}

    try:
        gl = gitlab.Gitlab.merge_config(vars(options), gitlab_id, config_files)
        if debug:
            gl.enable_debug()
        if gl.private_token or gl.oauth_token:
            gl.auth()
    except Exception as e:
        die(str(e))

    gitlab.v4.cli.run(
        gl, gitlab_resource, resource_action, args_dict, verbose, output, fields
    )

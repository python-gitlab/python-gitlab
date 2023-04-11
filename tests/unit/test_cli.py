import argparse
import io
import os
import sys
import tempfile
from contextlib import redirect_stderr  # noqa: H302
from unittest import mock

import pytest

import gitlab.base
from gitlab import cli
from gitlab.exceptions import GitlabError
from gitlab.v4 import cli as v4_cli


@pytest.mark.parametrize(
    "gitlab_resource,expected_class",
    [
        ("class", "Class"),
        ("test-class", "TestClass"),
        ("test-longer-class", "TestLongerClass"),
        ("current-user-gpg-key", "CurrentUserGPGKey"),
        ("user-gpg-key", "UserGPGKey"),
        ("ldap-group", "LDAPGroup"),
    ],
)
def test_gitlab_resource_to_cls(gitlab_resource, expected_class):
    def _namespace():
        pass

    ExpectedClass = type(expected_class, (gitlab.base.RESTObject,), {})
    _namespace.__dict__[expected_class] = ExpectedClass

    assert cli.gitlab_resource_to_cls(gitlab_resource, _namespace) == ExpectedClass


@pytest.mark.parametrize(
    "class_name,expected_gitlab_resource",
    [
        ("Class", "class"),
        ("TestClass", "test-class"),
        ("TestUPPERCASEClass", "test-uppercase-class"),
        ("UPPERCASETestClass", "uppercase-test-class"),
        ("CurrentUserGPGKey", "current-user-gpg-key"),
        ("UserGPGKey", "user-gpg-key"),
        ("LDAPGroup", "ldap-group"),
    ],
)
def test_cls_to_gitlab_resource(class_name, expected_gitlab_resource):
    TestClass = type(class_name, (), {})

    assert cli.cls_to_gitlab_resource(TestClass) == expected_gitlab_resource


@pytest.mark.parametrize(
    "message,error,expected",
    [
        ("foobar", None, "foobar\n"),
        ("foo", GitlabError("bar"), "foo (bar)\n"),
    ],
)
def test_die(message, error, expected):
    fl = io.StringIO()
    with redirect_stderr(fl):
        with pytest.raises(SystemExit) as test:
            cli.die(message, error)
    assert fl.getvalue() == expected
    assert test.value.code == 1


def test_parse_value():
    ret = cli._parse_value("foobar")
    assert ret == "foobar"

    ret = cli._parse_value(True)
    assert ret is True

    ret = cli._parse_value(1)
    assert ret == 1

    ret = cli._parse_value(None)
    assert ret is None

    fd, temp_path = tempfile.mkstemp()
    os.write(fd, b"content")
    os.close(fd)
    ret = cli._parse_value(f"@{temp_path}")
    assert ret == "content"
    os.unlink(temp_path)

    fl = io.StringIO()
    with redirect_stderr(fl):
        with pytest.raises(SystemExit) as exc:
            cli._parse_value("@/thisfileprobablydoesntexist")
        assert (
            fl.getvalue() == "[Errno 2] No such file or directory:"
            " '/thisfileprobablydoesntexist'\n"
        )
        assert exc.value.code == 1


def test_base_parser():
    parser = cli._get_base_parser()
    args = parser.parse_args(["-v", "-g", "gl_id", "-c", "foo.cfg", "-c", "bar.cfg"])
    assert args.verbose
    assert args.gitlab == "gl_id"
    assert args.config_file == ["foo.cfg", "bar.cfg"]


def test_v4_parse_args():
    parser = cli._get_parser()
    args = parser.parse_args(["project", "list"])
    assert args.gitlab_resource == "project"
    assert args.resource_action == "list"


def test_v4_parser():
    parser = cli._get_parser()
    subparsers = next(
        action
        for action in parser._actions
        if isinstance(action, argparse._SubParsersAction)
    )
    assert subparsers is not None
    assert "project" in subparsers.choices

    user_subparsers = next(
        action
        for action in subparsers.choices["project"]._actions
        if isinstance(action, argparse._SubParsersAction)
    )
    assert user_subparsers is not None
    assert "list" in user_subparsers.choices
    assert "get" in user_subparsers.choices
    assert "delete" in user_subparsers.choices
    assert "update" in user_subparsers.choices
    assert "create" in user_subparsers.choices
    assert "archive" in user_subparsers.choices
    assert "unarchive" in user_subparsers.choices

    actions = user_subparsers.choices["create"]._option_string_actions
    assert not actions["--description"].required

    user_subparsers = next(
        action
        for action in subparsers.choices["group"]._actions
        if isinstance(action, argparse._SubParsersAction)
    )
    actions = user_subparsers.choices["create"]._option_string_actions
    assert actions["--name"].required


@pytest.mark.skipif(sys.version_info < (3, 8), reason="added in 3.8")
def test_legacy_display_without_fields_warns(fake_object_no_id):
    printer = v4_cli.LegacyPrinter()

    with mock.patch("builtins.print") as mocked:
        printer.display(fake_object_no_id, obj=fake_object_no_id)

    assert "No default fields to show" in mocked.call_args.args[0]


@pytest.mark.skipif(sys.version_info < (3, 8), reason="added in 3.8")
def test_legacy_display_with_long_repr_truncates(fake_object_long_repr):
    printer = v4_cli.LegacyPrinter()

    with mock.patch("builtins.print") as mocked:
        printer.display(fake_object_long_repr, obj=fake_object_long_repr)

    assert len(mocked.call_args.args[0]) < 80

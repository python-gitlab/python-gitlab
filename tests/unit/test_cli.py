#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2016-2017 Gauvain Pocentek <gauvain@pocentek.net>
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
import io
import os
import tempfile
from contextlib import redirect_stderr  # noqa: H302

import pytest

from gitlab import cli


@pytest.mark.parametrize(
    "what,expected_class",
    [
        ("class", "Class"),
        ("test-class", "TestClass"),
        ("test-longer-class", "TestLongerClass"),
        ("current-user-gpg-key", "CurrentUserGPGKey"),
        ("user-gpg-key", "UserGPGKey"),
        ("ldap-group", "LDAPGroup"),
    ],
)
def test_what_to_cls(what, expected_class):
    def _namespace():
        pass

    ExpectedClass = type(expected_class, (), {})
    _namespace.__dict__[expected_class] = ExpectedClass

    assert cli.what_to_cls(what, _namespace) == ExpectedClass


@pytest.mark.parametrize(
    "class_name,expected_what",
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
def test_cls_to_what(class_name, expected_what):
    TestClass = type(class_name, (), {})

    assert cli.cls_to_what(TestClass) == expected_what


def test_die():
    fl = io.StringIO()
    with redirect_stderr(fl):
        with pytest.raises(SystemExit) as test:
            cli.die("foobar")
    assert fl.getvalue() == "foobar\n"
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
    assert args.what == "project"
    assert args.whaction == "list"


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

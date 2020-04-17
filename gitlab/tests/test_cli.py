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
import os
import tempfile
import io

from contextlib import redirect_stderr  # noqa: H302

import pytest

from gitlab import cli
import gitlab.v4.cli


def test_what_to_cls():
    assert "Foo" == cli.what_to_cls("foo")
    assert "FooBar" == cli.what_to_cls("foo-bar")


def test_cls_to_what():
    class Class(object):
        pass

    class TestClass(object):
        pass

    assert "test-class" == cli.cls_to_what(TestClass)
    assert "class" == cli.cls_to_what(Class)


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
    ret = cli._parse_value("@%s" % temp_path)
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
    parser = cli._get_parser(gitlab.v4.cli)
    args = parser.parse_args(["project", "list"])
    assert args.what == "project"
    assert args.whaction == "list"


def test_v4_parser():
    parser = cli._get_parser(gitlab.v4.cli)
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

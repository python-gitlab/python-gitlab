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

from __future__ import print_function
from __future__ import absolute_import

import argparse
import os
import tempfile

try:
    from contextlib import redirect_stderr  # noqa: H302
except ImportError:
    from contextlib import contextmanager  # noqa: H302
    import sys

    @contextmanager
    def redirect_stderr(new_target):
        old_target, sys.stderr = sys.stderr, new_target
        yield
        sys.stderr = old_target


try:
    import unittest
except ImportError:
    import unittest2 as unittest

import six

from gitlab import cli
import gitlab.v4.cli


class TestCLI(unittest.TestCase):
    def test_what_to_cls(self):
        self.assertEqual("Foo", cli.what_to_cls("foo"))
        self.assertEqual("FooBar", cli.what_to_cls("foo-bar"))

    def test_cls_to_what(self):
        class Class(object):
            pass

        class TestClass(object):
            pass

        self.assertEqual("test-class", cli.cls_to_what(TestClass))
        self.assertEqual("class", cli.cls_to_what(Class))

    def test_die(self):
        fl = six.StringIO()
        with redirect_stderr(fl):
            with self.assertRaises(SystemExit) as test:
                cli.die("foobar")
        self.assertEqual(fl.getvalue(), "foobar\n")
        self.assertEqual(test.exception.code, 1)

    def test_parse_value(self):
        ret = cli._parse_value("foobar")
        self.assertEqual(ret, "foobar")

        ret = cli._parse_value(True)
        self.assertEqual(ret, True)

        ret = cli._parse_value(1)
        self.assertEqual(ret, 1)

        ret = cli._parse_value(None)
        self.assertEqual(ret, None)

        fd, temp_path = tempfile.mkstemp()
        os.write(fd, b"content")
        os.close(fd)
        ret = cli._parse_value("@%s" % temp_path)
        self.assertEqual(ret, "content")
        os.unlink(temp_path)

        fl = six.StringIO()
        with redirect_stderr(fl):
            with self.assertRaises(SystemExit) as exc:
                cli._parse_value("@/thisfileprobablydoesntexist")
            self.assertEqual(
                fl.getvalue(),
                "[Errno 2] No such file or directory:"
                " '/thisfileprobablydoesntexist'\n",
            )
            self.assertEqual(exc.exception.code, 1)

    def test_base_parser(self):
        parser = cli._get_base_parser()
        args = parser.parse_args(
            ["-v", "-g", "gl_id", "-c", "foo.cfg", "-c", "bar.cfg"]
        )
        self.assertTrue(args.verbose)
        self.assertEqual(args.gitlab, "gl_id")
        self.assertEqual(args.config_file, ["foo.cfg", "bar.cfg"])


class TestV4CLI(unittest.TestCase):
    def test_parse_args(self):
        parser = cli._get_parser(gitlab.v4.cli)
        args = parser.parse_args(["project", "list"])
        self.assertEqual(args.what, "project")
        self.assertEqual(args.action, "list")

    def test_parser(self):
        parser = cli._get_parser(gitlab.v4.cli)
        subparsers = None
        for action in parser._actions:
            if type(action) == argparse._SubParsersAction:
                subparsers = action
                break
        self.assertIsNotNone(subparsers)
        self.assertIn("project", subparsers.choices)

        user_subparsers = None
        for action in subparsers.choices["project"]._actions:
            if type(action) == argparse._SubParsersAction:
                user_subparsers = action
                break
        self.assertIsNotNone(user_subparsers)
        self.assertIn("list", user_subparsers.choices)
        self.assertIn("get", user_subparsers.choices)
        self.assertIn("delete", user_subparsers.choices)
        self.assertIn("update", user_subparsers.choices)
        self.assertIn("create", user_subparsers.choices)
        self.assertIn("archive", user_subparsers.choices)
        self.assertIn("unarchive", user_subparsers.choices)

        actions = user_subparsers.choices["create"]._option_string_actions
        self.assertFalse(actions["--description"].required)

        user_subparsers = None
        for action in subparsers.choices["group"]._actions:
            if type(action) == argparse._SubParsersAction:
                user_subparsers = action
                break
        actions = user_subparsers.choices["create"]._option_string_actions
        self.assertTrue(actions["--name"].required)

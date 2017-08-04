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

import six
try:
    import unittest
except ImportError:
    import unittest2 as unittest

from gitlab import cli
import gitlab.v3.cli


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
        with self.assertRaises(SystemExit) as test:
            cli.die("foobar")

        self.assertEqual(test.exception.code, 1)

    def test_base_parser(self):
        parser = cli._get_base_parser()
        args = parser.parse_args(['-v', '-g', 'gl_id',
                                  '-c', 'foo.cfg', '-c', 'bar.cfg'])
        self.assertTrue(args.verbose)
        self.assertEqual(args.gitlab, 'gl_id')
        self.assertEqual(args.config_file, ['foo.cfg', 'bar.cfg'])


class TestV3CLI(unittest.TestCase):
    def test_parse_args(self):
        parser = cli._get_parser(gitlab.v3.cli)
        args = parser.parse_args(['project', 'list'])
        self.assertEqual(args.what, 'project')
        self.assertEqual(args.action, 'list')

    def test_parser(self):
        parser = cli._get_parser(gitlab.v3.cli)
        subparsers = None
        for action in parser._actions:
            if type(action) == argparse._SubParsersAction:
                subparsers = action
                break
        self.assertIsNotNone(subparsers)
        self.assertIn('user', subparsers.choices)

        user_subparsers = None
        for action in subparsers.choices['user']._actions:
            if type(action) == argparse._SubParsersAction:
                user_subparsers = action
                break
        self.assertIsNotNone(user_subparsers)
        self.assertIn('list', user_subparsers.choices)
        self.assertIn('get', user_subparsers.choices)
        self.assertIn('delete', user_subparsers.choices)
        self.assertIn('update', user_subparsers.choices)
        self.assertIn('create', user_subparsers.choices)
        self.assertIn('block', user_subparsers.choices)
        self.assertIn('unblock', user_subparsers.choices)

        actions = user_subparsers.choices['create']._option_string_actions
        self.assertFalse(actions['--twitter'].required)
        self.assertTrue(actions['--username'].required)

    def test_extra_actions(self):
        for cls, data in six.iteritems(gitlab.v3.cli.EXTRA_ACTIONS):
            for key in data:
                self.assertIsInstance(data[key], dict)

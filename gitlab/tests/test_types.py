# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 Gauvain Pocentek <gauvain@pocentek.net>
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

try:
    import unittest
except ImportError:
    import unittest2 as unittest

from gitlab import types


class TestGitlabAttribute(unittest.TestCase):
    def test_all(self):
        o = types.GitlabAttribute('whatever')
        self.assertEqual('whatever', o.get())

        o.set_from_cli('whatever2')
        self.assertEqual('whatever2', o.get())

        self.assertEqual('whatever2', o.get_for_api())

        o = types.GitlabAttribute()
        self.assertEqual(None, o._value)


class TestListAttribute(unittest.TestCase):
    def test_list_input(self):
        o = types.ListAttribute()
        o.set_from_cli('foo,bar,baz')
        self.assertEqual(['foo', 'bar', 'baz'], o.get())

        o.set_from_cli('foo')
        self.assertEqual(['foo'], o.get())

    def test_empty_input(self):
        o = types.ListAttribute()
        o.set_from_cli('')
        self.assertEqual([], o.get())

        o.set_from_cli('  ')
        self.assertEqual([], o.get())

    def test_get_for_api(self):
        o = types.ListAttribute()
        o.set_from_cli('foo,bar,baz')
        self.assertEqual('foo,bar,baz', o.get_for_api())


class TestLowercaseStringAttribute(unittest.TestCase):
    def test_get_for_api(self):
        o = types.LowercaseStringAttribute('FOO')
        self.assertEqual('foo', o.get_for_api())

# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 Gauvain Pocentek <gauvain@pocentek.net>
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

import unittest

from gitlab import utils


class TestUtils(unittest.TestCase):
    def test_clean_str_id(self):
        src = "nothing_special"
        dest = "nothing_special"
        self.assertEqual(dest, utils.clean_str_id(src))

        src = "foo#bar/baz/"
        dest = "foo%23bar%2Fbaz%2F"
        self.assertEqual(dest, utils.clean_str_id(src))

    def test_sanitized_url(self):
        src = "http://localhost/foo/bar"
        dest = "http://localhost/foo/bar"
        self.assertEqual(dest, utils.sanitized_url(src))

        src = "http://localhost/foo.bar.baz"
        dest = "http://localhost/foo%2Ebar%2Ebaz"
        self.assertEqual(dest, utils.sanitized_url(src))

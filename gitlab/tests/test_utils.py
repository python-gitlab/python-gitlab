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

from gitlab import utils


def test_clean_str_id():
    src = "nothing_special"
    dest = "nothing_special"
    assert dest == utils.clean_str_id(src)

    src = "foo#bar/baz/"
    dest = "foo%23bar%2Fbaz%2F"
    assert dest == utils.clean_str_id(src)


def test_sanitized_url():
    src = "http://localhost/foo/bar"
    dest = "http://localhost/foo/bar"
    assert dest == utils.sanitized_url(src)

    src = "http://localhost/foo.bar.baz"
    dest = "http://localhost/foo%2Ebar%2Ebaz"
    assert dest == utils.sanitized_url(src)


def test_sanitize_parameters_does_nothing():
    assert 1 == utils.sanitize_parameters(1)
    assert 1.5 == utils.sanitize_parameters(1.5)
    assert "foo" == utils.sanitize_parameters("foo")


def test_sanitize_parameters_slash():
    assert "foo%2Fbar" == utils.sanitize_parameters("foo/bar")


def test_sanitize_parameters_dict():
    source = {"url": "foo/bar", "id": 1}
    expected = {"url": "foo%2Fbar", "id": 1}
    assert expected == utils.sanitize_parameters(source)

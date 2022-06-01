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

import pytest

from gitlab import types


class TestRequiredOptional:
    def test_requiredoptional_empty(self):
        b = types.RequiredOptional()
        assert not b.required
        assert not b.optional
        assert not b.exclusive

    def test_requiredoptional_values_no_keywords(self):
        b = types.RequiredOptional(
            ("required1", "required2"),
            ("optional1", "optional2"),
            ("exclusive1", "exclusive2"),
        )
        assert b.required == ("required1", "required2")
        assert b.optional == ("optional1", "optional2")
        assert b.exclusive == ("exclusive1", "exclusive2")

    def test_requiredoptional_values_keywords(self):
        b = types.RequiredOptional(
            exclusive=("exclusive1", "exclusive2"),
            optional=("optional1", "optional2"),
            required=("required1", "required2"),
        )
        assert b.required == ("required1", "required2")
        assert b.optional == ("optional1", "optional2")
        assert b.exclusive == ("exclusive1", "exclusive2")

    def test_validate_attrs_required(self):
        data = {"required1": 1, "optional2": 2}
        rq = types.RequiredOptional(required=("required1",))
        rq.validate_attrs(data=data)
        data = {"optional1": 1, "optional2": 2}
        with pytest.raises(AttributeError, match="Missing attributes: required1"):
            rq.validate_attrs(data=data)

    def test_validate_attrs_exclusive(self):
        data = {"exclusive1": 1, "optional1": 1}
        rq = types.RequiredOptional(exclusive=("exclusive1", "exclusive2"))
        rq.validate_attrs(data=data)
        data = {"exclusive1": 1, "exclusive2": 2, "optional1": 1}
        with pytest.raises(
            AttributeError,
            match="Provide only one of these attributes: exclusive1, exclusive2",
        ):
            rq.validate_attrs(data=data)


def test_gitlab_attribute_get():
    o = types.GitlabAttribute("whatever")
    assert o.get() == "whatever"

    o.set_from_cli("whatever2")
    assert o.get() == "whatever2"
    assert o.get_for_api() == "whatever2"

    o = types.GitlabAttribute()
    assert o._value is None


def test_array_attribute_input():
    o = types.ArrayAttribute()
    o.set_from_cli("foo,bar,baz")
    assert o.get() == ["foo", "bar", "baz"]

    o.set_from_cli("foo")
    assert o.get() == ["foo"]


def test_array_attribute_empty_input():
    o = types.ArrayAttribute()
    o.set_from_cli("")
    assert o.get() == []

    o.set_from_cli("  ")
    assert o.get() == []


def test_array_attribute_get_for_api_from_cli():
    o = types.ArrayAttribute()
    o.set_from_cli("foo,bar,baz")
    assert o.get_for_api() == "foo,bar,baz"


def test_array_attribute_get_for_api_from_list():
    o = types.ArrayAttribute(["foo", "bar", "baz"])
    assert o.get_for_api() == "foo,bar,baz"


def test_array_attribute_get_for_api_from_int_list():
    o = types.ArrayAttribute([1, 9, 7])
    assert o.get_for_api() == "1,9,7"


def test_array_attribute_does_not_split_string():
    o = types.ArrayAttribute("foo")
    assert o.get_for_api() == "foo"


# CommaSeparatedListAttribute tests
def test_csv_string_attribute_get_for_api_from_cli():
    o = types.CommaSeparatedListAttribute()
    o.set_from_cli("foo,bar,baz")
    assert o.get_for_api() == "foo,bar,baz"


def test_csv_string_attribute_get_for_api_from_list():
    o = types.CommaSeparatedListAttribute(["foo", "bar", "baz"])
    assert o.get_for_api() == "foo,bar,baz"


def test_csv_string_attribute_get_for_api_from_int_list():
    o = types.CommaSeparatedListAttribute([1, 9, 7])
    assert o.get_for_api() == "1,9,7"


# LowercaseStringAttribute tests
def test_lowercase_string_attribute_get_for_api():
    o = types.LowercaseStringAttribute("FOO")
    assert o.get_for_api() == "foo"

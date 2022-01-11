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

import json

from gitlab import utils


def test_url_encode():
    src = "nothing_special"
    dest = "nothing_special"
    assert dest == utils._url_encode(src)

    src = "foo#bar/baz/"
    dest = "foo%23bar%2Fbaz%2F"
    assert dest == utils._url_encode(src)

    src = "foo%bar/baz/"
    dest = "foo%25bar%2Fbaz%2F"
    assert dest == utils._url_encode(src)

    # periods/dots should not be modified
    src = "docs/README.md"
    dest = "docs%2FREADME.md"
    assert dest == utils._url_encode(src)


class TestEncodedId:
    def test_init_str(self):
        obj = utils.EncodedId("Hello")
        assert "Hello" == str(obj)
        assert "Hello" == f"{obj}"

        obj = utils.EncodedId("this/is a/path")
        assert "this%2Fis%20a%2Fpath" == str(obj)
        assert "this%2Fis%20a%2Fpath" == f"{obj}"

    def test_init_int(self):
        obj = utils.EncodedId(23)
        assert "23" == str(obj)
        assert "23" == f"{obj}"

    def test_init_encodeid_str(self):
        value = "Goodbye"
        obj_init = utils.EncodedId(value)
        obj = utils.EncodedId(obj_init)
        assert value == str(obj)
        assert value == f"{obj}"
        assert value == obj.original_str

        value = "we got/a/path"
        expected = "we%20got%2Fa%2Fpath"
        obj_init = utils.EncodedId(value)
        assert value == obj_init.original_str
        assert expected == str(obj_init)
        assert expected == f"{obj_init}"
        # Show that no matter how many times we recursively call it we still only
        # URL-encode it once.
        obj = utils.EncodedId(
            utils.EncodedId(utils.EncodedId(utils.EncodedId(utils.EncodedId(obj_init))))
        )
        assert expected == str(obj)
        assert expected == f"{obj}"
        # We have stored a copy of our original string
        assert value == obj.original_str

        # Show assignments still only encode once
        obj2 = obj
        assert expected == str(obj2)
        assert expected == f"{obj2}"

    def test_init_encodeid_int(self):
        value = 23
        expected = f"{value}"
        obj_init = utils.EncodedId(value)
        obj = utils.EncodedId(obj_init)
        assert expected == str(obj)
        assert expected == f"{obj}"

    def test_json_serializable(self):
        obj = utils.EncodedId("someone")
        assert '"someone"' == json.dumps(obj)

        obj = utils.EncodedId("we got/a/path")
        assert '"we%20got%2Fa%2Fpath"' == json.dumps(obj)

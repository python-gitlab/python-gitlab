# -*- coding: utf-8 -*-
#
# Copyright (C) 2014 Mika Mäenpää <mika.j.maenpaa@tut.fi>,
#                    Tampere University of Technology
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or`
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import pickle

from httmock import HTTMock, response, urlmatch, with_httmock  # noqa

from gitlab import Gitlab, GitlabList
from gitlab.v4.objects import CurrentUser


username = "username"
user_id = 1


@urlmatch(scheme="http", netloc="localhost", path="/api/v4/user", method="get")
def resp_get_user(url, request):
    headers = {"content-type": "application/json"}
    content = '{{"id": {0:d}, "username": "{1:s}"}}'.format(user_id, username).encode(
        "utf-8"
    )
    return response(200, content, headers, None, 5, request)


@urlmatch(scheme="http", netloc="localhost", path="/api/v4/tests", method="get")
def resp_page_1(url, request):
    headers = {
        "content-type": "application/json",
        "X-Page": 1,
        "X-Next-Page": 2,
        "X-Per-Page": 1,
        "X-Total-Pages": 2,
        "X-Total": 2,
        "Link": ("<http://localhost/api/v4/tests?per_page=1&page=2>;" ' rel="next"'),
    }
    content = '[{"a": "b"}]'
    return response(200, content, headers, None, 5, request)


@urlmatch(
    scheme="http",
    netloc="localhost",
    path="/api/v4/tests",
    method="get",
    query=r".*page=2",
)
def resp_page_2(url, request):
    headers = {
        "content-type": "application/json",
        "X-Page": 2,
        "X-Next-Page": 2,
        "X-Per-Page": 1,
        "X-Total-Pages": 2,
        "X-Total": 2,
    }
    content = '[{"c": "d"}]'
    return response(200, content, headers, None, 5, request)


def test_gitlab_build_list(gl):
    with HTTMock(resp_page_1):
        obj = gl.http_list("/tests", as_list=False)
    assert len(obj) == 2
    assert obj._next_url == "http://localhost/api/v4/tests?per_page=1&page=2"
    assert obj.current_page == 1
    assert obj.prev_page is None
    assert obj.next_page == 2
    assert obj.per_page == 1
    assert obj.total_pages == 2
    assert obj.total == 2

    with HTTMock(resp_page_2):
        l = list(obj)
    assert len(l) == 2
    assert l[0]["a"] == "b"
    assert l[1]["c"] == "d"


@with_httmock(resp_page_1, resp_page_2)
def test_gitlab_all_omitted_when_as_list(gl):
    result = gl.http_list("/tests", as_list=False, all=True)
    assert isinstance(result, GitlabList)


def test_gitlab_strip_base_url(gl_trailing):
    assert gl_trailing.url == "http://localhost"


def test_gitlab_strip_api_url(gl_trailing):
    assert gl_trailing.api_url == "http://localhost/api/v4"


def test_gitlab_build_url(gl_trailing):
    r = gl_trailing._build_url("/projects")
    assert r == "http://localhost/api/v4/projects"


def test_gitlab_pickability(gl):
    original_gl_objects = gl._objects
    pickled = pickle.dumps(gl)
    unpickled = pickle.loads(pickled)
    assert isinstance(unpickled, Gitlab)
    assert hasattr(unpickled, "_objects")
    assert unpickled._objects == original_gl_objects


@with_httmock(resp_get_user)
def test_gitlab_token_auth(gl, callback=None):
    gl.auth()
    assert gl.user.username == username
    assert gl.user.id == user_id
    assert isinstance(gl.user, CurrentUser)


def test_gitlab_from_config(default_config):
    config_path = default_config
    Gitlab.from_config("one", [config_path])


def test_gitlab_subclass_from_config(default_config):
    class MyGitlab(Gitlab):
        pass

    config_path = default_config
    gl = MyGitlab.from_config("one", [config_path])
    assert isinstance(gl, MyGitlab)

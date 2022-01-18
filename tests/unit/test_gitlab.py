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

import copy
import pickle
import warnings

import pytest
import responses

import gitlab

localhost = "http://localhost"
token = "abc123"


@pytest.fixture
def resp_get_user():
    return {
        "method": responses.GET,
        "url": "http://localhost/api/v4/user",
        "json": {"id": 1, "username": "username"},
        "content_type": "application/json",
        "status": 200,
    }


@pytest.fixture
def resp_page_1():
    headers = {
        "X-Page": "1",
        "X-Next-Page": "2",
        "X-Per-Page": "1",
        "X-Total-Pages": "2",
        "X-Total": "2",
        "Link": ("<http://localhost/api/v4/tests?per_page=1&page=2>;" ' rel="next"'),
    }

    return {
        "method": responses.GET,
        "url": "http://localhost/api/v4/tests",
        "json": [{"a": "b"}],
        "headers": headers,
        "content_type": "application/json",
        "status": 200,
        "match": [responses.matchers.query_param_matcher({})],
    }


@pytest.fixture
def resp_page_2():
    headers = {
        "X-Page": "2",
        "X-Next-Page": "2",
        "X-Per-Page": "1",
        "X-Total-Pages": "2",
        "X-Total": "2",
    }
    params = {"per_page": "1", "page": "2"}

    return {
        "method": responses.GET,
        "url": "http://localhost/api/v4/tests",
        "json": [{"c": "d"}],
        "headers": headers,
        "content_type": "application/json",
        "status": 200,
        "match": [responses.matchers.query_param_matcher(params)],
    }


@responses.activate
def test_gitlab_build_list(gl, resp_page_1, resp_page_2):
    responses.add(**resp_page_1)
    obj = gl.http_list("/tests", as_list=False)
    assert len(obj) == 2
    assert obj._next_url == "http://localhost/api/v4/tests?per_page=1&page=2"
    assert obj.current_page == 1
    assert obj.prev_page is None
    assert obj.next_page == 2
    assert obj.per_page == 1
    assert obj.total_pages == 2
    assert obj.total == 2

    responses.add(**resp_page_2)
    test_list = list(obj)
    assert len(test_list) == 2
    assert test_list[0]["a"] == "b"
    assert test_list[1]["c"] == "d"


def _strip_pagination_headers(response):
    """
    https://docs.gitlab.com/ee/user/gitlab_com/index.html#pagination-response-headers
    """
    stripped = copy.deepcopy(response)

    del stripped["headers"]["X-Total-Pages"]
    del stripped["headers"]["X-Total"]

    return stripped


@responses.activate
def test_gitlab_build_list_missing_headers(gl, resp_page_1, resp_page_2):
    stripped_page_1 = _strip_pagination_headers(resp_page_1)
    stripped_page_2 = _strip_pagination_headers(resp_page_2)

    responses.add(**stripped_page_1)
    obj = gl.http_list("/tests", as_list=False)
    assert len(obj) == 0  # Lazy generator has no knowledge of total items
    assert obj.total_pages is None
    assert obj.total is None

    responses.add(**stripped_page_2)
    test_list = list(obj)
    assert len(test_list) == 2  # List has total items after making the API calls


@responses.activate
def test_gitlab_all_omitted_when_as_list(gl, resp_page_1, resp_page_2):
    responses.add(**resp_page_1)
    responses.add(**resp_page_2)
    result = gl.http_list("/tests", as_list=False, all=True)
    assert isinstance(result, gitlab.GitlabList)


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
    assert isinstance(unpickled, gitlab.Gitlab)
    assert hasattr(unpickled, "_objects")
    assert unpickled._objects == original_gl_objects


@responses.activate
def test_gitlab_token_auth(gl, resp_get_user):
    responses.add(**resp_get_user)
    gl.auth()
    assert gl.user.username == "username"
    assert gl.user.id == 1
    assert isinstance(gl.user, gitlab.v4.objects.CurrentUser)


def test_gitlab_default_url():
    gl = gitlab.Gitlab()
    assert gl.url == gitlab.const.DEFAULT_URL


@pytest.mark.parametrize(
    "args, kwargs, expected_url, expected_private_token, expected_oauth_token",
    [
        ([], {}, gitlab.const.DEFAULT_URL, None, None),
        ([None, token], {}, gitlab.const.DEFAULT_URL, token, None),
        ([localhost], {}, localhost, None, None),
        ([localhost, token], {}, localhost, token, None),
        ([localhost, None, token], {}, localhost, None, token),
        ([], {"private_token": token}, gitlab.const.DEFAULT_URL, token, None),
        ([], {"oauth_token": token}, gitlab.const.DEFAULT_URL, None, token),
        ([], {"url": localhost}, localhost, None, None),
        ([], {"url": localhost, "private_token": token}, localhost, token, None),
        ([], {"url": localhost, "oauth_token": token}, localhost, None, token),
    ],
    ids=[
        "no_args",
        "args_private_token",
        "args_url",
        "args_url_private_token",
        "args_url_oauth_token",
        "kwargs_private_token",
        "kwargs_oauth_token",
        "kwargs_url",
        "kwargs_url_private_token",
        "kwargs_url_oauth_token",
    ],
)
def test_gitlab_args_kwargs(
    args, kwargs, expected_url, expected_private_token, expected_oauth_token
):
    gl = gitlab.Gitlab(*args, **kwargs)
    assert gl.url == expected_url
    assert gl.private_token == expected_private_token
    assert gl.oauth_token == expected_oauth_token


def test_gitlab_from_config(default_config):
    config_path = default_config
    gitlab.Gitlab.from_config("one", [config_path])


def test_gitlab_subclass_from_config(default_config):
    class MyGitlab(gitlab.Gitlab):
        pass

    config_path = default_config
    gl = MyGitlab.from_config("one", [config_path])
    assert isinstance(gl, MyGitlab)


@pytest.mark.parametrize(
    "kwargs,expected_agent",
    [
        ({}, gitlab.const.USER_AGENT),
        ({"user_agent": "my-package/1.0.0"}, "my-package/1.0.0"),
    ],
)
def test_gitlab_user_agent(kwargs, expected_agent):
    gl = gitlab.Gitlab("http://localhost", **kwargs)
    assert gl.headers["User-Agent"] == expected_agent


def test_gitlab_deprecated_const():
    with warnings.catch_warnings(record=True) as caught_warnings:
        gitlab.NO_ACCESS
    assert len(caught_warnings) == 1
    warning = caught_warnings[0]
    assert isinstance(warning.message, DeprecationWarning)
    message = str(caught_warnings[0].message)
    assert "deprecated" in message
    assert "gitlab.const.NO_ACCESS" in message

    with warnings.catch_warnings(record=True) as caught_warnings:
        gitlab.const.NO_ACCESS
    assert len(caught_warnings) == 0

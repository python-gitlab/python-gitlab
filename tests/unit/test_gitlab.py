import copy
import logging
import pickle
from http.client import HTTPConnection

import pytest
import requests
import responses

import gitlab
from gitlab.config import GitlabConfigMissingError, GitlabDataError
from tests.unit import helpers

localhost = "http://localhost"
token = "abc123"


@pytest.fixture
def resp_get_user():
    return {
        "method": responses.GET,
        "url": "http://localhost/api/v4/user",
        "json": {
            "id": 1,
            "username": "username",
            "web_url": "http://localhost/username",
        },
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
        "match": helpers.MATCH_EMPTY_QUERY_PARAMS,
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


def test_gitlab_init_with_valid_api_version():
    gl = gitlab.Gitlab(api_version="4")
    assert gl.api_version == "4"


def test_gitlab_init_with_invalid_api_version():
    with pytest.raises(ModuleNotFoundError, match="gitlab.v1.objects"):
        gitlab.Gitlab(api_version="1")


def test_gitlab_as_context_manager():
    with gitlab.Gitlab() as gl:
        assert isinstance(gl, gitlab.Gitlab)


def test_gitlab_enable_debug(gl):
    gl.enable_debug()

    logger = logging.getLogger("requests.packages.urllib3")
    assert logger.level == logging.DEBUG
    assert HTTPConnection.debuglevel == 1


@responses.activate
@pytest.mark.parametrize(
    "status_code,response_json,expected",
    [
        (200, {"version": "0.0.0-pre", "revision": "abcdef"}, ("0.0.0-pre", "abcdef")),
        (200, None, ("unknown", "unknown")),
        (401, None, ("unknown", "unknown")),
    ],
)
def test_gitlab_get_version(gl, status_code, response_json, expected):
    responses.add(
        method=responses.GET,
        url="http://localhost/api/v4/version",
        json=response_json,
        status=status_code,
        match=helpers.MATCH_EMPTY_QUERY_PARAMS,
    )

    version = gl.version()
    assert version == expected


@responses.activate
@pytest.mark.parametrize(
    "response_json,expected",
    [
        ({"id": "1", "plan": "premium"}, {"id": "1", "plan": "premium"}),
        (None, {}),
    ],
)
def test_gitlab_get_license(gl, response_json, expected):
    responses.add(
        method=responses.GET,
        url="http://localhost/api/v4/license",
        json=response_json,
        status=200,
        match=helpers.MATCH_EMPTY_QUERY_PARAMS,
    )

    gitlab_license = gl.get_license()
    assert gitlab_license == expected


@responses.activate
def test_gitlab_set_license(gl):
    responses.add(
        method=responses.POST,
        url="http://localhost/api/v4/license",
        json={"id": 1, "plan": "premium"},
        status=201,
        match=helpers.MATCH_EMPTY_QUERY_PARAMS,
    )

    gitlab_license = gl.set_license("yJkYXRhIjoiMHM5Q")
    assert gitlab_license["plan"] == "premium"


@responses.activate
def test_gitlab_build_list(gl, resp_page_1, resp_page_2):
    responses.add(**resp_page_1)
    obj = gl.http_list("/tests", iterator=True)
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
    obj = gl.http_list("/tests", iterator=True)
    assert len(obj) == 0  # Lazy generator has no knowledge of total items
    assert obj.total_pages is None
    assert obj.total is None

    responses.add(**stripped_page_2)
    test_list = list(obj)
    assert len(test_list) == 2  # List has total items after making the API calls


@responses.activate
def test_gitlab_get_all_omitted_when_iterator(gl, resp_page_1, resp_page_2):
    responses.add(**resp_page_1)
    responses.add(**resp_page_2)
    result = gl.http_list("/tests", iterator=True, get_all=True)
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


@responses.activate
def test_gitlab_auth_with_mismatching_url_warns():
    responses.add(
        method=responses.GET,
        url="http://first.example.com/api/v4/user",
        json={
            "username": "test-user",
            "web_url": "http://second.example.com/test-user",
        },
        content_type="application/json",
        status=200,
    )
    gl = gitlab.Gitlab("http://first.example.com")

    with pytest.warns(UserWarning):
        gl.auth()


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


def test_gitlab_from_config_without_files_raises():
    with pytest.raises(GitlabConfigMissingError, match="non-existing"):
        gitlab.Gitlab.from_config("non-existing")


def test_gitlab_from_config_with_wrong_gitlab_id_raises(default_config):
    with pytest.raises(GitlabDataError, match="non-existing"):
        gitlab.Gitlab.from_config("non-existing", [default_config])


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


def test_gitlab_enum_const_does_not_warn(recwarn):
    no_access = gitlab.const.AccessLevel.NO_ACCESS

    assert not recwarn
    assert no_access == 0


def test_gitlab_plain_const_does_not_warn(recwarn):
    no_access = gitlab.const.NO_ACCESS

    assert not recwarn
    assert no_access == 0


@responses.activate
@pytest.mark.parametrize(
    "kwargs,link_header,expected_next_url,show_warning",
    [
        (
            {},
            "<http://localhost/api/v4/tests?per_page=1&page=2>;" ' rel="next"',
            "http://localhost/api/v4/tests?per_page=1&page=2",
            False,
        ),
        (
            {},
            "<http://orig_host/api/v4/tests?per_page=1&page=2>;" ' rel="next"',
            "http://orig_host/api/v4/tests?per_page=1&page=2",
            True,
        ),
        (
            {"keep_base_url": True},
            "<http://orig_host/api/v4/tests?per_page=1&page=2>;" ' rel="next"',
            "http://localhost/api/v4/tests?per_page=1&page=2",
            False,
        ),
    ],
    ids=["url-match-does-not-warn", "url-mismatch-warns", "url-mismatch-keeps-url"],
)
def test_gitlab_keep_base_url(kwargs, link_header, expected_next_url, show_warning):
    responses.add(
        **{
            "method": responses.GET,
            "url": "http://localhost/api/v4/tests",
            "json": [{"a": "b"}],
            "headers": {
                "X-Page": "1",
                "X-Next-Page": "2",
                "X-Per-Page": "1",
                "X-Total-Pages": "2",
                "X-Total": "2",
                "Link": (link_header),
            },
            "content_type": "application/json",
            "status": 200,
            "match": helpers.MATCH_EMPTY_QUERY_PARAMS,
        }
    )

    gl = gitlab.Gitlab(url="http://localhost", **kwargs)
    if show_warning:
        with pytest.warns(UserWarning) as warn_record:
            obj = gl.http_list("/tests", iterator=True)
        assert len(warn_record) == 1
    else:
        obj = gl.http_list("/tests", iterator=True)
    assert obj._next_url == expected_next_url


def test_no_custom_session(default_config):
    """Test no custom session"""

    config_path = default_config
    custom_session = requests.Session()
    test_gitlab = gitlab.Gitlab.from_config("one", [config_path])

    assert test_gitlab.session != custom_session


def test_custom_session(default_config):
    """Test custom session"""

    config_path = default_config
    custom_session = requests.Session()
    test_gitlab = gitlab.Gitlab.from_config(
        "one", [config_path], session=custom_session
    )

    assert test_gitlab.session == custom_session

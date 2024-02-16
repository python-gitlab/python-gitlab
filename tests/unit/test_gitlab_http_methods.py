import copy
import warnings

import pytest
import requests
import responses

from gitlab import GitlabHttpError, GitlabList, GitlabParsingError, RedirectError
from gitlab.const import RETRYABLE_TRANSIENT_ERROR_CODES
from tests.unit import helpers


def test_build_url(gl):
    r = gl._build_url("http://localhost/api/v4")
    assert r == "http://localhost/api/v4"
    r = gl._build_url("https://localhost/api/v4")
    assert r == "https://localhost/api/v4"
    r = gl._build_url("/projects")
    assert r == "http://localhost/api/v4/projects"


@responses.activate
def test_http_request(gl):
    url = "http://localhost/api/v4/projects"
    responses.add(
        method=responses.GET,
        url=url,
        json=[{"name": "project1"}],
        status=200,
        match=helpers.MATCH_EMPTY_QUERY_PARAMS,
    )

    http_r = gl.http_request("get", "/projects")
    http_r.json()
    assert http_r.status_code == 200
    assert responses.assert_call_count(url, 1) is True


@responses.activate
def test_http_request_with_url_encoded_kwargs_does_not_duplicate_params(gl):
    url = "http://localhost/api/v4/projects?topics%5B%5D=python"
    responses.add(
        method=responses.GET,
        url=url,
        json=[{"name": "project1"}],
        status=200,
        match=[responses.matchers.query_param_matcher({"topics[]": "python"})],
    )

    kwargs = {"topics[]": "python"}
    http_r = gl.http_request("get", "/projects?topics%5B%5D=python", **kwargs)
    http_r.json()
    assert http_r.status_code == 200
    assert responses.assert_call_count(url, 1)


@responses.activate
def test_http_request_404(gl):
    url = "http://localhost/api/v4/not_there"
    responses.add(
        method=responses.GET,
        url=url,
        json={},
        status=400,
        match=helpers.MATCH_EMPTY_QUERY_PARAMS,
    )

    with pytest.raises(GitlabHttpError):
        gl.http_request("get", "/not_there")
    assert responses.assert_call_count(url, 1) is True


@responses.activate
@pytest.mark.parametrize("status_code", RETRYABLE_TRANSIENT_ERROR_CODES)
def test_http_request_with_only_failures(gl, status_code):
    url = "http://localhost/api/v4/projects"
    responses.add(
        method=responses.GET,
        url=url,
        json={},
        status=status_code,
        match=helpers.MATCH_EMPTY_QUERY_PARAMS,
    )

    with pytest.raises(GitlabHttpError):
        gl.http_request("get", "/projects")

    assert responses.assert_call_count(url, 1) is True


@responses.activate
def test_http_request_with_retry_on_method_for_transient_failures(gl):
    call_count = 0
    calls_before_success = 3

    url = "http://localhost/api/v4/projects"

    def request_callback(request):
        nonlocal call_count
        call_count += 1
        status_code = 200 if call_count >= calls_before_success else 500
        headers = {}
        body = "[]"

        return (status_code, headers, body)

    responses.add_callback(
        method=responses.GET,
        url=url,
        callback=request_callback,
        content_type="application/json",
    )

    http_r = gl.http_request("get", "/projects", retry_transient_errors=True)

    assert http_r.status_code == 200
    assert len(responses.calls) == calls_before_success


@responses.activate
@pytest.mark.parametrize(
    "exception",
    [
        requests.ConnectionError("Connection aborted."),
        requests.exceptions.ChunkedEncodingError("Connection broken."),
    ],
)
def test_http_request_with_retry_on_method_for_transient_network_failures(
    gl, exception
):
    call_count = 0
    calls_before_success = 3

    url = "http://localhost/api/v4/projects"

    def request_callback(request):
        nonlocal call_count
        call_count += 1
        status_code = 200
        headers = {}
        body = "[]"

        if call_count >= calls_before_success:
            return (status_code, headers, body)
        raise exception

    responses.add_callback(
        method=responses.GET,
        url=url,
        callback=request_callback,
        content_type="application/json",
    )

    http_r = gl.http_request("get", "/projects", retry_transient_errors=True)

    assert http_r.status_code == 200
    assert len(responses.calls) == calls_before_success


@responses.activate
def test_http_request_with_retry_on_class_for_transient_failures(gl_retry):
    call_count = 0
    calls_before_success = 3

    url = "http://localhost/api/v4/projects"

    def request_callback(request: requests.models.PreparedRequest):
        nonlocal call_count
        call_count += 1
        status_code = 200 if call_count >= calls_before_success else 500
        headers = {}
        body = "[]"

        return (status_code, headers, body)

    responses.add_callback(
        method=responses.GET,
        url=url,
        callback=request_callback,
        content_type="application/json",
    )

    http_r = gl_retry.http_request("get", "/projects", retry_transient_errors=True)

    assert http_r.status_code == 200
    assert len(responses.calls) == calls_before_success


@responses.activate
def test_http_request_with_retry_on_class_for_transient_network_failures(gl_retry):
    call_count = 0
    calls_before_success = 3

    url = "http://localhost/api/v4/projects"

    def request_callback(request: requests.models.PreparedRequest):
        nonlocal call_count
        call_count += 1
        status_code = 200
        headers = {}
        body = "[]"

        if call_count >= calls_before_success:
            return (status_code, headers, body)
        raise requests.ConnectionError("Connection aborted.")

    responses.add_callback(
        method=responses.GET,
        url=url,
        callback=request_callback,
        content_type="application/json",
    )

    http_r = gl_retry.http_request("get", "/projects", retry_transient_errors=True)

    assert http_r.status_code == 200
    assert len(responses.calls) == calls_before_success


@responses.activate
def test_http_request_with_retry_on_class_and_method_for_transient_failures(gl_retry):
    call_count = 0
    calls_before_success = 3

    url = "http://localhost/api/v4/projects"

    def request_callback(request):
        nonlocal call_count
        call_count += 1
        status_code = 200 if call_count >= calls_before_success else 500
        headers = {}
        body = "[]"

        return (status_code, headers, body)

    responses.add_callback(
        method=responses.GET,
        url=url,
        callback=request_callback,
        content_type="application/json",
    )

    with pytest.raises(GitlabHttpError):
        gl_retry.http_request("get", "/projects", retry_transient_errors=False)

    assert len(responses.calls) == 1


@responses.activate
def test_http_request_with_retry_on_class_and_method_for_transient_network_failures(
    gl_retry,
):
    call_count = 0
    calls_before_success = 3

    url = "http://localhost/api/v4/projects"

    def request_callback(request):
        nonlocal call_count
        call_count += 1
        status_code = 200
        headers = {}
        body = "[]"

        if call_count >= calls_before_success:
            return (status_code, headers, body)
        raise requests.ConnectionError("Connection aborted.")

    responses.add_callback(
        method=responses.GET,
        url=url,
        callback=request_callback,
        content_type="application/json",
    )

    with pytest.raises(requests.ConnectionError):
        gl_retry.http_request("get", "/projects", retry_transient_errors=False)

    assert len(responses.calls) == 1


def create_redirect_response(
    *, response: requests.models.Response, http_method: str, api_path: str
) -> requests.models.Response:
    """Create a Requests response object that has a redirect in it"""

    assert api_path.startswith("/")
    http_method = http_method.upper()

    # Create a history which contains our original request which is redirected
    history = [
        helpers.httmock_response(
            status_code=302,
            content="",
            headers={"Location": f"http://example.com/api/v4{api_path}"},
            reason="Moved Temporarily",
            request=response.request,
        )
    ]

    # Create a "prepped" Request object to be the final redirect. The redirect
    # will be a "GET" method as Requests changes the method to "GET" when there
    # is a 301/302 redirect code.
    req = requests.Request(
        method="GET",
        url=f"http://example.com/api/v4{api_path}",
    )
    prepped = req.prepare()

    resp_obj = helpers.httmock_response(
        status_code=200,
        content="",
        headers={},
        reason="OK",
        elapsed=5,
        request=prepped,
    )
    resp_obj.history = history
    return resp_obj


def test_http_request_302_get_does_not_raise(gl):
    """Test to show that a redirect of a GET will not cause an error"""

    method = "get"
    api_path = "/user/status"
    url = f"http://localhost/api/v4{api_path}"

    def response_callback(
        response: requests.models.Response,
    ) -> requests.models.Response:
        return create_redirect_response(
            response=response, http_method=method, api_path=api_path
        )

    with responses.RequestsMock(response_callback=response_callback) as req_mock:
        req_mock.add(
            method=responses.GET,
            url=url,
            status=302,
            match=helpers.MATCH_EMPTY_QUERY_PARAMS,
        )
        gl.http_request(verb=method, path=api_path)


def test_http_request_302_put_raises_redirect_error(gl):
    """Test to show that a redirect of a PUT will cause an error"""

    method = "put"
    api_path = "/user/status"
    url = f"http://localhost/api/v4{api_path}"

    def response_callback(
        response: requests.models.Response,
    ) -> requests.models.Response:
        return create_redirect_response(
            response=response, http_method=method, api_path=api_path
        )

    with responses.RequestsMock(response_callback=response_callback) as req_mock:
        req_mock.add(
            method=responses.PUT,
            url=url,
            status=302,
            match=helpers.MATCH_EMPTY_QUERY_PARAMS,
        )
        with pytest.raises(RedirectError) as exc:
            gl.http_request(verb=method, path=api_path)
    error_message = exc.value.error_message
    assert "Moved Temporarily" in error_message
    assert "http://localhost/api/v4/user/status" in error_message
    assert "http://example.com/api/v4/user/status" in error_message


def test_http_request_on_409_resource_lock_retries(gl_retry):
    url = "http://localhost/api/v4/user"
    retried = False

    def response_callback(
        response: requests.models.Response,
    ) -> requests.models.Response:
        """We need a callback that adds a resource lock reason only on first call"""
        nonlocal retried

        if not retried:
            response.reason = "Resource lock"

        retried = True
        return response

    with responses.RequestsMock(response_callback=response_callback) as rsps:
        rsps.add(
            method=responses.GET,
            url=url,
            status=409,
            match=helpers.MATCH_EMPTY_QUERY_PARAMS,
        )
        rsps.add(
            method=responses.GET,
            url=url,
            status=200,
            match=helpers.MATCH_EMPTY_QUERY_PARAMS,
        )
        response = gl_retry.http_request("get", "/user")

    assert response.status_code == 200


def test_http_request_on_409_resource_lock_without_retry_raises(gl):
    url = "http://localhost/api/v4/user"

    def response_callback(
        response: requests.models.Response,
    ) -> requests.models.Response:
        """Without retry, this will fail on the first call"""
        response.reason = "Resource lock"
        return response

    with responses.RequestsMock(response_callback=response_callback) as req_mock:
        req_mock.add(
            method=responses.GET,
            url=url,
            status=409,
            match=helpers.MATCH_EMPTY_QUERY_PARAMS,
        )
        with pytest.raises(GitlabHttpError) as excinfo:
            gl.http_request("get", "/user")

    assert excinfo.value.response_code == 409


@responses.activate
def test_get_request(gl):
    url = "http://localhost/api/v4/projects"
    responses.add(
        method=responses.GET,
        url=url,
        json={"name": "project1"},
        status=200,
        match=helpers.MATCH_EMPTY_QUERY_PARAMS,
    )

    result = gl.http_get("/projects")
    assert isinstance(result, dict)
    assert result["name"] == "project1"
    assert responses.assert_call_count(url, 1) is True


@responses.activate
def test_get_request_raw(gl):
    url = "http://localhost/api/v4/projects"
    responses.add(
        method=responses.GET,
        url=url,
        content_type="application/octet-stream",
        body="content",
        status=200,
        match=helpers.MATCH_EMPTY_QUERY_PARAMS,
    )

    result = gl.http_get("/projects")
    assert result.content.decode("utf-8") == "content"
    assert responses.assert_call_count(url, 1) is True


@responses.activate
def test_get_request_404(gl):
    url = "http://localhost/api/v4/not_there"
    responses.add(
        method=responses.GET,
        url=url,
        json=[],
        status=404,
        match=helpers.MATCH_EMPTY_QUERY_PARAMS,
    )

    with pytest.raises(GitlabHttpError):
        gl.http_get("/not_there")
    assert responses.assert_call_count(url, 1) is True


@responses.activate
def test_get_request_invalid_data(gl):
    url = "http://localhost/api/v4/projects"
    responses.add(
        method=responses.GET,
        url=url,
        body='["name": "project1"]',
        content_type="application/json",
        status=200,
        match=helpers.MATCH_EMPTY_QUERY_PARAMS,
    )

    with pytest.raises(GitlabParsingError):
        result = gl.http_get("/projects")
        print(type(result))
        print(result.content)
    assert responses.assert_call_count(url, 1) is True


@responses.activate
def test_head_request(gl):
    url = "http://localhost/api/v4/projects"
    responses.add(
        method=responses.HEAD,
        url=url,
        headers={"X-Total": "1"},
        status=200,
        match=helpers.MATCH_EMPTY_QUERY_PARAMS,
    )

    result = gl.http_head("/projects")
    assert isinstance(result, requests.structures.CaseInsensitiveDict)
    assert result["X-Total"] == "1"


@responses.activate
def test_list_request(gl):
    url = "http://localhost/api/v4/projects"
    responses.add(
        method=responses.GET,
        url=url,
        json=[{"name": "project1"}],
        headers={"X-Total": "1"},
        status=200,
        match=helpers.MATCH_EMPTY_QUERY_PARAMS,
    )

    with warnings.catch_warnings(record=True) as caught_warnings:
        result = gl.http_list("/projects", iterator=False)
    assert len(caught_warnings) == 0
    assert isinstance(result, list)
    assert len(result) == 1

    result = gl.http_list("/projects", iterator=True)
    assert isinstance(result, GitlabList)
    assert len(list(result)) == 1

    result = gl.http_list("/projects", get_all=True)
    assert isinstance(result, list)
    assert len(result) == 1
    assert responses.assert_call_count(url, 3) is True


@responses.activate
def test_list_request_page_and_iterator(gl):
    response_dict = copy.deepcopy(large_list_response)
    response_dict["match"] = [responses.matchers.query_param_matcher({"page": "1"})]
    responses.add(**response_dict)

    with pytest.warns(
        UserWarning, match="`iterator=True` and `page=1` were both specified"
    ):
        result = gl.http_list("/projects", iterator=True, page=1)
    assert isinstance(result, list)
    assert len(result) == 20
    assert len(responses.calls) == 1


large_list_response = {
    "method": responses.GET,
    "url": "http://localhost/api/v4/projects",
    "json": [
        {"name": "project01"},
        {"name": "project02"},
        {"name": "project03"},
        {"name": "project04"},
        {"name": "project05"},
        {"name": "project06"},
        {"name": "project07"},
        {"name": "project08"},
        {"name": "project09"},
        {"name": "project10"},
        {"name": "project11"},
        {"name": "project12"},
        {"name": "project13"},
        {"name": "project14"},
        {"name": "project15"},
        {"name": "project16"},
        {"name": "project17"},
        {"name": "project18"},
        {"name": "project19"},
        {"name": "project20"},
    ],
    "headers": {"X-Total": "30", "x-per-page": "20"},
    "status": 200,
    "match": helpers.MATCH_EMPTY_QUERY_PARAMS,
}


@responses.activate
def test_list_request_pagination_warning(gl):
    responses.add(**large_list_response)

    with warnings.catch_warnings(record=True) as caught_warnings:
        result = gl.http_list("/projects", iterator=False)
    assert len(caught_warnings) == 1
    warning = caught_warnings[0]
    assert isinstance(warning.message, UserWarning)
    message = str(warning.message)
    assert "Calling a `list()` method" in message
    assert "python-gitlab.readthedocs.io" in message
    assert __file__ in message
    assert __file__ == warning.filename
    assert isinstance(result, list)
    assert len(result) == 20
    assert len(responses.calls) == 1


@responses.activate
def test_list_request_iterator_true_nowarning(gl):
    responses.add(**large_list_response)
    with warnings.catch_warnings(record=True) as caught_warnings:
        result = gl.http_list("/projects", iterator=True)
    assert len(caught_warnings) == 0
    assert isinstance(result, GitlabList)
    assert len(list(result)) == 20
    assert len(responses.calls) == 1


@responses.activate
def test_list_request_all_true_nowarning(gl):
    responses.add(**large_list_response)
    with warnings.catch_warnings(record=True) as caught_warnings:
        result = gl.http_list("/projects", get_all=True)
    assert len(caught_warnings) == 0
    assert isinstance(result, list)
    assert len(result) == 20
    assert len(responses.calls) == 1


@responses.activate
def test_list_request_all_false_nowarning(gl):
    responses.add(**large_list_response)
    with warnings.catch_warnings(record=True) as caught_warnings:
        result = gl.http_list("/projects", all=False)
    assert len(caught_warnings) == 0
    assert isinstance(result, list)
    assert len(result) == 20
    assert len(responses.calls) == 1


@responses.activate
def test_list_request_page_nowarning(gl):
    response_dict = copy.deepcopy(large_list_response)
    response_dict["match"] = [responses.matchers.query_param_matcher({"page": "1"})]
    responses.add(**response_dict)
    with warnings.catch_warnings(record=True) as caught_warnings:
        gl.http_list("/projects", page=1)
    assert len(caught_warnings) == 0
    assert len(responses.calls) == 1


@responses.activate
def test_list_request_404(gl):
    url = "http://localhost/api/v4/not_there"
    responses.add(
        method=responses.GET,
        url=url,
        json=[],
        status=404,
        match=helpers.MATCH_EMPTY_QUERY_PARAMS,
    )

    with pytest.raises(GitlabHttpError):
        gl.http_list("/not_there")
    assert responses.assert_call_count(url, 1) is True


@responses.activate
def test_list_request_invalid_data(gl):
    url = "http://localhost/api/v4/projects"
    responses.add(
        method=responses.GET,
        url=url,
        body='["name": "project1"]',
        content_type="application/json",
        status=200,
        match=helpers.MATCH_EMPTY_QUERY_PARAMS,
    )

    with pytest.raises(GitlabParsingError):
        gl.http_list("/projects")
    assert responses.assert_call_count(url, 1) is True


@responses.activate
def test_post_request(gl):
    url = "http://localhost/api/v4/projects"
    responses.add(
        method=responses.POST,
        url=url,
        json={"name": "project1"},
        status=200,
        match=helpers.MATCH_EMPTY_QUERY_PARAMS,
    )

    result = gl.http_post("/projects")
    assert isinstance(result, dict)
    assert result["name"] == "project1"
    assert responses.assert_call_count(url, 1) is True


@responses.activate
def test_post_request_404(gl):
    url = "http://localhost/api/v4/not_there"
    responses.add(
        method=responses.POST,
        url=url,
        json=[],
        status=404,
        match=helpers.MATCH_EMPTY_QUERY_PARAMS,
    )

    with pytest.raises(GitlabHttpError):
        gl.http_post("/not_there")
    assert responses.assert_call_count(url, 1) is True


@responses.activate
def test_post_request_invalid_data(gl):
    url = "http://localhost/api/v4/projects"
    responses.add(
        method=responses.POST,
        url=url,
        content_type="application/json",
        body='["name": "project1"]',
        status=200,
        match=helpers.MATCH_EMPTY_QUERY_PARAMS,
    )

    with pytest.raises(GitlabParsingError):
        gl.http_post("/projects")
    assert responses.assert_call_count(url, 1) is True


@responses.activate
def test_put_request(gl):
    url = "http://localhost/api/v4/projects"
    responses.add(
        method=responses.PUT,
        url=url,
        json={"name": "project1"},
        status=200,
        match=helpers.MATCH_EMPTY_QUERY_PARAMS,
    )

    result = gl.http_put("/projects")
    assert isinstance(result, dict)
    assert result["name"] == "project1"
    assert responses.assert_call_count(url, 1) is True


@responses.activate
def test_put_request_404(gl):
    url = "http://localhost/api/v4/not_there"
    responses.add(
        method=responses.PUT,
        url=url,
        json=[],
        status=404,
        match=helpers.MATCH_EMPTY_QUERY_PARAMS,
    )

    with pytest.raises(GitlabHttpError):
        gl.http_put("/not_there")
    assert responses.assert_call_count(url, 1) is True


@responses.activate
def test_put_request_204(gl):
    url = "http://localhost/api/v4/projects"
    responses.add(
        method=responses.PUT,
        url=url,
        status=204,
        match=helpers.MATCH_EMPTY_QUERY_PARAMS,
    )

    result = gl.http_put("/projects")
    assert isinstance(result, requests.Response)
    assert responses.assert_call_count(url, 1) is True


@responses.activate
def test_put_request_invalid_data(gl):
    url = "http://localhost/api/v4/projects"
    responses.add(
        method=responses.PUT,
        url=url,
        body='["name": "project1"]',
        content_type="application/json",
        status=200,
        match=helpers.MATCH_EMPTY_QUERY_PARAMS,
    )

    with pytest.raises(GitlabParsingError):
        gl.http_put("/projects")
    assert responses.assert_call_count(url, 1) is True


@responses.activate
def test_patch_request(gl):
    url = "http://localhost/api/v4/projects"
    responses.add(
        method=responses.PATCH,
        url=url,
        json={"name": "project1"},
        status=200,
        match=helpers.MATCH_EMPTY_QUERY_PARAMS,
    )

    result = gl.http_patch("/projects")
    assert isinstance(result, dict)
    assert result["name"] == "project1"
    assert responses.assert_call_count(url, 1) is True


@responses.activate
def test_patch_request_204(gl):
    url = "http://localhost/api/v4/projects"
    responses.add(
        method=responses.PATCH,
        url=url,
        status=204,
        match=helpers.MATCH_EMPTY_QUERY_PARAMS,
    )

    result = gl.http_patch("/projects")
    assert isinstance(result, requests.Response)
    assert responses.assert_call_count(url, 1) is True


@responses.activate
def test_patch_request_404(gl):
    url = "http://localhost/api/v4/not_there"
    responses.add(
        method=responses.PATCH,
        url=url,
        json=[],
        status=404,
        match=helpers.MATCH_EMPTY_QUERY_PARAMS,
    )

    with pytest.raises(GitlabHttpError):
        gl.http_patch("/not_there")
    assert responses.assert_call_count(url, 1) is True


@responses.activate
def test_patch_request_invalid_data(gl):
    url = "http://localhost/api/v4/projects"
    responses.add(
        method=responses.PATCH,
        url=url,
        body='["name": "project1"]',
        content_type="application/json",
        status=200,
        match=helpers.MATCH_EMPTY_QUERY_PARAMS,
    )

    with pytest.raises(GitlabParsingError):
        gl.http_patch("/projects")
    assert responses.assert_call_count(url, 1) is True


@responses.activate
def test_delete_request(gl):
    url = "http://localhost/api/v4/projects"
    responses.add(
        method=responses.DELETE,
        url=url,
        json=True,
        status=200,
        match=helpers.MATCH_EMPTY_QUERY_PARAMS,
    )

    result = gl.http_delete("/projects")
    assert isinstance(result, requests.Response)
    assert result.json() is True
    assert responses.assert_call_count(url, 1) is True


@responses.activate
def test_delete_request_404(gl):
    url = "http://localhost/api/v4/not_there"
    responses.add(
        method=responses.DELETE,
        url=url,
        json=[],
        status=404,
        match=helpers.MATCH_EMPTY_QUERY_PARAMS,
    )

    with pytest.raises(GitlabHttpError):
        gl.http_delete("/not_there")
    assert responses.assert_call_count(url, 1) is True

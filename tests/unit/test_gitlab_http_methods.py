import pytest
import requests
from httmock import HTTMock, response, urlmatch

from gitlab import GitlabHttpError, GitlabList, GitlabParsingError, RedirectError


def test_build_url(gl):
    r = gl._build_url("http://localhost/api/v4")
    assert r == "http://localhost/api/v4"
    r = gl._build_url("https://localhost/api/v4")
    assert r == "https://localhost/api/v4"
    r = gl._build_url("/projects")
    assert r == "http://localhost/api/v4/projects"


def test_http_request(gl):
    @urlmatch(scheme="http", netloc="localhost", path="/api/v4/projects", method="get")
    def resp_cont(url, request):
        headers = {"content-type": "application/json"}
        content = '[{"name": "project1"}]'
        return response(200, content, headers, None, 5, request)

    with HTTMock(resp_cont):
        http_r = gl.http_request("get", "/projects")
        http_r.json()
        assert http_r.status_code == 200


def test_http_request_404(gl):
    @urlmatch(scheme="http", netloc="localhost", path="/api/v4/not_there", method="get")
    def resp_cont(url, request):
        content = {"Here is why it failed"}
        return response(404, content, {}, None, 5, request)

    with HTTMock(resp_cont):
        with pytest.raises(GitlabHttpError):
            gl.http_request("get", "/not_there")


@pytest.mark.parametrize("status_code", [500, 502, 503, 504])
def test_http_request_with_only_failures(gl, status_code):
    call_count = 0

    @urlmatch(scheme="http", netloc="localhost", path="/api/v4/projects", method="get")
    def resp_cont(url, request):
        nonlocal call_count
        call_count += 1
        return response(status_code, {"Here is why it failed"}, {}, None, 5, request)

    with HTTMock(resp_cont):
        with pytest.raises(GitlabHttpError):
            gl.http_request("get", "/projects")

    assert call_count == 1


def test_http_request_with_retry_on_method_for_transient_failures(gl):
    call_count = 0
    calls_before_success = 3

    @urlmatch(scheme="http", netloc="localhost", path="/api/v4/projects", method="get")
    def resp_cont(url, request):
        nonlocal call_count
        call_count += 1
        status_code = 200 if call_count == calls_before_success else 500
        return response(
            status_code,
            {"Failure is the stepping stone to success"},
            {},
            None,
            5,
            request,
        )

    with HTTMock(resp_cont):
        http_r = gl.http_request("get", "/projects", retry_transient_errors=True)

        assert http_r.status_code == 200
        assert call_count == calls_before_success


def test_http_request_with_retry_on_class_for_transient_failures(gl_retry):
    call_count = 0
    calls_before_success = 3

    @urlmatch(scheme="http", netloc="localhost", path="/api/v4/projects", method="get")
    def resp_cont(url, request):
        nonlocal call_count
        call_count += 1
        status_code = 200 if call_count == calls_before_success else 500
        return response(
            status_code,
            {"Failure is the stepping stone to success"},
            {},
            None,
            5,
            request,
        )

    with HTTMock(resp_cont):
        http_r = gl_retry.http_request("get", "/projects")

        assert http_r.status_code == 200
        assert call_count == calls_before_success


def test_http_request_with_retry_on_class_and_method_for_transient_failures(gl_retry):
    call_count = 0
    calls_before_success = 3

    @urlmatch(scheme="http", netloc="localhost", path="/api/v4/projects", method="get")
    def resp_cont(url, request):
        nonlocal call_count
        call_count += 1
        status_code = 200 if call_count == calls_before_success else 500
        return response(status_code, {"Here is why it failed"}, {}, None, 5, request)

    with HTTMock(resp_cont):
        with pytest.raises(GitlabHttpError):
            gl_retry.http_request("get", "/projects", retry_transient_errors=False)

        assert call_count == 1


def create_redirect_response(
    *, request: requests.models.PreparedRequest, http_method: str, api_path: str
) -> requests.models.Response:
    """Create a Requests response object that has a redirect in it"""

    assert api_path.startswith("/")
    http_method = http_method.upper()

    # Create a history which contains our original request which is redirected
    history = [
        response(
            status_code=302,
            content="",
            headers={"Location": f"http://example.com/api/v4{api_path}"},
            reason="Moved Temporarily",
            request=request,
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

    resp_obj = response(
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

    @urlmatch(
        scheme="http", netloc="localhost", path=f"/api/v4{api_path}", method=method
    )
    def resp_cont(
        url: str, request: requests.models.PreparedRequest
    ) -> requests.models.Response:
        resp_obj = create_redirect_response(
            request=request, http_method=method, api_path=api_path
        )
        return resp_obj

    with HTTMock(resp_cont):
        gl.http_request(verb=method, path=api_path)


def test_http_request_302_put_raises_redirect_error(gl):
    """Test to show that a redirect of a PUT will cause an error"""

    method = "put"
    api_path = "/user/status"

    @urlmatch(
        scheme="http", netloc="localhost", path=f"/api/v4{api_path}", method=method
    )
    def resp_cont(
        url: str, request: requests.models.PreparedRequest
    ) -> requests.models.Response:
        resp_obj = create_redirect_response(
            request=request, http_method=method, api_path=api_path
        )
        return resp_obj

    with HTTMock(resp_cont):
        with pytest.raises(RedirectError) as exc:
            gl.http_request(verb=method, path=api_path)
        error_message = exc.value.error_message
        assert "Moved Temporarily" in error_message
        assert "http://localhost/api/v4/user/status" in error_message
        assert "http://example.com/api/v4/user/status" in error_message


def test_get_request(gl):
    @urlmatch(scheme="http", netloc="localhost", path="/api/v4/projects", method="get")
    def resp_cont(url: str, request: requests.models.PreparedRequest):
        headers = {"content-type": "application/json"}
        content = '{"name": "project1"}'
        return response(200, content, headers, None, 5, request)

    with HTTMock(resp_cont):
        result = gl.http_get("/projects")
        assert isinstance(result, dict)
        assert result["name"] == "project1"


def test_get_request_raw(gl):
    @urlmatch(scheme="http", netloc="localhost", path="/api/v4/projects", method="get")
    def resp_cont(url, request):
        headers = {"content-type": "application/octet-stream"}
        content = "content"
        return response(200, content, headers, None, 5, request)

    with HTTMock(resp_cont):
        result = gl.http_get("/projects")
        assert result.content.decode("utf-8") == "content"


def test_get_request_404(gl):
    @urlmatch(scheme="http", netloc="localhost", path="/api/v4/not_there", method="get")
    def resp_cont(url, request):
        content = {"Here is why it failed"}
        return response(404, content, {}, None, 5, request)

    with HTTMock(resp_cont):
        with pytest.raises(GitlabHttpError):
            gl.http_get("/not_there")


def test_get_request_invalid_data(gl):
    @urlmatch(scheme="http", netloc="localhost", path="/api/v4/projects", method="get")
    def resp_cont(url, request):
        headers = {"content-type": "application/json"}
        content = '["name": "project1"]'
        return response(200, content, headers, None, 5, request)

    with HTTMock(resp_cont):
        with pytest.raises(GitlabParsingError):
            gl.http_get("/projects")


def test_list_request(gl):
    @urlmatch(scheme="http", netloc="localhost", path="/api/v4/projects", method="get")
    def resp_cont(url, request):
        headers = {"content-type": "application/json", "X-Total": 1}
        content = '[{"name": "project1"}]'
        return response(200, content, headers, None, 5, request)

    with HTTMock(resp_cont):
        result = gl.http_list("/projects", as_list=True)
        assert isinstance(result, list)
        assert len(result) == 1

    with HTTMock(resp_cont):
        result = gl.http_list("/projects", as_list=False)
        assert isinstance(result, GitlabList)
        assert len(result) == 1

    with HTTMock(resp_cont):
        result = gl.http_list("/projects", all=True)
        assert isinstance(result, list)
        assert len(result) == 1


def test_list_request_404(gl):
    @urlmatch(scheme="http", netloc="localhost", path="/api/v4/not_there", method="get")
    def resp_cont(url, request):
        content = {"Here is why it failed"}
        return response(404, content, {}, None, 5, request)

    with HTTMock(resp_cont):
        with pytest.raises(GitlabHttpError):
            gl.http_list("/not_there")


def test_list_request_invalid_data(gl):
    @urlmatch(scheme="http", netloc="localhost", path="/api/v4/projects", method="get")
    def resp_cont(url, request):
        headers = {"content-type": "application/json"}
        content = '["name": "project1"]'
        return response(200, content, headers, None, 5, request)

    with HTTMock(resp_cont):
        with pytest.raises(GitlabParsingError):
            gl.http_list("/projects")


def test_post_request(gl):
    @urlmatch(scheme="http", netloc="localhost", path="/api/v4/projects", method="post")
    def resp_cont(url, request):
        headers = {"content-type": "application/json"}
        content = '{"name": "project1"}'
        return response(200, content, headers, None, 5, request)

    with HTTMock(resp_cont):
        result = gl.http_post("/projects")
        assert isinstance(result, dict)
        assert result["name"] == "project1"


def test_post_request_404(gl):
    @urlmatch(
        scheme="http", netloc="localhost", path="/api/v4/not_there", method="post"
    )
    def resp_cont(url, request):
        content = {"Here is why it failed"}
        return response(404, content, {}, None, 5, request)

    with HTTMock(resp_cont):
        with pytest.raises(GitlabHttpError):
            gl.http_post("/not_there")


def test_post_request_invalid_data(gl):
    @urlmatch(scheme="http", netloc="localhost", path="/api/v4/projects", method="post")
    def resp_cont(url, request):
        headers = {"content-type": "application/json"}
        content = '["name": "project1"]'
        return response(200, content, headers, None, 5, request)

    with HTTMock(resp_cont):
        with pytest.raises(GitlabParsingError):
            gl.http_post("/projects")


def test_put_request(gl):
    @urlmatch(scheme="http", netloc="localhost", path="/api/v4/projects", method="put")
    def resp_cont(url, request):
        headers = {"content-type": "application/json"}
        content = '{"name": "project1"}'
        return response(200, content, headers, None, 5, request)

    with HTTMock(resp_cont):
        result = gl.http_put("/projects")
        assert isinstance(result, dict)
        assert result["name"] == "project1"


def test_put_request_404(gl):
    @urlmatch(scheme="http", netloc="localhost", path="/api/v4/not_there", method="put")
    def resp_cont(url, request):
        content = {"Here is why it failed"}
        return response(404, content, {}, None, 5, request)

    with HTTMock(resp_cont):
        with pytest.raises(GitlabHttpError):
            gl.http_put("/not_there")


def test_put_request_invalid_data(gl):
    @urlmatch(scheme="http", netloc="localhost", path="/api/v4/projects", method="put")
    def resp_cont(url, request):
        headers = {"content-type": "application/json"}
        content = '["name": "project1"]'
        return response(200, content, headers, None, 5, request)

    with HTTMock(resp_cont):
        with pytest.raises(GitlabParsingError):
            gl.http_put("/projects")


def test_delete_request(gl):
    @urlmatch(
        scheme="http", netloc="localhost", path="/api/v4/projects", method="delete"
    )
    def resp_cont(url, request):
        headers = {"content-type": "application/json"}
        content = "true"
        return response(200, content, headers, None, 5, request)

    with HTTMock(resp_cont):
        result = gl.http_delete("/projects")
        assert isinstance(result, requests.Response)
        assert result.json() is True


def test_delete_request_404(gl):
    @urlmatch(
        scheme="http", netloc="localhost", path="/api/v4/not_there", method="delete"
    )
    def resp_cont(url, request):
        content = {"Here is why it failed"}
        return response(404, content, {}, None, 5, request)

    with HTTMock(resp_cont):
        with pytest.raises(GitlabHttpError):
            gl.http_delete("/not_there")

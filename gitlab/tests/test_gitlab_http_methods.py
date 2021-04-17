import pytest
import requests

from httmock import HTTMock, urlmatch, response

from gitlab import *


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
        content = {"Here is wh it failed"}
        return response(404, content, {}, None, 5, request)

    with HTTMock(resp_cont):
        with pytest.raises(GitlabHttpError):
            gl.http_request("get", "/not_there")


def test_get_request(gl):
    @urlmatch(scheme="http", netloc="localhost", path="/api/v4/projects", method="get")
    def resp_cont(url, request):
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
        content = {"Here is wh it failed"}
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
        content = {"Here is wh it failed"}
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
        content = {"Here is wh it failed"}
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
        content = {"Here is wh it failed"}
        return response(404, content, {}, None, 5, request)

    with HTTMock(resp_cont):
        with pytest.raises(GitlabHttpError):
            gl.http_delete("/not_there")

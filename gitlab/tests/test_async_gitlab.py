import httpx
import pytest
import respx
from httpx.status_codes import StatusCode

from gitlab import Gitlab, GitlabList
from gitlab import exceptions as exc


class TestGitlabList:
    @pytest.fixture
    def gl(self):
        return Gitlab("http://localhost", private_token="private_token", api_version=4)

    @respx.mock
    @pytest.mark.asyncio
    async def test_build_list(self, gl):
        request_1 = respx.get(
            "http://localhost/api/v4/tests",
            headers={
                "content-type": "application/json",
                "X-Page": "1",
                "X-Next-Page": "2",
                "X-Per-Page": "1",
                "X-Total-Pages": "2",
                "X-Total": "2",
                "Link": (
                    "<http://localhost/api/v4/tests?per_page=1&page=2>;" ' rel="next"'
                ),
            },
            content=[{"a": "b"}],
            status_code=StatusCode.OK,
        )
        request_2 = respx.get(
            "http://localhost/api/v4/tests?per_page=1&page=2",
            headers={
                "content-type": "application/json",
                "X-Page": "2",
                "X-Next-Page": "2",
                "X-Per-Page": "1",
                "X-Total-Pages": "2",
                "X-Total": "2",
            },
            content=[{"c": "d"}],
            status_code=StatusCode.OK,
        )

        obj = await gl.http_list("/tests", as_list=False)
        assert len(obj) == 2
        assert obj._next_url == "http://localhost/api/v4/tests?per_page=1&page=2"
        assert obj.current_page == 1
        assert obj.prev_page == None
        assert obj.next_page == 2
        assert obj.per_page == 1
        assert obj.total_pages == 2
        assert obj.total == 2

        l = await obj.as_list()
        assert len(l) == 2
        assert l[0]["a"] == "b"
        assert l[1]["c"] == "d"

    @respx.mock
    @pytest.mark.asyncio
    async def test_all_ommited_when_as_list(self, gl):
        request = respx.get(
            "http://localhost/api/v4/tests",
            headers={
                "content-type": "application/json",
                "X-Page": "2",
                "X-Next-Page": "2",
                "X-Per-Page": "1",
                "X-Total-Pages": "2",
                "X-Total": "2",
            },
            content=[{"c": "d"}],
            status_code=StatusCode.OK,
        )

        result = await gl.http_list("/tests", as_list=False, all=True)
        assert isinstance(result, GitlabList)


class TestGitlabHttpMethods:
    @pytest.fixture
    def gl(self):
        return Gitlab("http://localhost", private_token="private_token", api_version=4)

    @respx.mock
    @pytest.mark.asyncio
    async def test_http_request(self, gl):
        request = respx.get(
            "http://localhost/api/v4/projects",
            headers={"content-type": "application/json"},
            content=[{"name": "project1"}],
            status_code=StatusCode.OK,
        )

        http_r = await gl.http_request("get", "/projects")
        http_r.json()
        assert http_r.status_code == StatusCode.OK

    @respx.mock
    @pytest.mark.asyncio
    async def test_get_request(self, gl):
        request = respx.get(
            "http://localhost/api/v4/projects",
            headers={"content-type": "application/json"},
            content={"name": "project1"},
            status_code=StatusCode.OK,
        )

        result = await gl.http_get("/projects")
        assert isinstance(result, dict)
        assert result["name"] == "project1"

    @respx.mock
    @pytest.mark.asyncio
    async def test_get_request_raw(self, gl):
        request = respx.get(
            "http://localhost/api/v4/projects",
            headers={"content-type": "application/octet-stream"},
            content="content",
            status_code=StatusCode.OK,
        )

        result = await gl.http_get("/projects")
        assert result.content.decode("utf-8") == "content"

    @respx.mock
    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "respx_params, gl_exc, path",
        [
            (
                {
                    "url": "http://localhost/api/v4/not_there",
                    "content": "Here is why it failed",
                    "status_code": StatusCode.NOT_FOUND,
                },
                exc.GitlabHttpError,
                "/not_there",
            ),
            (
                {
                    "url": "http://localhost/api/v4/projects",
                    "headers": {"content-type": "application/json"},
                    "content": '["name": "project1"]',
                    "status_code": StatusCode.OK,
                },
                exc.GitlabParsingError,
                "/projects",
            ),
        ],
    )
    @pytest.mark.parametrize(
        "http_method, gl_method",
        [
            ("get", "http_get"),
            ("get", "http_list"),
            ("post", "http_post"),
            ("put", "http_put"),
        ],
    )
    async def test_errors(self, gl, http_method, gl_method, respx_params, gl_exc, path):
        request = getattr(respx, http_method)(**respx_params)

        with pytest.raises(gl_exc):
            http_r = await getattr(gl, gl_method)(path)

    @respx.mock
    @pytest.mark.asyncio
    async def test_list_request(self, gl):
        request = respx.get(
            "http://localhost/api/v4/projects",
            headers={"content-type": "application/json", "X-Total": "1"},
            content=[{"name": "project1"}],
            status_code=StatusCode.OK,
        )

        result = await gl.http_list("/projects", as_list=True)
        assert isinstance(result, list)
        assert len(result) == 1

        result = await gl.http_list("/projects", as_list=False)
        assert isinstance(result, GitlabList)
        assert len(result) == 1

        result = await gl.http_list("/projects", all=True)
        assert isinstance(result, list)
        assert len(result) == 1

    @respx.mock
    @pytest.mark.asyncio
    async def test_post_request(self, gl):
        request = respx.post(
            "http://localhost/api/v4/projects",
            headers={"content-type": "application/json"},
            content={"name": "project1"},
            status_code=StatusCode.OK,
        )

        result = await gl.http_post("/projects")
        assert isinstance(result, dict)
        assert result["name"] == "project1"

    @respx.mock
    @pytest.mark.asyncio
    async def test_put_request(self, gl):
        request = respx.put(
            "http://localhost/api/v4/projects",
            headers={"content-type": "application/json"},
            content='{"name": "project1"}',
            status_code=StatusCode.OK,
        )
        result = await gl.http_put("/projects")
        assert isinstance(result, dict)
        assert result["name"] == "project1"

    @respx.mock
    @pytest.mark.asyncio
    async def test_delete_request(self, gl):
        request = respx.delete(
            "http://localhost/api/v4/projects",
            headers={"content-type": "application/json"},
            content="true",
            status_code=StatusCode.OK,
        )

        result = await gl.http_delete("/projects")
        assert isinstance(result, httpx.Response)
        assert result.json() is True

    @respx.mock
    @pytest.mark.asyncio
    async def test_delete_request_404(self, gl):
        result = respx.delete(
            "http://localhost/api/v4/not_there",
            content="Here is why it failed",
            status_code=StatusCode.NOT_FOUND,
        )

        with pytest.raises(exc.GitlabHttpError):
            await gl.http_delete("/not_there")

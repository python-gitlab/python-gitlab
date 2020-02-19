import pytest
import respx
from httpx import status_codes
from httpx.status_codes import StatusCode

from gitlab import Gitlab, GitlabList


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

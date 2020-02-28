import pytest
import respx
from httpx.status_codes import StatusCode

from gitlab import AsyncGitlab


class TestProjectSnippets:
    @pytest.fixture
    def gl(self):
        return AsyncGitlab(
            "http://localhost",
            private_token="private_token",
            ssl_verify=True,
            api_version=4,
        )

    @respx.mock
    @pytest.mark.asyncio
    async def test_list_project_snippets(self, gl):
        title = "Example Snippet Title"
        visibility = "private"
        request = respx.get(
            "http://localhost/api/v4/projects/1/snippets",
            content=[
                {
                    "title": title,
                    "description": "More verbose snippet description",
                    "file_name": "example.txt",
                    "content": "source code with multiple lines",
                    "visibility": visibility,
                }
            ],
            status_code=StatusCode.OK,
        )

        project = gl.projects.get(1, lazy=True)
        snippets = await project.snippets.list()
        assert len(snippets) == 1
        assert snippets[0].title == title
        assert snippets[0].visibility == visibility

    @respx.mock
    @pytest.mark.asyncio
    async def test_get_project_snippet(self, gl):
        title = "Example Snippet Title"
        visibility = "private"
        request = respx.get(
            "http://localhost/api/v4/projects/1/snippets/1",
            content={
                "title": title,
                "description": "More verbose snippet description",
                "file_name": "example.txt",
                "content": "source code with multiple lines",
                "visibility": visibility,
            },
            status_code=StatusCode.OK,
        )

        project = gl.projects.get(1, lazy=True)
        snippet = await project.snippets.get(1)
        assert snippet.title == title
        assert snippet.visibility == visibility

    @respx.mock
    @pytest.mark.asyncio
    async def test_create_update_project_snippets(self, gl):
        title = "Example Snippet Title"
        new_title = "new-title"
        visibility = "private"
        request_update = respx.put(
            "http://localhost/api/v4/projects/1/snippets",
            content={
                "title": new_title,
                "description": "More verbose snippet description",
                "file_name": "example.txt",
                "content": "source code with multiple lines",
                "visibility": visibility,
            },
            status_code=StatusCode.OK,
        )

        request_create = respx.post(
            "http://localhost/api/v4/projects/1/snippets",
            content={
                "title": title,
                "description": "More verbose snippet description",
                "file_name": "example.txt",
                "content": "source code with multiple lines",
                "visibility": visibility,
            },
            status_code=StatusCode.OK,
        )

        project = gl.projects.get(1, lazy=True)
        snippet = await project.snippets.create(
            {
                "title": title,
                "file_name": title,
                "content": title,
                "visibility": visibility,
            }
        )
        assert snippet.title == title
        assert snippet.visibility == visibility

        snippet.title = new_title
        await snippet.save()
        assert snippet.title == new_title
        assert snippet.visibility == visibility

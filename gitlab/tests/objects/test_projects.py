import pytest
import respx
from httpx.status_codes import StatusCode

from gitlab import AsyncGitlab


class TestProjectSnippets:
    @respx.mock
    @pytest.mark.asyncio
    async def test_list_project_snippets(self, gl, gl_get_value):
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
        snippets = project.snippets.list()
        snippets = await gl_get_value(snippets)

        assert len(snippets) == 1
        assert snippets[0].title == title
        assert snippets[0].visibility == visibility

    @respx.mock
    @pytest.mark.asyncio
    async def test_get_project_snippet(self, gl, gl_get_value):
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
        snippet = project.snippets.get(1)
        snippet = await gl_get_value(snippet)
        assert snippet.title == title
        assert snippet.visibility == visibility

    @respx.mock
    @pytest.mark.asyncio
    async def test_create_update_project_snippets(self, gl, gl_get_value, is_gl_sync):
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
        snippet = project.snippets.create(
            {
                "title": title,
                "file_name": title,
                "content": title,
                "visibility": visibility,
            }
        )
        snippet = await gl_get_value(snippet)
        assert snippet.title == title
        assert snippet.visibility == visibility

        snippet.title = new_title
        if is_gl_sync:
            snippet.save()
        else:
            await snippet.save()
        assert snippet.title == new_title
        assert snippet.visibility == visibility

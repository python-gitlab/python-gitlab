"""
GitLab API: https://docs.gitlab.com/ce/api/project_snippets.html
             https://docs.gitlab.com/ee/api/snippets.html (todo)
"""

import pytest
import responses

title = "Example Snippet Title"
visibility = "private"
new_title = "new-title"


@pytest.fixture
def resp_snippet():
    content = {
        "title": title,
        "description": "More verbose snippet description",
        "file_name": "example.txt",
        "content": "source code with multiple lines",
        "visibility": visibility,
    }

    with responses.RequestsMock(assert_all_requests_are_fired=False) as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/projects/1/snippets",
            json=[content],
            content_type="application/json",
            status=200,
        )
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/projects/1/snippets/1",
            json=content,
            content_type="application/json",
            status=200,
        )
        rsps.add(
            method=responses.POST,
            url="http://localhost/api/v4/projects/1/snippets",
            json=content,
            content_type="application/json",
            status=200,
        )

        updated_content = dict(content)
        updated_content["title"] = new_title
        updated_content["visibility"] = visibility

        rsps.add(
            method=responses.PUT,
            url="http://localhost/api/v4/projects/1/snippets",
            json=updated_content,
            content_type="application/json",
            status=200,
        )
        yield rsps


def test_list_project_snippets(project, resp_snippet):
    snippets = project.snippets.list()
    assert len(snippets) == 1
    assert snippets[0].title == title
    assert snippets[0].visibility == visibility


def test_get_project_snippet(project, resp_snippet):
    snippet = project.snippets.get(1)
    assert snippet.title == title
    assert snippet.visibility == visibility


def test_create_update_project_snippets(project, resp_snippet):
    snippet = project.snippets.create(
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
    snippet.save()
    assert snippet.title == new_title
    assert snippet.visibility == visibility

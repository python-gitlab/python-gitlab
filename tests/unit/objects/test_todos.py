"""
GitLab API: https://docs.gitlab.com/ce/api/todos.html
"""

import pytest
import responses

from gitlab.v4.objects import Todo


@pytest.fixture
def json_content():
    return [
        {
            "id": 102,
            "project": {
                "id": 2,
                "name": "Gitlab Ce",
                "name_with_namespace": "Gitlab Org / Gitlab Ce",
                "path": "gitlab-ce",
                "path_with_namespace": "gitlab-org/gitlab-ce",
            },
            "author": {
                "name": "Administrator",
                "username": "root",
                "id": 1,
            },
            "action_name": "marked",
            "target_type": "MergeRequest",
            "target": {
                "id": 34,
                "iid": 7,
                "project_id": 2,
                "assignee": {
                    "name": "Administrator",
                    "username": "root",
                    "id": 1,
                },
            },
        }
    ]


@pytest.fixture
def resp_todo(json_content):
    with responses.RequestsMock(assert_all_requests_are_fired=False) as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/todos",
            json=json_content,
            content_type="application/json",
            status=200,
        )
        rsps.add(
            method=responses.POST,
            url="http://localhost/api/v4/todos/102/mark_as_done",
            json=json_content[0],
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_mark_all_as_done():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.POST,
            url="http://localhost/api/v4/todos/mark_as_done",
            status=204,
        )
        yield rsps


def test_todo(gl, resp_todo):
    todo = gl.todos.list()[0]
    assert isinstance(todo, Todo)
    assert todo.id == 102
    assert todo.target_type == "MergeRequest"
    assert todo.target["assignee"]["username"] == "root"

    todo.mark_as_done()


def test_todo_mark_all_as_done(gl, resp_mark_all_as_done):
    gl.todos.mark_all_as_done()

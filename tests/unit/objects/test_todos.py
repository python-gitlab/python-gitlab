"""
GitLab API: https://docs.gitlab.com/ce/api/todos.html
"""

import json

import pytest
import responses

from gitlab.v4.objects import Todo


@pytest.fixture()
def json_content(fixture_dir):
    with open(fixture_dir / "todo.json", "r", encoding="utf-8") as f:
        todo_content = f.read()
        return json.loads(todo_content)


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
            json={},
            content_type="application/json",
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

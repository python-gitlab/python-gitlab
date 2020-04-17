"""
GitLab API: https://docs.gitlab.com/ce/api/todos.html
"""

import json
import os

from httmock import response, urlmatch, with_httmock

from gitlab.v4.objects import Todo

from .mocks import headers


with open(os.path.dirname(__file__) + "/../data/todo.json", "r") as json_file:
    todo_content = json_file.read()
    json_content = json.loads(todo_content)
    encoded_content = todo_content.encode("utf-8")


@urlmatch(scheme="http", netloc="localhost", path="/api/v4/todos", method="get")
def resp_get_todo(url, request):
    return response(200, encoded_content, headers, None, 5, request)


@urlmatch(
    scheme="http",
    netloc="localhost",
    path="/api/v4/todos/102/mark_as_done",
    method="post",
)
def resp_mark_as_done(url, request):
    single_todo = json.dumps(json_content[0])
    content = single_todo.encode("utf-8")
    return response(200, content, headers, None, 5, request)


@urlmatch(
    scheme="http", netloc="localhost", path="/api/v4/todos/mark_as_done", method="post",
)
def resp_mark_all_as_done(url, request):
    return response(204, {}, headers, None, 5, request)


@with_httmock(resp_get_todo, resp_mark_as_done)
def test_todo(gl):
    todo = gl.todos.list()[0]
    assert isinstance(todo, Todo)
    assert todo.id == 102
    assert todo.target_type == "MergeRequest"
    assert todo.target["assignee"]["username"] == "root"

    todo.mark_as_done()


@with_httmock(resp_mark_all_as_done)
def test_todo_mark_all_as_done(gl):
    gl.todos.mark_all_as_done()

"""
GitLab API: https://docs.gitlab.com/ce/api/repository_submodules.html
"""

from httmock import response, urlmatch, with_httmock

from gitlab.v4.objects import Project

from .mocks import headers


@urlmatch(scheme="http", netloc="localhost", path="/api/v4/projects/1$", method="get")
def resp_get_project(url, request):
    content = '{"name": "name", "id": 1}'.encode("utf-8")
    return response(200, content, headers, None, 5, request)


@urlmatch(
    scheme="http",
    netloc="localhost",
    path="/api/v4/projects/1/repository/submodules/foo%2Fbar",
    method="put",
)
def resp_update_submodule(url, request):
    content = """{
    "id": "ed899a2f4b50b4370feeea94676502b42383c746",
    "short_id": "ed899a2f4b5",
    "title": "Message",
    "author_name": "Author",
    "author_email": "author@example.com",
    "committer_name": "Author",
    "committer_email": "author@example.com",
    "created_at": "2018-09-20T09:26:24.000-07:00",
    "message": "Message",
    "parent_ids": [ "ae1d9fb46aa2b07ee9836d49862ec4e2c46fbbba" ],
    "committed_date": "2018-09-20T09:26:24.000-07:00",
    "authored_date": "2018-09-20T09:26:24.000-07:00",
    "status": null}"""
    content = content.encode("utf-8")
    return response(200, content, headers, None, 5, request)


@with_httmock(resp_get_project, resp_update_submodule)
def test_update_submodule(gl):
    project = gl.projects.get(1)
    assert isinstance(project, Project)
    assert project.name == "name"
    assert project.id == 1

    ret = project.update_submodule(
        submodule="foo/bar",
        branch="master",
        commit_sha="4c3674f66071e30b3311dac9b9ccc90502a72664",
        commit_message="Message",
    )
    assert isinstance(ret, dict)
    assert ret["message"] == "Message"
    assert ret["id"] == "ed899a2f4b50b4370feeea94676502b42383c746"

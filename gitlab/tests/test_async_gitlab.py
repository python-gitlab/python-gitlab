import json
import os
import re

import httpx
import pytest
import respx
from httpx.status_codes import StatusCode

from gitlab import AsyncGitlab, Gitlab
from gitlab import exceptions as exc
from gitlab.types import GitlabList
from gitlab.v4.objects import (
    CurrentUser,
    Group,
    Hook,
    Project,
    ProjectAdditionalStatistics,
    ProjectEnvironment,
    ProjectIssuesStatistics,
    Todo,
    User,
    UserStatus,
)

sync_gitlab = Gitlab("http://localhost", private_token="private_token", api_version=4)
async_gitlab = AsyncGitlab(
    "http://localhost", private_token="private_token", api_version=4
)


@pytest.mark.parametrize(
    "gl, sync", [(sync_gitlab, True), (async_gitlab, False),],
)
class TestGitlabList:
    @respx.mock
    @pytest.mark.asyncio
    async def test_build_list(self, gl, sync):
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
        obj = gl.http_list("/tests", as_list=False)
        if not sync:
            obj = await obj

        assert len(obj) == 2
        assert obj._next_url == "http://localhost/api/v4/tests?per_page=1&page=2"
        assert obj.current_page == 1
        assert obj.prev_page is None
        assert obj.next_page == 2
        assert obj.per_page == 1
        assert obj.total_pages == 2
        assert obj.total == 2

        if not sync:
            l = await obj.as_list()
        else:
            l = list(obj)

        assert len(l) == 2
        assert l[0]["a"] == "b"
        assert l[1]["c"] == "d"

    @respx.mock
    @pytest.mark.asyncio
    async def test_all_ommited_when_as_list(self, gl, sync):
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

        result = gl.http_list("/tests", as_list=False, all=True)
        if not sync:
            result = await result

        assert isinstance(result, GitlabList)


@pytest.mark.parametrize(
    "gl, sync", [(sync_gitlab, True), (async_gitlab, False),],
)
class TestGitlabHttpMethods:
    @respx.mock
    @pytest.mark.asyncio
    async def test_http_request(self, gl, sync):
        request = respx.get(
            "http://localhost/api/v4/projects",
            headers={"content-type": "application/json"},
            content=[{"name": "project1"}],
            status_code=StatusCode.OK,
        )

        http_r = gl.http_request("get", "/projects")
        if not sync:
            http_r = await http_r
        http_r.json()
        assert http_r.status_code == StatusCode.OK

    @respx.mock
    @pytest.mark.asyncio
    async def test_get_request(self, gl, sync):
        request = respx.get(
            "http://localhost/api/v4/projects",
            headers={"content-type": "application/json"},
            content={"name": "project1"},
            status_code=StatusCode.OK,
        )

        result = gl.http_get("/projects")
        if not sync:
            result = await result
        assert isinstance(result, dict)
        assert result["name"] == "project1"

    @respx.mock
    @pytest.mark.asyncio
    async def test_get_request_raw(self, gl, sync):
        request = respx.get(
            "http://localhost/api/v4/projects",
            headers={"content-type": "application/octet-stream"},
            content="content",
            status_code=StatusCode.OK,
        )

        result = gl.http_get("/projects")
        if not sync:
            result = await result
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
    async def test_errors(
        self, gl, sync, http_method, gl_method, respx_params, gl_exc, path
    ):
        request = getattr(respx, http_method)(**respx_params)

        with pytest.raises(gl_exc):
            http_r = getattr(gl, gl_method)(path)
            if not sync:
                await http_r

    @respx.mock
    @pytest.mark.asyncio
    async def test_list_request(self, gl, sync):
        request = respx.get(
            "http://localhost/api/v4/projects",
            headers={"content-type": "application/json", "X-Total": "1"},
            content=[{"name": "project1"}],
            status_code=StatusCode.OK,
        )

        result = gl.http_list("/projects", as_list=True)
        if not sync:
            result = await result
        assert isinstance(result, list)
        assert len(result) == 1

        result = gl.http_list("/projects", as_list=False)
        if not sync:
            result = await result
        assert isinstance(result, GitlabList)
        assert len(result) == 1

        result = gl.http_list("/projects", all=True)
        if not sync:
            result = await result
        assert isinstance(result, list)
        assert len(result) == 1

    @respx.mock
    @pytest.mark.asyncio
    async def test_post_request(self, gl, sync):
        request = respx.post(
            "http://localhost/api/v4/projects",
            headers={"content-type": "application/json"},
            content={"name": "project1"},
            status_code=StatusCode.OK,
        )

        result = gl.http_post("/projects")
        if not sync:
            result = await result

        assert isinstance(result, dict)
        assert result["name"] == "project1"

    @respx.mock
    @pytest.mark.asyncio
    async def test_put_request(self, gl, sync):
        request = respx.put(
            "http://localhost/api/v4/projects",
            headers={"content-type": "application/json"},
            content='{"name": "project1"}',
            status_code=StatusCode.OK,
        )
        result = gl.http_put("/projects")
        if not sync:
            result = await result

        assert isinstance(result, dict)
        assert result["name"] == "project1"

    @respx.mock
    @pytest.mark.asyncio
    async def test_delete_request(self, gl, sync):
        request = respx.delete(
            "http://localhost/api/v4/projects",
            headers={"content-type": "application/json"},
            content="true",
            status_code=StatusCode.OK,
        )

        result = gl.http_delete("/projects")
        if not sync:
            result = await result

        assert isinstance(result, httpx.Response)
        assert result.json() is True

    @respx.mock
    @pytest.mark.asyncio
    async def test_delete_request_404(self, gl, sync):
        result = respx.delete(
            "http://localhost/api/v4/not_there",
            content="Here is why it failed",
            status_code=StatusCode.NOT_FOUND,
        )

        with pytest.raises(exc.GitlabHttpError):
            r = gl.http_delete("/not_there")
            if not sync:
                await r


@pytest.mark.parametrize(
    "gl, sync", [(sync_gitlab, True), (async_gitlab, False),],
)
class TestGitlab:
    @respx.mock
    @pytest.mark.asyncio
    async def test_token_auth(self, gl, sync):
        name = "username"
        id_ = 1

        request = respx.get(
            "http://localhost/api/v4/user",
            headers={"content-type": "application/json"},
            content='{{"id": {0:d}, "username": "{1:s}"}}'.format(id_, name).encode(
                "utf-8"
            ),
            status_code=StatusCode.OK,
        )

        if sync:
            gl.auth()
        else:
            await gl.auth()
        assert isinstance(gl.user, CurrentUser)
        assert gl.user.username == name
        assert gl.user.id == id_

    @respx.mock
    @pytest.mark.asyncio
    async def test_hooks(self, gl, sync):
        request = respx.get(
            "http://localhost/api/v4/hooks/1",
            headers={"content-type": "application/json"},
            content='{"url": "testurl", "id": 1}'.encode("utf-8"),
            status_code=StatusCode.OK,
        )

        data = gl.hooks.get(1)
        if not sync:
            data = await data
        assert isinstance(data, Hook)
        assert data.url == "testurl"
        assert data.id == 1

    @respx.mock
    @pytest.mark.asyncio
    async def test_projects(self, gl, sync):
        request = respx.get(
            "http://localhost/api/v4/projects/1",
            headers={"content-type": "application/json"},
            content='{"name": "name", "id": 1}'.encode("utf-8"),
            status_code=StatusCode.OK,
        )

        data = gl.projects.get(1)
        if not sync:
            data = await data
        assert isinstance(data, Project)
        assert data.name == "name"
        assert data.id == 1

    @respx.mock
    @pytest.mark.asyncio
    async def test_project_environments(self, gl, sync):
        request_get_project = respx.get(
            "http://localhost/api/v4/projects/1",
            headers={"content-type": "application/json"},
            content='{"name": "name", "id": 1}'.encode("utf-8"),
            status_code=StatusCode.OK,
        )
        request_get_environment = respx.get(
            "http://localhost/api/v4/projects/1/environments/1",
            headers={"content-type": "application/json"},
            content='{"name": "environment_name", "id": 1, "last_deployment": "sometime"}'.encode(
                "utf-8"
            ),
            status_code=StatusCode.OK,
        )

        project = gl.projects.get(1)
        if not sync:
            project = await project
        environment = project.environments.get(1)
        if not sync:
            environment = await environment

        assert isinstance(environment, ProjectEnvironment)
        assert environment.id == 1
        assert environment.last_deployment == "sometime"
        assert environment.name == "environment_name"

    @respx.mock
    @pytest.mark.asyncio
    async def test_project_additional_statistics(self, gl, sync):
        request_get_project = respx.get(
            "http://localhost/api/v4/projects/1",
            headers={"content-type": "application/json"},
            content='{"name": "name", "id": 1}'.encode("utf-8"),
            status_code=StatusCode.OK,
        )
        request_get_environment = respx.get(
            "http://localhost/api/v4/projects/1/statistics",
            headers={"content-type": "application/json"},
            content="""{"fetches": {"total": 50, "days": [{"count": 10, "date": "2018-01-10"}]}}""".encode(
                "utf-8"
            ),
            status_code=StatusCode.OK,
        )
        project = gl.projects.get(1)
        if not sync:
            project = await project
        statistics = project.additionalstatistics.get()
        if not sync:
            statistics = await statistics
        assert isinstance(statistics, ProjectAdditionalStatistics)
        assert statistics.fetches["total"] == 50

    @respx.mock
    @pytest.mark.asyncio
    async def test_project_issues_statistics(self, gl, sync):
        request_get_project = respx.get(
            "http://localhost/api/v4/projects/1",
            headers={"content-type": "application/json"},
            content='{"name": "name", "id": 1}'.encode("utf-8"),
            status_code=StatusCode.OK,
        )
        request_get_environment = respx.get(
            "http://localhost/api/v4/projects/1/issues_statistics",
            headers={"content-type": "application/json"},
            content="""{"statistics": {"counts": {"all": 20, "closed": 5, "opened": 15}}}""".encode(
                "utf-8"
            ),
            status_code=StatusCode.OK,
        )

        project = gl.projects.get(1)
        if not sync:
            project = await project
        statistics = project.issuesstatistics.get()
        if not sync:
            statistics = await statistics

        assert isinstance(statistics, ProjectIssuesStatistics)
        assert statistics.statistics["counts"]["all"] == 20

    @respx.mock
    @pytest.mark.asyncio
    async def test_groups(self, gl, sync):
        request = respx.get(
            "http://localhost/api/v4/groups/1",
            headers={"content-type": "application/json"},
            content='{"name": "name", "id": 1, "path": "path"}'.encode("utf-8"),
            status_code=StatusCode.OK,
        )

        data = gl.groups.get(1)
        if not sync:
            data = await data
        assert isinstance(data, Group)
        assert data.name == "name"
        assert data.path == "path"
        assert data.id == 1

    @respx.mock
    @pytest.mark.asyncio
    async def test_issues(self, gl, sync):
        request = respx.get(
            "http://localhost/api/v4/issues",
            headers={"content-type": "application/json"},
            content='[{"name": "name", "id": 1}, '
            '{"name": "other_name", "id": 2}]'.encode("utf-8"),
            status_code=StatusCode.OK,
        )

        data = gl.issues.list()
        if not sync:
            data = await data
        assert data[1].id == 2
        assert data[1].name == "other_name"

    @pytest.fixture
    def respx_get_user_params(self):
        return {
            "url": "http://localhost/api/v4/users/1",
            "headers": {"content-type": "application/json"},
            "content": (
                '{"name": "name", "id": 1, "password": "password", '
                '"username": "username", "email": "email"}'.encode("utf-8")
            ),
            "status_code": StatusCode.OK,
        }

    @respx.mock
    @pytest.mark.asyncio
    async def test_users(self, gl, sync, respx_get_user_params):
        request = respx.get(**respx_get_user_params)

        user = gl.users.get(1)
        if not sync:
            user = await user

        assert isinstance(user, User)
        assert user.name == "name"
        assert user.id == 1

    @respx.mock
    @pytest.mark.asyncio
    async def test_user_status(self, gl, sync, respx_get_user_params):
        request_user_status = respx.get(
            "http://localhost/api/v4/users/1/status",
            headers={"content-type": "application/json"},
            content='{"message": "test", "message_html": "<h1>Message</h1>", "emoji": "thumbsup"}'.encode(
                "utf-8"
            ),
            status_code=StatusCode.OK,
        )
        request_user = respx.get(**respx_get_user_params)

        user = gl.users.get(1)
        if not sync:
            user = await user
        status = user.status.get()
        if not sync:
            status = await status

        assert isinstance(status, UserStatus)
        assert status.message == "test"
        assert status.emoji == "thumbsup"

    @respx.mock
    @pytest.mark.asyncio
    async def test_todo(self, gl, sync):
        with open(os.path.dirname(__file__) + "/data/todo.json", "r") as json_file:
            todo_content = json_file.read()
            json_content = json.loads(todo_content)
            encoded_content = todo_content.encode("utf-8")

        request_get_todo = respx.get(
            "http://localhost/api/v4/todos",
            headers={"content-type": "application/json"},
            content=encoded_content,
            status_code=StatusCode.OK,
        )
        request_mark_as_done = respx.post(
            "http://localhost/api/v4/todos/102/mark_as_done",
            headers={"content-type": "application/json"},
            content=json.dumps(json_content[0]).encode("utf-8"),
            status_code=StatusCode.OK,
        )

        todo_list = gl.todos.list()
        if not sync:
            todo_list = await todo_list
        todo = todo_list[0]
        assert isinstance(todo, Todo)
        assert todo.id == 102
        assert todo.target_type == "MergeRequest"
        assert todo.target["assignee"]["username"] == "root"
        if sync:
            todo.mark_as_done()
        else:
            await todo.mark_as_done()

    @respx.mock
    @pytest.mark.asyncio
    async def test_todo_mark_all_as_done(self, gl, sync):
        request = respx.post(
            "http://localhost/api/v4/todos/mark_as_done",
            headers={"content-type": "application/json"},
            content={},
        )

        if sync:
            gl.todos.mark_all_as_done()
        else:
            await gl.todos.mark_all_as_done()

    @respx.mock
    @pytest.mark.asyncio
    async def test_deployment(self, gl, sync):

        content = '{"id": 42, "status": "success", "ref": "master"}'
        json_content = json.loads(content)

        request_deployment_create = respx.post(
            "http://localhost/api/v4/projects/1/deployments",
            headers={"content-type": "application/json"},
            content=json_content,
            status_code=StatusCode.OK,
        )

        project = gl.projects.get(1, lazy=True)
        deployment = project.deployments.create(
            {
                "environment": "Test",
                "sha": "1agf4gs",
                "ref": "master",
                "tag": False,
                "status": "created",
            }
        )
        if not sync:
            deployment = await deployment
        assert deployment.id == 42
        assert deployment.status == "success"
        assert deployment.ref == "master"

        json_content["status"] = "failed"
        request_deployment_update = respx.put(
            "http://localhost/api/v4/projects/1/deployments/42",
            headers={"content-type": "application/json"},
            content=json_content,
            status_code=StatusCode.OK,
        )
        if not sync:
            request_deployment_update = await request_deployment_update
        deployment.status = "failed"

        if sync:
            deployment.save()
        else:
            await deployment.save()

        assert deployment.status == "failed"

    @respx.mock
    @pytest.mark.asyncio
    async def test_user_activate_deactivate(self, gl, sync):
        request_activate = respx.post(
            "http://localhost/api/v4/users/1/activate",
            headers={"content-type": "application/json"},
            content={},
            status_code=StatusCode.CREATED,
        )
        request_deactivate = respx.post(
            "http://localhost/api/v4/users/1/deactivate",
            headers={"content-type": "application/json"},
            content={},
            status_code=StatusCode.CREATED,
        )

        user = gl.users.get(1, lazy=True)
        if sync:
            user.activate()
            user.deactivate()
        else:
            await user.activate()
            await user.deactivate()

    @respx.mock
    @pytest.mark.asyncio
    async def test_update_submodule(self, gl, sync):
        request_get_project = respx.get(
            "http://localhost/api/v4/projects/1",
            headers={"content-type": "application/json"},
            content='{"name": "name", "id": 1}'.encode("utf-8"),
            status_code=StatusCode.OK,
        )
        request_update_submodule = respx.put(
            "http://localhost/api/v4/projects/1/repository/submodules/foo%2Fbar",
            headers={"content-type": "application/json"},
            content="""{
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
            "status": null}""".encode(
                "utf-8"
            ),
            status_code=StatusCode.OK,
        )
        project = gl.projects.get(1)
        if not sync:
            project = await project
        assert isinstance(project, Project)
        assert project.name == "name"
        assert project.id == 1

        ret = project.update_submodule(
            submodule="foo/bar",
            branch="master",
            commit_sha="4c3674f66071e30b3311dac9b9ccc90502a72664",
            commit_message="Message",
        )
        if not sync:
            ret = await ret
        assert isinstance(ret, dict)
        assert ret["message"] == "Message"
        assert ret["id"] == "ed899a2f4b50b4370feeea94676502b42383c746"

    @respx.mock
    @pytest.mark.asyncio
    async def test_import_github(self, gl, sync):
        request = respx.post(
            re.compile(r"^http://localhost/api/v4/import/github"),
            headers={"content-type": "application/json"},
            content="""{
            "id": 27,
            "name": "my-repo",
            "full_path": "/root/my-repo",
            "full_name": "Administrator / my-repo"
            }""".encode(
                "utf-8"
            ),
            status_code=StatusCode.OK,
        )
        base_path = "/root"
        name = "my-repo"
        ret = gl.projects.import_github("githubkey", 1234, base_path, name)
        if not sync:
            ret = await ret
        assert isinstance(ret, dict)
        assert ret["name"] == name
        assert ret["full_path"] == "/".join((base_path, name))
        assert ret["full_name"].endswith(name)

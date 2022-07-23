import re

import pytest
import responses

import gitlab
from gitlab.v4.objects.runners import Runner, RunnerAll

runner_detail = {
    "active": True,
    "architecture": "amd64",
    "description": "test-1-20150125",
    "id": 6,
    "ip_address": "127.0.0.1",
    "is_shared": False,
    "contacted_at": "2016-01-25T16:39:48.066Z",
    "name": "test-runner",
    "online": True,
    "status": "online",
    "platform": "linux",
    "projects": [
        {
            "id": 1,
            "name": "GitLab Community Edition",
            "name_with_namespace": "GitLab.org / GitLab Community Edition",
            "path": "gitlab-foss",
            "path_with_namespace": "gitlab-org/gitlab-foss",
        }
    ],
    "revision": "5nj35",
    "tag_list": ["ruby", "mysql"],
    "version": "v13.0.0",
    "access_level": "ref_protected",
    "maximum_timeout": 3600,
}

runner_shortinfo = {
    "active": True,
    "description": "test-1-20150125",
    "id": 6,
    "is_shared": False,
    "ip_address": "127.0.0.1",
    "name": "test-name",
    "online": True,
    "status": "online",
}

runner_jobs = [
    {
        "id": 6,
        "ip_address": "127.0.0.1",
        "status": "running",
        "stage": "test",
        "name": "test",
        "ref": "main",
        "tag": False,
        "coverage": "99%",
        "created_at": "2017-11-16T08:50:29.000Z",
        "started_at": "2017-11-16T08:51:29.000Z",
        "finished_at": "2017-11-16T08:53:29.000Z",
        "duration": 120,
        "user": {
            "id": 1,
            "name": "John Doe2",
            "username": "user2",
            "state": "active",
            "avatar_url": "http://www.gravatar.com/avatar/c922747a93b40d1ea88262bf1aebee62?s=80&d=identicon",
            "web_url": "http://localhost/user2",
            "created_at": "2017-11-16T18:38:46.000Z",
            "bio": None,
            "location": None,
            "public_email": "",
            "skype": "",
            "linkedin": "",
            "twitter": "",
            "website_url": "",
            "organization": None,
        },
    }
]


@pytest.fixture
def resp_get_runners_jobs():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/runners/6/jobs",
            json=runner_jobs,
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_get_runners_list():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url=re.compile(r".*?(/runners(/all)?|/(groups|projects)/1/runners)"),
            json=[runner_shortinfo],
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_runner_detail():
    with responses.RequestsMock() as rsps:
        pattern = re.compile(r".*?/runners/6")
        rsps.add(
            method=responses.GET,
            url=pattern,
            json=runner_detail,
            content_type="application/json",
            status=200,
        )
        rsps.add(
            method=responses.PUT,
            url=pattern,
            json=runner_detail,
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_runner_register():
    with responses.RequestsMock() as rsps:
        pattern = re.compile(r".*?/runners")
        rsps.add(
            method=responses.POST,
            url=pattern,
            json={"id": "6", "token": "6337ff461c94fd3fa32ba3b1ff4125"},
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_runner_enable():
    with responses.RequestsMock() as rsps:
        pattern = re.compile(r".*?projects/1/runners")
        rsps.add(
            method=responses.POST,
            url=pattern,
            json=runner_shortinfo,
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_runner_delete():
    with responses.RequestsMock() as rsps:
        pattern = re.compile(r".*?/runners/6")
        rsps.add(
            method=responses.GET,
            url=pattern,
            json=runner_detail,
            content_type="application/json",
            status=200,
        )
        rsps.add(
            method=responses.DELETE,
            url=pattern,
            status=204,
        )
        yield rsps


@pytest.fixture
def resp_runner_delete_by_token():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.DELETE,
            url="http://localhost/api/v4/runners",
            status=204,
            match=[responses.matchers.query_param_matcher({"token": "auth-token"})],
        )
        yield rsps


@pytest.fixture
def resp_runner_disable():
    with responses.RequestsMock() as rsps:
        pattern = re.compile(r".*?/projects/1/runners/6")
        rsps.add(
            method=responses.DELETE,
            url=pattern,
            status=204,
        )
        yield rsps


@pytest.fixture
def resp_runner_verify():
    with responses.RequestsMock() as rsps:
        pattern = re.compile(r".*?/runners/verify")
        rsps.add(
            method=responses.POST,
            url=pattern,
            status=200,
        )
        yield rsps


def test_owned_runners_list(gl: gitlab.Gitlab, resp_get_runners_list):
    runners = gl.runners.list()
    assert runners[0].active is True
    assert runners[0].id == 6
    assert runners[0].name == "test-name"
    assert len(runners) == 1


def test_project_runners_list(gl: gitlab.Gitlab, resp_get_runners_list):
    runners = gl.projects.get(1, lazy=True).runners.list()
    assert runners[0].active is True
    assert runners[0].id == 6
    assert runners[0].name == "test-name"
    assert len(runners) == 1


def test_group_runners_list(gl: gitlab.Gitlab, resp_get_runners_list):
    runners = gl.groups.get(1, lazy=True).runners.list()
    assert runners[0].active is True
    assert runners[0].id == 6
    assert runners[0].name == "test-name"
    assert len(runners) == 1


def test_runners_all(gl: gitlab.Gitlab, resp_get_runners_list):
    runners = gl.runners.all()
    assert isinstance(runners[0], Runner)
    assert runners[0].active is True
    assert runners[0].id == 6
    assert runners[0].name == "test-name"
    assert len(runners) == 1


def test_runners_all_list(gl: gitlab.Gitlab, resp_get_runners_list):
    runners = gl.runners_all.list()
    assert isinstance(runners[0], RunnerAll)
    assert runners[0].active is True
    assert runners[0].id == 6
    assert runners[0].name == "test-name"
    assert len(runners) == 1


def test_create_runner(gl: gitlab.Gitlab, resp_runner_register):
    runner = gl.runners.create({"token": "token"})
    assert runner.id == "6"
    assert runner.token == "6337ff461c94fd3fa32ba3b1ff4125"


def test_get_update_runner(gl: gitlab.Gitlab, resp_runner_detail):
    runner = gl.runners.get(6)
    assert runner.active is True
    runner.tag_list.append("new")
    runner.save()


def test_delete_runner_by_id(gl: gitlab.Gitlab, resp_runner_delete):
    runner = gl.runners.get(6)
    runner.delete()
    gl.runners.delete(6)


def test_delete_runner_by_token(gl: gitlab.Gitlab, resp_runner_delete_by_token):
    gl.runners.delete(token="auth-token")


def test_disable_project_runner(gl: gitlab.Gitlab, resp_runner_disable):
    gl.projects.get(1, lazy=True).runners.delete(6)


def test_enable_project_runner(gl: gitlab.Gitlab, resp_runner_enable):
    runner = gl.projects.get(1, lazy=True).runners.create({"runner_id": 6})
    assert runner.active is True
    assert runner.id == 6
    assert runner.name == "test-name"


def test_verify_runner(gl: gitlab.Gitlab, resp_runner_verify):
    gl.runners.verify("token")


def test_runner_jobs(gl: gitlab.Gitlab, resp_get_runners_jobs):
    jobs = gl.runners.get(6, lazy=True).jobs.list()
    assert jobs[0].duration == 120
    assert jobs[0].name == "test"
    assert jobs[0].user.get("name") == "John Doe2"
    assert len(jobs) == 1

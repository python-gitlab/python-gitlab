"""
GitLab API: https://docs.gitlab.com/ce/api/system_hooks.html
GitLab API: https://docs.gitlab.com/ce/api/groups.html#hooks
GitLab API: https://docs.gitlab.com/ee/api/projects.html#hooks
"""

import re

import pytest
import responses

import gitlab
from gitlab.v4.objects import GroupHook, Hook, ProjectHook

hooks_content = [
    {
        "id": 1,
        "url": "testurl",
        "push_events": True,
        "tag_push_events": True,
    },
    {
        "id": 2,
        "url": "testurl_second",
        "push_events": False,
        "tag_push_events": False,
    },
]

hook_content = hooks_content[0]


@pytest.fixture
def resp_hooks_list():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url=re.compile(r"http://localhost/api/v4/((groups|projects)/1/|)hooks"),
            json=hooks_content,
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_hook_get():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url=re.compile(r"http://localhost/api/v4/((groups|projects)/1/|)hooks/1"),
            json=hook_content,
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_hook_create():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.POST,
            url=re.compile(r"http://localhost/api/v4/((groups|projects)/1/|)hooks"),
            json=hook_content,
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_hook_update():
    with responses.RequestsMock() as rsps:
        pattern = re.compile(r"http://localhost/api/v4/((groups|projects)/1/|)hooks/1")
        rsps.add(
            method=responses.GET,
            url=pattern,
            json=hook_content,
            content_type="application/json",
            status=200,
        )
        rsps.add(
            method=responses.PUT,
            url=pattern,
            json=hook_content,
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_hook_test():
    with responses.RequestsMock() as rsps:
        hook_pattern = re.compile(
            r"http://localhost/api/v4/((groups|projects)/1/|)hooks/1"
        )
        test_pattern = re.compile(
            r"http://localhost/api/v4/((groups|projects)/1/|)hooks/1/test/[a-z_]+"
        )
        rsps.add(
            method=responses.GET,
            url=hook_pattern,
            json=hook_content,
            content_type="application/json",
            status=200,
        )
        rsps.add(
            method=responses.POST,
            url=test_pattern,
            json={"message": "201 Created"},
            content_type="application/json",
            status=201,
        )
        yield rsps


@pytest.fixture
def resp_hook_test_error():
    with responses.RequestsMock() as rsps:
        hook_pattern = re.compile(
            r"http://localhost/api/v4/((groups|projects)/1/|)hooks/1"
        )
        test_pattern = re.compile(
            r"http://localhost/api/v4/((groups|projects)/1/|)hooks/1/test/[a-z_]+"
        )
        rsps.add(
            method=responses.GET,
            url=hook_pattern,
            json=hook_content,
            content_type="application/json",
            status=200,
        )
        rsps.add(
            method=responses.POST,
            url=test_pattern,
            json={"message": "<html>error</html>"},
            content_type="application/json",
            status=422,
        )
        yield rsps


@pytest.fixture
def resp_hook_delete():
    with responses.RequestsMock() as rsps:
        pattern = re.compile(r"http://localhost/api/v4/((groups|projects)/1/|)hooks/1")
        rsps.add(
            method=responses.GET,
            url=pattern,
            json=hook_content,
            content_type="application/json",
            status=200,
        )
        rsps.add(
            method=responses.DELETE,
            url=pattern,
            status=204,
        )
        yield rsps


def test_list_system_hooks(gl, resp_hooks_list):
    hooks = gl.hooks.list()
    assert hooks[0].id == 1
    assert hooks[0].url == "testurl"
    assert hooks[1].id == 2
    assert hooks[1].url == "testurl_second"


def test_get_system_hook(gl, resp_hook_get):
    data = gl.hooks.get(1)
    assert isinstance(data, Hook)
    assert data.url == "testurl"
    assert data.id == 1


def test_create_system_hook(gl, resp_hook_create):
    hook = gl.hooks.create(hook_content)
    assert hook.url == "testurl"
    assert hook.push_events is True
    assert hook.tag_push_events is True


# there is no update method for system hooks


def test_delete_system_hook(gl, resp_hook_delete):
    hook = gl.hooks.get(1)
    hook.delete()
    gl.hooks.delete(1)


def test_list_group_hooks(group, resp_hooks_list):
    hooks = group.hooks.list()
    assert hooks[0].id == 1
    assert hooks[0].url == "testurl"
    assert hooks[1].id == 2
    assert hooks[1].url == "testurl_second"


def test_get_group_hook(group, resp_hook_get):
    data = group.hooks.get(1)
    assert isinstance(data, GroupHook)
    assert data.url == "testurl"
    assert data.id == 1


def test_create_group_hook(group, resp_hook_create):
    hook = group.hooks.create(hook_content)
    assert hook.url == "testurl"
    assert hook.push_events is True
    assert hook.tag_push_events is True


def test_update_group_hook(group, resp_hook_update):
    hook = group.hooks.get(1)
    assert hook.id == 1
    hook.url = "testurl_more"
    hook.save()


def test_delete_group_hook(group, resp_hook_delete):
    hook = group.hooks.get(1)
    hook.delete()
    group.hooks.delete(1)


def test_test_group_hook(group, resp_hook_test):
    hook = group.hooks.get(1)
    hook.test("push_events")


def test_test_error_group_hook(group, resp_hook_test_error):
    hook = group.hooks.get(1)
    with pytest.raises(gitlab.exceptions.GitlabHookTestError):
        hook.test("push_events")


def test_list_project_hooks(project, resp_hooks_list):
    hooks = project.hooks.list()
    assert hooks[0].id == 1
    assert hooks[0].url == "testurl"
    assert hooks[1].id == 2
    assert hooks[1].url == "testurl_second"


def test_get_project_hook(project, resp_hook_get):
    data = project.hooks.get(1)
    assert isinstance(data, ProjectHook)
    assert data.url == "testurl"
    assert data.id == 1


def test_create_project_hook(project, resp_hook_create):
    hook = project.hooks.create(hook_content)
    assert hook.url == "testurl"
    assert hook.push_events is True
    assert hook.tag_push_events is True


def test_update_project_hook(project, resp_hook_update):
    hook = project.hooks.get(1)
    assert hook.id == 1
    hook.url = "testurl_more"
    hook.save()


def test_delete_project_hook(project, resp_hook_delete):
    hook = project.hooks.get(1)
    hook.delete()
    project.hooks.delete(1)

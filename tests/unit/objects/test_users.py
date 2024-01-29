"""
GitLab API:
https://docs.gitlab.com/ce/api/users.html
https://docs.gitlab.com/ee/api/projects.html#list-projects-starred-by-a-user
"""

import pytest
import responses

from gitlab.v4.objects import StarredProject, User, UserMembership, UserStatus

from .test_projects import project_content


@pytest.fixture
def resp_get_user():
    content = {
        "name": "name",
        "id": 1,
        "password": "password",
        "username": "username",
        "email": "email",
    }

    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/users/1",
            json=content,
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_get_user_memberships():
    content = [
        {
            "source_id": 1,
            "source_name": "Project one",
            "source_type": "Project",
            "access_level": "20",
        },
        {
            "source_id": 3,
            "source_name": "Group three",
            "source_type": "Namespace",
            "access_level": "20",
        },
    ]

    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/users/1/memberships",
            json=content,
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_activate():
    with responses.RequestsMock(assert_all_requests_are_fired=False) as rsps:
        rsps.add(
            method=responses.POST,
            url="http://localhost/api/v4/users/1/activate",
            json={},
            content_type="application/json",
            status=201,
        )
        rsps.add(
            method=responses.POST,
            url="http://localhost/api/v4/users/1/deactivate",
            json={},
            content_type="application/json",
            status=201,
        )
        yield rsps


@pytest.fixture
def resp_approve():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.POST,
            url="http://localhost/api/v4/users/1/approve",
            json={"message": "Success"},
            content_type="application/json",
            status=201,
        )
        yield rsps


@pytest.fixture
def resp_reject():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.POST,
            url="http://localhost/api/v4/users/1/reject",
            json={"message": "Success"},
            content_type="application/json",
            status=201,
        )
        yield rsps


@pytest.fixture
def resp_ban():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.POST,
            url="http://localhost/api/v4/users/1/ban",
            json={},
            content_type="application/json",
            status=201,
        )
        yield rsps


@pytest.fixture
def resp_unban():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.POST,
            url="http://localhost/api/v4/users/1/unban",
            json={},
            content_type="application/json",
            status=201,
        )
        yield rsps


@pytest.fixture
def resp_get_user_status():
    content = {
        "message": "test",
        "message_html": "<h1>Message</h1>",
        "emoji": "thumbsup",
    }

    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/users/1/status",
            json=content,
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_delete_user_identity():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.DELETE,
            url="http://localhost/api/v4/users/1/identities/test_provider",
            status=204,
        )
        yield rsps


@pytest.fixture
def resp_follow_unfollow():
    user = {
        "id": 1,
        "username": "john_smith",
        "name": "John Smith",
        "state": "active",
        "avatar_url": "http://localhost:3000/uploads/user/avatar/1/cd8.jpeg",
        "web_url": "http://localhost:3000/john_smith",
    }
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.POST,
            url="http://localhost/api/v4/users/1/follow",
            json=user,
            content_type="application/json",
            status=201,
        )
        rsps.add(
            method=responses.POST,
            url="http://localhost/api/v4/users/1/unfollow",
            json=user,
            content_type="application/json",
            status=201,
        )
        yield rsps


@pytest.fixture
def resp_followers_following():
    content = [
        {
            "id": 2,
            "name": "Lennie Donnelly",
            "username": "evette.kilback",
            "state": "active",
            "avatar_url": "https://www.gravatar.com/avatar/7955171a55ac4997ed81e5976287890a?s=80&d=identicon",
            "web_url": "http://127.0.0.1:3000/evette.kilback",
        },
        {
            "id": 4,
            "name": "Serena Bradtke",
            "username": "cammy",
            "state": "active",
            "avatar_url": "https://www.gravatar.com/avatar/a2daad869a7b60d3090b7b9bef4baf57?s=80&d=identicon",
            "web_url": "http://127.0.0.1:3000/cammy",
        },
    ]
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/users/1/followers",
            json=content,
            content_type="application/json",
            status=200,
        )
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/users/1/following",
            json=content,
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_starred_projects():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/users/1/starred_projects",
            json=[project_content],
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_runner_create():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.POST,
            url="http://localhost/api/v4/user/runners",
            json={"id": "6", "token": "6337ff461c94fd3fa32ba3b1ff4125"},
            content_type="application/json",
            status=201,
        )
        yield rsps


def test_get_user(gl, resp_get_user):
    user = gl.users.get(1)
    assert isinstance(user, User)
    assert user.name == "name"
    assert user.id == 1


def test_user_memberships(user, resp_get_user_memberships):
    memberships = user.memberships.list()
    assert isinstance(memberships[0], UserMembership)
    assert memberships[0].source_type == "Project"


def test_user_status(user, resp_get_user_status):
    status = user.status.get()
    assert isinstance(status, UserStatus)
    assert status.message == "test"
    assert status.emoji == "thumbsup"


def test_user_activate_deactivate(user, resp_activate):
    user.activate()
    user.deactivate()


def test_user_approve_(user, resp_approve):
    user.approve()


def test_user_approve_reject(user, resp_reject):
    user.reject()


def test_user_ban(user, resp_ban):
    user.ban()


def test_user_unban(user, resp_unban):
    user.unban()


def test_delete_user_identity(user, resp_delete_user_identity):
    user.identityproviders.delete("test_provider")


def test_user_follow_unfollow(user, resp_follow_unfollow):
    user.follow()
    user.unfollow()


def test_list_followers(user, resp_followers_following):
    followers = user.followers_users.list()
    followings = user.following_users.list()
    assert isinstance(followers[0], User)
    assert followers[0].id == 2
    assert isinstance(followings[0], User)
    assert followings[1].id == 4


def test_list_starred_projects(user, resp_starred_projects):
    projects = user.starred_projects.list()
    assert isinstance(projects[0], StarredProject)
    assert projects[0].id == project_content["id"]


def test_create_user_runner(current_user, resp_runner_create):
    runner = current_user.runners.create({"runner_type": "instance_type"})
    assert runner.id == "6"
    assert runner.token == "6337ff461c94fd3fa32ba3b1ff4125"

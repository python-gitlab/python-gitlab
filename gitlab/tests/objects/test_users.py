"""
GitLab API: https://docs.gitlab.com/ce/api/users.html
"""
import pytest
import responses

from gitlab.v4.objects import User, UserMembership, UserStatus


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

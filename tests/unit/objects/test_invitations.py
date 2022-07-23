"""
GitLab API: https://docs.gitlab.com/ce/api/invitations.html
"""

import re

import pytest
import responses

from gitlab.exceptions import GitlabInvitationError

create_content = {"email": "email@example.com", "access_level": 30}
success_content = {"status": "success"}
error_content = {
    "status": "error",
    "message": {
        "test@example.com": "Invite email has already been taken",
        "test2@example.com": "User already exists in source",
        "test_username": "Access level is not included in the list",
    },
}
invitations_content = [
    {
        "id": 1,
        "invite_email": "member@example.org",
        "created_at": "2020-10-22T14:13:35Z",
        "access_level": 30,
        "expires_at": "2020-11-22T14:13:35Z",
        "user_name": "Raymond Smith",
        "created_by_name": "Administrator",
    },
]
invitation_content = {
    "expires_at": "2012-10-22T14:13:35Z",
    "access_level": 40,
}


@pytest.fixture
def resp_invitations_list():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url=re.compile(r"http://localhost/api/v4/(groups|projects)/1/invitations"),
            json=invitations_content,
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_invitation_create():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.POST,
            url=re.compile(r"http://localhost/api/v4/(groups|projects)/1/invitations"),
            json=success_content,
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_invitation_create_error():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.POST,
            url=re.compile(r"http://localhost/api/v4/(groups|projects)/1/invitations"),
            json=error_content,
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_invitation_update():
    with responses.RequestsMock() as rsps:
        pattern = re.compile(
            r"http://localhost/api/v4/(groups|projects)/1/invitations/email%40example.com"
        )
        rsps.add(
            method=responses.PUT,
            url=pattern,
            json=invitation_content,
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_invitation_delete():
    with responses.RequestsMock() as rsps:
        pattern = re.compile(
            r"http://localhost/api/v4/(groups|projects)/1/invitations/email%40example.com"
        )
        rsps.add(
            method=responses.DELETE,
            url=pattern,
            status=204,
        )
        yield rsps


def test_list_group_invitations(group, resp_invitations_list):
    invitations = group.invitations.list()
    assert invitations[0].invite_email == "member@example.org"


def test_create_group_invitation(group, resp_invitation_create):
    invitation = group.invitations.create(create_content)
    assert invitation.status == "success"


def test_update_group_invitation(group, resp_invitation_update):
    invitation = group.invitations.get("email@example.com", lazy=True)
    invitation.access_level = 30
    invitation.save()


def test_delete_group_invitation(group, resp_invitation_delete):
    invitation = group.invitations.get("email@example.com", lazy=True)
    invitation.delete()
    group.invitations.delete("email@example.com")


def test_list_project_invitations(project, resp_invitations_list):
    invitations = project.invitations.list()
    assert invitations[0].invite_email == "member@example.org"


def test_create_project_invitation(project, resp_invitation_create):
    invitation = project.invitations.create(create_content)
    assert invitation.status == "success"


def test_update_project_invitation(project, resp_invitation_update):
    invitation = project.invitations.get("email@example.com", lazy=True)
    invitation.access_level = 30
    invitation.save()


def test_delete_project_invitation(project, resp_invitation_delete):
    invitation = project.invitations.get("email@example.com", lazy=True)
    invitation.delete()
    project.invitations.delete("email@example.com")


def test_create_group_invitation_raises(group, resp_invitation_create_error):
    with pytest.raises(GitlabInvitationError, match="User already exists"):
        group.invitations.create(create_content)


def test_create_project_invitation_raises(project, resp_invitation_create_error):
    with pytest.raises(GitlabInvitationError, match="User already exists"):
        project.invitations.create(create_content)

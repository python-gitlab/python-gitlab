"""
GitLab API: https://docs.gitlab.com/ee/api/members.html
"""

import pytest
import responses

from gitlab.const import AccessLevel
from gitlab.v4.objects import GroupBillableMember

billable_members_content = [
    {
        "id": 1,
        "username": "raymond_smith",
        "name": "Raymond Smith",
        "state": "active",
        "avatar_url": "https://www.gravatar.com/avatar/c2525a7f58ae3776070e44c106c48e15?s=80&d=identicon",
        "web_url": "http://192.168.1.8:3000/root",
        "last_activity_on": "2021-01-27",
        "membership_type": "group_member",
        "removable": True,
    }
]


@pytest.fixture
def resp_create_group_member():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.POST,
            url="http://localhost/api/v4/groups/1/members",
            json={"id": 1, "username": "jane_doe", "access_level": 30},
            content_type="application/json",
            status=201,
        )
        yield rsps


@pytest.fixture
def resp_list_billable_group_members():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/groups/1/billable_members",
            json=billable_members_content,
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_delete_billable_group_member():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.DELETE,
            url="http://localhost/api/v4/groups/1/billable_members/1",
            status=204,
        )
        yield rsps


def test_create_group_member(group, resp_create_group_member):
    member = group.members.create({"user_id": 1, "access_level": AccessLevel.DEVELOPER})
    assert member.access_level == 30


def test_list_group_billable_members(group, resp_list_billable_group_members):
    billable_members = group.billable_members.list()
    assert isinstance(billable_members, list)
    assert isinstance(billable_members[0], GroupBillableMember)
    assert billable_members[0].removable is True


def test_delete_group_billable_member(group, resp_delete_billable_group_member):
    group.billable_members.delete(1)

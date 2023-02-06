"""
GitLab API: https://docs.gitlab.com/ee/api/statistics.html
"""

import pytest
import responses

content = {
    "forks": "10",
    "issues": "76",
    "merge_requests": "27",
    "notes": "954",
    "snippets": "50",
    "ssh_keys": "10",
    "milestones": "40",
    "users": "50",
    "groups": "10",
    "projects": "20",
    "active_users": "50",
}


@pytest.fixture
def resp_application_statistics():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/application/statistics",
            json=content,
            content_type="application/json",
            status=200,
        )

        yield rsps


def test_get_statistics(gl, resp_application_statistics):
    statistics = gl.statistics.get()
    assert statistics.forks == content["forks"]
    assert statistics.merge_requests == content["merge_requests"]
    assert statistics.notes == content["notes"]
    assert statistics.snippets == content["snippets"]
    assert statistics.ssh_keys == content["ssh_keys"]
    assert statistics.milestones == content["milestones"]
    assert statistics.users == content["users"]
    assert statistics.groups == content["groups"]
    assert statistics.projects == content["projects"]
    assert statistics.active_users == content["active_users"]

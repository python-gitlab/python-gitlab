"""
GitLab API: https://docs.gitlab.com/ce/api/pull_mirror.html
"""

import pytest
import responses

from gitlab.v4.objects import ProjectPullMirror


@pytest.fixture
def resp_pull_mirror():
    content = {
        "update_status": "none",
        "url": "https://gitlab.example.com/root/mirror.git",
        "last_error": None,
        "last_update_at": "2024-12-03T08:01:05.466Z",
        "last_update_started_at": "2024-12-03T08:01:05.342Z",
        "last_successful_update_at": None,
        "enabled": True,
        "mirror_trigger_builds": False,
        "only_mirror_protected_branches": None,
        "mirror_overwrites_diverged_branches": None,
        "mirror_branch_regex": None,
    }

    with responses.RequestsMock(assert_all_requests_are_fired=False) as rsps:
        rsps.add(
            method=responses.PUT,
            url="http://localhost/api/v4/projects/1/mirror/pull",
            json=content,
            content_type="application/json",
            status=200,
        )

        rsps.add(
            method=responses.POST,
            url="http://localhost/api/v4/projects/1/mirror/pull",
            status=200,
        )

        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/projects/1/mirror/pull",
            json=content,
            content_type="application/json",
            status=200,
        )

        yield rsps


def test_create_project_pull_mirror(project, resp_pull_mirror):
    mirror = project.pull_mirror.create(
        {"url": "https://gitlab.example.com/root/mirror.git"}
    )
    assert mirror.enabled


def test_start_project_pull_mirror(project, resp_pull_mirror):
    project.pull_mirror.start()


def test_get_project_pull_mirror(project, resp_pull_mirror):
    mirror = project.pull_mirror.get()
    assert isinstance(mirror, ProjectPullMirror)
    assert mirror.enabled

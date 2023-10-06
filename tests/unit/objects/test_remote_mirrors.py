"""
GitLab API: https://docs.gitlab.com/ce/api/remote_mirrors.html
"""

import pytest
import responses

from gitlab.v4.objects import ProjectRemoteMirror


@pytest.fixture
def resp_remote_mirrors():
    content = {
        "enabled": True,
        "id": 1,
        "last_error": None,
        "last_successful_update_at": "2020-01-06T17:32:02.823Z",
        "last_update_at": "2020-01-06T17:32:02.823Z",
        "last_update_started_at": "2020-01-06T17:31:55.864Z",
        "only_protected_branches": True,
        "update_status": "none",
        "url": "https://*****:*****@gitlab.com/gitlab-org/security/gitlab.git",
    }

    with responses.RequestsMock(assert_all_requests_are_fired=False) as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/projects/1/remote_mirrors",
            json=[content],
            content_type="application/json",
            status=200,
        )
        rsps.add(
            method=responses.POST,
            url="http://localhost/api/v4/projects/1/remote_mirrors",
            json=content,
            content_type="application/json",
            status=200,
        )

        updated_content = dict(content)
        updated_content["update_status"] = "finished"

        rsps.add(
            method=responses.PUT,
            url="http://localhost/api/v4/projects/1/remote_mirrors/1",
            json=updated_content,
            content_type="application/json",
            status=200,
        )

        rsps.add(
            method=responses.DELETE,
            url="http://localhost/api/v4/projects/1/remote_mirrors/1",
            status=204,
        )
        yield rsps


def test_list_project_remote_mirrors(project, resp_remote_mirrors):
    mirrors = project.remote_mirrors.list()
    assert isinstance(mirrors, list)
    assert isinstance(mirrors[0], ProjectRemoteMirror)
    assert mirrors[0].enabled


def test_create_project_remote_mirror(project, resp_remote_mirrors):
    mirror = project.remote_mirrors.create({"url": "https://example.com"})
    assert isinstance(mirror, ProjectRemoteMirror)
    assert mirror.update_status == "none"


def test_update_project_remote_mirror(project, resp_remote_mirrors):
    mirror = project.remote_mirrors.create({"url": "https://example.com"})
    mirror.only_protected_branches = True
    mirror.save()
    assert mirror.update_status == "finished"
    assert mirror.only_protected_branches


def test_delete_project_remote_mirror(project, resp_remote_mirrors):
    mirror = project.remote_mirrors.create({"url": "https://example.com"})
    mirror.delete()

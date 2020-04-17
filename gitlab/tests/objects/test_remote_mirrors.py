"""
GitLab API: https://docs.gitlab.com/ce/api/remote_mirrors.html
"""

from httmock import response, urlmatch, with_httmock

from gitlab.v4.objects import ProjectRemoteMirror
from .mocks import headers


@urlmatch(
    scheme="http",
    netloc="localhost",
    path="/api/v4/projects/1/remote_mirrors",
    method="get",
)
def resp_get_remote_mirrors(url, request):
    """Mock for Project Remote Mirrors GET response."""
    content = """[
      {
        "enabled": true,
        "id": 101486,
        "last_error": null,
        "last_successful_update_at": "2020-01-06T17:32:02.823Z",
        "last_update_at": "2020-01-06T17:32:02.823Z",
        "last_update_started_at": "2020-01-06T17:31:55.864Z",
        "only_protected_branches": true,
        "update_status": "finished",
        "url": "https://*****:*****@gitlab.com/gitlab-org/security/gitlab.git"
      }
    ]"""
    content = content.encode("utf-8")
    return response(200, content, headers, None, 5, request)


@urlmatch(
    scheme="http",
    netloc="localhost",
    path="/api/v4/projects/1/remote_mirrors",
    method="post",
)
def resp_create_remote_mirror(url, request):
    """Mock for Project Remote Mirrors POST response."""
    content = """{
        "enabled": false,
        "id": 101486,
        "last_error": null,
        "last_successful_update_at": null,
        "last_update_at": null,
        "last_update_started_at": null,
        "only_protected_branches": false,
        "update_status": "none",
        "url": "https://*****:*****@example.com/gitlab/example.git"
    }"""
    content = content.encode("utf-8")
    return response(200, content, headers, None, 5, request)


@urlmatch(
    scheme="http",
    netloc="localhost",
    path="/api/v4/projects/1/remote_mirrors/1",
    method="put",
)
def resp_update_remote_mirror(url, request):
    """Mock for Project Remote Mirrors PUT response."""
    content = """{
        "enabled": false,
        "id": 101486,
        "last_error": null,
        "last_successful_update_at": "2020-01-06T17:32:02.823Z",
        "last_update_at": "2020-01-06T17:32:02.823Z",
        "last_update_started_at": "2020-01-06T17:31:55.864Z",
        "only_protected_branches": true,
        "update_status": "finished",
        "url": "https://*****:*****@gitlab.com/gitlab-org/security/gitlab.git"
    }"""
    content = content.encode("utf-8")
    return response(200, content, headers, None, 5, request)


@with_httmock(resp_get_remote_mirrors)
def test_list_project_remote_mirrors(project):
    mirrors = project.remote_mirrors.list()
    assert isinstance(mirrors, list)
    assert isinstance(mirrors[0], ProjectRemoteMirror)
    assert mirrors[0].enabled


@with_httmock(resp_create_remote_mirror)
def test_create_project_remote_mirror(project):
    mirror = project.remote_mirrors.create({"url": "https://example.com"})
    assert isinstance(mirror, ProjectRemoteMirror)
    assert mirror.update_status == "none"


@with_httmock(resp_create_remote_mirror, resp_update_remote_mirror)
def test_update_project_remote_mirror(project):
    mirror = project.remote_mirrors.create({"url": "https://example.com"})
    mirror.only_protected_branches = True
    mirror.save()
    assert mirror.update_status == "finished"
    assert mirror.only_protected_branches

"""
GitLab API: https://docs.gitlab.com/ce/api/commits.html
"""

from httmock import urlmatch, response, with_httmock

from .mocks import headers


@urlmatch(
    scheme="http",
    netloc="localhost",
    path="/api/v4/projects/1/repository/commits/6b2257ea",
    method="get",
)
def resp_get_commit(url, request):
    """Mock for commit GET response."""
    content = """{
    "id": "6b2257eabcec3db1f59dafbd84935e3caea04235",
    "short_id": "6b2257ea",
    "title": "Initial commit"
    }"""
    content = content.encode("utf-8")
    return response(200, content, headers, None, 5, request)


@urlmatch(
    scheme="http", path="/api/v4/projects/1/repository/commits", method="post",
)
def resp_create_commit(url, request):
    """Mock for commit create POST response."""
    content = """{
    "id": "ed899a2f4b50b4370feeea94676502b42383c746",
    "short_id": "ed899a2f",
    "title": "Commit message"
    }"""
    content = content.encode("utf-8")
    return response(200, content, headers, None, 5, request)


@urlmatch(
    scheme="http", path="/api/v4/projects/1/repository/commits/6b2257ea", method="post",
)
def resp_revert_commit(url, request):
    """Mock for commit revert POST response."""
    content = """{
    "id": "8b090c1b79a14f2bd9e8a738f717824ff53aebad",
    "short_id": "8b090c1b",
    "title":"Revert \\"Initial commit\\""
    }"""
    content = content.encode("utf-8")
    return response(200, content, headers, None, 5, request)


@urlmatch(
    scheme="http",
    netloc="localhost",
    path="/api/v4/projects/1/repository/commits/6b2257ea/signature",
    method="get",
)
def resp_get_commit_gpg_signature(url, request):
    """Mock for commit GPG signature GET response."""
    content = """{
    "gpg_key_id": 1,
    "gpg_key_primary_keyid": "8254AAB3FBD54AC9",
    "gpg_key_user_name": "John Doe",
    "gpg_key_user_email": "johndoe@example.com",
    "verification_status": "verified",
    "gpg_key_subkey_id": null
    }"""
    content = content.encode("utf-8")
    return response(200, content, headers, None, 5, request)


@with_httmock(resp_get_commit)
def test_get_commit(project):
    commit = project.commits.get("6b2257ea")
    assert commit.short_id == "6b2257ea"
    assert commit.title == "Initial commit"


@with_httmock(resp_create_commit)
def test_create_commit(project):
    data = {
        "branch": "master",
        "commit_message": "Commit message",
        "actions": [{"action": "create", "file_path": "README", "content": "",}],
    }
    commit = project.commits.create(data)
    assert commit.short_id == "ed899a2f"
    assert commit.title == data["commit_message"]


@with_httmock(resp_revert_commit)
def test_revert_commit(project):
    commit = project.commits.get("6b2257ea", lazy=True)
    revert_commit = commit.revert(branch="master")
    assert revert_commit["short_id"] == "8b090c1b"
    assert revert_commit["title"] == 'Revert "Initial commit"'


@with_httmock(resp_get_commit_gpg_signature)
def test_get_commit_gpg_signature(project):
    commit = project.commits.get("6b2257ea", lazy=True)
    signature = commit.signature()
    assert signature["gpg_key_primary_keyid"] == "8254AAB3FBD54AC9"
    assert signature["verification_status"] == "verified"

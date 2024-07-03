"""
GitLab API: https://docs.gitlab.com/ce/api/commits.html
"""

import pytest
import responses


@pytest.fixture
def resp_create_commit():
    content = {
        "id": "ed899a2f4b50b4370feeea94676502b42383c746",
        "short_id": "ed899a2f",
        "title": "Commit message",
    }

    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.POST,
            url="http://localhost/api/v4/projects/1/repository/commits",
            json=content,
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_commit():
    get_content = {
        "id": "6b2257eabcec3db1f59dafbd84935e3caea04235",
        "short_id": "6b2257ea",
        "title": "Initial commit",
    }
    revert_content = {
        "id": "8b090c1b79a14f2bd9e8a738f717824ff53aebad",
        "short_id": "8b090c1b",
        "title": 'Revert "Initial commit"',
    }

    with responses.RequestsMock(assert_all_requests_are_fired=False) as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/projects/1/repository/commits/6b2257ea",
            json=get_content,
            content_type="application/json",
            status=200,
        )
        rsps.add(
            method=responses.POST,
            url="http://localhost/api/v4/projects/1/repository/commits/6b2257ea/revert",
            json=revert_content,
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_get_commit_gpg_signature():
    content = {
        "gpg_key_id": 1,
        "gpg_key_primary_keyid": "8254AAB3FBD54AC9",
        "gpg_key_user_name": "John Doe",
        "gpg_key_user_email": "johndoe@example.com",
        "verification_status": "verified",
        "gpg_key_subkey_id": None,
    }

    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/projects/1/repository/commits/6b2257ea/signature",
            json=content,
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_get_commit_sequence():
    content = {
        "count": 1,
    }

    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/projects/1/repository/commits/6b2257ea/sequence",
            json=content,
            content_type="application/json",
            status=200,
        )
        yield rsps


def test_get_commit(project, resp_commit):
    commit = project.commits.get("6b2257ea")
    assert commit.short_id == "6b2257ea"
    assert commit.title == "Initial commit"


def test_create_commit(project, resp_create_commit):
    data = {
        "branch": "main",
        "commit_message": "Commit message",
        "actions": [
            {
                "action": "create",
                "file_path": "README",
                "content": "",
            }
        ],
    }
    commit = project.commits.create(data)
    assert commit.short_id == "ed899a2f"
    assert commit.title == data["commit_message"]


def test_revert_commit(project, resp_commit):
    commit = project.commits.get("6b2257ea", lazy=True)
    revert_commit = commit.revert(branch="main")
    assert revert_commit["short_id"] == "8b090c1b"
    assert revert_commit["title"] == 'Revert "Initial commit"'


def test_get_commit_gpg_signature(project, resp_get_commit_gpg_signature):
    commit = project.commits.get("6b2257ea", lazy=True)
    signature = commit.signature()
    assert signature["gpg_key_primary_keyid"] == "8254AAB3FBD54AC9"
    assert signature["verification_status"] == "verified"


def test_get_commit_sequence(project, resp_get_commit_sequence):
    commit = project.commits.get("6b2257ea", lazy=True)
    sequence = commit.sequence()
    assert sequence["count"] == 1

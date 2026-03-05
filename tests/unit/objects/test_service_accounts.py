"""
GitLab API: https://docs.gitlab.com/api/service_accounts/
"""

import pytest
import responses

from gitlab.v4.objects import (
    GroupServiceAccount,
    GroupServiceAccountAccessToken,
    ProjectServiceAccount,
    ProjectServiceAccountAccessToken,
    ServiceAccount,
)

# ---------------------------------------------------------------------------
# Fixtures – instance-level service accounts
# ---------------------------------------------------------------------------

instance_sa_content = {
    "id": 57,
    "username": "service_account_abc123",
    "name": "Service account user",
    "email": "service_account_abc123@noreply.example.com",
}


@pytest.fixture
def resp_list_service_accounts():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/service_accounts",
            json=[instance_sa_content],
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_create_service_account():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.POST,
            url="http://localhost/api/v4/service_accounts",
            json=instance_sa_content,
            content_type="application/json",
            status=201,
        )
        yield rsps


@pytest.fixture
def resp_update_service_account():
    updated = {**instance_sa_content, "name": "Renamed account"}
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.PATCH,
            url=f"http://localhost/api/v4/service_accounts/{instance_sa_content['id']}",
            json=updated,
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_create_and_save_service_account():
    updated = {**instance_sa_content, "name": "Renamed account"}
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.POST,
            url="http://localhost/api/v4/service_accounts",
            json=instance_sa_content,
            content_type="application/json",
            status=201,
        )
        rsps.add(
            method=responses.PATCH,
            url=f"http://localhost/api/v4/service_accounts/{instance_sa_content['id']}",
            json=updated,
            content_type="application/json",
            status=200,
        )
        yield rsps


# ---------------------------------------------------------------------------
# Fixtures – group service accounts
# ---------------------------------------------------------------------------

group_sa_content = {
    "id": 42,
    "username": "group-service-account",
    "name": "Group Service Account",
    "email": "group-sa@example.com",
}

group_sa_updated = {**group_sa_content, "name": "Renamed Group SA"}

sa_token_content = {
    "id": 1,
    "name": "my-token",
    "scopes": ["api", "read_api"],
    "user_id": 42,
    "revoked": False,
    "active": True,
    "expires_at": "2025-12-31",
    "token": "glpat-secret",
}

sa_token_rotated = {**sa_token_content, "token": "glpat-rotated"}


@pytest.fixture
def resp_list_group_service_accounts():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/groups/1/service_accounts",
            json=[group_sa_content],
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_create_group_service_account():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.POST,
            url="http://localhost/api/v4/groups/1/service_accounts",
            json=group_sa_content,
            content_type="application/json",
            status=201,
        )
        yield rsps


@pytest.fixture
def resp_update_group_service_account():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.PATCH,
            url="http://localhost/api/v4/groups/1/service_accounts/42",
            json=group_sa_updated,
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_delete_group_service_account():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.DELETE,
            url="http://localhost/api/v4/groups/1/service_accounts/42",
            status=204,
        )
        yield rsps


@pytest.fixture
def resp_list_group_sa_tokens():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/groups/1/service_accounts/42/personal_access_tokens",
            json=[sa_token_content],
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_create_group_sa_token():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.POST,
            url="http://localhost/api/v4/groups/1/service_accounts/42/personal_access_tokens",
            json=sa_token_content,
            content_type="application/json",
            status=201,
        )
        yield rsps


@pytest.fixture
def resp_delete_group_sa_token():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.DELETE,
            url="http://localhost/api/v4/groups/1/service_accounts/42/personal_access_tokens/1",
            status=204,
        )
        yield rsps


@pytest.fixture
def resp_list_and_delete_group_sa_token():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/groups/1/service_accounts/42/personal_access_tokens",
            json=[sa_token_content],
            content_type="application/json",
            status=200,
        )
        rsps.add(
            method=responses.DELETE,
            url="http://localhost/api/v4/groups/1/service_accounts/42/personal_access_tokens/1",
            status=204,
        )
        yield rsps


@pytest.fixture
def resp_rotate_group_sa_token():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.POST,
            url="http://localhost/api/v4/groups/1/service_accounts/42/personal_access_tokens/1/rotate",
            json=sa_token_rotated,
            content_type="application/json",
            status=200,
        )
        yield rsps


# ---------------------------------------------------------------------------
# Helper – lazy service account under group 1 with id 42
# ---------------------------------------------------------------------------


@pytest.fixture
def group_service_account(gl):
    manager = gl.groups.get(1, lazy=True).service_accounts
    return GroupServiceAccount(manager, group_sa_content)


# ---------------------------------------------------------------------------
# Tests – instance-level service accounts
# ---------------------------------------------------------------------------


def test_list_service_accounts(gl, resp_list_service_accounts):
    accounts = gl.service_accounts.list()
    assert len(accounts) == 1
    assert isinstance(accounts[0], ServiceAccount)
    assert accounts[0].id == 57
    assert accounts[0].username == "service_account_abc123"


def test_create_service_account_with_defaults(gl, resp_create_service_account):
    sa = gl.service_accounts.create({})
    assert isinstance(sa, ServiceAccount)
    assert sa.id == 57
    assert sa.name == "Service account user"


def test_create_service_account_with_attrs(gl, resp_create_service_account):
    sa = gl.service_accounts.create(
        {"name": "Service account user", "username": "service_account_abc123"}
    )
    assert isinstance(sa, ServiceAccount)
    assert sa.username == "service_account_abc123"


def test_update_service_account(gl, resp_update_service_account):
    updated = gl.service_accounts.update(57, {"name": "Renamed account"})
    assert updated["name"] == "Renamed account"


def test_save_service_account(gl, resp_create_and_save_service_account):
    sa = gl.service_accounts.create({})
    sa.name = "Renamed account"
    sa.save()


# ---------------------------------------------------------------------------
# Tests – group service accounts
# ---------------------------------------------------------------------------


def test_list_group_service_accounts(gl, resp_list_group_service_accounts):
    accounts = gl.groups.get(1, lazy=True).service_accounts.list()
    assert len(accounts) == 1
    assert isinstance(accounts[0], GroupServiceAccount)
    assert accounts[0].id == 42


def test_create_group_service_account(gl, resp_create_group_service_account):
    sa = gl.groups.get(1, lazy=True).service_accounts.create(
        {"name": "Group Service Account", "username": "group-service-account"}
    )
    assert isinstance(sa, GroupServiceAccount)
    assert sa.id == 42
    assert sa.username == "group-service-account"


def test_update_group_service_account(gl, resp_update_group_service_account):
    updated = gl.groups.get(1, lazy=True).service_accounts.update(
        42, {"name": "Renamed Group SA"}
    )
    assert updated["name"] == "Renamed Group SA"


def test_save_group_service_account(
    group_service_account, resp_update_group_service_account
):
    group_service_account.name = "Renamed Group SA"
    group_service_account.save()


def test_delete_group_service_account(gl, resp_delete_group_service_account):
    gl.groups.get(1, lazy=True).service_accounts.delete(42)


def test_delete_group_service_account_via_object(
    group_service_account, resp_delete_group_service_account
):
    group_service_account.delete()


# ---------------------------------------------------------------------------
# Tests – group service account personal access tokens
# ---------------------------------------------------------------------------


def test_list_group_sa_tokens(group_service_account, resp_list_group_sa_tokens):
    tokens = group_service_account.access_tokens.list()
    assert len(tokens) == 1
    assert isinstance(tokens[0], GroupServiceAccountAccessToken)
    assert tokens[0].name == "my-token"
    assert tokens[0].scopes == ["api", "read_api"]


def test_create_group_sa_token(group_service_account, resp_create_group_sa_token):
    token = group_service_account.access_tokens.create(
        {"name": "my-token", "scopes": ["api", "read_api"]}
    )
    assert isinstance(token, GroupServiceAccountAccessToken)
    assert token.id == 1
    assert token.token == "glpat-secret"


def test_delete_group_sa_token(group_service_account, resp_delete_group_sa_token):
    group_service_account.access_tokens.delete(1)


def test_delete_group_sa_token_via_object(
    group_service_account, resp_list_and_delete_group_sa_token
):
    token = group_service_account.access_tokens.list()[0]
    token.delete()


def test_rotate_group_sa_token(group_service_account, resp_rotate_group_sa_token):
    token = GroupServiceAccountAccessToken(
        group_service_account.access_tokens, sa_token_content
    )
    token.rotate()
    assert token.token == "glpat-rotated"


def test_rotate_group_sa_token_via_manager(
    group_service_account, resp_rotate_group_sa_token
):
    result = group_service_account.access_tokens.rotate(1)
    assert result["token"] == "glpat-rotated"


# ---------------------------------------------------------------------------
# Fixtures – project service accounts
# ---------------------------------------------------------------------------

proj_sa_content = {
    "id": 99,
    "username": "project-service-account",
    "name": "Project Service Account",
    "email": "proj-sa@example.com",
}

proj_sa_updated = {**proj_sa_content, "name": "Renamed Project SA"}

proj_sa_token_content = {
    "id": 2,
    "name": "proj-token",
    "scopes": ["read_api"],
    "user_id": 99,
    "revoked": False,
    "active": True,
    "expires_at": "2025-12-31",
    "token": "glpat-proj-secret",
}

proj_sa_token_rotated = {**proj_sa_token_content, "token": "glpat-proj-rotated"}


@pytest.fixture
def resp_list_project_service_accounts():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/projects/1/service_accounts",
            json=[proj_sa_content],
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_create_project_service_account():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.POST,
            url="http://localhost/api/v4/projects/1/service_accounts",
            json=proj_sa_content,
            content_type="application/json",
            status=201,
        )
        yield rsps


@pytest.fixture
def resp_update_project_service_account():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.PATCH,
            url="http://localhost/api/v4/projects/1/service_accounts/99",
            json=proj_sa_updated,
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_delete_project_service_account():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.DELETE,
            url="http://localhost/api/v4/projects/1/service_accounts/99",
            status=204,
        )
        yield rsps


@pytest.fixture
def resp_list_project_sa_tokens():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/projects/1/service_accounts/99/personal_access_tokens",
            json=[proj_sa_token_content],
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_create_project_sa_token():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.POST,
            url="http://localhost/api/v4/projects/1/service_accounts/99/personal_access_tokens",
            json=proj_sa_token_content,
            content_type="application/json",
            status=201,
        )
        yield rsps


@pytest.fixture
def resp_delete_project_sa_token():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.DELETE,
            url="http://localhost/api/v4/projects/1/service_accounts/99/personal_access_tokens/2",
            status=204,
        )
        yield rsps


@pytest.fixture
def resp_rotate_project_sa_token():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.POST,
            url="http://localhost/api/v4/projects/1/service_accounts/99/personal_access_tokens/2/rotate",
            json=proj_sa_token_rotated,
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def project_service_account(gl):
    manager = gl.projects.get(1, lazy=True).service_accounts
    return ProjectServiceAccount(manager, proj_sa_content)


# ---------------------------------------------------------------------------
# Tests – project service accounts
# ---------------------------------------------------------------------------


def test_list_project_service_accounts(gl, resp_list_project_service_accounts):
    accounts = gl.projects.get(1, lazy=True).service_accounts.list()
    assert len(accounts) == 1
    assert isinstance(accounts[0], ProjectServiceAccount)
    assert accounts[0].id == 99


def test_create_project_service_account(gl, resp_create_project_service_account):
    sa = gl.projects.get(1, lazy=True).service_accounts.create(
        {"name": "Project Service Account"}
    )
    assert isinstance(sa, ProjectServiceAccount)
    assert sa.id == 99
    assert sa.username == "project-service-account"


def test_update_project_service_account(gl, resp_update_project_service_account):
    updated = gl.projects.get(1, lazy=True).service_accounts.update(
        99, {"name": "Renamed Project SA"}
    )
    assert updated["name"] == "Renamed Project SA"


def test_save_project_service_account(
    project_service_account, resp_update_project_service_account
):
    project_service_account.name = "Renamed Project SA"
    project_service_account.save()


def test_delete_project_service_account(gl, resp_delete_project_service_account):
    gl.projects.get(1, lazy=True).service_accounts.delete(99)


def test_delete_project_service_account_via_object(
    project_service_account, resp_delete_project_service_account
):
    project_service_account.delete()


# ---------------------------------------------------------------------------
# Tests – project service account personal access tokens
# ---------------------------------------------------------------------------


def test_list_project_sa_tokens(project_service_account, resp_list_project_sa_tokens):
    tokens = project_service_account.access_tokens.list()
    assert len(tokens) == 1
    assert isinstance(tokens[0], ProjectServiceAccountAccessToken)
    assert tokens[0].name == "proj-token"


def test_create_project_sa_token(project_service_account, resp_create_project_sa_token):
    token = project_service_account.access_tokens.create(
        {"name": "proj-token", "scopes": ["read_api"]}
    )
    assert isinstance(token, ProjectServiceAccountAccessToken)
    assert token.id == 2
    assert token.token == "glpat-proj-secret"


def test_delete_project_sa_token(project_service_account, resp_delete_project_sa_token):
    project_service_account.access_tokens.delete(2)


def test_rotate_project_sa_token(project_service_account, resp_rotate_project_sa_token):
    token = ProjectServiceAccountAccessToken(
        project_service_account.access_tokens, proj_sa_token_content
    )
    token.rotate()
    assert token.token == "glpat-proj-rotated"


def test_rotate_project_sa_token_via_manager(
    project_service_account, resp_rotate_project_sa_token
):
    result = project_service_account.access_tokens.rotate(2)
    assert result["token"] == "glpat-proj-rotated"

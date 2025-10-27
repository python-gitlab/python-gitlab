"""
GitLab API: https://docs.gitlab.com/ee/api/user_service_accounts.html
"""

import pytest
import responses

create_service_account_defaults_content = {
    "id": 57,
    "username": "service_account_6018816a18e515214e0c34c2b33523fc",
    "name": "Service account user",
    "email": "service_account_6018816a18e515214e0c34c2b33523fc@noreply.gitlab.example.com",
}


create_service_account_content = {
    "id": 42,
    "username": "my_service_account",
    "name": "My Service account user",
    "email": "servicebot@example.com",
}


@pytest.fixture
def resp_create_service_account_defaults():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.POST,
            url="http://localhost/api/v4/service_accounts",
            json=create_service_account_defaults_content,
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
            json=create_service_account_content,
            content_type="application/json",
            status=200,
        )

        yield rsps


def test_create_service_account_defaults(gl, resp_create_service_account_defaults):
    service_account = gl.service_accounts.create()
    assert service_account.id == 57
    assert (
        service_account.username == "service_account_6018816a18e515214e0c34c2b33523fc"
    )
    assert service_account.name == "Service account user"
    assert (
        service_account.email
        == "service_account_6018816a18e515214e0c34c2b33523fc@noreply.gitlab.example.com"
    )


def test_create_service_account(gl, resp_create_service_account):
    service_account = gl.service_accounts.create(
        {
            "name": "My Service account user",
            "username": "my_service_account",
            "email": "servicebot@example.com",
        }
    )
    assert service_account.id == 42
    assert service_account.username == "my_service_account"
    assert service_account.name == "My Service account user"
    assert service_account.email == "servicebot@example.com"

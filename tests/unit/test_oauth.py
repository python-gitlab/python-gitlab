import pytest

from gitlab.oauth import PasswordCredentials


def test_password_credentials_without_password_raises():
    with pytest.raises(TypeError, match="missing 1 required positional argument"):
        PasswordCredentials("username")


def test_password_credentials_with_client_id_without_client_secret_raises():
    with pytest.raises(TypeError, match="client_id and client_secret must be defined"):
        PasswordCredentials(
            "username",
            "password",
            client_id="abcdef123456",
        )


def test_password_credentials_with_client_credentials_sets_basic_auth():
    credentials = PasswordCredentials(
        "username",
        "password",
        client_id="abcdef123456",
        client_secret="123456abcdef",
    )
    assert credentials.basic_auth == ("abcdef123456", "123456abcdef")

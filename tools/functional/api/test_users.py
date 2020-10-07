"""
GitLab API:
https://docs.gitlab.com/ee/api/users.html
https://docs.gitlab.com/ee/api/users.html#delete-authentication-identity-from-user
"""
import time
from pathlib import Path

import pytest
import requests


@pytest.fixture(scope="session")
def avatar_path(test_dir):
    return test_dir / "fixtures" / "avatar.png"


def test_create_user(gl, avatar_path):
    user = gl.users.create(
        {
            "email": "foo@bar.com",
            "username": "foo",
            "name": "foo",
            "password": "foo_password",
            "avatar": open(avatar_path, "rb"),
        }
    )

    created_user = gl.users.list(username="foo")[0]
    assert created_user.username == user.username
    assert created_user.email == user.email

    avatar_url = user.avatar_url.replace("gitlab.test", "localhost:8080")
    uploaded_avatar = requests.get(avatar_url).content
    assert uploaded_avatar == open(avatar_path, "rb").read()


def test_block_user(gl, user):
    user.block()
    users = gl.users.list(blocked=True)
    assert user in users

    user.unblock()
    users = gl.users.list(blocked=False)
    assert user in users


def test_delete_user(gl, wait_for_sidekiq):
    new_user = gl.users.create(
        {
            "email": "delete-user@test.com",
            "username": "delete-user",
            "name": "delete-user",
            "password": "delete-user-pass",
        }
    )

    new_user.delete()
    wait_for_sidekiq()

    assert new_user.id not in [user.id for user in gl.users.list()]


def test_user_projects_list(gl, user):
    projects = user.projects.list()
    assert len(projects) == 0


def test_user_events_list(gl, user):
    events = user.events.list()
    assert len(events) == 0


def test_user_bio(gl, user):
    user.bio = "This is the user bio"
    user.save()


def test_list_multiple_users(gl, user):
    second_email = f"{user.email}.2"
    second_username = f"{user.username}_2"
    second_user = gl.users.create(
        {
            "email": second_email,
            "username": second_username,
            "name": "Foo Bar",
            "password": "foobar_password",
        }
    )
    assert gl.users.list(search=second_user.username)[0].id == second_user.id

    expected = [user, second_user]
    actual = list(gl.users.list(search=user.username))

    assert len(expected) == len(actual)
    assert len(gl.users.list(search="asdf")) == 0


def test_user_gpg_keys(gl, user, GPG_KEY):
    gkey = user.gpgkeys.create({"key": GPG_KEY})
    assert len(user.gpgkeys.list()) == 1

    # Seems broken on the gitlab side
    # gkey = user.gpgkeys.get(gkey.id)

    gkey.delete()
    assert len(user.gpgkeys.list()) == 0


def test_user_ssh_keys(gl, user, SSH_KEY):
    key = user.keys.create({"title": "testkey", "key": SSH_KEY})
    assert len(user.keys.list()) == 1

    key.delete()
    assert len(user.keys.list()) == 0


def test_user_email(gl, user):
    email = user.emails.create({"email": "foo2@bar.com"})
    assert len(user.emails.list()) == 1

    email.delete()
    assert len(user.emails.list()) == 0


def test_user_custom_attributes(gl, user):
    attrs = user.customattributes.list()
    assert len(attrs) == 0

    attr = user.customattributes.set("key", "value1")
    assert len(gl.users.list(custom_attributes={"key": "value1"})) == 1
    assert attr.key == "key"
    assert attr.value == "value1"
    assert len(user.customattributes.list()) == 1

    attr = user.customattributes.set("key", "value2")
    attr = user.customattributes.get("key")
    assert attr.value == "value2"
    assert len(user.customattributes.list()) == 1

    attr.delete()
    assert len(user.customattributes.list()) == 0


def test_user_impersonation_tokens(gl, user):
    token = user.impersonationtokens.create(
        {"name": "token1", "scopes": ["api", "read_user"]}
    )

    tokens = user.impersonationtokens.list(state="active")
    assert len(tokens) == 1

    token.delete()
    tokens = user.impersonationtokens.list(state="active")
    assert len(tokens) == 0
    tokens = user.impersonationtokens.list(state="inactive")
    assert len(tokens) == 1


def test_user_identities(gl, user):
    provider = "test_provider"

    user.provider = provider
    user.extern_uid = "1"
    user.save()
    assert provider in [item["provider"] for item in user.identities]

    user.identityproviders.delete(provider)
    user = gl.users.get(user.id)
    assert provider not in [item["provider"] for item in user.identities]

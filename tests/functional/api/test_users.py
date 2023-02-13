"""
GitLab API:
https://docs.gitlab.com/ee/api/users.html
https://docs.gitlab.com/ee/api/users.html#delete-authentication-identity-from-user
"""

import requests


def test_create_user(gl, fixture_dir):
    user = gl.users.create(
        {
            "email": "foo@bar.com",
            "username": "foo",
            "name": "foo",
            "password": "E4596f8be406Bc3a14a4ccdb1df80587$3",
            "avatar": open(fixture_dir / "avatar.png", "rb"),
        }
    )

    created_user = gl.users.list(username="foo")[0]
    assert created_user.username == user.username
    assert created_user.email == user.email

    avatar_url = user.avatar_url.replace("gitlab.test", "localhost:8080")
    uploaded_avatar = requests.get(avatar_url).content
    with open(fixture_dir / "avatar.png", "rb") as f:
        assert uploaded_avatar == f.read()


def test_block_user(gl, user):
    result = user.block()
    assert result is True
    users = gl.users.list(blocked=True)
    assert user in users

    # block again
    result = user.block()
    # Trying to block an already blocked user returns None
    assert result is None

    result = user.unblock()
    assert result is True
    users = gl.users.list(blocked=False)
    assert user in users

    # unblock again
    result = user.unblock()
    # Trying to unblock an already blocked user returns False
    assert result is False


def test_ban_user(gl, user):
    user.ban()
    retrieved_user = gl.users.get(user.id)
    assert retrieved_user.state == "banned"

    user.unban()
    retrieved_user = gl.users.get(user.id)
    assert retrieved_user.state == "active"


def test_delete_user(gl, wait_for_sidekiq):
    new_user = gl.users.create(
        {
            "email": "delete-user@test.com",
            "username": "delete-user",
            "name": "delete-user",
            "password": "E4596f8be406Bc3a14a4ccdb1df80587#!",
        }
    )

    new_user.delete()
    wait_for_sidekiq(timeout=60)

    assert new_user.id not in [user.id for user in gl.users.list()]


def test_user_projects_list(gl, user):
    projects = user.projects.list()
    assert isinstance(projects, list)
    assert not projects


def test_user_events_list(gl, user):
    events = user.events.list()
    assert isinstance(events, list)
    assert not events


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
            "password": "E4596f8be406Bc3a14a4ccdb1df80587#!",
        }
    )
    assert gl.users.list(search=second_user.username)[0].id == second_user.id

    expected = [user, second_user]
    actual = list(gl.users.list(search=user.username))

    assert set(expected) == set(actual)
    assert not gl.users.list(search="asdf")


def test_user_gpg_keys(gl, user, GPG_KEY):
    gkey = user.gpgkeys.create({"key": GPG_KEY})
    assert gkey in user.gpgkeys.list()

    # Seems broken on the gitlab side
    # gkey = user.gpgkeys.get(gkey.id)

    gkey.delete()
    assert gkey not in user.gpgkeys.list()


def test_user_ssh_keys(gl, user, SSH_KEY):
    key = user.keys.create({"title": "testkey", "key": SSH_KEY})
    assert key in user.keys.list()

    get_key = user.keys.get(key.id)
    assert get_key.key == key.key

    key.delete()
    assert key not in user.keys.list()


def test_user_email(gl, user):
    email = user.emails.create({"email": "foo2@bar.com"})
    assert email in user.emails.list()

    email.delete()
    assert email not in user.emails.list()


def test_user_custom_attributes(gl, user):
    attrs = user.customattributes.list()
    assert not attrs

    attr = user.customattributes.set("key", "value1")
    assert user in gl.users.list(custom_attributes={"key": "value1"})
    assert attr.key == "key"
    assert attr.value == "value1"
    assert attr in user.customattributes.list()

    attr = user.customattributes.set("key", "value2")
    attr = user.customattributes.get("key")
    assert attr.value == "value2"
    assert attr in user.customattributes.list()

    attr.delete()
    assert attr not in user.customattributes.list()


def test_user_impersonation_tokens(gl, user):
    token = user.impersonationtokens.create(
        {"name": "token1", "scopes": ["api", "read_user"]}
    )
    assert token in user.impersonationtokens.list(state="active")

    token.delete()
    assert token not in user.impersonationtokens.list(state="active")
    assert token in user.impersonationtokens.list(state="inactive")


def test_user_identities(gl, user):
    provider = "test_provider"

    user.provider = provider
    user.extern_uid = "1"
    user.save()
    assert provider in [item["provider"] for item in user.identities]

    user.identityproviders.delete(provider)
    user = gl.users.get(user.id)
    assert provider not in [item["provider"] for item in user.identities]

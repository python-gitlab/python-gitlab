"""
GitLab API:
https://docs.gitlab.com/ee/api/users.html
https://docs.gitlab.com/ee/api/users.html#delete-authentication-identity-from-user
"""


def test_user_identities(gl, user):
    provider = "test_provider"

    user.provider = provider
    user.extern_uid = "1"
    user.save()

    assert provider in [item["provider"] for item in user.identities]

    user.identityproviders.delete(provider)
    user = gl.users.get(user.id)

    assert provider not in [item["provider"] for item in user.identities]

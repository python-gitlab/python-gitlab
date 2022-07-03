def test_current_user_email(gl):
    gl.auth()
    mail = gl.user.emails.create({"email": "current@user.com"})
    assert mail in gl.user.emails.list()

    mail.delete()
    assert mail not in gl.user.emails.list()


def test_current_user_gpg_keys(gl, GPG_KEY):
    gl.auth()
    gkey = gl.user.gpgkeys.create({"key": GPG_KEY})
    assert gkey in gl.user.gpgkeys.list()

    # Seems broken on the gitlab side
    gkey = gl.user.gpgkeys.get(gkey.id)
    gkey.delete()
    assert gkey not in gl.user.gpgkeys.list()


def test_current_user_ssh_keys(gl, SSH_KEY):
    gl.auth()
    key = gl.user.keys.create({"title": "testkey", "key": SSH_KEY})
    assert key in gl.user.keys.list()

    key.delete()
    assert key not in gl.user.keys.list()


def test_current_user_status(gl):
    gl.auth()
    message = "Test"
    emoji = "thumbsup"
    status = gl.user.status.get()

    status.message = message
    status.emoji = emoji
    status.save()

    new_status = gl.user.status.get()
    assert new_status.message == message
    assert new_status.emoji == emoji

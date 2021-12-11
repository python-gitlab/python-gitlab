def test_current_user_email(gl):
    gl.auth()
    mail = gl.user.emails.create({"email": "current@user.com"})
    assert len(gl.user.emails.list()) == 2

    mail.delete()
    assert len(gl.user.emails.list()) == 1


def test_current_user_gpg_keys(gl, GPG_KEY):
    gl.auth()
    gkey = gl.user.gpgkeys.create({"key": GPG_KEY})
    assert len(gl.user.gpgkeys.list()) == 1

    # Seems broken on the gitlab side
    gkey = gl.user.gpgkeys.get(gkey.id)
    gkey.delete()
    assert len(gl.user.gpgkeys.list()) == 0


def test_current_user_ssh_keys(gl, SSH_KEY):
    gl.auth()
    key = gl.user.keys.create({"title": "testkey", "key": SSH_KEY})
    assert len(gl.user.keys.list()) == 1

    key.delete()
    assert len(gl.user.keys.list()) == 0


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

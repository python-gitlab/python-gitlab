"""
GitLab API:
https://docs.gitlab.com/ce/api/keys.html
"""

import base64
import hashlib


def key_fingerprint(key: str) -> str:
    key_part = key.split()[1]
    decoded = base64.b64decode(key_part.encode("ascii"))
    digest = hashlib.sha256(decoded).digest()
    return f"SHA256:{base64.b64encode(digest).rstrip(b'=').decode('utf-8')}"


def test_keys_ssh(gl, user, SSH_KEY):
    key = user.keys.create({"title": "foo@bar", "key": SSH_KEY})

    # Get key by ID (admin only).
    key_by_id = gl.keys.get(key.id)
    assert key_by_id.title == key.title
    assert key_by_id.key == key.key

    fingerprint = key_fingerprint(SSH_KEY)
    # Get key by fingerprint (admin only).
    key_by_fingerprint = gl.keys.get(fingerprint=fingerprint)
    assert key_by_fingerprint.title == key.title
    assert key_by_fingerprint.key == key.key

    key.delete()


def test_keys_deploy(gl, project, DEPLOY_KEY):
    key = project.keys.create({"title": "foo@bar", "key": DEPLOY_KEY})

    fingerprint = key_fingerprint(DEPLOY_KEY)
    key_by_fingerprint = gl.keys.get(fingerprint=fingerprint)
    assert key_by_fingerprint.title == key.title
    assert key_by_fingerprint.key == key.key
    assert len(key_by_fingerprint.deploy_keys_projects) == 1

    key.delete()

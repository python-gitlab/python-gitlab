"""
GitLab API: https://docs.gitlab.com/ce/api/keys.html
"""

import pytest
import responses

from gitlab.v4.objects import Key

key_content = {"id": 1, "title": "title", "key": "ssh-keytype AAAAC3Nza/key comment"}


@pytest.fixture
def resp_get_key_by_id():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/keys/1",
            json=key_content,
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_get_key_by_fingerprint():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/keys?fingerprint=foo",
            json=key_content,
            content_type="application/json",
            status=200,
        )
        yield rsps


def test_get_key_by_id(gl, resp_get_key_by_id):
    key = gl.keys.get(1)
    assert isinstance(key, Key)
    assert key.id == 1
    assert key.title == "title"


def test_get_key_by_fingerprint(gl, resp_get_key_by_fingerprint):
    key = gl.keys.get(fingerprint="foo")
    assert isinstance(key, Key)
    assert key.id == 1
    assert key.title == "title"


def test_get_key_missing_attrs(gl):
    with pytest.raises(AttributeError):
        gl.keys.get()

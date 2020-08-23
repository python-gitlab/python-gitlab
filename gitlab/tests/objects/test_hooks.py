"""
GitLab API: https://docs.gitlab.com/ce/api/system_hooks.html
"""
import pytest
import responses

from gitlab.v4.objects import Hook


@pytest.fixture
def resp_get_hook():
    content = {"url": "testurl", "id": 1}

    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/hooks/1",
            json=content,
            content_type="application/json",
            status=200,
        )
        yield rsps


def test_hooks(gl, resp_get_hook):
    data = gl.hooks.get(1)
    assert isinstance(data, Hook)
    assert data.url == "testurl"
    assert data.id == 1

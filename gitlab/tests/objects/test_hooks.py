"""
GitLab API: https://docs.gitlab.com/ce/api/system_hooks.html
"""

from httmock import response, urlmatch, with_httmock

from gitlab.v4.objects import Hook

from .mocks import headers


@urlmatch(scheme="http", netloc="localhost", path="/api/v4/hooks/1", method="get")
def resp_get_hook(url, request):
    content = '{"url": "testurl", "id": 1}'.encode("utf-8")
    return response(200, content, headers, None, 5, request)


@with_httmock(resp_get_hook)
def test_hooks(gl):
    data = gl.hooks.get(1)
    assert isinstance(data, Hook)
    assert data.url == "testurl"
    assert data.id == 1

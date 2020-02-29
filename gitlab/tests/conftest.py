import asyncio

import pytest

from gitlab import AsyncGitlab, Gitlab

gitlab_kwargs = {
    "url": "http://localhost",
    "private_token": "private_token",
    "api_version": 4,
}


@pytest.fixture(
    params=[Gitlab(**gitlab_kwargs), AsyncGitlab(**gitlab_kwargs)],
    ids=["sync", "async"],
)
def gl(request):
    return request.param


async def awaiter(v):
    if asyncio.iscoroutine(v):
        return await v
    else:
        return v


async def returner(v):
    return v


@pytest.fixture
def gl_get_value(gl):
    """Fixture that returns async function that either return input value or awaits it

    Usage::

        result = gl.http_get()
        result = await gl_get_value(result)
    """
    if isinstance(gl, Gitlab):
        return returner
    else:
        return awaiter


@pytest.fixture
def is_gl_sync(gl):
    """If gitlab client sync or not
    """
    if isinstance(gl, Gitlab):
        return True
    else:
        return False

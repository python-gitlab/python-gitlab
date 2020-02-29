import asyncio

import pytest

from gitlab import AsyncGitlab, Gitlab


@pytest.fixture(params=[Gitlab, AsyncGitlab], ids=["sync", "async"])
def gitlab_class(request):
    return request.param


@pytest.fixture
def gl(gitlab_class):
    return gitlab_class(
        "http://localhost", private_token="private_token", api_version=4
    )


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
    
    Result function is based on client not the value of function argument, 
    so if we accidentally mess up with return gitlab client value, then 
    we will know

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

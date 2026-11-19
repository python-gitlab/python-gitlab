import time
from unittest import mock

import anyio
import pytest

from gitlab import utils


def test_handle_retry_on_status_ignores_unknown_status_code():
    retry = utils.Retry(max_retries=1, retry_transient_errors=True)
    assert retry.handle_retry_on_status(418) is False


def test_handle_retry_on_status_accepts_retry_after_header(
    monkeypatch: pytest.MonkeyPatch,
):
    mock_sleep = mock.Mock()
    monkeypatch.setattr(time, "sleep", mock_sleep)
    retry = utils.Retry(max_retries=1)
    headers = {"Retry-After": "1"}

    assert retry.handle_retry_on_status(429, headers=headers) is True
    assert isinstance(mock_sleep.call_args[0][0], int)


def test_handle_retry_on_status_accepts_ratelimit_reset_header(
    monkeypatch: pytest.MonkeyPatch,
):
    mock_sleep = mock.Mock()
    monkeypatch.setattr(time, "sleep", mock_sleep)

    retry = utils.Retry(max_retries=1)
    headers = {"RateLimit-Reset": str(int(time.time() + 1))}

    assert retry.handle_retry_on_status(429, headers=headers) is True
    assert isinstance(mock_sleep.call_args[0][0], float)


def test_handle_retry_on_status_returns_false_when_max_retries_reached():
    retry = utils.Retry(max_retries=0)
    assert retry.handle_retry_on_status(429) is False


@pytest.mark.anyio
async def test_async_handle_retry_on_status_ignores_unknown_status_code():
    retry = utils.Retry(max_retries=1, retry_transient_errors=True)
    assert await retry.async_handle_retry_on_status(418) is False


@pytest.mark.anyio
async def test_async_handle_retry_on_status_awaits_sleep(
    monkeypatch: pytest.MonkeyPatch,
):
    mock_sleep = mock.Mock()
    mock_async_sleep = mock.AsyncMock()
    monkeypatch.setattr(time, "sleep", mock_sleep)
    monkeypatch.setattr(anyio, "sleep", mock_async_sleep)
    retry = utils.Retry(max_retries=1)
    headers = {"Retry-After": "1"}

    assert await retry.async_handle_retry_on_status(429, headers=headers) is True
    mock_async_sleep.assert_awaited_once_with(1)
    mock_sleep.assert_not_called()


@pytest.mark.anyio
async def test_async_handle_retry_on_status_returns_false_when_max_retries_reached():
    retry = utils.Retry(max_retries=0)
    assert await retry.async_handle_retry_on_status(429) is False

import time
from unittest import mock

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


@pytest.mark.parametrize(
    ("retry_after", "delay"),
    [
        ("Wed, 21 Oct 2015 07:28:00 GMT", 60),
        ("Wednesday, 21-Oct-15 07:28:00 GMT", 60),
        ("Wed Oct 21 07:28:00 2015", 60),
        ("Wed, 21 Oct 2015 07:26:00 GMT", 0),
    ],
)
def test_handle_retry_on_status_accepts_retry_after_date(
    monkeypatch: pytest.MonkeyPatch, retry_after: str, delay: int
):
    mock_sleep = mock.Mock()
    monkeypatch.setattr(time, "sleep", mock_sleep)
    monkeypatch.setattr(time, "time", lambda: 1445412420)
    retry = utils.Retry(max_retries=1)

    assert retry.handle_retry_on_status(429, {"Retry-After": retry_after}) is True
    mock_sleep.assert_called_once_with(delay)


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

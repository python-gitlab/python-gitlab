import time
from unittest import mock

import pytest
import requests

from gitlab import utils
from gitlab._backends import requests_backend


def test_handle_retry_on_status_ignores_unknown_status_code():
    retry = utils.Retry(max_retries=1, retry_transient_errors=True)
    response = requests.Response()
    response.status_code = 418
    backend_response = requests_backend.RequestsResponse(response)

    assert retry.handle_retry_on_status(backend_response) is False


def test_handle_retry_on_status_accepts_retry_after_header(
    monkeypatch: pytest.MonkeyPatch,
):
    mock_sleep = mock.Mock()
    monkeypatch.setattr(time, "sleep", mock_sleep)

    retry = utils.Retry(max_retries=1)
    response = requests.Response()
    response.status_code = 429
    response.headers["Retry-After"] = "1"
    backend_response = requests_backend.RequestsResponse(response)

    assert retry.handle_retry_on_status(backend_response) is True
    assert isinstance(mock_sleep.call_args[0][0], int)


def test_handle_retry_on_status_accepts_ratelimit_reset_header(
    monkeypatch: pytest.MonkeyPatch,
):
    mock_sleep = mock.Mock()
    monkeypatch.setattr(time, "sleep", mock_sleep)

    retry = utils.Retry(max_retries=1)
    response = requests.Response()
    response.status_code = 429
    response.headers["RateLimit-Reset"] = str(int(time.time() + 1))
    backend_response = requests_backend.RequestsResponse(response)

    assert retry.handle_retry_on_status(backend_response) is True
    assert isinstance(mock_sleep.call_args[0][0], float)


def test_handle_retry_on_status_returns_false_when_max_retries_reached():
    retry = utils.Retry(max_retries=0)
    response = requests.Response()
    response.status_code = 429
    backend_response = requests_backend.RequestsResponse(response)

    assert retry.handle_retry_on_status(backend_response) is False

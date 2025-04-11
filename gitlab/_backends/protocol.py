from __future__ import annotations

import abc
from typing import Any, Protocol

import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder  # type: ignore


class BackendResponse(Protocol):
    @abc.abstractmethod
    def __init__(self, response: requests.Response) -> None: ...


class Backend(Protocol):
    @abc.abstractmethod
    def http_request(
        self,
        method: str,
        url: str,
        json: dict[str, Any] | bytes | None,
        data: dict[str, Any] | MultipartEncoder | None,
        params: Any | None,
        timeout: float | None,
        verify: bool | str | None,
        stream: bool | None,
        **kwargs: Any,
    ) -> BackendResponse: ...

from __future__ import annotations

import sys
from typing import Any, Dict, Optional, Union

import gitlab

try:
    import httpx
except ImportError:
    sys.exit(
        "Using httpx, but the 'httpx' package is not installed. "
        "Make sure to install httpx using "
        "`pip install python-gitlab[httpx]`."
    )


class _Httpx_Client:
    def __init__(
        self,
        url: Optional[str] = None,
        http_client: Optional[httpx.Client] = None,
    ) -> None:
        self._client = http_client or httpx.Client()
        self._base_url = self._get_base_url(url)

    def __enter__(self: _Httpx_Client) -> _Httpx_Client:
        return self

    def __exit__(self, *args: Any) -> None:
        return self._client.close()

    def close(self: _Httpx_Client) -> None:
        self._client.close()

    def http_get(
        self,
        path: str,
        query_data: Optional[Dict[str, Any]] = None,
        streamed: bool = False,
        raw: bool = False,
        **kwargs: Any,
    ) -> Union[Dict[str, Any], httpx.Response]:
        pass

    def http_head(
        self: _Httpx_Client,
        path: str,
        query_data: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Any:
        pass

    def http_post(
        self: _Httpx_Client,
        path: str,
        query_data: Optional[Dict[str, Any]] = None,
        post_data: Optional[Dict[str, Any]] = None,
        raw: bool = False,
        files: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Union[Dict[str, Any], Any]:
        pass

    def http_put(
        self: _Httpx_Client,
        path: str,
        query_data: Optional[Dict[str, Any]] = None,
        post_data: Optional[Union[Dict[str, Any], bytes]] = None,
        raw: bool = False,
        files: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Union[Dict[str, Any], Any]:
        pass

    def http_delete(self: _Httpx_Client, path: str, **kwargs: Any) -> Any:
        pass

    def http_request(
        self,
        verb: str,
        path: str,
        query_data: Optional[Dict[str, Any]] = None,
        post_data: Optional[Union[Dict[str, Any], bytes]] = None,
        raw: bool = False,
        streamed: bool = False,
        files: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = None,
        obey_rate_limit: bool = True,
        retry_transient_errors: Optional[bool] = None,
        max_retries: int = 10,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        pass

    @staticmethod
    def _get_base_url(url: Optional[str] = None) -> str:
        """Return the base URL with the trailing slash stripped.
        If the URL is a Falsy value, return the default URL.
        Returns:
            The base URL
        """
        if not url:
            return gitlab.const.DEFAULT_URL

        return url.rstrip("/")

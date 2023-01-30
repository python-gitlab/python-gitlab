from __future__ import annotations

from typing import Any, Dict, Optional, Tuple, TYPE_CHECKING, Union

import requests
from requests.structures import CaseInsensitiveDict
from requests_toolbelt.multipart.encoder import MultipartEncoder  # type: ignore


class RequestsResponse:
    def __init__(self, response: requests.Response) -> None:
        self._response: requests.Response = response

    @property
    def response(self) -> requests.Response:
        return self._response

    @property
    def status_code(self) -> int:
        return self._response.status_code

    @property
    def headers(self) -> CaseInsensitiveDict[str]:
        return self._response.headers

    @property
    def content(self) -> bytes:
        return self._response.content

    @property
    def reason(self) -> str:
        return self._response.reason

    def json(self) -> Any:
        return self._response.json()


class RequestsBackend:
    def __init__(self, session: Optional[requests.Session] = None) -> None:
        self._client: requests.Session = session or requests.Session()

    @property
    def client(self) -> requests.Session:
        return self._client

    @staticmethod
    def prepare_send_data(
        files: Optional[Dict[str, Any]] = None,
        post_data: Optional[Union[Dict[str, Any], bytes]] = None,
        raw: bool = False,
    ) -> Tuple[
        Optional[Union[Dict[str, Any], bytes]],
        Optional[Union[Dict[str, Any], MultipartEncoder]],
        str,
    ]:
        if files:
            if post_data is None:
                post_data = {}
            else:
                # booleans does not exists for data (neither for MultipartEncoder):
                # cast to string int to avoid: 'bool' object has no attribute 'encode'
                if TYPE_CHECKING:
                    assert isinstance(post_data, dict)
                for k, v in post_data.items():
                    if isinstance(v, bool):
                        post_data[k] = str(int(v))
            post_data["file"] = files.get("file")
            post_data["avatar"] = files.get("avatar")

            data = MultipartEncoder(post_data)
            return (None, data, data.content_type)

        if raw and post_data:
            return (None, post_data, "application/octet-stream")

        return (post_data, None, "application/json")

    def http_request(
        self,
        method: str,
        url: str,
        json: Optional[Union[Dict[str, Any], bytes]] = None,
        data: Optional[Union[Dict[str, Any], MultipartEncoder]] = None,
        params: Optional[Any] = None,
        timeout: Optional[float] = None,
        verify: Optional[Union[bool, str]] = True,
        stream: Optional[bool] = False,
        **kwargs: Any,
    ) -> RequestsResponse:
        """Make HTTP request

        Args:
            method: The HTTP method to call ('get', 'post', 'put', 'delete', etc.)
            url: The full URL
            data: The data to send to the server in the body of the request
            json: Data to send in the body in json by default
            timeout: The timeout, in seconds, for the request
            verify: Whether SSL certificates should be validated. If
                the value is a string, it is the path to a CA file used for
                certificate validation.
            stream: Whether the data should be streamed

        Returns:
            A requests Response object.
        """
        response: requests.Response = self._client.request(
            method=method,
            url=url,
            params=params,
            data=data,
            timeout=timeout,
            stream=stream,
            verify=verify,
            json=json,
            **kwargs,
        )
        return RequestsResponse(response=response)

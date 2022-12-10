from typing import Any, Dict, Optional, Union

import requests
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
    def headers(self) -> Any:
        return self._response.headers

    @property
    def content(self) -> bytes:
        return self._response.content

    def json(self) -> Any:
        return self._response.json()


class RequestsBackend:
    def __init__(self, session: Optional[requests.Session] = None) -> None:
        self._client: requests.Session = session or requests.Session()

    @property
    def client(self) -> requests.Session:
        return self._client

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
        **kwargs: Any
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
            **kwargs
        )
        return RequestsResponse(response=response)

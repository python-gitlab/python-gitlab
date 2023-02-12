import abc
import sys
from typing import Any, Dict, Optional, Union

import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder  # type: ignore

if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol


class BackendResponse(Protocol):
    @abc.abstractmethod
    def __init__(self, response: requests.Response) -> None:
        ...


class Backend(Protocol):
    @abc.abstractmethod
    def http_request(
        self,
        method: str,
        url: str,
        json: Optional[Union[Dict[str, Any], bytes]],
        data: Optional[Union[Dict[str, Any], MultipartEncoder]],
        params: Optional[Any],
        timeout: Optional[float],
        verify: Optional[Union[bool, str]],
        stream: Optional[bool],
        **kwargs: Any,
    ) -> BackendResponse:
        ...

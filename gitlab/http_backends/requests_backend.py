from typing import Optional

import requests


class RequestsBackend:
    def __init__(
        self,
        session: Optional[requests.Session] = None,
        timeout: Optional[float] = None,
    ) -> None:
        self._client: requests.Session = session or requests.Session()
        self._timeout: Optional[float] = timeout

    @property
    def client(self) -> requests.Session:
        return self._client

    @property
    def timeout(self) -> Optional[float]:
        return self._timeout

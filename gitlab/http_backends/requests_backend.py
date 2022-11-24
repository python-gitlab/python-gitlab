from typing import Optional

import requests


class RequestsBackend:
    def __init__(self, session: Optional[requests.Session] = None) -> None:
        self._client: requests.Session = session or requests.Session()

    @property
    def client(self) -> requests.Session:
        return self._client

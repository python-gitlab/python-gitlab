from typing import Any

import requests
from gql.transport.requests import RequestsHTTPTransport


class GitlabSyncTransport(RequestsHTTPTransport):
    """A gql requests transport that reuses an existing requests.Session.

    By default, gql's requests transport does not have a keep-alive session
    and does not enable providing your own session.

    This transport lets us provide and close our session on our own.
    For details, see https://github.com/graphql-python/gql/issues/91.
    """

    def __init__(self, *args: Any, session: requests.Session, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self.session = session

    def connect(self) -> None:
        pass

    def close(self) -> None:
        pass

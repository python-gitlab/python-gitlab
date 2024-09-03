from typing import Any

import httpx
from gql.transport.httpx import HTTPXTransport


class GitlabTransport(HTTPXTransport):
    """A gql httpx transport that reuses an existing httpx.Client.
    By default, gql's transports do not have a keep-alive session
    and do not enable providing your own session that's kept open.
    This transport lets us provide and close our session on our own
    and provide additional auth.
    For details, see https://github.com/graphql-python/gql/issues/91.
    """

    def __init__(self, *args: Any, client: httpx.Client, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self.client = client

    def connect(self) -> None:
        pass

    def close(self) -> None:
        pass

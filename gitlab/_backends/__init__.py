"""
Defines http backends for processing http requests
"""

from .requests_backend import (
    JobTokenAuth,
    OAuthTokenAuth,
    PrivateTokenAuth,
    RequestsBackend,
    RequestsResponse,
)

DefaultBackend = RequestsBackend
DefaultResponse = RequestsResponse

__all__ = [
    "DefaultBackend",
    "DefaultResponse",
    "JobTokenAuth",
    "OAuthTokenAuth",
    "PrivateTokenAuth",
]

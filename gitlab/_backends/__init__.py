"""
Defines http backends for processing http requests
"""

from .requests_backend import RequestsBackend, RequestsResponse

DefaultBackend = RequestsBackend
DefaultResponse = RequestsResponse

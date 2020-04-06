"""Common mocks for resources in gitlab.v4.objects"""

from httmock import response, urlmatch


headers = {"content-type": "application/json"}
binary_content = b"binary content"


@urlmatch(
    scheme="http",
    netloc="localhost",
    path="/api/v4/(groups|projects)/1/export",
    method="post",
)
def resp_create_export(url, request):
    """Common mock for Group/Project Export POST response."""
    content = """{
    "message": "202 Accepted"
    }"""
    content = content.encode("utf-8")
    return response(202, content, headers, None, 25, request)


@urlmatch(
    scheme="http",
    netloc="localhost",
    path="/api/v4/(groups|projects)/1/export/download",
    method="get",
)
def resp_download_export(url, request):
    """Common mock for Group/Project Export Download GET response."""
    headers = {"content-type": "application/octet-stream"}
    content = binary_content
    return response(200, content, headers, None, 25, request)

import requests
import responses

from gitlab import _backends


@responses.activate
def test_streamed_response_content_with_requests(capsys):
    responses.add(
        method="GET",
        url="https://example.com",
        status=200,
        body="test",
        content_type="application/octet-stream",
    )

    resp = requests.get("https://example.com", stream=True)
    _backends.RequestsBackend.response_content(
        resp, streamed=True, action=None, chunk_size=1024, iterator=False
    )

    captured = capsys.readouterr()
    assert "test" in captured.out

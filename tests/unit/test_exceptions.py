import pytest

from gitlab import exceptions


def test_error_raises_from_http_error():
    """Methods decorated with @on_http_error should raise from GitlabHttpError."""

    class TestError(Exception):
        pass

    @exceptions.on_http_error(TestError)
    def raise_error_from_http_error():
        raise exceptions.GitlabHttpError

    with pytest.raises(TestError) as context:
        raise_error_from_http_error()
    assert isinstance(context.value.__cause__, exceptions.GitlabHttpError)


def test_gitlabauthenticationerror_with_auth_type():
    with pytest.raises(exceptions.GitlabAuthenticationError) as context:
        raise exceptions.GitlabAuthenticationError(
            error_message="401 Unauthorized",
            response_code=401,
            response_body=b"bad user",
            auth_type="job_token",
        )
    assert "authentication_type" in str(context.value)
    assert "job_token" in str(context.value)
    assert "401 Unauthorized" in str(context.value)


def test_gitlabauthenticationerror_no_auth_type():
    with pytest.raises(exceptions.GitlabAuthenticationError) as context:
        raise exceptions.GitlabAuthenticationError(
            error_message="401 Unauthorized",
            response_code=401,
            response_body=b"bad user",
        )
    assert "authentication_type" not in str(context.value)
    assert "401 Unauthorized" in str(context.value)

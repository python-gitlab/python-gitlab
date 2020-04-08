import unittest

from gitlab import exceptions
import pytest


class TestExceptions(unittest.TestCase):
    def test_error_raises_from_http_error(self):
        """Methods decorated with @on_http_error should raise from GitlabHttpError."""

        class TestError(Exception):
            pass

        @exceptions.on_http_error(TestError)
        def raise_error_from_http_error():
            raise exceptions.GitlabHttpError

        with pytest.raises(TestError) as context:
            raise_error_from_http_error()
        assert isinstance(context.value.__cause__, exceptions.GitlabHttpError)

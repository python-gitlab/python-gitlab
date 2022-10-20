import pytest


def test_install() -> None:
    with pytest.raises(ImportError):
        import httpx  # noqa

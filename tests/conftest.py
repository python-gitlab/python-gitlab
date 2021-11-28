import pytest


@pytest.fixture(scope="session")
def test_dir(pytestconfig):
    return pytestconfig.rootdir / "tests"

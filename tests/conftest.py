import pytest


@pytest.fixture(scope="session")
def test_dir(pytestconfig):
    return pytestconfig.rootdir / "tests"


@pytest.fixture
def valid_gitlab_ci_yml():
    return """---
:test_job:
  :script: echo 1
"""


@pytest.fixture
def invalid_gitlab_ci_yml():
    return "invalid"

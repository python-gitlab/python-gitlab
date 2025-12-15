"""
pytest-docker fixture overrides.
See https://github.com/avast/pytest-docker#available-fixtures.
"""

import pytest


@pytest.fixture(scope="session")
def docker_compose_project_name():
    """Set a consistent project name to enable optional reuse of containers."""
    return "pytest-python-gitlab"


@pytest.fixture(scope="session")
def docker_compose_file(fixture_dir):
    return fixture_dir / "docker-compose.yml"


@pytest.fixture(scope="session")
def docker_cleanup(request):
    """Conditionally keep containers around by overriding the cleanup command."""
    if request.config.getoption("--keep-containers"):
        # Print version and exit.
        return "-v"
    return "down -v"

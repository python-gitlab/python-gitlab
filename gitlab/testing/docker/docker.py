"""
pytest-docker fixture overrides.
See https://github.com/avast/pytest-docker#available-fixtures.
"""

import pytest
import pytest_docker


@pytest.fixture(scope="session")
def docker_compose_project_name():
    """Set a consistent project name to enable optional reuse of containers."""
    return "pytest-python-gitlab"


pytest_docker.docker_compose_project_name = docker_compose_project_name


@pytest.fixture(scope="session")
def docker_compose_file(docker_assets_dir):
    return docker_assets_dir / "docker-compose.yml"


pytest_docker.docker_compose_file = docker_compose_file


@pytest.fixture(scope="session")
def docker_cleanup(request):
    """Conditionally keep containers around by overriding the cleanup command."""
    if request.config.getoption("--keep-containers-running"):
        # Print version and exit.
        return "-v"
    if request.config.getoption("--keep-containers"):
        # Stop the containers.
        return "stop"
    return "down"


pytest_docker.docker_cleanup = docker_cleanup

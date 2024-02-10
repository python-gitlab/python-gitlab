import pytest
import responses

from gitlab.const import DEFAULT_URL


@pytest.fixture
def gitlab_cli(script_runner, gitlab_config):
    """Wrapper fixture to help make test cases less verbose."""

    def _gitlab_cli(subcommands):
        """
        Return a script_runner.run method that takes a default gitlab
        command, and subcommands passed as arguments inside test cases.
        """
        command = ["gitlab", "--config-file", gitlab_config]

        for subcommand in subcommands:
            # ensure we get strings (e.g from IDs)
            command.append(str(subcommand))

        return script_runner.run(command)

    return _gitlab_cli


@pytest.fixture
def resp_get_project():
    return {
        "method": responses.GET,
        "url": f"{DEFAULT_URL}/api/v4/projects/1",
        "json": {"name": "name", "path": "test-path", "id": 1},
        "content_type": "application/json",
        "status": 200,
    }


@pytest.fixture
def resp_current_user():
    return {
        "method": responses.GET,
        "url": f"{DEFAULT_URL}/api/v4/user",
        "json": {"username": "name", "id": 1},
        "content_type": "application/json",
        "status": 200,
    }


@pytest.fixture
def resp_delete_registry_tags_in_bulk():
    return {
        "method": responses.DELETE,
        "url": f"{DEFAULT_URL}/api/v4/projects/1/registry/repositories/1/tags",
        "status": 202,
    }

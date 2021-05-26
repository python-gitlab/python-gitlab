import pytest


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

        return script_runner.run(*command)

    return _gitlab_cli

import tempfile
import time
import uuid
from pathlib import Path
from random import randint
from subprocess import check_output

import pytest

import gitlab


def reset_gitlab(gl):
    # previously tools/reset_gitlab.py
    for project in gl.projects.list():
        project.delete()
    for group in gl.groups.list():
        group.delete()
    for variable in gl.variables.list():
        variable.delete()
    for user in gl.users.list():
        if user.username != "root":
            user.delete()


def set_token(container, rootdir):
    set_token_rb = rootdir / "fixtures" / "set_token.rb"

    with open(set_token_rb, "r") as f:
        set_token_command = f.read().strip()

    rails_command = [
        "docker",
        "exec",
        container,
        "gitlab-rails",
        "runner",
        set_token_command,
    ]
    output = check_output(rails_command).decode().strip()

    return output


@pytest.fixture(scope="session")
def temp_dir():
    return Path(tempfile.gettempdir())


@pytest.fixture(scope="session")
def test_dir(pytestconfig):
    return pytestconfig.rootdir / "tools" / "functional"


@pytest.fixture(scope="session")
def docker_compose_file(test_dir):
    return test_dir / "fixtures" / "docker-compose.yml"


@pytest.fixture(scope="session")
def check_is_alive(request):
    """
    Return a healthcheck function fixture for the GitLab container spinup.
    """
    start = time.time()

    # Temporary manager to disable capsys in a session-scoped fixture
    # so people know it takes a while for GitLab to spin up
    # https://github.com/pytest-dev/pytest/issues/2704
    capmanager = request.config.pluginmanager.getplugin("capturemanager")

    def _check(container):
        delay = int(time.time() - start)

        with capmanager.global_and_fixture_disabled():
            print(f"Waiting for GitLab to reconfigure.. (~{delay}s)")

        logs = ["docker", "logs", container]
        output = check_output(logs).decode()

        return "gitlab Reconfigured!" in output

    return _check


@pytest.fixture(scope="session")
def gitlab_config(check_is_alive, docker_ip, docker_services, temp_dir, test_dir):
    config_file = temp_dir / "python-gitlab.cfg"
    port = docker_services.port_for("gitlab", 80)

    docker_services.wait_until_responsive(
        timeout=180, pause=5, check=lambda: check_is_alive("gitlab-test")
    )

    token = set_token("gitlab-test", rootdir=test_dir)

    config = f"""[global]
default = local
timeout = 60

[local]
url = http://{docker_ip}:{port}
private_token = {token}
api_version = 4"""

    with open(config_file, "w") as f:
        f.write(config)

    return config_file


@pytest.fixture(scope="session")
def gl(gitlab_config):
    """Helper instance to make fixtures and asserts directly via the API."""

    instance = gitlab.Gitlab.from_config("local", [gitlab_config])
    reset_gitlab(instance)

    return instance


@pytest.fixture(scope="module")
def group(gl):
    """Group fixture for group API resource tests."""
    _id = uuid.uuid4().hex
    data = {
        "name": f"test-group-{_id}",
        "path": f"group-{_id}",
    }
    group = gl.groups.create(data)

    yield group

    try:
        group.delete()
    except gitlab.exceptions.GitlabDeleteError as e:
        print(f"Group already deleted: {e}")


@pytest.fixture(scope="module")
def project(gl):
    """Project fixture for project API resource tests."""
    _id = uuid.uuid4().hex
    name = f"test-project-{_id}"

    project = gl.projects.create(name=name)

    yield project

    try:
        project.delete()
    except gitlab.exceptions.GitlabDeleteError as e:
        print(f"Project already deleted: {e}")


@pytest.fixture(scope="module")
def user(gl):
    """User fixture for user API resource tests."""
    _id = uuid.uuid4().hex
    email = f"user{_id}@email.com"
    username = f"user{_id}"
    name = f"User {_id}"
    password = "fakepassword"

    user = gl.users.create(email=email, username=username, name=name, password=password)

    yield user

    try:
        user.delete()
    except gitlab.exceptions.GitlabDeleteError as e:
        print(f"User already deleted: {e}")


@pytest.fixture(scope="module")
def issue(project):
    """Issue fixture for issue API resource tests."""
    _id = uuid.uuid4().hex
    data = {"title": f"Issue {_id}", "description": f"Issue {_id} description"}

    return project.issues.create(data)


@pytest.fixture(scope="module")
def label(project):
    """Label fixture for project label API resource tests."""
    _id = uuid.uuid4().hex
    data = {
        "name": f"prjlabel{_id}",
        "description": f"prjlabel1 {_id} description",
        "color": "#112233",
    }

    return project.labels.create(data)


@pytest.fixture(scope="module")
def group_label(group):
    """Label fixture for group label API resource tests."""
    _id = uuid.uuid4().hex
    data = {
        "name": f"grplabel{_id}",
        "description": f"grplabel1 {_id} description",
        "color": "#112233",
    }

    return group.labels.create(data)


@pytest.fixture(scope="module")
def variable(project):
    """Variable fixture for project variable API resource tests."""
    _id = uuid.uuid4().hex
    data = {"key": f"var{_id}", "value": f"Variable {_id}"}

    return project.variables.create(data)


@pytest.fixture(scope="module")
def deploy_token(project):
    """Deploy token fixture for project deploy token API resource tests."""
    _id = uuid.uuid4().hex
    data = {
        "name": f"token-{_id}",
        "username": "root",
        "expires_at": "2021-09-09",
        "scopes": "read_registry",
    }

    return project.deploytokens.create(data)


@pytest.fixture(scope="module")
def group_deploy_token(group):
    """Deploy token fixture for group deploy token API resource tests."""
    _id = uuid.uuid4().hex
    data = {
        "name": f"group-token-{_id}",
        "username": "root",
        "expires_at": "2021-09-09",
        "scopes": "read_registry",
    }

    return group.deploytokens.create(data)

import os
import tempfile
from random import randint

import pytest

import gitlab


TEMP_DIR = tempfile.gettempdir()


def random_id():
    """
    Helper to ensure new resource creation does not clash with
    existing resources, for example when a previous test deleted a
    resource but GitLab is still deleting it asynchronously in the
    background. TODO: Expand to make it 100% safe.
    """
    return randint(9, 9999)


@pytest.fixture(scope="session")
def CONFIG():
    return os.path.join(TEMP_DIR, "python-gitlab.cfg")


@pytest.fixture(scope="session")
def gl(CONFIG):
    """Helper instance to make fixtures and asserts directly via the API."""
    return gitlab.Gitlab.from_config("local", [CONFIG])


@pytest.fixture(scope="module")
def group(gl):
    """Group fixture for group API resource tests."""
    _id = random_id()
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
    _id = random_id()
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
    _id = random_id()
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
    _id = random_id()
    data = {"title": f"Issue {_id}", "description": f"Issue {_id} description"}

    return project.issues.create(data)


@pytest.fixture(scope="module")
def label(project):
    """Label fixture for project label API resource tests."""
    _id = random_id()
    data = {
        "name": f"prjlabel{_id}",
        "description": f"prjlabel1 {_id} description",
        "color": "#112233",
    }

    return project.labels.create(data)


@pytest.fixture(scope="module")
def group_label(group):
    """Label fixture for group label API resource tests."""
    _id = random_id()
    data = {
        "name": f"grplabel{_id}",
        "description": f"grplabel1 {_id} description",
        "color": "#112233",
    }

    return group.labels.create(data)


@pytest.fixture(scope="module")
def variable(project):
    """Variable fixture for project variable API resource tests."""
    _id = random_id()
    data = {"key": f"var{_id}", "value": f"Variable {_id}"}

    return project.variables.create(data)


@pytest.fixture(scope="module")
def deploy_token(project):
    """Deploy token fixture for project deploy token API resource tests."""
    _id = random_id()
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
    _id = random_id()
    data = {
        "name": f"group-token-{_id}",
        "username": "root",
        "expires_at": "2021-09-09",
        "scopes": "read_registry",
    }

    return group.deploytokens.create(data)

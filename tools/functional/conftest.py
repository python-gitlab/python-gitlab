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


def pytest_report_collectionfinish(config, startdir, items):
    return [
        "",
        "Starting GitLab container.",
        "Waiting for GitLab to reconfigure.",
        "This may take a few minutes.",
    ]


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
def check_is_alive():
    """
    Return a healthcheck function fixture for the GitLab container spinup.
    """

    def _check(container):
        logs = ["docker", "logs", container]
        return "gitlab Reconfigured!" in check_output(logs).decode()

    return _check


@pytest.fixture
def wait_for_sidekiq(gl):
    """
    Return a helper function to wait until there are no busy sidekiq processes.

    Use this with asserts for slow tasks (group/project/user creation/deletion).
    """

    def _wait(timeout=30, step=0.5):
        for _ in range(timeout):
            if not gl.sidekiq.process_metrics()["processes"][0]["busy"]:
                return
            time.sleep(step)

    return _wait


@pytest.fixture(scope="session")
def gitlab_config(check_is_alive, docker_ip, docker_services, temp_dir, test_dir):
    config_file = temp_dir / "python-gitlab.cfg"
    port = docker_services.port_for("gitlab", 80)

    docker_services.wait_until_responsive(
        timeout=200, pause=5, check=lambda: check_is_alive("gitlab-test")
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
def milestone(project):
    _id = uuid.uuid4().hex
    data = {"title": f"milestone{_id}"}

    return project.milestones.create(data)


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


@pytest.fixture(scope="session")
def GPG_KEY():
    return """-----BEGIN PGP PUBLIC KEY BLOCK-----

mQENBFn5mzYBCADH6SDVPAp1zh/hxmTi0QplkOfExBACpuY6OhzNdIg+8/528b3g
Y5YFR6T/HLv/PmeHskUj21end1C0PNG2T9dTx+2Vlh9ISsSG1kyF9T5fvMR3bE0x
Dl6S489CXZrjPTS9SHk1kF+7dwjUxLJyxF9hPiSihFefDFu3NeOtG/u8vbC1mewQ
ZyAYue+mqtqcCIFFoBz7wHKMWjIVSJSyTkXExu4OzpVvy3l2EikbvavI3qNz84b+
Mgkv/kiBlNoCy3CVuPk99RYKZ3lX1vVtqQ0OgNGQvb4DjcpyjmbKyibuZwhDjIOh
au6d1OyEbayTntd+dQ4j9EMSnEvm/0MJ4eXPABEBAAG0G0dpdGxhYlRlc3QxIDxm
YWtlQGZha2UudGxkPokBNwQTAQgAIQUCWfmbNgIbAwULCQgHAgYVCAkKCwIEFgID
AQIeAQIXgAAKCRBgxELHf8f3hF3yB/wNJlWPKY65UsB4Lo0hs1OxdxCDqXogSi0u
6crDEIiyOte62pNZKzWy8TJcGZvznRTZ7t8hXgKFLz3PRMcl+vAiRC6quIDUj+2V
eYfwaItd1lUfzvdCaC7Venf4TQ74f5vvNg/zoGwE6eRoSbjlLv9nqsxeA0rUBUQL
LYikWhVMP3TrlfgfduYvh6mfgh57BDLJ9kJVpyfxxx9YLKZbaas9sPa6LgBtR555
JziUxHmbEv8XCsUU8uoFeP1pImbNBplqE3wzJwzOMSmmch7iZzrAwfN7N2j3Wj0H
B5kQddJ9dmB4BbU0IXGhWczvdpxboI2wdY8a1JypxOdePoph/43iuQENBFn5mzYB
CADnTPY0Zf3d9zLjBNgIb3yDl94uOcKCq0twNmyjMhHzGqw+UMe9BScy34GL94Al
xFRQoaL+7P8hGsnsNku29A/VDZivcI+uxTx4WQ7OLcn7V0bnHV4d76iky2ufbUt/
GofthjDs1SonePO2N09sS4V4uK0d5N4BfCzzXgvg8etCLxNmC9BGt7AaKUUzKBO4
2QvNNaC2C/8XEnOgNWYvR36ylAXAmo0sGFXUsBCTiq1fugS9pwtaS2JmaVpZZ3YT
pMZlS0+SjC5BZYFqSmKCsA58oBRzCxQz57nR4h5VEflgD+Hy0HdW0UHETwz83E6/
U0LL6YyvhwFr6KPq5GxinSvfABEBAAGJAR8EGAEIAAkFAln5mzYCGwwACgkQYMRC
x3/H94SJgwgAlKQb10/xcL/epdDkR7vbiei7huGLBpRDb/L5fM8B5W77Qi8Xmuqj
cCu1j99ZCA5hs/vwVn8j8iLSBGMC5gxcuaar/wtmiaEvT9fO/h6q4opG7NcuiJ8H
wRj8ccJmRssNqDD913PLz7T40Ts62blhrEAlJozGVG/q7T3RAZcskOUHKeHfc2RI
YzGsC/I9d7k6uxAv1L9Nm5F2HaAQDzhkdd16nKkGaPGR35cT1JLInkfl5cdm7ldN
nxs4TLO3kZjUTgWKdhpgRNF5hwaz51ZjpebaRf/ZqRuNyX4lIRolDxzOn/+O1o8L
qG2ZdhHHmSK2LaQLFiSprUkikStNU9BqSQ==
=5OGa
-----END PGP PUBLIC KEY BLOCK-----"""


@pytest.fixture(scope="session")
def SSH_KEY():
    return (
        "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDZAjAX8vTiHD7Yi3/EzuVaDChtih"
        "79HyJZ6H9dEqxFfmGA1YnncE0xujQ64TCebhkYJKzmTJCImSVkOu9C4hZgsw6eE76n"
        "+Cg3VwEeDUFy+GXlEJWlHaEyc3HWioxgOALbUp3rOezNh+d8BDwwqvENGoePEBsz5l"
        "a6WP5lTi/HJIjAl6Hu+zHgdj1XVExeH+S52EwpZf/ylTJub0Bl5gHwf/siVE48mLMI"
        "sqrukXTZ6Zg+8EHAIvIQwJ1dKcXe8P5IoLT7VKrbkgAnolS0I8J+uH7KtErZJb5oZh"
        "S4OEwsNpaXMAr+6/wWSpircV2/e7sFLlhlKBC4Iq1MpqlZ7G3p foo@bar"
    )


@pytest.fixture(scope="session")
def DEPLOY_KEY():
    return (
        "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDFdRyjJQh+1niBpXqE2I8dzjG"
        "MXFHlRjX9yk/UfOn075IdaockdU58sw2Ai1XIWFpZpfJkW7z+P47ZNSqm1gzeXI"
        "rtKa9ZUp8A7SZe8vH4XVn7kh7bwWCUirqtn8El9XdqfkzOs/+FuViriUWoJVpA6"
        "WZsDNaqINFKIA5fj/q8XQw+BcS92L09QJg9oVUuH0VVwNYbU2M2IRmSpybgC/gu"
        "uWTrnCDMmLItksATifLvRZwgdI8dr+q6tbxbZknNcgEPrI2jT0hYN9ZcjNeWuyv"
        "rke9IepE7SPBT41C+YtUX4dfDZDmczM1cE0YL/krdUCfuZHMa4ZS2YyNd6slufc"
        "vn bar@foo"
    )

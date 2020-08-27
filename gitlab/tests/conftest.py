import pytest
import gitlab


@pytest.fixture
def gl():
    return gitlab.Gitlab(
        "http://localhost",
        private_token="private_token",
        ssl_verify=True,
        api_version=4,
    )


# Todo: parametrize, but check what tests it's really useful for
@pytest.fixture
def gl_trailing():
    return gitlab.Gitlab(
        "http://localhost/", private_token="private_token", api_version=4
    )


@pytest.fixture
def default_config(tmpdir):
    valid_config = """[global]
    default = one
    ssl_verify = true
    timeout = 2

    [one]
    url = http://one.url
    private_token = ABCDEF
    """

    config_path = tmpdir.join("python-gitlab.cfg")
    config_path.write(valid_config)
    return str(config_path)


@pytest.fixture
def group(gl):
    return gl.groups.get(1, lazy=True)


@pytest.fixture
def project(gl):
    return gl.projects.get(1, lazy=True)


@pytest.fixture
def user(gl):
    return gl.users.get(1, lazy=True)

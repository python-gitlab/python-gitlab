import pytest
import responses

import gitlab
from tests.unit import helpers


@pytest.fixture
def fake_manager(gl):
    return helpers.FakeManager(gl)


@pytest.fixture
def fake_manager_with_parent(gl, fake_manager):
    return helpers.FakeManagerWithParent(
        gl, parent=helpers.FakeParent(manager=fake_manager, attrs={})
    )


@pytest.fixture
def fake_object(fake_manager):
    return helpers.FakeObject(fake_manager, {"attr1": "foo", "alist": [1, 2, 3]})


@pytest.fixture
def fake_object_no_id(fake_manager):
    return helpers.FakeObjectWithoutId(fake_manager, {})


@pytest.fixture
def fake_object_long_repr(fake_manager):
    return helpers.FakeObjectWithLongRepr(fake_manager, {"test": "a" * 100})


@pytest.fixture
def fake_object_with_parent(fake_manager_with_parent):
    return helpers.FakeObject(
        fake_manager_with_parent, {"attr1": "foo", "alist": [1, 2, 3]}
    )


@pytest.fixture
def gl():
    return gitlab.Gitlab(
        "http://localhost",
        private_token="private_token",
        ssl_verify=True,
        api_version="4",
    )


@pytest.fixture
def gl_retry():
    return gitlab.Gitlab(
        "http://localhost",
        private_token="private_token",
        ssl_verify=True,
        api_version="4",
        retry_transient_errors=True,
    )


@pytest.fixture
def resp_get_current_user():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/user",
            json={
                "id": 1,
                "username": "username",
                "web_url": "http://localhost/username",
            },
            content_type="application/json",
            status=200,
        )
        yield rsps


# Todo: parametrize, but check what tests it's really useful for
@pytest.fixture
def gl_trailing():
    return gitlab.Gitlab(
        "http://localhost/", private_token="private_token", api_version="4"
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
def tag_name():
    return "v1.0.0"


@pytest.fixture
def group(gl):
    return gl.groups.get(1, lazy=True)


@pytest.fixture
def project(gl):
    return gl.projects.get(1, lazy=True)


@pytest.fixture
def another_project(gl):
    return gl.projects.get(2, lazy=True)


@pytest.fixture
def project_issue(project):
    return project.issues.get(1, lazy=True)


@pytest.fixture
def project_merge_request(project):
    return project.mergerequests.get(1, lazy=True)


@pytest.fixture
def release(project, tag_name):
    return project.releases.get(tag_name, lazy=True)


@pytest.fixture
def schedule(project):
    return project.pipelineschedules.get(1, lazy=True)


@pytest.fixture
def user(gl):
    return gl.users.get(1, lazy=True)


@pytest.fixture
def current_user(gl, resp_get_current_user):
    gl.auth()
    return gl.user


@pytest.fixture
def migration(gl):
    return gl.bulk_imports.get(1, lazy=True)

import dataclasses
import datetime
import logging
import pathlib
import tempfile
import time
import uuid
from subprocess import check_output
from typing import Optional

import pytest
import requests

import gitlab
import gitlab.base
from tests.functional import helpers
from tests.functional.fixtures.docker import *  # noqa

SLEEP_TIME = 10


@dataclasses.dataclass
class GitlabVersion:
    major: int
    minor: int
    patch: str
    revision: str

    def __post_init__(self):
        self.major, self.minor = int(self.major), int(self.minor)


@pytest.fixture(scope="session")
def gitlab_version(gl) -> GitlabVersion:
    version, revision = gl.version()
    major, minor, patch = version.split(".")
    return GitlabVersion(major=major, minor=minor, patch=patch, revision=revision)


@pytest.fixture(scope="session")
def fixture_dir(test_dir: pathlib.Path) -> pathlib.Path:
    return test_dir / "functional" / "fixtures"


@pytest.fixture(scope="session")
def gitlab_service_name() -> str:
    """The "service" name is the one defined in the `docker-compose.yml` file"""
    return "gitlab"


@pytest.fixture(scope="session")
def gitlab_container_name() -> str:
    """The "container" name is the one defined in the `docker-compose.yml` file
    for the "gitlab" service"""
    return "gitlab-test"


@pytest.fixture(scope="session")
def gitlab_docker_port(docker_services, gitlab_service_name: str) -> int:
    port: int = docker_services.port_for(gitlab_service_name, container_port=80)
    return port


@pytest.fixture(scope="session")
def gitlab_url(docker_ip: str, gitlab_docker_port: int) -> str:
    return f"http://{docker_ip}:{gitlab_docker_port}"


def reset_gitlab(gl: gitlab.Gitlab) -> None:
    """Delete resources (such as projects, groups, users) that shouldn't
    exist."""
    if helpers.get_gitlab_plan(gl):
        logging.info("GitLab EE detected")
        # NOTE(jlvillal, timknight): By default in GitLab EE it will wait 7 days before
        # deleting a group or project.
        # In GL 16.0 we need to call delete with `permanently_remove=True` for projects and sub groups
        # (handled in helpers.py safe_delete)
        settings = gl.settings.get()
        modified_settings = False
        if settings.deletion_adjourned_period != 1:
            logging.info("Setting `deletion_adjourned_period` to 1 Day")
            settings.deletion_adjourned_period = 1
            modified_settings = True
        if modified_settings:
            settings.save()

    for project in gl.projects.list():
        for deploy_token in project.deploytokens.list():
            logging.info(
                f"Deleting deploy token: {deploy_token.username!r} in "
                f"project: {project.path_with_namespace!r}"
            )
            helpers.safe_delete(deploy_token)
        logging.info(f"Deleting project: {project.path_with_namespace!r}")
        helpers.safe_delete(project)

    for group in gl.groups.list():
        # skip deletion of a descendant group to prevent scenarios where parent group
        # gets deleted leaving a dangling descendant whose deletion will throw 404s.
        if group.parent_id:
            logging.info(
                f"Skipping deletion of {group.full_path} as it is a descendant "
                f"group and will be removed when the parent group is deleted"
            )
            continue

        for deploy_token in group.deploytokens.list():
            logging.info(
                f"Deleting deploy token: {deploy_token.username!r} in "
                f"group: {group.path_with_namespace!r}"
            )
            helpers.safe_delete(deploy_token)
        logging.info(f"Deleting group: {group.full_path!r}")
        helpers.safe_delete(group)
    for topic in gl.topics.list():
        logging.info(f"Deleting topic: {topic.name!r}")
        helpers.safe_delete(topic)
    for variable in gl.variables.list():
        logging.info(f"Deleting variable: {variable.key!r}")
        helpers.safe_delete(variable)
    for user in gl.users.list():
        if user.username not in ["root", "ghost"]:
            logging.info(f"Deleting user: {user.username!r}")
            helpers.safe_delete(user)


def set_token(container: str, fixture_dir: pathlib.Path) -> str:
    logging.info("Creating API token.")
    set_token_rb = fixture_dir / "set_token.rb"

    with open(set_token_rb, "r", encoding="utf-8") as f:
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
    logging.info("Finished creating API token.")

    return output


def pytest_report_collectionfinish(config, startdir, items):
    return [
        "",
        "Starting GitLab container.",
        "Waiting for GitLab to reconfigure.",
        "This will take a few minutes.",
    ]


def pytest_addoption(parser):
    parser.addoption(
        "--keep-containers",
        action="store_true",
        help="Keep containers running after testing",
    )


@pytest.fixture(scope="session")
def temp_dir() -> pathlib.Path:
    return pathlib.Path(tempfile.gettempdir())


@pytest.fixture(scope="session")
def check_is_alive():
    """
    Return a healthcheck function fixture for the GitLab container spinup.
    """

    def _check(
        *,
        container: str,
        start_time: float,
        gitlab_url: str,
    ) -> bool:
        setup_time = time.perf_counter() - start_time
        minutes, seconds = int(setup_time / 60), int(setup_time % 60)
        logging.info(
            f"Checking if GitLab container is up. "
            f"Have been checking for {minutes} minute(s), {seconds} seconds ..."
        )
        logs = ["docker", "logs", container]
        if "gitlab Reconfigured!" not in check_output(logs).decode():
            return False
        logging.debug("GitLab has finished reconfiguring.")
        for check in ("health", "readiness", "liveness"):
            url = f"{gitlab_url}/-/{check}"
            logging.debug(f"Checking {check!r} endpoint at: {url}")
            try:
                result = requests.get(url, timeout=1.0)
            except requests.exceptions.Timeout:
                logging.info(f"{check!r} check timed out")
                return False
            if result.status_code != 200:
                logging.info(f"{check!r} check did not return 200: {result!r}")
                return False
            logging.debug(f"{check!r} check passed: {result!r}")
        logging.debug(f"Sleeping for {SLEEP_TIME}")
        time.sleep(SLEEP_TIME)
        return True

    return _check


@pytest.fixture(scope="session")
def gitlab_token(
    check_is_alive,
    gitlab_container_name: str,
    gitlab_url: str,
    docker_services,
    fixture_dir: pathlib.Path,
) -> str:
    start_time = time.perf_counter()
    logging.info("Waiting for GitLab container to become ready.")
    docker_services.wait_until_responsive(
        timeout=300,
        pause=10,
        check=lambda: check_is_alive(
            container=gitlab_container_name,
            start_time=start_time,
            gitlab_url=gitlab_url,
        ),
    )
    setup_time = time.perf_counter() - start_time
    minutes, seconds = int(setup_time / 60), int(setup_time % 60)
    logging.info(
        f"GitLab container is now ready after {minutes} minute(s), {seconds} seconds"
    )

    return set_token(gitlab_container_name, fixture_dir=fixture_dir)


@pytest.fixture(scope="session")
def gitlab_config(gitlab_url: str, gitlab_token: str, temp_dir: pathlib.Path):
    config_file = temp_dir / "python-gitlab.cfg"

    config = f"""[global]
default = local
timeout = 60

[local]
url = {gitlab_url}
private_token = {gitlab_token}
api_version = 4"""

    with open(config_file, "w", encoding="utf-8") as f:
        f.write(config)

    return config_file


@pytest.fixture(scope="session")
def gl(gitlab_url: str, gitlab_token: str) -> gitlab.Gitlab:
    """Helper instance to make fixtures and asserts directly via the API."""

    logging.info("Instantiating python-gitlab gitlab.Gitlab instance")
    instance = gitlab.Gitlab(gitlab_url, private_token=gitlab_token)

    logging.info("Reset GitLab")
    reset_gitlab(instance)

    return instance


@pytest.fixture(scope="session")
def gitlab_plan(gl: gitlab.Gitlab) -> Optional[str]:
    return helpers.get_gitlab_plan(gl)


@pytest.fixture(autouse=True)
def gitlab_premium(gitlab_plan, request) -> None:
    if gitlab_plan in ("premium", "ultimate"):
        return

    if request.node.get_closest_marker("gitlab_ultimate"):
        pytest.skip("Test requires GitLab Premium plan")


@pytest.fixture(autouse=True)
def gitlab_ultimate(gitlab_plan, request) -> None:
    if gitlab_plan == "ultimate":
        return

    if request.node.get_closest_marker("gitlab_ultimate"):
        pytest.skip("Test requires GitLab Ultimate plan")


@pytest.fixture(scope="session")
def gitlab_runner(gl):
    container = "gitlab-runner-test"
    runner_name = "python-gitlab-runner"
    token = "registration-token"
    url = "http://gitlab"

    docker_exec = ["docker", "exec", container, "gitlab-runner"]
    register = [
        "register",
        "--run-untagged",
        "--non-interactive",
        "--registration-token",
        token,
        "--name",
        runner_name,
        "--url",
        url,
        "--clone-url",
        url,
        "--executor",
        "shell",
    ]
    unregister = ["unregister", "--name", runner_name]

    yield check_output(docker_exec + register).decode()

    check_output(docker_exec + unregister).decode()


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

    helpers.safe_delete(group)


@pytest.fixture(scope="module")
def project(gl):
    """Project fixture for project API resource tests."""
    _id = uuid.uuid4().hex
    name = f"test-project-{_id}"

    project = gl.projects.create(name=name)

    yield project

    helpers.safe_delete(project)


@pytest.fixture(scope="function")
def make_merge_request(project):
    """Fixture factory used to create a merge_request.

    It will create a branch, add a commit to the branch, and then create a
    merge request against project.default_branch. The MR will be returned.

    When finished any created merge requests and branches will be deleted.

    NOTE: No attempt is made to restore project.default_branch to its previous
    state. So if the merge request is merged then its content will be in the
    project.default_branch branch.
    """

    to_delete = []

    def _make_merge_request(*, source_branch: str, create_pipeline: bool = False):
        # Wait for processes to be done before we start...
        # NOTE(jlvillal): Sometimes the CI would give a "500 Internal Server
        # Error". Hoping that waiting until all other processes are done will
        # help with that.
        # Pause to let GL catch up (happens on hosted too, sometimes takes a while for server to be ready to merge)
        time.sleep(30)

        project.refresh()  # Gets us the current default branch
        logging.info(f"Creating branch {source_branch}")
        mr_branch = project.branches.create(
            {"branch": source_branch, "ref": project.default_branch}
        )
        # NOTE(jlvillal): Must create a commit in the new branch before we can
        # create an MR that will work.
        project.files.create(
            {
                "file_path": f"README.{source_branch}",
                "branch": source_branch,
                "content": "Initial content",
                "commit_message": "New commit in new branch",
            }
        )

        if create_pipeline:
            project.files.create(
                {
                    "file_path": ".gitlab-ci.yml",
                    "branch": source_branch,
                    "content": """
test:
  rules:
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
  script:
    - sleep 24h  # We don't expect this to finish
""",
                    "commit_message": "Add a simple pipeline",
                }
            )
        mr = project.mergerequests.create(
            {
                "source_branch": source_branch,
                "target_branch": project.default_branch,
                "title": "Should remove source branch",
                "remove_source_branch": True,
            }
        )

        # Pause to let GL catch up (happens on hosted too, sometimes takes a while for server to be ready to merge)
        time.sleep(5)

        mr_iid = mr.iid
        for _ in range(60):
            mr = project.mergerequests.get(mr_iid)
            if (
                mr.detailed_merge_status == "checking"
                or mr.detailed_merge_status == "unchecked"
            ):
                time.sleep(0.5)
            else:
                break

        assert mr.detailed_merge_status != "checking"
        assert mr.detailed_merge_status != "unchecked"

        to_delete.extend([mr, mr_branch])
        return mr

    yield _make_merge_request

    for object in to_delete:
        helpers.safe_delete(object)


@pytest.fixture(scope="function")
def merge_request(make_merge_request, project):
    _id = uuid.uuid4().hex
    return make_merge_request(source_branch=f"branch-{_id}")


@pytest.fixture(scope="function")
def merge_request_with_pipeline(make_merge_request, project):
    _id = uuid.uuid4().hex
    return make_merge_request(source_branch=f"branch-{_id}", create_pipeline=True)


@pytest.fixture(scope="module")
def project_file(project):
    """File fixture for tests requiring a project with files and branches."""
    project_file = project.files.create(
        {
            "file_path": "README",
            "branch": "main",
            "content": "Initial content",
            "commit_message": "Initial commit",
        }
    )

    return project_file


@pytest.fixture(scope="function")
def release(project, project_file):
    _id = uuid.uuid4().hex
    name = f"we_have_a_slash/test-release-{_id}"

    project.refresh()  # Gets us the current default branch
    release = project.releases.create(
        {
            "name": name,
            "tag_name": _id,
            "description": "description",
            "ref": project.default_branch,
        }
    )

    return release


@pytest.fixture(scope="function")
def service(project):
    """This is just a convenience fixture to make test cases slightly prettier. Project
    services are not idempotent. A service cannot be retrieved until it is enabled.
    After it is enabled the first time, it can never be fully deleted, only disabled."""
    service = project.services.update("asana", {"api_key": "api_key"})

    yield service

    try:
        project.services.delete("asana")
    except gitlab.exceptions.GitlabDeleteError as e:
        print(f"Service already disabled: {e}")


@pytest.fixture(scope="module")
def user(gl):
    """User fixture for user API resource tests."""
    _id = uuid.uuid4().hex
    email = f"user{_id}@email.com"
    username = f"user{_id}"
    name = f"User {_id}"
    password = "E4596f8be406Bc3a14a4ccdb1df80587"

    user = gl.users.create(email=email, username=username, name=name, password=password)

    yield user

    helpers.safe_delete(user)


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
def epic(group):
    """Fixture for group epic API resource tests."""
    _id = uuid.uuid4().hex
    return group.epics.create({"title": f"epic-{_id}", "description": f"Epic {_id}"})


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
        "expires_at": datetime.date.today().isoformat(),
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
        "expires_at": datetime.date.today().isoformat(),
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

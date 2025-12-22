import pathlib

import pytest

import gitlab
from gitlab.testing.fixtures.helpers import get_gitlab_plan


@pytest.fixture(scope="session")
def fixture_dir(test_dir: pathlib.Path) -> pathlib.Path:
    return test_dir / "functional" / "fixtures"


@pytest.fixture(scope="session")
def gitlab_plan(gl: gitlab.Gitlab) -> str | None:
    return get_gitlab_plan(gl)


@pytest.fixture(autouse=True)
def gitlab_premium(gitlab_plan, request) -> None:
    if gitlab_plan in ("premium", "ultimate"):
        return

    if request.node.get_closest_marker("gitlab_premium"):
        pytest.skip("Test requires GitLab Premium plan")


@pytest.fixture(autouse=True)
def gitlab_ultimate(gitlab_plan, request) -> None:
    if gitlab_plan == "ultimate":
        return

    if request.node.get_closest_marker("gitlab_ultimate"):
        pytest.skip("Test requires GitLab Ultimate plan")

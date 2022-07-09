import pytest
import responses

from gitlab import exceptions

ci_lint_create_content = {"status": "valid", "errors": [], "warnings": []}
ci_lint_create_invalid_content = {
    "status": "invalid",
    "errors": ["invalid format"],
    "warnings": [],
}


project_ci_lint_content = {
    "valid": True,
    "merged_yaml": "---\n:test_job:\n  :script: echo 1\n",
    "errors": [],
    "warnings": [],
}


@pytest.fixture
def resp_create_ci_lint():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.POST,
            url="http://localhost/api/v4/ci/lint",
            json=ci_lint_create_content,
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_create_ci_lint_invalid():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.POST,
            url="http://localhost/api/v4/ci/lint",
            json=ci_lint_create_invalid_content,
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_get_project_ci_lint():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/projects/1/ci/lint",
            json=project_ci_lint_content,
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_create_project_ci_lint():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.POST,
            url="http://localhost/api/v4/projects/1/ci/lint",
            json=project_ci_lint_content,
            content_type="application/json",
            status=200,
        )
        yield rsps


def test_ci_lint_create(gl, resp_create_ci_lint, valid_gitlab_ci_yml):
    lint_result = gl.ci_lint.create({"content": valid_gitlab_ci_yml})
    assert lint_result.status == "valid"


def test_ci_lint_validate(gl, resp_create_ci_lint, valid_gitlab_ci_yml):
    gl.ci_lint.validate({"content": valid_gitlab_ci_yml})


def test_ci_lint_validate_invalid_raises(
    gl, resp_create_ci_lint_invalid, invalid_gitlab_ci_yml
):
    with pytest.raises(exceptions.GitlabCiLintError, match="invalid format"):
        gl.ci_lint.validate({"content": invalid_gitlab_ci_yml})


def test_project_ci_lint_get(project, resp_get_project_ci_lint):
    lint_result = project.ci_lint.get()
    assert lint_result.valid is True


def test_project_ci_lint_create(
    project, resp_create_project_ci_lint, valid_gitlab_ci_yml
):
    lint_result = project.ci_lint.create({"content": valid_gitlab_ci_yml})
    assert lint_result.valid is True

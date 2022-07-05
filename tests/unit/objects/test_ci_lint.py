import pytest
import responses

ci_lint_get_content = {
    "valid": True,
    "merged_yaml": "---\n:test_job:\n  :script: echo 1\n",
    "errors": [],
    "warnings": [],
}


@pytest.fixture
def resp_get_ci_lint():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/projects/1/ci/lint",
            json=ci_lint_get_content,
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_create_ci_lint():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.POST,
            url="http://localhost/api/v4/projects/1/ci/lint",
            json=ci_lint_get_content,
            content_type="application/json",
            status=200,
        )
        yield rsps


def test_project_ci_lint_get(project, resp_get_ci_lint):
    lint_result = project.ci_lint.get()
    assert lint_result.valid is True


def test_project_ci_lint_create(project, resp_create_ci_lint):
    gitlab_ci_yml = """---
:test_job:
  :script: echo 1
"""
    lint_result = project.ci_lint.create({"content": gitlab_ci_yml})
    assert lint_result.valid is True

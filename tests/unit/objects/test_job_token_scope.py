"""
GitLab API: https://docs.gitlab.com/ee/api/project_job_token_scopes.html
"""

import pytest
import responses

from gitlab.v4.objects import ProjectJobTokenScope

job_token_scope_content = {
    "inbound_enabled": True,
    "outbound_enabled": False,
}


@pytest.fixture
def resp_get_job_token_scope():
    with responses.RequestsMock(assert_all_requests_are_fired=False) as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/projects/1/job_token_scope",
            json=job_token_scope_content,
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_patch_job_token_scope():
    with responses.RequestsMock(assert_all_requests_are_fired=False) as rsps:
        rsps.add(
            method=responses.PATCH,
            url="http://localhost/api/v4/projects/1/job_token_scope",
            status=204,
            match=[responses.matchers.json_params_matcher({"enabled": False})],
        )
        yield rsps


@pytest.fixture
def job_token_scope(project, resp_get_job_token_scope):
    return project.job_token_scope.get()


def test_get_job_token_scope(project, resp_get_job_token_scope):
    scope = project.job_token_scope.get()
    assert isinstance(scope, ProjectJobTokenScope)
    assert scope.inbound_enabled is True


def test_refresh_job_token_scope(job_token_scope, resp_get_job_token_scope):
    job_token_scope.refresh()
    assert job_token_scope.inbound_enabled is True


def test_save_job_token_scope(job_token_scope, resp_patch_job_token_scope):
    job_token_scope.enabled = False
    job_token_scope.save()


def test_update_job_token_scope(project, resp_patch_job_token_scope):
    project.job_token_scope.update(new_data={"enabled": False})

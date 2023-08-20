"""
GitLab API: https://docs.gitlab.com/ee/api/job_artifacts.html
"""

import pytest
import responses

ref_name = "main"
job = "build"


@pytest.fixture
def resp_artifacts_by_ref_name(binary_content):
    url = f"http://localhost/api/v4/projects/1/jobs/artifacts/{ref_name}/download?job={job}"

    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url=url,
            body=binary_content,
            content_type="application/octet-stream",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_project_artifacts_delete():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.DELETE,
            url="http://localhost/api/v4/projects/1/artifacts",
            status=204,
        )
        yield rsps


def test_project_artifacts_delete(gl, resp_project_artifacts_delete):
    project = gl.projects.get(1, lazy=True)
    project.artifacts.delete()


def test_project_artifacts_download_by_ref_name(
    gl, binary_content, resp_artifacts_by_ref_name
):
    project = gl.projects.get(1, lazy=True)
    artifacts = project.artifacts.download(ref_name=ref_name, job=job)
    assert artifacts == binary_content

"""
GitLab API: https://docs.gitlab.com/ee/api/jobs.html
"""

import pytest
import responses

from gitlab.v4.objects import ProjectJob

job_content = {
    "commit": {
        "author_email": "admin@example.com",
        "author_name": "Administrator",
    },
    "coverage": None,
    "allow_failure": False,
    "created_at": "2015-12-24T15:51:21.880Z",
    "started_at": "2015-12-24T17:54:30.733Z",
    "finished_at": "2015-12-24T17:54:31.198Z",
    "duration": 0.465,
    "queued_duration": 0.010,
    "artifacts_expire_at": "2016-01-23T17:54:31.198Z",
    "tag_list": ["docker runner", "macos-10.15"],
    "id": 1,
    "name": "rubocop",
    "pipeline": {
        "id": 1,
        "project_id": 1,
    },
    "ref": "main",
    "artifacts": [],
    "runner": None,
    "stage": "test",
    "status": "failed",
    "tag": False,
    "web_url": "https://example.com/foo/bar/-/jobs/1",
    "user": {"id": 1},
}


@pytest.fixture
def resp_get_job():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/projects/1/jobs/1",
            json=job_content,
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_cancel_job():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.POST,
            url="http://localhost/api/v4/projects/1/jobs/1/cancel",
            json=job_content,
            content_type="application/json",
            status=201,
        )
        yield rsps


@pytest.fixture
def resp_retry_job():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.POST,
            url="http://localhost/api/v4/projects/1/jobs/1/retry",
            json=job_content,
            content_type="application/json",
            status=201,
        )
        yield rsps


def test_get_project_job(project, resp_get_job):
    job = project.jobs.get(1)
    assert isinstance(job, ProjectJob)
    assert job.ref == "main"


def test_cancel_project_job(project, resp_cancel_job):
    job = project.jobs.get(1, lazy=True)

    output = job.cancel()
    assert output["ref"] == "main"


def test_retry_project_job(project, resp_retry_job):
    job = project.jobs.get(1, lazy=True)

    output = job.retry()
    assert output["ref"] == "main"

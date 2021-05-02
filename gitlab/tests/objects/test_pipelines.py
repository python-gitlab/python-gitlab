"""
GitLab API: https://docs.gitlab.com/ee/api/pipelines.html
"""
import pytest
import responses

from gitlab.v4.objects import ProjectPipeline


pipeline_content = {
    "id": 46,
    "project_id": 1,
    "status": "pending",
    "ref": "master",
    "sha": "a91957a858320c0e17f3a0eca7cfacbff50ea29a",
    "before_sha": "a91957a858320c0e17f3a0eca7cfacbff50ea29a",
    "tag": False,
    "yaml_errors": None,
    "user": {
        "name": "Administrator",
        "username": "root",
        "id": 1,
        "state": "active",
        "avatar_url": "http://www.gravatar.com/avatar/e64c7d89f26bd1972efa854d13d7dd61?s=80&d=identicon",
        "web_url": "http://localhost:3000/root",
    },
    "created_at": "2016-08-11T11:28:34.085Z",
    "updated_at": "2016-08-11T11:32:35.169Z",
    "started_at": None,
    "finished_at": "2016-08-11T11:32:35.145Z",
    "committed_at": None,
    "duration": None,
    "queued_duration": 0.010,
    "coverage": None,
    "web_url": "https://example.com/foo/bar/pipelines/46",
}


@pytest.fixture
def resp_get_pipeline():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/projects/1/pipelines/1",
            json=pipeline_content,
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_cancel_pipeline():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.POST,
            url="http://localhost/api/v4/projects/1/pipelines/1/cancel",
            json=pipeline_content,
            content_type="application/json",
            status=201,
        )
        yield rsps


@pytest.fixture
def resp_retry_pipeline():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.POST,
            url="http://localhost/api/v4/projects/1/pipelines/1/retry",
            json=pipeline_content,
            content_type="application/json",
            status=201,
        )
        yield rsps


def test_get_project_pipeline(project, resp_get_pipeline):
    pipeline = project.pipelines.get(1)
    assert isinstance(pipeline, ProjectPipeline)
    assert pipeline.ref == "master"


def test_cancel_project_pipeline(project, resp_cancel_pipeline):
    pipeline = project.pipelines.get(1, lazy=True)

    output = pipeline.cancel()
    assert output["ref"] == "master"


def test_retry_project_pipeline(project, resp_retry_pipeline):
    pipeline = project.pipelines.get(1, lazy=True)

    output = pipeline.retry()
    assert output["ref"] == "master"

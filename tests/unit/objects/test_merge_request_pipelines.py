"""
GitLab API: https://docs.gitlab.com/ee/api/merge_requests.html#list-mr-pipelines
"""

import pytest
import responses

from gitlab.v4.objects import ProjectMergeRequestPipeline

pipeline_content = {
    "id": 1,
    "sha": "959e04d7c7a30600c894bd3c0cd0e1ce7f42c11d",
    "ref": "main",
    "status": "success",
}


@pytest.fixture()
def resp_list_merge_request_pipelines():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/projects/1/merge_requests/1/pipelines",
            json=[pipeline_content],
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture()
def resp_create_merge_request_pipeline():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.POST,
            url="http://localhost/api/v4/projects/1/merge_requests/1/pipelines",
            json=pipeline_content,
            content_type="application/json",
            status=201,
        )
        yield rsps


def test_list_merge_requests_pipelines(project, resp_list_merge_request_pipelines):
    pipelines = project.mergerequests.get(1, lazy=True).pipelines.list()
    assert len(pipelines) == 1
    assert isinstance(pipelines[0], ProjectMergeRequestPipeline)
    assert pipelines[0].sha == pipeline_content["sha"]


def test_create_merge_requests_pipelines(project, resp_create_merge_request_pipeline):
    pipeline = project.mergerequests.get(1, lazy=True).pipelines.create()
    assert isinstance(pipeline, ProjectMergeRequestPipeline)
    assert pipeline.sha == pipeline_content["sha"]

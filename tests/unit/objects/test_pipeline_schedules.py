"""
GitLab API: https://docs.gitlab.com/ce/api/pipeline_schedules.html
"""

import pytest
import responses

from gitlab.v4.objects import ProjectPipelineSchedulePipeline

pipeline_content = {
    "id": 48,
    "iid": 13,
    "project_id": 29,
    "status": "pending",
    "source": "scheduled",
    "ref": "new-pipeline",
    "sha": "eb94b618fb5865b26e80fdd8ae531b7a63ad851a",
    "web_url": "https://example.com/foo/bar/pipelines/48",
    "created_at": "2016-08-12T10:06:04.561Z",
    "updated_at": "2016-08-12T10:09:56.223Z",
}


@pytest.fixture
def resp_create_pipeline_schedule():
    content = {
        "id": 14,
        "description": "Build packages",
        "ref": "main",
        "cron": "0 1 * * 5",
        "cron_timezone": "UTC",
        "next_run_at": "2017-05-26T01:00:00.000Z",
        "active": True,
        "created_at": "2017-05-19T13:43:08.169Z",
        "updated_at": "2017-05-19T13:43:08.169Z",
        "last_pipeline": None,
        "owner": {
            "name": "Administrator",
            "username": "root",
            "id": 1,
            "state": "active",
            "avatar_url": "http://www.gravatar.com/avatar/e64c7d89f26bd1972efa854d13d7dd61?s=80&d=identicon",
            "web_url": "https://gitlab.example.com/root",
        },
    }

    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.POST,
            url="http://localhost/api/v4/projects/1/pipeline_schedules",
            json=content,
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_play_pipeline_schedule(created_content):
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.POST,
            url="http://localhost/api/v4/projects/1/pipeline_schedules/1/play",
            json=created_content,
            content_type="application/json",
            status=201,
        )
        yield rsps


@pytest.fixture
def resp_list_schedule_pipelines():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/projects/1/pipeline_schedules/1/pipelines",
            json=[pipeline_content],
            content_type="application/json",
            status=200,
        )
        yield rsps


def test_create_project_pipeline_schedule(project, resp_create_pipeline_schedule):
    description = "Build packages"
    cronline = "0 1 * * 5"
    sched = project.pipelineschedules.create(
        {"ref": "main", "description": description, "cron": cronline}
    )
    assert sched is not None
    assert description == sched.description
    assert cronline == sched.cron


def test_play_project_pipeline_schedule(schedule, resp_play_pipeline_schedule):
    play_result = schedule.play()
    assert play_result is not None
    assert "message" in play_result
    assert play_result["message"] == "201 Created"


def test_list_project_pipeline_schedule_pipelines(
    schedule, resp_list_schedule_pipelines
):
    pipelines = schedule.pipelines.list()
    assert isinstance(pipelines, list)
    assert isinstance(pipelines[0], ProjectPipelineSchedulePipeline)
    assert pipelines[0].source == "scheduled"

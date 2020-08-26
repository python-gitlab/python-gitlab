"""
GitLab API: https://docs.gitlab.com/ce/api/pipeline_schedules.html
"""
import pytest
import responses


@pytest.fixture
def resp_project_pipeline_schedule(created_content):
    content = {
        "id": 14,
        "description": "Build packages",
        "ref": "master",
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
        rsps.add(
            method=responses.POST,
            url="http://localhost/api/v4/projects/1/pipeline_schedules/14/play",
            json=created_content,
            content_type="application/json",
            status=201,
        )
        yield rsps


def test_project_pipeline_schedule_play(project, resp_project_pipeline_schedule):
    description = "Build packages"
    cronline = "0 1 * * 5"
    sched = project.pipelineschedules.create(
        {"ref": "master", "description": description, "cron": cronline}
    )
    assert sched is not None
    assert description == sched.description
    assert cronline == sched.cron

    play_result = sched.play()
    assert play_result is not None
    assert "message" in play_result
    assert play_result["message"] == "201 Created"

"""
GitLab API: https://docs.gitlab.com/ce/api/pipeline_schedules.html
"""

from httmock import response, urlmatch, with_httmock

from .mocks import headers


@urlmatch(
    scheme="http",
    netloc="localhost",
    path="/api/v4/projects/1/pipeline_schedules$",
    method="post",
)
def resp_create_project_pipeline_schedule(url, request):
    """Mock for creating project pipeline Schedules POST response."""
    content = """{
    "id": 14,
    "description": "Build packages",
    "ref": "master",
    "cron": "0 1 * * 5",
    "cron_timezone": "UTC",
    "next_run_at": "2017-05-26T01:00:00.000Z",
    "active": true,
    "created_at": "2017-05-19T13:43:08.169Z",
    "updated_at": "2017-05-19T13:43:08.169Z",
    "last_pipeline": null,
    "owner": {
        "name": "Administrator",
        "username": "root",
        "id": 1,
        "state": "active",
        "avatar_url": "http://www.gravatar.com/avatar/e64c7d89f26bd1972efa854d13d7dd61?s=80&d=identicon",
        "web_url": "https://gitlab.example.com/root"
    }
}"""
    content = content.encode("utf-8")
    return response(200, content, headers, None, 5, request)


@urlmatch(
    scheme="http",
    netloc="localhost",
    path="/api/v4/projects/1/pipeline_schedules/14/play",
    method="post",
)
def resp_play_project_pipeline_schedule(url, request):
    """Mock for playing a project pipeline schedule POST response."""
    content = """{"message": "201 Created"}"""
    content = content.encode("utf-8")
    return response(200, content, headers, None, 5, request)


@with_httmock(
    resp_create_project_pipeline_schedule, resp_play_project_pipeline_schedule
)
def test_project_pipeline_schedule_play(project):
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

"""
GitLab API: https://docs.gitlab.com/ce/api/environments.html
"""

from httmock import response, urlmatch, with_httmock

from gitlab.v4.objects import ProjectEnvironment

from .mocks import headers


@urlmatch(
    scheme="http",
    netloc="localhost",
    path="/api/v4/projects/1/environments/1",
    method="get",
)
def resp_get_environment(url, request):
    content = '{"name": "environment_name", "id": 1, "last_deployment": "sometime"}'.encode(
        "utf-8"
    )
    return response(200, content, headers, None, 5, request)


@with_httmock(resp_get_environment)
def test_project_environments(project):
    environment = project.environments.get(1)
    assert isinstance(environment, ProjectEnvironment)
    assert environment.id == 1
    assert environment.last_deployment == "sometime"
    assert environment.name == "environment_name"

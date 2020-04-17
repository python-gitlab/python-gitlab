"""
GitLab API: https://docs.gitlab.com/ce/api/project_statistics.html
"""

from httmock import response, urlmatch, with_httmock

from gitlab.v4.objects import ProjectAdditionalStatistics

from .mocks import headers


@urlmatch(
    scheme="http",
    netloc="localhost",
    path="/api/v4/projects/1/statistics",
    method="get",
)
def resp_get_statistics(url, request):
    content = """{"fetches": {"total": 50, "days": [{"count": 10, "date": "2018-01-10"}]}}""".encode(
        "utf-8"
    )
    return response(200, content, headers, None, 5, request)


@with_httmock(resp_get_statistics)
def test_project_additional_statistics(project):
    statistics = project.additionalstatistics.get()
    assert isinstance(statistics, ProjectAdditionalStatistics)
    assert statistics.fetches["total"] == 50

"""
GitLab API: https://docs.gitlab.com/ce/api/project_statistics.html
"""

import pytest
import responses

from gitlab.v4.objects import ProjectAdditionalStatistics


@pytest.fixture
def resp_project_statistics():
    content = {"fetches": {"total": 50, "days": [{"count": 10, "date": "2018-01-10"}]}}

    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/projects/1/statistics",
            json=content,
            content_type="application/json",
            status=200,
        )
        yield rsps


def test_project_additional_statistics(project, resp_project_statistics):
    statistics = project.additionalstatistics.get()
    assert isinstance(statistics, ProjectAdditionalStatistics)
    assert statistics.fetches["total"] == 50

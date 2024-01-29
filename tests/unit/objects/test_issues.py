"""
GitLab API: https://docs.gitlab.com/ce/api/issues.html
"""

import re

import pytest
import responses

from gitlab.v4.objects import (
    GroupIssuesStatistics,
    IssuesStatistics,
    ProjectIssuesStatistics,
)


@pytest.fixture
def resp_list_issues():
    content = [{"name": "name", "id": 1}, {"name": "other_name", "id": 2}]

    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/issues",
            json=content,
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_get_issue():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/issues/1",
            json={"name": "name", "id": 1},
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_reorder_issue():
    match_params = {"move_after_id": 2, "move_before_id": 3}
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.PUT,
            url="http://localhost/api/v4/projects/1/issues/1/reorder",
            json={"name": "name", "id": 1},
            content_type="application/json",
            status=200,
            match=[responses.matchers.json_params_matcher(match_params)],
        )
        yield rsps


@pytest.fixture
def resp_issue_statistics():
    content = {"statistics": {"counts": {"all": 20, "closed": 5, "opened": 15}}}

    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url=re.compile(
                r"http://localhost/api/v4/((groups|projects)/1/)?issues_statistics"
            ),
            json=content,
            content_type="application/json",
            status=200,
        )
        yield rsps


def test_list_issues(gl, resp_list_issues):
    data = gl.issues.list()
    assert data[1].id == 2
    assert data[1].name == "other_name"


def test_get_issue(gl, resp_get_issue):
    issue = gl.issues.get(1)
    assert issue.id == 1
    assert issue.name == "name"


def test_reorder_issue(project, resp_reorder_issue):
    issue = project.issues.get(1, lazy=True)
    issue.reorder(move_after_id=2, move_before_id=3)


def test_get_issues_statistics(gl, resp_issue_statistics):
    statistics = gl.issues_statistics.get()
    assert isinstance(statistics, IssuesStatistics)
    assert statistics.statistics["counts"]["all"] == 20


def test_get_group_issues_statistics(group, resp_issue_statistics):
    statistics = group.issues_statistics.get()
    assert isinstance(statistics, GroupIssuesStatistics)
    assert statistics.statistics["counts"]["all"] == 20


def test_get_project_issues_statistics(project, resp_issue_statistics):
    statistics = project.issues_statistics.get()
    assert isinstance(statistics, ProjectIssuesStatistics)
    assert statistics.statistics["counts"]["all"] == 20

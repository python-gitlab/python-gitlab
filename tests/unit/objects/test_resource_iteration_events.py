"""
GitLab API: https://docs.gitlab.com/ee/api/resource_iteration_events.html
"""

import pytest
import responses

from gitlab.v4.objects import ProjectIssueResourceIterationEvent

issue_event_content = {"id": 1, "resource_type": "Issue"}


@pytest.fixture()
def resp_list_project_issue_iteration_events():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/projects/1/issues/1/resource_iteration_events",
            json=[issue_event_content],
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture()
def resp_get_project_issue_iteration_event():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/projects/1/issues/1/resource_iteration_events/1",
            json=issue_event_content,
            content_type="application/json",
            status=200,
        )
        yield rsps


def test_list_project_issue_iteration_events(
    project_issue, resp_list_project_issue_iteration_events
):
    iteration_events = project_issue.resource_iteration_events.list()
    assert isinstance(iteration_events, list)

    iteration_event = iteration_events[0]
    assert isinstance(iteration_event, ProjectIssueResourceIterationEvent)
    assert iteration_event.resource_type == "Issue"


def test_get_project_issue_iteration_event(
    project_issue, resp_get_project_issue_iteration_event
):
    iteration_event = project_issue.resource_iteration_events.get(1)
    assert isinstance(iteration_event, ProjectIssueResourceIterationEvent)
    assert iteration_event.resource_type == "Issue"

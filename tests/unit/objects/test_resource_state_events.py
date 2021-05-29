"""
GitLab API: https://docs.gitlab.com/ee/api/resource_state_events.html
"""

import pytest
import responses

from gitlab.v4.objects import (
    ProjectIssueResourceStateEvent,
    ProjectMergeRequestResourceStateEvent,
)

issue_event_content = {"id": 1, "resource_type": "Issue"}
mr_event_content = {"id": 1, "resource_type": "MergeRequest"}


@pytest.fixture()
def resp_list_project_issue_state_events():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/projects/1/issues/1/resource_state_events",
            json=[issue_event_content],
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture()
def resp_get_project_issue_state_event():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/projects/1/issues/1/resource_state_events/1",
            json=issue_event_content,
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture()
def resp_list_merge_request_state_events():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/projects/1/merge_requests/1/resource_state_events",
            json=[mr_event_content],
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture()
def resp_get_merge_request_state_event():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/projects/1/merge_requests/1/resource_state_events/1",
            json=mr_event_content,
            content_type="application/json",
            status=200,
        )
        yield rsps


def test_list_project_issue_state_events(
    project_issue, resp_list_project_issue_state_events
):
    state_events = project_issue.resourcestateevents.list()
    assert isinstance(state_events, list)

    state_event = state_events[0]
    assert isinstance(state_event, ProjectIssueResourceStateEvent)
    assert state_event.resource_type == "Issue"


def test_get_project_issue_state_event(
    project_issue, resp_get_project_issue_state_event
):
    state_event = project_issue.resourcestateevents.get(1)
    assert isinstance(state_event, ProjectIssueResourceStateEvent)
    assert state_event.resource_type == "Issue"


def test_list_merge_request_state_events(
    project_merge_request, resp_list_merge_request_state_events
):
    state_events = project_merge_request.resourcestateevents.list()
    assert isinstance(state_events, list)

    state_event = state_events[0]
    assert isinstance(state_event, ProjectMergeRequestResourceStateEvent)
    assert state_event.resource_type == "MergeRequest"


def test_get_merge_request_state_event(
    project_merge_request, resp_get_merge_request_state_event
):
    state_event = project_merge_request.resourcestateevents.get(1)
    assert isinstance(state_event, ProjectMergeRequestResourceStateEvent)
    assert state_event.resource_type == "MergeRequest"

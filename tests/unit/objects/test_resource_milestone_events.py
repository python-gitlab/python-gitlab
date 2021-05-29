"""
GitLab API: https://docs.gitlab.com/ee/api/resource_milestone_events.html
"""

import pytest
import responses

from gitlab.v4.objects import (
    ProjectIssueResourceMilestoneEvent,
    ProjectMergeRequestResourceMilestoneEvent,
)


@pytest.fixture()
def resp_merge_request_milestone_events():
    mr_content = {"iid": 1}
    events_content = {"id": 1, "resource_type": "MergeRequest"}
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/projects/1/merge_requests",
            json=[mr_content],
            content_type="application/json",
            status=200,
        )
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/projects/1/merge_requests/1/resource_milestone_events",
            json=[events_content],
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture()
def resp_project_issue_milestone_events():
    issue_content = {"iid": 1}
    events_content = {"id": 1, "resource_type": "Issue"}
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/projects/1/issues",
            json=[issue_content],
            content_type="application/json",
            status=200,
        )
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/projects/1/issues/1/resource_milestone_events",
            json=[events_content],
            content_type="application/json",
            status=200,
        )
        yield rsps


def test_project_issue_milestone_events(project, resp_project_issue_milestone_events):
    issue = project.issues.list()[0]
    milestone_events = issue.resourcemilestoneevents.list()
    assert isinstance(milestone_events, list)
    milestone_event = milestone_events[0]
    assert isinstance(milestone_event, ProjectIssueResourceMilestoneEvent)
    assert milestone_event.resource_type == "Issue"


def test_merge_request_milestone_events(project, resp_merge_request_milestone_events):
    mr = project.mergerequests.list()[0]
    milestone_events = mr.resourcemilestoneevents.list()
    assert isinstance(milestone_events, list)
    milestone_event = milestone_events[0]
    assert isinstance(milestone_event, ProjectMergeRequestResourceMilestoneEvent)
    assert milestone_event.resource_type == "MergeRequest"

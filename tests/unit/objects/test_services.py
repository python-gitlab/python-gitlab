"""
GitLab API: https://docs.gitlab.com/ce/api/integrations.html
"""

import pytest
import responses

from gitlab.v4.objects import ProjectIntegration, ProjectService


@pytest.fixture
def resp_integration():
    content = {
        "id": 100152,
        "title": "Pipelines emails",
        "slug": "pipelines-email",
        "created_at": "2019-01-14T08:46:43.637+01:00",
        "updated_at": "2019-07-01T14:10:36.156+02:00",
        "active": True,
        "commit_events": True,
        "push_events": True,
        "issues_events": True,
        "confidential_issues_events": True,
        "merge_requests_events": True,
        "tag_push_events": True,
        "note_events": True,
        "confidential_note_events": True,
        "pipeline_events": True,
        "wiki_page_events": True,
        "job_events": True,
        "comment_on_event_enabled": True,
        "project_id": 1,
    }

    with responses.RequestsMock(assert_all_requests_are_fired=False) as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/projects/1/integrations",
            json=[content],
            content_type="application/json",
            status=200,
        )
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/projects/1/integrations",
            json=content,
            content_type="application/json",
            status=200,
        )
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/projects/1/integrations/pipelines-email",
            json=content,
            content_type="application/json",
            status=200,
        )
        updated_content = dict(content)
        updated_content["issues_events"] = False
        rsps.add(
            method=responses.PUT,
            url="http://localhost/api/v4/projects/1/integrations/pipelines-email",
            json=updated_content,
            content_type="application/json",
            status=200,
        )
        yield rsps


def test_list_active_integrations(project, resp_integration):
    integrations = project.integrations.list()
    assert isinstance(integrations, list)
    assert isinstance(integrations[0], ProjectIntegration)
    assert integrations[0].active
    assert integrations[0].push_events


def test_list_available_integrations(project, resp_integration):
    integrations = project.integrations.available()
    assert isinstance(integrations, list)
    assert isinstance(integrations[0], str)


def test_get_integration(project, resp_integration):
    integration = project.integrations.get("pipelines-email")
    assert isinstance(integration, ProjectIntegration)
    assert integration.push_events is True


def test_update_integration(project, resp_integration):
    integration = project.integrations.get("pipelines-email")
    integration.issues_events = False
    integration.save()
    assert integration.issues_events is False


def test_get_service_returns_service(project, resp_integration):
    # todo: remove when services are removed
    service = project.services.get("pipelines-email")
    assert isinstance(service, ProjectService)

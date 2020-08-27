"""
GitLab API: https://docs.gitlab.com/ce/api/services.html
"""

import pytest
import responses

from gitlab.v4.objects import ProjectService


@pytest.fixture
def resp_service():
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
            url="http://localhost/api/v4/projects/1/services",
            json=[content],
            content_type="application/json",
            status=200,
        )
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/projects/1/services",
            json=content,
            content_type="application/json",
            status=200,
        )
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/projects/1/services/pipelines-email",
            json=content,
            content_type="application/json",
            status=200,
        )
        updated_content = dict(content)
        updated_content["issues_events"] = False
        rsps.add(
            method=responses.PUT,
            url="http://localhost/api/v4/projects/1/services/pipelines-email",
            json=updated_content,
            content_type="application/json",
            status=200,
        )
        yield rsps


def test_list_active_services(project, resp_service):
    services = project.services.list()
    assert isinstance(services, list)
    assert isinstance(services[0], ProjectService)
    assert services[0].active
    assert services[0].push_events


def test_list_available_services(project, resp_service):
    services = project.services.available()
    assert isinstance(services, list)
    assert isinstance(services[0], str)


def test_get_service(project, resp_service):
    service = project.services.get("pipelines-email")
    assert isinstance(service, ProjectService)
    assert service.push_events is True


def test_update_service(project, resp_service):
    service = project.services.get("pipelines-email")
    service.issues_events = False
    service.save()
    assert service.issues_events is False

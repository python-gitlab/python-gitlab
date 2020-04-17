"""
GitLab API: https://docs.gitlab.com/ce/api/services.html
"""

from httmock import urlmatch, response, with_httmock

from gitlab.v4.objects import ProjectService
from .mocks import headers


@urlmatch(
    scheme="http",
    netloc="localhost",
    path="/api/v4/projects/1/services/pipelines-email",
    method="put",
)
def resp_update_service(url, request):
    """Mock for Service update PUT response."""
    content = """{
        "id": 100152,
        "title": "Pipelines emails",
        "slug": "pipelines-email",
        "created_at": "2019-01-14T08:46:43.637+01:00",
        "updated_at": "2019-07-01T14:10:36.156+02:00",
        "active": true,
        "commit_events": true,
        "push_events": true,
        "issues_events": true,
        "confidential_issues_events": true,
        "merge_requests_events": true,
        "tag_push_events": true,
        "note_events": true,
        "confidential_note_events": true,
        "pipeline_events": true,
        "wiki_page_events": true,
        "job_events": true,
        "comment_on_event_enabled": true,
        "project_id": 1
    }"""
    content = content.encode("utf-8")
    return response(200, content, headers, None, 5, request)


@urlmatch(
    scheme="http",
    netloc="localhost",
    path="/api/v4/projects/1/services/pipelines-email",
    method="get",
)
def resp_get_service(url, request):
    """Mock for Service GET response."""
    content = """{
        "id": 100152,
        "title": "Pipelines emails",
        "slug": "pipelines-email",
        "created_at": "2019-01-14T08:46:43.637+01:00",
        "updated_at": "2019-07-01T14:10:36.156+02:00",
        "active": true,
        "commit_events": true,
        "push_events": true,
        "issues_events": true,
        "confidential_issues_events": true,
        "merge_requests_events": true,
        "tag_push_events": true,
        "note_events": true,
        "confidential_note_events": true,
        "pipeline_events": true,
        "wiki_page_events": true,
        "job_events": true,
        "comment_on_event_enabled": true,
        "project_id": 1
    }"""
    content = content.encode("utf-8")
    return response(200, content, headers, None, 5, request)


@urlmatch(
    scheme="http", netloc="localhost", path="/api/v4/projects/1/services", method="get",
)
def resp_get_active_services(url, request):
    """Mock for active Services GET response."""
    content = """[{
        "id": 100152,
        "title": "Pipelines emails",
        "slug": "pipelines-email",
        "created_at": "2019-01-14T08:46:43.637+01:00",
        "updated_at": "2019-07-01T14:10:36.156+02:00",
        "active": true,
        "commit_events": true,
        "push_events": true,
        "issues_events": true,
        "confidential_issues_events": true,
        "merge_requests_events": true,
        "tag_push_events": true,
        "note_events": true,
        "confidential_note_events": true,
        "pipeline_events": true,
        "wiki_page_events": true,
        "job_events": true,
        "comment_on_event_enabled": true,
        "project_id": 1
    }]"""
    content = content.encode("utf-8")
    return response(200, content, headers, None, 5, request)


@with_httmock(resp_get_active_services)
def test_list_active_services(project):
    services = project.services.list()
    assert isinstance(services, list)
    assert isinstance(services[0], ProjectService)
    assert services[0].active
    assert services[0].push_events


def test_list_available_services(project):
    services = project.services.available()
    assert isinstance(services, list)
    assert isinstance(services[0], str)


@with_httmock(resp_get_service)
def test_get_service(project):
    service = project.services.get("pipelines-email")
    assert isinstance(service, ProjectService)
    assert service.push_events is True


@with_httmock(resp_get_service, resp_update_service)
def test_update_service(project):
    service = project.services.get("pipelines-email")
    service.issues_events = True
    service.save()
    assert service.issues_events is True

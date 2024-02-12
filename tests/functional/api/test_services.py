"""
GitLab API:
https://docs.gitlab.com/ee/api/integrations.html
"""

import gitlab


def test_get_service_lazy(project):
    service = project.services.get("jira", lazy=True)
    assert isinstance(service, gitlab.v4.objects.ProjectService)


def test_update_service(project):
    service_dict = project.services.update(
        "emails-on-push", {"recipients": "email@example.com"}
    )
    assert service_dict["active"]


def test_list_services(project, service):
    services = project.services.list()
    assert isinstance(services[0], gitlab.v4.objects.ProjectService)
    assert services[0].active


def test_get_service(project, service):
    service_object = project.services.get(service["slug"])
    assert isinstance(service_object, gitlab.v4.objects.ProjectService)
    assert service_object.active


def test_delete_service(project, service):
    service_object = project.services.get(service["slug"])

    service_object.delete()

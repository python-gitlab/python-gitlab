"""
GitLab API:
https://docs.gitlab.com/ee/api/resource_groups.html
"""

import pytest
import responses

from gitlab.v4.objects import ProjectResourceGroup, ProjectResourceGroupUpcomingJob

from .test_jobs import failed_job_content

resource_group_content = {
    "id": 3,
    "key": "production",
    "process_mode": "unordered",
    "created_at": "2021-09-01T08:04:59.650Z",
    "updated_at": "2021-09-01T08:04:59.650Z",
}


@pytest.fixture
def resp_list_resource_groups():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/projects/1/resource_groups",
            json=[resource_group_content],
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_get_resource_group():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/projects/1/resource_groups/production",
            json=resource_group_content,
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_list_upcoming_jobs():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/projects/1/resource_groups/production/upcoming_jobs",
            json=[failed_job_content],
            content_type="application/json",
            status=200,
        )
        yield rsps


def test_list_project_resource_groups(project, resp_list_resource_groups):
    resource_groups = project.resource_groups.list()
    assert isinstance(resource_groups, list)
    assert isinstance(resource_groups[0], ProjectResourceGroup)
    assert resource_groups[0].process_mode == "unordered"


def test_get_project_resource_group(project, resp_get_resource_group):
    resource_group = project.resource_groups.get("production")
    assert isinstance(resource_group, ProjectResourceGroup)
    assert resource_group.process_mode == "unordered"


def test_list_resource_group_upcoming_jobs(project, resp_list_upcoming_jobs):
    resource_group = project.resource_groups.get("production", lazy=True)
    upcoming_jobs = resource_group.upcoming_jobs.list()

    assert isinstance(upcoming_jobs, list)
    assert isinstance(upcoming_jobs[0], ProjectResourceGroupUpcomingJob)
    assert upcoming_jobs[0].ref == "main"

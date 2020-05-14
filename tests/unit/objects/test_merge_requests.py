"""
GitLab API:
https://docs.gitlab.com/ce/api/merge_requests.html
https://docs.gitlab.com/ee/api/deployments.html#list-of-merge-requests-associated-with-a-deployment
"""
import re

import pytest
import responses

from gitlab.v4.objects import ProjectDeploymentMergeRequest, ProjectMergeRequest

mr_content = {
    "id": 1,
    "iid": 1,
    "project_id": 3,
    "title": "test1",
    "description": "fixed login page css paddings",
    "state": "merged",
    "merged_by": {
        "id": 87854,
        "name": "Douwe Maan",
        "username": "DouweM",
        "state": "active",
        "avatar_url": "https://gitlab.example.com/uploads/-/system/user/avatar/87854/avatar.png",
        "web_url": "https://gitlab.com/DouweM",
    },
}


@pytest.fixture
def resp_list_merge_requests():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url=re.compile(
                r"http://localhost/api/v4/projects/1/(deployments/1/)?merge_requests"
            ),
            json=[mr_content],
            content_type="application/json",
            status=200,
        )
        yield rsps


def test_list_project_merge_requests(project, resp_list_merge_requests):
    mrs = project.mergerequests.list()
    assert isinstance(mrs[0], ProjectMergeRequest)
    assert mrs[0].iid == mr_content["iid"]


def test_list_deployment_merge_requests(project, resp_list_merge_requests):
    deployment = project.deployments.get(1, lazy=True)
    mrs = deployment.mergerequests.list()
    assert isinstance(mrs[0], ProjectDeploymentMergeRequest)
    assert mrs[0].iid == mr_content["iid"]

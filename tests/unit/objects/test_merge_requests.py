"""
GitLab API:
https://docs.gitlab.com/ce/api/merge_requests.html
https://docs.gitlab.com/ee/api/deployments.html#list-of-merge-requests-associated-with-a-deployment
"""

import re

import pytest
import responses

from gitlab.v4.objects import (
    ProjectDeploymentMergeRequest,
    ProjectMergeRequest,
    ProjectMergeRequestReviewerDetail,
)

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
    "reviewers": [
        {
            "id": 2,
            "name": "Sam Bauch",
            "username": "kenyatta_oconnell",
            "state": "active",
            "avatar_url": "https://www.gravatar.com/avatar/956c92487c6f6f7616b536927e22c9a0?s=80&d=identicon",
            "web_url": "http://gitlab.example.com//kenyatta_oconnell",
        }
    ],
    "related_issues": [1, 2],
}

reviewers_content = [
    {
        "user": {
            "id": 2,
            "name": "Sam Bauch",
            "username": "kenyatta_oconnell",
            "state": "active",
            "avatar_url": "https://www.gravatar.com/avatar/956c92487c6f6f7616b536927e22c9a0?s=80&d=identicon",
            "web_url": "http://gitlab.example.com//kenyatta_oconnell",
        },
        "state": "unreviewed",
        "created_at": "2022-07-27T17:03:27.684Z",
    }
]


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


@pytest.fixture
def resp_get_merge_request_reviewers():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/projects/1/merge_requests/1",
            json=mr_content,
            content_type="application/json",
            status=200,
        )
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/projects/3/merge_requests/1/reviewers",
            json=reviewers_content,
            content_type="application/json",
            status=200,
        )
        yield rsps


def test_list_related_issues(project, resp_list_merge_requests):
    mrs = project.mergerequests.list()
    assert isinstance(mrs[0], ProjectMergeRequest)
    assert mrs[0].related_issues == mr_content["related_issues"]


def test_list_project_merge_requests(project, resp_list_merge_requests):
    mrs = project.mergerequests.list()
    assert isinstance(mrs[0], ProjectMergeRequest)
    assert mrs[0].iid == mr_content["iid"]


def test_list_deployment_merge_requests(project, resp_list_merge_requests):
    deployment = project.deployments.get(1, lazy=True)
    mrs = deployment.mergerequests.list()
    assert isinstance(mrs[0], ProjectDeploymentMergeRequest)
    assert mrs[0].iid == mr_content["iid"]


def test_get_merge_request_reviewers(project, resp_get_merge_request_reviewers):
    mr = project.mergerequests.get(1)
    reviewers_details = mr.reviewer_details.list()
    assert isinstance(mr, ProjectMergeRequest)
    assert isinstance(reviewers_details, list)
    assert isinstance(reviewers_details[0], ProjectMergeRequestReviewerDetail)
    assert mr.reviewers[0]["name"] == reviewers_details[0].user["name"]
    assert reviewers_details[0].state == "unreviewed"
    assert reviewers_details[0].created_at == "2022-07-27T17:03:27.684Z"

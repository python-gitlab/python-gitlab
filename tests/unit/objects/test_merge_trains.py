"""
GitLab API:
https://docs.gitlab.com/ee/api/merge_trains.html
"""

import pytest
import responses

from gitlab.v4.objects import ProjectMergeTrain, ProjectMergeTrainMergeRequest

mr_content = {
    "id": 110,
    "merge_request": {
        "id": 1,
        "iid": 1,
        "project_id": 3,
        "title": "Test merge train",
        "description": "",
        "state": "merged",
        "created_at": "2020-02-06T08:39:14.883Z",
        "updated_at": "2020-02-06T08:40:57.038Z",
        "web_url": "http://gitlab.example.com/root/merge-train-race-condition/-/merge_requests/1",
    },
    "user": {
        "id": 1,
        "name": "Administrator",
        "username": "root",
        "state": "active",
        "avatar_url": "https://www.gravatar.com/avatar/e64c7d89f26bd1972efa854d13d7dd61?s=80&d=identicon",
        "web_url": "http://gitlab.example.com/root",
    },
    "pipeline": {
        "id": 246,
        "sha": "bcc17a8ffd51be1afe45605e714085df28b80b13",
        "ref": "refs/merge-requests/1/train",
        "status": "success",
        "created_at": "2020-02-06T08:40:42.410Z",
        "updated_at": "2020-02-06T08:40:46.912Z",
        "web_url": "http://gitlab.example.com/root/merge-train-race-condition/pipelines/246",
    },
    "created_at": "2020-02-06T08:39:47.217Z",
    "updated_at": "2020-02-06T08:40:57.720Z",
    "target_branch": "feature-1580973432",
    "status": "merged",
    "merged_at": "2020-02-06T08:40:57.719Z",
    "duration": 70,
}


@pytest.fixture
def resp_list_merge_trains():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/projects/1/merge_trains",
            json=[mr_content],
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_merge_trains_merge_request_get():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/projects/1/merge_trains/merge_requests/123",
            json=mr_content,
            content_type="application/json",
            status=200,
        )
        yield rsps


def test_list_project_merge_requests(project, resp_list_merge_trains):
    merge_trains = project.merge_trains.list()
    assert isinstance(merge_trains[0], ProjectMergeTrain)
    assert merge_trains[0].id == mr_content["id"]


def test_merge_trains_status_merge_request(
    project, resp_merge_trains_merge_request_get
):
    # flow will be : project -> merge_trains : -> get merge_requests -> merge_request_iod
    merge_train_mr: ProjectMergeTrainMergeRequest = project.merge_trains.get(
        1, lazy=True
    ).merge_requests.get(123)
    assert isinstance(merge_train_mr, ProjectMergeTrainMergeRequest)
    assert merge_train_mr.get_id() == 110

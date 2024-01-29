"""
GitLab API: https://docs.gitlab.com/ce/api/deployments.html
"""

import pytest
import responses


@pytest.fixture
def resp_deployment_get():
    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/projects/1/deployments/42",
            json=response_get_content,
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def deployment(project):
    return project.deployments.get(42, lazy=True)


@pytest.fixture
def resp_deployment_create():
    content = {"id": 42, "status": "success", "ref": "main"}

    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.POST,
            url="http://localhost/api/v4/projects/1/deployments",
            json=content,
            content_type="application/json",
            status=200,
        )

        updated_content = dict(content)
        updated_content["status"] = "failed"

        rsps.add(
            method=responses.PUT,
            url="http://localhost/api/v4/projects/1/deployments/42",
            json=updated_content,
            content_type="application/json",
            status=200,
        )
        yield rsps


@pytest.fixture
def resp_deployment_approval():
    content = {
        "user": {
            "id": 100,
            "username": "security-user-1",
            "name": "security user-1",
            "state": "active",
            "avatar_url": "https://www.gravatar.com/avatar/e130fcd3a1681f41a3de69d10841afa9?s=80&d=identicon",
            "web_url": "http://localhost:3000/security-user-1",
        },
        "status": "approved",
        "created_at": "2022-02-24T20:22:30.097Z",
        "comment": "Looks good to me",
    }

    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.POST,
            url="http://localhost/api/v4/projects/1/deployments/42/approval",
            json=content,
            content_type="application/json",
            status=200,
        )
        yield rsps


def test_deployment_get(project, resp_deployment_get):
    deployment = project.deployments.get(42)
    assert deployment.id == 42
    assert deployment.iid == 2
    assert deployment.status == "success"
    assert deployment.ref == "main"


def test_deployment_create(project, resp_deployment_create):
    deployment = project.deployments.create(
        {
            "environment": "Test",
            "sha": "1agf4gs",
            "ref": "main",
            "tag": False,
            "status": "created",
        }
    )
    assert deployment.id == 42
    assert deployment.status == "success"
    assert deployment.ref == "main"

    deployment.status = "failed"
    deployment.save()
    assert deployment.status == "failed"


def test_deployment_approval(deployment, resp_deployment_approval) -> None:
    result = deployment.approval(status="approved")
    assert result["status"] == "approved"
    assert result["comment"] == "Looks good to me"


response_get_content = {
    "id": 42,
    "iid": 2,
    "ref": "main",
    "sha": "a91957a858320c0e17f3a0eca7cfacbff50ea29a",
    "created_at": "2016-08-11T11:32:35.444Z",
    "updated_at": "2016-08-11T11:34:01.123Z",
    "status": "success",
    "user": {
        "name": "Administrator",
        "username": "root",
        "id": 1,
        "state": "active",
        "avatar_url": "http://www.gravatar.com/avatar/e64c7d89f26bd1972efa854d13d7dd61?s=80&d=identicon",
        "web_url": "http://localhost:3000/root",
    },
    "environment": {
        "id": 9,
        "name": "production",
        "external_url": "https://about.gitlab.com",
    },
    "deployable": {
        "id": 664,
        "status": "success",
        "stage": "deploy",
        "name": "deploy",
        "ref": "main",
        "tag": False,
        "coverage": None,
        "created_at": "2016-08-11T11:32:24.456Z",
        "started_at": None,
        "finished_at": "2016-08-11T11:32:35.145Z",
        "user": {
            "id": 1,
            "name": "Administrator",
            "username": "root",
            "state": "active",
            "avatar_url": "http://www.gravatar.com/avatar/e64c7d89f26bd1972efa854d13d7dd61?s=80&d=identicon",
            "web_url": "http://gitlab.dev/root",
            "created_at": "2015-12-21T13:14:24.077Z",
            "bio": None,
            "location": None,
            "skype": "",
            "linkedin": "",
            "twitter": "",
            "website_url": "",
            "organization": "",
        },
        "commit": {
            "id": "a91957a858320c0e17f3a0eca7cfacbff50ea29a",
            "short_id": "a91957a8",
            "title": "Merge branch 'rename-readme' into 'main'\r",
            "author_name": "Administrator",
            "author_email": "admin@example.com",
            "created_at": "2016-08-11T13:28:26.000+02:00",
            "message": "Merge branch 'rename-readme' into 'main'\r\n\r\nRename README\r\n\r\n\r\n\r\nSee merge request !2",
        },
        "pipeline": {
            "created_at": "2016-08-11T07:43:52.143Z",
            "id": 42,
            "ref": "main",
            "sha": "a91957a858320c0e17f3a0eca7cfacbff50ea29a",
            "status": "success",
            "updated_at": "2016-08-11T07:43:52.143Z",
            "web_url": "http://gitlab.dev/root/project/pipelines/5",
        },
        "runner": None,
    },
}

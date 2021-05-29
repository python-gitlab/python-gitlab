"""
GitLab API: https://docs.gitlab.com/ce/api/deployments.html
"""
import pytest
import responses


@pytest.fixture
def resp_deployment():
    content = {"id": 42, "status": "success", "ref": "master"}

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


def test_deployment(project, resp_deployment):
    deployment = project.deployments.create(
        {
            "environment": "Test",
            "sha": "1agf4gs",
            "ref": "master",
            "tag": False,
            "status": "created",
        }
    )
    assert deployment.id == 42
    assert deployment.status == "success"
    assert deployment.ref == "master"

    deployment.status = "failed"
    deployment.save()
    assert deployment.status == "failed"

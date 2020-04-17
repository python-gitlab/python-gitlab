"""
GitLab API: https://docs.gitlab.com/ce/api/deployments.html
"""

import json

from httmock import response, urlmatch, with_httmock

from .mocks import headers

content = '{"id": 42, "status": "success", "ref": "master"}'
json_content = json.loads(content)


@urlmatch(
    scheme="http",
    netloc="localhost",
    path="/api/v4/projects/1/deployments",
    method="post",
)
def resp_deployment_create(url, request):
    return response(200, json_content, headers, None, 5, request)


@urlmatch(
    scheme="http",
    netloc="localhost",
    path="/api/v4/projects/1/deployments/42",
    method="put",
)
def resp_deployment_update(url, request):
    return response(200, json_content, headers, None, 5, request)


@with_httmock(resp_deployment_create, resp_deployment_update)
def test_deployment(project):
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

    json_content["status"] = "failed"
    deployment.status = "failed"
    deployment.save()
    assert deployment.status == "failed"

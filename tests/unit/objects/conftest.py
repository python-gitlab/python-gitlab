"""Common mocks for resources in gitlab.v4.objects"""

import re

import pytest
import responses


@pytest.fixture
def binary_content():
    return b"binary content"


@pytest.fixture
def accepted_content():
    return {"message": "202 Accepted"}


@pytest.fixture
def created_content():
    return {"message": "201 Created"}


@pytest.fixture
def token_content():
    return {
        "user_id": 141,
        "scopes": ["api"],
        "name": "token",
        "expires_at": "2021-01-31",
        "id": 42,
        "active": True,
        "created_at": "2021-01-20T22:11:48.151Z",
        "revoked": False,
        "token": "s3cr3t",
    }


@pytest.fixture
def resp_export(accepted_content, binary_content):
    """Common fixture for group and project exports."""
    export_status_content = {
        "id": 1,
        "description": "Itaque perspiciatis minima aspernatur",
        "name": "Gitlab Test",
        "name_with_namespace": "Gitlab Org / Gitlab Test",
        "path": "gitlab-test",
        "path_with_namespace": "gitlab-org/gitlab-test",
        "created_at": "2017-08-29T04:36:44.383Z",
        "export_status": "finished",
        "_links": {
            "api_url": "https://gitlab.test/api/v4/projects/1/export/download",
            "web_url": "https://gitlab.test/gitlab-test/download_export",
        },
    }

    with responses.RequestsMock(assert_all_requests_are_fired=False) as rsps:
        rsps.add(
            method=responses.POST,
            url=re.compile(r".*/api/v4/(groups|projects)/1/export"),
            json=accepted_content,
            content_type="application/json",
            status=202,
        )
        rsps.add(
            method=responses.GET,
            url=re.compile(r".*/api/v4/(groups|projects)/1/export/download"),
            body=binary_content,
            content_type="application/octet-stream",
            status=200,
        )
        # Currently only project export supports status checks
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/projects/1/export",
            json=export_status_content,
            content_type="application/json",
            status=200,
        )
        yield rsps

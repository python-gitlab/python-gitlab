"""
GitLab API: https://docs.gitlab.com/ce/api/applications.html
"""

import pytest
import responses

title = "GitLab Test Instance"
description = "gitlab-test.example.com"
new_title = "new-title"
new_description = "new-description"


@pytest.fixture
def resp_application_create():
    content = {
        "name": "test_app",
        "redirect_uri": "http://localhost:8080",
        "scopes": ["api", "email"],
    }

    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.POST,
            url="http://localhost/api/v4/applications",
            json=content,
            content_type="application/json",
            status=200,
        )
        yield rsps


def test_create_application(gl, resp_application_create):
    application = gl.applications.create(
        {
            "name": "test_app",
            "redirect_uri": "http://localhost:8080",
            "scopes": ["api", "email"],
            "confidential": False,
        }
    )
    assert application.name == "test_app"
    assert application.redirect_uri == "http://localhost:8080"
    assert application.scopes == ["api", "email"]

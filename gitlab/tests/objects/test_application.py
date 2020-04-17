"""
GitLab API: https://docs.gitlab.com/ce/api/applications.html
"""

import json

from httmock import urlmatch, response, with_httmock  # noqa

from .mocks import headers


title = "GitLab Test Instance"
description = "gitlab-test.example.com"
new_title = "new-title"
new_description = "new-description"


@urlmatch(
    scheme="http", netloc="localhost", path="/api/v4/applications", method="post",
)
def resp_application_create(url, request):
    content = '{"name": "test_app", "redirect_uri": "http://localhost:8080", "scopes": ["api", "email"]}'
    json_content = json.loads(content)
    return response(200, json_content, headers, None, 5, request)


@urlmatch(
    scheme="http",
    netloc="localhost",
    path="/api/v4/application/appearance",
    method="get",
)
def resp_get_appearance(url, request):
    content = """{
    "title": "%s",
    "description": "%s",
    "logo": "/uploads/-/system/appearance/logo/1/logo.png",
    "header_logo": "/uploads/-/system/appearance/header_logo/1/header.png",
    "favicon": "/uploads/-/system/appearance/favicon/1/favicon.png",
    "new_project_guidelines": "Please read the FAQs for help.",
    "header_message": "",
    "footer_message": "",
    "message_background_color": "#e75e40",
    "message_font_color": "#ffffff",
    "email_header_and_footer_enabled": false}""" % (
        title,
        description,
    )
    content = content.encode("utf-8")
    return response(200, content, headers, None, 25, request)


@urlmatch(
    scheme="http",
    netloc="localhost",
    path="/api/v4/application/appearance",
    method="put",
)
def resp_update_appearance(url, request):
    content = """{
    "title": "%s",
    "description": "%s",
    "logo": "/uploads/-/system/appearance/logo/1/logo.png",
    "header_logo": "/uploads/-/system/appearance/header_logo/1/header.png",
    "favicon": "/uploads/-/system/appearance/favicon/1/favicon.png",
    "new_project_guidelines": "Please read the FAQs for help.",
    "header_message": "",
    "footer_message": "",
    "message_background_color": "#e75e40",
    "message_font_color": "#ffffff",
    "email_header_and_footer_enabled": false}""" % (
        new_title,
        new_description,
    )
    content = content.encode("utf-8")
    return response(200, content, headers, None, 25, request)


@with_httmock(resp_application_create)
def test_create_application(gl):
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


@with_httmock(resp_get_appearance, resp_update_appearance)
def test_get_update_appearance(gl):
    appearance = gl.appearance.get()
    assert appearance.title == title
    assert appearance.description == description
    appearance.title = new_title
    appearance.description = new_description
    appearance.save()
    assert appearance.title == new_title
    assert appearance.description == new_description


@with_httmock(resp_update_appearance)
def test_update_application_appearance(gl):
    resp = gl.appearance.update(title=new_title, description=new_description)

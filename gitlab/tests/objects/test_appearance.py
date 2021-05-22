"""
GitLab API: https://docs.gitlab.com/ce/api/appearance.html
"""

import pytest
import responses

title = "GitLab Test Instance"
description = "gitlab-test.example.com"
new_title = "new-title"
new_description = "new-description"


@pytest.fixture
def resp_application_appearance():
    content = {
        "title": title,
        "description": description,
        "logo": "/uploads/-/system/appearance/logo/1/logo.png",
        "header_logo": "/uploads/-/system/appearance/header_logo/1/header.png",
        "favicon": "/uploads/-/system/appearance/favicon/1/favicon.png",
        "new_project_guidelines": "Please read the FAQs for help.",
        "header_message": "",
        "footer_message": "",
        "message_background_color": "#e75e40",
        "message_font_color": "#ffffff",
        "email_header_and_footer_enabled": False,
    }

    with responses.RequestsMock(assert_all_requests_are_fired=False) as rsps:
        rsps.add(
            method=responses.GET,
            url="http://localhost/api/v4/application/appearance",
            json=content,
            content_type="application/json",
            status=200,
        )

        updated_content = dict(content)
        updated_content["title"] = new_title
        updated_content["description"] = new_description

        rsps.add(
            method=responses.PUT,
            url="http://localhost/api/v4/application/appearance",
            json=updated_content,
            content_type="application/json",
            status=200,
        )
        yield rsps


def test_get_update_appearance(gl, resp_application_appearance):
    appearance = gl.appearance.get()
    assert appearance.title == title
    assert appearance.description == description
    appearance.title = new_title
    appearance.description = new_description
    appearance.save()
    assert appearance.title == new_title
    assert appearance.description == new_description


def test_update_appearance(gl, resp_application_appearance):
    gl.appearance.update(title=new_title, description=new_description)

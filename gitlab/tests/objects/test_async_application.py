import re

import pytest
import respx
from httpx.status_codes import StatusCode

from gitlab import AsyncGitlab


class TestApplicationAppearance:
    @pytest.fixture
    def gl(self):
        return AsyncGitlab(
            "http://localhost",
            private_token="private_token",
            ssl_verify=True,
            api_version="4",
        )

    @respx.mock
    @pytest.mark.asyncio
    async def test_get_update_appearance(self, gl):
        title = "GitLab Test Instance"
        new_title = "new-title"
        description = "gitlab-test.example.com"
        new_description = "new-description"

        request_get_appearance = respx.get(
            "http://localhost/api/v4/application/appearance",
            content={
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
            },
            status_code=StatusCode.OK,
        )
        request_update_appearance = respx.put(
            "http://localhost/api/v4/application/appearance",
            content={
                "title": new_title,
                "description": new_description,
                "logo": "/uploads/-/system/appearance/logo/1/logo.png",
                "header_logo": "/uploads/-/system/appearance/header_logo/1/header.png",
                "favicon": "/uploads/-/system/appearance/favicon/1/favicon.png",
                "new_project_guidelines": "Please read the FAQs for help.",
                "header_message": "",
                "footer_message": "",
                "message_background_color": "#e75e40",
                "message_font_color": "#ffffff",
                "email_header_and_footer_enabled": False,
            },
            status_code=StatusCode.OK,
        )

        appearance = await gl.appearance.get()
        assert appearance.title == title
        assert appearance.description == description
        appearance.title = new_title
        appearance.description = new_description
        await appearance.save()
        assert appearance.title == new_title
        assert appearance.description == new_description

    @respx.mock
    @pytest.mark.asyncio
    async def test_update_appearance(self, gl):
        new_title = "new-title"
        new_description = "new-description"

        request = respx.put(
            re.compile("^http://localhost/api/v4/application/appearance"),
            content={
                "title": new_title,
                "description": new_description,
                "logo": "/uploads/-/system/appearance/logo/1/logo.png",
                "header_logo": "/uploads/-/system/appearance/header_logo/1/header.png",
                "favicon": "/uploads/-/system/appearance/favicon/1/favicon.png",
                "new_project_guidelines": "Please read the FAQs for help.",
                "header_message": "",
                "footer_message": "",
                "message_background_color": "#e75e40",
                "message_font_color": "#ffffff",
                "email_header_and_footer_enabled": False,
            },
            status_code=StatusCode.OK,
        )

        await gl.appearance.update(title=new_title, description=new_description)

import re

import pytest
import respx
from gitlab import AsyncGitlab
from httpx import codes


class TestApplicationAppearance:
    @respx.mock
    @pytest.mark.asyncio
    async def test_get_update_appearance(self, gl, gl_get_value, is_gl_sync):
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
            status_code=codes.OK,
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
            status_code=codes.OK,
        )

        appearance = gl.appearance.get()
        appearance = await gl_get_value(appearance)

        assert appearance.title == title
        assert appearance.description == description
        appearance.title = new_title
        appearance.description = new_description
        if is_gl_sync:
            appearance.save()
        else:
            await appearance.save()
        assert appearance.title == new_title
        assert appearance.description == new_description

    @respx.mock
    @pytest.mark.asyncio
    async def test_update_appearance(self, gl, is_gl_sync):
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
            status_code=codes.OK,
        )

        if is_gl_sync:
            gl.appearance.update(title=new_title, description=new_description)
        else:
            await gl.appearance.update(title=new_title, description=new_description)

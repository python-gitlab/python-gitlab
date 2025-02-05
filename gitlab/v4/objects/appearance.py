from __future__ import annotations

from typing import Any

from gitlab import exceptions as exc
from gitlab.base import RESTObject
from gitlab.mixins import GetWithoutIdMixin, SaveMixin, UpdateMixin
from gitlab.types import RequiredOptional

__all__ = ["ApplicationAppearance", "ApplicationAppearanceManager"]


class ApplicationAppearance(SaveMixin, RESTObject):
    _id_attr = None


class ApplicationAppearanceManager(
    GetWithoutIdMixin[ApplicationAppearance], UpdateMixin[ApplicationAppearance]
):
    _path = "/application/appearance"
    _obj_cls = ApplicationAppearance
    _update_attrs = RequiredOptional(
        optional=(
            "title",
            "description",
            "logo",
            "header_logo",
            "favicon",
            "new_project_guidelines",
            "header_message",
            "footer_message",
            "message_background_color",
            "message_font_color",
            "email_header_and_footer_enabled",
        )
    )

    @exc.on_http_error(exc.GitlabUpdateError)
    def update(
        self,
        id: str | int | None = None,
        new_data: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Update an object on the server.

        Args:
            id: ID of the object to update (can be None if not required)
            new_data: the update data for the object
            **kwargs: Extra options to send to the server (e.g. sudo)

        Returns:
            The new object data (*not* a RESTObject)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabUpdateError: If the server cannot perform the request
        """
        new_data = new_data or {}
        data = new_data.copy()
        return super().update(id, data, **kwargs)

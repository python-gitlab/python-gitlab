from gitlab import exceptions as exc
from gitlab.base import RequiredOptional, RESTManager, RESTObject
from gitlab.mixins import GetWithoutIdMixin, SaveMixin, UpdateMixin


__all__ = [
    "ApplicationAppearance",
    "ApplicationAppearanceManager",
]


class ApplicationAppearance(SaveMixin, RESTObject):
    _id_attr = None


class ApplicationAppearanceManager(GetWithoutIdMixin, UpdateMixin, RESTManager):
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
        ),
    )

    @exc.on_http_error(exc.GitlabUpdateError)
    def update(self, id=None, new_data=None, **kwargs):
        """Update an object on the server.

        Args:
            id: ID of the object to update (can be None if not required)
            new_data: the update data for the object
            **kwargs: Extra options to send to the server (e.g. sudo)

        Returns:
            dict: The new object data (*not* a RESTObject)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabUpdateError: If the server cannot perform the request
        """
        new_data = new_data or {}
        data = new_data.copy()
        super(ApplicationAppearanceManager, self).update(id, data, **kwargs)

from gitlab import cli
from gitlab import exceptions as exc
from gitlab.base import RequiredOptional, RESTManager, RESTObject
from gitlab.mixins import NoUpdateMixin, ObjectDeleteMixin

__all__ = [
    "ProjectTag",
    "ProjectTagManager",
    "ProjectProtectedTag",
    "ProjectProtectedTagManager",
]


class ProjectTag(ObjectDeleteMixin, RESTObject):
    _id_attr = "name"
    _short_print_attr = "name"

    @cli.register_custom_action("ProjectTag", ("description",))
    def set_release_description(self, description, **kwargs):
        """Set the release notes on the tag.

        If the release doesn't exist yet, it will be created. If it already
        exists, its description will be updated.

        Args:
            description (str): Description of the release.
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabCreateError: If the server fails to create the release
            GitlabUpdateError: If the server fails to update the release
        """
        id = self.get_id().replace("/", "%2F")
        path = "%s/%s/release" % (self.manager.path, id)
        data = {"description": description}
        if self.release is None:
            try:
                server_data = self.manager.gitlab.http_post(
                    path, post_data=data, **kwargs
                )
            except exc.GitlabHttpError as e:
                raise exc.GitlabCreateError(e.response_code, e.error_message) from e
        else:
            try:
                server_data = self.manager.gitlab.http_put(
                    path, post_data=data, **kwargs
                )
            except exc.GitlabHttpError as e:
                raise exc.GitlabUpdateError(e.response_code, e.error_message) from e
        self.release = server_data


class ProjectTagManager(NoUpdateMixin, RESTManager):
    _path = "/projects/%(project_id)s/repository/tags"
    _obj_cls = ProjectTag
    _from_parent_attrs = {"project_id": "id"}
    _create_attrs = RequiredOptional(
        required=("tag_name", "ref"), optional=("message",)
    )


class ProjectProtectedTag(ObjectDeleteMixin, RESTObject):
    _id_attr = "name"
    _short_print_attr = "name"


class ProjectProtectedTagManager(NoUpdateMixin, RESTManager):
    _path = "/projects/%(project_id)s/protected_tags"
    _obj_cls = ProjectProtectedTag
    _from_parent_attrs = {"project_id": "id"}
    _create_attrs = RequiredOptional(
        required=("name",), optional=("create_access_level",)
    )

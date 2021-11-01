from gitlab import cli
from gitlab import exceptions as exc
from gitlab.base import RequiredOptional, RESTManager, RESTObject
from gitlab.mixins import (
    CreateMixin,
    DeleteMixin,
    ObjectDeleteMixin,
    RetrieveMixin,
    SaveMixin,
    UpdateMixin,
)

__all__ = [
    "ProjectEnvironment",
    "ProjectEnvironmentManager",
]


class ProjectEnvironment(SaveMixin, ObjectDeleteMixin, RESTObject):
    @cli.register_custom_action("ProjectEnvironment")
    @exc.on_http_error(exc.GitlabStopError)
    def stop(self, **kwargs):
        """Stop the environment.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabStopError: If the operation failed
        """
        path = f"{self.manager.path}/{self.get_id()}/stop"
        self.manager.gitlab.http_post(path, **kwargs)


class ProjectEnvironmentManager(
    RetrieveMixin, CreateMixin, UpdateMixin, DeleteMixin, RESTManager
):
    _path = "/projects/%(project_id)s/environments"
    _obj_cls = ProjectEnvironment
    _from_parent_attrs = {"project_id": "id"}
    _create_attrs = RequiredOptional(required=("name",), optional=("external_url",))
    _update_attrs = RequiredOptional(optional=("name", "external_url"))

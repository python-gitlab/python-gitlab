from gitlab import cli
from gitlab import exceptions as exc
from gitlab.base import RESTManager, RESTObject
from gitlab.mixins import CRUDMixin, ObjectDeleteMixin, SaveMixin


__all__ = [
    "ProjectTrigger",
    "ProjectTriggerManager",
]


class ProjectTrigger(SaveMixin, ObjectDeleteMixin, RESTObject):
    @cli.register_custom_action("ProjectTrigger")
    @exc.on_http_error(exc.GitlabOwnershipError)
    def take_ownership(self, **kwargs):
        """Update the owner of a trigger.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabOwnershipError: If the request failed
        """
        path = "%s/%s/take_ownership" % (self.manager.path, self.get_id())
        server_data = self.manager.gitlab.http_post(path, **kwargs)
        self._update_attrs(server_data)


class ProjectTriggerManager(CRUDMixin, RESTManager):
    _path = "/projects/%(project_id)s/triggers"
    _obj_cls = ProjectTrigger
    _from_parent_attrs = {"project_id": "id"}
    _create_attrs = (("description",), tuple())
    _update_attrs = (("description",), tuple())

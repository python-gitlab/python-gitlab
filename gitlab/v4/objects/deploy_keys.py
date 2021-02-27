from gitlab import cli
from gitlab import exceptions as exc
from gitlab.base import RESTObject
from gitlab.mixins import CRUDMixin, ListMixin, ObjectDeleteMixin, SaveMixin


__all__ = [
    "DeployKey",
    "DeployKeyManager",
    "ProjectKey",
    "ProjectKeyManager",
]


class DeployKey(RESTObject):
    pass


class DeployKeyManager(ListMixin):
    _path = "/deploy_keys"
    _obj_cls = DeployKey


class ProjectKey(SaveMixin, ObjectDeleteMixin):
    pass


class ProjectKeyManager(CRUDMixin):
    _path = "/projects/%(project_id)s/deploy_keys"
    _obj_cls = ProjectKey
    _from_parent_attrs = {"project_id": "id"}
    _create_attrs = (("title", "key"), ("can_push",))
    _update_attrs = (tuple(), ("title", "can_push"))

    @cli.register_custom_action("ProjectKeyManager", ("key_id",))
    @exc.on_http_error(exc.GitlabProjectDeployKeyError)
    def enable(self, key_id, **kwargs):
        """Enable a deploy key for a project.

        Args:
            key_id (int): The ID of the key to enable
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabProjectDeployKeyError: If the key could not be enabled
        """
        path = "%s/%s/enable" % (self.path, key_id)
        self.gitlab.http_post(path, **kwargs)

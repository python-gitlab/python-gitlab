from gitlab import exceptions as exc
from gitlab.base import *  # noqa
from gitlab.mixins import *  # noqa


__all__ = [
    "GroupCluster",
    "GroupClusterManager",
    "ProjectCluster",
    "ProjectClusterManager",
]


class GroupCluster(SaveMixin, ObjectDeleteMixin, RESTObject):
    pass


class GroupClusterManager(CRUDMixin, RESTManager):
    _path = "/groups/%(group_id)s/clusters"
    _obj_cls = GroupCluster
    _from_parent_attrs = {"group_id": "id"}
    _create_attrs = (
        ("name", "platform_kubernetes_attributes"),
        ("domain", "enabled", "managed", "environment_scope"),
    )
    _update_attrs = (
        tuple(),
        (
            "name",
            "domain",
            "management_project_id",
            "platform_kubernetes_attributes",
            "environment_scope",
        ),
    )

    @exc.on_http_error(exc.GitlabStopError)
    def create(self, data, **kwargs):
        """Create a new object.

        Args:
            data (dict): Parameters to send to the server to create the
                         resource
            **kwargs: Extra options to send to the server (e.g. sudo or
                      'ref_name', 'stage', 'name', 'all')

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabCreateError: If the server cannot perform the request

        Returns:
            RESTObject: A new instance of the manage object class build with
                        the data sent by the server
        """
        path = "%s/user" % (self.path)
        return CreateMixin.create(self, data, path=path, **kwargs)


class ProjectCluster(SaveMixin, ObjectDeleteMixin, RESTObject):
    pass


class ProjectClusterManager(CRUDMixin, RESTManager):
    _path = "/projects/%(project_id)s/clusters"
    _obj_cls = ProjectCluster
    _from_parent_attrs = {"project_id": "id"}
    _create_attrs = (
        ("name", "platform_kubernetes_attributes"),
        ("domain", "enabled", "managed", "environment_scope"),
    )
    _update_attrs = (
        tuple(),
        (
            "name",
            "domain",
            "management_project_id",
            "platform_kubernetes_attributes",
            "environment_scope",
        ),
    )

    @exc.on_http_error(exc.GitlabStopError)
    def create(self, data, **kwargs):
        """Create a new object.

        Args:
            data (dict): Parameters to send to the server to create the
                         resource
            **kwargs: Extra options to send to the server (e.g. sudo or
                      'ref_name', 'stage', 'name', 'all')

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabCreateError: If the server cannot perform the request

        Returns:
            RESTObject: A new instance of the manage object class build with
                        the data sent by the server
        """
        path = "%s/user" % (self.path)
        return CreateMixin.create(self, data, path=path, **kwargs)

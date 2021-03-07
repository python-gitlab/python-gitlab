from gitlab import cli
from gitlab import exceptions as exc
from gitlab.base import RequiredOptional, RESTManager, RESTObject
from gitlab.mixins import (
    DeleteMixin,
    ObjectDeleteMixin,
    RetrieveMixin,
    SaveMixin,
    UpdateMixin,
)


__all__ = [
    "GeoNode",
    "GeoNodeManager",
]


class GeoNode(SaveMixin, ObjectDeleteMixin, RESTObject):
    @cli.register_custom_action("GeoNode")
    @exc.on_http_error(exc.GitlabRepairError)
    def repair(self, **kwargs):
        """Repair the OAuth authentication of the geo node.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabRepairError: If the server failed to perform the request
        """
        path = "/geo_nodes/%s/repair" % self.get_id()
        server_data = self.manager.gitlab.http_post(path, **kwargs)
        self._update_attrs(server_data)

    @cli.register_custom_action("GeoNode")
    @exc.on_http_error(exc.GitlabGetError)
    def status(self, **kwargs):
        """Get the status of the geo node.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabGetError: If the server failed to perform the request

        Returns:
            dict: The status of the geo node
        """
        path = "/geo_nodes/%s/status" % self.get_id()
        return self.manager.gitlab.http_get(path, **kwargs)


class GeoNodeManager(RetrieveMixin, UpdateMixin, DeleteMixin, RESTManager):
    _path = "/geo_nodes"
    _obj_cls = GeoNode
    _update_attrs = RequiredOptional(
        optional=("enabled", "url", "files_max_capacity", "repos_max_capacity"),
    )

    @cli.register_custom_action("GeoNodeManager")
    @exc.on_http_error(exc.GitlabGetError)
    def status(self, **kwargs):
        """Get the status of all the geo nodes.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabGetError: If the server failed to perform the request

        Returns:
            list: The status of all the geo nodes
        """
        return self.gitlab.http_list("/geo_nodes/status", **kwargs)

    @cli.register_custom_action("GeoNodeManager")
    @exc.on_http_error(exc.GitlabGetError)
    def current_failures(self, **kwargs):
        """Get the list of failures on the current geo node.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabGetError: If the server failed to perform the request

        Returns:
            list: The list of failures
        """
        return self.gitlab.http_list("/geo_nodes/current/failures", **kwargs)

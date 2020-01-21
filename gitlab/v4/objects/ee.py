from gitlab.base import *  # noqa
from gitlab.exceptions import *  # noqa
from gitlab.mixins import *  # noqa
from gitlab import types
from gitlab import utils


class AuditEvent(RESTObject):
    _id_attr = "id"


class AuditEventManager(ListMixin, RESTManager):
    _path = "/audit_events"
    _obj_cls = AuditEvent
    _list_filters = ("created_after", "created_before", "entity_type", "entity_id")


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
    _update_attrs = (
        tuple(),
        ("enabled", "url", "files_max_capacity", "repos_max_capacity"),
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


class LDAPGroup(RESTObject):
    _id_attr = None


class LDAPGroupManager(RESTManager):
    _path = "/ldap/groups"
    _obj_cls = LDAPGroup
    _list_filters = ("search", "provider")

    @exc.on_http_error(exc.GitlabListError)
    def list(self, **kwargs):
        """Retrieve a list of objects.

        Args:
            all (bool): If True, return all the items, without pagination
            per_page (int): Number of items to retrieve per request
            page (int): ID of the page to return (starts with page 1)
            as_list (bool): If set to False and no pagination option is
                defined, return a generator instead of a list
            **kwargs: Extra options to send to the server (e.g. sudo)

        Returns:
            list: The list of objects, or a generator if `as_list` is False

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabListError: If the server cannot perform the request
        """
        data = kwargs.copy()
        if self.gitlab.per_page:
            data.setdefault("per_page", self.gitlab.per_page)

        if "provider" in data:
            path = "/ldap/%s/groups" % data["provider"]
        else:
            path = self._path

        obj = self.gitlab.http_list(path, **data)
        if isinstance(obj, list):
            return [self._obj_cls(self, item) for item in obj]
        else:
            return base.RESTObjectList(self, self._obj_cls, obj)

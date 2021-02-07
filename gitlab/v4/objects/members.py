from gitlab import cli
from gitlab import exceptions as exc
from gitlab.base import *  # noqa
from gitlab.mixins import *  # noqa


__all__ = [
    "GroupMember",
    "GroupMemberManager",
    "ProjectMember",
    "ProjectMemberManager",
]


class GroupMember(SaveMixin, ObjectDeleteMixin, RESTObject):
    _short_print_attr = "username"


class GroupMemberManager(CRUDMixin, RESTManager):
    _path = "/groups/%(group_id)s/members"
    _obj_cls = GroupMember
    _from_parent_attrs = {"group_id": "id"}
    _create_attrs = (("access_level", "user_id"), ("expires_at",))
    _update_attrs = (("access_level",), ("expires_at",))

    @cli.register_custom_action("GroupMemberManager")
    @exc.on_http_error(exc.GitlabListError)
    def all(self, **kwargs):
        """List all the members, included inherited ones.

        Args:
            all (bool): If True, return all the items, without pagination
            per_page (int): Number of items to retrieve per request
            page (int): ID of the page to return (starts with page 1)
            as_list (bool): If set to False and no pagination option is
                defined, return a generator instead of a list
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabListError: If the list could not be retrieved

        Returns:
            RESTObjectList: The list of members
        """

        path = "%s/all" % self.path
        obj = self.gitlab.http_list(path, **kwargs)
        return [self._obj_cls(self, item) for item in obj]


class ProjectMember(SaveMixin, ObjectDeleteMixin, RESTObject):
    _short_print_attr = "username"


class ProjectMemberManager(CRUDMixin, RESTManager):
    _path = "/projects/%(project_id)s/members"
    _obj_cls = ProjectMember
    _from_parent_attrs = {"project_id": "id"}
    _create_attrs = (("access_level", "user_id"), ("expires_at",))
    _update_attrs = (("access_level",), ("expires_at",))

    @cli.register_custom_action("ProjectMemberManager")
    @exc.on_http_error(exc.GitlabListError)
    def all(self, **kwargs):
        """List all the members, included inherited ones.

        Args:
            all (bool): If True, return all the items, without pagination
            per_page (int): Number of items to retrieve per request
            page (int): ID of the page to return (starts with page 1)
            as_list (bool): If set to False and no pagination option is
                defined, return a generator instead of a list
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabListError: If the list could not be retrieved

        Returns:
            RESTObjectList: The list of members
        """

        path = "%s/all" % self.path
        obj = self.gitlab.http_list(path, **kwargs)
        return [self._obj_cls(self, item) for item in obj]

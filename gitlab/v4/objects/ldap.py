from typing import Any, List, Union

from ... import exceptions as exc
from ...base import RESTManager, RESTObject, RESTObjectList

__all__ = [
    "LDAPGroup",
    "LDAPGroupManager",
]


class LDAPGroup(RESTObject):
    _id_attr = None


class LDAPGroupManager(RESTManager):
    _path = "/ldap/groups"
    _obj_cls = LDAPGroup
    _list_filters = ("search", "provider")

    @exc.on_http_error(exc.GitlabListError)
    def list(self, **kwargs: Any) -> Union[List[LDAPGroup], RESTObjectList]:
        """Retrieve a list of objects.

        Args:
            all: If True, return all the items, without pagination
            per_page: Number of items to retrieve per request
            page: ID of the page to return (starts with page 1)
            as_list: If set to False and no pagination option is
                defined, return a generator instead of a list
            **kwargs: Extra options to send to the server (e.g. sudo)

        Returns:
            The list of objects, or a generator if `as_list` is False

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabListError: If the server cannot perform the request
        """
        data = kwargs.copy()
        if self.gitlab.per_page:
            data.setdefault("per_page", self.gitlab.per_page)

        if "provider" in data:
            path = f"/ldap/{data['provider']}/groups"
        else:
            path = self._path

        obj = self.gitlab.http_list(path, **data)
        if isinstance(obj, list):
            return [self._obj_cls(self, item) for item in obj]
        else:
            return RESTObjectList(self, self._obj_cls, obj)

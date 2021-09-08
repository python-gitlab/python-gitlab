# -*- coding: utf-8 -*-
#
# Copyright (C) 2013-2017 Gauvain Pocentek <gauvain@pocentek.net>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from types import ModuleType
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Tuple,
    Type,
    TYPE_CHECKING,
    Union,
)

import requests

import gitlab
from gitlab import base, cli
from gitlab import exceptions as exc
from gitlab import types as g_types
from gitlab import utils

__all__ = [
    "GetMixin",
    "GetWithoutIdMixin",
    "RefreshMixin",
    "ListMixin",
    "RetrieveMixin",
    "CreateMixin",
    "UpdateMixin",
    "SetMixin",
    "DeleteMixin",
    "CRUDMixin",
    "NoUpdateMixin",
    "SaveMixin",
    "ObjectDeleteMixin",
    "UserAgentDetailMixin",
    "AccessRequestMixin",
    "DownloadMixin",
    "SubscribableMixin",
    "TodoMixin",
    "TimeTrackingMixin",
    "ParticipantsMixin",
    "BadgeRenderMixin",
]

if TYPE_CHECKING:
    # When running mypy we use these as the base classes
    _RestManagerBase = base.RESTManager
    _RestObjectBase = base.RESTObject
else:
    _RestManagerBase = object
    _RestObjectBase = object


class GetMixin(_RestManagerBase):
    _computed_path: Optional[str]
    _from_parent_attrs: Dict[str, Any]
    _obj_cls: Optional[Type[base.RESTObject]]
    _optional_get_attrs: Tuple[str, ...] = ()
    _parent: Optional[base.RESTObject]
    _parent_attrs: Dict[str, Any]
    _path: Optional[str]
    gitlab: gitlab.Gitlab

    @exc.on_http_error(exc.GitlabGetError)
    def get(
        self, id: Union[str, int], lazy: bool = False, **kwargs: Any
    ) -> base.RESTObject:
        """Retrieve a single object.

        Args:
            id (int or str): ID of the object to retrieve
            lazy (bool): If True, don't request the server, but create a
                         shallow object giving access to the managers. This is
                         useful if you want to avoid useless calls to the API.
            **kwargs: Extra options to send to the server (e.g. sudo)

        Returns:
            object: The generated RESTObject.

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabGetError: If the server cannot perform the request
        """
        if not isinstance(id, int):
            id = utils.clean_str_id(id)
        path = "%s/%s" % (self.path, id)
        if TYPE_CHECKING:
            assert self._obj_cls is not None
        if lazy is True:
            if TYPE_CHECKING:
                assert self._obj_cls._id_attr is not None
            return self._obj_cls(self, {self._obj_cls._id_attr: id})
        server_data = self.gitlab.http_get(path, **kwargs)
        if TYPE_CHECKING:
            assert not isinstance(server_data, requests.Response)
        return self._obj_cls(self, server_data)


class GetWithoutIdMixin(_RestManagerBase):
    _computed_path: Optional[str]
    _from_parent_attrs: Dict[str, Any]
    _obj_cls: Optional[Type[base.RESTObject]]
    _optional_get_attrs: Tuple[str, ...] = ()
    _parent: Optional[base.RESTObject]
    _parent_attrs: Dict[str, Any]
    _path: Optional[str]
    gitlab: gitlab.Gitlab

    @exc.on_http_error(exc.GitlabGetError)
    def get(
        self, id: Optional[Union[int, str]] = None, **kwargs: Any
    ) -> Optional[base.RESTObject]:
        """Retrieve a single object.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Returns:
            object: The generated RESTObject

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabGetError: If the server cannot perform the request
        """
        if TYPE_CHECKING:
            assert self.path is not None
        server_data = self.gitlab.http_get(self.path, **kwargs)
        if server_data is None:
            return None
        if TYPE_CHECKING:
            assert not isinstance(server_data, requests.Response)
            assert self._obj_cls is not None
        return self._obj_cls(self, server_data)


class RefreshMixin(_RestObjectBase):
    _id_attr: Optional[str]
    _attrs: Dict[str, Any]
    _module: ModuleType
    _parent_attrs: Dict[str, Any]
    _updated_attrs: Dict[str, Any]
    manager: base.RESTManager

    @exc.on_http_error(exc.GitlabGetError)
    def refresh(self, **kwargs: Any) -> None:
        """Refresh a single object from server.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Returns None (updates the object)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabGetError: If the server cannot perform the request
        """
        if self._id_attr:
            path = "%s/%s" % (self.manager.path, self.id)
        else:
            if TYPE_CHECKING:
                assert self.manager.path is not None
            path = self.manager.path
        server_data = self.manager.gitlab.http_get(path, **kwargs)
        if TYPE_CHECKING:
            assert not isinstance(server_data, requests.Response)
        self._update_attrs(server_data)


class ListMixin(_RestManagerBase):
    _computed_path: Optional[str]
    _from_parent_attrs: Dict[str, Any]
    _list_filters: Tuple[str, ...] = ()
    _obj_cls: Optional[Type[base.RESTObject]]
    _parent: Optional[base.RESTObject]
    _parent_attrs: Dict[str, Any]
    _path: Optional[str]
    gitlab: gitlab.Gitlab

    @exc.on_http_error(exc.GitlabListError)
    def list(self, **kwargs: Any) -> Union[base.RESTObjectList, List[base.RESTObject]]:
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

        # Duplicate data to avoid messing with what the user sent us
        data = kwargs.copy()
        if self.gitlab.per_page:
            data.setdefault("per_page", self.gitlab.per_page)

        # global keyset pagination
        if self.gitlab.pagination:
            data.setdefault("pagination", self.gitlab.pagination)

        if self.gitlab.order_by:
            data.setdefault("order_by", self.gitlab.order_by)

        # We get the attributes that need some special transformation
        if self._types:
            for attr_name, type_cls in self._types.items():
                if attr_name in data.keys():
                    type_obj = type_cls(data[attr_name])
                    data[attr_name] = type_obj.get_for_api()

        # Allow to overwrite the path, handy for custom listings
        path = data.pop("path", self.path)

        if TYPE_CHECKING:
            assert self._obj_cls is not None
        obj = self.gitlab.http_list(path, **data)
        if isinstance(obj, list):
            return [self._obj_cls(self, item) for item in obj]
        else:
            return base.RESTObjectList(self, self._obj_cls, obj)


class RetrieveMixin(ListMixin, GetMixin):
    _computed_path: Optional[str]
    _from_parent_attrs: Dict[str, Any]
    _obj_cls: Optional[Type[base.RESTObject]]
    _parent: Optional[base.RESTObject]
    _parent_attrs: Dict[str, Any]
    _path: Optional[str]
    gitlab: gitlab.Gitlab

    pass


class CreateMixin(_RestManagerBase):
    _computed_path: Optional[str]
    _from_parent_attrs: Dict[str, Any]
    _obj_cls: Optional[Type[base.RESTObject]]
    _parent: Optional[base.RESTObject]
    _parent_attrs: Dict[str, Any]
    _path: Optional[str]
    gitlab: gitlab.Gitlab

    def _check_missing_create_attrs(self, data: Dict[str, Any]) -> None:
        missing = []
        for attr in self._create_attrs.required:
            if attr not in data:
                missing.append(attr)
                continue
        if missing:
            raise AttributeError("Missing attributes: %s" % ", ".join(missing))

    @exc.on_http_error(exc.GitlabCreateError)
    def create(
        self, data: Optional[Dict[str, Any]] = None, **kwargs: Any
    ) -> base.RESTObject:
        """Create a new object.

        Args:
            data (dict): parameters to send to the server to create the
                         resource
            **kwargs: Extra options to send to the server (e.g. sudo)

        Returns:
            RESTObject: a new instance of the managed object class built with
                the data sent by the server

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabCreateError: If the server cannot perform the request
        """
        if data is None:
            data = {}

        self._check_missing_create_attrs(data)
        files = {}

        # We get the attributes that need some special transformation
        if self._types:
            # Duplicate data to avoid messing with what the user sent us
            data = data.copy()
            for attr_name, type_cls in self._types.items():
                if attr_name in data.keys():
                    type_obj = type_cls(data[attr_name])

                    # if the type if FileAttribute we need to pass the data as
                    # file
                    if isinstance(type_obj, g_types.FileAttribute):
                        k = type_obj.get_file_name(attr_name)
                        files[attr_name] = (k, data.pop(attr_name))
                    else:
                        data[attr_name] = type_obj.get_for_api()

        # Handle specific URL for creation
        path = kwargs.pop("path", self.path)
        server_data = self.gitlab.http_post(path, post_data=data, files=files, **kwargs)
        if TYPE_CHECKING:
            assert not isinstance(server_data, requests.Response)
            assert self._obj_cls is not None
        return self._obj_cls(self, server_data)


class UpdateMixin(_RestManagerBase):
    _computed_path: Optional[str]
    _from_parent_attrs: Dict[str, Any]
    _obj_cls: Optional[Type[base.RESTObject]]
    _parent: Optional[base.RESTObject]
    _parent_attrs: Dict[str, Any]
    _path: Optional[str]
    _update_uses_post: bool = False
    gitlab: gitlab.Gitlab

    def _check_missing_update_attrs(self, data: Dict[str, Any]) -> None:
        if TYPE_CHECKING:
            assert self._obj_cls is not None
        # Remove the id field from the required list as it was previously moved
        # to the http path.
        required = tuple(
            [k for k in self._update_attrs.required if k != self._obj_cls._id_attr]
        )
        missing = []
        for attr in required:
            if attr not in data:
                missing.append(attr)
                continue
        if missing:
            raise AttributeError("Missing attributes: %s" % ", ".join(missing))

    def _get_update_method(
        self,
    ) -> Callable[..., Union[Dict[str, Any], requests.Response]]:
        """Return the HTTP method to use.

        Returns:
            object: http_put (default) or http_post
        """
        if self._update_uses_post:
            http_method = self.gitlab.http_post
        else:
            http_method = self.gitlab.http_put
        return http_method

    @exc.on_http_error(exc.GitlabUpdateError)
    def update(
        self,
        id: Optional[Union[str, int]] = None,
        new_data: Optional[Dict[str, Any]] = None,
        **kwargs: Any
    ) -> Dict[str, Any]:
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

        if id is None:
            path = self.path
        else:
            path = "%s/%s" % (self.path, id)

        self._check_missing_update_attrs(new_data)
        files = {}

        # We get the attributes that need some special transformation
        if self._types:
            # Duplicate data to avoid messing with what the user sent us
            new_data = new_data.copy()
            for attr_name, type_cls in self._types.items():
                if attr_name in new_data.keys():
                    type_obj = type_cls(new_data[attr_name])

                    # if the type if FileAttribute we need to pass the data as
                    # file
                    if isinstance(type_obj, g_types.FileAttribute):
                        k = type_obj.get_file_name(attr_name)
                        files[attr_name] = (k, new_data.pop(attr_name))
                    else:
                        new_data[attr_name] = type_obj.get_for_api()

        http_method = self._get_update_method()
        result = http_method(path, post_data=new_data, files=files, **kwargs)
        if TYPE_CHECKING:
            assert not isinstance(result, requests.Response)
        return result


class SetMixin(_RestManagerBase):
    _computed_path: Optional[str]
    _from_parent_attrs: Dict[str, Any]
    _obj_cls: Optional[Type[base.RESTObject]]
    _parent: Optional[base.RESTObject]
    _parent_attrs: Dict[str, Any]
    _path: Optional[str]
    gitlab: gitlab.Gitlab

    @exc.on_http_error(exc.GitlabSetError)
    def set(self, key: str, value: str, **kwargs: Any) -> base.RESTObject:
        """Create or update the object.

        Args:
            key (str): The key of the object to create/update
            value (str): The value to set for the object
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabSetError: If an error occured

        Returns:
            obj: The created/updated attribute
        """
        path = "%s/%s" % (self.path, utils.clean_str_id(key))
        data = {"value": value}
        server_data = self.gitlab.http_put(path, post_data=data, **kwargs)
        if TYPE_CHECKING:
            assert not isinstance(server_data, requests.Response)
            assert self._obj_cls is not None
        return self._obj_cls(self, server_data)


class DeleteMixin(_RestManagerBase):
    _computed_path: Optional[str]
    _from_parent_attrs: Dict[str, Any]
    _obj_cls: Optional[Type[base.RESTObject]]
    _parent: Optional[base.RESTObject]
    _parent_attrs: Dict[str, Any]
    _path: Optional[str]
    gitlab: gitlab.Gitlab

    @exc.on_http_error(exc.GitlabDeleteError)
    def delete(self, id: Union[str, int], **kwargs: Any) -> None:
        """Delete an object on the server.

        Args:
            id: ID of the object to delete
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabDeleteError: If the server cannot perform the request
        """
        if id is None:
            path = self.path
        else:
            if not isinstance(id, int):
                id = utils.clean_str_id(id)
            path = "%s/%s" % (self.path, id)
        self.gitlab.http_delete(path, **kwargs)


class CRUDMixin(GetMixin, ListMixin, CreateMixin, UpdateMixin, DeleteMixin):
    _computed_path: Optional[str]
    _from_parent_attrs: Dict[str, Any]
    _obj_cls: Optional[Type[base.RESTObject]]
    _parent: Optional[base.RESTObject]
    _parent_attrs: Dict[str, Any]
    _path: Optional[str]
    gitlab: gitlab.Gitlab

    pass


class NoUpdateMixin(GetMixin, ListMixin, CreateMixin, DeleteMixin):
    _computed_path: Optional[str]
    _from_parent_attrs: Dict[str, Any]
    _obj_cls: Optional[Type[base.RESTObject]]
    _parent: Optional[base.RESTObject]
    _parent_attrs: Dict[str, Any]
    _path: Optional[str]
    gitlab: gitlab.Gitlab

    pass


class SaveMixin(_RestObjectBase):
    """Mixin for RESTObject's that can be updated."""

    _id_attr: Optional[str]
    _attrs: Dict[str, Any]
    _module: ModuleType
    _parent_attrs: Dict[str, Any]
    _updated_attrs: Dict[str, Any]
    manager: base.RESTManager

    def _get_updated_data(self) -> Dict[str, Any]:
        updated_data = {}
        for attr in self.manager._update_attrs.required:
            # Get everything required, no matter if it's been updated
            updated_data[attr] = getattr(self, attr)
        # Add the updated attributes
        updated_data.update(self._updated_attrs)

        return updated_data

    def save(self, **kwargs: Any) -> None:
        """Save the changes made to the object to the server.

        The object is updated to match what the server returns.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raise:
            GitlabAuthenticationError: If authentication is not correct
            GitlabUpdateError: If the server cannot perform the request
        """
        updated_data = self._get_updated_data()
        # Nothing to update. Server fails if sent an empty dict.
        if not updated_data:
            return

        # call the manager
        obj_id = self.get_id()
        if TYPE_CHECKING:
            assert isinstance(self.manager, UpdateMixin)
        server_data = self.manager.update(obj_id, updated_data, **kwargs)
        if server_data is not None:
            self._update_attrs(server_data)


class ObjectDeleteMixin(_RestObjectBase):
    """Mixin for RESTObject's that can be deleted."""

    _id_attr: Optional[str]
    _attrs: Dict[str, Any]
    _module: ModuleType
    _parent_attrs: Dict[str, Any]
    _updated_attrs: Dict[str, Any]
    manager: base.RESTManager

    def delete(self, **kwargs: Any) -> None:
        """Delete the object from the server.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabDeleteError: If the server cannot perform the request
        """
        if TYPE_CHECKING:
            assert isinstance(self.manager, DeleteMixin)
        self.manager.delete(self.get_id(), **kwargs)


class UserAgentDetailMixin(_RestObjectBase):
    _id_attr: Optional[str]
    _attrs: Dict[str, Any]
    _module: ModuleType
    _parent_attrs: Dict[str, Any]
    _updated_attrs: Dict[str, Any]
    manager: base.RESTManager

    @cli.register_custom_action(("Snippet", "ProjectSnippet", "ProjectIssue"))
    @exc.on_http_error(exc.GitlabGetError)
    def user_agent_detail(self, **kwargs: Any) -> Dict[str, Any]:
        """Get the user agent detail.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabGetError: If the server cannot perform the request
        """
        path = "%s/%s/user_agent_detail" % (self.manager.path, self.get_id())
        result = self.manager.gitlab.http_get(path, **kwargs)
        if TYPE_CHECKING:
            assert not isinstance(result, requests.Response)
        return result


class AccessRequestMixin(_RestObjectBase):
    _id_attr: Optional[str]
    _attrs: Dict[str, Any]
    _module: ModuleType
    _parent_attrs: Dict[str, Any]
    _updated_attrs: Dict[str, Any]
    manager: base.RESTManager

    @cli.register_custom_action(
        ("ProjectAccessRequest", "GroupAccessRequest"), tuple(), ("access_level",)
    )
    @exc.on_http_error(exc.GitlabUpdateError)
    def approve(
        self, access_level: int = gitlab.DEVELOPER_ACCESS, **kwargs: Any
    ) -> None:
        """Approve an access request.

        Args:
            access_level (int): The access level for the user
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabUpdateError: If the server fails to perform the request
        """

        path = "%s/%s/approve" % (self.manager.path, self.id)
        data = {"access_level": access_level}
        server_data = self.manager.gitlab.http_put(path, post_data=data, **kwargs)
        if TYPE_CHECKING:
            assert not isinstance(server_data, requests.Response)
        self._update_attrs(server_data)


class DownloadMixin(_RestObjectBase):
    _id_attr: Optional[str]
    _attrs: Dict[str, Any]
    _module: ModuleType
    _parent_attrs: Dict[str, Any]
    _updated_attrs: Dict[str, Any]
    manager: base.RESTManager

    @cli.register_custom_action(("GroupExport", "ProjectExport"))
    @exc.on_http_error(exc.GitlabGetError)
    def download(
        self,
        streamed: bool = False,
        action: Optional[Callable] = None,
        chunk_size: int = 1024,
        **kwargs: Any
    ) -> Optional[bytes]:
        """Download the archive of a resource export.

        Args:
            streamed (bool): If True the data will be processed by chunks of
                `chunk_size` and each chunk is passed to `action` for
                reatment
            action (callable): Callable responsible of dealing with chunk of
                data
            chunk_size (int): Size of each chunk
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabGetError: If the server failed to perform the request

        Returns:
            str: The blob content if streamed is False, None otherwise
        """
        path = "%s/download" % (self.manager.path)
        result = self.manager.gitlab.http_get(
            path, streamed=streamed, raw=True, **kwargs
        )
        if TYPE_CHECKING:
            assert isinstance(result, requests.Response)
        return utils.response_content(result, streamed, action, chunk_size)


class SubscribableMixin(_RestObjectBase):
    _id_attr: Optional[str]
    _attrs: Dict[str, Any]
    _module: ModuleType
    _parent_attrs: Dict[str, Any]
    _updated_attrs: Dict[str, Any]
    manager: base.RESTManager

    @cli.register_custom_action(
        ("ProjectIssue", "ProjectMergeRequest", "ProjectLabel", "GroupLabel")
    )
    @exc.on_http_error(exc.GitlabSubscribeError)
    def subscribe(self, **kwargs: Any) -> None:
        """Subscribe to the object notifications.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabSubscribeError: If the subscription cannot be done
        """
        path = "%s/%s/subscribe" % (self.manager.path, self.get_id())
        server_data = self.manager.gitlab.http_post(path, **kwargs)
        if TYPE_CHECKING:
            assert not isinstance(server_data, requests.Response)
        self._update_attrs(server_data)

    @cli.register_custom_action(
        ("ProjectIssue", "ProjectMergeRequest", "ProjectLabel", "GroupLabel")
    )
    @exc.on_http_error(exc.GitlabUnsubscribeError)
    def unsubscribe(self, **kwargs: Any) -> None:
        """Unsubscribe from the object notifications.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabUnsubscribeError: If the unsubscription cannot be done
        """
        path = "%s/%s/unsubscribe" % (self.manager.path, self.get_id())
        server_data = self.manager.gitlab.http_post(path, **kwargs)
        if TYPE_CHECKING:
            assert not isinstance(server_data, requests.Response)
        self._update_attrs(server_data)


class TodoMixin(_RestObjectBase):
    _id_attr: Optional[str]
    _attrs: Dict[str, Any]
    _module: ModuleType
    _parent_attrs: Dict[str, Any]
    _updated_attrs: Dict[str, Any]
    manager: base.RESTManager

    @cli.register_custom_action(("ProjectIssue", "ProjectMergeRequest"))
    @exc.on_http_error(exc.GitlabTodoError)
    def todo(self, **kwargs: Any) -> None:
        """Create a todo associated to the object.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabTodoError: If the todo cannot be set
        """
        path = "%s/%s/todo" % (self.manager.path, self.get_id())
        self.manager.gitlab.http_post(path, **kwargs)


class TimeTrackingMixin(_RestObjectBase):
    _id_attr: Optional[str]
    _attrs: Dict[str, Any]
    _module: ModuleType
    _parent_attrs: Dict[str, Any]
    _updated_attrs: Dict[str, Any]
    manager: base.RESTManager

    @cli.register_custom_action(("ProjectIssue", "ProjectMergeRequest"))
    @exc.on_http_error(exc.GitlabTimeTrackingError)
    def time_stats(self, **kwargs: Any) -> Dict[str, Any]:
        """Get time stats for the object.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabTimeTrackingError: If the time tracking update cannot be done
        """
        # Use the existing time_stats attribute if it exist, otherwise make an
        # API call
        if "time_stats" in self.attributes:
            return self.attributes["time_stats"]

        path = "%s/%s/time_stats" % (self.manager.path, self.get_id())
        result = self.manager.gitlab.http_get(path, **kwargs)
        if TYPE_CHECKING:
            assert not isinstance(result, requests.Response)
        return result

    @cli.register_custom_action(("ProjectIssue", "ProjectMergeRequest"), ("duration",))
    @exc.on_http_error(exc.GitlabTimeTrackingError)
    def time_estimate(self, duration: str, **kwargs: Any) -> Dict[str, Any]:
        """Set an estimated time of work for the object.

        Args:
            duration (str): Duration in human format (e.g. 3h30)
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabTimeTrackingError: If the time tracking update cannot be done
        """
        path = "%s/%s/time_estimate" % (self.manager.path, self.get_id())
        data = {"duration": duration}
        result = self.manager.gitlab.http_post(path, post_data=data, **kwargs)
        if TYPE_CHECKING:
            assert not isinstance(result, requests.Response)
        return result

    @cli.register_custom_action(("ProjectIssue", "ProjectMergeRequest"))
    @exc.on_http_error(exc.GitlabTimeTrackingError)
    def reset_time_estimate(self, **kwargs: Any) -> Dict[str, Any]:
        """Resets estimated time for the object to 0 seconds.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabTimeTrackingError: If the time tracking update cannot be done
        """
        path = "%s/%s/reset_time_estimate" % (self.manager.path, self.get_id())
        result = self.manager.gitlab.http_post(path, **kwargs)
        if TYPE_CHECKING:
            assert not isinstance(result, requests.Response)
        return result

    @cli.register_custom_action(("ProjectIssue", "ProjectMergeRequest"), ("duration",))
    @exc.on_http_error(exc.GitlabTimeTrackingError)
    def add_spent_time(self, duration: str, **kwargs: Any) -> Dict[str, Any]:
        """Add time spent working on the object.

        Args:
            duration (str): Duration in human format (e.g. 3h30)
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabTimeTrackingError: If the time tracking update cannot be done
        """
        path = "%s/%s/add_spent_time" % (self.manager.path, self.get_id())
        data = {"duration": duration}
        result = self.manager.gitlab.http_post(path, post_data=data, **kwargs)
        if TYPE_CHECKING:
            assert not isinstance(result, requests.Response)
        return result

    @cli.register_custom_action(("ProjectIssue", "ProjectMergeRequest"))
    @exc.on_http_error(exc.GitlabTimeTrackingError)
    def reset_spent_time(self, **kwargs: Any) -> Dict[str, Any]:
        """Resets the time spent working on the object.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabTimeTrackingError: If the time tracking update cannot be done
        """
        path = "%s/%s/reset_spent_time" % (self.manager.path, self.get_id())
        result = self.manager.gitlab.http_post(path, **kwargs)
        if TYPE_CHECKING:
            assert not isinstance(result, requests.Response)
        return result


class ParticipantsMixin(_RestObjectBase):
    _id_attr: Optional[str]
    _attrs: Dict[str, Any]
    _module: ModuleType
    _parent_attrs: Dict[str, Any]
    _updated_attrs: Dict[str, Any]
    manager: base.RESTManager

    @cli.register_custom_action(("ProjectMergeRequest", "ProjectIssue"))
    @exc.on_http_error(exc.GitlabListError)
    def participants(self, **kwargs: Any) -> Dict[str, Any]:
        """List the participants.

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
            RESTObjectList: The list of participants
        """

        path = "%s/%s/participants" % (self.manager.path, self.get_id())
        result = self.manager.gitlab.http_get(path, **kwargs)
        if TYPE_CHECKING:
            assert not isinstance(result, requests.Response)
        return result


class BadgeRenderMixin(_RestManagerBase):
    @cli.register_custom_action(
        ("GroupBadgeManager", "ProjectBadgeManager"), ("link_url", "image_url")
    )
    @exc.on_http_error(exc.GitlabRenderError)
    def render(self, link_url: str, image_url: str, **kwargs: Any) -> Dict[str, Any]:
        """Preview link_url and image_url after interpolation.

        Args:
            link_url (str): URL of the badge link
            image_url (str): URL of the badge image
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabRenderError: If the rendering failed

        Returns:
            dict: The rendering properties
        """
        path = "%s/render" % self.path
        data = {"link_url": link_url, "image_url": image_url}
        result = self.gitlab.http_get(path, data, **kwargs)
        if TYPE_CHECKING:
            assert not isinstance(result, requests.Response)
        return result

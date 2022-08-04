from types import ModuleType
from typing import (
    Any,
    Callable,
    Dict,
    Iterator,
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


class HeadMixin(_RestManagerBase):
    @exc.on_http_error(exc.GitlabHeadError)
    def head(
        self, id: Optional[Union[str, int]] = None, **kwargs: Any
    ) -> "requests.structures.CaseInsensitiveDict[Any]":
        """Retrieve headers from an endpoint.

        Args:
            id: ID of the object to retrieve
            **kwargs: Extra options to send to the server (e.g. sudo)

        Returns:
            A requests header object.

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabHeadError: If the server cannot perform the request
        """
        if TYPE_CHECKING:
            assert self.path is not None

        path = self.path
        if id is not None:
            path = f"{path}/{utils.EncodedId(id)}"

        return self.gitlab.http_head(path, **kwargs)


class GetMixin(HeadMixin, _RestManagerBase):
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
            id: ID of the object to retrieve
            lazy: If True, don't request the server, but create a
                         shallow object giving access to the managers. This is
                         useful if you want to avoid useless calls to the API.
            **kwargs: Extra options to send to the server (e.g. sudo)

        Returns:
            The generated RESTObject.

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabGetError: If the server cannot perform the request
        """
        if isinstance(id, str):
            id = utils.EncodedId(id)
        path = f"{self.path}/{id}"
        if TYPE_CHECKING:
            assert self._obj_cls is not None
        if lazy is True:
            if TYPE_CHECKING:
                assert self._obj_cls._id_attr is not None
            return self._obj_cls(self, {self._obj_cls._id_attr: id}, lazy=lazy)
        server_data = self.gitlab.http_get(path, **kwargs)
        if TYPE_CHECKING:
            assert not isinstance(server_data, requests.Response)
        return self._obj_cls(self, server_data, lazy=lazy)


class GetWithoutIdMixin(HeadMixin, _RestManagerBase):
    _computed_path: Optional[str]
    _from_parent_attrs: Dict[str, Any]
    _obj_cls: Optional[Type[base.RESTObject]]
    _optional_get_attrs: Tuple[str, ...] = ()
    _parent: Optional[base.RESTObject]
    _parent_attrs: Dict[str, Any]
    _path: Optional[str]
    gitlab: gitlab.Gitlab

    @exc.on_http_error(exc.GitlabGetError)
    def get(self, **kwargs: Any) -> base.RESTObject:
        """Retrieve a single object.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Returns:
            The generated RESTObject

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabGetError: If the server cannot perform the request
        """
        if TYPE_CHECKING:
            assert self.path is not None
        server_data = self.gitlab.http_get(self.path, **kwargs)
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
            path = f"{self.manager.path}/{self.encoded_id}"
        else:
            if TYPE_CHECKING:
                assert self.manager.path is not None
            path = self.manager.path
        server_data = self.manager.gitlab.http_get(path, **kwargs)
        if TYPE_CHECKING:
            assert not isinstance(server_data, requests.Response)
        self._update_attrs(server_data)


class ListMixin(HeadMixin, _RestManagerBase):
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
            all: If True, return all the items, without pagination
            per_page: Number of items to retrieve per request
            page: ID of the page to return (starts with page 1)
            iterator: If set to True and no pagination option is
                defined, return a generator instead of a list
            **kwargs: Extra options to send to the server (e.g. sudo)

        Returns:
            The list of objects, or a generator if `iterator` is True

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabListError: If the server cannot perform the request
        """

        data, _ = utils._transform_types(
            data=kwargs,
            custom_types=self._types,
            transform_data=True,
            transform_files=False,
        )

        if self.gitlab.per_page:
            data.setdefault("per_page", self.gitlab.per_page)

        # global keyset pagination
        if self.gitlab.pagination:
            data.setdefault("pagination", self.gitlab.pagination)

        if self.gitlab.order_by:
            data.setdefault("order_by", self.gitlab.order_by)

        # Allow to overwrite the path, handy for custom listings
        path = data.pop("path", self.path)

        if TYPE_CHECKING:
            assert self._obj_cls is not None
        obj = self.gitlab.http_list(path, **data)
        if isinstance(obj, list):
            return [self._obj_cls(self, item, created_from_list=True) for item in obj]
        return base.RESTObjectList(self, self._obj_cls, obj)


class RetrieveMixin(ListMixin, GetMixin):
    _computed_path: Optional[str]
    _from_parent_attrs: Dict[str, Any]
    _obj_cls: Optional[Type[base.RESTObject]]
    _parent: Optional[base.RESTObject]
    _parent_attrs: Dict[str, Any]
    _path: Optional[str]
    gitlab: gitlab.Gitlab


class CreateMixin(_RestManagerBase):
    _computed_path: Optional[str]
    _from_parent_attrs: Dict[str, Any]
    _obj_cls: Optional[Type[base.RESTObject]]
    _parent: Optional[base.RESTObject]
    _parent_attrs: Dict[str, Any]
    _path: Optional[str]
    gitlab: gitlab.Gitlab

    @exc.on_http_error(exc.GitlabCreateError)
    def create(
        self, data: Optional[Dict[str, Any]] = None, **kwargs: Any
    ) -> base.RESTObject:
        """Create a new object.

        Args:
            data: parameters to send to the server to create the
                         resource
            **kwargs: Extra options to send to the server (e.g. sudo)

        Returns:
            A new instance of the managed object class built with
                the data sent by the server

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabCreateError: If the server cannot perform the request
        """
        if data is None:
            data = {}

        self._create_attrs.validate_attrs(data=data)
        data, files = utils._transform_types(
            data=data, custom_types=self._types, transform_data=False
        )

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

    def _get_update_method(
        self,
    ) -> Callable[..., Union[Dict[str, Any], requests.Response]]:
        """Return the HTTP method to use.

        Returns:
            http_put (default) or http_post
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
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """Update an object on the server.

        Args:
            id: ID of the object to update (can be None if not required)
            new_data: the update data for the object
            **kwargs: Extra options to send to the server (e.g. sudo)

        Returns:
            The new object data (*not* a RESTObject)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabUpdateError: If the server cannot perform the request
        """
        new_data = new_data or {}

        if id is None:
            path = self.path
        else:
            path = f"{self.path}/{utils.EncodedId(id)}"

        excludes = []
        if self._obj_cls is not None and self._obj_cls._id_attr is not None:
            excludes = [self._obj_cls._id_attr]
        self._update_attrs.validate_attrs(data=new_data, excludes=excludes)
        new_data, files = utils._transform_types(
            data=new_data, custom_types=self._types, transform_data=False
        )

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
            key: The key of the object to create/update
            value: The value to set for the object
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabSetError: If an error occurred

        Returns:
            The created/updated attribute
        """
        path = f"{self.path}/{utils.EncodedId(key)}"
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
    def delete(self, id: Optional[Union[str, int]] = None, **kwargs: Any) -> None:
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
            path = f"{self.path}/{utils.EncodedId(id)}"

        if TYPE_CHECKING:
            assert path is not None
        self.gitlab.http_delete(path, **kwargs)


class CRUDMixin(GetMixin, ListMixin, CreateMixin, UpdateMixin, DeleteMixin):
    _computed_path: Optional[str]
    _from_parent_attrs: Dict[str, Any]
    _obj_cls: Optional[Type[base.RESTObject]]
    _parent: Optional[base.RESTObject]
    _parent_attrs: Dict[str, Any]
    _path: Optional[str]
    gitlab: gitlab.Gitlab


class NoUpdateMixin(GetMixin, ListMixin, CreateMixin, DeleteMixin):
    _computed_path: Optional[str]
    _from_parent_attrs: Dict[str, Any]
    _obj_cls: Optional[Type[base.RESTObject]]
    _parent: Optional[base.RESTObject]
    _parent_attrs: Dict[str, Any]
    _path: Optional[str]
    gitlab: gitlab.Gitlab


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

    def save(self, **kwargs: Any) -> Optional[Dict[str, Any]]:
        """Save the changes made to the object to the server.

        The object is updated to match what the server returns.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Returns:
            The new object data (*not* a RESTObject)

        Raise:
            GitlabAuthenticationError: If authentication is not correct
            GitlabUpdateError: If the server cannot perform the request
        """
        updated_data = self._get_updated_data()
        # Nothing to update. Server fails if sent an empty dict.
        if not updated_data:
            return None

        # call the manager
        obj_id = self.encoded_id
        if TYPE_CHECKING:
            assert isinstance(self.manager, UpdateMixin)
        server_data = self.manager.update(obj_id, updated_data, **kwargs)
        self._update_attrs(server_data)
        return server_data


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
            assert self.encoded_id is not None
        self.manager.delete(self.encoded_id, **kwargs)


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
        path = f"{self.manager.path}/{self.encoded_id}/user_agent_detail"
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
        ("ProjectAccessRequest", "GroupAccessRequest"), (), ("access_level",)
    )
    @exc.on_http_error(exc.GitlabUpdateError)
    def approve(
        self, access_level: int = gitlab.const.DEVELOPER_ACCESS, **kwargs: Any
    ) -> None:
        """Approve an access request.

        Args:
            access_level: The access level for the user
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabUpdateError: If the server fails to perform the request
        """

        path = f"{self.manager.path}/{self.encoded_id}/approve"
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
        action: Optional[Callable[[bytes], None]] = None,
        chunk_size: int = 1024,
        *,
        iterator: bool = False,
        **kwargs: Any,
    ) -> Optional[Union[bytes, Iterator[Any]]]:
        """Download the archive of a resource export.

        Args:
            streamed: If True the data will be processed by chunks of
                `chunk_size` and each chunk is passed to `action` for
                treatment
            iterator: If True directly return the underlying response
                iterator
            action: Callable responsible of dealing with chunk of
                data
            chunk_size: Size of each chunk
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabGetError: If the server failed to perform the request

        Returns:
            The blob content if streamed is False, None otherwise
        """
        path = f"{self.manager.path}/download"
        result = self.manager.gitlab.http_get(
            path, streamed=streamed, raw=True, **kwargs
        )
        if TYPE_CHECKING:
            assert isinstance(result, requests.Response)
        return utils.response_content(
            result, streamed, action, chunk_size, iterator=iterator
        )


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
        path = f"{self.manager.path}/{self.encoded_id}/subscribe"
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
        path = f"{self.manager.path}/{self.encoded_id}/unsubscribe"
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
        path = f"{self.manager.path}/{self.encoded_id}/todo"
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
            time_stats = self.attributes["time_stats"]
            if TYPE_CHECKING:
                assert isinstance(time_stats, dict)
            return time_stats

        path = f"{self.manager.path}/{self.encoded_id}/time_stats"
        result = self.manager.gitlab.http_get(path, **kwargs)
        if TYPE_CHECKING:
            assert not isinstance(result, requests.Response)
        return result

    @cli.register_custom_action(("ProjectIssue", "ProjectMergeRequest"), ("duration",))
    @exc.on_http_error(exc.GitlabTimeTrackingError)
    def time_estimate(self, duration: str, **kwargs: Any) -> Dict[str, Any]:
        """Set an estimated time of work for the object.

        Args:
            duration: Duration in human format (e.g. 3h30)
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabTimeTrackingError: If the time tracking update cannot be done
        """
        path = f"{self.manager.path}/{self.encoded_id}/time_estimate"
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
        path = f"{self.manager.path}/{self.encoded_id}/reset_time_estimate"
        result = self.manager.gitlab.http_post(path, **kwargs)
        if TYPE_CHECKING:
            assert not isinstance(result, requests.Response)
        return result

    @cli.register_custom_action(("ProjectIssue", "ProjectMergeRequest"), ("duration",))
    @exc.on_http_error(exc.GitlabTimeTrackingError)
    def add_spent_time(self, duration: str, **kwargs: Any) -> Dict[str, Any]:
        """Add time spent working on the object.

        Args:
            duration: Duration in human format (e.g. 3h30)
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabTimeTrackingError: If the time tracking update cannot be done
        """
        path = f"{self.manager.path}/{self.encoded_id}/add_spent_time"
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
        path = f"{self.manager.path}/{self.encoded_id}/reset_spent_time"
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
            all: If True, return all the items, without pagination
            per_page: Number of items to retrieve per request
            page: ID of the page to return (starts with page 1)
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabListError: If the list could not be retrieved

        Returns:
            The list of participants
        """

        path = f"{self.manager.path}/{self.encoded_id}/participants"
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
            link_url: URL of the badge link
            image_url: URL of the badge image
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabRenderError: If the rendering failed

        Returns:
            The rendering properties
        """
        path = f"{self.path}/render"
        data = {"link_url": link_url, "image_url": image_url}
        result = self.gitlab.http_get(path, data, **kwargs)
        if TYPE_CHECKING:
            assert not isinstance(result, requests.Response)
        return result


class PromoteMixin(_RestObjectBase):
    _id_attr: Optional[str]
    _attrs: Dict[str, Any]
    _module: ModuleType
    _parent_attrs: Dict[str, Any]
    _updated_attrs: Dict[str, Any]
    _update_uses_post: bool = False
    manager: base.RESTManager

    def _get_update_method(
        self,
    ) -> Callable[..., Union[Dict[str, Any], requests.Response]]:
        """Return the HTTP method to use.

        Returns:
            http_put (default) or http_post
        """
        if self._update_uses_post:
            http_method = self.manager.gitlab.http_post
        else:
            http_method = self.manager.gitlab.http_put
        return http_method

    @exc.on_http_error(exc.GitlabPromoteError)
    def promote(self, **kwargs: Any) -> Dict[str, Any]:
        """Promote the item.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabPromoteError: If the item could not be promoted
            GitlabParsingError: If the json data could not be parsed

        Returns:
            The updated object data (*not* a RESTObject)
        """

        path = f"{self.manager.path}/{self.encoded_id}/promote"
        http_method = self._get_update_method()
        result = http_method(path, **kwargs)
        if TYPE_CHECKING:
            assert not isinstance(result, requests.Response)
        return result

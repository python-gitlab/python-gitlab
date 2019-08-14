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

import gitlab
from gitlab import base
from gitlab import cli
from gitlab import exceptions as exc
from gitlab import types as g_types
from gitlab import utils


class GetMixin(object):
    @exc.on_http_error(exc.GitlabGetError)
    def get(self, id, lazy=False, **kwargs):
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
        if lazy is True:
            return self._obj_cls(self, {self._obj_cls._id_attr: id})
        server_data = self.gitlab.http_get(path, **kwargs)
        return self._obj_cls(self, server_data)


class GetWithoutIdMixin(object):
    @exc.on_http_error(exc.GitlabGetError)
    def get(self, id=None, **kwargs):
        """Retrieve a single object.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Returns:
            object: The generated RESTObject

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabGetError: If the server cannot perform the request
        """
        server_data = self.gitlab.http_get(self.path, **kwargs)
        if server_data is None:
            return None
        return self._obj_cls(self, server_data)


class RefreshMixin(object):
    @exc.on_http_error(exc.GitlabGetError)
    def refresh(self, **kwargs):
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
            path = self.manager.path
        server_data = self.manager.gitlab.http_get(path, **kwargs)
        self._update_attrs(server_data)


class ListMixin(object):
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

        # Duplicate data to avoid messing with what the user sent us
        data = kwargs.copy()
        if self.gitlab.per_page:
            data.setdefault("per_page", self.gitlab.per_page)

        # We get the attributes that need some special transformation
        types = getattr(self, "_types", {})
        if types:
            for attr_name, type_cls in types.items():
                if attr_name in data.keys():
                    type_obj = type_cls(data[attr_name])
                    data[attr_name] = type_obj.get_for_api()

        # Allow to overwrite the path, handy for custom listings
        path = data.pop("path", self.path)

        obj = self.gitlab.http_list(path, **data)
        if isinstance(obj, list):
            return [self._obj_cls(self, item) for item in obj]
        else:
            return base.RESTObjectList(self, self._obj_cls, obj)


class RetrieveMixin(ListMixin, GetMixin):
    pass


class CreateMixin(object):
    def _check_missing_create_attrs(self, data):
        required, optional = self.get_create_attrs()
        missing = []
        for attr in required:
            if attr not in data:
                missing.append(attr)
                continue
        if missing:
            raise AttributeError("Missing attributes: %s" % ", ".join(missing))

    def get_create_attrs(self):
        """Return the required and optional arguments.

        Returns:
            tuple: 2 items: list of required arguments and list of optional
                   arguments for creation (in that order)
        """
        return getattr(self, "_create_attrs", (tuple(), tuple()))

    @exc.on_http_error(exc.GitlabCreateError)
    def create(self, data, **kwargs):
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
        self._check_missing_create_attrs(data)
        files = {}

        # We get the attributes that need some special transformation
        types = getattr(self, "_types", {})
        if types:
            # Duplicate data to avoid messing with what the user sent us
            data = data.copy()
            for attr_name, type_cls in types.items():
                if attr_name in data.keys():
                    type_obj = type_cls(data[attr_name])

                    # if the type if FileAttribute we need to pass the data as
                    # file
                    if issubclass(type_cls, g_types.FileAttribute):
                        k = type_obj.get_file_name(attr_name)
                        files[attr_name] = (k, data.pop(attr_name))
                    else:
                        data[attr_name] = type_obj.get_for_api()

        # Handle specific URL for creation
        path = kwargs.pop("path", self.path)
        server_data = self.gitlab.http_post(path, post_data=data, files=files, **kwargs)
        return self._obj_cls(self, server_data)


class UpdateMixin(object):
    def _check_missing_update_attrs(self, data):
        required, optional = self.get_update_attrs()
        # Remove the id field from the required list as it was previously moved to the http path.
        required = tuple(filter(lambda k: k != self._obj_cls._id_attr, required))
        missing = []
        for attr in required:
            if attr not in data:
                missing.append(attr)
                continue
        if missing:
            raise AttributeError("Missing attributes: %s" % ", ".join(missing))

    def get_update_attrs(self):
        """Return the required and optional arguments.

        Returns:
            tuple: 2 items: list of required arguments and list of optional
                   arguments for update (in that order)
        """
        return getattr(self, "_update_attrs", (tuple(), tuple()))

    def _get_update_method(self):
        """Return the HTTP method to use.

        Returns:
            object: http_put (default) or http_post
        """
        if getattr(self, "_update_uses_post", False):
            http_method = self.gitlab.http_post
        else:
            http_method = self.gitlab.http_put
        return http_method

    @exc.on_http_error(exc.GitlabUpdateError)
    def update(self, id=None, new_data=None, **kwargs):
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
        types = getattr(self, "_types", {})
        if types:
            # Duplicate data to avoid messing with what the user sent us
            new_data = new_data.copy()
            for attr_name, type_cls in types.items():
                if attr_name in new_data.keys():
                    type_obj = type_cls(new_data[attr_name])

                    # if the type if FileAttribute we need to pass the data as
                    # file
                    if issubclass(type_cls, g_types.FileAttribute):
                        k = type_obj.get_file_name(attr_name)
                        files[attr_name] = (k, new_data.pop(attr_name))
                    else:
                        new_data[attr_name] = type_obj.get_for_api()

        http_method = self._get_update_method()
        return http_method(path, post_data=new_data, files=files, **kwargs)


class SetMixin(object):
    @exc.on_http_error(exc.GitlabSetError)
    def set(self, key, value, **kwargs):
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
        return self._obj_cls(self, server_data)


class DeleteMixin(object):
    @exc.on_http_error(exc.GitlabDeleteError)
    def delete(self, id, **kwargs):
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
    pass


class NoUpdateMixin(GetMixin, ListMixin, CreateMixin, DeleteMixin):
    pass


class SaveMixin(object):
    """Mixin for RESTObject's that can be updated."""

    def _get_updated_data(self):
        updated_data = {}
        required, optional = self.manager.get_update_attrs()
        for attr in required:
            # Get everything required, no matter if it's been updated
            updated_data[attr] = getattr(self, attr)
        # Add the updated attributes
        updated_data.update(self._updated_attrs)

        return updated_data

    def save(self, **kwargs):
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
        server_data = self.manager.update(obj_id, updated_data, **kwargs)
        if server_data is not None:
            self._update_attrs(server_data)


class ObjectDeleteMixin(object):
    """Mixin for RESTObject's that can be deleted."""

    def delete(self, **kwargs):
        """Delete the object from the server.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabDeleteError: If the server cannot perform the request
        """
        self.manager.delete(self.get_id())


class UserAgentDetailMixin(object):
    @cli.register_custom_action(("Snippet", "ProjectSnippet", "ProjectIssue"))
    @exc.on_http_error(exc.GitlabGetError)
    def user_agent_detail(self, **kwargs):
        """Get the user agent detail.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabGetError: If the server cannot perform the request
        """
        path = "%s/%s/user_agent_detail" % (self.manager.path, self.get_id())
        return self.manager.gitlab.http_get(path, **kwargs)


class AccessRequestMixin(object):
    @cli.register_custom_action(
        ("ProjectAccessRequest", "GroupAccessRequest"), tuple(), ("access_level",)
    )
    @exc.on_http_error(exc.GitlabUpdateError)
    def approve(self, access_level=gitlab.DEVELOPER_ACCESS, **kwargs):
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
        self._update_attrs(server_data)


class SubscribableMixin(object):
    @cli.register_custom_action(
        ("ProjectIssue", "ProjectMergeRequest", "ProjectLabel", "GroupLabel")
    )
    @exc.on_http_error(exc.GitlabSubscribeError)
    def subscribe(self, **kwargs):
        """Subscribe to the object notifications.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabSubscribeError: If the subscription cannot be done
        """
        path = "%s/%s/subscribe" % (self.manager.path, self.get_id())
        server_data = self.manager.gitlab.http_post(path, **kwargs)
        self._update_attrs(server_data)

    @cli.register_custom_action(
        ("ProjectIssue", "ProjectMergeRequest", "ProjectLabel", "GroupLabel")
    )
    @exc.on_http_error(exc.GitlabUnsubscribeError)
    def unsubscribe(self, **kwargs):
        """Unsubscribe from the object notifications.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabUnsubscribeError: If the unsubscription cannot be done
        """
        path = "%s/%s/unsubscribe" % (self.manager.path, self.get_id())
        server_data = self.manager.gitlab.http_post(path, **kwargs)
        self._update_attrs(server_data)


class TodoMixin(object):
    @cli.register_custom_action(("ProjectIssue", "ProjectMergeRequest"))
    @exc.on_http_error(exc.GitlabTodoError)
    def todo(self, **kwargs):
        """Create a todo associated to the object.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabTodoError: If the todo cannot be set
        """
        path = "%s/%s/todo" % (self.manager.path, self.get_id())
        self.manager.gitlab.http_post(path, **kwargs)


class TimeTrackingMixin(object):
    @cli.register_custom_action(("ProjectIssue", "ProjectMergeRequest"))
    @exc.on_http_error(exc.GitlabTimeTrackingError)
    def time_stats(self, **kwargs):
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
        return self.manager.gitlab.http_get(path, **kwargs)

    @cli.register_custom_action(("ProjectIssue", "ProjectMergeRequest"), ("duration",))
    @exc.on_http_error(exc.GitlabTimeTrackingError)
    def time_estimate(self, duration, **kwargs):
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
        return self.manager.gitlab.http_post(path, post_data=data, **kwargs)

    @cli.register_custom_action(("ProjectIssue", "ProjectMergeRequest"))
    @exc.on_http_error(exc.GitlabTimeTrackingError)
    def reset_time_estimate(self, **kwargs):
        """Resets estimated time for the object to 0 seconds.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabTimeTrackingError: If the time tracking update cannot be done
        """
        path = "%s/%s/reset_time_estimate" % (self.manager.path, self.get_id())
        return self.manager.gitlab.http_post(path, **kwargs)

    @cli.register_custom_action(("ProjectIssue", "ProjectMergeRequest"), ("duration",))
    @exc.on_http_error(exc.GitlabTimeTrackingError)
    def add_spent_time(self, duration, **kwargs):
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
        return self.manager.gitlab.http_post(path, post_data=data, **kwargs)

    @cli.register_custom_action(("ProjectIssue", "ProjectMergeRequest"))
    @exc.on_http_error(exc.GitlabTimeTrackingError)
    def reset_spent_time(self, **kwargs):
        """Resets the time spent working on the object.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabTimeTrackingError: If the time tracking update cannot be done
        """
        path = "%s/%s/reset_spent_time" % (self.manager.path, self.get_id())
        return self.manager.gitlab.http_post(path, **kwargs)


class ParticipantsMixin(object):
    @cli.register_custom_action(("ProjectMergeRequest", "ProjectIssue"))
    @exc.on_http_error(exc.GitlabListError)
    def participants(self, **kwargs):
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
        return self.manager.gitlab.http_get(path, **kwargs)


class BadgeRenderMixin(object):
    @cli.register_custom_action(
        ("GroupBadgeManager", "ProjectBadgeManager"), ("link_url", "image_url")
    )
    @exc.on_http_error(exc.GitlabRenderError)
    def render(self, link_url, image_url, **kwargs):
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
        return self.gitlab.http_get(path, data, **kwargs)

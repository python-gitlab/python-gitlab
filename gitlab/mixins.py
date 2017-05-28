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


class GetMixin(object):
    def get(self, id, **kwargs):
        """Retrieve a single object.

        Args:
            id (int or str): ID of the object to retrieve
            **kwargs: Extra data to send to the Gitlab server (e.g. sudo)

        Returns:
            object: The generated RESTObject.

        Raises:
            GitlabGetError: If the server cannot perform the request.
        """
        path = '%s/%s' % (self.path, id)
        server_data = self.gitlab.http_get(path, **kwargs)
        return self._obj_cls(self, server_data)


class GetWithoutIdMixin(object):
    def get(self, **kwargs):
        """Retrieve a single object.

        Args:
            **kwargs: Extra data to send to the Gitlab server (e.g. sudo)

        Returns:
            object: The generated RESTObject.

        Raises:
            GitlabGetError: If the server cannot perform the request.
        """
        server_data = self.gitlab.http_get(self.path, **kwargs)
        return self._obj_cls(self, server_data)


class ListMixin(object):
    def list(self, **kwargs):
        """Retrieves a list of objects.

        Args:
            **kwargs: Extra data to send to the Gitlab server (e.g. sudo).
                      If ``all`` is passed and set to True, the entire list of
                      objects will be returned.

        Returns:
            RESTObjectList: Generator going through the list of objects, making
                            queries to the server when required.
                            If ``all=True`` is passed as argument, returns
                            list(RESTObjectList).
        """

        # Allow to overwrite the path, handy for custom listings
        path = kwargs.pop('path', self.path)

        obj = self.gitlab.http_list(path, **kwargs)
        if isinstance(obj, list):
            return [self._obj_cls(self, item) for item in obj]
        else:
            return base.RESTObjectList(self, self._obj_cls, obj)


class GetFromListMixin(ListMixin):
    def get(self, id, **kwargs):
        """Retrieve a single object.

        Args:
            id (int or str): ID of the object to retrieve
            **kwargs: Extra data to send to the Gitlab server (e.g. sudo)

        Returns:
            object: The generated RESTObject.

        Raises:
            GitlabGetError: If the server cannot perform the request.
        """
        gen = self.list()
        for obj in gen:
            if str(obj.get_id()) == str(id):
                return obj


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
        """Returns the required and optional arguments.

        Returns:
            tuple: 2 items: list of required arguments and list of optional
                   arguments for creation (in that order)
        """
        return getattr(self, '_create_attrs', (tuple(), tuple()))

    def create(self, data, **kwargs):
        """Creates a new object.

        Args:
            data (dict): parameters to send to the server to create the
                         resource
            **kwargs: Extra data to send to the Gitlab server (e.g. sudo)

        Returns:
            RESTObject: a new instance of the manage object class build with
                        the data sent by the server
        """
        self._check_missing_create_attrs(data)
        if hasattr(self, '_sanitize_data'):
            data = self._sanitize_data(data, 'create')
        # Handle specific URL for creation
        path = kwargs.get('path', self.path)
        server_data = self.gitlab.http_post(path, post_data=data, **kwargs)
        return self._obj_cls(self, server_data)


class UpdateMixin(object):
    def _check_missing_update_attrs(self, data):
        required, optional = self.get_update_attrs()
        missing = []
        for attr in required:
            if attr not in data:
                missing.append(attr)
                continue
        if missing:
            raise AttributeError("Missing attributes: %s" % ", ".join(missing))

    def get_update_attrs(self):
        """Returns the required and optional arguments.

        Returns:
            tuple: 2 items: list of required arguments and list of optional
                   arguments for update (in that order)
        """
        return getattr(self, '_update_attrs', (tuple(), tuple()))

    def update(self, id=None, new_data={}, **kwargs):
        """Update an object on the server.

        Args:
            id: ID of the object to update (can be None if not required)
            new_data: the update data for the object
            **kwargs: Extra data to send to the Gitlab server (e.g. sudo)

        Returns:
            dict: The new object data (*not* a RESTObject)
        """

        if id is None:
            path = self.path
        else:
            path = '%s/%s' % (self.path, id)

        self._check_missing_update_attrs(new_data)
        if hasattr(self, '_sanitize_data'):
            data = self._sanitize_data(new_data, 'update')
        else:
            data = new_data
        server_data = self.gitlab.http_put(path, post_data=data, **kwargs)
        return server_data


class DeleteMixin(object):
    def delete(self, id, **kwargs):
        """Deletes an object on the server.

        Args:
            id: ID of the object to delete
            **kwargs: Extra data to send to the Gitlab server (e.g. sudo)
        """
        path = '%s/%s' % (self.path, id)
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
        """Saves the changes made to the object to the server.

        Args:
            **kwargs: Extra option to send to the server (e.g. sudo)

        The object is updated to match what the server returns.
        """
        updated_data = self._get_updated_data()

        # call the manager
        obj_id = self.get_id()
        server_data = self.manager.update(obj_id, updated_data, **kwargs)
        self._update_attrs(server_data)


class AccessRequestMixin(object):
    def approve(self, access_level=gitlab.DEVELOPER_ACCESS, **kwargs):
        """Approve an access request.

        Attrs:
            access_level (int): The access level for the user.

        Raises:
            GitlabConnectionError: If the server cannot be reached.
            GitlabUpdateError: If the server fails to perform the request.
        """

        path = '%s/%s/approve' % (self.manager.path, self.id)
        data = {'access_level': access_level}
        server_data = self.manager.gitlab.http_put(url, post_data=data,
                                                   **kwargs)
        self._update_attrs(server_data)


class SubscribableMixin(object):
    def subscribe(self, **kwarg):
        """Subscribe to the object notifications.

        raises:
            gitlabconnectionerror: if the server cannot be reached.
            gitlabsubscribeerror: if the subscription cannot be done
        """
        path = '%s/%s/subscribe' % (self.manager.path, self.get_id())
        server_data = self.manager.gitlab.http_post(path, **kwargs)
        self._update_attrs(server_data)

    def unsubscribe(self, **kwargs):
        """Unsubscribe from the object notifications.

        raises:
            gitlabconnectionerror: if the server cannot be reached.
            gitlabunsubscribeerror: if the unsubscription cannot be done
        """
        path = '%s/%s/unsubscribe' % (self.manager.path, self.get_id())
        server_data = self.manager.gitlab.http_post(path, **kwargs)
        self._update_attrs(server_data)


class TodoMixin(object):
    def todo(self, **kwargs):
        """Create a todo associated to the object.

        Raises:
            GitlabConnectionError: If the server cannot be reached.
        """
        path = '%s/%s/todo' % (self.manager.path, self.get_id())
        self.manager.gitlab.http_post(path, **kwargs)


class TimeTrackingMixin(object):
    def time_stats(self, **kwargs):
        """Get time stats for the object.

        Raises:
            GitlabConnectionError: If the server cannot be reached.
        """
        path = '%s/%s/time_stats' % (self.manager.path, self.get_id())
        return self.manager.gitlab.http_get(path, **kwargs)

    def time_estimate(self, duration, **kwargs):
        """Set an estimated time of work for the object.

        Args:
            duration (str): duration in human format (e.g. 3h30)

        Raises:
            GitlabConnectionError: If the server cannot be reached.
        """
        path = '%s/%s/time_estimate' % (self.manager.path, self.get_id())
        data = {'duration': duration}
        return self.manager.gitlab.http_post(path, post_data=data, **kwargs)

    def reset_time_estimate(self, **kwargs):
        """Resets estimated time for the object to 0 seconds.

        Raises:
            GitlabConnectionError: If the server cannot be reached.
        """
        path = '%s/%s/rest_time_estimate' % (self.manager.path, self.get_id())
        return self.manager.gitlab.http_post(path, **kwargs)

    def add_spent_time(self, duration, **kwargs):
        """Add time spent working on the object.

        Args:
            duration (str): duration in human format (e.g. 3h30)

        Raises:
            GitlabConnectionError: If the server cannot be reached.
        """
        path = '%s/%s/add_spent_time' % (self.manager.path, self.get_id())
        data = {'duration': duration}
        return self.manager.gitlab.http_post(path, post_data=data, **kwargs)

    def reset_spent_time(self, **kwargs):
        """Resets the time spent working on the object.

        Raises:
            GitlabConnectionError: If the server cannot be reached.
        """
        path = '%s/%s/reset_spent_time' % (self.manager.path, self.get_id())
        return self.manager.gitlab.http_post(path, **kwargs)

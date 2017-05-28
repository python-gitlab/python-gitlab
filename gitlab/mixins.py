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
        path = '%s/%s' % (self._path, id)
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
        server_data = self.gitlab.http_get(self._path, **kwargs)
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

        obj = self.gitlab.http_list(self._path, **kwargs)
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
    def _check_missing_attrs(self, data):
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
        if hasattr(self, '_create_attrs'):
            return (self._create_attrs['required'],
                    self._create_attrs['optional'])
        return (tuple(), tuple())

    def create(self, data, **kwargs):
        """Created a new object.

        Args:
            data (dict): parameters to send to the server to create the
                         resource
            **kwargs: Extra data to send to the Gitlab server (e.g. sudo)

        Returns:
            RESTObject: a new instance of the manage object class build with
                        the data sent by the server
        """
        self._check_missing_attrs(data)
        if hasattr(self, '_sanitize_data'):
            data = self._sanitize_data(data, 'create')
        server_data = self.gitlab.http_post(self._path, post_data=data, **kwargs)
        return self._obj_cls(self, server_data)


class UpdateMixin(object):
    def _check_missing_attrs(self, data):
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
        if hasattr(self, '_update_attrs'):
            return (self._update_attrs['required'],
                    self._update_attrs['optional'])
        return (tuple(), tuple())

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
            path = self._path
        else:
            path = '%s/%s' % (self._path, id)

        self._check_missing_attrs(new_data)
        if hasattr(self, '_sanitize_data'):
            data = self._sanitize_data(new_data, 'update')
        server_data = self.gitlab.http_put(self._path, post_data=data,
                                           **kwargs)
        return server_data


class DeleteMixin(object):
    def delete(self, id, **kwargs):
        """Deletes an object on the server.

        Args:
            id: ID of the object to delete
            **kwargs: Extra data to send to the Gitlab server (e.g. sudo)
        """
        path = '%s/%s' % (self._path, id)
        self.gitlab.http_delete(path, **kwargs)


class CRUDMixin(GetMixin, ListMixin, CreateMixin, UpdateMixin, DeleteMixin):
    pass

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

import importlib


class RESTObject(object):
    """Represents an object built from server data.

    It holds the attributes know from the server, and the updated attributes in
    another. This allows smart updates, if the object allows it.

    You can redefine ``_id_attr`` in child classes to specify which attribute
    must be used as uniq ID. ``None`` means that the object can be updated
    without ID in the url.
    """

    _id_attr = "id"

    def __init__(self, manager, attrs):
        self.__dict__.update(
            {
                "manager": manager,
                "_attrs": attrs,
                "_updated_attrs": {},
                "_module": importlib.import_module(self.__module__),
            }
        )
        self.__dict__["_parent_attrs"] = self.manager.parent_attrs
        self._create_managers()

    def __getstate__(self):
        state = self.__dict__.copy()
        module = state.pop("_module")
        state["_module_name"] = module.__name__
        return state

    def __setstate__(self, state):
        module_name = state.pop("_module_name")
        self.__dict__.update(state)
        self.__dict__["_module"] = importlib.import_module(module_name)

    def __getattr__(self, name):
        try:
            return self.__dict__["_updated_attrs"][name]
        except KeyError:
            try:
                value = self.__dict__["_attrs"][name]

                # If the value is a list, we copy it in the _updated_attrs dict
                # because we are not able to detect changes made on the object
                # (append, insert, pop, ...). Without forcing the attr
                # creation __setattr__ is never called, the list never ends up
                # in the _updated_attrs dict, and the update() and save()
                # method never push the new data to the server.
                # See https://github.com/python-gitlab/python-gitlab/issues/306
                #
                # note: _parent_attrs will only store simple values (int) so we
                # don't make this check in the next except block.
                if isinstance(value, list):
                    self.__dict__["_updated_attrs"][name] = value[:]
                    return self.__dict__["_updated_attrs"][name]

                return value

            except KeyError:
                try:
                    return self.__dict__["_parent_attrs"][name]
                except KeyError:
                    raise AttributeError(name)

    def __setattr__(self, name, value):
        self.__dict__["_updated_attrs"][name] = value

    def __str__(self):
        data = self._attrs.copy()
        data.update(self._updated_attrs)
        return "%s => %s" % (type(self), data)

    def __repr__(self):
        if self._id_attr:
            return "<%s %s:%s>" % (
                self.__class__.__name__,
                self._id_attr,
                self.get_id(),
            )
        else:
            return "<%s>" % self.__class__.__name__

    def __eq__(self, other):
        if self.get_id() and other.get_id():
            return self.get_id() == other.get_id()
        return super(RESTObject, self) == other

    def __ne__(self, other):
        if self.get_id() and other.get_id():
            return self.get_id() != other.get_id()
        return super(RESTObject, self) != other

    def __hash__(self):
        if not self.get_id():
            return super(RESTObject, self).__hash__()
        return hash(self.get_id())

    def _create_managers(self):
        managers = getattr(self, "_managers", None)
        if managers is None:
            return

        for attr, cls_name in self._managers:
            cls = getattr(self._module, cls_name)
            manager = cls(self.manager.gitlab, parent=self)
            self.__dict__[attr] = manager

    def _update_attrs(self, new_attrs):
        self.__dict__["_updated_attrs"] = {}
        self.__dict__["_attrs"].update(new_attrs)

    def get_id(self):
        """Returns the id of the resource."""
        if self._id_attr is None or not hasattr(self, self._id_attr):
            return None
        return getattr(self, self._id_attr)

    @property
    def attributes(self):
        d = self.__dict__["_updated_attrs"].copy()
        d.update(self.__dict__["_attrs"])
        d.update(self.__dict__["_parent_attrs"])
        return d


class RESTObjectList(object):
    """Generator object representing a list of RESTObject's.

    This generator uses the Gitlab pagination system to fetch new data when
    required.

    Note: you should not instanciate such objects, they are returned by calls
    to RESTManager.list()

    Args:
        manager: Manager to attach to the created objects
        obj_cls: Type of objects to create from the json data
        _list: A GitlabList object
    """

    def __init__(self, manager, obj_cls, _list):
        """Creates an objects list from a GitlabList.

        You should not create objects of this type, but use managers list()
        methods instead.

        Args:
            manager: the RESTManager to attach to the objects
            obj_cls: the class of the created objects
            _list: the GitlabList holding the data
        """
        self.manager = manager
        self._obj_cls = obj_cls
        self._list = _list

    def __iter__(self):
        return self

    def __len__(self):
        return len(self._list)

    def __next__(self):
        return self.next()

    def next(self):
        data = self._list.next()
        return self._obj_cls(self.manager, data)

    @property
    def current_page(self):
        """The current page number."""
        return self._list.current_page

    @property
    def prev_page(self):
        """The next page number.

        If None, the current page is the last.
        """
        return self._list.prev_page

    @property
    def next_page(self):
        """The next page number.

        If None, the current page is the last.
        """
        return self._list.next_page

    @property
    def per_page(self):
        """The number of items per page."""
        return self._list.per_page

    @property
    def total_pages(self):
        """The total number of pages."""
        return self._list.total_pages

    @property
    def total(self):
        """The total number of items."""
        return self._list.total


class RESTManager(object):
    """Base class for CRUD operations on objects.

    Derived class must define ``_path`` and ``_obj_cls``.

    ``_path``: Base URL path on which requests will be sent (e.g. '/projects')
    ``_obj_cls``: The class of objects that will be created
    """

    _path = None
    _obj_cls = None

    def __init__(self, gl, parent=None):
        """REST manager constructor.

        Args:
            gl (Gitlab): :class:`~gitlab.Gitlab` connection to use to make
                         requests.
            parent: REST object to which the manager is attached.
        """
        self.gitlab = gl
        self._parent = parent  # for nested managers
        self._computed_path = self._compute_path()

    @property
    def parent_attrs(self):
        return self._parent_attrs

    def _compute_path(self, path=None):
        self._parent_attrs = {}
        if path is None:
            path = self._path
        if self._parent is None or not hasattr(self, "_from_parent_attrs"):
            return path

        data = {
            self_attr: getattr(self._parent, parent_attr, None)
            for self_attr, parent_attr in self._from_parent_attrs.items()
        }
        self._parent_attrs = data
        return path % data

    @property
    def path(self):
        return self._computed_path

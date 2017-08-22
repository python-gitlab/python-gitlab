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

import copy
import importlib
import itertools
import json
import sys

import six

import gitlab
from gitlab.exceptions import *  # noqa


class jsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, GitlabObject):
            return obj.as_dict()
        elif isinstance(obj, gitlab.Gitlab):
            return {'url': obj._url}
        return json.JSONEncoder.default(self, obj)


class BaseManager(object):
    """Base manager class for API operations.

    Managers provide method to manage GitLab API objects, such as retrieval,
    listing, creation.

    Inherited class must define the ``obj_cls`` attribute.

    Attributes:
        obj_cls (class): class of objects wrapped by this manager.
    """

    obj_cls = None

    def __init__(self, gl, parent=None, args=[]):
        """Constructs a manager.

        Args:
            gl (gitlab.Gitlab): Gitlab object referencing the GitLab server.
            parent (Optional[Manager]): A parent manager.
            args (list): A list of tuples defining a link between the
                parent/child attributes.

        Raises:
            AttributeError: If `obj_cls` is None.
        """
        self.gitlab = gl
        self.args = args
        self.parent = parent

        if self.obj_cls is None:
            raise AttributeError("obj_cls must be defined")

    def _set_parent_args(self, **kwargs):
        args = copy.copy(kwargs)
        if self.parent is not None:
            for attr, parent_attr in self.args:
                args.setdefault(attr, getattr(self.parent, parent_attr))

        return args

    def get(self, id=None, **kwargs):
        """Get a GitLab object.

        Args:
            id: ID of the object to retrieve.
            **kwargs: Additional arguments to send to GitLab.

        Returns:
            object: An object of class `obj_cls`.

        Raises:
            NotImplementedError: If objects cannot be retrieved.
            GitlabGetError: If the server fails to perform the request.
        """
        args = self._set_parent_args(**kwargs)
        if not self.obj_cls.canGet:
            raise NotImplementedError
        if id is None and self.obj_cls.getRequiresId is True:
            raise ValueError('The id argument must be defined.')
        return self.obj_cls.get(self.gitlab, id, **args)

    def list(self, **kwargs):
        """Get a list of GitLab objects.

        Args:
            **kwargs: Additional arguments to send to GitLab.

        Returns:
            list[object]: A list of `obj_cls` objects.

        Raises:
            NotImplementedError: If objects cannot be listed.
            GitlabListError: If the server fails to perform the request.
        """
        args = self._set_parent_args(**kwargs)
        if not self.obj_cls.canList:
            raise NotImplementedError
        return self.obj_cls.list(self.gitlab, **args)

    def create(self, data, **kwargs):
        """Create a new object of class `obj_cls`.

        Args:
            data (dict): The parameters to send to the GitLab server to create
                the object. Required and optional arguments are defined in the
                `requiredCreateAttrs` and `optionalCreateAttrs` of the
                `obj_cls` class.
            **kwargs: Additional arguments to send to GitLab.

        Returns:
            object: A newly create `obj_cls` object.

        Raises:
            NotImplementedError: If objects cannot be created.
            GitlabCreateError: If the server fails to perform the request.
        """
        args = self._set_parent_args(**kwargs)
        if not self.obj_cls.canCreate:
            raise NotImplementedError
        return self.obj_cls.create(self.gitlab, data, **args)

    def delete(self, id, **kwargs):
        """Delete a GitLab object.

        Args:
            id: ID of the object to delete.

        Raises:
            NotImplementedError: If objects cannot be deleted.
            GitlabDeleteError: If the server fails to perform the request.
        """
        args = self._set_parent_args(**kwargs)
        if not self.obj_cls.canDelete:
            raise NotImplementedError
        self.gitlab.delete(self.obj_cls, id, **args)


class GitlabObject(object):
    """Base class for all classes that interface with GitLab."""
    #: Url to use in GitLab for this object
    _url = None
    # Some objects (e.g. merge requests) have different urls for singular and
    # plural
    _urlPlural = None
    _id_in_delete_url = True
    _id_in_update_url = True
    _constructorTypes = None

    #: Tells if GitLab-api allows retrieving single objects.
    canGet = True
    #: Tells if GitLab-api allows listing of objects.
    canList = True
    #: Tells if GitLab-api allows creation of new objects.
    canCreate = True
    #: Tells if GitLab-api allows updating object.
    canUpdate = True
    #: Tells if GitLab-api allows deleting object.
    canDelete = True
    #: Attributes that are required for constructing url.
    requiredUrlAttrs = []
    #: Attributes that are required when retrieving list of objects.
    requiredListAttrs = []
    #: Attributes that are optional when retrieving list of objects.
    optionalListAttrs = []
    #: Attributes that are optional when retrieving single object.
    optionalGetAttrs = []
    #: Attributes that are required when retrieving single object.
    requiredGetAttrs = []
    #: Attributes that are required when deleting object.
    requiredDeleteAttrs = []
    #: Attributes that are required when creating a new object.
    requiredCreateAttrs = []
    #: Attributes that are optional when creating a new object.
    optionalCreateAttrs = []
    #: Attributes that are required when updating an object.
    requiredUpdateAttrs = []
    #: Attributes that are optional when updating an object.
    optionalUpdateAttrs = []
    #: Whether the object ID is required in the GET url.
    getRequiresId = True
    #: List of managers to create.
    managers = []
    #: Name of the identifier of an object.
    idAttr = 'id'
    #: Attribute to use as ID when displaying the object.
    shortPrintAttr = None

    def _data_for_gitlab(self, extra_parameters={}, update=False,
                         as_json=True):
        data = {}
        if update and (self.requiredUpdateAttrs or self.optionalUpdateAttrs):
            attributes = itertools.chain(self.requiredUpdateAttrs,
                                         self.optionalUpdateAttrs)
        else:
            attributes = itertools.chain(self.requiredCreateAttrs,
                                         self.optionalCreateAttrs)
        attributes = list(attributes) + ['sudo', 'page', 'per_page']
        for attribute in attributes:
            if hasattr(self, attribute):
                value = getattr(self, attribute)
                # labels need to be sent as a comma-separated list
                if attribute == 'labels' and isinstance(value, list):
                    value = ", ".join(value)
                elif attribute == 'sudo':
                    value = str(value)
                data[attribute] = value

        data.update(extra_parameters)

        return json.dumps(data) if as_json else data

    @classmethod
    def list(cls, gl, **kwargs):
        """Retrieve a list of objects from GitLab.

        Args:
            gl (gitlab.Gitlab): Gitlab object referencing the GitLab server.
            per_page (int): Maximum number of items to return.
            page (int): ID of the page to return when using pagination.

        Returns:
            list[object]: A list of objects.

        Raises:
            NotImplementedError: If objects can't be listed.
            GitlabListError: If the server cannot perform the request.
        """
        if not cls.canList:
            raise NotImplementedError

        if not cls._url:
            raise NotImplementedError

        return gl.list(cls, **kwargs)

    @classmethod
    def get(cls, gl, id, **kwargs):
        """Retrieve a single object.

        Args:
            gl (gitlab.Gitlab): Gitlab object referencing the GitLab server.
            id (int or str): ID of the object to retrieve.

        Returns:
            object: The found GitLab object.

        Raises:
            NotImplementedError: If objects can't be retrieved.
            GitlabGetError: If the server cannot perform the request.
        """

        if cls.canGet is False:
            raise NotImplementedError
        elif cls.canGet is True:
            return cls(gl, id, **kwargs)
        elif cls.canGet == 'from_list':
            for obj in cls.list(gl, **kwargs):
                obj_id = getattr(obj, obj.idAttr)
                if str(obj_id) == str(id):
                    return obj

            raise GitlabGetError("Object not found")

    def _get_object(self, k, v, **kwargs):
        if self._constructorTypes and k in self._constructorTypes:
            cls = getattr(self._module, self._constructorTypes[k])
            return cls(self.gitlab, v, **kwargs)
        else:
            return v

    def _set_from_dict(self, data, **kwargs):
        if not hasattr(data, 'items'):
            return

        for k, v in data.items():
            # If a k attribute already exists and is a Manager, do nothing (see
            # https://github.com/python-gitlab/python-gitlab/issues/209)
            if isinstance(getattr(self, k, None), BaseManager):
                continue

            if isinstance(v, list):
                self.__dict__[k] = []
                for i in v:
                    self.__dict__[k].append(self._get_object(k, i, **kwargs))
            elif v is None:
                self.__dict__[k] = None
            else:
                self.__dict__[k] = self._get_object(k, v, **kwargs)

    def _create(self, **kwargs):
        if not self.canCreate:
            raise NotImplementedError

        json = self.gitlab.create(self, **kwargs)
        self._set_from_dict(json)
        self._from_api = True

    def _update(self, **kwargs):
        if not self.canUpdate:
            raise NotImplementedError

        json = self.gitlab.update(self, **kwargs)
        self._set_from_dict(json)

    def save(self, **kwargs):
        if self._from_api:
            self._update(**kwargs)
        else:
            self._create(**kwargs)

    def delete(self, **kwargs):
        if not self.canDelete:
            raise NotImplementedError

        if not self._from_api:
            raise GitlabDeleteError("Object not yet created")

        return self.gitlab.delete(self, **kwargs)

    @classmethod
    def create(cls, gl, data, **kwargs):
        """Create an object.

        Args:
            gl (gitlab.Gitlab): Gitlab object referencing the GitLab server.
            data (dict): The data used to define the object.

        Returns:
            object: The new object.

        Raises:
            NotImplementedError: If objects can't be created.
            GitlabCreateError: If the server cannot perform the request.
        """
        if not cls.canCreate:
            raise NotImplementedError

        obj = cls(gl, data, **kwargs)
        obj.save()

        return obj

    def __init__(self, gl, data=None, **kwargs):
        """Constructs a new object.

        Do not use this method. Use the `get` or `create` class methods
        instead.

        Args:
            gl (gitlab.Gitlab): Gitlab object referencing the GitLab server.
            data: If `data` is a dict, create a new object using the
                information. If it is an int or a string, get a GitLab object
                from an API request.
            **kwargs: Additional arguments to send to GitLab.
        """
        self._from_api = False
        #: (gitlab.Gitlab): Gitlab connection.
        self.gitlab = gl

        # store the module in which the object has been created (v3/v4) to be
        # able to reference other objects from the same module
        self._module = importlib.import_module(self.__module__)

        if (data is None or isinstance(data, six.integer_types) or
           isinstance(data, six.string_types)):
            if not self.canGet:
                raise NotImplementedError
            data = self.gitlab.get(self.__class__, data, **kwargs)
            self._from_api = True

            # the API returned a list because custom kwargs where used
            # instead of the id to request an object. Usually parameters
            # other than an id return ambiguous results. However in the
            # gitlab universe iids together with a project_id are
            # unambiguous for merge requests and issues, too.
            # So if there is only one element we can use it as our data
            # source.
            if 'iid' in kwargs and isinstance(data, list):
                if len(data) < 1:
                    raise GitlabGetError('Not found')
                elif len(data) == 1:
                    data = data[0]
                else:
                    raise GitlabGetError('Impossible! You found multiple'
                                         ' elements with the same iid.')

        self._set_from_dict(data, **kwargs)

        if kwargs:
            for k, v in kwargs.items():
                # Don't overwrite attributes returned by the server (#171)
                if k not in self.__dict__ or not self.__dict__[k]:
                    self.__dict__[k] = v

        # Special handling for api-objects that don't have id-number in api
        # responses. Currently only Labels and Files
        if not hasattr(self, "id"):
            self.id = None

    def _set_manager(self, var, cls, attrs):
        manager = cls(self.gitlab, self, attrs)
        setattr(self, var, manager)

    def __getattr__(self, name):
        # build a manager if it doesn't exist yet
        for var, cls, attrs in self.managers:
            if var != name:
                continue
            # Build the full class path if needed
            if isinstance(cls, six.string_types):
                cls = getattr(self._module, cls)
            self._set_manager(var, cls, attrs)
            return getattr(self, var)

        raise AttributeError(name)

    def __str__(self):
        return '%s => %s' % (type(self), str(self.__dict__))

    def __repr__(self):
        return '<%s %s:%s>' % (self.__class__.__name__,
                               self.idAttr,
                               getattr(self, self.idAttr))

    def display(self, pretty):
        if pretty:
            self.pretty_print()
        else:
            self.short_print()

    def short_print(self, depth=0):
        """Print the object on the standard output (verbose).

        Args:
            depth (int): Used internaly for recursive call.
        """
        id = self.__dict__[self.idAttr]
        print("%s%s: %s" % (" " * depth * 2, self.idAttr, id))
        if self.shortPrintAttr:
            print("%s%s: %s" % (" " * depth * 2,
                                self.shortPrintAttr.replace('_', '-'),
                                self.__dict__[self.shortPrintAttr]))

    @staticmethod
    def _get_display_encoding():
        return sys.stdout.encoding or sys.getdefaultencoding()

    @staticmethod
    def _obj_to_str(obj):
        if isinstance(obj, dict):
            s = ", ".join(["%s: %s" %
                          (x, GitlabObject._obj_to_str(y))
                          for (x, y) in obj.items()])
            return "{ %s }" % s
        elif isinstance(obj, list):
            s = ", ".join([GitlabObject._obj_to_str(x) for x in obj])
            return "[ %s ]" % s
        elif six.PY2 and isinstance(obj, six.text_type):
            return obj.encode(GitlabObject._get_display_encoding(), "replace")
        else:
            return str(obj)

    def pretty_print(self, depth=0):
        """Print the object on the standard output (verbose).

        Args:
            depth (int): Used internaly for recursive call.
        """
        id = self.__dict__[self.idAttr]
        print("%s%s: %s" % (" " * depth * 2, self.idAttr, id))
        for k in sorted(self.__dict__.keys()):
            if k in (self.idAttr, 'id', 'gitlab'):
                continue
            if k[0] == '_':
                continue
            v = self.__dict__[k]
            pretty_k = k.replace('_', '-')
            if six.PY2:
                pretty_k = pretty_k.encode(
                    GitlabObject._get_display_encoding(), "replace")
            if isinstance(v, GitlabObject):
                if depth == 0:
                    print("%s:" % pretty_k)
                    v.pretty_print(1)
                else:
                    print("%s: %s" % (pretty_k, v.id))
            elif isinstance(v, BaseManager):
                continue
            else:
                if hasattr(v, __name__) and v.__name__ == 'Gitlab':
                    continue
                v = GitlabObject._obj_to_str(v)
                print("%s%s: %s" % (" " * depth * 2, pretty_k, v))

    def json(self):
        """Dump the object as json.

        Returns:
            str: The json string.
        """
        return json.dumps(self, cls=jsonEncoder)

    def as_dict(self):
        """Dump the object as a dict."""
        return {k: v for k, v in six.iteritems(self.__dict__)
                if (not isinstance(v, BaseManager) and not k[0] == '_')}

    def __eq__(self, other):
        if type(other) is type(self):
            return self.as_dict() == other.as_dict()
        return False

    def __ne__(self, other):
        return not self.__eq__(other)


class RESTObject(object):
    """Represents an object built from server data.

    It holds the attributes know from te server, and the updated attributes in
    another. This allows smart updates, if the object allows it.

    You can redefine ``_id_attr`` in child classes to specify which attribute
    must be used as uniq ID. ``None`` means that the object can be updated
    without ID in the url.
    """
    _id_attr = 'id'

    def __init__(self, manager, attrs):
        self.__dict__.update({
            'manager': manager,
            '_attrs': attrs,
            '_updated_attrs': {},
            '_module': importlib.import_module(self.__module__)
        })
        self.__dict__['_parent_attrs'] = self.manager.parent_attrs

        # TODO(gpocentek): manage the creation of new objects from the received
        # data (_constructor_types)

        self._create_managers()

    def __getattr__(self, name):
        try:
            return self.__dict__['_updated_attrs'][name]
        except KeyError:
            try:
                return self.__dict__['_attrs'][name]
            except KeyError:
                try:
                    return self.__dict__['_parent_attrs'][name]
                except KeyError:
                    raise AttributeError(name)

    def __setattr__(self, name, value):
        self.__dict__['_updated_attrs'][name] = value

    def __str__(self):
        data = self._attrs.copy()
        data.update(self._updated_attrs)
        return '%s => %s' % (type(self), data)

    def __repr__(self):
        if self._id_attr:
            return '<%s %s:%s>' % (self.__class__.__name__,
                                   self._id_attr,
                                   self.get_id())
        else:
            return '<%s>' % self.__class__.__name__

    def _create_managers(self):
        managers = getattr(self, '_managers', None)
        if managers is None:
            return

        for attr, cls_name in self._managers:
            cls = getattr(self._module, cls_name)
            manager = cls(self.manager.gitlab, parent=self)
            self.__dict__[attr] = manager

    def _update_attrs(self, new_attrs):
        self.__dict__['_updated_attrs'] = {}
        self.__dict__['_attrs'].update(new_attrs)

    def get_id(self):
        """Returns the id of the resource."""
        if self._id_attr is None:
            return None
        return getattr(self, self._id_attr)

    @property
    def attributes(self):
        d = self.__dict__['_updated_attrs'].copy()
        d.update(self.__dict__['_attrs'])
        d.update(self.__dict__['_parent_attrs'])
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


class RESTManager(object):
    """Base class for CRUD operations on objects.

    Derivated class must define ``_path`` and ``_obj_cls``.

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
        if self._parent is None or not hasattr(self, '_from_parent_attrs'):
            return path

        data = {self_attr: getattr(self._parent, parent_attr)
                for self_attr, parent_attr in self._from_parent_attrs.items()}
        self._parent_attrs = data
        return path % data

    @property
    def path(self):
        return self._computed_path

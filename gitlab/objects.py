# -*- coding: utf-8 -*-
#
# Copyright (C) 2013-2015 Gauvain Pocentek <gauvain@pocentek.net>
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

from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
import base64
import copy
import itertools
import json
import sys
import warnings

import six

import gitlab
from gitlab.exceptions import *  # noqa
from gitlab import utils


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
                if isinstance(value, list):
                    value = ",".join(value)
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

    def _get_object(self, k, v):
        if self._constructorTypes and k in self._constructorTypes:
            return globals()[self._constructorTypes[k]](self.gitlab, v)
        else:
            return v

    def _set_from_dict(self, data):
        if not hasattr(data, 'items'):
            return

        for k, v in data.items():
            if isinstance(v, list):
                self.__dict__[k] = []
                for i in v:
                    self.__dict__[k].append(self._get_object(k, i))
            elif v is None:
                self.__dict__[k] = None
            else:
                self.__dict__[k] = self._get_object(k, v)

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

        if (data is None or isinstance(data, six.integer_types) or
           isinstance(data, six.string_types)):
            if not self.canGet:
                raise NotImplementedError
            data = self.gitlab.get(self.__class__, data, **kwargs)
            self._from_api = True

        self._set_from_dict(data)

        if kwargs:
            for k, v in kwargs.items():
                self.__dict__[k] = v

        # Special handling for api-objects that don't have id-number in api
        # responses. Currently only Labels and Files
        if not hasattr(self, "id"):
            self.id = None

        self._set_managers()

    def _set_managers(self):
        for var, cls, attrs in self.managers:
            manager = cls(self.gitlab, self, attrs)
            setattr(self, var, manager)

    def __str__(self):
        return '%s => %s' % (type(self), str(self.__dict__))

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


class SidekiqManager(object):
    """Manager for the Sidekiq methods.

    This manager doesn't actually manage objects but provides helper fonction
    for the sidekiq metrics API.
    """
    def __init__(self, gl):
        """Constructs a Sidekiq manager.

        Args:
            gl (gitlab.Gitlab): Gitlab object referencing the GitLab server.
        """
        self.gitlab = gl

    def _simple_get(self, url, **kwargs):
        r = self.gitlab._raw_get(url, **kwargs)
        raise_error_from_response(r, GitlabGetError)
        return r.json()

    def queue_metrics(self, **kwargs):
        """Returns the registred queues information."""
        return self._simple_get('/sidekiq/queue_metrics', **kwargs)

    def process_metrics(self, **kwargs):
        """Returns the registred sidekiq workers."""
        return self._simple_get('/sidekiq/process_metrics', **kwargs)

    def job_stats(self, **kwargs):
        """Returns statistics about the jobs performed."""
        return self._simple_get('/sidekiq/job_stats', **kwargs)

    def compound_metrics(self, **kwargs):
        """Returns all available metrics and statistics."""
        return self._simple_get('/sidekiq/compound_metrics', **kwargs)


class UserEmail(GitlabObject):
    _url = '/users/%(user_id)s/emails'
    canUpdate = False
    shortPrintAttr = 'email'
    requiredUrlAttrs = ['user_id']
    requiredCreateAttrs = ['email']


class UserEmailManager(BaseManager):
    obj_cls = UserEmail


class UserKey(GitlabObject):
    _url = '/users/%(user_id)s/keys'
    canGet = 'from_list'
    canUpdate = False
    requiredUrlAttrs = ['user_id']
    requiredCreateAttrs = ['title', 'key']


class UserKeyManager(BaseManager):
    obj_cls = UserKey


class User(GitlabObject):
    _url = '/users'
    shortPrintAttr = 'username'
    requiredCreateAttrs = ['email', 'username', 'name', 'password']
    optionalCreateAttrs = ['skype', 'linkedin', 'twitter', 'projects_limit',
                           'extern_uid', 'provider', 'bio', 'admin',
                           'can_create_group', 'website_url', 'confirm',
                           'external']
    requiredUpdateAttrs = ['email', 'username', 'name']
    optionalUpdateAttrs = ['password', 'skype', 'linkedin', 'twitter',
                           'projects_limit', 'extern_uid', 'provider', 'bio',
                           'admin', 'can_create_group', 'website_url',
                           'confirm', 'external']
    managers = [
        ('emails', UserEmailManager, [('user_id', 'id')]),
        ('keys', UserKeyManager, [('user_id', 'id')])
    ]

    def _data_for_gitlab(self, extra_parameters={}, update=False,
                         as_json=True):
        if hasattr(self, 'confirm'):
            self.confirm = str(self.confirm).lower()
        return super(User, self)._data_for_gitlab(extra_parameters)

    def block(self, **kwargs):
        """Blocks the user."""
        url = '/users/%s/block' % self.id
        r = self.gitlab._raw_put(url, **kwargs)
        raise_error_from_response(r, GitlabBlockError)
        self.state = 'blocked'

    def unblock(self, **kwargs):
        """Unblocks the user."""
        url = '/users/%s/unblock' % self.id
        r = self.gitlab._raw_put(url, **kwargs)
        raise_error_from_response(r, GitlabUnblockError)
        self.state = 'active'

    def __eq__(self, other):
        if type(other) is type(self):
            selfdict = self.as_dict()
            otherdict = other.as_dict()
            selfdict.pop('password', None)
            otherdict.pop('password', None)
            return selfdict == otherdict
        return False


class UserManager(BaseManager):
    obj_cls = User

    def search(self, query, **kwargs):
        """Search users.

        Args:
            query (str): The query string to send to GitLab for the search.
            all (bool): If True, return all the items, without pagination
            **kwargs: Additional arguments to send to GitLab.

        Returns:
            list(User): A list of matching users.

        Raises:
            GitlabConnectionError: If the server cannot be reached.
            GitlabListError: If the server fails to perform the request.
        """
        url = self.obj_cls._url + '?search=' + query
        return self.gitlab._raw_list(url, self.obj_cls, **kwargs)

    def get_by_username(self, username, **kwargs):
        """Get a user by its username.

        Args:
            username (str): The name of the user.
            **kwargs: Additional arguments to send to GitLab.

        Returns:
            User: The matching user.

        Raises:
            GitlabConnectionError: If the server cannot be reached.
            GitlabGetError: If the server fails to perform the request.
        """
        url = self.obj_cls._url + '?username=' + username
        results = self.gitlab._raw_list(url, self.obj_cls, **kwargs)
        assert len(results) in (0, 1)
        try:
            return results[0]
        except IndexError:
            raise GitlabGetError('no such user: ' + username)


class CurrentUserEmail(GitlabObject):
    _url = '/user/emails'
    canUpdate = False
    shortPrintAttr = 'email'
    requiredCreateAttrs = ['email']


class CurrentUserEmailManager(BaseManager):
    obj_cls = CurrentUserEmail


class CurrentUserKey(GitlabObject):
    _url = '/user/keys'
    canUpdate = False
    shortPrintAttr = 'title'
    requiredCreateAttrs = ['title', 'key']


class CurrentUserKeyManager(BaseManager):
    obj_cls = CurrentUserKey


class CurrentUser(GitlabObject):
    _url = '/user'
    canList = False
    canCreate = False
    canUpdate = False
    canDelete = False
    shortPrintAttr = 'username'
    managers = [
        ('emails', CurrentUserEmailManager, [('user_id', 'id')]),
        ('keys', CurrentUserKeyManager, [('user_id', 'id')])
    ]


class ApplicationSettings(GitlabObject):
    _url = '/application/settings'
    _id_in_update_url = False
    optionalUpdateAttrs = ['after_sign_out_path',
                           'container_registry_token_expire_delay',
                           'default_branch_protection',
                           'default_project_visibility',
                           'default_projects_limit',
                           'default_snippet_visibility',
                           'domain_blacklist',
                           'domain_blacklist_enabled',
                           'domain_whitelist',
                           'enabled_git_access_protocol',
                           'gravatar_enabled',
                           'home_page_url',
                           'max_attachment_size',
                           'repository_storage',
                           'restricted_signup_domains',
                           'restricted_visibility_levels',
                           'session_expire_delay',
                           'sign_in_text',
                           'signin_enabled',
                           'signup_enabled',
                           'twitter_sharing_enabled',
                           'user_oauth_applications']
    canList = False
    canCreate = False
    canDelete = False


class ApplicationSettingsManager(BaseManager):
    obj_cls = ApplicationSettings


class Key(GitlabObject):
    _url = '/deploy_keys'
    canGet = 'from_list'
    canCreate = False
    canUpdate = False
    canDelete = False


class KeyManager(BaseManager):
    obj_cls = Key


class GroupIssue(GitlabObject):
    _url = '/groups/%(group_id)s/issues'
    canGet = 'from_list'
    canCreate = False
    canUpdate = False
    canDelete = False
    requiredUrlAttrs = ['group_id']
    optionalListAttrs = ['state', 'labels', 'milestone', 'order_by', 'sort']


class GroupIssueManager(BaseManager):
    obj_cls = GroupIssue


class GroupMember(GitlabObject):
    _url = '/groups/%(group_id)s/members'
    canGet = 'from_list'
    requiredUrlAttrs = ['group_id']
    requiredCreateAttrs = ['access_level', 'user_id']
    requiredUpdateAttrs = ['access_level']
    shortPrintAttr = 'username'

    def _update(self, **kwargs):
        self.user_id = self.id
        super(GroupMember, self)._update(**kwargs)


class GroupMemberManager(BaseManager):
    obj_cls = GroupMember


class GroupProject(GitlabObject):
    _url = '/groups/%(group_id)s/projects'
    canGet = 'from_list'
    canCreate = False
    canDelete = False
    canUpdate = False
    optionalListAttrs = ['archived', 'visibility', 'order_by', 'sort',
                         'search', 'ci_enabled_first']


class GroupProjectManager(BaseManager):
    obj_cls = GroupProject


class GroupAccessRequest(GitlabObject):
    _url = '/groups/%(group_id)s/access_requests'
    canGet = 'from_list'
    canUpdate = False

    def approve(self, access_level=gitlab.DEVELOPER_ACCESS, **kwargs):
        """Approve an access request.

        Attrs:
            access_level (int): The access level for the user.

        Raises:
            GitlabConnectionError: If the server cannot be reached.
            GitlabUpdateError: If the server fails to perform the request.
        """

        url = ('/groups/%(group_id)s/access_requests/%(id)s/approve' %
               {'group_id': self.group_id, 'id': self.id})
        data = {'access_level': access_level}
        r = self.gitlab._raw_put(url, data=data, **kwargs)
        raise_error_from_response(r, GitlabUpdateError, 201)
        self._set_from_dict(r.json())


class GroupAccessRequestManager(BaseManager):
    obj_cls = GroupAccessRequest


class Group(GitlabObject):
    _url = '/groups'
    _constructorTypes = {'projects': 'Project'}
    requiredCreateAttrs = ['name', 'path']
    optionalCreateAttrs = ['description', 'visibility_level']
    optionalUpdateAttrs = ['name', 'path', 'description', 'visibility_level']
    shortPrintAttr = 'name'
    managers = [
        ('accessrequests', GroupAccessRequestManager, [('group_id', 'id')]),
        ('members', GroupMemberManager, [('group_id', 'id')]),
        ('projects', GroupProjectManager, [('group_id', 'id')]),
        ('issues', GroupIssueManager, [('group_id', 'id')])
    ]

    GUEST_ACCESS = gitlab.GUEST_ACCESS
    REPORTER_ACCESS = gitlab.REPORTER_ACCESS
    DEVELOPER_ACCESS = gitlab.DEVELOPER_ACCESS
    MASTER_ACCESS = gitlab.MASTER_ACCESS
    OWNER_ACCESS = gitlab.OWNER_ACCESS

    VISIBILITY_PRIVATE = gitlab.VISIBILITY_PRIVATE
    VISIBILITY_INTERNAL = gitlab.VISIBILITY_INTERNAL
    VISIBILITY_PUBLIC = gitlab.VISIBILITY_PUBLIC

    def transfer_project(self, id, **kwargs):
        """Transfers a project to this new groups.

        Attrs:
            id (int): ID of the project to transfer.

        Raises:
            GitlabConnectionError: If the server cannot be reached.
            GitlabTransferProjectError: If the server fails to perform the
                request.
        """
        url = '/groups/%d/projects/%d' % (self.id, id)
        r = self.gitlab._raw_post(url, None, **kwargs)
        raise_error_from_response(r, GitlabTransferProjectError, 201)


class GroupManager(BaseManager):
    obj_cls = Group

    def search(self, query, **kwargs):
        """Searches groups by name.

        Args:
            query (str): The search string
            all (bool): If True, return all the items, without pagination

        Returns:
            list(Group): a list of matching groups.
        """
        url = '/groups?search=' + query
        return self.gitlab._raw_list(url, self.obj_cls, **kwargs)


class Hook(GitlabObject):
    _url = '/hooks'
    canUpdate = False
    requiredCreateAttrs = ['url']
    shortPrintAttr = 'url'


class HookManager(BaseManager):
    obj_cls = Hook


class Issue(GitlabObject):
    _url = '/issues'
    _constructorTypes = {'author': 'User', 'assignee': 'User',
                         'milestone': 'ProjectMilestone'}
    canGet = 'from_list'
    canDelete = False
    canUpdate = False
    canCreate = False
    shortPrintAttr = 'title'
    optionalListAttrs = ['state', 'labels', 'order_by', 'sort']


class IssueManager(BaseManager):
    obj_cls = Issue


class License(GitlabObject):
    _url = '/licenses'
    canDelete = False
    canUpdate = False
    canCreate = False
    idAttr = 'key'

    optionalListAttrs = ['popular']
    optionalGetAttrs = ['project', 'fullname']


class LicenseManager(BaseManager):
    obj_cls = License


class Namespace(GitlabObject):
    _url = '/namespaces'
    canGet = 'from_list'
    canUpdate = False
    canDelete = False
    canCreate = False
    optionalListAttrs = ['search']


class NamespaceManager(BaseManager):
    obj_cls = Namespace


class ProjectBranch(GitlabObject):
    _url = '/projects/%(project_id)s/repository/branches'
    _constructorTypes = {'author': 'User', "committer": "User"}

    idAttr = 'name'
    canUpdate = False
    requiredUrlAttrs = ['project_id']
    requiredCreateAttrs = ['branch_name', 'ref']

    def protect(self, protect=True, **kwargs):
        """Protects the project."""
        url = self._url % {'project_id': self.project_id}
        action = 'protect' if protect else 'unprotect'
        url = "%s/%s/%s" % (url, self.name, action)
        r = self.gitlab._raw_put(url, data=None, content_type=None, **kwargs)
        raise_error_from_response(r, GitlabProtectError)

        if protect:
            self.protected = protect
        else:
            del self.protected

    def unprotect(self, **kwargs):
        """Unprotects the project."""
        self.protect(False, **kwargs)


class ProjectBranchManager(BaseManager):
    obj_cls = ProjectBranch


class ProjectBuild(GitlabObject):
    _url = '/projects/%(project_id)s/builds'
    _constructorTypes = {'user': 'User',
                         'commit': 'ProjectCommit',
                         'runner': 'Runner'}
    requiredUrlAttrs = ['project_id']
    canDelete = False
    canUpdate = False
    canCreate = False

    def cancel(self, **kwargs):
        """Cancel the build."""
        url = '/projects/%s/builds/%s/cancel' % (self.project_id, self.id)
        r = self.gitlab._raw_post(url)
        raise_error_from_response(r, GitlabBuildCancelError, 201)

    def retry(self, **kwargs):
        """Retry the build."""
        url = '/projects/%s/builds/%s/retry' % (self.project_id, self.id)
        r = self.gitlab._raw_post(url)
        raise_error_from_response(r, GitlabBuildRetryError, 201)

    def play(self, **kwargs):
        """Trigger a build explicitly."""
        url = '/projects/%s/builds/%s/play' % (self.project_id, self.id)
        r = self.gitlab._raw_post(url)
        raise_error_from_response(r, GitlabBuildPlayError, 201)

    def erase(self, **kwargs):
        """Erase the build (remove build artifacts and trace)."""
        url = '/projects/%s/builds/%s/erase' % (self.project_id, self.id)
        r = self.gitlab._raw_post(url)
        raise_error_from_response(r, GitlabBuildEraseError, 201)

    def keep_artifacts(self, **kwargs):
        """Prevent artifacts from being delete when expiration is set.

        Raises:
            GitlabConnectionError: If the server cannot be reached.
            GitlabCreateError: If the request failed.
        """
        url = ('/projects/%s/builds/%s/artifacts/keep' %
               (self.project_id, self.id))
        r = self.gitlab._raw_post(url)
        raise_error_from_response(r, GitlabGetError, 200)

    def artifacts(self, streamed=False, action=None, chunk_size=1024,
                  **kwargs):
        """Get the build artifacts.

        Args:
            streamed (bool): If True the data will be processed by chunks of
                `chunk_size` and each chunk is passed to `action` for
                treatment.
            action (callable): Callable responsible of dealing with chunk of
                data.
            chunk_size (int): Size of each chunk.

        Returns:
            str: The artifacts if `streamed` is False, None otherwise.

        Raises:
            GitlabConnectionError: If the server cannot be reached.
            GitlabGetError: If the artifacts are not available.
        """
        url = '/projects/%s/builds/%s/artifacts' % (self.project_id, self.id)
        r = self.gitlab._raw_get(url, streamed=streamed, **kwargs)
        raise_error_from_response(r, GitlabGetError, 200)
        return utils.response_content(r, streamed, action, chunk_size)

    def trace(self, streamed=False, action=None, chunk_size=1024, **kwargs):
        """Get the build trace.

        Args:
            streamed (bool): If True the data will be processed by chunks of
                `chunk_size` and each chunk is passed to `action` for
                treatment.
            action (callable): Callable responsible of dealing with chunk of
                data.
            chunk_size (int): Size of each chunk.

        Returns:
            str: The trace.

        Raises:
            GitlabConnectionError: If the server cannot be reached.
            GitlabGetError: If the trace is not available.
        """
        url = '/projects/%s/builds/%s/trace' % (self.project_id, self.id)
        r = self.gitlab._raw_get(url, streamed=streamed, **kwargs)
        raise_error_from_response(r, GitlabGetError, 200)
        return utils.response_content(r, streamed, action, chunk_size)


class ProjectBuildManager(BaseManager):
    obj_cls = ProjectBuild


class ProjectCommitStatus(GitlabObject):
    _url = '/projects/%(project_id)s/repository/commits/%(commit_id)s/statuses'
    _create_url = '/projects/%(project_id)s/statuses/%(commit_id)s'
    canUpdate = False
    canDelete = False
    requiredUrlAttrs = ['project_id', 'commit_id']
    optionalGetAttrs = ['ref_name', 'stage', 'name', 'all']
    requiredCreateAttrs = ['state']
    optionalCreateAttrs = ['description', 'name', 'context', 'ref',
                           'target_url']


class ProjectCommitStatusManager(BaseManager):
    obj_cls = ProjectCommitStatus


class ProjectCommitComment(GitlabObject):
    _url = '/projects/%(project_id)s/repository/commits/%(commit_id)s/comments'
    canUpdate = False
    canGet = False
    canDelete = False
    requiredUrlAttrs = ['project_id', 'commit_id']
    requiredCreateAttrs = ['note']
    optionalCreateAttrs = ['path', 'line', 'line_type']


class ProjectCommitCommentManager(BaseManager):
    obj_cls = ProjectCommitComment


class ProjectCommit(GitlabObject):
    _url = '/projects/%(project_id)s/repository/commits'
    canDelete = False
    canUpdate = False
    canCreate = False
    requiredUrlAttrs = ['project_id']
    shortPrintAttr = 'title'
    managers = [('comments', ProjectCommitCommentManager,
                 [('project_id', 'project_id'), ('commit_id', 'id')]),
                ('statuses', ProjectCommitStatusManager,
                 [('project_id', 'project_id'), ('commit_id', 'id')])]

    def diff(self, **kwargs):
        """Generate the commit diff."""
        url = ('/projects/%(project_id)s/repository/commits/%(commit_id)s/diff'
               % {'project_id': self.project_id, 'commit_id': self.id})
        r = self.gitlab._raw_get(url, **kwargs)
        raise_error_from_response(r, GitlabGetError)

        return r.json()

    def blob(self, filepath, streamed=False, action=None, chunk_size=1024,
             **kwargs):
        """Generate the content of a file for this commit.

        Args:
            filepath (str): Path of the file to request.
            streamed (bool): If True the data will be processed by chunks of
                `chunk_size` and each chunk is passed to `action` for
                treatment.
            action (callable): Callable responsible of dealing with chunk of
                data.
            chunk_size (int): Size of each chunk.

        Returns:
            str: The content of the file

        Raises:
            GitlabConnectionError: If the server cannot be reached.
            GitlabGetError: If the server fails to perform the request.
        """
        url = ('/projects/%(project_id)s/repository/blobs/%(commit_id)s' %
               {'project_id': self.project_id, 'commit_id': self.id})
        url += '?filepath=%s' % filepath
        r = self.gitlab._raw_get(url, streamed=streamed, **kwargs)
        raise_error_from_response(r, GitlabGetError)
        return utils.response_content(r, streamed, action, chunk_size)

    def builds(self, **kwargs):
        """List the build for this commit.

        Returns:
            list(ProjectBuild): A list of builds.

        Raises:
            GitlabConnectionError: If the server cannot be reached.
            GitlabListError: If the server fails to perform the request.
        """
        url = '/projects/%s/repository/commits/%s/builds' % (self.project_id,
                                                             self.id)
        return self.gitlab._raw_list(url, ProjectBuild,
                                     {'project_id': self.project_id},
                                     **kwargs)


class ProjectCommitManager(BaseManager):
    obj_cls = ProjectCommit


class ProjectEnvironment(GitlabObject):
    _url = '/projects/%(project_id)s/environments'
    canGet = 'from_list'
    requiredUrlAttrs = ['project_id']
    requiredCreateAttrs = ['name']
    optionalCreateAttrs = ['external_url']
    optionalUpdateAttrs = ['name', 'external_url']


class ProjectEnvironmentManager(BaseManager):
    obj_cls = ProjectEnvironment


class ProjectKey(GitlabObject):
    _url = '/projects/%(project_id)s/keys'
    canUpdate = False
    requiredUrlAttrs = ['project_id']
    requiredCreateAttrs = ['title', 'key']


class ProjectKeyManager(BaseManager):
    obj_cls = ProjectKey


class ProjectEvent(GitlabObject):
    _url = '/projects/%(project_id)s/events'
    canGet = 'from_list'
    canDelete = False
    canUpdate = False
    canCreate = False
    requiredUrlAttrs = ['project_id']
    shortPrintAttr = 'target_title'


class ProjectEventManager(BaseManager):
    obj_cls = ProjectEvent


class ProjectFork(GitlabObject):
    _url = '/projects/fork/%(project_id)s'
    canUpdate = False
    canDelete = False
    canList = False
    canGet = False
    requiredUrlAttrs = ['project_id']
    optionalCreateAttrs = ['namespace']


class ProjectForkManager(BaseManager):
    obj_cls = ProjectFork


class ProjectHook(GitlabObject):
    _url = '/projects/%(project_id)s/hooks'
    requiredUrlAttrs = ['project_id']
    requiredCreateAttrs = ['url']
    optionalCreateAttrs = ['push_events', 'issues_events', 'note_events',
                           'merge_requests_events', 'tag_push_events',
                           'build_events', 'enable_ssl_verification']
    shortPrintAttr = 'url'


class ProjectHookManager(BaseManager):
    obj_cls = ProjectHook


class ProjectIssueNote(GitlabObject):
    _url = '/projects/%(project_id)s/issues/%(issue_id)s/notes'
    _constructorTypes = {'author': 'User'}
    canDelete = False
    requiredUrlAttrs = ['project_id', 'issue_id']
    requiredCreateAttrs = ['body']


class ProjectIssueNoteManager(BaseManager):
    obj_cls = ProjectIssueNote


class ProjectIssue(GitlabObject):
    _url = '/projects/%(project_id)s/issues/'
    _constructorTypes = {'author': 'User', 'assignee': 'User',
                         'milestone': 'ProjectMilestone'}
    optionalListAttrs = ['state', 'labels', 'milestone', 'iid', 'order_by',
                         'sort']
    requiredUrlAttrs = ['project_id']
    requiredCreateAttrs = ['title']
    optionalCreateAttrs = ['description', 'assignee_id', 'milestone_id',
                           'labels', 'created_at']
    optionalUpdateAttrs = ['title', 'description', 'assignee_id',
                           'milestone_id', 'labels', 'created_at',
                           'state_event']
    shortPrintAttr = 'title'
    managers = [('notes', ProjectIssueNoteManager,
                 [('project_id', 'project_id'), ('issue_id', 'id')])]

    def _data_for_gitlab(self, extra_parameters={}, update=False,
                         as_json=True):
        # Gitlab-api returns labels in a json list and takes them in a
        # comma separated list.
        if hasattr(self, "labels"):
            if (self.labels is not None and
               not isinstance(self.labels, six.string_types)):
                labels = ", ".join(self.labels)
                extra_parameters['labels'] = labels

        return super(ProjectIssue, self)._data_for_gitlab(extra_parameters,
                                                          update)

    def subscribe(self, **kwargs):
        """Subscribe to an issue.

        Raises:
            GitlabConnectionError: If the server cannot be reached.
            GitlabSubscribeError: If the subscription cannot be done
        """
        url = ('/projects/%(project_id)s/issues/%(issue_id)s/subscription' %
               {'project_id': self.project_id, 'issue_id': self.id})

        r = self.gitlab._raw_post(url, **kwargs)
        raise_error_from_response(r, GitlabSubscribeError)
        self._set_from_dict(r.json())

    def unsubscribe(self, **kwargs):
        """Unsubscribe an issue.

        Raises:
            GitlabConnectionError: If the server cannot be reached.
            GitlabUnsubscribeError: If the unsubscription cannot be done
        """
        url = ('/projects/%(project_id)s/issues/%(issue_id)s/subscription' %
               {'project_id': self.project_id, 'issue_id': self.id})

        r = self.gitlab._raw_delete(url, **kwargs)
        raise_error_from_response(r, GitlabUnsubscribeError)
        self._set_from_dict(r.json())

    def move(self, to_project_id, **kwargs):
        """Move the issue to another project.

        Raises:
            GitlabConnectionError: If the server cannot be reached.
        """
        url = ('/projects/%(project_id)s/issues/%(issue_id)s/move' %
               {'project_id': self.project_id, 'issue_id': self.id})

        data = {'to_project_id': to_project_id}
        data.update(**kwargs)
        r = self.gitlab._raw_post(url, data=data)
        raise_error_from_response(r, GitlabUpdateError, 201)
        self._set_from_dict(r.json())

    def todo(self, **kwargs):
        """Create a todo for the issue.

        Raises:
            GitlabConnectionError: If the server cannot be reached.
        """
        url = ('/projects/%(project_id)s/issues/%(issue_id)s/todo' %
               {'project_id': self.project_id, 'issue_id': self.id})
        r = self.gitlab._raw_post(url, **kwargs)
        raise_error_from_response(r, GitlabTodoError, [201, 304])


class ProjectIssueManager(BaseManager):
    obj_cls = ProjectIssue


class ProjectMember(GitlabObject):
    _url = '/projects/%(project_id)s/members'
    requiredUrlAttrs = ['project_id']
    requiredCreateAttrs = ['access_level', 'user_id']
    requiredUpdateAttrs = ['access_level']
    shortPrintAttr = 'username'


class ProjectMemberManager(BaseManager):
    obj_cls = ProjectMember


class ProjectNote(GitlabObject):
    _url = '/projects/%(project_id)s/notes'
    _constructorTypes = {'author': 'User'}
    canUpdate = False
    canDelete = False
    requiredUrlAttrs = ['project_id']
    requiredCreateAttrs = ['body']


class ProjectNoteManager(BaseManager):
    obj_cls = ProjectNote


class ProjectTagRelease(GitlabObject):
    _url = '/projects/%(project_id)s/repository/tags/%(tag_name)/release'
    canDelete = False
    canList = False
    requiredUrlAttrs = ['project_id', 'tag_name']
    requiredCreateAttrs = ['description']
    shortPrintAttr = 'description'


class ProjectTag(GitlabObject):
    _url = '/projects/%(project_id)s/repository/tags'
    _constructorTypes = {'release': 'ProjectTagRelease',
                         'commit': 'ProjectCommit'}
    idAttr = 'name'
    canGet = 'from_list'
    canUpdate = False
    requiredUrlAttrs = ['project_id']
    requiredCreateAttrs = ['tag_name', 'ref']
    optionalCreateAttrs = ['message']
    shortPrintAttr = 'name'

    def set_release_description(self, description):
        """Set the release notes on the tag.

        If the release doesn't exist yet, it will be created. If it already
        exists, its description will be updated.

        Args:
            description (str): Description of the release.

        Raises:
            GitlabConnectionError: If the server cannot be reached.
            GitlabCreateError: If the server fails to create the release.
            GitlabUpdateError: If the server fails to update the release.
        """
        url = '/projects/%s/repository/tags/%s/release' % (self.project_id,
                                                           self.name)
        if self.release is None:
            r = self.gitlab._raw_post(url, data={'description': description})
            raise_error_from_response(r, GitlabCreateError, 201)
        else:
            r = self.gitlab._raw_put(url, data={'description': description})
            raise_error_from_response(r, GitlabUpdateError, 200)
        self.release = ProjectTagRelease(self, r.json())


class ProjectTagManager(BaseManager):
    obj_cls = ProjectTag


class ProjectMergeRequestNote(GitlabObject):
    _url = '/projects/%(project_id)s/merge_requests/%(merge_request_id)s/notes'
    _constructorTypes = {'author': 'User'}
    canDelete = False
    requiredUrlAttrs = ['project_id', 'merge_request_id']
    requiredCreateAttrs = ['body']


class ProjectMergeRequestNoteManager(BaseManager):
    obj_cls = ProjectMergeRequestNote


class ProjectMergeRequest(GitlabObject):
    _url = '/projects/%(project_id)s/merge_requests'
    _constructorTypes = {'author': 'User', 'assignee': 'User'}
    requiredUrlAttrs = ['project_id']
    requiredCreateAttrs = ['source_branch', 'target_branch', 'title']
    optionalCreateAttrs = ['assignee_id', 'description', 'target_project_id',
                           'labels', 'milestone_id']
    optionalUpdateAttrs = ['target_branch', 'assignee_id', 'title',
                           'description', 'state_event', 'labels',
                           'milestone_id']
    optionalListAttrs = ['iid', 'state', 'order_by', 'sort']

    managers = [('notes', ProjectMergeRequestNoteManager,
                 [('project_id', 'project_id'), ('merge_request_id', 'id')])]

    def _data_for_gitlab(self, extra_parameters={}, update=False,
                         as_json=True):
        data = (super(ProjectMergeRequest, self)
                ._data_for_gitlab(extra_parameters, update=update,
                                  as_json=False))
        if update:
            # Drop source_branch attribute as it is not accepted by the gitlab
            # server (Issue #76)
            data.pop('source_branch', None)
        return json.dumps(data)

    def subscribe(self, **kwargs):
        """Subscribe to a MR.

        Raises:
            GitlabConnectionError: If the server cannot be reached.
            GitlabSubscribeError: If the subscription cannot be done
        """
        url = ('/projects/%(project_id)s/merge_requests/%(mr_id)s/'
               'subscription' %
               {'project_id': self.project_id, 'mr_id': self.id})

        r = self.gitlab._raw_post(url, **kwargs)
        raise_error_from_response(r, GitlabSubscribeError, [201, 304])
        if r.status_code == 201:
            self._set_from_dict(r.json())

    def unsubscribe(self, **kwargs):
        """Unsubscribe a MR.

        Raises:
            GitlabConnectionError: If the server cannot be reached.
            GitlabUnsubscribeError: If the unsubscription cannot be done
        """
        url = ('/projects/%(project_id)s/merge_requests/%(mr_id)s/'
               'subscription' %
               {'project_id': self.project_id, 'mr_id': self.id})

        r = self.gitlab._raw_delete(url, **kwargs)
        raise_error_from_response(r, GitlabUnsubscribeError, [200, 304])
        if r.status_code == 200:
            self._set_from_dict(r.json())

    def cancel_merge_when_build_succeeds(self, **kwargs):
        """Cancel merge when build succeeds."""

        u = ('/projects/%s/merge_requests/%s/cancel_merge_when_build_succeeds'
             % (self.project_id, self.id))
        r = self.gitlab._raw_put(u, **kwargs)
        errors = {401: GitlabMRForbiddenError,
                  405: GitlabMRClosedError,
                  406: GitlabMROnBuildSuccessError}
        raise_error_from_response(r, errors)
        return ProjectMergeRequest(self, r.json())

    def closes_issues(self, **kwargs):
        """List issues closed by the MR.

        Returns:
            list (ProjectIssue): List of closed issues

        Raises:
            GitlabConnectionError: If the server cannot be reached.
            GitlabGetError: If the server fails to perform the request.
        """
        url = ('/projects/%s/merge_requests/%s/closes_issues' %
               (self.project_id, self.id))
        return self.gitlab._raw_list(url, ProjectIssue,
                                     {'project_id': self.project_id},
                                     **kwargs)

    def commits(self, **kwargs):
        """List the merge request commits.

        Returns:
            list (ProjectCommit): List of commits

        Raises:
            GitlabConnectionError: If the server cannot be reached.
            GitlabListError: If the server fails to perform the request.
        """
        url = ('/projects/%s/merge_requests/%s/commits' %
               (self.project_id, self.id))
        return self.gitlab._raw_list(url, ProjectCommit,
                                     {'project_id': self.project_id},
                                     **kwargs)

    def changes(self, **kwargs):
        """List the merge request changes.

        Returns:
            list (dict): List of changes

        Raises:
            GitlabConnectionError: If the server cannot be reached.
            GitlabListError: If the server fails to perform the request.
        """
        url = ('/projects/%s/merge_requests/%s/commits' %
               (self.project_id, self.id))
        r = self.gitlab._raw_get(url, **kwargs)
        raise_error_from_response(r, GitlabListError)
        return r.json()

    def merge(self, merge_commit_message=None,
              should_remove_source_branch=False,
              merged_when_build_succeeds=False,
              **kwargs):
        """Accept the merge request.

        Args:
            merge_commit_message (bool): Commit message
            should_remove_source_branch (bool): If True, removes the source
                                                branch
            merged_when_build_succeeds (bool): Wait for the build to succeed,
                                               then merge

        Returns:
            ProjectMergeRequest: The updated MR
        Raises:
            GitlabConnectionError: If the server cannot be reached.
            GitlabMRForbiddenError: If the user doesn't have permission to
                                    close thr MR
            GitlabMRClosedError: If the MR is already closed
        """
        url = '/projects/%s/merge_requests/%s/merge' % (self.project_id,
                                                        self.id)
        data = {}
        if merge_commit_message:
            data['merge_commit_message'] = merge_commit_message
        if should_remove_source_branch:
            data['should_remove_source_branch'] = 'should_remove_source_branch'
        if merged_when_build_succeeds:
            data['merged_when_build_succeeds'] = 'merged_when_build_succeeds'

        r = self.gitlab._raw_put(url, data=data, **kwargs)
        errors = {401: GitlabMRForbiddenError,
                  405: GitlabMRClosedError}
        raise_error_from_response(r, errors)
        self._set_from_dict(r.json())

    def todo(self, **kwargs):
        """Create a todo for the merge request.

        Raises:
            GitlabConnectionError: If the server cannot be reached.
        """
        url = ('/projects/%(project_id)s/merge_requests/%(mr_id)s/todo' %
               {'project_id': self.project_id, 'mr_id': self.id})
        r = self.gitlab._raw_post(url, **kwargs)
        raise_error_from_response(r, GitlabTodoError, [201, 304])


class ProjectMergeRequestManager(BaseManager):
    obj_cls = ProjectMergeRequest


class ProjectMilestone(GitlabObject):
    _url = '/projects/%(project_id)s/milestones'
    canDelete = False
    requiredUrlAttrs = ['project_id']
    optionalListAttrs = ['iid', 'state']
    requiredCreateAttrs = ['title']
    optionalCreateAttrs = ['description', 'due_date', 'state_event']
    optionalUpdateAttrs = requiredCreateAttrs + optionalCreateAttrs
    shortPrintAttr = 'title'

    def issues(self, **kwargs):
        url = "/projects/%s/milestones/%s/issues" % (self.project_id, self.id)
        return self.gitlab._raw_list(url, ProjectIssue,
                                     {'project_id': self.project_id},
                                     **kwargs)


class ProjectMilestoneManager(BaseManager):
    obj_cls = ProjectMilestone


class ProjectLabel(GitlabObject):
    _url = '/projects/%(project_id)s/labels'
    _id_in_delete_url = False
    _id_in_update_url = False
    canGet = 'from_list'
    requiredUrlAttrs = ['project_id']
    idAttr = 'name'
    requiredDeleteAttrs = ['name']
    requiredCreateAttrs = ['name', 'color']
    optionalCreateAttrs = ['description']
    requiredUpdateAttrs = ['name']
    optionalUpdateAttrs = ['new_name', 'color', 'description']

    def subscribe(self, **kwargs):
        """Subscribe to a label.

        Raises:
            GitlabConnectionError: If the server cannot be reached.
            GitlabSubscribeError: If the subscription cannot be done
        """
        url = ('/projects/%(project_id)s/labels/%(label_id)s/subscription' %
               {'project_id': self.project_id, 'label_id': self.name})

        r = self.gitlab._raw_post(url, **kwargs)
        raise_error_from_response(r, GitlabSubscribeError, [201, 304])
        self._set_from_dict(r.json())

    def unsubscribe(self, **kwargs):
        """Unsubscribe a label.

        Raises:
            GitlabConnectionError: If the server cannot be reached.
            GitlabUnsubscribeError: If the unsubscription cannot be done
        """
        url = ('/projects/%(project_id)s/labels/%(label_id)s/subscription' %
               {'project_id': self.project_id, 'label_id': self.name})

        r = self.gitlab._raw_delete(url, **kwargs)
        raise_error_from_response(r, GitlabUnsubscribeError, [200, 304])
        self._set_from_dict(r.json())


class ProjectLabelManager(BaseManager):
    obj_cls = ProjectLabel


class ProjectFile(GitlabObject):
    _url = '/projects/%(project_id)s/repository/files'
    canList = False
    requiredUrlAttrs = ['project_id']
    requiredGetAttrs = ['file_path', 'ref']
    requiredCreateAttrs = ['file_path', 'branch_name', 'content',
                           'commit_message']
    optionalCreateAttrs = ['encoding']
    requiredDeleteAttrs = ['branch_name', 'commit_message', 'file_path']
    shortPrintAttr = 'file_path'
    getRequiresId = False

    def decode(self):
        """Returns the decoded content of the file.

        Returns:
            (str): the decoded content.
        """
        return base64.b64decode(self.content)


class ProjectFileManager(BaseManager):
    obj_cls = ProjectFile


class ProjectPipeline(GitlabObject):
    _url = '/projects/%(project_id)s/pipelines'
    canCreate = False
    canUpdate = False
    canDelete = False

    def retry(self, **kwargs):
        """Retries failed builds in a pipeline.

        Raises:
            GitlabConnectionError: If the server cannot be reached.
            GitlabPipelineRetryError: If the retry cannot be done.
        """
        url = ('/projects/%(project_id)s/pipelines/%(id)s/retry' %
               {'project_id': self.project_id, 'id': self.id})
        r = self.gitlab._raw_post(url, data=None, content_type=None, **kwargs)
        raise_error_from_response(r, GitlabPipelineRetryError, 201)
        self._set_from_dict(r.json())

    def cancel(self, **kwargs):
        """Cancel builds in a pipeline.

        Raises:
            GitlabConnectionError: If the server cannot be reached.
            GitlabPipelineCancelError: If the retry cannot be done.
        """
        url = ('/projects/%(project_id)s/pipelines/%(id)s/cancel' %
               {'project_id': self.project_id, 'id': self.id})
        r = self.gitlab._raw_post(url, data=None, content_type=None, **kwargs)
        raise_error_from_response(r, GitlabPipelineRetryError, 200)
        self._set_from_dict(r.json())


class ProjectPipelineManager(BaseManager):
    obj_cls = ProjectPipeline


class ProjectSnippetNote(GitlabObject):
    _url = '/projects/%(project_id)s/snippets/%(snippet_id)s/notes'
    _constructorTypes = {'author': 'User'}
    canUpdate = False
    canDelete = False
    requiredUrlAttrs = ['project_id', 'snippet_id']
    requiredCreateAttrs = ['body']


class ProjectSnippetNoteManager(BaseManager):
    obj_cls = ProjectSnippetNote


class ProjectSnippet(GitlabObject):
    _url = '/projects/%(project_id)s/snippets'
    _constructorTypes = {'author': 'User'}
    requiredUrlAttrs = ['project_id']
    requiredCreateAttrs = ['title', 'file_name', 'code']
    optionalCreateAttrs = ['lifetime', 'visibility_level']
    optionalUpdateAttrs = ['title', 'file_name', 'code', 'visibility_level']
    shortPrintAttr = 'title'
    managers = [('notes', ProjectSnippetNoteManager,
                 [('project_id', 'project_id'), ('snippet_id', 'id')])]

    def Content(self, **kwargs):
        warnings.warn("`Content` is deprecated, use `content` instead",
                      DeprecationWarning)
        return self.content()

    def content(self, streamed=False, action=None, chunk_size=1024, **kwargs):
        """Return the raw content of a snippet.

        Args:
            streamed (bool): If True the data will be processed by chunks of
                `chunk_size` and each chunk is passed to `action` for
                treatment.
            action (callable): Callable responsible of dealing with chunk of
                data.
            chunk_size (int): Size of each chunk.

        Returns:
            str: The snippet content

        Raises:
            GitlabConnectionError: If the server cannot be reached.
            GitlabGetError: If the server fails to perform the request.
        """
        url = ("/projects/%(project_id)s/snippets/%(snippet_id)s/raw" %
               {'project_id': self.project_id, 'snippet_id': self.id})
        r = self.gitlab._raw_get(url, **kwargs)
        raise_error_from_response(r, GitlabGetError)
        return utils.response_content(r, streamed, action, chunk_size)


class ProjectSnippetManager(BaseManager):
    obj_cls = ProjectSnippet


class ProjectTrigger(GitlabObject):
    _url = '/projects/%(project_id)s/triggers'
    canUpdate = False
    idAttr = 'token'
    requiredUrlAttrs = ['project_id']


class ProjectTriggerManager(BaseManager):
    obj_cls = ProjectTrigger


class ProjectVariable(GitlabObject):
    _url = '/projects/%(project_id)s/variables'
    idAttr = 'key'
    requiredUrlAttrs = ['project_id']
    requiredCreateAttrs = ['key', 'value']


class ProjectVariableManager(BaseManager):
    obj_cls = ProjectVariable


class ProjectService(GitlabObject):
    _url = '/projects/%(project_id)s/services/%(service_name)s'
    canList = False
    canCreate = False
    _id_in_update_url = False
    _id_in_delete_url = False
    requiredUrlAttrs = ['project_id', 'service_name']

    _service_attrs = {
        'asana': (('api_key', ), ('restrict_to_branch', )),
        'assembla': (('token', ), ('subdomain', )),
        'bamboo': (('bamboo_url', 'build_key', 'username', 'password'),
                   tuple()),
        'buildkite': (('token', 'project_url'), ('enable_ssl_verification', )),
        'campfire': (('token', ), ('subdomain', 'room')),
        'custom-issue-tracker': (('new_issue_url', 'issues_url',
                                  'project_url'),
                                 ('description', 'title')),
        'drone-ci': (('token', 'drone_url'), ('enable_ssl_verification', )),
        'emails-on-push': (('recipients', ), ('disable_diffs',
                                              'send_from_committer_email')),
        'external-wiki': (('external_wiki_url', ), tuple()),
        'flowdock': (('token', ), tuple()),
        'gemnasium': (('api_key', 'token', ), tuple()),
        'hipchat': (('token', ), ('color', 'notify', 'room', 'api_version',
                                  'server')),
        'irker': (('recipients', ), ('default_irc_uri', 'server_port',
                                     'server_host', 'colorize_messages')),
        'jira': (('new_issue_url', 'project_url', 'issues_url'),
                 ('api_url', 'description', 'username', 'password')),
        'pivotaltracker': (('token', ), tuple()),
        'pushover': (('api_key', 'user_key', 'priority'), ('device', 'sound')),
        'redmine': (('new_issue_url', 'project_url', 'issues_url'),
                    ('description', )),
        'slack': (('webhook', ), ('username', 'channel')),
        'teamcity': (('teamcity_url', 'build_type', 'username', 'password'),
                     tuple())
    }

    def _data_for_gitlab(self, extra_parameters={}, update=False,
                         as_json=True):
        data = (super(ProjectService, self)
                ._data_for_gitlab(extra_parameters, update=update,
                                  as_json=False))
        missing = []
        # Mandatory args
        for attr in self._service_attrs[self.service_name][0]:
            if not hasattr(self, attr):
                missing.append(attr)
            else:
                data[attr] = getattr(self, attr)

        if missing:
            raise GitlabUpdateError('Missing attribute(s): %s' %
                                    ", ".join(missing))

        # Optional args
        for attr in self._service_attrs[self.service_name][1]:
            if hasattr(self, attr):
                data[attr] = getattr(self, attr)

        return json.dumps(data)


class ProjectServiceManager(BaseManager):
    obj_cls = ProjectService

    def available(self, **kwargs):
        """List the services known by python-gitlab.

        Returns:
            list (str): The list of service code names.
        """
        return json.dumps(ProjectService._service_attrs.keys())


class ProjectAccessRequest(GitlabObject):
    _url = '/projects/%(project_id)s/access_requests'
    canGet = 'from_list'
    canUpdate = False

    def approve(self, access_level=gitlab.DEVELOPER_ACCESS, **kwargs):
        """Approve an access request.

        Attrs:
            access_level (int): The access level for the user.

        Raises:
            GitlabConnectionError: If the server cannot be reached.
            GitlabUpdateError: If the server fails to perform the request.
        """

        url = ('/projects/%(project_id)s/access_requests/%(id)s/approve' %
               {'project_id': self.project_id, 'id': self.id})
        data = {'access_level': access_level}
        r = self.gitlab._raw_put(url, data=data, **kwargs)
        raise_error_from_response(r, GitlabUpdateError, 201)
        self._set_from_dict(r.json())


class ProjectAccessRequestManager(BaseManager):
    obj_cls = ProjectAccessRequest


class ProjectDeployment(GitlabObject):
    _url = '/projects/%(project_id)s/deployments'
    canCreate = False
    canUpdate = False
    canDelete = False


class ProjectDeploymentManager(BaseManager):
    obj_cls = ProjectDeployment


class Project(GitlabObject):
    _url = '/projects'
    _constructorTypes = {'owner': 'User', 'namespace': 'Group'}
    requiredCreateAttrs = ['name']
    optionalCreateAttrs = ['default_branch', 'issues_enabled', 'wall_enabled',
                           'merge_requests_enabled', 'wiki_enabled',
                           'snippets_enabled', 'container_registry_enabled',
                           'public', 'visibility_level', 'namespace_id',
                           'description', 'path', 'import_url',
                           'builds_enabled', 'public_builds',
                           'only_allow_merge_if_build_succeeds']
    optionalUpdateAttrs = ['name', 'default_branch', 'issues_enabled',
                           'wall_enabled', 'merge_requests_enabled',
                           'wiki_enabled', 'snippets_enabled',
                           'container_registry_enabled', 'public',
                           'visibility_level', 'namespace_id', 'description',
                           'path', 'import_url', 'builds_enabled',
                           'public_builds',
                           'only_allow_merge_if_build_succeeds']
    shortPrintAttr = 'path'
    managers = [
        ('accessrequests', ProjectAccessRequestManager,
         [('project_id', 'id')]),
        ('branches', ProjectBranchManager, [('project_id', 'id')]),
        ('builds', ProjectBuildManager, [('project_id', 'id')]),
        ('commits', ProjectCommitManager, [('project_id', 'id')]),
        ('commit_comments', ProjectCommitCommentManager,
         [('project_id', 'id')]),
        ('commit_statuses', ProjectCommitStatusManager,
         [('project_id', 'id')]),
        ('deployments', ProjectDeploymentManager, [('project_id', 'id')]),
        ('environments', ProjectEnvironmentManager, [('project_id', 'id')]),
        ('events', ProjectEventManager, [('project_id', 'id')]),
        ('files', ProjectFileManager, [('project_id', 'id')]),
        ('forks', ProjectForkManager, [('project_id', 'id')]),
        ('hooks', ProjectHookManager, [('project_id', 'id')]),
        ('keys', ProjectKeyManager, [('project_id', 'id')]),
        ('issues', ProjectIssueManager, [('project_id', 'id')]),
        ('labels', ProjectLabelManager, [('project_id', 'id')]),
        ('members', ProjectMemberManager, [('project_id', 'id')]),
        ('mergerequests', ProjectMergeRequestManager, [('project_id', 'id')]),
        ('milestones', ProjectMilestoneManager, [('project_id', 'id')]),
        ('notes', ProjectNoteManager, [('project_id', 'id')]),
        ('pipelines', ProjectPipelineManager, [('project_id', 'id')]),
        ('services', ProjectServiceManager, [('project_id', 'id')]),
        ('snippets', ProjectSnippetManager, [('project_id', 'id')]),
        ('tags', ProjectTagManager, [('project_id', 'id')]),
        ('triggers', ProjectTriggerManager, [('project_id', 'id')]),
        ('variables', ProjectVariableManager, [('project_id', 'id')]),
    ]

    VISIBILITY_PRIVATE = gitlab.VISIBILITY_PRIVATE
    VISIBILITY_INTERNAL = gitlab.VISIBILITY_INTERNAL
    VISIBILITY_PUBLIC = gitlab.VISIBILITY_PUBLIC

    def tree(self, path='', ref_name='', **kwargs):
        warnings.warn("`tree` is deprecated, use `repository_tree` instead",
                      DeprecationWarning)
        return self.repository_tree(path, ref_name, **kwargs)

    def repository_tree(self, path='', ref_name='', **kwargs):
        """Return a list of files in the repository.

        Args:
            path (str): Path of the top folder (/ by default)
            ref_name (str): Reference to a commit or branch

        Returns:
            str: The json representation of the tree.

        Raises:
            GitlabConnectionError: If the server cannot be reached.
            GitlabGetError: If the server fails to perform the request.
        """
        url = "/projects/%s/repository/tree" % (self.id)
        params = []
        if path:
            params.append("path=%s" % path)
        if ref_name:
            params.append("ref_name=%s" % ref_name)
        if params:
            url += '?' + "&".join(params)
        r = self.gitlab._raw_get(url, **kwargs)
        raise_error_from_response(r, GitlabGetError)
        return r.json()

    def blob(self, sha, filepath, **kwargs):
        warnings.warn("`blob` is deprecated, use `repository_blob` instead",
                      DeprecationWarning)
        return self.repository_blob(sha, filepath, **kwargs)

    def repository_blob(self, sha, filepath, streamed=False, action=None,
                        chunk_size=1024, **kwargs):
        """Return the content of a file for a commit.

        Args:
            sha (str): ID of the commit
            filepath (str): Path of the file to return
            streamed (bool): If True the data will be processed by chunks of
                `chunk_size` and each chunk is passed to `action` for
                treatment.
            action (callable): Callable responsible of dealing with chunk of
                data.
            chunk_size (int): Size of each chunk.

        Returns:
            str: The file content

        Raises:
            GitlabConnectionError: If the server cannot be reached.
            GitlabGetError: If the server fails to perform the request.
        """
        url = "/projects/%s/repository/blobs/%s" % (self.id, sha)
        url += '?filepath=%s' % (filepath)
        r = self.gitlab._raw_get(url, streamed=streamed, **kwargs)
        raise_error_from_response(r, GitlabGetError)
        return utils.response_content(r, streamed, action, chunk_size)

    def repository_raw_blob(self, sha, streamed=False, action=None,
                            chunk_size=1024, **kwargs):
        """Returns the raw file contents for a blob by blob SHA.

        Args:
            sha(str): ID of the blob
            streamed (bool): If True the data will be processed by chunks of
                `chunk_size` and each chunk is passed to `action` for
                treatment.
            action (callable): Callable responsible of dealing with chunk of
                data.
            chunk_size (int): Size of each chunk.

        Returns:
            str: The blob content

        Raises:
            GitlabConnectionError: If the server cannot be reached.
            GitlabGetError: If the server fails to perform the request.
        """
        url = "/projects/%s/repository/raw_blobs/%s" % (self.id, sha)
        r = self.gitlab._raw_get(url, streamed=streamed, **kwargs)
        raise_error_from_response(r, GitlabGetError)
        return utils.response_content(r, streamed, action, chunk_size)

    def repository_compare(self, from_, to, **kwargs):
        """Returns a diff between two branches/commits.

        Args:
            from_(str): orig branch/SHA
            to(str): dest branch/SHA

        Returns:
            str: The diff

        Raises:
            GitlabConnectionError: If the server cannot be reached.
            GitlabGetError: If the server fails to perform the request.
        """
        url = "/projects/%s/repository/compare" % self.id
        url = "%s?from=%s&to=%s" % (url, from_, to)
        r = self.gitlab._raw_get(url, **kwargs)
        raise_error_from_response(r, GitlabGetError)
        return r.json()

    def repository_contributors(self):
        """Returns a list of contributors for the project.

        Returns:
            list: The contibutors

        Raises:
            GitlabConnectionError: If the server cannot be reached.
            GitlabGetError: If the server fails to perform the request.
        """
        url = "/projects/%s/repository/contributors" % self.id
        r = self.gitlab._raw_get(url)
        raise_error_from_response(r, GitlabListError)
        return r.json()

    def archive(self, sha=None, **kwargs):
        warnings.warn("`archive` is deprecated, "
                      "use `repository_archive` instead",
                      DeprecationWarning)
        return self.repository_archive(sha, **kwargs)

    def repository_archive(self, sha=None, streamed=False, action=None,
                           chunk_size=1024, **kwargs):
        """Return a tarball of the repository.

        Args:
            sha (str): ID of the commit (default branch by default).
            streamed (bool): If True the data will be processed by chunks of
                `chunk_size` and each chunk is passed to `action` for
                treatment.
            action (callable): Callable responsible of dealing with chunk of
                data.
            chunk_size (int): Size of each chunk.

        Returns:
            str: The binary data of the archive.

        Raises:
            GitlabConnectionError: If the server cannot be reached.
            GitlabGetError: If the server fails to perform the request.
        """
        url = '/projects/%s/repository/archive' % self.id
        if sha:
            url += '?sha=%s' % sha
        r = self.gitlab._raw_get(url, streamed=streamed, **kwargs)
        raise_error_from_response(r, GitlabGetError)
        return utils.response_content(r, streamed, action, chunk_size)

    def create_file(self, path, branch, content, message, **kwargs):
        """Creates file in project repository

        Args:
            path (str): Full path to new file.
            branch (str): The name of branch.
            content (str): Content of the file.
            message (str): Commit message.
            **kwargs: Arbitrary keyword arguments.

        Raises:
            GitlabConnectionError: If the server cannot be reached.
            GitlabCreateError: If the server fails to perform the request.
        """
        warnings.warn("`create_file` is deprecated, "
                      "use `files.create()` instead",
                      DeprecationWarning)
        url = "/projects/%s/repository/files" % self.id
        url += ("?file_path=%s&branch_name=%s&content=%s&commit_message=%s" %
                (path, branch, content, message))
        r = self.gitlab._raw_post(url, data=None, content_type=None, **kwargs)
        raise_error_from_response(r, GitlabCreateError, 201)

    def update_file(self, path, branch, content, message, **kwargs):
        warnings.warn("`update_file` is deprecated, "
                      "use `files.update()` instead",
                      DeprecationWarning)
        url = "/projects/%s/repository/files" % self.id
        url += ("?file_path=%s&branch_name=%s&content=%s&commit_message=%s" %
                (path, branch, content, message))
        r = self.gitlab._raw_put(url, data=None, content_type=None, **kwargs)
        raise_error_from_response(r, GitlabUpdateError)

    def delete_file(self, path, branch, message, **kwargs):
        warnings.warn("`delete_file` is deprecated, "
                      "use `files.delete()` instead",
                      DeprecationWarning)
        url = "/projects/%s/repository/files" % self.id
        url += ("?file_path=%s&branch_name=%s&commit_message=%s" %
                (path, branch, message))
        r = self.gitlab._raw_delete(url, **kwargs)
        raise_error_from_response(r, GitlabDeleteError)

    def create_fork_relation(self, forked_from_id):
        """Create a forked from/to relation between existing projects.

        Args:
            forked_from_id (int): The ID of the project that was forked from

        Raises:
            GitlabConnectionError: If the server cannot be reached.
            GitlabCreateError: If the server fails to perform the request.
        """
        url = "/projects/%s/fork/%s" % (self.id, forked_from_id)
        r = self.gitlab._raw_post(url)
        raise_error_from_response(r, GitlabCreateError, 201)

    def delete_fork_relation(self):
        """Delete a forked relation between existing projects.

        Raises:
            GitlabConnectionError: If the server cannot be reached.
            GitlabDeleteError: If the server fails to perform the request.
        """
        url = "/projects/%s/fork" % self.id
        r = self.gitlab._raw_delete(url)
        raise_error_from_response(r, GitlabDeleteError)

    def star(self, **kwargs):
        """Star a project.

        Returns:
            Project: the updated Project

        Raises:
            GitlabCreateError: If the action cannot be done
            GitlabConnectionError: If the server cannot be reached.
        """
        url = "/projects/%s/star" % self.id
        r = self.gitlab._raw_post(url, **kwargs)
        raise_error_from_response(r, GitlabCreateError, [201, 304])
        return Project(self.gitlab, r.json()) if r.status_code == 201 else self

    def unstar(self, **kwargs):
        """Unstar a project.

        Returns:
            Project: the updated Project

        Raises:
            GitlabDeleteError: If the action cannot be done
            GitlabConnectionError: If the server cannot be reached.
        """
        url = "/projects/%s/star" % self.id
        r = self.gitlab._raw_delete(url, **kwargs)
        raise_error_from_response(r, GitlabDeleteError, [200, 304])
        return Project(self.gitlab, r.json()) if r.status_code == 200 else self

    def archive_(self, **kwargs):
        """Archive a project.

        Returns:
            Project: the updated Project

        Raises:
            GitlabCreateError: If the action cannot be done
            GitlabConnectionError: If the server cannot be reached.
        """
        url = "/projects/%s/archive" % self.id
        r = self.gitlab._raw_post(url, **kwargs)
        raise_error_from_response(r, GitlabCreateError, 201)
        return Project(self.gitlab, r.json()) if r.status_code == 201 else self

    def unarchive_(self, **kwargs):
        """Unarchive a project.

        Returns:
            Project: the updated Project

        Raises:
            GitlabDeleteError: If the action cannot be done
            GitlabConnectionError: If the server cannot be reached.
        """
        url = "/projects/%s/unarchive" % self.id
        r = self.gitlab._raw_delete(url, **kwargs)
        raise_error_from_response(r, GitlabCreateError, 201)
        return Project(self.gitlab, r.json()) if r.status_code == 201 else self

    def share(self, group_id, group_access, **kwargs):
        """Share the project with a group.

        Args:
            group_id (int): ID of the group.
            group_access (int): Access level for the group.

        Raises:
            GitlabConnectionError: If the server cannot be reached.
            GitlabCreateError: If the server fails to perform the request.
        """
        url = "/projects/%s/share" % self.id
        data = {'group_id': group_id, 'group_access': group_access}
        r = self.gitlab._raw_post(url, data=data, **kwargs)
        raise_error_from_response(r, GitlabCreateError, 201)


class Runner(GitlabObject):
    _url = '/runners'
    canCreate = False
    optionalUpdateAttrs = ['description', 'active', 'tag_list']


class RunnerManager(BaseManager):
    obj_cls = Runner

    def all(self, scope=None, **kwargs):
        """List all the runners.

        Args:
            scope (str): The scope of runners to show, one of: specific,
                shared, active, paused, online

        Returns:
            list(Runner): a list of runners matching the scope.

        Raises:
            GitlabConnectionError: If the server cannot be reached.
            GitlabListError: If the resource cannot be found
        """
        url = '/runners/all'
        if scope is not None:
            url += '?scope=' + scope
        return self.gitlab._raw_list(url, self.obj_cls, **kwargs)


class TeamMember(GitlabObject):
    _url = '/user_teams/%(team_id)s/members'
    canUpdate = False
    requiredUrlAttrs = ['teamd_id']
    requiredCreateAttrs = ['access_level']
    shortPrintAttr = 'username'


class Todo(GitlabObject):
    _url = '/todos'
    canGet = 'from_list'
    canUpdate = False
    canCreate = False
    optionalListAttrs = ['action', 'author_id', 'project_id', 'state', 'type']


class TodoManager(BaseManager):
    obj_cls = Todo

    def delete_all(self, **kwargs):
        """Mark all the todos as done.

        Raises:
            GitlabConnectionError: If the server cannot be reached.
            GitlabDeleteError: If the resource cannot be found

        Returns:
            The number of todos maked done.
        """
        url = '/todos'
        r = self.gitlab._raw_delete(url, **kwargs)
        raise_error_from_response(r, GitlabDeleteError)
        return int(r.text)


class UserProject(GitlabObject):
    _url = '/projects/user/%(user_id)s'
    _constructorTypes = {'owner': 'User', 'namespace': 'Group'}
    canUpdate = False
    canDelete = False
    canList = False
    canGet = False
    requiredUrlAttrs = ['user_id']
    requiredCreateAttrs = ['name']
    optionalCreateAttrs = ['default_branch', 'issues_enabled', 'wall_enabled',
                           'merge_requests_enabled', 'wiki_enabled',
                           'snippets_enabled', 'public', 'visibility_level',
                           'description', 'builds_enabled', 'public_builds',
                           'import_url', 'only_allow_merge_if_build_succeeds']


class ProjectManager(BaseManager):
    obj_cls = Project

    def search(self, query, **kwargs):
        """Search projects by name.

        .. note::

           The search is only performed on the project name (not on the
           namespace or the description). To perform a smarter search, use the
           ``search`` argument of the ``list()`` method:

           .. code-block:: python

               gl.projects.list(search=your_search_string)

        Args:
            query (str): The query string to send to GitLab for the search.
            all (bool): If True, return all the items, without pagination
            **kwargs: Additional arguments to send to GitLab.

        Returns:
            list(gitlab.Gitlab.Project): A list of matching projects.
        """
        return self.gitlab._raw_list("/projects/search/" + query, Project,
                                     **kwargs)

    def all(self, **kwargs):
        """List all the projects (need admin rights).

        Args:
            all (bool): If True, return all the items, without pagination
            **kwargs: Additional arguments to send to GitLab.

        Returns:
            list(gitlab.Gitlab.Project): The list of projects.
        """
        return self.gitlab._raw_list("/projects/all", Project, **kwargs)

    def owned(self, **kwargs):
        """List owned projects.

        Args:
            all (bool): If True, return all the items, without pagination
            **kwargs: Additional arguments to send to GitLab.

        Returns:
            list(gitlab.Gitlab.Project): The list of owned projects.
        """
        return self.gitlab._raw_list("/projects/owned", Project, **kwargs)

    def starred(self, **kwargs):
        """List starred projects.

        Args:
            all (bool): If True, return all the items, without pagination
            **kwargs: Additional arguments to send to GitLab.

        Returns:
            list(gitlab.Gitlab.Project): The list of starred projects.
        """
        return self.gitlab._raw_list("/projects/starred", Project, **kwargs)


class UserProjectManager(BaseManager):
    obj_cls = UserProject


class TeamMemberManager(BaseManager):
    obj_cls = TeamMember


class TeamProject(GitlabObject):
    _url = '/user_teams/%(team_id)s/projects'
    _constructorTypes = {'owner': 'User', 'namespace': 'Group'}
    canUpdate = False
    requiredCreateAttrs = ['greatest_access_level']
    requiredUrlAttrs = ['team_id']
    shortPrintAttr = 'name'


class TeamProjectManager(BaseManager):
    obj_cls = TeamProject


class Team(GitlabObject):
    _url = '/user_teams'
    shortPrintAttr = 'name'
    requiredCreateAttrs = ['name', 'path']
    canUpdate = False
    managers = [
        ('members', TeamMemberManager, [('team_id', 'id')]),
        ('projects', TeamProjectManager, [('team_id', 'id')])
    ]


class TeamManager(BaseManager):
    obj_cls = Team

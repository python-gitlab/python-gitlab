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


class jsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, GitlabObject):
            return {k: v for k, v in six.iteritems(obj.__dict__)
                    if (not isinstance(v, BaseManager)
                        and not k[0] == '_')}
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

    def _custom_list(self, url, cls, **kwargs):
        r = self.gitlab._raw_get(url, **kwargs)
        raise_error_from_response(r, GitlabListError)

        l = []
        for j in r.json():
            o = cls(self, j)
            o._from_api = True
            l.append(o)

        return l


class GitlabObject(object):
    """Base class for all classes that interface with GitLab."""
    #: Url to use in GitLab for this object
    _url = None
    # Some objects (e.g. merge requests) have different urls for singular and
    # plural
    _urlPlural = None
    _id_in_delete_url = True
    _id_in_update_url = True
    _returnClass = None
    _constructorTypes = None

    #: Whether _get_list_or_object should return list or object when id is None
    getListWhenNoId = True
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

    def _data_for_gitlab(self, extra_parameters={}, update=False):
        data = {}
        if update and (self.requiredUpdateAttrs or self.optionalUpdateAttrs):
            attributes = itertools.chain(self.requiredUpdateAttrs,
                                         self.optionalUpdateAttrs)
        else:
            attributes = itertools.chain(self.requiredCreateAttrs,
                                         self.optionalCreateAttrs)
        for attribute in attributes:
            if hasattr(self, attribute):
                data[attribute] = getattr(self, attribute)

        data.update(extra_parameters)

        return json.dumps(data)

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

    @classmethod
    def _get_list_or_object(cls, gl, id, **kwargs):
        if id is None and cls.getListWhenNoId:
            return cls.list(gl, **kwargs)
        else:
            return cls.get(gl, id, **kwargs)

    def _get_object(self, k, v):
        if self._constructorTypes and k in self._constructorTypes:
            return globals()[self._constructorTypes[k]](self.gitlab, v)
        else:
            return v

    def _set_from_dict(self, data):
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
                           'can_create_group', 'website_url', 'confirm']
    requiredUpdateAttrs = ['email', 'username', 'name']
    optionalUpdateAttrs = ['password', 'skype', 'linkedin', 'twitter',
                           'projects_limit', 'extern_uid', 'provider', 'bio',
                           'admin', 'can_create_group', 'website_url',
                           'confirm']
    managers = [('keys', UserKeyManager, [('user_id', 'id')])]

    def _data_for_gitlab(self, extra_parameters={}, update=False):
        if hasattr(self, 'confirm'):
            self.confirm = str(self.confirm).lower()
        return super(User, self)._data_for_gitlab(extra_parameters)

    def Key(self, id=None, **kwargs):
        warnings.warn("`Key` is deprecated, use `keys` instead",
                      DeprecationWarning)
        return UserKey._get_list_or_object(self.gitlab, id,
                                           user_id=self.id,
                                           **kwargs)


class UserManager(BaseManager):
    obj_cls = User


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
    managers = [('keys', CurrentUserKeyManager, [('user_id', 'id')])]

    def Key(self, id=None, **kwargs):
        warnings.warn("`Key` is deprecated, use `keys` instead",
                      DeprecationWarning)
        return CurrentUserKey._get_list_or_object(self.gitlab, id, **kwargs)


class ApplicationSettings(GitlabObject):
    _url = '/application/settings'
    _id_in_update_url = False
    optionalUpdateAttrs = ['after_sign_out_path', 'default_branch_protection',
                           'default_project_visibility',
                           'default_projects_limit',
                           'default_snippet_visibility', 'gravatar_enabled',
                           'home_page_url', 'restricted_signup_domains',
                           'restricted_visibility_levels',
                           'session_expire_delay', 'sign_in_text',
                           'signin_enabled', 'signup_enabled',
                           'twitter_sharing_enabled',
                           'user_oauth_applications']
    canList = False
    canCreate = False
    canDelete = False


class ApplicationSettingsManager(BaseManager):
    obj_cls = ApplicationSettings


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


class Group(GitlabObject):
    _url = '/groups'
    canUpdate = False
    _constructorTypes = {'projects': 'Project'}
    requiredCreateAttrs = ['name', 'path']
    shortPrintAttr = 'name'
    managers = [('members', GroupMemberManager, [('group_id', 'id')])]

    GUEST_ACCESS = 10
    REPORTER_ACCESS = 20
    DEVELOPER_ACCESS = 30
    MASTER_ACCESS = 40
    OWNER_ACCESS = 50

    def Member(self, id=None, **kwargs):
        warnings.warn("`Member` is deprecated, use `members` instead",
                      DeprecationWarning)
        return GroupMember._get_list_or_object(self.gitlab, id,
                                               group_id=self.id,
                                               **kwargs)

    def transfer_project(self, id, **kwargs):
        url = '/groups/%d/projects/%d' % (self.id, id)
        r = self.gitlab._raw_post(url, None, **kwargs)
        raise_error_from_response(r, GitlabTransferProjectError, 201)


class GroupManager(BaseManager):
    obj_cls = Group

    def search(self, query, **kwargs):
        """Searches groups by name.

        Returns a list of matching groups.
        """
        url = '/groups?search=' + query
        return self._custom_list(url, Group, **kwargs)


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


class IssueManager(BaseManager):
    obj_cls = Issue


class ProjectBranch(GitlabObject):
    _url = '/projects/%(project_id)s/repository/branches'
    _constructorTypes = {'author': 'User', "committer": "User"}

    idAttr = 'name'
    canUpdate = False
    requiredUrlAttrs = ['project_id']
    requiredCreateAttrs = ['branch_name', 'ref']

    def protect(self, protect=True, **kwargs):
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
        self.protect(False, **kwargs)


class ProjectBranchManager(BaseManager):
    obj_cls = ProjectBranch


class ProjectCommit(GitlabObject):
    _url = '/projects/%(project_id)s/repository/commits'
    canDelete = False
    canUpdate = False
    canCreate = False
    requiredUrlAttrs = ['project_id']
    shortPrintAttr = 'title'

    def diff(self, **kwargs):
        url = ('/projects/%(project_id)s/repository/commits/%(commit_id)s/diff'
               % {'project_id': self.project_id, 'commit_id': self.id})
        r = self.gitlab._raw_get(url, **kwargs)
        raise_error_from_response(r, GitlabGetError)

        return r.json()

    def blob(self, filepath, **kwargs):
        url = ('/projects/%(project_id)s/repository/blobs/%(commit_id)s' %
               {'project_id': self.project_id, 'commit_id': self.id})
        url += '?filepath=%s' % filepath
        r = self.gitlab._raw_get(url, **kwargs)
        raise_error_from_response(r, GitlabGetError)

        return r.content


class ProjectCommitManager(BaseManager):
    obj_cls = ProjectCommit


class ProjectCommitStatus(GitlabObject):
    _url = '/projects/%(project_id)s/statuses/%(commit_id)s'
    canUpdate = False
    canDelete = False
    requiredUrlAttrs = ['project_id', 'commit_id']
    requiredCreateAttrs = ['state']
    optionalCreateAttrs = ['description', 'name', 'ref', 'target_url']
    requiredGetAttrs = []
    requiredUpdateAttrs = []
    requiredDeleteAttrs = []


class ProjectCommitStatusManager(BaseManager):
    obj_cls = ProjectCommitStatus


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


class ProjectForkManager(BaseManager):
    obj_cls = ProjectFork


class ProjectHook(GitlabObject):
    _url = '/projects/%(project_id)s/hooks'
    requiredUrlAttrs = ['project_id']
    requiredCreateAttrs = ['url']
    optionalCreateAttrs = ['push_events', 'issues_events',
                           'merge_requests_events', 'tag_push_events']
    shortPrintAttr = 'url'


class ProjectHookManager(BaseManager):
    obj_cls = ProjectHook


class ProjectIssueNote(GitlabObject):
    _url = '/projects/%(project_id)s/issues/%(issue_id)s/notes'
    _constructorTypes = {'author': 'User'}
    canUpdate = False
    canDelete = False
    requiredUrlAttrs = ['project_id', 'issue_id']
    requiredCreateAttrs = ['body']


class ProjectIssueNoteManager(BaseManager):
    obj_cls = ProjectIssueNote


class ProjectIssue(GitlabObject):
    _url = '/projects/%(project_id)s/issues/'
    _constructorTypes = {'author': 'User', 'assignee': 'User',
                         'milestone': 'ProjectMilestone'}
    canDelete = False
    requiredUrlAttrs = ['project_id']
    requiredCreateAttrs = ['title']
    # FIXME: state_event is only valid with update
    optionalCreateAttrs = ['description', 'assignee_id', 'milestone_id',
                           'labels', 'state_event']
    shortPrintAttr = 'title'
    managers = [('notes', ProjectIssueNoteManager,
                 [('project_id', 'project_id'), ('issue_id', 'id')])]

    def _data_for_gitlab(self, extra_parameters={}, update=False):
        # Gitlab-api returns labels in a json list and takes them in a
        # comma separated list.
        if hasattr(self, "labels"):
            if (self.labels is not None and
               not isinstance(self.labels, six.string_types)):
                labels = ", ".join(self.labels)
                extra_parameters['labels'] = labels

        return super(ProjectIssue, self)._data_for_gitlab(extra_parameters)

    def Note(self, id=None, **kwargs):
        warnings.warn("`Note` is deprecated, use `notes` instead",
                      DeprecationWarning)
        return ProjectIssueNote._get_list_or_object(self.gitlab, id,
                                                    project_id=self.project_id,
                                                    issue_id=self.id,
                                                    **kwargs)


class ProjectIssueManager(BaseManager):
    obj_cls = ProjectIssue


class ProjectMember(GitlabObject):
    _url = '/projects/%(project_id)s/members'
    requiredUrlAttrs = ['project_id']
    requiredCreateAttrs = ['access_level', 'user_id']
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


class ProjectTagReleaseManager(BaseManager):
    obj_cls = ProjectTagRelease


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
    _url = '/projects/%(project_id)s/merge_request'
    _urlPlural = '/projects/%(project_id)s/merge_requests'
    _constructorTypes = {'author': 'User', 'assignee': 'User'}
    canDelete = False
    requiredUrlAttrs = ['project_id']
    requiredCreateAttrs = ['source_branch', 'target_branch', 'title']
    optionalCreateAttrs = ['assignee_id']
    managers = [('notes', ProjectMergeRequestNoteManager,
                 [('project_id', 'project_id'), ('merge_request_id', 'id')])]

    def Note(self, id=None, **kwargs):
        warnings.warn("`Note` is deprecated, use `notes` instead",
                      DeprecationWarning)
        return ProjectMergeRequestNote._get_list_or_object(
            self.gitlab, id, project_id=self.project_id,
            merge_request_id=self.id, **kwargs)


class ProjectMergeRequestManager(BaseManager):
    obj_cls = ProjectMergeRequest


class ProjectMilestone(GitlabObject):
    _url = '/projects/%(project_id)s/milestones'
    canDelete = False
    requiredUrlAttrs = ['project_id']
    requiredCreateAttrs = ['title']
    optionalCreateAttrs = ['description', 'due_date', 'state_event']
    shortPrintAttr = 'title'

    def issues(self):
        url = "/projects/%s/milestones/%s/issues" % (self.project_id, self.id)
        r = self.gitlab._raw_get(url)
        raise_error_from_response(r, GitlabDeleteError)

        l = []
        for j in r.json():
            o = ProjectIssue(self, j)
            o._from_api = True
            l.append(o)

        return l


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
    requiredUpdateAttrs = []
    # FIXME: new_name is only valid with update
    optionalCreateAttrs = ['new_name']


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
    requiredDeleteAttrs = ['branch_name', 'commit_message']
    getListWhenNoId = False
    shortPrintAttr = 'file_path'
    getRequiresId = False

    def decode(self):
        """Returns the decoded content.

        Returns:
            (str): the decoded content.
        """
        return base64.b64decode(self.content)


class ProjectFileManager(BaseManager):
    obj_cls = ProjectFile


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
    optionalCreateAttrs = ['lifetime']
    shortPrintAttr = 'title'
    managers = [('notes', ProjectSnippetNoteManager,
                 [('project_id', 'project_id'), ('snippet_id', 'id')])]

    def Content(self, **kwargs):
        url = ("/projects/%(project_id)s/snippets/%(snippet_id)s/raw" %
               {'project_id': self.project_id, 'snippet_id': self.id})
        r = self.gitlab._raw_get(url, **kwargs)
        raise_error_from_response(r, GitlabGetError)
        return r.content

    def Note(self, id=None, **kwargs):
        warnings.warn("`Note` is deprecated, use `notes` instead",
                      DeprecationWarning)
        return ProjectSnippetNote._get_list_or_object(
            self.gitlab, id,
            project_id=self.project_id,
            snippet_id=self.id,
            **kwargs)


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


class Project(GitlabObject):
    _url = '/projects'
    _constructorTypes = {'owner': 'User', 'namespace': 'Group'}
    requiredCreateAttrs = ['name']
    requiredUpdateAttrs = []
    optionalCreateAttrs = ['default_branch', 'issues_enabled', 'wall_enabled',
                           'merge_requests_enabled', 'wiki_enabled',
                           'snippets_enabled', 'public', 'visibility_level',
                           'namespace_id', 'description', 'path', 'import_url']
    shortPrintAttr = 'path'
    managers = [
        ('branches', ProjectBranchManager, [('project_id', 'id')]),
        ('commits', ProjectCommitManager, [('project_id', 'id')]),
        ('commitstatuses', ProjectCommitStatusManager, [('project_id', 'id')]),
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
        ('snippets', ProjectSnippetManager, [('project_id', 'id')]),
        ('tags', ProjectTagManager, [('project_id', 'id')]),
        ('triggers', ProjectTriggerManager, [('project_id', 'id')]),
        ('variables', ProjectVariableManager, [('project_id', 'id')]),
    ]

    def Branch(self, id=None, **kwargs):
        warnings.warn("`Branch` is deprecated, use `branches` instead",
                      DeprecationWarning)
        return ProjectBranch._get_list_or_object(self.gitlab, id,
                                                 project_id=self.id,
                                                 **kwargs)

    def Commit(self, id=None, **kwargs):
        warnings.warn("`Commit` is deprecated, use `commits` instead",
                      DeprecationWarning)
        return ProjectCommit._get_list_or_object(self.gitlab, id,
                                                 project_id=self.id,
                                                 **kwargs)

    def Event(self, id=None, **kwargs):
        warnings.warn("`Event` is deprecated, use `events` instead",
                      DeprecationWarning)
        return ProjectEvent._get_list_or_object(self.gitlab, id,
                                                project_id=self.id,
                                                **kwargs)

    def File(self, id=None, **kwargs):
        warnings.warn("`File` is deprecated, use `files` instead",
                      DeprecationWarning)
        return ProjectFile._get_list_or_object(self.gitlab, id,
                                               project_id=self.id,
                                               **kwargs)

    def Hook(self, id=None, **kwargs):
        warnings.warn("`Hook` is deprecated, use `hooks` instead",
                      DeprecationWarning)
        return ProjectHook._get_list_or_object(self.gitlab, id,
                                               project_id=self.id,
                                               **kwargs)

    def Key(self, id=None, **kwargs):
        warnings.warn("`Key` is deprecated, use `keys` instead",
                      DeprecationWarning)
        return ProjectKey._get_list_or_object(self.gitlab, id,
                                              project_id=self.id,
                                              **kwargs)

    def Issue(self, id=None, **kwargs):
        warnings.warn("`Issue` is deprecated, use `issues` instead",
                      DeprecationWarning)
        return ProjectIssue._get_list_or_object(self.gitlab, id,
                                                project_id=self.id,
                                                **kwargs)

    def Label(self, id=None, **kwargs):
        warnings.warn("`Label` is deprecated, use `labels` instead",
                      DeprecationWarning)
        return ProjectLabel._get_list_or_object(self.gitlab, id,
                                                project_id=self.id,
                                                **kwargs)

    def Member(self, id=None, **kwargs):
        warnings.warn("`Member` is deprecated, use `members` instead",
                      DeprecationWarning)
        return ProjectMember._get_list_or_object(self.gitlab, id,
                                                 project_id=self.id,
                                                 **kwargs)

    def MergeRequest(self, id=None, **kwargs):
        warnings.warn(
            "`MergeRequest` is deprecated, use `mergerequests` instead",
            DeprecationWarning)
        return ProjectMergeRequest._get_list_or_object(self.gitlab, id,
                                                       project_id=self.id,
                                                       **kwargs)

    def Milestone(self, id=None, **kwargs):
        warnings.warn("`Milestone` is deprecated, use `milestones` instead",
                      DeprecationWarning)
        return ProjectMilestone._get_list_or_object(self.gitlab, id,
                                                    project_id=self.id,
                                                    **kwargs)

    def Note(self, id=None, **kwargs):
        warnings.warn("`Note` is deprecated, use `notes` instead",
                      DeprecationWarning)
        return ProjectNote._get_list_or_object(self.gitlab, id,
                                               project_id=self.id,
                                               **kwargs)

    def Snippet(self, id=None, **kwargs):
        warnings.warn("`Snippet` is deprecated, use `snippets` instead",
                      DeprecationWarning)
        return ProjectSnippet._get_list_or_object(self.gitlab, id,
                                                  project_id=self.id,
                                                  **kwargs)

    def Tag(self, id=None, **kwargs):
        warnings.warn("`Tag` is deprecated, use `tags` instead",
                      DeprecationWarning)
        return ProjectTag._get_list_or_object(self.gitlab, id,
                                              project_id=self.id,
                                              **kwargs)

    def tree(self, path='', ref_name='', **kwargs):
        url = "%s/%s/repository/tree" % (self._url, self.id)
        url += '?path=%s&ref_name=%s' % (path, ref_name)
        r = self.gitlab._raw_get(url, **kwargs)
        raise_error_from_response(r, GitlabGetError)
        return r.json()

    def blob(self, sha, filepath, **kwargs):
        url = "%s/%s/repository/blobs/%s" % (self._url, self.id, sha)
        url += '?filepath=%s' % (filepath)
        r = self.gitlab._raw_get(url, **kwargs)
        raise_error_from_response(r, GitlabGetError)
        return r.content

    def archive(self, sha=None, **kwargs):
        url = '/projects/%s/repository/archive' % self.id
        if sha:
            url += '?sha=%s' % sha
        r = self.gitlab._raw_get(url, **kwargs)
        raise_error_from_response(r, GitlabGetError)
        return r.content

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
        url = "/projects/%s/repository/files" % self.id
        url += ("?file_path=%s&branch_name=%s&content=%s&commit_message=%s" %
                (path, branch, content, message))
        r = self.gitlab._raw_post(url, data=None, content_type=None, **kwargs)
        raise_error_from_response(r, GitlabCreateError, 201)

    def update_file(self, path, branch, content, message, **kwargs):
        url = "/projects/%s/repository/files" % self.id
        url += ("?file_path=%s&branch_name=%s&content=%s&commit_message=%s" %
                (path, branch, content, message))
        r = self.gitlab._raw_put(url, data=None, content_type=None, **kwargs)
        raise_error_from_response(r, GitlabUpdateError)

    def delete_file(self, path, branch, message, **kwargs):
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


class TeamMember(GitlabObject):
    _url = '/user_teams/%(team_id)s/members'
    canUpdate = False
    requiredUrlAttrs = ['teamd_id']
    requiredCreateAttrs = ['access_level']
    shortPrintAttr = 'username'


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
                           'description']


class ProjectManager(BaseManager):
    obj_cls = Project

    def search(self, query, **kwargs):
        """Search projects by name.

        Args:
            query (str): The query string to send to GitLab for the search.
            **kwargs: Additional arguments to send to GitLab.

        Returns:
            list(Project): A list of matching projects.
        """
        return self._custom_list("/projects/search/" + query, Project,
                                 **kwargs)

    def all(self, **kwargs):
        """List all the projects (need admin rights).

        Args:
            **kwargs: Additional arguments to send to GitLab.

        Returns:
            list(Project): The list of projects.
        """
        return self._custom_list("/projects/all", Project, **kwargs)

    def owned(self, **kwargs):
        """List owned projects.

        Args:
            **kwargs: Additional arguments to send to GitLab.

        Returns:
            list(Project): The list of owned projects.
        """
        return self._custom_list("/projects/owned", Project, **kwargs)


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

    def Member(self, id=None, **kwargs):
        warnings.warn("`Member` is deprecated, use `members` instead",
                      DeprecationWarning)
        return TeamMember._get_list_or_object(self.gitlab, id,
                                              team_id=self.id,
                                              **kwargs)

    def Project(self, id=None, **kwargs):
        warnings.warn("`Project` is deprecated, use `projects` instead",
                      DeprecationWarning)
        return TeamProject._get_list_or_object(self.gitlab, id,
                                               team_id=self.id,
                                               **kwargs)


class TeamManager(BaseManager):
    obj_cls = Team

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
"""Package for interfacing with GitLab-api """
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
import itertools
import json
import warnings

import requests
import six

import gitlab.config
from gitlab.exceptions import *  # noqa
from gitlab.objects import *  # noqa

__title__ = 'python-gitlab'
__version__ = '0.10'
__author__ = 'Gauvain Pocentek'
__email__ = 'gauvain@pocentek.net'
__license__ = 'LGPL3'
__copyright__ = 'Copyright 2013-2015 Gauvain Pocentek'

warnings.simplefilter('always', DeprecationWarning)


def _sanitize(value):
    if isinstance(value, six.string_types):
        return value.replace('/', '%2F')
    return value


def _sanitize_dict(src):
    return dict((k, _sanitize(v)) for k, v in src.items())


class Gitlab(object):
    """Represents a GitLab server connection

    Args:
        url (str): the URL of the Gitlab server
        private_token (str): the user private token
        email (str): the user email/login
        password (str): the user password (associated with email)
        ssl_verify (bool): (Passed to requests-library)
        timeout (float or tuple(float,float)): (Passed to
            requests-library). Timeout to use for requests to gitlab server
    """

    def __init__(self, url, private_token=None,
                 email=None, password=None, ssl_verify=True, timeout=None):

        self._url = '%s/api/v3' % url
        #: Timeout to use for requests to gitlab server
        self.timeout = timeout
        #: Headers that will be used in request to GitLab
        self.headers = {}
        self.set_token(private_token)
        #: the user email
        self.email = email
        #: the user password (associated with email)
        self.password = password
        #: (Passed to requests-library)
        self.ssl_verify = ssl_verify

        self.user_keys = UserKeyManager(self)
        self.users = UserManager(self)
        self.group_members = GroupMemberManager(self)
        self.groups = GroupManager(self)
        self.hooks = HookManager(self)
        self.issues = IssueManager(self)
        self.project_branches = ProjectBranchManager(self)
        self.project_commits = ProjectCommitManager(self)
        self.project_keys = ProjectKeyManager(self)
        self.project_events = ProjectEventManager(self)
        self.project_hooks = ProjectHookManager(self)
        self.project_issue_notes = ProjectIssueNoteManager(self)
        self.project_issues = ProjectIssueManager(self)
        self.project_members = ProjectMemberManager(self)
        self.project_notes = ProjectNoteManager(self)
        self.project_tags = ProjectTagManager(self)
        self.project_mergerequest_notes = ProjectMergeRequestNoteManager(self)
        self.project_mergerequests = ProjectMergeRequestManager(self)
        self.project_milestones = ProjectMilestoneManager(self)
        self.project_labels = ProjectLabelManager(self)
        self.project_files = ProjectFileManager(self)
        self.project_snippet_notes = ProjectSnippetNoteManager(self)
        self.project_snippets = ProjectSnippetManager(self)
        self.user_projects = UserProjectManager(self)
        self.projects = ProjectManager(self)
        self.team_members = TeamMemberManager(self)
        self.team_projects = TeamProjectManager(self)
        self.teams = TeamManager(self)

    @staticmethod
    def from_config(gitlab_id=None, config_files=None):
        config = gitlab.config.GitlabConfigParser(gitlab_id=gitlab_id,
                                                  config_files=config_files)
        return Gitlab(config.url, private_token=config.token,
                      ssl_verify=config.ssl_verify, timeout=config.timeout)

    def auth(self):
        """Performs an authentication.

        Uses either the private token, or the email/password pair.

        The user attribute will hold a CurrentUser object on success.
        """
        if self.private_token:
            self.token_auth()
        else:
            self.credentials_auth()

    def credentials_auth(self):
        if not self.email or not self.password:
            raise GitlabAuthenticationError("Missing email/password")

        data = json.dumps({'email': self.email, 'password': self.password})
        r = self._raw_post('/session', data, content_type='application/json')
        raise_error_from_response(r, GitlabAuthenticationError, 201)
        self.user = CurrentUser(self, r.json())
        self.set_token(self.user.private_token)

    def token_auth(self):
        self.user = CurrentUser(self)

    def set_url(self, url):
        """Updates the gitlab URL."""
        self._url = '%s/api/v3' % url

    def _construct_url(self, id_, obj, parameters):
        if 'next_url' in parameters:
            return parameters['next_url']
        args = _sanitize_dict(parameters)
        if id_ is None and obj._urlPlural is not None:
            url = obj._urlPlural % args
        else:
            url = obj._url % args

        if id_ is not None:
            url = '%s%s/%s' % (self._url, url, str(id_))
        else:
            url = '%s%s' % (self._url, url)
        return url

    def _create_headers(self, content_type=None, headers={}):
        request_headers = self.headers.copy()
        request_headers.update(headers)
        if content_type is not None:
            request_headers['Content-type'] = content_type
        return request_headers

    def set_token(self, token):
        """Sets the private token for authentication."""
        self.private_token = token if token else None
        if token:
            self.headers["PRIVATE-TOKEN"] = token
        elif "PRIVATE-TOKEN" in self.headers:
            del self.headers["PRIVATE-TOKEN"]

    def set_credentials(self, email, password):
        """Sets the email/login and password for authentication."""
        self.email = email
        self.password = password

    def _raw_get(self, path, content_type=None, **kwargs):
        url = '%s%s' % (self._url, path)
        headers = self._create_headers(content_type)

        try:
            return requests.get(url,
                                params=kwargs,
                                headers=headers,
                                verify=self.ssl_verify,
                                timeout=self.timeout)
        except Exception:
            raise GitlabConnectionError(
                "Can't connect to GitLab server (%s)" % self._url)

    def _raw_post(self, path, data=None, content_type=None, **kwargs):
        url = '%s%s' % (self._url, path)
        headers = self._create_headers(content_type)
        try:
            return requests.post(url, params=kwargs, data=data,
                                 headers=headers,
                                 verify=self.ssl_verify,
                                 timeout=self.timeout)
        except Exception:
            raise GitlabConnectionError(
                "Can't connect to GitLab server (%s)" % self._url)

    def _raw_put(self, path, data=None, content_type=None, **kwargs):
        url = '%s%s' % (self._url, path)
        headers = self._create_headers(content_type)

        try:
            return requests.put(url, data=data, params=kwargs,
                                headers=headers,
                                verify=self.ssl_verify,
                                timeout=self.timeout)
        except Exception:
            raise GitlabConnectionError(
                "Can't connect to GitLab server (%s)" % self._url)

    def _raw_delete(self, path, content_type=None, **kwargs):
        url = '%s%s' % (self._url, path)
        headers = self._create_headers(content_type)

        try:
            return requests.delete(url,
                                   params=kwargs,
                                   headers=headers,
                                   verify=self.ssl_verify,
                                   timeout=self.timeout)
        except Exception:
            raise GitlabConnectionError(
                "Can't connect to GitLab server (%s)" % self._url)

    def list(self, obj_class, **kwargs):
        missing = []
        for k in itertools.chain(obj_class.requiredUrlAttrs,
                                 obj_class.requiredListAttrs):
            if k not in kwargs:
                missing.append(k)
        if missing:
            raise GitlabListError('Missing attribute(s): %s' %
                                  ", ".join(missing))

        url = self._construct_url(id_=None, obj=obj_class, parameters=kwargs)
        headers = self._create_headers()

        # Remove attributes that are used in url so that there is only
        # url-parameters left
        params = kwargs.copy()
        for attribute in obj_class.requiredUrlAttrs:
            del params[attribute]

        try:
            r = requests.get(url, params=params, headers=headers,
                             verify=self.ssl_verify,
                             timeout=self.timeout)
        except Exception:
            raise GitlabConnectionError(
                "Can't connect to GitLab server (%s)" % self._url)

        raise_error_from_response(r, GitlabListError)

        cls = obj_class
        if obj_class._returnClass:
            cls = obj_class._returnClass

        cls_kwargs = kwargs.copy()

        # Add _from_api manually, because we are not creating objects
        # through normal path
        cls_kwargs['_from_api'] = True

        get_all_results = params.get('all', False)

        # Remove parameters from kwargs before passing it to constructor
        for key in ['all', 'page', 'per_page', 'sudo']:
            if key in cls_kwargs:
                del cls_kwargs[key]

        results = [cls(self, item, **cls_kwargs) for item in r.json()
                   if item is not None]
        if ('next' in r.links and 'url' in r.links['next']
           and get_all_results is True):
            args = kwargs.copy()
            args['next_url'] = r.links['next']['url']
            results.extend(self.list(obj_class, **args))
        return results

    def get(self, obj_class, id=None, **kwargs):
        missing = []
        for k in itertools.chain(obj_class.requiredUrlAttrs,
                                 obj_class.requiredGetAttrs):
            if k not in kwargs:
                missing.append(k)
        if missing:
            raise GitlabGetError('Missing attribute(s): %s' %
                                 ", ".join(missing))

        sanitized_id = _sanitize(id)
        url = self._construct_url(id_=sanitized_id, obj=obj_class,
                                  parameters=kwargs)
        headers = self._create_headers()

        # Remove attributes that are used in url so that there is only
        # url-parameters left
        params = kwargs.copy()
        for attribute in obj_class.requiredUrlAttrs:
            del params[attribute]

        try:
            r = requests.get(url, params=params, headers=headers,
                             verify=self.ssl_verify, timeout=self.timeout)
        except Exception:
            raise GitlabConnectionError(
                "Can't connect to GitLab server (%s)" % self._url)

        raise_error_from_response(r, GitlabGetError)
        return r.json()

    def delete(self, obj, **kwargs):
        params = obj.__dict__.copy()
        params.update(kwargs)
        missing = []
        for k in itertools.chain(obj.requiredUrlAttrs,
                                 obj.requiredDeleteAttrs):
            if k not in params:
                missing.append(k)
        if missing:
            raise GitlabDeleteError('Missing attribute(s): %s' %
                                    ", ".join(missing))

        obj_id = getattr(obj, obj.idAttr)
        url = self._construct_url(id_=obj_id, obj=obj, parameters=params)
        headers = self._create_headers()

        # Remove attributes that are used in url so that there is only
        # url-parameters left
        for attribute in obj.requiredUrlAttrs:
            del params[attribute]

        try:
            r = requests.delete(url,
                                params=params,
                                headers=headers,
                                verify=self.ssl_verify,
                                timeout=self.timeout)
        except Exception:
            raise GitlabConnectionError(
                "Can't connect to GitLab server (%s)" % self._url)

        raise_error_from_response(r, GitlabDeleteError)
        return True

    def create(self, obj, **kwargs):
        params = obj.__dict__.copy()
        params.update(kwargs)
        missing = []
        for k in itertools.chain(obj.requiredUrlAttrs,
                                 obj.requiredCreateAttrs):
            if k not in params:
                missing.append(k)
        if missing:
            raise GitlabCreateError('Missing attribute(s): %s' %
                                    ", ".join(missing))

        url = self._construct_url(id_=None, obj=obj, parameters=params)
        headers = self._create_headers(content_type="application/json")

        # build data that can really be sent to server
        data = obj._data_for_gitlab(extra_parameters=kwargs)

        try:
            r = requests.post(url, data=data,
                              headers=headers,
                              verify=self.ssl_verify,
                              timeout=self.timeout)
        except Exception:
            raise GitlabConnectionError(
                "Can't connect to GitLab server (%s)" % self._url)

        raise_error_from_response(r, GitlabCreateError, 201)
        return r.json()

    def update(self, obj, **kwargs):
        params = obj.__dict__.copy()
        params.update(kwargs)
        missing = []
        for k in itertools.chain(obj.requiredUrlAttrs,
                                 obj.requiredCreateAttrs):
            if k not in params:
                missing.append(k)
        if missing:
            raise GitlabUpdateError('Missing attribute(s): %s' %
                                    ", ".join(missing))
        url = self._construct_url(id_=obj.id, obj=obj, parameters=params)
        headers = self._create_headers(content_type="application/json")

        # build data that can really be sent to server
        data = obj._data_for_gitlab(extra_parameters=kwargs)

        try:
            r = requests.put(url, data=data,
                             headers=headers,
                             verify=self.ssl_verify,
                             timeout=self.timeout)
        except Exception:
            raise GitlabConnectionError(
                "Can't connect to GitLab server (%s)" % self._url)

        raise_error_from_response(r, GitlabUpdateError)
        return r.json()

    def Hook(self, id=None, **kwargs):
        """Creates/tests/lists system hook(s) known by the GitLab server.

        If id is None, returns a list of hooks.

        If id is an integer, tests the matching hook.

        If id is a dict, creates a new object using attributes provided. The
        object is NOT saved on the server. Use the save() method on the object
        to write it on the server.
        """
        return Hook._get_list_or_object(self, id, **kwargs)

    def Project(self, id=None, **kwargs):
        """Creates/gets/lists project(s) known by the GitLab server.

        If id is None, returns a list of projects.

        If id is an integer, returns the matching project (or raises a
        GitlabGetError if not found)

        If id is a dict, creates a new object using attributes provided. The
        object is NOT saved on the server. Use the save() method on the object
        to write it on the server.
        """
        return Project._get_list_or_object(self, id, **kwargs)

    def UserProject(self, id=None, **kwargs):
        """Creates a project for a user.

        id must be a dict.
        """
        return UserProject._get_list_or_object(self, id, **kwargs)

    def _list_projects(self, url, **kwargs):
        r = self._raw_get(url, **kwargs)
        raise_error_from_response(r, GitlabListError)

        l = []
        for o in r.json():
            p = Project(self, o)
            p._from_api = True
            l.append(p)

        return l

    def search_projects(self, query, **kwargs):
        """Searches projects by  name.

        Returns a list of matching projects.
        """
        return self._list_projects("/projects/search/" + query, **kwargs)

    def all_projects(self, **kwargs):
        """Lists all the projects (need admin rights)."""
        return self._list_projects("/projects/all", **kwargs)

    def owned_projects(self, **kwargs):
        """Lists owned projects."""
        return self._list_projects("/projects/owned", **kwargs)

    def Group(self, id=None, **kwargs):
        """Creates/gets/lists group(s) known by the GitLab server

        Args:
            id: If id is None, returns a list of groups.
            id: If id is an integer,
                returns the matching group (or raises a GitlabGetError if not
                found).
            id: If id is a dict, creates a new object using attributes
                provided. The object is NOT saved on the server. Use the
                save() method on the object to write it on the server.
            kwargs: Arbitrary keyword arguments
        """
        return Group._get_list_or_object(self, id, **kwargs)

    def Issue(self, id=None, **kwargs):
        """Lists issues(s) known by the GitLab server.

        Does not support creation or getting a single issue unlike other
        methods in this class yet.
        """
        return Issue._get_list_or_object(self, id, **kwargs)

    def User(self, id=None, **kwargs):
        """Creates/gets/lists users(s) known by the GitLab server.

        If id is None, returns a list of users.

        If id is an integer, returns the matching user (or raises a
        GitlabGetError if not found)

        If id is a dict, creates a new object using attributes provided. The
        object is NOT saved on the server. Use the save() method on the object
        to write it on the server.
        """
        return User._get_list_or_object(self, id, **kwargs)

    def Team(self, id=None, **kwargs):
        """Creates/gets/lists team(s) known by the GitLab server.

        If id is None, returns a list of teams.

        If id is an integer, returns the matching team (or raises a
        GitlabGetError if not found)

        If id is a dict, create a new object using attributes provided. The
        object is NOT saved on the server. Use the save() method on the object
        to write it on the server.
        """
        return Team._get_list_or_object(self, id, **kwargs)

    def ProjectFork(self, id=None, **kwargs):
        """Fork a project for a user.

        id must be a dict.
        """
        return ProjectFork._get_list_or_object(self, id, **kwargs)


def _get_display_encoding():
    return sys.stdout.encoding or sys.getdefaultencoding()


def _sanitize(value):
    if isinstance(value, six.string_types):
        return value.replace('/', '%2F')
    return value


def _sanitize_dict(src):
    return dict((k, _sanitize(v)) for k, v in src.items())


class GitlabObject(object):
    """Base class for all classes that interface with GitLab

    Args:
        gl (gitlab.Gitlab): GitLab server connection
        data: If data is integer or string type, get object from GitLab
        data: If data is dictionary, create new object locally. To save object
           in GitLab, call save-method
        kwargs: Arbitrary keyword arguments
    """
    #: Url to use in GitLab for this object
    _url = None
    # Some objects (e.g. merge requests) have different urls for singular and
    # plural
    _urlPlural = None
    _returnClass = None
    _constructorTypes = None
    #: Whether _get_list_or_object should return list or object when id is None
    getListWhenNoId = True

    #: Tells if GitLab-api allows retrieving single objects
    canGet = True
    #: Tells if GitLab-api allows listing of objects
    canList = True
    #: Tells if GitLab-api allows creation of new objects
    canCreate = True
    #: Tells if GitLab-api allows updating object
    canUpdate = True
    #: Tells if GitLab-api allows deleting object
    canDelete = True
    #: Attributes that are required for constructing url
    requiredUrlAttrs = []
    #: Attributes that are required when retrieving list of objects
    requiredListAttrs = []
    #: Attributes that are required when retrieving single object
    requiredGetAttrs = []
    #: Attributes that are required when deleting object
    requiredDeleteAttrs = []
    #: Attributes that are required when creating a new object
    requiredCreateAttrs = []
    #: Attributes that are optional when creating a new object
    optionalCreateAttrs = []
    #: Attributes that are required when updating an object
    requiredUpdateAttrs = None
    #: Attributes that are optional when updating an object
    optionalUpdateAttrs = None
    #: Whether the object ID is required in the GET url
    getRequiresId = True

    idAttr = 'id'
    shortPrintAttr = None

    def _data_for_gitlab(self, extra_parameters={}):
        data = {}
        for attribute in itertools.chain(self.requiredCreateAttrs,
                                         self.optionalCreateAttrs):
            if hasattr(self, attribute):
                data[attribute] = getattr(self, attribute)

        data.update(extra_parameters)

        return json.dumps(data)

    @classmethod
    def list(cls, gl, **kwargs):
        if not cls.canList:
            raise NotImplementedError

        if not cls._url:
            raise NotImplementedError

        return gl.list(cls, **kwargs)

    @classmethod
    def _get_list_or_object(cls, gl, id, **kwargs):
        if id is None and cls.getListWhenNoId:
            return cls.list(gl, **kwargs)
        else:
            return cls(gl, id, **kwargs)

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
        self._created = True

    def _update(self, **kwargs):
        if not self.canUpdate:
            raise NotImplementedError

        json = self.gitlab.update(self, **kwargs)
        self._set_from_dict(json)

    def save(self, **kwargs):
        if self._created:
            self._update(**kwargs)
        else:
            self._create(**kwargs)

    def delete(self, **kwargs):
        if not self.canDelete:
            raise NotImplementedError

        if not self._created:
            raise GitlabDeleteError("Object not yet created")

        return self.gitlab.delete(self, **kwargs)

    def __init__(self, gl, data=None, **kwargs):
        self._created = False
        self.gitlab = gl

        if (data is None or isinstance(data, six.integer_types) or
           isinstance(data, six.string_types)):
            if not self.canGet:
                raise NotImplementedError
            data = self.gitlab.get(self.__class__, data, **kwargs)
            # Object is created because we got it from api
            self._created = True

        self._set_from_dict(data)

        if kwargs:
            for k, v in kwargs.items():
                self.__dict__[k] = v

        # Special handling for api-objects that don't have id-number in api
        # responses. Currently only Labels and Files
        if not hasattr(self, "id"):
            self.id = None

    def __str__(self):
        return '%s => %s' % (type(self), str(self.__dict__))

    def display(self, pretty):
        if pretty:
            self.pretty_print()
        else:
            self.short_print()

    def short_print(self, depth=0):
        id = self.__dict__[self.idAttr]
        print("%s%s: %s" % (" " * depth * 2, self.idAttr, id))
        if self.shortPrintAttr:
            print("%s%s: %s" % (" " * depth * 2,
                                self.shortPrintAttr.replace('_', '-'),
                                self.__dict__[self.shortPrintAttr]))

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
            return obj.encode(_get_display_encoding(), "replace")
        else:
            return str(obj)

    def pretty_print(self, depth=0):
        id = self.__dict__[self.idAttr]
        print("%s%s: %s" % (" " * depth * 2, self.idAttr, id))
        for k in sorted(self.__dict__.keys()):
            if k == self.idAttr or k == 'id':
                continue
            if k[0] == '_':
                continue
            v = self.__dict__[k]
            pretty_k = k.replace('_', '-')
            if six.PY2:
                pretty_k = pretty_k.encode(_get_display_encoding(), "replace")
            if isinstance(v, GitlabObject):
                if depth == 0:
                    print("%s:" % pretty_k)
                    v.pretty_print(1)
                else:
                    print("%s: %s" % (pretty_k, v.id))
            else:
                if isinstance(v, Gitlab):
                    continue
                v = GitlabObject._obj_to_str(v)
                print("%s%s: %s" % (" " * depth * 2, pretty_k, v))

    def json(self):
        return json.dumps(self.__dict__, cls=jsonEncoder)


class UserKey(GitlabObject):
    _url = '/users/%(user_id)s/keys'
    canGet = False
    canUpdate = False
    requiredUrlAttrs = ['user_id']
    requiredCreateAttrs = ['title', 'key']


class User(GitlabObject):
    _url = '/users'
    shortPrintAttr = 'username'
    # FIXME: password is required for create but not for update
    requiredCreateAttrs = ['email', 'username', 'name']
    optionalCreateAttrs = ['password', 'skype', 'linkedin', 'twitter',
                           'projects_limit', 'extern_uid', 'provider',
                           'bio', 'admin', 'can_create_group', 'website_url',
                           'confirm']

    def _data_for_gitlab(self, extra_parameters={}):
        if hasattr(self, 'confirm'):
            self.confirm = str(self.confirm).lower()
        return super(User, self)._data_for_gitlab(extra_parameters)

    def Key(self, id=None, **kwargs):
        return UserKey._get_list_or_object(self.gitlab, id,
                                           user_id=self.id,
                                           **kwargs)


class CurrentUserKey(GitlabObject):
    _url = '/user/keys'
    canUpdate = False
    shortPrintAttr = 'title'
    requiredCreateAttrs = ['title', 'key']


class CurrentUser(GitlabObject):
    _url = '/user'
    canList = False
    canCreate = False
    canUpdate = False
    canDelete = False
    shortPrintAttr = 'username'

    def Key(self, id=None, **kwargs):
        return CurrentUserKey._get_list_or_object(self.gitlab, id, **kwargs)


class GroupMember(GitlabObject):
    _url = '/groups/%(group_id)s/members'
    canGet = False
    canUpdate = False
    requiredUrlAttrs = ['group_id']
    requiredCreateAttrs = ['access_level', 'user_id']
    shortPrintAttr = 'username'


class Group(GitlabObject):
    _url = '/groups'
    canUpdate = False
    _constructorTypes = {'projects': 'Project'}
    requiredCreateAttrs = ['name', 'path']
    shortPrintAttr = 'name'

    GUEST_ACCESS = 10
    REPORTER_ACCESS = 20
    DEVELOPER_ACCESS = 30
    MASTER_ACCESS = 40
    OWNER_ACCESS = 50

    def Member(self, id=None, **kwargs):
        return GroupMember._get_list_or_object(self.gitlab, id,
                                               group_id=self.id,
                                               **kwargs)

    def transfer_project(self, id, **kwargs):
        url = '/groups/%d/projects/%d' % (self.id, id)
        r = self.gitlab._raw_post(url, None, **kwargs)
        if r.status_code != 201:
            _raise_error_from_response(r, GitlabTransferProjectError)


class Hook(GitlabObject):
    _url = '/hooks'
    canUpdate = False
    requiredCreateAttrs = ['url']
    shortPrintAttr = 'url'


class Issue(GitlabObject):
    _url = '/issues'
    _constructorTypes = {'author': 'User', 'assignee': 'User',
                         'milestone': 'ProjectMilestone'}
    canGet = False
    canDelete = False
    canUpdate = False
    canCreate = False
    shortPrintAttr = 'title'


class ProjectBranch(GitlabObject):
    _url = '/projects/%(project_id)s/repository/branches'
    _constructorTypes = {'author': 'User', "committer": "User"}

    idAttr = 'name'
    canUpdate = False
    requiredUrlAttrs = ['project_id']
    requiredCreateAttrs = ['branch_name', 'ref']
    _constructorTypes = {'commit': 'ProjectCommit'}

    def protect(self, protect=True, **kwargs):
        url = self._url % {'project_id': self.project_id}
        action = 'protect' if protect else 'unprotect'
        url = "%s/%s/%s" % (url, self.name, action)
        r = self.gitlab._raw_put(url, data=None, content_type=None, **kwargs)

        if r.status_code == 200:
            if protect:
                self.protected = protect
            else:
                del self.protected
        else:
            _raise_error_from_response(r, GitlabProtectError)

    def unprotect(self, **kwargs):
        self.protect(False, **kwargs)


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
        if r.status_code == 200:
            return r.json()
        else:
            _raise_error_from_response(r, GitlabGetError)

    def blob(self, filepath, **kwargs):
        url = ('/projects/%(project_id)s/repository/blobs/%(commit_id)s' %
               {'project_id': self.project_id, 'commit_id': self.id})
        url += '?filepath=%s' % filepath
        r = self.gitlab._raw_get(url, **kwargs)
        if r.status_code == 200:
            return r.content
        else:
            _raise_error_from_response(r, GitlabGetError)


class ProjectKey(GitlabObject):
    _url = '/projects/%(project_id)s/keys'
    canUpdate = False
    requiredUrlAttrs = ['project_id']
    requiredCreateAttrs = ['title', 'key']


class ProjectEvent(GitlabObject):
    _url = '/projects/%(project_id)s/events'
    canGet = False
    canDelete = False
    canUpdate = False
    canCreate = False
    requiredUrlAttrs = ['project_id']
    shortPrintAttr = 'target_title'


class ProjectHook(GitlabObject):
    _url = '/projects/%(project_id)s/hooks'
    requiredUrlAttrs = ['project_id']
    requiredCreateAttrs = ['url']
    optionalCreateAttrs = ['push_events', 'issues_events',
                           'merge_requests_events', 'tag_push_events']
    shortPrintAttr = 'url'


class ProjectIssueNote(GitlabObject):
    _url = '/projects/%(project_id)s/issues/%(issue_id)s/notes'
    _constructorTypes = {'author': 'User'}
    canUpdate = False
    canDelete = False
    requiredUrlAttrs = ['project_id', 'issue_id']
    requiredCreateAttrs = ['body']


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

    def _data_for_gitlab(self, extra_parameters={}):
        # Gitlab-api returns labels in a json list and takes them in a
        # comma separated list.
        if hasattr(self, "labels"):
            if (self.labels is not None and
               not isinstance(self.labels, six.string_types)):
                labels = ", ".join(self.labels)
                extra_parameters['labels'] = labels

        return super(ProjectIssue, self)._data_for_gitlab(extra_parameters)

    def Note(self, id=None, **kwargs):
        return ProjectIssueNote._get_list_or_object(self.gitlab, id,
                                                    project_id=self.project_id,
                                                    issue_id=self.id,
                                                    **kwargs)


class ProjectMember(GitlabObject):
    _url = '/projects/%(project_id)s/members'
    requiredUrlAttrs = ['project_id']
    requiredCreateAttrs = ['access_level', 'user_id']
    shortPrintAttr = 'username'


class ProjectNote(GitlabObject):
    _url = '/projects/%(project_id)s/notes'
    _constructorTypes = {'author': 'User'}
    canUpdate = False
    canDelete = False
    requiredUrlAttrs = ['project_id']
    requiredCreateAttrs = ['body']


class ProjectTag(GitlabObject):
    _url = '/projects/%(project_id)s/repository/tags'
    idAttr = 'name'
    canGet = False
    canDelete = False
    canUpdate = False
    requiredUrlAttrs = ['project_id']
    requiredCreateAttrs = ['tag_name', 'ref']
    optionalCreateAttrs = ['message']
    shortPrintAttr = 'name'


class ProjectMergeRequestNote(GitlabObject):
    _url = '/projects/%(project_id)s/merge_requests/%(merge_request_id)s/notes'
    _constructorTypes = {'author': 'User'}
    canDelete = False
    requiredUrlAttrs = ['project_id', 'merge_request_id']
    requiredCreateAttrs = ['body']


class ProjectMergeRequest(GitlabObject):
    _url = '/projects/%(project_id)s/merge_request'
    _urlPlural = '/projects/%(project_id)s/merge_requests'
    _constructorTypes = {'author': 'User', 'assignee': 'User'}
    canDelete = False
    requiredUrlAttrs = ['project_id']
    requiredCreateAttrs = ['source_branch', 'target_branch', 'title']
    optionalCreateAttrs = ['assignee_id']

    def Note(self, id=None, **kwargs):
        return ProjectMergeRequestNote._get_list_or_object(
            self.gitlab, id, project_id=self.project_id,
            merge_request_id=self.id, **kwargs)


class ProjectMilestone(GitlabObject):
    _url = '/projects/%(project_id)s/milestones'
    canDelete = False
    requiredUrlAttrs = ['project_id']
    requiredCreateAttrs = ['title']
    optionalCreateAttrs = ['description', 'due_date', 'state_event']
    shortPrintAttr = 'title'


class ProjectLabel(GitlabObject):
    _url = '/projects/%(project_id)s/labels'
    requiredUrlAttrs = ['project_id']
    idAttr = 'name'
    requiredDeleteAttrs = ['name']
    requiredCreateAttrs = ['name', 'color']
    requiredUpdateAttrs = []
    # FIXME: new_name is only valid with update
    optionalCreateAttrs = ['new_name']


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


class ProjectSnippetNote(GitlabObject):
    _url = '/projects/%(project_id)s/snippets/%(snippet_id)s/notes'
    _constructorTypes = {'author': 'User'}
    canUpdate = False
    canDelete = False
    requiredUrlAttrs = ['project_id', 'snippet_id']
    requiredCreateAttrs = ['body']


class ProjectSnippet(GitlabObject):
    _url = '/projects/%(project_id)s/snippets'
    _constructorTypes = {'author': 'User'}
    requiredUrlAttrs = ['project_id']
    requiredCreateAttrs = ['title', 'file_name', 'code']
    optionalCreateAttrs = ['lifetime']
    shortPrintAttr = 'title'

    def Content(self, **kwargs):
        url = ("/projects/%(project_id)s/snippets/%(snippet_id)s/raw" %
               {'project_id': self.project_id, 'snippet_id': self.id})
        r = self.gitlab._raw_get(url, **kwargs)

        if r.status_code == 200:
            return r.content
        else:
            _raise_error_from_response(r, GitlabGetError)

    def Note(self, id=None, **kwargs):
        return ProjectSnippetNote._get_list_or_object(
            self.gitlab, id,
            project_id=self.project_id,
            snippet_id=self.id,
            **kwargs)


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

    def Branch(self, id=None, **kwargs):
        return ProjectBranch._get_list_or_object(self.gitlab, id,
                                                 project_id=self.id,
                                                 **kwargs)

    def Commit(self, id=None, **kwargs):
        return ProjectCommit._get_list_or_object(self.gitlab, id,
                                                 project_id=self.id,
                                                 **kwargs)

    def Event(self, id=None, **kwargs):
        return ProjectEvent._get_list_or_object(self.gitlab, id,
                                                project_id=self.id,
                                                **kwargs)

    def Hook(self, id=None, **kwargs):
        return ProjectHook._get_list_or_object(self.gitlab, id,
                                               project_id=self.id,
                                               **kwargs)

    def Key(self, id=None, **kwargs):
        return ProjectKey._get_list_or_object(self.gitlab, id,
                                              project_id=self.id,
                                              **kwargs)

    def Issue(self, id=None, **kwargs):
        return ProjectIssue._get_list_or_object(self.gitlab, id,
                                                project_id=self.id,
                                                **kwargs)

    def Member(self, id=None, **kwargs):
        return ProjectMember._get_list_or_object(self.gitlab, id,
                                                 project_id=self.id,
                                                 **kwargs)

    def MergeRequest(self, id=None, **kwargs):
        return ProjectMergeRequest._get_list_or_object(self.gitlab, id,
                                                       project_id=self.id,
                                                       **kwargs)

    def Milestone(self, id=None, **kwargs):
        return ProjectMilestone._get_list_or_object(self.gitlab, id,
                                                    project_id=self.id,
                                                    **kwargs)

    def Note(self, id=None, **kwargs):
        return ProjectNote._get_list_or_object(self.gitlab, id,
                                               project_id=self.id,
                                               **kwargs)

    def Snippet(self, id=None, **kwargs):
        return ProjectSnippet._get_list_or_object(self.gitlab, id,
                                                  project_id=self.id,
                                                  **kwargs)

    def Label(self, id=None, **kwargs):
        return ProjectLabel._get_list_or_object(self.gitlab, id,
                                                project_id=self.id,
                                                **kwargs)

    def File(self, id=None, **kwargs):
        return ProjectFile._get_list_or_object(self.gitlab, id,
                                               project_id=self.id,
                                               **kwargs)

    def Tag(self, id=None, **kwargs):
        return ProjectTag._get_list_or_object(self.gitlab, id,
                                              project_id=self.id,
                                              **kwargs)

    def tree(self, path='', ref_name='', **kwargs):
        url = "%s/%s/repository/tree" % (self._url, self.id)
        url += '?path=%s&ref_name=%s' % (path, ref_name)
        r = self.gitlab._raw_get(url, **kwargs)
        if r.status_code == 200:
            return r.json()
        else:
            _raise_error_from_response(r, GitlabGetError)

    def blob(self, sha, filepath, **kwargs):
        url = "%s/%s/repository/blobs/%s" % (self._url, self.id, sha)
        url += '?filepath=%s' % (filepath)
        r = self.gitlab._raw_get(url, **kwargs)
        if r.status_code == 200:
            return r.content
        else:
            _raise_error_from_response(r, GitlabGetError)

    def archive(self, sha=None, **kwargs):
        url = '/projects/%s/repository/archive' % self.id
        if sha:
            url += '?sha=%s' % sha
        r = self.gitlab._raw_get(url, **kwargs)
        if r.status_code == 200:
            return r.content
        else:
            _raise_error_from_response(r, GitlabGetError)

    def create_file(self, path, branch, content, message, **kwargs):
        """Creates file in project repository

        Args:
            path (str): Full path to new file
            branch (str): The name of branch
            content (str): Content of the file
            message (str): Commit message
            kwargs: Arbitrary keyword arguments

        Raises:
            GitlabCreateError: Operation failed
            GitlabConnectionError: Connection to GitLab-server failed
        """
        url = "/projects/%s/repository/files" % self.id
        url += ("?file_path=%s&branch_name=%s&content=%s&commit_message=%s" %
                (path, branch, content, message))
        r = self.gitlab._raw_post(url, data=None, content_type=None, **kwargs)
        if r.status_code != 201:
            _raise_error_from_response(r, GitlabCreateError)

    def update_file(self, path, branch, content, message, **kwargs):
        url = "/projects/%s/repository/files" % self.id
        url += ("?file_path=%s&branch_name=%s&content=%s&commit_message=%s" %
                (path, branch, content, message))
        r = self.gitlab._raw_put(url, data=None, content_type=None, **kwargs)
        if r.status_code != 200:
            _raise_error_from_response(r, GitlabUpdateError)

    def delete_file(self, path, branch, message, **kwargs):
        url = "/projects/%s/repository/files" % self.id
        url += ("?file_path=%s&branch_name=%s&commit_message=%s" %
                (path, branch, message))
        r = self.gitlab._raw_delete(url, **kwargs)
        if r.status_code != 200:
            _raise_error_from_response(r, GitlabDeleteError)

    def create_fork_relation(self, forked_from_id):
        """Create a forked from/to relation between existing projects.

        Args:
            forked_from_id (int): The ID of the project that was forked from

        Raises:
            GitlabCreateError: Operation failed
            GitlabConnectionError: Connection to GitLab-server failed
        """
        url = "/projects/%s/fork/%s" % (self.id, forked_from_id)
        r = self.gitlab._raw_post(url)
        if r.status_code != 201:
            _raise_error_from_response(r, GitlabCreateError)

    def delete_fork_relation(self):
        url = "/projects/%s/fork" % self.id
        r = self.gitlab._raw_delete(url)
        if r.status_code != 200:
            _raise_error_from_response(r, GitlabDeleteError)


class TeamMember(GitlabObject):
    _url = '/user_teams/%(team_id)s/members'
    canUpdate = False
    requiredUrlAttrs = ['teamd_id']
    requiredCreateAttrs = ['access_level']
    shortPrintAttr = 'username'


class TeamProject(GitlabObject):
    _url = '/user_teams/%(team_id)s/projects'
    _constructorTypes = {'owner': 'User', 'namespace': 'Group'}
    canUpdate = False
    requiredCreateAttrs = ['greatest_access_level']
    requiredUrlAttrs = ['team_id']
    shortPrintAttr = 'name'


class Team(GitlabObject):
    _url = '/user_teams'
    shortPrintAttr = 'name'
    requiredCreateAttrs = ['name', 'path']
    canUpdate = False

    def Member(self, id=None, **kwargs):
        return TeamMember._get_list_or_object(self.gitlab, id,
                                              team_id=self.id,
                                              **kwargs)

    def Project(self, id=None, **kwargs):
        return TeamProject._get_list_or_object(self.gitlab, id,
                                               team_id=self.id,
                                               **kwargs)

class ProjectFork(GitlabObject):
    _url = '/projects/fork/%(project_id)s'
    canUpdate = False
    canDelete = False
    canList = False
    canGet = False
    requiredUrlAttrs = ['project_id']

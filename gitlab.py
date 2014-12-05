# -*- coding: utf-8 -*-
#
# Copyright (C) 2013-2014 Gauvain Pocentek <gauvain@pocentek.net>
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

from __future__ import print_function, division, absolute_import

import six

import json
import requests
import sys

from itertools import chain

__title__ = 'python-gitlab'
__version__ = '0.8'
__author__ = 'Gauvain Pocentek'
__email__ = 'gauvain@pocentek.net'
__license__ = 'LGPL3'
__copyright__ = 'Copyright 2013-2014 Gauvain Pocentek'


class jsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, GitlabObject):
            return obj.__dict__
        elif isinstance(obj, Gitlab):
            return {'url': obj._url}
        return json.JSONEncoder.default(self, obj)


class GitlabError(Exception):
    def __init__(self, error_message="", response_code=None,
                 response_body=None):

        Exception.__init__(self, error_message)
        # Http status code
        self.response_code = response_code
        # Full http response
        self.response_body = response_body
        # Parsed error message from gitlab
        self.error_message = error_message

    def __str__(self):
        if self.response_code is not None:
            return "{0}: {1}".format(self.response_code, self.error_message)
        else:
            return "{0}".format(self.error_message)


class GitlabAuthenticationError(GitlabError):
    pass


class GitlabConnectionError(GitlabError):
    pass


class GitlabOperationError(GitlabError):
    pass


class GitlabListError(GitlabOperationError):
    pass


class GitlabGetError(GitlabOperationError):
    pass


class GitlabCreateError(GitlabOperationError):
    pass


class GitlabUpdateError(GitlabOperationError):
    pass


class GitlabDeleteError(GitlabOperationError):
    pass


class GitlabProtectError(GitlabOperationError):
    pass


class GitlabTransferProjectError(GitlabOperationError):
    pass


def _raiseErrorFromResponse(response, error):
    """ Tries to parse gitlab error message from response and raises error.

    If response status code is 401, raises instead GitlabAuthenticationError.
    
    response: requests response object
    error: Error-class to raise. Should be inherited from GitLabError
    """

    try:
        message = response.json()['message']
    except (KeyError, ValueError):
        message = response.content

    if response.status_code == 401:
        error = GitlabAuthenticationError

    raise error(error_message=message,
                response_code=response.status_code,
                response_body=response.content)


class Gitlab(object):
    """Represents a GitLab server connection"""
    def __init__(self, url, private_token=None,
                 email=None, password=None, ssl_verify=True, timeout=None):
        """Stores informations about the server

        url: the URL of the Gitlab server
        private_token: the user private token
        email: the user email/login
        password: the user password (associated with email)
        ssl_verify: (Passed to requests-library)
        timeout: (Passed to requests-library). Timeout to use for requests to
          gitlab server. Float or tuple(Float,Float).
        """
        self._url = '%s/api/v3' % url
        self.timeout = timeout
        self.headers = {}
        self.setToken(private_token)
        self.email = email
        self.password = password
        self.ssl_verify = ssl_verify
        # Gitlab should handle UTF-8
        self.gitlab_encoding = 'UTF-8'

    def auth(self):
        """Performs an authentication using either the private token, or the
        email/password pair.

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
        r = self.rawPost('/session', data, content_type='application/json')

        if r.status_code == 201:
            self.user = CurrentUser(self, r.json())
        else:
            _raiseErrorFromResponse(r, GitlabAuthenticationError)

        self.setToken(self.user.private_token)

    def token_auth(self):
        self.user = CurrentUser(self)

    def setUrl(self, url):
        """Updates the gitlab URL"""
        self._url = '%s/api/v3' % url

    def constructUrl(self, id_, obj, parameters):
        args = _sanitize_dict(parameters)
        url = obj._url % args
        if id_ is not None:
            url = '%s%s/%s' % (self._url, url, str(id_))
        else:
            url = '%s%s' % (self._url, url)
        return url

    def _createHeaders(self, content_type=None, headers={} ):
        request_headers = self.headers.copy()
        request_headers.update(headers)
        if content_type is not None:
            request_headers['Content-type'] = content_type
        return request_headers

    def setToken(self, token):
        """Sets the private token for authentication"""
        self.private_token = token if token else None
        if token:
            self.headers["PRIVATE-TOKEN"] = token
        elif "PRIVATE-TOKEN" in self.headers:
            del self.headers["PRIVATE-TOKEN"]

    def setCredentials(self, email, password):
        """Sets the email/login and password for authentication"""
        self.email = email
        self.password = password

    def rawGet(self, path, content_type=None, **kwargs):
        url = '%s%s' % (self._url, path)
        headers = self._createHeaders(content_type)

        try:
            return requests.get(url,
                                params=kwargs,
                                headers=headers,
                                verify=self.ssl_verify,
                                timeout=self.timeout)
        except:
            raise GitlabConnectionError(
                "Can't connect to GitLab server (%s)" % self._url)

    def rawPost(self, path, data=None, content_type=None, **kwargs):
        url = '%s%s' % (self._url, path)
        headers = self._createHeaders(content_type)
        try:
            return requests.post(url, params=kwargs, data=data,
                                 headers=headers,
                                 verify=self.ssl_verify,
                                 timeout=self.timeout)
        except:
            raise GitlabConnectionError(
                "Can't connect to GitLab server (%s)" % self._url)

    def rawPut(self, path, data=None, content_type=None, **kwargs):
        url = '%s%s' % (self._url, path)
        headers = self._createHeaders(content_type)

        try:
            return requests.put(url, data=data, params=kwargs,
                                headers=headers,
                                verify=self.ssl_verify,
                                timeout=self.timeout)
        except:
            raise GitlabConnectionError(
                "Can't connect to GitLab server (%s)" % self._url)

    def rawDelete(self, path, content_type=None, **kwargs):
        url = '%s%s' % (self._url, path)
        headers = self._createHeaders(content_type)

        try:
            return requests.delete(url,
                                   params=kwargs,
                                   headers=headers,
                                   verify=self.ssl_verify,
                                   timeout=self.timeout)
        except:
            raise GitlabConnectionError(
                "Can't connect to GitLab server (%s)" % self._url)

    def list(self, obj_class, **kwargs):
        missing = []
        for k in chain(obj_class.requiredUrlAttrs,
                       obj_class.requiredListAttrs):
            if k not in kwargs:
                missing.append(k)
        if missing:
            raise GitlabListError('Missing attribute(s): %s' %
                                  ", ".join(missing))

        url = self.constructUrl(id_=None, obj=obj_class, parameters=kwargs)
        headers = self._createHeaders()

        # Remove attributes that are used in url so that there is only
        # url-parameters left
        params = kwargs.copy()
        for attribute in obj_class.requiredUrlAttrs:
            del params[attribute]

        try:
            r = requests.get(url, params=params, headers=headers,
                             verify=self.ssl_verify,
                             timeout=self.timeout)
        except:
            raise GitlabConnectionError(
                "Can't connect to GitLab server (%s)" % self._url)

        if r.status_code == 200:
            cls = obj_class
            if obj_class._returnClass:
                cls = obj_class._returnClass

            cls_kwargs = kwargs.copy()

            # Add _created manually, because we are not creating objects
            # through normal path
            cls_kwargs['_created'] = True

            # Remove parameters from kwargs before passing it to constructor
            for key in ['page', 'per_page', 'sudo']:
                if key in cls_kwargs:
                    del cls_kwargs[key]

            return [cls(self, item, **cls_kwargs) for item in r.json() if item is not None]
        else:
            _raiseErrorFromResponse(r, GitlabListError)


    def get(self, obj_class, id=None, **kwargs):
        missing = []
        for k in chain(obj_class.requiredUrlAttrs,
                       obj_class.requiredGetAttrs):
            if k not in kwargs:
                missing.append(k)
        if missing:
            raise GitlabGetError('Missing attribute(s): %s' %
                                 ", ".join(missing))

        url = self.constructUrl(id_=id, obj=obj_class, parameters=kwargs)
        headers = self._createHeaders()

        # Remove attributes that are used in url so that there is only
        # url-parameters left
        params = kwargs.copy()
        for attribute in obj_class.requiredUrlAttrs:
            del params[attribute]

        try:
            r = requests.get(url, params=params, headers=headers,
                             verify=self.ssl_verify, timeout=self.timeout)
        except:
            raise GitlabConnectionError(
                "Can't connect to GitLab server (%s)" % self._url)

        if r.status_code == 200:
            return r.json()
        else:
            _raiseErrorFromResponse(r, GitlabGetError)


    def delete(self, obj, **kwargs):
        params = obj.__dict__.copy()
        params.update(kwargs)
        missing = []
        for k in chain(obj.requiredUrlAttrs, obj.requiredDeleteAttrs):
            if k not in params:
                missing.append(k)
        if missing:
            raise GitlabDeleteError('Missing attribute(s): %s' %
                                    ", ".join(missing))

        url = self.constructUrl(id_=obj.id, obj=obj, parameters=params)
        headers = self._createHeaders()

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
        except:
            raise GitlabConnectionError(
                "Can't connect to GitLab server (%s)" % self._url)

        if r.status_code == 200:
            return True
        else:
            _raiseErrorFromResponse(r, GitlabDeleteError)

    def create(self, obj, **kwargs):
        params = obj.__dict__.copy()
        params.update(kwargs)
        missing = []
        for k in chain(obj.requiredUrlAttrs, obj.requiredCreateAttrs):
            if k not in params:
                missing.append(k)
        if missing:
            raise GitlabCreateError('Missing attribute(s): %s' %
                                    ", ".join(missing))

        url = self.constructUrl(id_=None, obj=obj, parameters=params)
        headers = self._createHeaders(content_type="application/json")

        # build data that can really be sent to server
        data = obj._dataForGitlab(extra_parameters=kwargs)

        try:
            r = requests.post(url, data=data,
                              headers=headers,
                              verify=self.ssl_verify,
                              timeout=self.timeout)
        except:
            raise GitlabConnectionError(
                "Can't connect to GitLab server (%s)" % self._url)

        if r.status_code == 201:
            return r.json()
        else:
            _raiseErrorFromResponse(r, GitlabCreateError)

    def update(self, obj, **kwargs):
        params = obj.__dict__.copy()
        params.update(kwargs)
        missing = []
        for k in chain(obj.requiredUrlAttrs, obj.requiredCreateAttrs):
            if k not in params:
                missing.append(k)
        if missing:
            raise GitlabUpdateError('Missing attribute(s): %s' %
                                    ", ".join(missing))
        url = self.constructUrl(id_=obj.id, obj=obj, parameters=params)
        headers = self._createHeaders(content_type="application/json")

        # build data that can really be sent to server
        data = obj._dataForGitlab()

        try:
            r = requests.put(url, data=data,
                             headers=headers,
                             verify=self.ssl_verify,
                             timeout=self.timeout)
        except:
            raise GitlabConnectionError(
                "Can't connect to GitLab server (%s)" % self._url)

        if r.status_code == 200:
            return r.json()
        else:
            _raiseErrorFromResponse(r, GitlabUpdateError)

    def Hook(self, id=None, **kwargs):
        """Creates/tests/lists system hook(s) known by the GitLab server.

        If id is None, returns a list of hooks.

        If id is an integer, tests the matching hook.

        If id is a dict, creates a new object using attributes provided. The
        object is NOT saved on the server. Use the save() method on the object
        to write it on the server.
        """
        return Hook._getListOrObject(self, id, **kwargs)

    def Project(self, id=None, **kwargs):
        """Creates/gets/lists project(s) known by the GitLab server.

        If id is None, returns a list of projects.

        If id is an integer, returns the matching project (or raises a
        GitlabGetError if not found)

        If id is a dict, creates a new object using attributes provided. The
        object is NOT saved on the server. Use the save() method on the object
        to write it on the server.
        """
        return Project._getListOrObject(self, id, **kwargs)

    def UserProject(self, id=None, **kwargs):
        """Creates a project for a user.

        id must be a dict.
        """
        return UserProject._getListOrObject(self, id, **kwargs)

    def _list_projects(self, url, **kwargs):
        r = self.rawGet(url, **kwargs)
        if r.status_code != 200:
            _raiseErrorFromResponse(r, GitlabListError)

        l = []
        for o in r.json():
            l.append(Project(self, o))

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
        """Creates/gets/lists group(s) known by the GitLab server.

        If id is None, returns a list of groups.

        If id is an integer, returns the matching group (or raises a
        GitlabGetError if not found)

        If id is a dict, creates a new object using attributes provided. The
        object is NOT saved on the server. Use the save() method on the object
        to write it on the server.
        """
        return Group._getListOrObject(self, id, **kwargs)

    def Issue(self, id=None, **kwargs):
        """Lists issues(s) known by the GitLab server.

        Does not support creation or getting a single issue unlike other
        methods in this class yet.
        """
        return Issue._getListOrObject(self, id, **kwargs)

    def User(self, id=None, **kwargs):
        """Creates/gets/lists users(s) known by the GitLab server.

        If id is None, returns a list of users.

        If id is an integer, returns the matching user (or raises a
        GitlabGetError if not found)

        If id is a dict, creates a new object using attributes provided. The
        object is NOT saved on the server. Use the save() method on the object
        to write it on the server.
        """
        return User._getListOrObject(self, id, **kwargs)

    def Team(self, id=None, **kwargs):
        """Creates/gets/lists team(s) known by the GitLab server.

        If id is None, returns a list of teams.

        If id is an integer, returns the matching team (or raises a
        GitlabGetError if not found)

        If id is a dict, create a new object using attributes provided. The
        object is NOT saved on the server. Use the save() method on the object
        to write it on the server.
        """
        return Team._getListOrObject(self, id, **kwargs)


def _get_display_encoding():
    return sys.stdout.encoding or sys.getdefaultencoding()


def _sanitize(value):
    if isinstance(value, six.string_types):
        return value.replace('/', '%2F')
    return value


def _sanitize_dict(src):
    return dict((k, _sanitize(v)) for k, v in src.items())


class GitlabObject(object):
    _url = None
    _returnClass = None
    _constructorTypes = None
    # Tells if _getListOrObject should return list or object when id is None
    getListWhenNoId = True
    canGet = True
    canList = True
    canCreate = True
    canUpdate = True
    canDelete = True
    requiredUrlAttrs = []
    requiredListAttrs = []
    requiredGetAttrs = []
    requiredDeleteAttrs = []
    requiredCreateAttrs = []
    optionalCreateAttrs = []
    idAttr = 'id'
    shortPrintAttr = None

    def _dataForGitlab(self, extra_parameters={}):
        data = {}
        for attribute in chain(self.requiredCreateAttrs,
                               self.optionalCreateAttrs):
            if hasattr(self, attribute):
                data[attribute] = getattr(self,attribute)

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
    def _getListOrObject(cls, gl, id, **kwargs):
        if id is None and cls.getListWhenNoId:
            return cls.list(gl, **kwargs)
        else:
            return cls(gl, id, **kwargs)

    def _getObject(self, k, v):
        if self._constructorTypes and k in self._constructorTypes:
            return globals()[self._constructorTypes[k]](self.gitlab, v)
        else:
            return v

    def _setFromDict(self, data):
        for k, v in data.items():
            if isinstance(v, list):
                self.__dict__[k] = []
                for i in v:
                    self.__dict__[k].append(self._getObject(k, i))
            elif v is None:
                self.__dict__[k] = None
            else:
                self.__dict__[k] = self._getObject(k, v)

    def _create(self, **kwargs):
        if not self.canCreate:
            raise NotImplementedError

        json = self.gitlab.create(self, **kwargs)
        self._setFromDict(json)
        self._created = True

    def _update(self, **kwargs):
        if not self.canUpdate:
            raise NotImplementedError

        json = self.gitlab.update(self, **kwargs)
        self._setFromDict(json)

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

        if data is None or isinstance(data, six.integer_types) or\
                isinstance(data, six.string_types):
            if not self.canGet:
                raise NotImplementedError
            data = self.gitlab.get(self.__class__, data, **kwargs)
            # Object is created because we got it from api
            self._created = True

        self._setFromDict(data)

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
                           'bio', 'admin', 'can_create_group', 'website_url']


    def Key(self, id=None, **kwargs):
        return UserKey._getListOrObject(self.gitlab, id,
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
        return CurrentUserKey._getListOrObject(self.gitlab, id, **kwargs)

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
        return GroupMember._getListOrObject(self.gitlab, id,
                                            group_id=self.id,
                                            **kwargs)

    def transfer_project(self, id, **kwargs):
        url = '/groups/%d/projects/%d' % (self.id, id)
        r = self.gitlab.rawPost(url, None, **kwargs)
        if r.status_code != 201:
            _raiseErrorFromResponse(r, GitlabTransferProjectError)

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
        r = self.gitlab.rawPut(url, data=None, content_type=None, **kwargs)

        if r.status_code == 200:
            if protect:
                self.protected = protect
            else:
                del self.protected
        else:
            _raiseErrorFromResponse(r, GitlabProtectError)

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
        r = self.gitlab.rawGet(url, **kwargs)
        if r.status_code == 200:
            return r.json()
        else:
            _raiseErrorFromResponse(r, GitlabGetError)


    def blob(self, filepath, **kwargs):
        url = '/projects/%(project_id)s/repository/blobs/%(commit_id)s' % \
              {'project_id': self.project_id, 'commit_id': self.id}
        url += '?filepath=%s' % filepath
        r = self.gitlab.rawGet(url, **kwargs)
        if r.status_code == 200:
            return r.content
        else:
            _raiseErrorFromResponse(r, GitlabGetError)


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

    def Note(self, id=None, **kwargs):
        return ProjectIssueNote._getListOrObject(self.gitlab, id,
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
    canUpdate = False
    canDelete = False
    requiredUrlAttrs = ['project_id', 'merge_request_id']
    requiredCreateAttrs = ['body']


class ProjectMergeRequest(GitlabObject):
    _url = '/projects/%(project_id)s/merge_requests'
    _constructorTypes = {'author': 'User', 'assignee': 'User'}
    canDelete = False
    requiredUrlAttrs = ['project_id']
    requiredCreateAttrs = ['source_branch', 'target_branch', 'title']
    optionalCreateAttrs = ['assignee_id']

    def Note(self, id=None, **kwargs):
        return ProjectMergeRequestNote._getListOrObject(
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
    shortPrintAttr = 'name'


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
        url = "/projects/%(project_id)s/snippets/%(snippet_id)s/raw" % \
            {'project_id': self.project_id, 'snippet_id': self.id}
        r = self.gitlab.rawGet(url, **kwargs)

        if r.status_code == 200:
            return r.content
        else:
            _raiseErrorFromResponse(r, GitlabGetError)

    def Note(self, id=None, **kwargs):
        return ProjectSnippetNote._getListOrObject(self.gitlab, id,
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
    canUpdate = False
    requiredCreateAttrs = ['name']
    optionalCreateAttrs = ['default_branch', 'issues_enabled', 'wall_enabled',
                           'merge_requests_enabled', 'wiki_enabled',
                           'snippets_enabled', 'public', 'visibility_level',
                           'namespace_id', 'description', 'path', 'import_url']

    shortPrintAttr = 'path'

    def Branch(self, id=None, **kwargs):
        return ProjectBranch._getListOrObject(self.gitlab, id,
                                              project_id=self.id,
                                              **kwargs)

    def Commit(self, id=None, **kwargs):
        return ProjectCommit._getListOrObject(self.gitlab, id,
                                              project_id=self.id,
                                              **kwargs)

    def Event(self, id=None, **kwargs):
        return ProjectEvent._getListOrObject(self.gitlab, id,
                                             project_id=self.id,
                                             **kwargs)

    def Hook(self, id=None, **kwargs):
        return ProjectHook._getListOrObject(self.gitlab, id,
                                            project_id=self.id,
                                            **kwargs)

    def Key(self, id=None, **kwargs):
        return ProjectKey._getListOrObject(self.gitlab, id,
                                           project_id=self.id,
                                           **kwargs)

    def Issue(self, id=None, **kwargs):
        return ProjectIssue._getListOrObject(self.gitlab, id,
                                             project_id=self.id,
                                             **kwargs)

    def Member(self, id=None, **kwargs):
        return ProjectMember._getListOrObject(self.gitlab, id,
                                              project_id=self.id,
                                              **kwargs)

    def MergeRequest(self, id=None, **kwargs):
        return ProjectMergeRequest._getListOrObject(self.gitlab, id,
                                                    project_id=self.id,
                                                    **kwargs)

    def Milestone(self, id=None, **kwargs):
        return ProjectMilestone._getListOrObject(self.gitlab, id,
                                                 project_id=self.id,
                                                 **kwargs)

    def Note(self, id=None, **kwargs):
        return ProjectNote._getListOrObject(self.gitlab, id,
                                            project_id=self.id,
                                            **kwargs)

    def Snippet(self, id=None, **kwargs):
        return ProjectSnippet._getListOrObject(self.gitlab, id,
                                               project_id=self.id,
                                               **kwargs)

    def Label(self, id=None, **kwargs):
        return ProjectLabel._getListOrObject(self.gitlab, id,
                                             project_id=self.id,
                                             **kwargs)

    def File(self, id=None, **kwargs):
        return ProjectFile._getListOrObject(self.gitlab, id,
                                            project_id=self.id,
                                            **kwargs)

    def Tag(self, id=None, **kwargs):
        return ProjectTag._getListOrObject(self.gitlab, id,
                                           project_id=self.id,
                                           **kwargs)

    def tree(self, path='', ref_name='', **kwargs):
        url = "%s/%s/repository/tree" % (self._url, self.id)
        url += '?path=%s&ref_name=%s' % (path, ref_name)
        r = self.gitlab.rawGet(url, **kwargs)
        if r.status_code == 200:
            return r.json()
        else:
            _raiseErrorFromResponse(r, GitlabGetError)

    def blob(self, sha, filepath, **kwargs):
        url = "%s/%s/repository/blobs/%s" % (self._url, self.id, sha)
        url += '?filepath=%s' % (filepath)
        r = self.gitlab.rawGet(url, **kwargs)
        if r.status_code == 200:
            return r.content
        else:
            _raiseErrorFromResponse(r, GitlabGetError)

    def archive(self, sha=None, **kwargs):
        url = '/projects/%s/repository/archive' % self.id
        if sha:
            url += '?sha=%s' % sha
        r = self.gitlab.rawGet(url, **kwargs)
        if r.status_code == 200:
            return r.content
        else:
            _raiseErrorFromResponse(r, GitlabGetError)

    def create_file(self, path, branch, content, message, **kwargs):
        url = "/projects/%s/repository/files" % self.id
        url += "?file_path=%s&branch_name=%s&content=%s&commit_message=%s" % \
            (path, branch, content, message)
        r = self.gitlab.rawPost(url, data=None, content_type=None, **kwargs)
        if r.status_code != 201:
            _raiseErrorFromResponse(r, GitlabCreateError)

    def update_file(self, path, branch, content, message, **kwargs):
        url = "/projects/%s/repository/files" % self.id
        url += "?file_path=%s&branch_name=%s&content=%s&commit_message=%s" % \
            (path, branch, content, message)
        r = self.gitlab.rawPut(url, data=None, content_type=None, **kwargs)
        if r.status_code != 200:
            _raiseErrorFromResponse(r, GitlabUpdateError)

    def delete_file(self, path, branch, message, **kwargs):
        url = "/projects/%s/repository/files" % self.id
        url += "?file_path=%s&branch_name=%s&commit_message=%s" % \
            (path, branch, message)
        r = self.gitlab.rawDelete(url, **kwargs)
        if r.status_code != 200:
            _raiseErrorFromResponse(r, GitlabDeleteError)


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
        return TeamMember._getListOrObject(self.gitlab, id,
                                           team_id=self.id,
                                           **kwargs)

    def Project(self, id=None, **kwargs):
        return TeamProject._getListOrObject(self.gitlab, id,
                                            team_id=self.id,
                                            **kwargs)

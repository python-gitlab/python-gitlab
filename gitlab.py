#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2013 Gauvain Pocentek <gauvain@pocentek.net>
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

import json
import requests

__title__ = 'python-gitlab'
__version__ = '0.1'
__author__ = 'Gauvain Pocentek'
__email__ = 'gauvain@pocentek.net'
__license__ = 'LGPL3'
__copyright__ = 'Copyright 2013 Gauvain Pocentek'


class jsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, GitlabObject):
            return obj.__dict__
        elif isinstance(obj, Gitlab):
            return {'url': obj._url}
        return json.JSONEncoder.default(self, obj)


class GitlabConnectionError(Exception):
    pass


class GitlabListError(Exception):
    pass


class GitlabGetError(Exception):
    pass


class GitlabCreateError(Exception):
    pass


class GitlabUpdateError(Exception):
    pass


class GitlabDeleteError(Exception):
    pass


class GitlabProtectError(Exception):
    pass


class GitlabTransferProjectError(Exception):
    pass


class GitlabAuthenticationError(Exception):
    pass


class Gitlab(object):
    """Represents a GitLab server connection"""
    def __init__(self, url, private_token=None, email=None, password=None):
        """Stores informations about the server

        url: the URL of the Gitlab server
        private_token: the user private token
        email: the user email/login
        password: the user password (associated with email)
        """
        self._url = '%s/api/v3' % url
        self.private_token = private_token
        self.email = email
        self.password = password

    def auth(self):
        """Performs an authentication using either the private token, or the
        email/password pair.

        The user attribute will hold a CurrentUser object on success.
        """
        r = False
        if self.private_token:
            r = self.token_auth()

        if not r:
            self.credentials_auth()

    def credentials_auth(self):
        if not self.email or not self.password:
            raise GitlabAuthenticationError("Missing email/password")

        r = self.rawPost('/session',
                         {'email': self.email, 'password': self.password})
        if r.status_code == 201:
            self.user = CurrentUser(self, r.json())
        else:
            raise GitlabAuthenticationError(r.json()['message'])

        self.private_token = self.user.private_token

    def token_auth(self):
        try:
            self.user = CurrentUser(self)
            return True
        except:
            return False

    def setUrl(self, url):
        """Updates the gitlab URL"""
        self._url = '%s/api/v3' % url

    def setToken(self, token):
        """Sets the private token for authentication"""
        self.private_token = token

    def setCredentials(self, email, password):
        """Sets the email/login and password for authentication"""
        self.email = email
        self.password = password

    def rawGet(self, path, with_token=False):
        url = '%s%s' % (self._url, path)
        if with_token:
            url += "?private_token=%s" % self.private_token

        try:
            r = requests.get(url)
        except:
            raise GitlabConnectionError(
                "Can't connect to GitLab server (%s)" % self._url)

        return r

    def rawPost(self, path, data):
        url = '%s%s' % (self._url, path)
        try:
            r = requests.post(url, data)
        except:
            raise GitlabConnectionError(
                "Can't connect to GitLab server (%s)" % self._url)

        return r

    def rawPut(self, path, with_token=False):
        url = '%s%s' % (self._url, path)
        if with_token:
            url += "?private_token=%s" % self.private_token

        try:
            r = requests.put(url)
        except:
            raise GitlabConnectionError(
                "Can't connect to GitLab server (%s)" % self._url)

        return r

    def list(self, obj_class, **kwargs):
        missing = []
        for k in obj_class.requiredListAttrs:
            if k not in kwargs:
                missing.append (k)
        if missing:
            raise GitlabListError('Missing attribute(s): %s' % \
                    ", ".join(missing))

        url = obj_class._url
        if kwargs:
            url = obj_class._url % kwargs
        url = '%s%s?private_token=%s' % (self._url, url, self.private_token)
        if kwargs:
            url += "&%s" % ("&".join(
                        ["%s=%s" % (k, v) for k, v in kwargs.items()]))

        try:
            r = requests.get(url)
        except:
            raise GitlabConnectionError(
                "Can't connect to GitLab server (%s)" % self._url)

        if r.status_code == 200:
            cls = obj_class
            if obj_class._returnClass:
                cls = obj_class._returnClass
            l = [cls(self, item) for item in r.json()]
            if kwargs:
                for k, v in kwargs.items():
                    if k in ('page', 'per_page'):
                        continue
                    for obj in l:
                        obj.__dict__[k] = str(v)
            return l
        elif r.status_code == 401:
            raise GitlabAuthenticationError(r.json()['message'])
        else:
            raise GitlabGetError('%d: %s' % (r.status_code, r.text))

    def get(self, obj_class, id=None, **kwargs):
        missing = []
        for k in obj_class.requiredGetAttrs:
            if k not in kwargs:
                missing.append (k)
        if missing:
            raise GitlabListError('Missing attribute(s): %s' % \
                    ", ".join(missing))

        url = obj_class._url
        if kwargs:
            url = obj_class._url % kwargs
        if id is not None:
            try:
                url = '%s%s/%d?private_token=%s' % \
                        (self._url, url, id, self.private_token)
            except TypeError:  # id might be a str (ProjectBranch)
                url = '%s%s/%s?private_token=%s' % \
                        (self._url, url, id, self.private_token)
        else:
            url = '%s%s?private_token=%s' % \
                    (self._url, url, self.private_token)

        try:
            r = requests.get(url)
        except:
            raise GitlabConnectionError(
                "Can't connect to GitLab server (%s)" % self._url)

        if r.status_code == 200:
            return r.json()
        elif r.status_code == 401:
            raise GitlabAuthenticationError(r.json()['message'])
        elif r.status_code == 404:
            raise GitlabGetError("Object doesn't exist")
        else:
            raise GitlabGetError('%d: %s' % (r.status_code, r.text))

    def delete(self, obj):
        url = obj._url % obj.__dict__
        url = '%s%s/%d?private_token=%s' % \
                (self._url, url, obj.id, self.private_token)

        try:
            r = requests.delete(url)
        except:
            raise GitlabConnectionError(
                "Can't connect to GitLab server (%s)" % self._url)

        if r.status_code == 200:
            return True
        elif r.status_code == 401:
            raise GitlabAuthenticationError(r.json()['message'])
        else:
            raise GitlabDeleteError(r.json()['message'])
        return False

    def create(self, obj):
        missing = []
        for k in obj.requiredCreateAttrs:
            if k not in obj.__dict__:
                missing.append (k)
        if missing:
            raise GitlabCreateError('Missing attribute(s): %s' % \
                    ", ".join(missing))

        url = obj._url % obj.__dict__
        url = '%s%s?private_token=%s' % (self._url, url, self.private_token)

        print url
        print obj.__dict__

        try:
            # TODO: avoid too much work on the server side by filtering the
            # __dict__ keys
            r = requests.post(url, obj.__dict__)
        except:
            raise GitlabConnectionError(
                "Can't connect to GitLab server (%s)" % self._url)

        if r.status_code == 201:
            return r.json()
        elif r.status_code == 401:
            raise GitlabAuthenticationError(r.json()['message'])
        else:
            raise GitlabCreateError('%d: %s' % (r.status_code, r.text))

    def update(self, obj):
        url = obj._url % obj.__dict__
        url = '%s%s/%d?private_token=%s' % \
                (self._url, url, obj.id, self.private_token)

        # build a dict of data that can really be sent to server
        d = {}
        for k, v in obj.__dict__.items():
            if type(v) in (int, str, unicode, bool):
                d[k] = str(v)

        try:
            r = requests.put(url, d)
        except:
            raise GitlabConnectionError(
                "Can't connect to GitLab server (%s)" % self._url)

        if r.status_code == 200:
            return r.json()
        elif r.status_code == 401:
            raise GitlabAuthenticationError(r.json()['message'])
        else:
            raise GitlabUpdateError('%d: %s' % (r.status_code, r.text))

    def _getListOrObject(self, cls, id, **kwargs):
        if id is None:
            return cls.list(self, **kwargs)
        else:
            return cls(self, id, **kwargs)

    def Hook(self, id=None, **kwargs):
        """Creates/tests/lists system hook(s) known by the GitLab server.

        If id is None, returns a list of hooks.

        If id is an integer, test the matching hook.

        If id is a dict, create a new object using attributes provided. The
        object is NOT saved on the server. Use the save() method on the object
        to write it on the server.
        """
        return self._getListOrObject(Hook, id, **kwargs)

    def Project(self, id=None, **kwargs):
        """Creates/gets/lists project(s) known by the GitLab server.

        If id is None, returns a list of projects.

        If id is an integer, returns the matching project (or raise a
        GitlabGetError if not found)

        If id is a dict, create a new object using attributes provided. The
        object is NOT saved on the server. Use the save() method on the object
        to write it on the server.
        """
        return self._getListOrObject(Project, id, **kwargs)

    def Group(self, id=None, **kwargs):
        """Creates/gets/lists groups(s) known by the GitLab server.

        If id is None, returns a list of projects.

        If id is an integer, returns the matching project (or raise a
        GitlabGetError if not found)

        If id is a dict, create a new object using attributes provided. The
        object is NOT saved on the server. Use the save() method on the object
        to write it on the server.
        """
        return self._getListOrObject(Group, id, **kwargs)

    def Issue(self, id=None, **kwargs):
        """Lists issues(s) known by the GitLab server."""
        return self._getListOrObject(Issue, id, **kwargs)

    def User(self, id=None, **kwargs):
        """Creates/gets/lists users(s) known by the GitLab server.

        If id is None, returns a list of projects.

        If id is an integer, returns the matching project (or raise a
        GitlabGetError if not found)

        If id is a dict, create a new object using attributes provided. The
        object is NOT saved on the server. Use the save() method on the object
        to write it on the server.
        """
        return self._getListOrObject(User, id, **kwargs)

    def Team(self, id=None, **kwargs):
        """Creates/gets/lists team(s) known by the GitLab server.

        If id is None, returns a list of teams.

        If id is an integer, returns the matching project (or raise a
        GitlabGetError if not found)

        If id is a dict, create a new object using attributes provided. The
        object is NOT saved on the server. Use the save() method on the object
        to write it on the server.
        """
        return self._getListOrObject(Team, id, **kwargs)


class GitlabObject(object):
    _url = None
    _returnClass = None
    _constructorTypes = None
    canGet = True
    canList = True
    canCreate = True
    canUpdate = True
    canDelete = True
    requiredListAttrs = []
    requiredGetAttrs = []
    requiredCreateAttrs = []
    optionalCreateAttrs = []
    idAttr = 'id'
    shortPrintAttr = None

    @classmethod
    def list(cls, gl, **kwargs):
        if not cls.canList:
            raise NotImplementedError

        if not cls._url:
            raise NotImplementedError

        return gl.list(cls, **kwargs)

    def _getListOrObject(self, cls, id, **kwargs):
        if id is None:
            if not cls.canList:
                raise GitlabGetError

            return cls.list(self.gitlab, **kwargs)
        elif isinstance(id, dict):
            if not cls.canCreate:
                raise GitlabCreateError

            return cls(self.gitlab, id, **kwargs)
        else:
            if not cls.canGet:
                raise GitlabGetError

            return cls(self.gitlab, id, **kwargs)

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
            elif v:
                self.__dict__[k] = self._getObject(k, v)
            else:  # None object
                self.__dict__[k] = None

    def _create(self):
        if not self.canCreate:
            raise NotImplementedError

        json = self.gitlab.create(self)
        self._setFromDict(json)

    def _update(self):
        if not self.canUpdate:
            raise NotImplementedError

        json = self.gitlab.update(self)
        self._setFromDict(json)

    def save(self):
        if hasattr(self, 'id'):
            self._update()
        else:
            self._create()

    def delete(self):
        if not self.canDelete:
            raise NotImplementedError

        if not hasattr(self, 'id'):
            raise GitlabDeleteError

        return self.gitlab.delete(self)

    def __init__(self, gl, data=None, **kwargs):
        self.gitlab = gl

        if data is None or isinstance(data, int) or isinstance(data, str):
            data = self.gitlab.get(self.__class__, data, **kwargs)

        self._setFromDict(data)

        if kwargs:
            for k, v in kwargs.items():
                self.__dict__[k] = v

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
            print ("%s%s: %s" % (" " * depth * 2,
                                 self.shortPrintAttr.replace('_', '-'),
                                 self.__dict__[self.shortPrintAttr]))

    @staticmethod
    def _obj_to_str(obj):
        if isinstance(obj, dict):
            s = ", ".join(["%s: %s" % (x, GitlabObject._obj_to_str(y)) for (x, y) in obj.items()])
            return "{ %s }" % s
        elif isinstance(obj, list):
            s = ", ".join([GitlabObject._obj_to_str(x) for x in obj])
            return "[ %s ]" %s
        else:
            return str(obj)

    def pretty_print(self, depth=0):
        id = self.__dict__[self.idAttr]
        print("%s%s: %s" % (" " * depth * 2, self.idAttr, id))
        for k in sorted(self.__dict__.keys()):
            if k == self.idAttr:
                continue
            v = self.__dict__[k]
            pretty_k = k.replace('_', '-')
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


class User(GitlabObject):
    _url = '/users'
    shortPrintAttr = 'username'
    requiredCreateAttrs = ['email', 'password', 'username', 'name']
    optionalCreateAttrs = ['skype', 'linkedin', 'twitter', 'projects_limit',
                           'extern_uid', 'provider', 'bio']


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
        if id is None:
            return CurrentUserKey.list(self.gitlab, **kwargs)
        else:
            return CurrentUserKey(self.gitlab, id)


class Group(GitlabObject):
    _url = '/groups'
    _constructorTypes = {'projects': 'Project'}
    requiredCreateAttrs = ['name', 'path']
    shortPrintAttr = 'name'

    def transfer_project(self, id):
        url = '/groups/%d/projects/%d?private_token=%s' % \
                (self.id, id, self.gitlab.private_token)
        r = self.gitlab.rawPost(url, None)
        if r.status_code != 201:
            raise GitlabTransferProjectError()


class Hook(GitlabObject):
    _url = '/hooks'
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
    idAttr = 'name'
    canDelete = False
    canUpdate = False
    canCreate = False
    requiredGetAttrs = ['project_id']
    requiredListAttrs = ['project_id']
    _constructorTypes = {'commit': 'ProjectCommit'}

    def protect(self, protect=True):
        url = self._url % {'project_id': self.project_id}
        if protect:
            url = "%s/%s/protect" % (url, self.name)
        else:
            url = "%s/%s/unprotect" % (url, self.name)
        r = self.gitlab.rawPut(url, True)

        if r.status_code == 200:
            if protect:
                self.protected = protect
            else:
                del self.protected
        else:
            raise GitlabProtectError

    def unprotect(self):
        self.protect(False)


class ProjectCommit(GitlabObject):
    _url = '/projects/%(project_id)s/repository/commits'
    canGet = False
    canDelete = False
    canUpdate = False
    canCreate = False
    requiredListAttrs = ['project_id']
    shortPrintAttr = 'title'


class ProjectKey(GitlabObject):
    _url = '/projects/%(project_id)s/keys'
    canUpdate = False
    requiredListAttrs = ['project_id']
    requiredGetAttrs = ['project_id']
    requiredCreateAttrs = ['project_id', 'title', 'key']


class ProjectHook(GitlabObject):
    _url = '/projects/%(project_id)s/hooks'
    requiredListAttrs = ['project_id']
    requiredGetAttrs = ['project_id']
    requiredCreateAttrs = ['project_id', 'url']
    shortPrintAttr = 'url'


class ProjectIssueNote(GitlabObject):
    _url = '/projects/%(project_id)s/issues/%(issue_id)s/notes'
    _constructorTypes = {'author': 'User'}
    canUpdate = False
    canDelete = False
    requiredListAttrs = ['project_id', 'issue_id']
    requiredGetAttrs = ['project_id', 'issue_id']
    requiredCreateAttrs = ['project_id', 'body']


class ProjectIssue(GitlabObject):
    _url = '/projects/%(project_id)s/issues/'
    _constructorTypes = {'author': 'User', 'assignee': 'User',
                         'milestone': 'ProjectMilestone'}
    canDelete = False
    requiredListAttrs = ['project_id']
    requiredGetAttrs = ['project_id']
    requiredCreateAttrs = ['project_id', 'title']
    optionalCreateAttrs = ['description', 'assignee_id', 'milestone_id',
                           'labels']
    shortPrintAttr = 'title'

    def Note(self, id=None, **kwargs):
        return self._getListOrObject(ProjectIssueNote, id,
                                     project_id=self.project_id,
                                     issue_id=self.id,
                                     **kwargs)


class ProjectMember(GitlabObject):
    _url = '/projects/%(project_id)s/members'
    _returnClass = User
    requiredListAttrs = ['project_id']
    requiredGetAttrs = ['project_id']
    requiredCreateAttrs = ['project_id', 'user_id', 'access_level']
    shortPrintAttr = 'username'


class ProjectNote(GitlabObject):
    _url = '/projects/%(project_id)s/notes'
    _constructorTypes = {'author': 'User'}
    canUpdate = False
    canDelete = False
    requiredListAttrs = ['project_id']
    requiredGetAttrs = ['project_id']
    requiredCreateAttrs = ['project_id', 'body']


class ProjectTag(GitlabObject):
    _url = '/projects/%(project_id)s/repository/tags'
    idAttr = 'name'
    canGet = False
    canDelete = False
    canUpdate = False
    canCreate = False
    requiredListAttrs = ['project_id']
    shortPrintAttr = 'name'


class ProjectMergeRequestNote(GitlabObject):
    _url = '/projects/%(project_id)s/merge_requests/%(merge_request_id)s/notes'
    _constructorTypes = {'author': 'User'}
    canGet = False
    canCreate = False
    canUpdate = False
    canDelete = False
    requiredListAttrs = ['project_id', 'merge_request_id']


class ProjectMergeRequest(GitlabObject):
    _url = '/projects/%(project_id)s/merge_request'
    _constructorTypes = {'author': 'User', 'assignee': 'User'}
    canDelete = False
    requiredListAttrs = ['project_id']
    requiredGetAttrs = ['project_id']
    requiredCreateAttrs = ['project_id', 'source_branch', 'target_branch', 'title']
    optionalCreateAttrs = ['assignee_id']

    def Note(self, id=None, **kwargs):
        return self._getListOrObject(ProjectMergeRequestNote, id,
                                     project_id=self.id,
                                     merge_request_id=self.id,
                                     **kwargs)


class ProjectMilestone(GitlabObject):
    _url = '/projects/%(project_id)s/milestones'
    canDelete = False
    requiredListAttrs = ['project_id']
    requiredGetAttrs = ['project_id']
    requiredCreateAttrs = ['project_id', 'title']
    optionalCreateAttrs = ['description', 'due_date']
    shortPrintAttr = 'title'


class ProjectSnippetNote(GitlabObject):
    _url = '/projects/%(project_id)s/snippets/%(snippet_id)s/notes'
    _constructorTypes = {'author': 'User'}
    canUpdate = False
    canDelete = False
    requiredListAttrs = ['project_id', 'snippet_id']
    requiredGetAttrs = ['project_id', 'snippet_id']
    requiredCreateAttrs = ['project_id', 'snippet_id', 'body']


class ProjectSnippet(GitlabObject):
    _url = '/projects/%(project_id)s/snippets'
    _constructorTypes = {'author': 'User'}
    requiredListAttrs = ['project_id']
    requiredGetAttrs = ['project_id']
    requiredCreateAttrs = ['project_id', 'title', 'file_name', 'code']
    optionalCreateAttrs = ['lifetime']
    shortPrintAttr = 'title'

    def Content(self):
        url = "/projects/%(project_id)s/snippets/%(snippet_id)s/raw" % \
            {'project_id': self.project_id, 'snippet_id': self.id}
        r = self.gitlab.rawGet(url, True)

        if r.status_code == 200:
            return r.content
        else:
            raise GitlabGetError

    def Note(self, id=None, **kwargs):
        return self._getListOrObject(ProjectSnippetNote, id,
                                     project_id=self.project_id,
                                     snippet_id=self.id,
                                     **kwargs)


class Project(GitlabObject):
    _url = '/projects'
    _constructorTypes = {'owner': 'User', 'namespace': 'Group'}
    canUpdate = False
    canDelete = False
    requiredCreateAttrs = ['name']
    optionalCreateAttrs = ['default_branch', 'issues_enabled', 'wall_enabled',
                           'merge_requests_enabled', 'wiki_enabled',
                           'namespace_id']
    shortPrintAttr = 'path'

    def Branch(self, id=None, **kwargs):
        return self._getListOrObject(ProjectBranch, id,
                                     project_id=self.id,
                                     **kwargs)

    def Commit(self, id=None, **kwargs):
        return self._getListOrObject(ProjectCommit, id,
                                     project_id=self.id,
                                     **kwargs)

    def Hook(self, id=None, **kwargs):
        return self._getListOrObject(ProjectHook, id,
                                     project_id=self.id,
                                     **kwargs)

    def Key(self, id=None, **kwargs):
        return self._getListOrObject(ProjectKey, id,
                                     project_id=self.id,
                                     **kwargs)

    def Issue(self, id=None, **kwargs):
        return self._getListOrObject(ProjectIssue, id,
                                     project_id=self.id,
                                     **kwargs)

    def Member(self, id=None, **kwargs):
        return self._getListOrObject(ProjectMember, id,
                                     project_id=self.id,
                                     **kwargs)

    def MergeRequest(self, id=None, **kwargs):
        return self._getListOrObject(ProjectMergeRequest, id,
                                     project_id=self.id,
                                     **kwargs)

    def Milestone(self, id=None, **kwargs):
        return self._getListOrObject(ProjectMilestone, id,
                                     project_id=self.id,
                                     **kwargs)

    def Note(self, id=None, **kwargs):
        return self._getListOrObject(ProjectNote, id,
                                     project_id=self.id,
                                     **kwargs)

    def Snippet(self, id=None, **kwargs):
        return self._getListOrObject(ProjectSnippet, id,
                                     project_id=self.id,
                                     **kwargs)

    def Tag(self, id=None, **kwargs):
        return self._getListOrObject(ProjectTag, id,
                                     project_id=self.id,
                                     **kwargs)


class TeamMember(GitlabObject):
    _url = '/user_teams/%(team_id)s/members'
    canUpdate = False
    requiredCreateAttrs = ['team_id', 'user_id', 'access_level']
    requiredDeleteAttrs = ['team_id']
    requiredGetAttrs = ['team_id']
    requiredListAttrs = ['team_id']
    shortPrintAttr = 'username'


class TeamProject(GitlabObject):
    _url = '/user_teams/%(team_id)s/projects'
    _constructorTypes = {'owner': 'User', 'namespace': 'Group'}
    canUpdate = False
    requiredCreateAttrs = ['team_id', 'project_id', 'greatest_access_level']
    requiredDeleteAttrs = ['team_id', 'project_id']
    requiredGetAttrs = ['team_id']
    requiredListAttrs = ['team_id']
    shortPrintAttr = 'name'


class Team(GitlabObject):
    _url = '/user_teams'
    shortPrintAttr = 'name'
    requiredCreateAttrs = ['name', 'path']
    canUpdate = False

    def Member(self, id=None, **kwargs):
        return self._getListOrObject(TeamMember, id,
                                     team_id=self.id,
                                     **kwargs)

    def Project(self, id=None, **kwargs):
        return self._getListOrObject(TeamProject, id,
                                     team_id=self.id,
                                     **kwargs)

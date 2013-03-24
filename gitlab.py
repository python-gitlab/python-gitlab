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

import requests

__title__ = 'python-gitlab'
__version__ = '0.1'
__author__ = 'Gauvain Pocentek'
__email__ = 'gauvain@pocentek.net'
__license__ = 'LGPL3'
__copyright__ = 'Copyright 2013 Gauvain Pocentek'


class GitlabConnectionError(Exception):
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
                        obj.__dict__[k] = v
            return l
        elif r.status_code == 401:
            raise GitlabAuthenticationError(r.json()['message'])
        else:
            raise GitlabGetError('%d: %s' % (r.status_code, r.text))

    def get(self, obj_class, id=None, **kwargs):
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
        return False

    def create(self, obj):
        url = obj._url % obj.__dict__
        url = '%s%s?private_token=%s' % (self._url, url, self.private_token)

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
                d[k] = v

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


class GitlabObject(object):
    _url = None
    _returnClass = None
    _constructorTypes = None
    canGet = True
    canGetList = True
    canCreate = True
    canUpdate = True
    canDelete = True

    @classmethod
    def list(cls, gl, **kwargs):
        if not cls.canGetList:
            raise NotImplementedError

        if not cls._url:
            raise NotImplementedError

        return gl.list(cls, **kwargs)

    def _getListOrObject(self, cls, id, **kwargs):
        if id is None:
            if not cls.canGetList:
                raise GitlabGetError

            return cls.list(self.gitlab, **kwargs)
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


class User(GitlabObject):
    _url = '/users'


class CurrentUserKey(GitlabObject):
    _url = '/user/keys'
    canUpdate = False


class CurrentUser(GitlabObject):
    _url = '/user'
    canGetList = False
    canCreate = False
    canUpdate = False
    canDelete = False

    def Key(self, id=None, **kwargs):
        if id is None:
            return CurrentUserKey.list(self.gitlab, **kwargs)
        else:
            return CurrentUserKey(self.gitlab, id)


class Group(GitlabObject):
    _url = '/groups'
    _constructorTypes = {'projects': 'Project'}


class Issue(GitlabObject):
    _url = '/issues'
    _constructorTypes = {'author': 'User', 'assignee': 'User',
                         'milestone': 'ProjectMilestone'}
    canGet = False
    canDelete = False
    canUpdate = False
    canCreate = False


class ProjectBranch(GitlabObject):
    _url = '/projects/%(project_id)d/repository/branches'
    canDelete = False
    canUpdate = False
    canCreate = False

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
    _url = '/projects/%(project_id)d/repository/commits'
    canGet = False
    canDelete = False
    canUpdate = False
    canCreate = False


class ProjectHook(GitlabObject):
    _url = '/projects/%(project_id)d/hooks'


class ProjectIssueNote(GitlabObject):
    _url = '/projects/%(project_id)d/issues/%(issue_id)d/notes'
    _constructorTypes = {'author': 'User'}
    canUpdate = False
    canDelete = False


class ProjectIssue(GitlabObject):
    _url = '/projects/%(project_id)s/issues/'
    _constructorTypes = {'author': 'User', 'assignee': 'User',
                         'milestone': 'ProjectMilestone'}
    canDelete = False

    def Note(self, id=None, **kwargs):
        return self._getListOrObject(ProjectIssueNote, id,
                                     project_id=self.project_id,
                                     issue_id=self.id,
                                     **kwargs)


class ProjectMember(GitlabObject):
    _url = '/projects/%(project_id)d/members'
    _returnClass = User


class ProjectNote(GitlabObject):
    _url = '/projects/%(project_id)d/notes'
    _constructorTypes = {'author': 'User'}
    canUpdate = False
    canDelete = False


class ProjectTag(GitlabObject):
    _url = '/projects/%(project_id)d/repository/tags'
    canGet = False
    canDelete = False
    canUpdate = False
    canCreate = False


class ProjectMergeRequestNote(GitlabObject):
    _url = '/projects/%(project_id)d/merge_requests/%(merge_request_id)d/notes'
    _constructorTypes = {'author': 'User'}
    canGet = False
    canCreate = False
    canUpdate = False
    canDelete = False


class ProjectMergeRequest(GitlabObject):
    _url = '/projects/%(project_id)d/merge_request'
    _constructorTypes = {'author': 'User', 'assignee': 'User'}
    canDelete = False

    def Note(self, id=None, **kwargs):
        return self._getListOrObject(ProjectMergeRequestNote, id,
                                     project_id=self.id,
                                     merge_request_id=self.id,
                                     **kwargs)


class ProjectMilestone(GitlabObject):
    _url = '/projects/%(project_id)s/milestones'
    canDelete = False


class ProjectSnippetNote(GitlabObject):
    _url = '/projects/%(project_id)d/snippets/%(snippet_id)d/notes'
    _constructorTypes = {'author': 'User'}
    canUpdate = False
    canDelete = False


class ProjectSnippet(GitlabObject):
    _url = '/projects/%(project_id)d/snippets'
    _constructorTypes = {'author': 'User'}

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

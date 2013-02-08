#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2013 Gauvain Pocentek <gauvain@pocentek.net>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import requests

class GitlabConnectionError(Exception):
    pass

class GitlabGetError(Exception):
    pass

class GitlabCreateError(Exception):
    pass

class GitlabUpdateError(Exception):
    pass

class GitlabSessionError(Exception):
    pass

class Gitlab(object):
    def __init__(self, url, private_token):
        self.url = '%s/api/v3'%url
        self.private_token = private_token

    def setUrl(self, url):
        self.url = '%s/api/v3'%url

    def setToken(self, token):
        self.private_token = token

    def rawPost(self, path, data):
        url = '%s%s'%(self.url, path)
        try:
            r = requests.post(url, data)
        except:
            GitlabConnectionError('Can\'t connect to GitLab server (%s)'%self.url)

        return r

    def list(self, objClass, **kwargs):
        url = objClass.url
        if kwargs:
            url = objClass.url % kwargs
        url = '%s%s?private_token=%s'%(self.url, url, self.private_token)
        if kwargs:
            url += "&%s"%("&".join(["%s=%s"%(k,v) for k,v in kwargs.items()]))

        try:
            r = requests.get(url)
        except:
            raise GitlabConnectionError('Can\'t connect to GitLab server (%s)'%self.url)

        if r.status_code == 200:
            cls = objClass
            if objClass.returnClass:
                cls = objClass.returnClass
            l = [cls(self, item) for item in r.json]
            if kwargs:
                for k,v in kwargs.items():
                    for obj in l:
                        obj.__dict__[k] = v
            return l
        else:
            raise GitlabGetError('%d: %s'%(r.status_code, r.text))

    def get(self, objClass, id, **kwargs):
        url = objClass.url
        if kwargs:
            url = objClass.url % kwargs
        url = '%s%s/%d?private_token=%s'%(self.url, url, id, self.private_token)

        try:
            r = requests.get(url)
        except:
            raise GitlabConnectionError('Can\'t connect to GitLab server (%s)'%self.url)

        if r.status_code == 200:
            cls = objClass
            if objClass.returnClass:
                cls = objClass.returnClass

            obj = cls(self, r.json)
            if kwargs:
                for k,v in kwargs.items():
                    obj.__dict__[k] = v
            return obj
        else:
            raise GitlabGetError('%d: %s'%(r.status_code, r.text))

    def delete(self, objClass, id, **kwargs):
        # FIXME: not working for project members, gitlab bug or not?
        url = objClass.url
        if kwargs:
            url = objClass.url % kwargs
        url = '%s%s/%d?private_token=%s'%(self.url, url, id, self.private_token)

        try:
            r = requests.delete(url)
        except:
            raise GitlabConnectionError('Can\'t connect to GitLab server (%s)'%self.url)

        if r.status_code == 200:
            return True
        return False

    def create(self, objClass, objData, **kwargs):
        url = objClass.url
        if kwargs:
            url = objClass.url % kwargs
        url = '%s%s?private_token=%s'%(self.url, url, self.private_token)

        try:
            r = requests.post(url, objData)
        except:
            raise GitlabConnectionError('Can\'t connect to GitLab server (%s)'%self.url)

        if r.status_code == 201:
            cls = objClass
            if objClass.returnClass:
                cls = objClass.returnClass

            return cls(self, r.json)
        else:
            raise GitlabCreateError('%d: %s'%(r.status_code, r.text))

    def update(self, objClass, id, objData, **kwargs):
        url = objClass.url
        if kwargs:
            url = objClass.url % kwargs
        url = '%s%s/%d?private_token=%s'%(self.url, url, id, self.private_token)

        try:
            r = requests.put(url, objData)
        except:
            raise GitlabConnectionError('Can\'t connect to GitLab server (%s)'%self.url)

        if r.status_code == 200:
            cls = objClass
            if objClass.returnClass:
                cls = objClass.returnClass

            return cls(self, r.json)
        else:
            raise GitlabUpdateError('%d: %s'%(r.status_code, r.text))


class GitlabObject(object):
    url = None
    returnClass = None
    constructorTypes = None
    canGet = True
    canGetList = True
    canCreate = True
    canUpdate = True
    canDelete = True

    @classmethod
    def update(cls, gl, id, data, **kwargs):
        if not cls.canUpdate:
            raise NotImplementedError

        if not cls.url:
            raise NotImplementedError

        return gl.update(cls, id, data, **kwargs)

    @classmethod
    def create(cls, gl, data, **kwargs):
        if not cls.canCreate:
            raise NotImplementedError

        if not cls.url:
            raise NotImplementedError

        return gl.create(cls, data, **kwargs)

    @classmethod
    def list(cls, gl, **kwargs):
        if not cls.canGetList:
            raise NotImplementedError

        if not cls.url:
            raise NotImplementedError

        return gl.list(cls, **kwargs)

    @classmethod
    def get(cls, gl, id, **kwargs):
        if not cls.canGet:
            raise NotImplementedError

        if not cls.url:
            raise NotImplementedError

        return gl.get(cls, id, **kwargs)

    @classmethod
    def delete(cls, gl, id, **kwargs):
        if not cls.canDelete:
            raise NotImplementedError

        if not cls.url:
            raise NotImplementedError

        return gl.delete(cls, id, **kwargs)

    def getListOrObject(self, cls, id, **kwargs):
        if id == None:
            return cls.list(self.gitlab, **kwargs)
        else:
            return cls.get(self.gitlab, id, **kwargs)

    def getObject(self, k, v):
        if self.constructorTypes and k in self.constructorTypes:
            return globals()[self.constructorTypes[k]](self.gitlab, v)
        else:
            return v

    def __init__(self, gl, data):
        self.gitlab = gl
        for k, v in data.items():
            if isinstance (v, list):
                self.__dict__[k] = []
                for i in v:
                    self.__dict__[k].append(self.getObject(k,i))
            else:
                self.__dict__[k] = self.getObject(k,v)

    def __str__(self):
        return '%s => %s'%(type(self), str(self.__dict__))


class User(GitlabObject):
    url = '/users'

class CurrentUser(GitlabObject):
    url = '/user'
    canGetList = False
    canCreate = False
    canUpdate = False
    canDelete = False

class CurrentUserKey(GitlabObject):
    url = '/user/keys'
    canUpdate = False

    url = '/users'

class Group(GitlabObject):
    url = '/groups'
    constructorTypes = {'projects': 'Project'}

class Issue(GitlabObject):
    url = '/issues'
    constructorTypes = {'author': 'User', 'assignee': 'User',
                        'milestone': 'ProjectMilestone'}
    canGet = False
    canDelete = False
    canUpdate = False
    canCreate = False

def Session(gl, email, password):
    r = gl.rawPost('/session', {'email': email, 'password': password})
    if r.status_code == 201:
        return User(gl, r.json)
    else:
        raise GitlabSessionError()

class ProjectBranch(GitlabObject):
    url = '/projects/%(project_id)d/repository/branches'
    canDelete = False
    canUpdate = False
    canCreate = False

class ProjectCommit(GitlabObject):
    url = '/projects/%(project_id)d/repository/commits'
    canGet = False
    canDelete = False
    canUpdate = False
    canCreate = False

class ProjectHook(GitlabObject):
    url = '/projects/%(project_id)d/hooks'

class ProjectIssueNote(GitlabObject):
    url = '/projects/%(project_id)d/issues/%(issue_id)d/notes'
    constructorTypes = {'author': 'User'}
    canUpdate = False
    canDelete = False

class ProjectIssue(GitlabObject):
    url = '/projects/%(project_id)s/issues/'
    constructorTypes = {'author': 'User', 'assignee': 'User',
                        'milestone': 'ProjectMilestone'}
    canDelete = False

    def Note(self, id=None):
        return self.getListOrObject(ProjectIssueNote, id, project_id=self.id, issue_id=self.id)

class ProjectMember(GitlabObject):
    url = '/projects/%(project_id)d/members'
    returnClass = User

class ProjectNote(GitlabObject):
    url = '/projects/%(project_id)d/notes'
    constructorTypes = {'author': 'User'}
    canUpdate = False
    canDelete = False

class ProjectTag(GitlabObject):
    url = '/projects/%(project_id)d/repository/tags'
    canGet = False
    canDelete = False
    canUpdate = False
    canCreate = False

class ProjectMergeRequestNote(GitlabObject):
    url = '/projects/%(project_id)d/merge_requests/%(merge_request_id)d/notes'
    constructorTypes = {'author': 'User'}
    canGet = False
    canCreate = False
    canUpdate = False
    canDelete = False

class ProjectMergeRequest(GitlabObject):
    url = '/projects/%(project_id)d/merge_request'
    constructorTypes = {'author': 'User', 'assignee': 'User'}
    canDelete = False

    def Note(self, id=None):
        return self.getListOrObject(ProjectMergeRequestNote, id,
                                    project_id=self.id, merge_request_id=self.id)

class ProjectMilestone(GitlabObject):
    url = '/projects/%(project_id)s/milestones'
    canDelete = False

class ProjectSnippetNote(GitlabObject):
    url = '/projects/%(project_id)d/snippets/%(snippet_id)d/notes'
    constructorTypes = {'author': 'User'}
    canUpdate = False
    canDelete = False

class ProjectSnippet(GitlabObject):
    url = '/projects/%(project_id)d/snippets'
    constructorTypes = {'author': 'User'}

    def Note(self, id=None):
        return self.getListOrObject(ProjectSnippetNote, id,
                                    project_id=self.id, snippet_id=self.id)

class Project(GitlabObject):
    url = '/projects'
    constructorTypes = {'owner': 'User', 'namespace': 'Group'}
    canUpdate = False
    canDelete = False

    def Branch(self, id=None):
        return self.getListOrObject(ProjectBranch, id, project_id=self.id)

    def Commit(self, id=None):
        return self.getListOrObject(ProjectCommit, id, project_id=self.id)

    def Hook(self, id=None):
        return self.getListOrObject(ProjectHook, id, project_id=self.id)

    def Issue(self, id=None):
        return self.getListOrObject(ProjectIssue, id, project_id=self.id)

    def Member(self, id=None):
        return self.getListOrObject(ProjectMember, id, project_id=self.id)

    def MergeRequest(self, id=None):
        return self.getListOrObject(ProjectMergeRequest, id, project_id=self.id)

    def Milestone(self, id=None):
        return self.getListOrObject(ProjectMilestone, id, project_id=self.id)

    def Note(self, id=None):
        return self.getListOrObject(ProjectNote, id, project_id=self.id)

    def Snippet(self, id=None):
        return self.getListOrObject(ProjectSnippet, id, project_id=self.id)

    def Tag(self, id=None):
        return self.getListOrObject(ProjectTag, id, project_id=self.id)

if __name__ == '__main__':
    # quick "doc"
    #
    # See https://github.com/gitlabhq/gitlabhq/tree/master/doc/api for the
    # source

    # register a connection to a gitlab instance, using its URL and a user
    # private token
    gl = Gitlab('http://192.168.123.107:8080', 'JVNSESs8EwWRx5yDxM5q')

    # get a list of projects
    for p in Project.list(gl):
        print p.name
        # get associated issues
        issues = ProjectIssue.list(gl, project_id=p.id)
        for issue in issues:
            print "  %d => %s (closed: %d)"%(issue.id, issue.title, issue.closed)
            # and close them all
            ProjectIssue.update(gl, issue.id, {'closed': 1}, project_id=p.id)


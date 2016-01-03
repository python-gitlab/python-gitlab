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
import itertools
import json
import sys

import six

from gitlab.exceptions import *  # noqa


class jsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, GitlabObject):
            return obj.__dict__
        elif isinstance(obj, Gitlab):
            return {'url': obj._url}
        return json.JSONEncoder.default(self, obj)


class BaseManager(object):
    obj_cls = None

    def __init__(self, gl, parent=None, args=[]):
        self.gitlab = gl
        self.args = args
        self.parent = parent

        if self.obj_cls is None:
            raise AttributeError("obj_cls must be defined")

    def _set_parent_args(self, **kwargs):
        if self.parent is not None:
            for attr, parent_attr in self.args:
                kwargs.setdefault(attr, getattr(self.parent, parent_attr))

    def get(self, id, **kwargs):
        self._set_parent_args(**kwargs)
        if not self.obj_cls.canGet:
            raise NotImplementedError
        return self.obj_cls.get(self.gitlab, id, **kwargs)

    def list(self, **kwargs):
        self._set_parent_args(**kwargs)
        if not self.obj_cls.canList:
            raise NotImplementedError
        return self.obj_cls.list(self.gitlab, **kwargs)

    def create(self, data, **kwargs):
        self._set_parent_args(**kwargs)
        if not self.obj_cls.canCreate:
            raise NotImplementedError
        return self.obj_cls.create(self.gitlab, data, **kwargs)


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
    #: List of managers to create
    managers = []

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
    def get(cls, gl, id, **kwargs):
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
        if not cls.canCreate:
            raise NotImplementedError

        obj = cls(gl, data, **kwargs)
        obj.save()

        return obj

    def __init__(self, gl, data=None, **kwargs):
        self._from_api = False
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
        return json.dumps(self.__dict__, cls=jsonEncoder)


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
    # FIXME: password is required for create but not for update
    requiredCreateAttrs = ['email', 'username', 'name']
    optionalCreateAttrs = ['password', 'skype', 'linkedin', 'twitter',
                           'projects_limit', 'extern_uid', 'provider',
                           'bio', 'admin', 'can_create_group', 'website_url',
                           'confirm']
    managers = [('keys', UserKeyManager, [('user_id', 'id')])]

    def _data_for_gitlab(self, extra_parameters={}):
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
    _constructorTypes = {'commit': 'ProjectCommit'}

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


class ProjectTag(GitlabObject):
    _url = '/projects/%(project_id)s/repository/tags'
    idAttr = 'name'
    canGet = 'from_list'
    canDelete = False
    canUpdate = False
    requiredUrlAttrs = ['project_id']
    requiredCreateAttrs = ['tag_name', 'ref']
    optionalCreateAttrs = ['message']
    shortPrintAttr = 'name'


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


class ProjectMilestoneManager(BaseManager):
    obj_cls = ProjectMilestone


class ProjectLabel(GitlabObject):
    _url = '/projects/%(project_id)s/labels'
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
        ('events', ProjectEventManager, [('project_id', 'id')]),
        ('files', ProjectFileManager, [('project_id', 'id')]),
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

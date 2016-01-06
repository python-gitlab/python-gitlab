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

    def ProjectFork(self, id=None, **kwargs):
        """Fork a project for a user.

        id must be a dict.
        """
        return ProjectFork._get_list_or_object(self, id, **kwargs)

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

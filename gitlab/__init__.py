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
"""Wrapper for the GitLab API."""

from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
import inspect
import itertools
import json
import warnings

import requests
import six

import gitlab.config
from gitlab.exceptions import *  # noqa
from gitlab.objects import *  # noqa

__title__ = 'python-gitlab'
__version__ = '0.13'
__author__ = 'Gauvain Pocentek'
__email__ = 'gauvain@pocentek.net'
__license__ = 'LGPL3'
__copyright__ = 'Copyright 2013-2016 Gauvain Pocentek'

warnings.filterwarnings('default', category=DeprecationWarning,
                        module='^gitlab')


def _sanitize(value):
    if isinstance(value, dict):
        return dict((k, _sanitize(v))
                    for k, v in six.iteritems(value))
    if isinstance(value, six.string_types):
        return value.replace('/', '%2F')
    return value


class Gitlab(object):
    """Represents a GitLab server connection.

    Args:
        url (str): The URL of the GitLab server.
        private_token (str): The user private token
        email (str): The user email or login.
        password (str): The user password (associated with email).
        ssl_verify (bool): Whether SSL certificates should be validated.
        timeout (float or tuple(float,float)): Timeout to use for requests to
            the GitLab server.

    Attributes:
        user_keys (UserKeyManager): Manager for GitLab users' SSH keys.
        users (UserManager): Manager for GitLab users
        group_members (GroupMemberManager): Manager for GitLab group members
        groups (GroupManager): Manager for GitLab members
        hooks (HookManager): Manager for GitLab hooks
        issues (IssueManager): Manager for GitLab issues
        licenses (LicenseManager): Manager for licenses
        project_branches (ProjectBranchManager): Manager for GitLab projects
            branches
        project_commits (ProjectCommitManager): Manager for GitLab projects
            commits
        project_keys (ProjectKeyManager): Manager for GitLab projects keys
        project_events (ProjectEventManager): Manager for GitLab projects
            events
        project_forks (ProjectForkManager): Manager for GitLab projects forks
        project_hooks (ProjectHookManager): Manager for GitLab projects hooks
        project_issue_notes (ProjectIssueNoteManager): Manager for GitLab notes
            on issues
        project_issues (ProjectIssueManager): Manager for GitLab projects
            issues
        project_members (ProjectMemberManager): Manager for GitLab projects
            members
        project_notes (ProjectNoteManager): Manager for GitLab projects notes
        project_tags (ProjectTagManager): Manager for GitLab projects tags
        project_mergerequest_notes (ProjectMergeRequestNoteManager): Manager
            for GitLab notes on merge requests
        project_mergerequests (ProjectMergeRequestManager): Manager for GitLab
            projects merge requests
        project_milestones (ProjectMilestoneManager): Manager for GitLab
            projects milestones
        project_labels (ProjectLabelManager): Manager for GitLab projects
            labels
        project_files (ProjectFileManager): Manager for GitLab projects files
        project_snippet_notes (ProjectSnippetNoteManager): Manager for GitLab
            note on snippets
        project_snippets (ProjectSnippetManager): Manager for GitLab projects
            snippets
        user_projects (UserProjectManager): Manager for GitLab projects users
        projects (ProjectManager): Manager for GitLab projects
        team_members (TeamMemberManager): Manager for GitLab teams members
        team_projects (TeamProjectManager): Manager for GitLab teams projects
        teams (TeamManager): Manager for GitLab teams
    """

    def __init__(self, url, private_token=None,
                 email=None, password=None, ssl_verify=True, timeout=None):

        self._url = '%s/api/v3' % url
        #: Timeout to use for requests to gitlab server
        self.timeout = timeout
        #: Headers that will be used in request to GitLab
        self.headers = {}
        self.set_token(private_token)
        #: The user email
        self.email = email
        #: The user password (associated with email)
        self.password = password
        #: Whether SSL certificates should be validated
        self.ssl_verify = ssl_verify

        #: Create a session object for requests
        self.session = requests.Session()

        self.settings = ApplicationSettingsManager(self)
        self.user_keys = UserKeyManager(self)
        self.users = UserManager(self)
        self.group_members = GroupMemberManager(self)
        self.groups = GroupManager(self)
        self.hooks = HookManager(self)
        self.issues = IssueManager(self)
        self.licenses = LicenseManager(self)
        self.project_branches = ProjectBranchManager(self)
        self.project_commits = ProjectCommitManager(self)
        self.project_keys = ProjectKeyManager(self)
        self.project_events = ProjectEventManager(self)
        self.project_forks = ProjectForkManager(self)
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
        """Create a Gitlab connection from configuration files.

        Args:
            gitlab_id (str): ID of the configuration section.
            config_files list[str]: List of paths to configuration files.

        Returns:
            (gitlab.Gitlab): A Gitlab connection.

        Raises:
            gitlab.config.GitlabDataError: If the configuration is not correct.
        """
        config = gitlab.config.GitlabConfigParser(gitlab_id=gitlab_id,
                                                  config_files=config_files)
        return Gitlab(config.url, private_token=config.token,
                      ssl_verify=config.ssl_verify, timeout=config.timeout)

    def auth(self):
        """Performs an authentication.

        Uses either the private token, or the email/password pair.

        The `user` attribute will hold a `gitlab.objects.CurrentUser` object on
        success.
        """
        if self.private_token:
            self.token_auth()
        else:
            self.credentials_auth()

    def credentials_auth(self):
        """Performs an authentication using email/password."""
        if not self.email or not self.password:
            raise GitlabAuthenticationError("Missing email/password")

        data = json.dumps({'email': self.email, 'password': self.password})
        r = self._raw_post('/session', data, content_type='application/json')
        raise_error_from_response(r, GitlabAuthenticationError, 201)
        self.user = CurrentUser(self, r.json())
        """(gitlab.objects.CurrentUser): Object representing the user currently
            logged.
        """
        self.set_token(self.user.private_token)

    def token_auth(self):
        """Performs an authentication using the private token."""
        self.user = CurrentUser(self)

    def set_url(self, url):
        """Updates the GitLab URL.

        Args:
            url (str): Base URL of the GitLab server.
        """
        self._url = '%s/api/v3' % url

    def _construct_url(self, id_, obj, parameters):
        if 'next_url' in parameters:
            return parameters['next_url']
        args = _sanitize(parameters)
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
        """Sets the private token for authentication.

        Args:
            token (str): The private token.
        """
        self.private_token = token if token else None
        if token:
            self.headers["PRIVATE-TOKEN"] = token
        elif "PRIVATE-TOKEN" in self.headers:
            del self.headers["PRIVATE-TOKEN"]

    def set_credentials(self, email, password):
        """Sets the email/login and password for authentication.

        Args:
            email (str): The user email or login.
            password (str): The user password.
        """
        self.email = email
        self.password = password

    def _raw_get(self, path, content_type=None, **kwargs):
        url = '%s%s' % (self._url, path)
        headers = self._create_headers(content_type)

        try:
            return self.session.get(url,
                                    params=kwargs,
                                    headers=headers,
                                    verify=self.ssl_verify,
                                    timeout=self.timeout)
        except Exception as e:
            raise GitlabConnectionError(
                "Can't connect to GitLab server (%s)" % e)

    def _raw_list(self, path, cls, **kwargs):
        r = self._raw_get(path, **kwargs)
        raise_error_from_response(r, GitlabListError)

        cls_kwargs = kwargs.copy()

        # Add _from_api manually, because we are not creating objects
        # through normal path
        cls_kwargs['_from_api'] = True
        get_all_results = kwargs.get('all', False)

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
            results.extend(self.list(cls, **args))
        return results

    def _raw_post(self, path, data=None, content_type=None, **kwargs):
        url = '%s%s' % (self._url, path)
        headers = self._create_headers(content_type)
        try:
            return self.session.post(url, params=kwargs, data=data,
                                     headers=headers,
                                     verify=self.ssl_verify,
                                     timeout=self.timeout)
        except Exception as e:
            raise GitlabConnectionError(
                "Can't connect to GitLab server (%s)" % e)

    def _raw_put(self, path, data=None, content_type=None, **kwargs):
        url = '%s%s' % (self._url, path)
        headers = self._create_headers(content_type)

        try:
            return self.session.put(url, data=data, params=kwargs,
                                    headers=headers,
                                    verify=self.ssl_verify,
                                    timeout=self.timeout)
        except Exception as e:
            raise GitlabConnectionError(
                "Can't connect to GitLab server (%s)" % e)

    def _raw_delete(self, path, content_type=None, **kwargs):
        url = '%s%s' % (self._url, path)
        headers = self._create_headers(content_type)

        try:
            return self.session.delete(url,
                                       params=kwargs,
                                       headers=headers,
                                       verify=self.ssl_verify,
                                       timeout=self.timeout)
        except Exception as e:
            raise GitlabConnectionError(
                "Can't connect to GitLab server (%s)" % e)

    def list(self, obj_class, **kwargs):
        """Request the listing of GitLab resources.

        Args:
            obj_class (object): The class of resource to request.
            **kwargs: Additional arguments to send to GitLab.

        Returns:
            list(obj_class): A list of objects of class `obj_class`.

        Raises:
            GitlabConnectionError: If the server cannot be reached.
            GitlabListError: If the server fails to perform the request.
        """
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

        # Also remove the next-url attribute that make queries fail
        if 'next_url' in params:
            del params['next_url']

        try:
            r = self.session.get(url, params=params, headers=headers,
                                 verify=self.ssl_verify,
                                 timeout=self.timeout)
        except Exception as e:
            raise GitlabConnectionError(
                "Can't connect to GitLab server (%s)" % e)

        raise_error_from_response(r, GitlabListError)

        cls = obj_class
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
        """Request a GitLab resources.

        Args:
            obj_class (object): The class of resource to request.
            id: The object ID.
            **kwargs: Additional arguments to send to GitLab.

        Returns:
            obj_class: An object of class `obj_class`.

        Raises:
            GitlabConnectionError: If the server cannot be reached.
            GitlabGetError: If the server fails to perform the request.
        """
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
            r = self.session.get(url, params=params, headers=headers,
                                 verify=self.ssl_verify, timeout=self.timeout)
        except Exception as e:
            raise GitlabConnectionError(
                "Can't connect to GitLab server (%s)" % e)

        raise_error_from_response(r, GitlabGetError)
        return r.json()

    def delete(self, obj, id=None, **kwargs):
        """Delete an object on the GitLab server.

        Args:
            obj (object or id): The object, or the class of the object to
                delete. If it is the class, the id of the object must be
                specified as the `id` arguments.
            id: ID of the object to remove. Required if `obj` is a class.
            **kwargs: Additional arguments to send to GitLab.

        Returns:
            bool: True if the operation succeeds.

        Raises:
            GitlabConnectionError: If the server cannot be reached.
            GitlabDeleteError: If the server fails to perform the request.
        """
        if inspect.isclass(obj):
            if not issubclass(obj, GitlabObject):
                raise GitlabError("Invalid class: %s" % obj)

        params = {obj.idAttr: id if id else getattr(obj, obj.idAttr)}
        params.update(kwargs)

        missing = []
        for k in itertools.chain(obj.requiredUrlAttrs,
                                 obj.requiredDeleteAttrs):
            if k not in params:
                try:
                    params[k] = getattr(obj, k)
                except KeyError:
                    missing.append(k)
        if missing:
            raise GitlabDeleteError('Missing attribute(s): %s' %
                                    ", ".join(missing))

        obj_id = params[obj.idAttr] if obj._id_in_delete_url else None
        url = self._construct_url(id_=obj_id, obj=obj, parameters=params)
        headers = self._create_headers()

        # Remove attributes that are used in url so that there is only
        # url-parameters left
        for attribute in obj.requiredUrlAttrs:
            del params[attribute]
        if obj._id_in_delete_url:
            # The ID is already built, no need to add it as extra key in query
            # string
            params.pop(obj.idAttr)

        try:
            r = self.session.delete(url,
                                    params=params,
                                    headers=headers,
                                    verify=self.ssl_verify,
                                    timeout=self.timeout)
        except Exception as e:
            raise GitlabConnectionError(
                "Can't connect to GitLab server (%s)" % e)

        raise_error_from_response(r, GitlabDeleteError)
        return True

    def create(self, obj, **kwargs):
        """Create an object on the GitLab server.

        The object class and attributes define the request to be made on the
        GitLab server.

        Args:
            obj (object): The object to create.
            **kwargs: Additional arguments to send to GitLab.

        Returns:
            str: A json representation of the object as returned by the GitLab
                server

        Raises:
            GitlabConnectionError: If the server cannot be reached.
            GitlabCreateError: If the server fails to perform the request.
        """
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
            r = self.session.post(url, data=data,
                                  headers=headers,
                                  verify=self.ssl_verify,
                                  timeout=self.timeout)
        except Exception as e:
            raise GitlabConnectionError(
                "Can't connect to GitLab server (%s)" % e)

        raise_error_from_response(r, GitlabCreateError, 201)
        return r.json()

    def update(self, obj, **kwargs):
        """Update an object on the GitLab server.

        The object class and attributes define the request to be made on the
        GitLab server.

        Args:
            obj (object): The object to create.
            **kwargs: Additional arguments to send to GitLab.

        Returns:
            str: A json representation of the object as returned by the GitLab
                server

        Raises:
            GitlabConnectionError: If the server cannot be reached.
            GitlabUpdateError: If the server fails to perform the request.
        """
        params = obj.__dict__.copy()
        params.update(kwargs)
        missing = []
        if obj.requiredUpdateAttrs or obj.optionalUpdateAttrs:
            required_attrs = obj.requiredUpdateAttrs
        else:
            required_attrs = obj.requiredCreateAttrs
        for k in itertools.chain(obj.requiredUrlAttrs, required_attrs):
            if k not in params:
                missing.append(k)
        if missing:
            raise GitlabUpdateError('Missing attribute(s): %s' %
                                    ", ".join(missing))
        obj_id = params[obj.idAttr] if obj._id_in_update_url else None
        url = self._construct_url(id_=obj_id, obj=obj, parameters=params)
        headers = self._create_headers(content_type="application/json")

        # build data that can really be sent to server
        data = obj._data_for_gitlab(extra_parameters=kwargs, update=True)

        try:
            r = self.session.put(url, data=data,
                                 headers=headers,
                                 verify=self.ssl_verify,
                                 timeout=self.timeout)
        except Exception as e:
            raise GitlabConnectionError(
                "Can't connect to GitLab server (%s)" % e)

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
        warnings.warn("`Hook` is deprecated, use `hooks` instead",
                      DeprecationWarning)
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
        warnings.warn("`Project` is deprecated, use `projects` instead",
                      DeprecationWarning)
        return Project._get_list_or_object(self, id, **kwargs)

    def UserProject(self, id=None, **kwargs):
        """Creates a project for a user.

        id must be a dict.
        """
        warnings.warn("`UserProject` is deprecated, "
                      "use `user_projects` instead",
                      DeprecationWarning)
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
        warnings.warn("`search_projects()` is deprecated, "
                      "use `projects.search()` instead",
                      DeprecationWarning)
        return self._list_projects("/projects/search/" + query, **kwargs)

    def all_projects(self, **kwargs):
        """Lists all the projects (need admin rights)."""
        warnings.warn("`all_projects()` is deprecated, "
                      "use `projects.all()` instead",
                      DeprecationWarning)
        return self._list_projects("/projects/all", **kwargs)

    def owned_projects(self, **kwargs):
        """Lists owned projects."""
        warnings.warn("`owned_projects()` is deprecated, "
                      "use `projects.owned()` instead",
                      DeprecationWarning)
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
        warnings.warn("`Group` is deprecated, use `groups` instead",
                      DeprecationWarning)
        return Group._get_list_or_object(self, id, **kwargs)

    def Issue(self, id=None, **kwargs):
        """Lists issues(s) known by the GitLab server.

        Does not support creation or getting a single issue unlike other
        methods in this class yet.
        """
        warnings.warn("`Issue` is deprecated, use `issues` instead",
                      DeprecationWarning)
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
        warnings.warn("`User` is deprecated, use `users` instead",
                      DeprecationWarning)
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
        warnings.warn("`Team` is deprecated, use `teams` instead",
                      DeprecationWarning)
        return Team._get_list_or_object(self, id, **kwargs)

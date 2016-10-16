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
from gitlab.const import *  # noqa
from gitlab.exceptions import *  # noqa
from gitlab.objects import *  # noqa

__title__ = 'python-gitlab'
__version__ = '0.16'
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
        http_username: (str): Username for HTTP authentication
        http_password: (str): Password for HTTP authentication
    Attributes:
        user_emails (UserEmailManager): Manager for GitLab users' emails.
        user_keys (UserKeyManager): Manager for GitLab users' SSH keys.
        users (UserManager): Manager for GitLab users
        keys (DeployKeyManager): Manager for deploy keys
        group_accessrequests (GroupAccessRequestManager): Manager for GitLab
            groups access requests
        group_issues (GroupIssueManager): Manager for GitLab group issues
        group_projects (GroupProjectManager): Manager for GitLab group projects
        group_members (GroupMemberManager): Manager for GitLab group members
        groups (GroupManager): Manager for GitLab members
        hooks (HookManager): Manager for GitLab hooks
        issues (IssueManager): Manager for GitLab issues
        licenses (LicenseManager): Manager for licenses
        namespaces (NamespaceManager): Manager for namespaces
        project_accessrequests (ProjectAccessRequestManager): Manager for
            GitLab projects access requests
        project_branches (ProjectBranchManager): Manager for GitLab projects
            branches
        project_builds (ProjectBuildManager): Manager for GitLab projects
            builds
        project_commits (ProjectCommitManager): Manager for GitLab projects
            commits
        project_commit_comments (ProjectCommitCommentManager): Manager for
            GitLab projects commits comments
        project_commit_statuses (ProjectCommitStatusManager): Manager for
            GitLab projects commits statuses
        project_deployments (ProjectDeploymentManager): Manager for GitLab
            projects deployments
        project_keys (ProjectKeyManager): Manager for GitLab projects keys
        project_environments (ProjectEnvironmentManager): Manager for GitLab
            projects environments
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
        project_pipelines (ProjectPipelineManager): Manager for GitLab projects
            pipelines
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
        project_services (ProjectServiceManager): Manager for the GitLab
            projects services
        project_snippet_notes (ProjectSnippetNoteManager): Manager for GitLab
            note on snippets
        project_snippets (ProjectSnippetManager): Manager for GitLab projects
            snippets
        project_triggers (ProjectTriggerManager): Manager for build triggers
        project_variables (ProjectVariableManager): Manager for build variables
        user_projects (UserProjectManager): Manager for GitLab projects users
        projects (ProjectManager): Manager for GitLab projects
        runners (RunnerManager): Manager for the CI runners
        settings (ApplicationSettingsManager): manager for the Gitlab settings
        team_members (TeamMemberManager): Manager for GitLab teams members
        team_projects (TeamProjectManager): Manager for GitLab teams projects
        teams (TeamManager): Manager for GitLab teams
        todos (TodoManager): Manager for user todos
    """

    def __init__(self, url, private_token=None, email=None, password=None,
                 ssl_verify=True, http_username=None, http_password=None,
                 timeout=None):

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
        self.http_username = http_username
        self.http_password = http_password

        #: Create a session object for requests
        self.session = requests.Session()

        self.settings = ApplicationSettingsManager(self)
        self.user_emails = UserEmailManager(self)
        self.user_keys = UserKeyManager(self)
        self.users = UserManager(self)
        self.keys = KeyManager(self)
        self.group_accessrequests = GroupAccessRequestManager(self)
        self.group_issues = GroupIssueManager(self)
        self.group_projects = GroupProjectManager(self)
        self.group_members = GroupMemberManager(self)
        self.groups = GroupManager(self)
        self.hooks = HookManager(self)
        self.issues = IssueManager(self)
        self.licenses = LicenseManager(self)
        self.namespaces = NamespaceManager(self)
        self.project_accessrequests = ProjectAccessRequestManager(self)
        self.project_branches = ProjectBranchManager(self)
        self.project_builds = ProjectBuildManager(self)
        self.project_commits = ProjectCommitManager(self)
        self.project_commit_comments = ProjectCommitCommentManager(self)
        self.project_commit_statuses = ProjectCommitStatusManager(self)
        self.project_deployments = ProjectDeploymentManager(self)
        self.project_keys = ProjectKeyManager(self)
        self.project_environments = ProjectEnvironmentManager(self)
        self.project_events = ProjectEventManager(self)
        self.project_forks = ProjectForkManager(self)
        self.project_hooks = ProjectHookManager(self)
        self.project_issue_notes = ProjectIssueNoteManager(self)
        self.project_issues = ProjectIssueManager(self)
        self.project_members = ProjectMemberManager(self)
        self.project_notes = ProjectNoteManager(self)
        self.project_pipelines = ProjectPipelineManager(self)
        self.project_tags = ProjectTagManager(self)
        self.project_mergerequest_notes = ProjectMergeRequestNoteManager(self)
        self.project_mergerequests = ProjectMergeRequestManager(self)
        self.project_milestones = ProjectMilestoneManager(self)
        self.project_labels = ProjectLabelManager(self)
        self.project_files = ProjectFileManager(self)
        self.project_services = ProjectServiceManager(self)
        self.project_snippet_notes = ProjectSnippetNoteManager(self)
        self.project_snippets = ProjectSnippetManager(self)
        self.project_triggers = ProjectTriggerManager(self)
        self.project_variables = ProjectVariableManager(self)
        self.user_projects = UserProjectManager(self)
        self.projects = ProjectManager(self)
        self.runners = RunnerManager(self)
        self.team_members = TeamMemberManager(self)
        self.team_projects = TeamProjectManager(self)
        self.teams = TeamManager(self)
        self.todos = TodoManager(self)
        self.sidekiq = SidekiqManager(self)

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
                      ssl_verify=config.ssl_verify, timeout=config.timeout,
                      http_username=config.http_username,
                      http_password=config.http_password)

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

    def _construct_url(self, id_, obj, parameters, action=None):
        if 'next_url' in parameters:
            return parameters['next_url']
        args = _sanitize(parameters)

        url_attr = '_url'
        if action is not None:
            attr = '_%s_url' % action
            if hasattr(obj, attr):
                url_attr = attr
        obj_url = getattr(obj, url_attr)

        # TODO(gpocentek): the following will need an update when we have
        # object with both urlPlural and _ACTION_url attributes
        if id_ is None and obj._urlPlural is not None:
            url = obj._urlPlural % args
        else:
            url = obj_url % args

        if id_ is not None:
            return '%s/%s' % (url, str(id_))
        else:
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

    def enable_debug(self):
        import logging
        try:
            from http.client import HTTPConnection
        except ImportError:
            from httplib import HTTPConnection  # noqa

        HTTPConnection.debuglevel = 1
        logging.basicConfig()
        logging.getLogger().setLevel(logging.DEBUG)
        requests_log = logging.getLogger("requests.packages.urllib3")
        requests_log.setLevel(logging.DEBUG)
        requests_log.propagate = True

    def _raw_get(self, path_, content_type=None, streamed=False, **kwargs):
        if path_.startswith('http://') or path_.startswith('https://'):
            url = path_
        else:
            url = '%s%s' % (self._url, path_)

        headers = self._create_headers(content_type)
        try:
            return self.session.get(url,
                                    params=kwargs,
                                    headers=headers,
                                    verify=self.ssl_verify,
                                    timeout=self.timeout,
                                    stream=streamed,
                                    auth=requests.auth.HTTPBasicAuth(
                                        self.http_username,
                                        self.http_password))
        except Exception as e:
            raise GitlabConnectionError(
                "Can't connect to GitLab server (%s)" % e)

    def _raw_list(self, path_, cls, extra_attrs={}, **kwargs):
        params = extra_attrs.copy()
        params.update(kwargs.copy())

        get_all_results = kwargs.get('all', False)

        # Remove these keys to avoid breaking the listing (urls will get too
        # long otherwise)
        for key in ['all', 'next_url']:
            if key in params:
                del params[key]

        r = self._raw_get(path_, **params)
        raise_error_from_response(r, GitlabListError)

        # These attributes are not needed in the object
        for key in ['page', 'per_page', 'sudo']:
            if key in params:
                del params[key]

        # Add _from_api manually, because we are not creating objects
        # through normal path_
        params['_from_api'] = True

        results = [cls(self, item, **params) for item in r.json()
                   if item is not None]
        if ('next' in r.links and 'url' in r.links['next']
           and get_all_results is True):
            args = kwargs.copy()
            args['next_url'] = r.links['next']['url']
            results.extend(self.list(cls, **args))
        return results

    def _raw_post(self, path_, data=None, content_type=None, **kwargs):
        url = '%s%s' % (self._url, path_)
        headers = self._create_headers(content_type)
        try:
            return self.session.post(url, params=kwargs, data=data,
                                     headers=headers,
                                     verify=self.ssl_verify,
                                     timeout=self.timeout,
                                     auth=requests.auth.HTTPBasicAuth(
                                         self.http_username,
                                         self.http_password))
        except Exception as e:
            raise GitlabConnectionError(
                "Can't connect to GitLab server (%s)" % e)

    def _raw_put(self, path_, data=None, content_type=None, **kwargs):
        url = '%s%s' % (self._url, path_)
        headers = self._create_headers(content_type)

        try:
            return self.session.put(url, data=data, params=kwargs,
                                    headers=headers,
                                    verify=self.ssl_verify,
                                    timeout=self.timeout,
                                    auth=requests.auth.HTTPBasicAuth(
                                        self.http_username,
                                        self.http_password))
        except Exception as e:
            raise GitlabConnectionError(
                "Can't connect to GitLab server (%s)" % e)

    def _raw_delete(self, path_, content_type=None, **kwargs):
        url = '%s%s' % (self._url, path_)
        headers = self._create_headers(content_type)

        try:
            return self.session.delete(url,
                                       params=kwargs,
                                       headers=headers,
                                       verify=self.ssl_verify,
                                       timeout=self.timeout,
                                       auth=requests.auth.HTTPBasicAuth(
                                           self.http_username,
                                           self.http_password))
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

        return self._raw_list(url, obj_class, **kwargs)

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

        url = self._construct_url(id_=_sanitize(id), obj=obj_class,
                                  parameters=kwargs)

        r = self._raw_get(url, **kwargs)
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

        if obj._id_in_delete_url:
            # The ID is already built, no need to add it as extra key in query
            # string
            params.pop(obj.idAttr)

        r = self._raw_delete(url, **params)
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

        url = self._construct_url(id_=None, obj=obj, parameters=params,
                                  action='create')

        # build data that can really be sent to server
        data = obj._data_for_gitlab(extra_parameters=kwargs)

        r = self._raw_post(url, data=data, content_type='application/json')
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

        # build data that can really be sent to server
        data = obj._data_for_gitlab(extra_parameters=kwargs, update=True)

        r = self._raw_put(url, data=data, content_type='application/json')
        raise_error_from_response(r, GitlabUpdateError)
        return r.json()

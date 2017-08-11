# -*- coding: utf-8 -*-
#
# Copyright (C) 2013-2017 Gauvain Pocentek <gauvain@pocentek.net>
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
from __future__ import absolute_import
import base64
import json
import warnings

import six
from six.moves import urllib

import gitlab
from gitlab.base import *  # noqa
from gitlab.exceptions import *  # noqa
from gitlab import utils


class SidekiqManager(object):
    """Manager for the Sidekiq methods.

    This manager doesn't actually manage objects but provides helper fonction
    for the sidekiq metrics API.
    """
    def __init__(self, gl):
        """Constructs a Sidekiq manager.

        Args:
            gl (gitlab.Gitlab): Gitlab object referencing the GitLab server.
        """
        self.gitlab = gl

    def _simple_get(self, url, **kwargs):
        r = self.gitlab._raw_get(url, **kwargs)
        raise_error_from_response(r, GitlabGetError)
        return r.json()

    def queue_metrics(self, **kwargs):
        """Returns the registred queues information."""
        return self._simple_get('/sidekiq/queue_metrics', **kwargs)

    def process_metrics(self, **kwargs):
        """Returns the registred sidekiq workers."""
        return self._simple_get('/sidekiq/process_metrics', **kwargs)

    def job_stats(self, **kwargs):
        """Returns statistics about the jobs performed."""
        return self._simple_get('/sidekiq/job_stats', **kwargs)

    def compound_metrics(self, **kwargs):
        """Returns all available metrics and statistics."""
        return self._simple_get('/sidekiq/compound_metrics', **kwargs)


class UserEmail(GitlabObject):
    _url = '/users/%(user_id)s/emails'
    canUpdate = False
    shortPrintAttr = 'email'
    requiredUrlAttrs = ['user_id']
    requiredCreateAttrs = ['email']


class UserEmailManager(BaseManager):
    obj_cls = UserEmail


class UserKey(GitlabObject):
    _url = '/users/%(user_id)s/keys'
    canGet = 'from_list'
    canUpdate = False
    requiredUrlAttrs = ['user_id']
    requiredCreateAttrs = ['title', 'key']


class UserKeyManager(BaseManager):
    obj_cls = UserKey


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
                           'description', 'builds_enabled', 'public_builds',
                           'import_url', 'only_allow_merge_if_build_succeeds']


class UserProjectManager(BaseManager):
    obj_cls = UserProject


class User(GitlabObject):
    _url = '/users'
    shortPrintAttr = 'username'
    requiredCreateAttrs = ['email', 'username', 'name']
    optionalCreateAttrs = ['password', 'reset_password', 'skype', 'linkedin',
                           'twitter', 'projects_limit', 'extern_uid',
                           'provider', 'bio', 'admin', 'can_create_group',
                           'website_url', 'confirm', 'external',
                           'organization', 'location']
    requiredUpdateAttrs = ['email', 'username', 'name']
    optionalUpdateAttrs = ['password', 'skype', 'linkedin', 'twitter',
                           'projects_limit', 'extern_uid', 'provider', 'bio',
                           'admin', 'can_create_group', 'website_url',
                           'confirm', 'external', 'organization', 'location']
    managers = (
        ('emails', 'UserEmailManager', [('user_id', 'id')]),
        ('keys', 'UserKeyManager', [('user_id', 'id')]),
        ('projects', 'UserProjectManager', [('user_id', 'id')]),
    )

    def _data_for_gitlab(self, extra_parameters={}, update=False,
                         as_json=True):
        if hasattr(self, 'confirm'):
            self.confirm = str(self.confirm).lower()
        return super(User, self)._data_for_gitlab(extra_parameters)

    def block(self, **kwargs):
        """Blocks the user."""
        url = '/users/%s/block' % self.id
        r = self.gitlab._raw_put(url, **kwargs)
        raise_error_from_response(r, GitlabBlockError)
        self.state = 'blocked'

    def unblock(self, **kwargs):
        """Unblocks the user."""
        url = '/users/%s/unblock' % self.id
        r = self.gitlab._raw_put(url, **kwargs)
        raise_error_from_response(r, GitlabUnblockError)
        self.state = 'active'

    def __eq__(self, other):
        if type(other) is type(self):
            selfdict = self.as_dict()
            otherdict = other.as_dict()
            selfdict.pop('password', None)
            otherdict.pop('password', None)
            return selfdict == otherdict
        return False


class UserManager(BaseManager):
    obj_cls = User

    def search(self, query, **kwargs):
        """Search users.

        Args:
            query (str): The query string to send to GitLab for the search.
            all (bool): If True, return all the items, without pagination
            **kwargs: Additional arguments to send to GitLab.

        Returns:
            list(User): A list of matching users.

        Raises:
            GitlabConnectionError: If the server cannot be reached.
            GitlabListError: If the server fails to perform the request.
        """
        url = self.obj_cls._url + '?search=' + query
        return self.gitlab._raw_list(url, self.obj_cls, **kwargs)

    def get_by_username(self, username, **kwargs):
        """Get a user by its username.

        Args:
            username (str): The name of the user.
            **kwargs: Additional arguments to send to GitLab.

        Returns:
            User: The matching user.

        Raises:
            GitlabConnectionError: If the server cannot be reached.
            GitlabGetError: If the server fails to perform the request.
        """
        url = self.obj_cls._url + '?username=' + username
        results = self.gitlab._raw_list(url, self.obj_cls, **kwargs)
        assert len(results) in (0, 1)
        try:
            return results[0]
        except IndexError:
            raise GitlabGetError('no such user: ' + username)


class CurrentUserEmail(GitlabObject):
    _url = '/user/emails'
    canUpdate = False
    shortPrintAttr = 'email'
    requiredCreateAttrs = ['email']


class CurrentUserEmailManager(BaseManager):
    obj_cls = CurrentUserEmail


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
    managers = (
        ('emails', 'CurrentUserEmailManager', [('user_id', 'id')]),
        ('keys', 'CurrentUserKeyManager', [('user_id', 'id')]),
    )


class ApplicationSettings(GitlabObject):
    _url = '/application/settings'
    _id_in_update_url = False
    getRequiresId = False
    optionalUpdateAttrs = ['after_sign_out_path',
                           'container_registry_token_expire_delay',
                           'default_branch_protection',
                           'default_project_visibility',
                           'default_projects_limit',
                           'default_snippet_visibility',
                           'domain_blacklist',
                           'domain_blacklist_enabled',
                           'domain_whitelist',
                           'enabled_git_access_protocol',
                           'gravatar_enabled',
                           'home_page_url',
                           'max_attachment_size',
                           'repository_storage',
                           'restricted_signup_domains',
                           'restricted_visibility_levels',
                           'session_expire_delay',
                           'sign_in_text',
                           'signin_enabled',
                           'signup_enabled',
                           'twitter_sharing_enabled',
                           'user_oauth_applications']
    canList = False
    canCreate = False
    canDelete = False

    def _data_for_gitlab(self, extra_parameters={}, update=False,
                         as_json=True):
        data = (super(ApplicationSettings, self)
                ._data_for_gitlab(extra_parameters, update=update,
                                  as_json=False))
        if not self.domain_whitelist:
            data.pop('domain_whitelist', None)
        return json.dumps(data)


class ApplicationSettingsManager(BaseManager):
    obj_cls = ApplicationSettings


class BroadcastMessage(GitlabObject):
    _url = '/broadcast_messages'
    requiredCreateAttrs = ['message']
    optionalCreateAttrs = ['starts_at', 'ends_at', 'color', 'font']
    requiredUpdateAttrs = []
    optionalUpdateAttrs = ['message', 'starts_at', 'ends_at', 'color', 'font']


class BroadcastMessageManager(BaseManager):
    obj_cls = BroadcastMessage


class Key(GitlabObject):
    _url = '/deploy_keys'
    canGet = 'from_list'
    canCreate = False
    canUpdate = False
    canDelete = False

    def __init__(self, *args, **kwargs):
        warnings.warn("`Key` is deprecated, use `DeployKey` instead",
                      DeprecationWarning)
        super(Key, self).__init__(*args, **kwargs)


class KeyManager(BaseManager):
    obj_cls = Key


class DeployKey(GitlabObject):
    _url = '/deploy_keys'
    canGet = 'from_list'
    canCreate = False
    canUpdate = False
    canDelete = False


class DeployKeyManager(BaseManager):
    obj_cls = DeployKey


class NotificationSettings(GitlabObject):
    _url = '/notification_settings'
    _id_in_update_url = False
    getRequiresId = False
    optionalUpdateAttrs = ['level',
                           'notification_email',
                           'new_note',
                           'new_issue',
                           'reopen_issue',
                           'close_issue',
                           'reassign_issue',
                           'new_merge_request',
                           'reopen_merge_request',
                           'close_merge_request',
                           'reassign_merge_request',
                           'merge_merge_request']
    canList = False
    canCreate = False
    canDelete = False


class NotificationSettingsManager(BaseManager):
    obj_cls = NotificationSettings


class Gitignore(GitlabObject):
    _url = '/templates/gitignores'
    canDelete = False
    canUpdate = False
    canCreate = False
    idAttr = 'name'


class GitignoreManager(BaseManager):
    obj_cls = Gitignore


class Gitlabciyml(GitlabObject):
    _url = '/templates/gitlab_ci_ymls'
    canDelete = False
    canUpdate = False
    canCreate = False
    idAttr = 'name'


class GitlabciymlManager(BaseManager):
    obj_cls = Gitlabciyml


class GroupIssue(GitlabObject):
    _url = '/groups/%(group_id)s/issues'
    canGet = 'from_list'
    canCreate = False
    canUpdate = False
    canDelete = False
    requiredUrlAttrs = ['group_id']
    optionalListAttrs = ['state', 'labels', 'milestone', 'order_by', 'sort']


class GroupIssueManager(BaseManager):
    obj_cls = GroupIssue


class GroupMember(GitlabObject):
    _url = '/groups/%(group_id)s/members'
    canGet = 'from_list'
    requiredUrlAttrs = ['group_id']
    requiredCreateAttrs = ['access_level', 'user_id']
    optionalCreateAttrs = ['expires_at']
    requiredUpdateAttrs = ['access_level']
    optionalCreateAttrs = ['expires_at']
    shortPrintAttr = 'username'

    def _update(self, **kwargs):
        self.user_id = self.id
        super(GroupMember, self)._update(**kwargs)


class GroupMemberManager(BaseManager):
    obj_cls = GroupMember


class GroupNotificationSettings(NotificationSettings):
    _url = '/groups/%(group_id)s/notification_settings'
    requiredUrlAttrs = ['group_id']


class GroupNotificationSettingsManager(BaseManager):
    obj_cls = GroupNotificationSettings


class GroupAccessRequest(GitlabObject):
    _url = '/groups/%(group_id)s/access_requests'
    canGet = 'from_list'
    canUpdate = False

    def approve(self, access_level=gitlab.DEVELOPER_ACCESS, **kwargs):
        """Approve an access request.

        Args:
            access_level (int): The access level for the user.

        Raises:
            GitlabConnectionError: If the server cannot be reached.
            GitlabUpdateError: If the server fails to perform the request.
        """

        url = ('/groups/%(group_id)s/access_requests/%(id)s/approve' %
               {'group_id': self.group_id, 'id': self.id})
        data = {'access_level': access_level}
        r = self.gitlab._raw_put(url, data=data, **kwargs)
        raise_error_from_response(r, GitlabUpdateError, 201)
        self._set_from_dict(r.json())


class GroupAccessRequestManager(BaseManager):
    obj_cls = GroupAccessRequest


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
    optionalListAttrs = ['state', 'labels', 'order_by', 'sort']


class IssueManager(BaseManager):
    obj_cls = Issue


class License(GitlabObject):
    _url = '/licenses'
    canDelete = False
    canUpdate = False
    canCreate = False
    idAttr = 'key'

    optionalListAttrs = ['popular']
    optionalGetAttrs = ['project', 'fullname']


class LicenseManager(BaseManager):
    obj_cls = License


class Snippet(GitlabObject):
    _url = '/snippets'
    _constructorTypes = {'author': 'User'}
    requiredCreateAttrs = ['title', 'file_name', 'content']
    optionalCreateAttrs = ['lifetime', 'visibility_level']
    optionalUpdateAttrs = ['title', 'file_name', 'content', 'visibility_level']
    shortPrintAttr = 'title'

    def raw(self, streamed=False, action=None, chunk_size=1024, **kwargs):
        """Return the raw content of a snippet.

        Args:
            streamed (bool): If True the data will be processed by chunks of
                `chunk_size` and each chunk is passed to `action` for
                treatment.
            action (callable): Callable responsible of dealing with chunk of
                data.
            chunk_size (int): Size of each chunk.

        Returns:
            str: The snippet content.

        Raises:
            GitlabConnectionError: If the server cannot be reached.
            GitlabGetError: If the server fails to perform the request.
        """
        url = ("/snippets/%(snippet_id)s/raw" % {'snippet_id': self.id})
        r = self.gitlab._raw_get(url, **kwargs)
        raise_error_from_response(r, GitlabGetError)
        return utils.response_content(r, streamed, action, chunk_size)


class SnippetManager(BaseManager):
    obj_cls = Snippet

    def public(self, **kwargs):
        """List all the public snippets.

        Args:
            all (bool): If True, return all the items, without pagination
            **kwargs: Additional arguments to send to GitLab.

        Returns:
            list(gitlab.Gitlab.Snippet): The list of snippets.
        """
        return self.gitlab._raw_list("/snippets/public", Snippet, **kwargs)


class Namespace(GitlabObject):
    _url = '/namespaces'
    canGet = 'from_list'
    canUpdate = False
    canDelete = False
    canCreate = False
    optionalListAttrs = ['search']


class NamespaceManager(BaseManager):
    obj_cls = Namespace


class ProjectBoardList(GitlabObject):
    _url = '/projects/%(project_id)s/boards/%(board_id)s/lists'
    requiredUrlAttrs = ['project_id', 'board_id']
    _constructorTypes = {'label': 'ProjectLabel'}
    requiredCreateAttrs = ['label_id']
    requiredUpdateAttrs = ['position']


class ProjectBoardListManager(BaseManager):
    obj_cls = ProjectBoardList


class ProjectBoard(GitlabObject):
    _url = '/projects/%(project_id)s/boards'
    requiredUrlAttrs = ['project_id']
    _constructorTypes = {'labels': 'ProjectBoardList'}
    canGet = 'from_list'
    canUpdate = False
    canCreate = False
    canDelete = False
    managers = (
        ('lists', 'ProjectBoardListManager',
            [('project_id', 'project_id'), ('board_id', 'id')]),
    )


class ProjectBoardManager(BaseManager):
    obj_cls = ProjectBoard


class ProjectBranch(GitlabObject):
    _url = '/projects/%(project_id)s/repository/branches'
    _constructorTypes = {'author': 'User', "committer": "User"}

    idAttr = 'name'
    canUpdate = False
    requiredUrlAttrs = ['project_id']
    requiredCreateAttrs = ['branch_name', 'ref']

    def protect(self, protect=True, **kwargs):
        """Protects the branch."""
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
        """Unprotects the branch."""
        self.protect(False, **kwargs)


class ProjectBranchManager(BaseManager):
    obj_cls = ProjectBranch


class ProjectBuild(GitlabObject):
    _url = '/projects/%(project_id)s/builds'
    _constructorTypes = {'user': 'User',
                         'commit': 'ProjectCommit',
                         'runner': 'Runner'}
    requiredUrlAttrs = ['project_id']
    canDelete = False
    canUpdate = False
    canCreate = False

    def cancel(self, **kwargs):
        """Cancel the build."""
        url = '/projects/%s/builds/%s/cancel' % (self.project_id, self.id)
        r = self.gitlab._raw_post(url)
        raise_error_from_response(r, GitlabBuildCancelError, 201)

    def retry(self, **kwargs):
        """Retry the build."""
        url = '/projects/%s/builds/%s/retry' % (self.project_id, self.id)
        r = self.gitlab._raw_post(url)
        raise_error_from_response(r, GitlabBuildRetryError, 201)

    def play(self, **kwargs):
        """Trigger a build explicitly."""
        url = '/projects/%s/builds/%s/play' % (self.project_id, self.id)
        r = self.gitlab._raw_post(url)
        raise_error_from_response(r, GitlabBuildPlayError)

    def erase(self, **kwargs):
        """Erase the build (remove build artifacts and trace)."""
        url = '/projects/%s/builds/%s/erase' % (self.project_id, self.id)
        r = self.gitlab._raw_post(url)
        raise_error_from_response(r, GitlabBuildEraseError, 201)

    def keep_artifacts(self, **kwargs):
        """Prevent artifacts from being delete when expiration is set.

        Raises:
            GitlabConnectionError: If the server cannot be reached.
            GitlabCreateError: If the request failed.
        """
        url = ('/projects/%s/builds/%s/artifacts/keep' %
               (self.project_id, self.id))
        r = self.gitlab._raw_post(url)
        raise_error_from_response(r, GitlabGetError, 200)

    def artifacts(self, streamed=False, action=None, chunk_size=1024,
                  **kwargs):
        """Get the build artifacts.

        Args:
            streamed (bool): If True the data will be processed by chunks of
                `chunk_size` and each chunk is passed to `action` for
                treatment.
            action (callable): Callable responsible of dealing with chunk of
                data.
            chunk_size (int): Size of each chunk.

        Returns:
            str: The artifacts if `streamed` is False, None otherwise.

        Raises:
            GitlabConnectionError: If the server cannot be reached.
            GitlabGetError: If the artifacts are not available.
        """
        url = '/projects/%s/builds/%s/artifacts' % (self.project_id, self.id)
        r = self.gitlab._raw_get(url, streamed=streamed, **kwargs)
        raise_error_from_response(r, GitlabGetError, 200)
        return utils.response_content(r, streamed, action, chunk_size)

    def trace(self, streamed=False, action=None, chunk_size=1024, **kwargs):
        """Get the build trace.

        Args:
            streamed (bool): If True the data will be processed by chunks of
                `chunk_size` and each chunk is passed to `action` for
                treatment.
            action (callable): Callable responsible of dealing with chunk of
                data.
            chunk_size (int): Size of each chunk.

        Returns:
            str: The trace.

        Raises:
            GitlabConnectionError: If the server cannot be reached.
            GitlabGetError: If the trace is not available.
        """
        url = '/projects/%s/builds/%s/trace' % (self.project_id, self.id)
        r = self.gitlab._raw_get(url, streamed=streamed, **kwargs)
        raise_error_from_response(r, GitlabGetError, 200)
        return utils.response_content(r, streamed, action, chunk_size)


class ProjectBuildManager(BaseManager):
    obj_cls = ProjectBuild


class ProjectCommitStatus(GitlabObject):
    _url = '/projects/%(project_id)s/repository/commits/%(commit_id)s/statuses'
    _create_url = '/projects/%(project_id)s/statuses/%(commit_id)s'
    canUpdate = False
    canDelete = False
    requiredUrlAttrs = ['project_id', 'commit_id']
    optionalGetAttrs = ['ref_name', 'stage', 'name', 'all']
    requiredCreateAttrs = ['state']
    optionalCreateAttrs = ['description', 'name', 'context', 'ref',
                           'target_url']


class ProjectCommitStatusManager(BaseManager):
    obj_cls = ProjectCommitStatus


class ProjectCommitComment(GitlabObject):
    _url = '/projects/%(project_id)s/repository/commits/%(commit_id)s/comments'
    canUpdate = False
    canGet = False
    canDelete = False
    requiredUrlAttrs = ['project_id', 'commit_id']
    requiredCreateAttrs = ['note']
    optionalCreateAttrs = ['path', 'line', 'line_type']


class ProjectCommitCommentManager(BaseManager):
    obj_cls = ProjectCommitComment


class ProjectCommit(GitlabObject):
    _url = '/projects/%(project_id)s/repository/commits'
    canDelete = False
    canUpdate = False
    requiredUrlAttrs = ['project_id']
    requiredCreateAttrs = ['branch_name', 'commit_message', 'actions']
    optionalCreateAttrs = ['author_email', 'author_name']
    shortPrintAttr = 'title'
    managers = (
        ('comments', 'ProjectCommitCommentManager',
            [('project_id', 'project_id'), ('commit_id', 'id')]),
        ('statuses', 'ProjectCommitStatusManager',
            [('project_id', 'project_id'), ('commit_id', 'id')]),
    )

    def diff(self, **kwargs):
        """Generate the commit diff."""
        url = ('/projects/%(project_id)s/repository/commits/%(commit_id)s/diff'
               % {'project_id': self.project_id, 'commit_id': self.id})
        r = self.gitlab._raw_get(url, **kwargs)
        raise_error_from_response(r, GitlabGetError)

        return r.json()

    def blob(self, filepath, streamed=False, action=None, chunk_size=1024,
             **kwargs):
        """Generate the content of a file for this commit.

        Args:
            filepath (str): Path of the file to request.
            streamed (bool): If True the data will be processed by chunks of
                `chunk_size` and each chunk is passed to `action` for
                treatment.
            action (callable): Callable responsible of dealing with chunk of
                data.
            chunk_size (int): Size of each chunk.

        Returns:
            str: The content of the file

        Raises:
            GitlabConnectionError: If the server cannot be reached.
            GitlabGetError: If the server fails to perform the request.
        """
        url = ('/projects/%(project_id)s/repository/blobs/%(commit_id)s' %
               {'project_id': self.project_id, 'commit_id': self.id})
        url += '?filepath=%s' % filepath
        r = self.gitlab._raw_get(url, streamed=streamed, **kwargs)
        raise_error_from_response(r, GitlabGetError)
        return utils.response_content(r, streamed, action, chunk_size)

    def builds(self, **kwargs):
        """List the build for this commit.

        Returns:
            list(ProjectBuild): A list of builds.

        Raises:
            GitlabConnectionError: If the server cannot be reached.
            GitlabListError: If the server fails to perform the request.
        """
        url = '/projects/%s/repository/commits/%s/builds' % (self.project_id,
                                                             self.id)
        return self.gitlab._raw_list(url, ProjectBuild, **kwargs)

    def cherry_pick(self, branch, **kwargs):
        """Cherry-pick a commit into a branch.

        Args:
            branch (str): Name of target branch.

        Raises:
            GitlabCherryPickError: If the cherry pick could not be applied.
        """
        url = ('/projects/%s/repository/commits/%s/cherry_pick' %
               (self.project_id, self.id))

        r = self.gitlab._raw_post(url, data={'project_id': self.project_id,
                                             'branch': branch}, **kwargs)
        errors = {400: GitlabCherryPickError}
        raise_error_from_response(r, errors, expected_code=201)


class ProjectCommitManager(BaseManager):
    obj_cls = ProjectCommit


class ProjectEnvironment(GitlabObject):
    _url = '/projects/%(project_id)s/environments'
    canGet = 'from_list'
    requiredUrlAttrs = ['project_id']
    requiredCreateAttrs = ['name']
    optionalCreateAttrs = ['external_url']
    optionalUpdateAttrs = ['name', 'external_url']


class ProjectEnvironmentManager(BaseManager):
    obj_cls = ProjectEnvironment


class ProjectKey(GitlabObject):
    _url = '/projects/%(project_id)s/keys'
    canUpdate = False
    requiredUrlAttrs = ['project_id']
    requiredCreateAttrs = ['title', 'key']


class ProjectKeyManager(BaseManager):
    obj_cls = ProjectKey

    def enable(self, key_id):
        """Enable a deploy key for a project."""
        url = '/projects/%s/deploy_keys/%s/enable' % (self.parent.id, key_id)
        r = self.gitlab._raw_post(url)
        raise_error_from_response(r, GitlabProjectDeployKeyError, 201)

    def disable(self, key_id):
        """Disable a deploy key for a project."""
        url = '/projects/%s/deploy_keys/%s/disable' % (self.parent.id, key_id)
        r = self.gitlab._raw_delete(url)
        raise_error_from_response(r, GitlabProjectDeployKeyError, 200)


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
    optionalCreateAttrs = ['namespace']


class ProjectForkManager(BaseManager):
    obj_cls = ProjectFork


class ProjectHook(GitlabObject):
    _url = '/projects/%(project_id)s/hooks'
    requiredUrlAttrs = ['project_id']
    requiredCreateAttrs = ['url']
    optionalCreateAttrs = ['push_events', 'issues_events', 'note_events',
                           'merge_requests_events', 'tag_push_events',
                           'build_events', 'enable_ssl_verification', 'token',
                           'pipeline_events']
    shortPrintAttr = 'url'


class ProjectHookManager(BaseManager):
    obj_cls = ProjectHook


class ProjectIssueNote(GitlabObject):
    _url = '/projects/%(project_id)s/issues/%(issue_id)s/notes'
    _constructorTypes = {'author': 'User'}
    canDelete = False
    requiredUrlAttrs = ['project_id', 'issue_id']
    requiredCreateAttrs = ['body']
    optionalCreateAttrs = ['created_at']


class ProjectIssueNoteManager(BaseManager):
    obj_cls = ProjectIssueNote


class ProjectIssue(GitlabObject):
    _url = '/projects/%(project_id)s/issues/'
    _constructorTypes = {'author': 'User', 'assignee': 'User',
                         'milestone': 'ProjectMilestone'}
    optionalListAttrs = ['state', 'labels', 'milestone', 'iid', 'order_by',
                         'sort']
    requiredUrlAttrs = ['project_id']
    requiredCreateAttrs = ['title']
    optionalCreateAttrs = ['description', 'assignee_id', 'milestone_id',
                           'labels', 'created_at', 'due_date']
    optionalUpdateAttrs = ['title', 'description', 'assignee_id',
                           'milestone_id', 'labels', 'created_at',
                           'updated_at', 'state_event', 'due_date']
    shortPrintAttr = 'title'
    managers = (
        ('notes', 'ProjectIssueNoteManager',
            [('project_id', 'project_id'), ('issue_id', 'id')]),
    )

    def subscribe(self, **kwargs):
        """Subscribe to an issue.

        Raises:
            GitlabConnectionError: If the server cannot be reached.
            GitlabSubscribeError: If the subscription cannot be done
        """
        url = ('/projects/%(project_id)s/issues/%(issue_id)s/subscription' %
               {'project_id': self.project_id, 'issue_id': self.id})

        r = self.gitlab._raw_post(url, **kwargs)
        raise_error_from_response(r, GitlabSubscribeError)
        self._set_from_dict(r.json())

    def unsubscribe(self, **kwargs):
        """Unsubscribe an issue.

        Raises:
            GitlabConnectionError: If the server cannot be reached.
            GitlabUnsubscribeError: If the unsubscription cannot be done
        """
        url = ('/projects/%(project_id)s/issues/%(issue_id)s/subscription' %
               {'project_id': self.project_id, 'issue_id': self.id})

        r = self.gitlab._raw_delete(url, **kwargs)
        raise_error_from_response(r, GitlabUnsubscribeError)
        self._set_from_dict(r.json())

    def move(self, to_project_id, **kwargs):
        """Move the issue to another project.

        Raises:
            GitlabConnectionError: If the server cannot be reached.
        """
        url = ('/projects/%(project_id)s/issues/%(issue_id)s/move' %
               {'project_id': self.project_id, 'issue_id': self.id})

        data = {'to_project_id': to_project_id}
        data.update(**kwargs)
        r = self.gitlab._raw_post(url, data=data)
        raise_error_from_response(r, GitlabUpdateError, 201)
        self._set_from_dict(r.json())

    def todo(self, **kwargs):
        """Create a todo for the issue.

        Raises:
            GitlabConnectionError: If the server cannot be reached.
        """
        url = ('/projects/%(project_id)s/issues/%(issue_id)s/todo' %
               {'project_id': self.project_id, 'issue_id': self.id})
        r = self.gitlab._raw_post(url, **kwargs)
        raise_error_from_response(r, GitlabTodoError, [201, 304])

    def time_stats(self, **kwargs):
        """Get time stats for the issue.

        Raises:
            GitlabConnectionError: If the server cannot be reached.
        """
        url = ('/projects/%(project_id)s/issues/%(issue_id)s/time_stats' %
               {'project_id': self.project_id, 'issue_id': self.id})
        r = self.gitlab._raw_get(url, **kwargs)
        raise_error_from_response(r, GitlabGetError)
        return r.json()

    def time_estimate(self, **kwargs):
        """Set an estimated time of work for the issue.

        Raises:
            GitlabConnectionError: If the server cannot be reached.
        """
        url = ('/projects/%(project_id)s/issues/%(issue_id)s/time_estimate' %
               {'project_id': self.project_id, 'issue_id': self.id})
        r = self.gitlab._raw_post(url, **kwargs)
        raise_error_from_response(r, GitlabTimeTrackingError, 201)
        return r.json()

    def reset_time_estimate(self, **kwargs):
        """Resets estimated time for the issue to 0 seconds.

        Raises:
            GitlabConnectionError: If the server cannot be reached.
        """
        url = ('/projects/%(project_id)s/issues/%(issue_id)s/'
               'reset_time_estimate' %
               {'project_id': self.project_id, 'issue_id': self.id})
        r = self.gitlab._raw_post(url, **kwargs)
        raise_error_from_response(r, GitlabTimeTrackingError, 200)
        return r.json()

    def add_spent_time(self, **kwargs):
        """Set an estimated time of work for the issue.

        Raises:
            GitlabConnectionError: If the server cannot be reached.
        """
        url = ('/projects/%(project_id)s/issues/%(issue_id)s/'
               'add_spent_time' %
               {'project_id': self.project_id, 'issue_id': self.id})
        r = self.gitlab._raw_post(url, **kwargs)
        raise_error_from_response(r, GitlabTimeTrackingError, 200)
        return r.json()

    def reset_spent_time(self, **kwargs):
        """Set an estimated time of work for the issue.

        Raises:
            GitlabConnectionError: If the server cannot be reached.
        """
        url = ('/projects/%(project_id)s/issues/%(issue_id)s/'
               'reset_spent_time' %
               {'project_id': self.project_id, 'issue_id': self.id})
        r = self.gitlab._raw_post(url, **kwargs)
        raise_error_from_response(r, GitlabTimeTrackingError, 200)
        return r.json()


class ProjectIssueManager(BaseManager):
    obj_cls = ProjectIssue


class ProjectMember(GitlabObject):
    _url = '/projects/%(project_id)s/members'
    requiredUrlAttrs = ['project_id']
    requiredCreateAttrs = ['access_level', 'user_id']
    optionalCreateAttrs = ['expires_at']
    requiredUpdateAttrs = ['access_level']
    optionalCreateAttrs = ['expires_at']
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


class ProjectNotificationSettings(NotificationSettings):
    _url = '/projects/%(project_id)s/notification_settings'
    requiredUrlAttrs = ['project_id']


class ProjectNotificationSettingsManager(BaseManager):
    obj_cls = ProjectNotificationSettings


class ProjectTagRelease(GitlabObject):
    _url = '/projects/%(project_id)s/repository/tags/%(tag_name)/release'
    canDelete = False
    canList = False
    requiredUrlAttrs = ['project_id', 'tag_name']
    requiredCreateAttrs = ['description']
    shortPrintAttr = 'description'


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
        """Set the release notes on the tag.

        If the release doesn't exist yet, it will be created. If it already
        exists, its description will be updated.

        Args:
            description (str): Description of the release.

        Raises:
            GitlabConnectionError: If the server cannot be reached.
            GitlabCreateError: If the server fails to create the release.
            GitlabUpdateError: If the server fails to update the release.
        """
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


class ProjectMergeRequestDiff(GitlabObject):
    _url = ('/projects/%(project_id)s/merge_requests/'
            '%(merge_request_id)s/versions')
    canCreate = False
    canUpdate = False
    canDelete = False
    requiredUrlAttrs = ['project_id', 'merge_request_id']


class ProjectMergeRequestDiffManager(BaseManager):
    obj_cls = ProjectMergeRequestDiff


class ProjectMergeRequestNote(GitlabObject):
    _url = '/projects/%(project_id)s/merge_requests/%(merge_request_id)s/notes'
    _constructorTypes = {'author': 'User'}
    requiredUrlAttrs = ['project_id', 'merge_request_id']
    requiredCreateAttrs = ['body']


class ProjectMergeRequestNoteManager(BaseManager):
    obj_cls = ProjectMergeRequestNote


class ProjectMergeRequest(GitlabObject):
    _url = '/projects/%(project_id)s/merge_requests'
    _constructorTypes = {'author': 'User', 'assignee': 'User'}
    requiredUrlAttrs = ['project_id']
    requiredCreateAttrs = ['source_branch', 'target_branch', 'title']
    optionalCreateAttrs = ['assignee_id', 'description', 'target_project_id',
                           'labels', 'milestone_id', 'remove_source_branch']
    optionalUpdateAttrs = ['target_branch', 'assignee_id', 'title',
                           'description', 'state_event', 'labels',
                           'milestone_id']
    optionalListAttrs = ['iid', 'state', 'order_by', 'sort']

    managers = (
        ('notes', 'ProjectMergeRequestNoteManager',
            [('project_id', 'project_id'), ('merge_request_id', 'id')]),
        ('diffs', 'ProjectMergeRequestDiffManager',
            [('project_id', 'project_id'), ('merge_request_id', 'id')]),
    )

    def _data_for_gitlab(self, extra_parameters={}, update=False,
                         as_json=True):
        data = (super(ProjectMergeRequest, self)
                ._data_for_gitlab(extra_parameters, update=update,
                                  as_json=False))
        if update:
            # Drop source_branch attribute as it is not accepted by the gitlab
            # server (Issue #76)
            data.pop('source_branch', None)
        return json.dumps(data)

    def subscribe(self, **kwargs):
        """Subscribe to a MR.

        Raises:
            GitlabConnectionError: If the server cannot be reached.
            GitlabSubscribeError: If the subscription cannot be done
        """
        url = ('/projects/%(project_id)s/merge_requests/%(mr_id)s/'
               'subscription' %
               {'project_id': self.project_id, 'mr_id': self.id})

        r = self.gitlab._raw_post(url, **kwargs)
        raise_error_from_response(r, GitlabSubscribeError, [201, 304])
        if r.status_code == 201:
            self._set_from_dict(r.json())

    def unsubscribe(self, **kwargs):
        """Unsubscribe a MR.

        Raises:
            GitlabConnectionError: If the server cannot be reached.
            GitlabUnsubscribeError: If the unsubscription cannot be done
        """
        url = ('/projects/%(project_id)s/merge_requests/%(mr_id)s/'
               'subscription' %
               {'project_id': self.project_id, 'mr_id': self.id})

        r = self.gitlab._raw_delete(url, **kwargs)
        raise_error_from_response(r, GitlabUnsubscribeError, [200, 304])
        if r.status_code == 200:
            self._set_from_dict(r.json())

    def cancel_merge_when_build_succeeds(self, **kwargs):
        """Cancel merge when build succeeds."""

        u = ('/projects/%s/merge_requests/%s/cancel_merge_when_build_succeeds'
             % (self.project_id, self.id))
        r = self.gitlab._raw_put(u, **kwargs)
        errors = {401: GitlabMRForbiddenError,
                  405: GitlabMRClosedError,
                  406: GitlabMROnBuildSuccessError}
        raise_error_from_response(r, errors)
        return ProjectMergeRequest(self, r.json())

    def closes_issues(self, **kwargs):
        """List issues closed by the MR.

        Returns:
            list (ProjectIssue): List of closed issues

        Raises:
            GitlabConnectionError: If the server cannot be reached.
            GitlabGetError: If the server fails to perform the request.
        """
        url = ('/projects/%s/merge_requests/%s/closes_issues' %
               (self.project_id, self.id))
        return self.gitlab._raw_list(url, ProjectIssue, **kwargs)

    def commits(self, **kwargs):
        """List the merge request commits.

        Returns:
            list (ProjectCommit): List of commits

        Raises:
            GitlabConnectionError: If the server cannot be reached.
            GitlabListError: If the server fails to perform the request.
        """
        url = ('/projects/%s/merge_requests/%s/commits' %
               (self.project_id, self.id))
        return self.gitlab._raw_list(url, ProjectCommit, **kwargs)

    def changes(self, **kwargs):
        """List the merge request changes.

        Returns:
            list (dict): List of changes

        Raises:
            GitlabConnectionError: If the server cannot be reached.
            GitlabListError: If the server fails to perform the request.
        """
        url = ('/projects/%s/merge_requests/%s/changes' %
               (self.project_id, self.id))
        r = self.gitlab._raw_get(url, **kwargs)
        raise_error_from_response(r, GitlabListError)
        return r.json()

    def merge(self, merge_commit_message=None,
              should_remove_source_branch=False,
              merge_when_build_succeeds=False,
              **kwargs):
        """Accept the merge request.

        Args:
            merge_commit_message (bool): Commit message
            should_remove_source_branch (bool): If True, removes the source
                                                branch
            merge_when_build_succeeds (bool): Wait for the build to succeed,
                                              then merge

        Returns:
            ProjectMergeRequest: The updated MR
        Raises:
            GitlabConnectionError: If the server cannot be reached.
            GitlabMRForbiddenError: If the user doesn't have permission to
                                    close thr MR
            GitlabMRClosedError: If the MR is already closed
        """
        url = '/projects/%s/merge_requests/%s/merge' % (self.project_id,
                                                        self.id)
        data = {}
        if merge_commit_message:
            data['merge_commit_message'] = merge_commit_message
        if should_remove_source_branch:
            data['should_remove_source_branch'] = True
        if merge_when_build_succeeds:
            data['merge_when_build_succeeds'] = True

        r = self.gitlab._raw_put(url, data=data, **kwargs)
        errors = {401: GitlabMRForbiddenError,
                  405: GitlabMRClosedError}
        raise_error_from_response(r, errors)
        self._set_from_dict(r.json())

    def todo(self, **kwargs):
        """Create a todo for the merge request.

        Raises:
            GitlabConnectionError: If the server cannot be reached.
        """
        url = ('/projects/%(project_id)s/merge_requests/%(mr_id)s/todo' %
               {'project_id': self.project_id, 'mr_id': self.id})
        r = self.gitlab._raw_post(url, **kwargs)
        raise_error_from_response(r, GitlabTodoError, [201, 304])

    def time_stats(self, **kwargs):
        """Get time stats for the merge request.

        Raises:
            GitlabConnectionError: If the server cannot be reached.
        """
        url = ('/projects/%(project_id)s/merge_requests/%(mr_id)s/time_stats' %
               {'project_id': self.project_id, 'mr_id': self.id})
        r = self.gitlab._raw_get(url, **kwargs)
        raise_error_from_response(r, GitlabGetError)
        return r.json()

    def time_estimate(self, **kwargs):
        """Set an estimated time of work for the merge request.

        Raises:
            GitlabConnectionError: If the server cannot be reached.
        """
        url = ('/projects/%(project_id)s/merge_requests/%(mr_id)s/'
               'time_estimate' %
               {'project_id': self.project_id, 'mr_id': self.id})
        r = self.gitlab._raw_post(url, **kwargs)
        raise_error_from_response(r, GitlabTimeTrackingError, 201)
        return r.json()

    def reset_time_estimate(self, **kwargs):
        """Resets estimated time for the merge request to 0 seconds.

        Raises:
            GitlabConnectionError: If the server cannot be reached.
        """
        url = ('/projects/%(project_id)s/merge_requests/%(mr_id)s/'
               'reset_time_estimate' %
               {'project_id': self.project_id, 'mr_id': self.id})
        r = self.gitlab._raw_post(url, **kwargs)
        raise_error_from_response(r, GitlabTimeTrackingError, 200)
        return r.json()

    def add_spent_time(self, **kwargs):
        """Set an estimated time of work for the merge request.

        Raises:
            GitlabConnectionError: If the server cannot be reached.
        """
        url = ('/projects/%(project_id)s/merge_requests/%(mr_id)s/'
               'add_spent_time' %
               {'project_id': self.project_id, 'mr_id': self.id})
        r = self.gitlab._raw_post(url, **kwargs)
        raise_error_from_response(r, GitlabTimeTrackingError, 200)
        return r.json()

    def reset_spent_time(self, **kwargs):
        """Set an estimated time of work for the merge request.

        Raises:
            GitlabConnectionError: If the server cannot be reached.
        """
        url = ('/projects/%(project_id)s/merge_requests/%(mr_id)s/'
               'reset_spent_time' %
               {'project_id': self.project_id, 'mr_id': self.id})
        r = self.gitlab._raw_post(url, **kwargs)
        raise_error_from_response(r, GitlabTimeTrackingError, 200)
        return r.json()


class ProjectMergeRequestManager(BaseManager):
    obj_cls = ProjectMergeRequest


class ProjectMilestone(GitlabObject):
    _url = '/projects/%(project_id)s/milestones'
    canDelete = False
    requiredUrlAttrs = ['project_id']
    optionalListAttrs = ['iid', 'state']
    requiredCreateAttrs = ['title']
    optionalCreateAttrs = ['description', 'due_date', 'start_date',
                           'state_event']
    optionalUpdateAttrs = requiredCreateAttrs + optionalCreateAttrs
    shortPrintAttr = 'title'

    def issues(self, **kwargs):
        url = "/projects/%s/milestones/%s/issues" % (self.project_id, self.id)
        return self.gitlab._raw_list(url, ProjectIssue, **kwargs)

    def merge_requests(self, **kwargs):
        """List the merge requests related to this milestone

        Returns:
            list (ProjectMergeRequest): List of merge requests

        Raises:
            GitlabConnectionError: If the server cannot be reached.
            GitlabListError: If the server fails to perform the request.
        """
        url = ('/projects/%s/milestones/%s/merge_requests' %
               (self.project_id, self.id))
        return self.gitlab._raw_list(url, ProjectMergeRequest, **kwargs)


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
    optionalCreateAttrs = ['description', 'priority']
    requiredUpdateAttrs = ['name']
    optionalUpdateAttrs = ['new_name', 'color', 'description', 'priority']

    def subscribe(self, **kwargs):
        """Subscribe to a label.

        Raises:
            GitlabConnectionError: If the server cannot be reached.
            GitlabSubscribeError: If the subscription cannot be done
        """
        url = ('/projects/%(project_id)s/labels/%(label_id)s/subscription' %
               {'project_id': self.project_id, 'label_id': self.name})

        r = self.gitlab._raw_post(url, **kwargs)
        raise_error_from_response(r, GitlabSubscribeError, [201, 304])
        self._set_from_dict(r.json())

    def unsubscribe(self, **kwargs):
        """Unsubscribe a label.

        Raises:
            GitlabConnectionError: If the server cannot be reached.
            GitlabUnsubscribeError: If the unsubscription cannot be done
        """
        url = ('/projects/%(project_id)s/labels/%(label_id)s/subscription' %
               {'project_id': self.project_id, 'label_id': self.name})

        r = self.gitlab._raw_delete(url, **kwargs)
        raise_error_from_response(r, GitlabUnsubscribeError, [200, 304])
        self._set_from_dict(r.json())


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
    requiredDeleteAttrs = ['branch_name', 'commit_message', 'file_path']
    shortPrintAttr = 'file_path'
    getRequiresId = False

    def decode(self):
        """Returns the decoded content of the file.

        Returns:
            (str): the decoded content.
        """
        return base64.b64decode(self.content)


class ProjectFileManager(BaseManager):
    obj_cls = ProjectFile


class ProjectPipeline(GitlabObject):
    _url = '/projects/%(project_id)s/pipelines'
    _create_url = '/projects/%(project_id)s/pipeline'

    canUpdate = False
    canDelete = False

    requiredUrlAttrs = ['project_id']
    requiredCreateAttrs = ['ref']

    def retry(self, **kwargs):
        """Retries failed builds in a pipeline.

        Raises:
            GitlabConnectionError: If the server cannot be reached.
            GitlabPipelineRetryError: If the retry cannot be done.
        """
        url = ('/projects/%(project_id)s/pipelines/%(id)s/retry' %
               {'project_id': self.project_id, 'id': self.id})
        r = self.gitlab._raw_post(url, data=None, content_type=None, **kwargs)
        raise_error_from_response(r, GitlabPipelineRetryError, 201)
        self._set_from_dict(r.json())

    def cancel(self, **kwargs):
        """Cancel builds in a pipeline.

        Raises:
            GitlabConnectionError: If the server cannot be reached.
            GitlabPipelineCancelError: If the retry cannot be done.
        """
        url = ('/projects/%(project_id)s/pipelines/%(id)s/cancel' %
               {'project_id': self.project_id, 'id': self.id})
        r = self.gitlab._raw_post(url, data=None, content_type=None, **kwargs)
        raise_error_from_response(r, GitlabPipelineRetryError, 200)
        self._set_from_dict(r.json())


class ProjectPipelineManager(BaseManager):
    obj_cls = ProjectPipeline


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
    optionalCreateAttrs = ['lifetime', 'visibility_level']
    optionalUpdateAttrs = ['title', 'file_name', 'code', 'visibility_level']
    shortPrintAttr = 'title'
    managers = (
        ('notes', 'ProjectSnippetNoteManager',
            [('project_id', 'project_id'), ('snippet_id', 'id')]),
    )

    def content(self, streamed=False, action=None, chunk_size=1024, **kwargs):
        """Return the raw content of a snippet.

        Args:
            streamed (bool): If True the data will be processed by chunks of
                `chunk_size` and each chunk is passed to `action` for
                treatment.
            action (callable): Callable responsible of dealing with chunk of
                data.
            chunk_size (int): Size of each chunk.

        Returns:
            str: The snippet content

        Raises:
            GitlabConnectionError: If the server cannot be reached.
            GitlabGetError: If the server fails to perform the request.
        """
        url = ("/projects/%(project_id)s/snippets/%(snippet_id)s/raw" %
               {'project_id': self.project_id, 'snippet_id': self.id})
        r = self.gitlab._raw_get(url, **kwargs)
        raise_error_from_response(r, GitlabGetError)
        return utils.response_content(r, streamed, action, chunk_size)


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


class ProjectService(GitlabObject):
    _url = '/projects/%(project_id)s/services/%(service_name)s'
    canList = False
    canCreate = False
    _id_in_update_url = False
    _id_in_delete_url = False
    getRequiresId = False
    requiredUrlAttrs = ['project_id', 'service_name']

    _service_attrs = {
        'asana': (('api_key', ), ('restrict_to_branch', )),
        'assembla': (('token', ), ('subdomain', )),
        'bamboo': (('bamboo_url', 'build_key', 'username', 'password'),
                   tuple()),
        'buildkite': (('token', 'project_url'), ('enable_ssl_verification', )),
        'campfire': (('token', ), ('subdomain', 'room')),
        'custom-issue-tracker': (('new_issue_url', 'issues_url',
                                  'project_url'),
                                 ('description', 'title')),
        'drone-ci': (('token', 'drone_url'), ('enable_ssl_verification', )),
        'emails-on-push': (('recipients', ), ('disable_diffs',
                                              'send_from_committer_email')),
        'builds-email': (('recipients', ), ('add_pusher',
                                            'notify_only_broken_builds')),
        'pipelines-email': (('recipients', ), ('add_pusher',
                                               'notify_only_broken_builds')),
        'external-wiki': (('external_wiki_url', ), tuple()),
        'flowdock': (('token', ), tuple()),
        'gemnasium': (('api_key', 'token', ), tuple()),
        'hipchat': (('token', ), ('color', 'notify', 'room', 'api_version',
                                  'server')),
        'irker': (('recipients', ), ('default_irc_uri', 'server_port',
                                     'server_host', 'colorize_messages')),
        'jira': (tuple(), (
                 # Required fields in GitLab >= 8.14
                 'url', 'project_key',

                 # Required fields in GitLab < 8.14
                 'new_issue_url', 'project_url', 'issues_url', 'api_url',
                 'description',

                 # Optional fields
                 'username', 'password', 'jira_issue_transition_id')),
        'pivotaltracker': (('token', ), tuple()),
        'pushover': (('api_key', 'user_key', 'priority'), ('device', 'sound')),
        'redmine': (('new_issue_url', 'project_url', 'issues_url'),
                    ('description', )),
        'slack': (('webhook', ), ('username', 'channel')),
        'teamcity': (('teamcity_url', 'build_type', 'username', 'password'),
                     tuple())
    }

    def _data_for_gitlab(self, extra_parameters={}, update=False,
                         as_json=True):
        data = (super(ProjectService, self)
                ._data_for_gitlab(extra_parameters, update=update,
                                  as_json=False))
        missing = []
        # Mandatory args
        for attr in self._service_attrs[self.service_name][0]:
            if not hasattr(self, attr):
                missing.append(attr)
            else:
                data[attr] = getattr(self, attr)

        if missing:
            raise GitlabUpdateError('Missing attribute(s): %s' %
                                    ", ".join(missing))

        # Optional args
        for attr in self._service_attrs[self.service_name][1]:
            if hasattr(self, attr):
                data[attr] = getattr(self, attr)

        return json.dumps(data)


class ProjectServiceManager(BaseManager):
    obj_cls = ProjectService

    def available(self, **kwargs):
        """List the services known by python-gitlab.

        Returns:
            list (str): The list of service code names.
        """
        return list(ProjectService._service_attrs.keys())


class ProjectAccessRequest(GitlabObject):
    _url = '/projects/%(project_id)s/access_requests'
    canGet = 'from_list'
    canUpdate = False

    def approve(self, access_level=gitlab.DEVELOPER_ACCESS, **kwargs):
        """Approve an access request.

        Args:
            access_level (int): The access level for the user.

        Raises:
            GitlabConnectionError: If the server cannot be reached.
            GitlabUpdateError: If the server fails to perform the request.
        """

        url = ('/projects/%(project_id)s/access_requests/%(id)s/approve' %
               {'project_id': self.project_id, 'id': self.id})
        data = {'access_level': access_level}
        r = self.gitlab._raw_put(url, data=data, **kwargs)
        raise_error_from_response(r, GitlabUpdateError, 201)
        self._set_from_dict(r.json())


class ProjectAccessRequestManager(BaseManager):
    obj_cls = ProjectAccessRequest


class ProjectDeployment(GitlabObject):
    _url = '/projects/%(project_id)s/deployments'
    canCreate = False
    canUpdate = False
    canDelete = False


class ProjectDeploymentManager(BaseManager):
    obj_cls = ProjectDeployment


class ProjectRunner(GitlabObject):
    _url = '/projects/%(project_id)s/runners'
    canUpdate = False
    requiredCreateAttrs = ['runner_id']


class ProjectRunnerManager(BaseManager):
    obj_cls = ProjectRunner


class Project(GitlabObject):
    _url = '/projects'
    _constructorTypes = {'owner': 'User', 'namespace': 'Group'}
    optionalListAttrs = ['search']
    requiredCreateAttrs = ['name']
    optionalListAttrs = ['search']
    optionalCreateAttrs = ['path', 'namespace_id', 'description',
                           'issues_enabled', 'merge_requests_enabled',
                           'builds_enabled', 'wiki_enabled',
                           'snippets_enabled', 'container_registry_enabled',
                           'shared_runners_enabled', 'public',
                           'visibility_level', 'import_url', 'public_builds',
                           'only_allow_merge_if_build_succeeds',
                           'only_allow_merge_if_all_discussions_are_resolved',
                           'lfs_enabled', 'request_access_enabled']
    optionalUpdateAttrs = ['name', 'path', 'default_branch', 'description',
                           'issues_enabled', 'merge_requests_enabled',
                           'builds_enabled', 'wiki_enabled',
                           'snippets_enabled', 'container_registry_enabled',
                           'shared_runners_enabled', 'public',
                           'visibility_level', 'import_url', 'public_builds',
                           'only_allow_merge_if_build_succeeds',
                           'only_allow_merge_if_all_discussions_are_resolved',
                           'lfs_enabled', 'request_access_enabled']
    shortPrintAttr = 'path'
    managers = (
        ('accessrequests', 'ProjectAccessRequestManager',
         [('project_id', 'id')]),
        ('boards', 'ProjectBoardManager', [('project_id', 'id')]),
        ('board_lists', 'ProjectBoardListManager', [('project_id', 'id')]),
        ('branches', 'ProjectBranchManager', [('project_id', 'id')]),
        ('builds', 'ProjectBuildManager', [('project_id', 'id')]),
        ('commits', 'ProjectCommitManager', [('project_id', 'id')]),
        ('deployments', 'ProjectDeploymentManager', [('project_id', 'id')]),
        ('environments', 'ProjectEnvironmentManager', [('project_id', 'id')]),
        ('events', 'ProjectEventManager', [('project_id', 'id')]),
        ('files', 'ProjectFileManager', [('project_id', 'id')]),
        ('forks', 'ProjectForkManager', [('project_id', 'id')]),
        ('hooks', 'ProjectHookManager', [('project_id', 'id')]),
        ('keys', 'ProjectKeyManager', [('project_id', 'id')]),
        ('issues', 'ProjectIssueManager', [('project_id', 'id')]),
        ('labels', 'ProjectLabelManager', [('project_id', 'id')]),
        ('members', 'ProjectMemberManager', [('project_id', 'id')]),
        ('mergerequests', 'ProjectMergeRequestManager',
         [('project_id', 'id')]),
        ('milestones', 'ProjectMilestoneManager', [('project_id', 'id')]),
        ('notes', 'ProjectNoteManager', [('project_id', 'id')]),
        ('notificationsettings', 'ProjectNotificationSettingsManager',
         [('project_id', 'id')]),
        ('pipelines', 'ProjectPipelineManager', [('project_id', 'id')]),
        ('runners', 'ProjectRunnerManager', [('project_id', 'id')]),
        ('services', 'ProjectServiceManager', [('project_id', 'id')]),
        ('snippets', 'ProjectSnippetManager', [('project_id', 'id')]),
        ('tags', 'ProjectTagManager', [('project_id', 'id')]),
        ('triggers', 'ProjectTriggerManager', [('project_id', 'id')]),
        ('variables', 'ProjectVariableManager', [('project_id', 'id')]),
    )

    VISIBILITY_PRIVATE = gitlab.VISIBILITY_PRIVATE
    VISIBILITY_INTERNAL = gitlab.VISIBILITY_INTERNAL
    VISIBILITY_PUBLIC = gitlab.VISIBILITY_PUBLIC

    def repository_tree(self, path='', ref_name='', **kwargs):
        """Return a list of files in the repository.

        Args:
            path (str): Path of the top folder (/ by default)
            ref_name (str): Reference to a commit or branch

        Returns:
            str: The json representation of the tree.

        Raises:
            GitlabConnectionError: If the server cannot be reached.
            GitlabGetError: If the server fails to perform the request.
        """
        url = "/projects/%s/repository/tree" % (self.id)
        params = []
        if path:
            params.append(urllib.parse.urlencode({'path': path}))
        if ref_name:
            params.append("ref_name=%s" % ref_name)
        if params:
            url += '?' + "&".join(params)
        r = self.gitlab._raw_get(url, **kwargs)
        raise_error_from_response(r, GitlabGetError)
        return r.json()

    def repository_blob(self, sha, filepath, streamed=False, action=None,
                        chunk_size=1024, **kwargs):
        """Return the content of a file for a commit.

        Args:
            sha (str): ID of the commit
            filepath (str): Path of the file to return
            streamed (bool): If True the data will be processed by chunks of
                `chunk_size` and each chunk is passed to `action` for
                treatment.
            action (callable): Callable responsible of dealing with chunk of
                data.
            chunk_size (int): Size of each chunk.

        Returns:
            str: The file content

        Raises:
            GitlabConnectionError: If the server cannot be reached.
            GitlabGetError: If the server fails to perform the request.
        """
        url = "/projects/%s/repository/blobs/%s" % (self.id, sha)
        url += '?%s' % (urllib.parse.urlencode({'filepath': filepath}))
        r = self.gitlab._raw_get(url, streamed=streamed, **kwargs)
        raise_error_from_response(r, GitlabGetError)
        return utils.response_content(r, streamed, action, chunk_size)

    def repository_raw_blob(self, sha, streamed=False, action=None,
                            chunk_size=1024, **kwargs):
        """Returns the raw file contents for a blob by blob SHA.

        Args:
            sha(str): ID of the blob
            streamed (bool): If True the data will be processed by chunks of
                `chunk_size` and each chunk is passed to `action` for
                treatment.
            action (callable): Callable responsible of dealing with chunk of
                data.
            chunk_size (int): Size of each chunk.

        Returns:
            str: The blob content

        Raises:
            GitlabConnectionError: If the server cannot be reached.
            GitlabGetError: If the server fails to perform the request.
        """
        url = "/projects/%s/repository/raw_blobs/%s" % (self.id, sha)
        r = self.gitlab._raw_get(url, streamed=streamed, **kwargs)
        raise_error_from_response(r, GitlabGetError)
        return utils.response_content(r, streamed, action, chunk_size)

    def repository_compare(self, from_, to, **kwargs):
        """Returns a diff between two branches/commits.

        Args:
            from_(str): orig branch/SHA
            to(str): dest branch/SHA

        Returns:
            str: The diff

        Raises:
            GitlabConnectionError: If the server cannot be reached.
            GitlabGetError: If the server fails to perform the request.
        """
        url = "/projects/%s/repository/compare" % self.id
        url = "%s?from=%s&to=%s" % (url, from_, to)
        r = self.gitlab._raw_get(url, **kwargs)
        raise_error_from_response(r, GitlabGetError)
        return r.json()

    def repository_contributors(self):
        """Returns a list of contributors for the project.

        Returns:
            list: The contibutors

        Raises:
            GitlabConnectionError: If the server cannot be reached.
            GitlabGetError: If the server fails to perform the request.
        """
        url = "/projects/%s/repository/contributors" % self.id
        r = self.gitlab._raw_get(url)
        raise_error_from_response(r, GitlabListError)
        return r.json()

    def repository_archive(self, sha=None, streamed=False, action=None,
                           chunk_size=1024, **kwargs):
        """Return a tarball of the repository.

        Args:
            sha (str): ID of the commit (default branch by default).
            streamed (bool): If True the data will be processed by chunks of
                `chunk_size` and each chunk is passed to `action` for
                treatment.
            action (callable): Callable responsible of dealing with chunk of
                data.
            chunk_size (int): Size of each chunk.

        Returns:
            str: The binary data of the archive.

        Raises:
            GitlabConnectionError: If the server cannot be reached.
            GitlabGetError: If the server fails to perform the request.
        """
        url = '/projects/%s/repository/archive' % self.id
        if sha:
            url += '?sha=%s' % sha
        r = self.gitlab._raw_get(url, streamed=streamed, **kwargs)
        raise_error_from_response(r, GitlabGetError)
        return utils.response_content(r, streamed, action, chunk_size)

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

    def star(self, **kwargs):
        """Star a project.

        Returns:
            Project: the updated Project

        Raises:
            GitlabCreateError: If the action cannot be done
            GitlabConnectionError: If the server cannot be reached.
        """
        url = "/projects/%s/star" % self.id
        r = self.gitlab._raw_post(url, **kwargs)
        raise_error_from_response(r, GitlabCreateError, [201, 304])
        return Project(self.gitlab, r.json()) if r.status_code == 201 else self

    def unstar(self, **kwargs):
        """Unstar a project.

        Returns:
            Project: the updated Project

        Raises:
            GitlabDeleteError: If the action cannot be done
            GitlabConnectionError: If the server cannot be reached.
        """
        url = "/projects/%s/star" % self.id
        r = self.gitlab._raw_delete(url, **kwargs)
        raise_error_from_response(r, GitlabDeleteError, [200, 304])
        return Project(self.gitlab, r.json()) if r.status_code == 200 else self

    def archive(self, **kwargs):
        """Archive a project.

        Returns:
            Project: the updated Project

        Raises:
            GitlabCreateError: If the action cannot be done
            GitlabConnectionError: If the server cannot be reached.
        """
        url = "/projects/%s/archive" % self.id
        r = self.gitlab._raw_post(url, **kwargs)
        raise_error_from_response(r, GitlabCreateError, 201)
        return Project(self.gitlab, r.json()) if r.status_code == 201 else self

    def archive_(self, **kwargs):
        warnings.warn("`archive_()` is deprecated, use `archive()` instead",
                      DeprecationWarning)
        return self.archive(**kwargs)

    def unarchive(self, **kwargs):
        """Unarchive a project.

        Returns:
            Project: the updated Project

        Raises:
            GitlabDeleteError: If the action cannot be done
            GitlabConnectionError: If the server cannot be reached.
        """
        url = "/projects/%s/unarchive" % self.id
        r = self.gitlab._raw_delete(url, **kwargs)
        raise_error_from_response(r, GitlabCreateError, 201)
        return Project(self.gitlab, r.json()) if r.status_code == 201 else self

    def unarchive_(self, **kwargs):
        warnings.warn("`unarchive_()` is deprecated, "
                      "use `unarchive()` instead",
                      DeprecationWarning)
        return self.unarchive(**kwargs)

    def share(self, group_id, group_access, **kwargs):
        """Share the project with a group.

        Args:
            group_id (int): ID of the group.
            group_access (int): Access level for the group.

        Raises:
            GitlabConnectionError: If the server cannot be reached.
            GitlabCreateError: If the server fails to perform the request.
        """
        url = "/projects/%s/share" % self.id
        data = {'group_id': group_id, 'group_access': group_access}
        r = self.gitlab._raw_post(url, data=data, **kwargs)
        raise_error_from_response(r, GitlabCreateError, 201)

    def trigger_build(self, ref, token, variables={}, **kwargs):
        """Trigger a CI build.

        See https://gitlab.com/help/ci/triggers/README.md#trigger-a-build

        Args:
            ref (str): Commit to build; can be a commit SHA, a branch name, ...
            token (str): The trigger token
            variables (dict): Variables passed to the build script

        Raises:
            GitlabConnectionError: If the server cannot be reached.
            GitlabCreateError: If the server fails to perform the request.
        """
        url = "/projects/%s/trigger/builds" % self.id
        form = {r'variables[%s]' % k: v for k, v in six.iteritems(variables)}
        data = {'ref': ref, 'token': token}
        data.update(form)
        r = self.gitlab._raw_post(url, data=data, **kwargs)
        raise_error_from_response(r, GitlabCreateError, 201)


class Runner(GitlabObject):
    _url = '/runners'
    canCreate = False
    optionalUpdateAttrs = ['description', 'active', 'tag_list']
    optionalListAttrs = ['scope']


class RunnerManager(BaseManager):
    obj_cls = Runner

    def all(self, scope=None, **kwargs):
        """List all the runners.

        Args:
            scope (str): The scope of runners to show, one of: specific,
                shared, active, paused, online

        Returns:
            list(Runner): a list of runners matching the scope.

        Raises:
            GitlabConnectionError: If the server cannot be reached.
            GitlabListError: If the resource cannot be found
        """
        url = '/runners/all'
        if scope is not None:
            url += '?scope=' + scope
        return self.gitlab._raw_list(url, self.obj_cls, **kwargs)


class TeamMember(GitlabObject):
    _url = '/user_teams/%(team_id)s/members'
    canUpdate = False
    requiredUrlAttrs = ['teamd_id']
    requiredCreateAttrs = ['access_level']
    shortPrintAttr = 'username'


class Todo(GitlabObject):
    _url = '/todos'
    canGet = 'from_list'
    canUpdate = False
    canCreate = False
    optionalListAttrs = ['action', 'author_id', 'project_id', 'state', 'type']


class TodoManager(BaseManager):
    obj_cls = Todo

    def delete_all(self, **kwargs):
        """Mark all the todos as done.

        Raises:
            GitlabConnectionError: If the server cannot be reached.
            GitlabDeleteError: If the resource cannot be found

        Returns:
            The number of todos maked done.
        """
        url = '/todos'
        r = self.gitlab._raw_delete(url, **kwargs)
        raise_error_from_response(r, GitlabDeleteError)
        return int(r.text)


class ProjectManager(BaseManager):
    obj_cls = Project

    def search(self, query, **kwargs):
        """Search projects by name.

        API v3 only.

        .. note::

           The search is only performed on the project name (not on the
           namespace or the description). To perform a smarter search, use the
           ``search`` argument of the ``list()`` method:

           .. code-block:: python

               gl.projects.list(search=your_search_string)

        Args:
            query (str): The query string to send to GitLab for the search.
            all (bool): If True, return all the items, without pagination
            **kwargs: Additional arguments to send to GitLab.

        Returns:
            list(gitlab.Gitlab.Project): A list of matching projects.
        """
        if self.gitlab.api_version == '4':
            raise NotImplementedError("Not supported by v4 API")

        return self.gitlab._raw_list("/projects/search/" + query, Project,
                                     **kwargs)

    def all(self, **kwargs):
        """List all the projects (need admin rights).

        Args:
            all (bool): If True, return all the items, without pagination
            **kwargs: Additional arguments to send to GitLab.

        Returns:
            list(gitlab.Gitlab.Project): The list of projects.
        """
        return self.gitlab._raw_list("/projects/all", Project, **kwargs)

    def owned(self, **kwargs):
        """List owned projects.

        Args:
            all (bool): If True, return all the items, without pagination
            **kwargs: Additional arguments to send to GitLab.

        Returns:
            list(gitlab.Gitlab.Project): The list of owned projects.
        """
        return self.gitlab._raw_list("/projects/owned", Project, **kwargs)

    def starred(self, **kwargs):
        """List starred projects.

        Args:
            all (bool): If True, return all the items, without pagination
            **kwargs: Additional arguments to send to GitLab.

        Returns:
            list(gitlab.Gitlab.Project): The list of starred projects.
        """
        return self.gitlab._raw_list("/projects/starred", Project, **kwargs)


class GroupProject(Project):
    _url = '/groups/%(group_id)s/projects'
    canGet = 'from_list'
    canCreate = False
    canDelete = False
    canUpdate = False
    optionalListAttrs = ['archived', 'visibility', 'order_by', 'sort',
                         'search', 'ci_enabled_first']

    def __init__(self, *args, **kwargs):
        Project.__init__(self, *args, **kwargs)


class GroupProjectManager(ProjectManager):
    obj_cls = GroupProject


class Group(GitlabObject):
    _url = '/groups'
    requiredCreateAttrs = ['name', 'path']
    optionalCreateAttrs = ['description', 'visibility_level', 'parent_id',
                           'lfs_enabled', 'request_access_enabled']
    optionalUpdateAttrs = ['name', 'path', 'description', 'visibility_level',
                           'lfs_enabled', 'request_access_enabled']
    shortPrintAttr = 'name'
    managers = (
        ('accessrequests', 'GroupAccessRequestManager', [('group_id', 'id')]),
        ('members', 'GroupMemberManager', [('group_id', 'id')]),
        ('notificationsettings', 'GroupNotificationSettingsManager',
         [('group_id', 'id')]),
        ('projects', 'GroupProjectManager', [('group_id', 'id')]),
        ('issues', 'GroupIssueManager', [('group_id', 'id')]),
    )

    GUEST_ACCESS = gitlab.GUEST_ACCESS
    REPORTER_ACCESS = gitlab.REPORTER_ACCESS
    DEVELOPER_ACCESS = gitlab.DEVELOPER_ACCESS
    MASTER_ACCESS = gitlab.MASTER_ACCESS
    OWNER_ACCESS = gitlab.OWNER_ACCESS

    VISIBILITY_PRIVATE = gitlab.VISIBILITY_PRIVATE
    VISIBILITY_INTERNAL = gitlab.VISIBILITY_INTERNAL
    VISIBILITY_PUBLIC = gitlab.VISIBILITY_PUBLIC

    def transfer_project(self, id, **kwargs):
        """Transfers a project to this new groups.

        Args:
            id (int): ID of the project to transfer.

        Raises:
            GitlabConnectionError: If the server cannot be reached.
            GitlabTransferProjectError: If the server fails to perform the
                request.
        """
        url = '/groups/%d/projects/%d' % (self.id, id)
        r = self.gitlab._raw_post(url, None, **kwargs)
        raise_error_from_response(r, GitlabTransferProjectError, 201)


class GroupManager(BaseManager):
    obj_cls = Group

    def search(self, query, **kwargs):
        """Searches groups by name.

        Args:
            query (str): The search string
            all (bool): If True, return all the items, without pagination

        Returns:
            list(Group): a list of matching groups.
        """
        url = '/groups?search=' + query
        return self.gitlab._raw_list(url, self.obj_cls, **kwargs)


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
    managers = (
        ('members', 'TeamMemberManager', [('team_id', 'id')]),
        ('projects', 'TeamProjectManager', [('team_id', 'id')]),
    )


class TeamManager(BaseManager):
    obj_cls = Team

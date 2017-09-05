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

import six

from gitlab.base import *  # noqa
from gitlab import cli
from gitlab.exceptions import *  # noqa
from gitlab.mixins import *  # noqa
from gitlab import utils

VISIBILITY_PRIVATE = 'private'
VISIBILITY_INTERNAL = 'internal'
VISIBILITY_PUBLIC = 'public'

ACCESS_GUEST = 10
ACCESS_REPORTER = 20
ACCESS_DEVELOPER = 30
ACCESS_MASTER = 40
ACCESS_OWNER = 50


class SidekiqManager(RESTManager):
    """Manager for the Sidekiq methods.

    This manager doesn't actually manage objects but provides helper fonction
    for the sidekiq metrics API.
    """

    @cli.register_custom_action('SidekiqManager')
    @exc.on_http_error(exc.GitlabGetError)
    def queue_metrics(self, **kwargs):
        """Return the registred queues information.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabGetError: If the information couldn't be retrieved

        Returns:
            dict: Information about the Sidekiq queues
        """
        return self.gitlab.http_get('/sidekiq/queue_metrics', **kwargs)

    @cli.register_custom_action('SidekiqManager')
    @exc.on_http_error(exc.GitlabGetError)
    def process_metrics(self, **kwargs):
        """Return the registred sidekiq workers.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabGetError: If the information couldn't be retrieved

        Returns:
            dict: Information about the register Sidekiq worker
        """
        return self.gitlab.http_get('/sidekiq/process_metrics', **kwargs)

    @cli.register_custom_action('SidekiqManager')
    @exc.on_http_error(exc.GitlabGetError)
    def job_stats(self, **kwargs):
        """Return statistics about the jobs performed.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabGetError: If the information couldn't be retrieved

        Returns:
            dict: Statistics about the Sidekiq jobs performed
        """
        return self.gitlab.http_get('/sidekiq/job_stats', **kwargs)

    @cli.register_custom_action('SidekiqManager')
    @exc.on_http_error(exc.GitlabGetError)
    def compound_metrics(self, **kwargs):
        """Return all available metrics and statistics.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabGetError: If the information couldn't be retrieved

        Returns:
            dict: All available Sidekiq metrics and statistics
        """
        return self.gitlab.http_get('/sidekiq/compound_metrics', **kwargs)


class UserEmail(ObjectDeleteMixin, RESTObject):
    _short_print_attr = 'email'


class UserEmailManager(RetrieveMixin, CreateMixin, DeleteMixin, RESTManager):
    _path = '/users/%(user_id)s/emails'
    _obj_cls = UserEmail
    _from_parent_attrs = {'user_id': 'id'}
    _create_attrs = (('email', ), tuple())


class UserKey(ObjectDeleteMixin, RESTObject):
    pass


class UserKeyManager(GetFromListMixin, CreateMixin, DeleteMixin, RESTManager):
    _path = '/users/%(user_id)s/keys'
    _obj_cls = UserKey
    _from_parent_attrs = {'user_id': 'id'}
    _create_attrs = (('title', 'key'), tuple())


class UserProject(RESTObject):
    _constructor_types = {'owner': 'User', 'namespace': 'Group'}


class UserProjectManager(CreateMixin, RESTManager):
    _path = '/projects/user/%(user_id)s'
    _obj_cls = UserProject
    _from_parent_attrs = {'user_id': 'id'}
    _create_attrs = (
        ('name', ),
        ('default_branch', 'issues_enabled', 'wall_enabled',
         'merge_requests_enabled', 'wiki_enabled', 'snippets_enabled',
         'public', 'visibility', 'description', 'builds_enabled',
         'public_builds', 'import_url', 'only_allow_merge_if_build_succeeds')
    )


class User(SaveMixin, ObjectDeleteMixin, RESTObject):
    _short_print_attr = 'username'
    _managers = (
        ('emails', 'UserEmailManager'),
        ('keys', 'UserKeyManager'),
        ('projects', 'UserProjectManager'),
    )

    @cli.register_custom_action('User')
    @exc.on_http_error(exc.GitlabBlockError)
    def block(self, **kwargs):
        """Block the user.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabBlockError: If the user could not be blocked

        Returns:
            bool: Whether the user status has been changed
        """
        path = '/users/%s/block' % self.id
        server_data = self.manager.gitlab.http_post(path, **kwargs)
        if server_data is True:
            self._attrs['state'] = 'blocked'
        return server_data

    @cli.register_custom_action('User')
    @exc.on_http_error(exc.GitlabUnblockError)
    def unblock(self, **kwargs):
        """Unblock the user.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabUnblockError: If the user could not be unblocked

        Returns:
            bool: Whether the user status has been changed
        """
        path = '/users/%s/unblock' % self.id
        server_data = self.manager.gitlab.http_post(path, **kwargs)
        if server_data is True:
            self._attrs['state'] = 'active'
        return server_data


class UserManager(CRUDMixin, RESTManager):
    _path = '/users'
    _obj_cls = User

    _list_filters = ('active', 'blocked', 'username', 'extern_uid', 'provider',
                     'external', 'search')
    _create_attrs = (
        tuple(),
        ('email', 'username', 'name', 'password', 'reset_password', 'skype',
         'linkedin', 'twitter', 'projects_limit', 'extern_uid', 'provider',
         'bio', 'admin', 'can_create_group', 'website_url',
         'skip_confirmation', 'external', 'organization', 'location')
    )
    _update_attrs = (
        ('email', 'username', 'name'),
        ('password', 'skype', 'linkedin', 'twitter', 'projects_limit',
         'extern_uid', 'provider', 'bio', 'admin', 'can_create_group',
         'website_url', 'skip_confirmation', 'external', 'organization',
         'location')
    )

    def _sanitize_data(self, data, action):
        new_data = data.copy()
        if 'confirm' in data:
            new_data['confirm'] = str(new_data['confirm']).lower()
        return new_data


class CurrentUserEmail(ObjectDeleteMixin, RESTObject):
    _short_print_attr = 'email'


class CurrentUserEmailManager(RetrieveMixin, CreateMixin, DeleteMixin,
                              RESTManager):
    _path = '/user/emails'
    _obj_cls = CurrentUserEmail
    _create_attrs = (('email', ), tuple())


class CurrentUserKey(ObjectDeleteMixin, RESTObject):
    _short_print_attr = 'title'


class CurrentUserKeyManager(RetrieveMixin, CreateMixin, DeleteMixin,
                            RESTManager):
    _path = '/user/keys'
    _obj_cls = CurrentUserKey
    _create_attrs = (('title', 'key'), tuple())


class CurrentUser(RESTObject):
    _id_attr = None
    _short_print_attr = 'username'
    _managers = (
        ('emails', 'CurrentUserEmailManager'),
        ('keys', 'CurrentUserKeyManager'),
    )


class CurrentUserManager(GetWithoutIdMixin, RESTManager):
    _path = '/user'
    _obj_cls = CurrentUser


class ApplicationSettings(SaveMixin, RESTObject):
    _id_attr = None


class ApplicationSettingsManager(GetWithoutIdMixin, UpdateMixin, RESTManager):
    _path = '/application/settings'
    _obj_cls = ApplicationSettings
    _update_attrs = (
        tuple(),
        ('after_sign_out_path', 'container_registry_token_expire_delay',
         'default_branch_protection', 'default_project_visibility',
         'default_projects_limit', 'default_snippet_visibility',
         'domain_blacklist', 'domain_blacklist_enabled', 'domain_whitelist',
         'enabled_git_access_protocol', 'gravatar_enabled', 'home_page_url',
         'max_attachment_size', 'repository_storage',
         'restricted_signup_domains', 'restricted_visibility_levels',
         'session_expire_delay', 'sign_in_text', 'signin_enabled',
         'signup_enabled', 'twitter_sharing_enabled',
         'user_oauth_applications')
    )

    def _sanitize_data(self, data, action):
        new_data = data.copy()
        if 'domain_whitelist' in data and data['domain_whitelist'] is None:
            new_data.pop('domain_whitelist')
        return new_data


class BroadcastMessage(SaveMixin, ObjectDeleteMixin, RESTObject):
    pass


class BroadcastMessageManager(CRUDMixin, RESTManager):
    _path = '/broadcast_messages'
    _obj_cls = BroadcastMessage

    _create_attrs = (('message', ), ('starts_at', 'ends_at', 'color', 'font'))
    _update_attrs = (tuple(), ('message', 'starts_at', 'ends_at', 'color',
                               'font'))


class DeployKey(RESTObject):
    pass


class DeployKeyManager(GetFromListMixin, RESTManager):
    _path = '/deploy_keys'
    _obj_cls = DeployKey


class NotificationSettings(SaveMixin, RESTObject):
    _id_attr = None


class NotificationSettingsManager(GetWithoutIdMixin, UpdateMixin, RESTManager):
    _path = '/notification_settings'
    _obj_cls = NotificationSettings

    _update_attrs = (
        tuple(),
        ('level', 'notification_email', 'new_note', 'new_issue',
         'reopen_issue', 'close_issue', 'reassign_issue', 'new_merge_request',
         'reopen_merge_request', 'close_merge_request',
         'reassign_merge_request', 'merge_merge_request')
    )


class Dockerfile(RESTObject):
    _id_attr = 'name'


class DockerfileManager(RetrieveMixin, RESTManager):
    _path = '/templates/dockerfiles'
    _obj_cls = Dockerfile


class Gitignore(RESTObject):
    _id_attr = 'name'


class GitignoreManager(RetrieveMixin, RESTManager):
    _path = '/templates/gitignores'
    _obj_cls = Gitignore


class Gitlabciyml(RESTObject):
    _id_attr = 'name'


class GitlabciymlManager(RetrieveMixin, RESTManager):
    _path = '/templates/gitlab_ci_ymls'
    _obj_cls = Gitlabciyml


class GroupIssue(RESTObject):
    pass


class GroupIssueManager(GetFromListMixin, RESTManager):
    _path = '/groups/%(group_id)s/issues'
    _obj_cls = GroupIssue
    _from_parent_attrs = {'group_id': 'id'}
    _list_filters = ('state', 'labels', 'milestone', 'order_by', 'sort')


class GroupMember(SaveMixin, ObjectDeleteMixin, RESTObject):
    _short_print_attr = 'username'


class GroupMemberManager(GetFromListMixin, CreateMixin, UpdateMixin,
                         DeleteMixin, RESTManager):
    _path = '/groups/%(group_id)s/members'
    _obj_cls = GroupMember
    _from_parent_attrs = {'group_id': 'id'}
    _create_attrs = (('access_level', 'user_id'), ('expires_at', ))
    _update_attrs = (('access_level', ), ('expires_at', ))


class GroupNotificationSettings(NotificationSettings):
    pass


class GroupNotificationSettingsManager(NotificationSettingsManager):
    _path = '/groups/%(group_id)s/notification_settings'
    _obj_cls = GroupNotificationSettings
    _from_parent_attrs = {'group_id': 'id'}


class GroupAccessRequest(AccessRequestMixin, ObjectDeleteMixin, RESTObject):
    pass


class GroupAccessRequestManager(GetFromListMixin, CreateMixin, DeleteMixin,
                                RESTManager):
    _path = '/groups/%(group_id)s/access_requests'
    _obj_cls = GroupAccessRequest
    _from_parent_attrs = {'group_id': 'id'}


class Hook(ObjectDeleteMixin, RESTObject):
    _url = '/hooks'
    _short_print_attr = 'url'


class HookManager(NoUpdateMixin, RESTManager):
    _path = '/hooks'
    _obj_cls = Hook
    _create_attrs = (('url', ), tuple())


class Issue(RESTObject):
    _url = '/issues'
    _constructor_types = {'author': 'User',
                          'assignee': 'User',
                          'milestone': 'ProjectMilestone'}
    _short_print_attr = 'title'


class IssueManager(GetFromListMixin, RESTManager):
    _path = '/issues'
    _obj_cls = Issue
    _list_filters = ('state', 'labels', 'order_by', 'sort')


class License(RESTObject):
    _id_attr = 'key'


class LicenseManager(RetrieveMixin, RESTManager):
    _path = '/templates/licenses'
    _obj_cls = License
    _list_filters = ('popular', )
    _optional_get_attrs = ('project', 'fullname')


class Snippet(SaveMixin, ObjectDeleteMixin, RESTObject):
    _constructor_types = {'author': 'User'}
    _short_print_attr = 'title'

    @cli.register_custom_action('Snippet')
    @exc.on_http_error(exc.GitlabGetError)
    def content(self, streamed=False, action=None, chunk_size=1024, **kwargs):
        """Return the content of a snippet.

        Args:
            streamed (bool): If True the data will be processed by chunks of
                `chunk_size` and each chunk is passed to `action` for
                treatment.
            action (callable): Callable responsible of dealing with chunk of
                data
            chunk_size (int): Size of each chunk
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabGetError: If the content could not be retrieved

        Returns:
            str: The snippet content
        """
        path = '/snippets/%s/raw' % self.get_id()
        result = self.manager.gitlab.http_get(path, streamed=streamed,
                                              **kwargs)
        return utils.response_content(result, streamed, action, chunk_size)


class SnippetManager(CRUDMixin, RESTManager):
    _path = '/snippets'
    _obj_cls = Snippet
    _create_attrs = (('title', 'file_name', 'content'),
                     ('lifetime', 'visibility'))
    _update_attrs = (tuple(),
                     ('title', 'file_name', 'content', 'visibility'))

    @cli.register_custom_action('SnippetManager')
    def public(self, **kwargs):
        """List all the public snippets.

        Args:
            all (bool): If True the returned object will be a list
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabListError: If the list could not be retrieved

        Returns:
            RESTObjectList: A generator for the snippets list
        """
        return self.list(path='/snippets/public', **kwargs)


class Namespace(RESTObject):
    pass


class NamespaceManager(GetFromListMixin, RESTManager):
    _path = '/namespaces'
    _obj_cls = Namespace
    _list_filters = ('search', )


class ProjectBoardList(SaveMixin, ObjectDeleteMixin, RESTObject):
    _constructor_types = {'label': 'ProjectLabel'}


class ProjectBoardListManager(CRUDMixin, RESTManager):
    _path = '/projects/%(project_id)s/boards/%(board_id)s/lists'
    _obj_cls = ProjectBoardList
    _from_parent_attrs = {'project_id': 'project_id',
                          'board_id': 'id'}
    _create_attrs = (('label_id', ), tuple())
    _update_attrs = (('position', ), tuple())


class ProjectBoard(RESTObject):
    _constructor_types = {'labels': 'ProjectBoardList'}
    _managers = (('lists', 'ProjectBoardListManager'), )


class ProjectBoardManager(GetFromListMixin, RESTManager):
    _path = '/projects/%(project_id)s/boards'
    _obj_cls = ProjectBoard
    _from_parent_attrs = {'project_id': 'id'}


class ProjectBranch(ObjectDeleteMixin, RESTObject):
    _constructor_types = {'author': 'User', "committer": "User"}
    _id_attr = 'name'

    @cli.register_custom_action('ProjectBranch', tuple(),
                                ('developers_can_push',
                                 'developers_can_merge'))
    @exc.on_http_error(exc.GitlabProtectError)
    def protect(self, developers_can_push=False, developers_can_merge=False,
                **kwargs):
        """Protect the branch.

        Args:
            developers_can_push (bool): Set to True if developers are allowed
                                        to push to the branch
            developers_can_merge (bool): Set to True if developers are allowed
                                         to merge to the branch
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabProtectError: If the branch could not be protected
        """
        path = '%s/%s/protect' % (self.manager.path, self.get_id())
        post_data = {'developers_can_push': developers_can_push,
                     'developers_can_merge': developers_can_merge}
        self.manager.gitlab.http_put(path, post_data=post_data, **kwargs)
        self._attrs['protected'] = True

    @cli.register_custom_action('ProjectBranch')
    @exc.on_http_error(exc.GitlabProtectError)
    def unprotect(self, **kwargs):
        """Unprotect the branch.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabProtectError: If the branch could not be unprotected
        """
        path = '%s/%s/unprotect' % (self.manager.path, self.get_id())
        self.manager.gitlab.http_put(path, **kwargs)
        self._attrs['protected'] = False


class ProjectBranchManager(NoUpdateMixin, RESTManager):
    _path = '/projects/%(project_id)s/repository/branches'
    _obj_cls = ProjectBranch
    _from_parent_attrs = {'project_id': 'id'}
    _create_attrs = (('branch', 'ref'), tuple())


class ProjectJob(RESTObject):
    _constructor_types = {'user': 'User',
                          'commit': 'ProjectCommit',
                          'runner': 'Runner'}

    @cli.register_custom_action('ProjectJob')
    @exc.on_http_error(exc.GitlabJobCancelError)
    def cancel(self, **kwargs):
        """Cancel the job.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabJobCancelError: If the job could not be canceled
        """
        path = '%s/%s/cancel' % (self.manager.path, self.get_id())
        self.manager.gitlab.http_post(path)

    @cli.register_custom_action('ProjectJob')
    @exc.on_http_error(exc.GitlabJobRetryError)
    def retry(self, **kwargs):
        """Retry the job.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabJobRetryError: If the job could not be retried
        """
        path = '%s/%s/retry' % (self.manager.path, self.get_id())
        self.manager.gitlab.http_post(path)

    @cli.register_custom_action('ProjectJob')
    @exc.on_http_error(exc.GitlabJobPlayError)
    def play(self, **kwargs):
        """Trigger a job explicitly.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabJobPlayError: If the job could not be triggered
        """
        path = '%s/%s/play' % (self.manager.path, self.get_id())
        self.manager.gitlab.http_post(path)

    @cli.register_custom_action('ProjectJob')
    @exc.on_http_error(exc.GitlabJobEraseError)
    def erase(self, **kwargs):
        """Erase the job (remove job artifacts and trace).

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabJobEraseError: If the job could not be erased
        """
        path = '%s/%s/erase' % (self.manager.path, self.get_id())
        self.manager.gitlab.http_post(path)

    @cli.register_custom_action('ProjectJob')
    @exc.on_http_error(exc.GitlabCreateError)
    def keep_artifacts(self, **kwargs):
        """Prevent artifacts from being deleted when expiration is set.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabCreateError: If the request could not be performed
        """
        path = '%s/%s/artifacts/keep' % (self.manager.path, self.get_id())
        self.manager.gitlab.http_post(path)

    @cli.register_custom_action('ProjectJob')
    @exc.on_http_error(exc.GitlabGetError)
    def artifacts(self, streamed=False, action=None, chunk_size=1024,
                  **kwargs):
        """Get the job artifacts.

        Args:
            streamed (bool): If True the data will be processed by chunks of
                `chunk_size` and each chunk is passed to `action` for
                treatment
            action (callable): Callable responsible of dealing with chunk of
                data
            chunk_size (int): Size of each chunk
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabGetError: If the artifacts could not be retrieved

        Returns:
            str: The artifacts if `streamed` is False, None otherwise.
        """
        path = '%s/%s/artifacts' % (self.manager.path, self.get_id())
        result = self.manager.gitlab.get_http(path, streamed=streamed,
                                              **kwargs)
        return utils.response_content(result, streamed, action, chunk_size)

    @cli.register_custom_action('ProjectJob')
    @exc.on_http_error(exc.GitlabGetError)
    def trace(self, streamed=False, action=None, chunk_size=1024, **kwargs):
        """Get the job trace.

        Args:
            streamed (bool): If True the data will be processed by chunks of
                `chunk_size` and each chunk is passed to `action` for
                treatment
            action (callable): Callable responsible of dealing with chunk of
                data
            chunk_size (int): Size of each chunk
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabGetError: If the artifacts could not be retrieved

        Returns:
            str: The trace
        """
        path = '%s/%s/trace' % (self.manager.path, self.get_id())
        result = self.manager.gitlab.get_http(path, streamed=streamed,
                                              **kwargs)
        return utils.response_content(result, streamed, action, chunk_size)


class ProjectJobManager(RetrieveMixin, RESTManager):
    _path = '/projects/%(project_id)s/jobs'
    _obj_cls = ProjectJob
    _from_parent_attrs = {'project_id': 'id'}


class ProjectCommitStatus(RESTObject):
    pass


class ProjectCommitStatusManager(GetFromListMixin, CreateMixin, RESTManager):
    _path = ('/projects/%(project_id)s/repository/commits/%(commit_id)s'
             '/statuses')
    _obj_cls = ProjectCommitStatus
    _from_parent_attrs = {'project_id': 'project_id', 'commit_id': 'id'}
    _create_attrs = (('state', 'sha'),
                     ('description', 'name', 'context', 'ref', 'target_url',
                      'coverage'))

    def create(self, data, **kwargs):
        """Create a new object.

        Args:
            data (dict): Parameters to send to the server to create the
                         resource
            **kwargs: Extra data to send to the Gitlab server (e.g. sudo or
                      'ref_name', 'stage', 'name', 'all'.

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabCreateError: If the server cannot perform the request

        Returns:
            RESTObject: A new instance of the manage object class build with
                        the data sent by the server
        """
        path = '/projects/%(project_id)s/statuses/%(commit_id)s'
        computed_path = self._compute_path(path)
        return CreateMixin.create(self, data, path=computed_path, **kwargs)


class ProjectCommitComment(RESTObject):
    _id_attr = None


class ProjectCommitCommentManager(ListMixin, CreateMixin, RESTManager):
    _path = ('/projects/%(project_id)s/repository/commits/%(commit_id)s'
             '/comments')
    _obj_cls = ProjectCommitComment
    _from_parent_attrs = {'project_id': 'project_id', 'commit_id': 'id'}
    _create_attrs = (('note', ), ('path', 'line', 'line_type'))


class ProjectCommit(RESTObject):
    _short_print_attr = 'title'
    _managers = (
        ('comments', 'ProjectCommitCommentManager'),
        ('statuses', 'ProjectCommitStatusManager'),
    )

    @cli.register_custom_action('ProjectCommit')
    @exc.on_http_error(exc.GitlabGetError)
    def diff(self, **kwargs):
        """Generate the commit diff.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabGetError: If the diff could not be retrieved

        Returns:
            list: The changes done in this commit
        """
        path = '%s/%s/diff' % (self.manager.path, self.get_id())
        return self.manager.gitlab.http_get(path, **kwargs)

    @cli.register_custom_action('ProjectCommit', ('branch',))
    @exc.on_http_error(exc.GitlabCherryPickError)
    def cherry_pick(self, branch, **kwargs):
        """Cherry-pick a commit into a branch.

        Args:
            branch (str): Name of target branch
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabCherryPickError: If the cherry-pick could not be performed
        """
        path = '%s/%s/cherry_pick' % (self.manager.path, self.get_id())
        post_data = {'branch': branch}
        self.manager.gitlab.http_post(path, post_data=post_data, **kwargs)


class ProjectCommitManager(RetrieveMixin, CreateMixin, RESTManager):
    _path = '/projects/%(project_id)s/repository/commits'
    _obj_cls = ProjectCommit
    _from_parent_attrs = {'project_id': 'id'}
    _create_attrs = (('branch', 'commit_message', 'actions'),
                     ('author_email', 'author_name'))


class ProjectEnvironment(SaveMixin, ObjectDeleteMixin, RESTObject):
    pass


class ProjectEnvironmentManager(GetFromListMixin, CreateMixin, UpdateMixin,
                                DeleteMixin, RESTManager):
    _path = '/projects/%(project_id)s/environments'
    _obj_cls = ProjectEnvironment
    _from_parent_attrs = {'project_id': 'id'}
    _create_attrs = (('name', ), ('external_url', ))
    _update_attrs = (tuple(), ('name', 'external_url'))


class ProjectKey(ObjectDeleteMixin, RESTObject):
    pass


class ProjectKeyManager(NoUpdateMixin, RESTManager):
    _path = '/projects/%(project_id)s/deploy_keys'
    _obj_cls = ProjectKey
    _from_parent_attrs = {'project_id': 'id'}
    _create_attrs = (('title', 'key'), tuple())

    @cli.register_custom_action('ProjectKeyManager', ('key_id',))
    @exc.on_http_error(exc.GitlabProjectDeployKeyError)
    def enable(self, key_id, **kwargs):
        """Enable a deploy key for a project.

        Args:
            key_id (int): The ID of the key to enable
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabProjectDeployKeyError: If the key could not be enabled
        """
        path = '%s/%s/enable' % (self.path, key_id)
        self.gitlab.http_post(path, **kwargs)


class ProjectEvent(RESTObject):
    _id_attr = None
    _short_print_attr = 'target_title'


class ProjectEventManager(ListMixin, RESTManager):
    _path = '/projects/%(project_id)s/events'
    _obj_cls = ProjectEvent
    _from_parent_attrs = {'project_id': 'id'}


class ProjectFork(RESTObject):
    pass


class ProjectForkManager(CreateMixin, RESTManager):
    _path = '/projects/%(project_id)s/fork'
    _obj_cls = ProjectFork
    _from_parent_attrs = {'project_id': 'id'}
    _create_attrs = (tuple(), ('namespace', ))


class ProjectHook(SaveMixin, ObjectDeleteMixin, RESTObject):
    _short_print_attr = 'url'


class ProjectHookManager(CRUDMixin, RESTManager):
    _path = '/projects/%(project_id)s/hooks'
    _obj_cls = ProjectHook
    _from_parent_attrs = {'project_id': 'id'}
    _create_attrs = (
        ('url', ),
        ('push_events', 'issues_events', 'note_events',
         'merge_requests_events', 'tag_push_events', 'build_events',
         'enable_ssl_verification', 'token', 'pipeline_events')
    )
    _update_attrs = (
        ('url', ),
        ('push_events', 'issues_events', 'note_events',
         'merge_requests_events', 'tag_push_events', 'build_events',
         'enable_ssl_verification', 'token', 'pipeline_events')
    )


class ProjectIssueNote(SaveMixin, ObjectDeleteMixin, RESTObject):
    _constructor_types = {'author': 'User'}


class ProjectIssueNoteManager(CRUDMixin, RESTManager):
    _path = '/projects/%(project_id)s/issues/%(issue_iid)s/notes'
    _obj_cls = ProjectIssueNote
    _from_parent_attrs = {'project_id': 'project_id', 'issue_iid': 'iid'}
    _create_attrs = (('body', ), ('created_at', ))
    _update_attrs = (('body', ), tuple())


class ProjectIssue(SubscribableMixin, TodoMixin, TimeTrackingMixin, SaveMixin,
                   ObjectDeleteMixin, RESTObject):
    _constructor_types = {'author': 'User', 'assignee': 'User', 'milestone':
                          'ProjectMilestone'}
    _short_print_attr = 'title'
    _id_attr = 'iid'
    _managers = (('notes', 'ProjectIssueNoteManager'), )

    @cli.register_custom_action('ProjectIssue', ('to_project_id',))
    @exc.on_http_error(exc.GitlabUpdateError)
    def move(self, to_project_id, **kwargs):
        """Move the issue to another project.

        Args:
            to_project_id(int): ID of the target project
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabUpdateError: If the issue could not be moved
        """
        path = '%s/%s/move' % (self.manager.path, self.get_id())
        data = {'to_project_id': to_project_id}
        server_data = self.manager.gitlab.http_post(path, post_data=data,
                                                    **kwargs)
        self._update_attrs(server_data)


class ProjectIssueManager(CRUDMixin, RESTManager):
    _path = '/projects/%(project_id)s/issues/'
    _obj_cls = ProjectIssue
    _from_parent_attrs = {'project_id': 'id'}
    _list_filters = ('state', 'labels', 'milestone', 'order_by', 'sort')
    _create_attrs = (('title', ),
                     ('description', 'assignee_id', 'milestone_id', 'labels',
                      'created_at', 'due_date'))
    _update_attrs = (tuple(), ('title', 'description', 'assignee_id',
                               'milestone_id', 'labels', 'created_at',
                               'updated_at', 'state_event', 'due_date'))


class ProjectMember(SaveMixin, ObjectDeleteMixin, RESTObject):
    _short_print_attr = 'username'


class ProjectMemberManager(CRUDMixin, RESTManager):
    _path = '/projects/%(project_id)s/members'
    _obj_cls = ProjectMember
    _from_parent_attrs = {'project_id': 'id'}
    _create_attrs = (('access_level', 'user_id'), ('expires_at', ))
    _update_attrs = (('access_level', ), ('expires_at', ))


class ProjectNote(RESTObject):
    _constructor_types = {'author': 'User'}


class ProjectNoteManager(RetrieveMixin, RESTManager):
    _path = '/projects/%(project_id)s/notes'
    _obj_cls = ProjectNote
    _from_parent_attrs = {'project_id': 'id'}
    _create_attrs = (('body', ), tuple())


class ProjectNotificationSettings(NotificationSettings):
    pass


class ProjectNotificationSettingsManager(NotificationSettingsManager):
    _path = '/projects/%(project_id)s/notification_settings'
    _obj_cls = ProjectNotificationSettings
    _from_parent_attrs = {'project_id': 'id'}


class ProjectTag(ObjectDeleteMixin, RESTObject):
    _constructor_types = {'release': 'ProjectTagRelease',
                          'commit': 'ProjectCommit'}
    _id_attr = 'name'
    _short_print_attr = 'name'

    @cli.register_custom_action('ProjectTag', ('description', ))
    def set_release_description(self, description, **kwargs):
        """Set the release notes on the tag.

        If the release doesn't exist yet, it will be created. If it already
        exists, its description will be updated.

        Args:
            description (str): Description of the release.
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabCreateError: If the server fails to create the release
            GitlabUpdateError: If the server fails to update the release
        """
        path = '%s/%s/release' % (self.manager.path, self.get_id())
        data = {'description': description}
        if self.release is None:
            try:
                server_data = self.manager.gitlab.http_post(path,
                                                            post_data=data,
                                                            **kwargs)
            except exc.GitlabHttpError as e:
                raise exc.GitlabCreateError(e.response_code, e.error_message)
        else:
            try:
                server_data = self.manager.gitlab.http_put(path,
                                                           post_data=data,
                                                           **kwargs)
            except exc.GitlabHttpError as e:
                raise exc.GitlabUpdateError(e.response_code, e.error_message)
        self.release = server_data


class ProjectTagManager(GetFromListMixin, CreateMixin, DeleteMixin,
                        RESTManager):
    _path = '/projects/%(project_id)s/repository/tags'
    _obj_cls = ProjectTag
    _from_parent_attrs = {'project_id': 'id'}
    _create_attrs = (('tag_name', 'ref'), ('message',))


class ProjectMergeRequestDiff(RESTObject):
    pass


class ProjectMergeRequestDiffManager(RetrieveMixin, RESTManager):
    _path = '/projects/%(project_id)s/merge_requests/%(mr_iid)s/versions'
    _obj_cls = ProjectMergeRequestDiff
    _from_parent_attrs = {'project_id': 'project_id', 'mr_iid': 'iid'}


class ProjectMergeRequestNote(SaveMixin, ObjectDeleteMixin, RESTObject):
    _constructor_types = {'author': 'User'}


class ProjectMergeRequestNoteManager(CRUDMixin, RESTManager):
    _path = '/projects/%(project_id)s/merge_requests/%(mr_iid)s/notes'
    _obj_cls = ProjectMergeRequestNote
    _from_parent_attrs = {'project_id': 'project_id', 'mr_iid': 'iid'}
    _create_attrs = (('body', ), tuple())
    _update_attrs = (('body', ), tuple())


class ProjectMergeRequest(SubscribableMixin, TodoMixin, TimeTrackingMixin,
                          SaveMixin, ObjectDeleteMixin, RESTObject):
    _constructor_types = {'author': 'User', 'assignee': 'User'}
    _id_attr = 'iid'

    _managers = (
        ('notes', 'ProjectMergeRequestNoteManager'),
        ('diffs', 'ProjectMergeRequestDiffManager')
    )

    @cli.register_custom_action('ProjectMergeRequest')
    @exc.on_http_error(exc.GitlabMROnBuildSuccessError)
    def cancel_merge_when_pipeline_succeeds(self, **kwargs):
        """Cancel merge when the pipeline succeeds.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabMROnBuildSuccessError: If the server could not handle the
                request
        """

        path = ('%s/%s/cancel_merge_when_pipeline_succeeds' %
                (self.manager.path, self.get_id()))
        server_data = self.manager.gitlab.http_put(path, **kwargs)
        self._update_attrs(server_data)

    @cli.register_custom_action('ProjectMergeRequest')
    @exc.on_http_error(exc.GitlabListError)
    def closes_issues(self, **kwargs):
        """List issues that will close on merge."

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabListError: If the list could not be retrieved

        Returns:
            RESTObjectList: List of issues
        """
        path = '%s/%s/closes_issues' % (self.manager.path, self.get_id())
        data_list = self.manager.gitlab.http_list(path, as_list=False,
                                                  **kwargs)
        manager = ProjectIssueManager(self.manager.gitlab,
                                      parent=self.manager._parent)
        return RESTObjectList(manager, ProjectIssue, data_list)

    @cli.register_custom_action('ProjectMergeRequest')
    @exc.on_http_error(exc.GitlabListError)
    def commits(self, **kwargs):
        """List the merge request commits.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabListError: If the list could not be retrieved

        Returns:
            RESTObjectList: The list of commits
        """

        path = '%s/%s/commits' % (self.manager.path, self.get_id())
        data_list = self.manager.gitlab.http_list(path, as_list=False,
                                                  **kwargs)
        manager = ProjectCommitManager(self.manager.gitlab,
                                       parent=self.manager._parent)
        return RESTObjectList(manager, ProjectCommit, data_list)

    @cli.register_custom_action('ProjectMergeRequest')
    @exc.on_http_error(exc.GitlabListError)
    def changes(self, **kwargs):
        """List the merge request changes.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabListError: If the list could not be retrieved

        Returns:
            RESTObjectList: List of changes
        """
        path = '%s/%s/changes' % (self.manager.path, self.get_id())
        return self.manager.gitlab.http_get(path, **kwargs)

    @cli.register_custom_action('ProjectMergeRequest', tuple(),
                                ('merge_commit_message',
                                 'should_remove_source_branch',
                                 'merge_when_pipeline_succeeds'))
    @exc.on_http_error(exc.GitlabMRClosedError)
    def merge(self, merge_commit_message=None,
              should_remove_source_branch=False,
              merge_when_pipeline_succeeds=False,
              **kwargs):
        """Accept the merge request.

        Args:
            merge_commit_message (bool): Commit message
            should_remove_source_branch (bool): If True, removes the source
                                                branch
            merge_when_pipeline_succeeds (bool): Wait for the build to succeed,
                                                 then merge
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabMRClosedError: If the merge failed
        """
        path = '%s/%s/merge' % (self.manager.path, self.get_id())
        data = {}
        if merge_commit_message:
            data['merge_commit_message'] = merge_commit_message
        if should_remove_source_branch:
            data['should_remove_source_branch'] = True
        if merge_when_pipeline_succeeds:
            data['merge_when_pipeline_succeeds'] = True

        server_data = self.manager.gitlab.http_put(path, post_data=data,
                                                   **kwargs)
        self._update_attrs(server_data)


class ProjectMergeRequestManager(CRUDMixin, RESTManager):
    _path = '/projects/%(project_id)s/merge_requests'
    _obj_cls = ProjectMergeRequest
    _from_parent_attrs = {'project_id': 'id'}
    _create_attrs = (
        ('source_branch', 'target_branch', 'title'),
        ('assignee_id', 'description', 'target_project_id', 'labels',
         'milestone_id', 'remove_source_branch')
    )
    _update_attrs = (tuple(), ('target_branch', 'assignee_id', 'title',
                               'description', 'state_event', 'labels',
                               'milestone_id'))
    _list_filters = ('iids', 'state', 'order_by', 'sort')


class ProjectMilestone(SaveMixin, ObjectDeleteMixin, RESTObject):
    _short_print_attr = 'title'

    @cli.register_custom_action('ProjectMilestone')
    @exc.on_http_error(exc.GitlabListError)
    def issues(self, **kwargs):
        """List issues related to this milestone.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabListError: If the list could not be retrieved

        Returns:
            RESTObjectList: The list of issues
        """

        path = '%s/%s/issues' % (self.manager.path, self.get_id())
        data_list = self.manager.gitlab.http_list(path, as_list=False,
                                                  **kwargs)
        manager = ProjectCommitManager(self.manager.gitlab,
                                       parent=self.manager._parent)
        # FIXME(gpocentek): the computed manager path is not correct
        return RESTObjectList(manager, ProjectIssue, data_list)

    @cli.register_custom_action('ProjectMilestone')
    @exc.on_http_error(exc.GitlabListError)
    def merge_requests(self, **kwargs):
        """List the merge requests related to this milestone.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabListError: If the list could not be retrieved

        Returns:
            RESTObjectList: The list of merge requests
        """
        path = '%s/%s/merge_requests' % (self.manager.path, self.get_id())
        data_list = self.manager.gitlab.http_list(path, as_list=False,
                                                  **kwargs)
        manager = ProjectCommitManager(self.manager.gitlab,
                                       parent=self.manager._parent)
        # FIXME(gpocentek): the computed manager path is not correct
        return RESTObjectList(manager, ProjectMergeRequest, data_list)


class ProjectMilestoneManager(CRUDMixin, RESTManager):
    _path = '/projects/%(project_id)s/milestones'
    _obj_cls = ProjectMilestone
    _from_parent_attrs = {'project_id': 'id'}
    _create_attrs = (('title', ), ('description', 'due_date', 'start_date',
                                   'state_event'))
    _update_attrs = (tuple(), ('title', 'description', 'due_date',
                               'start_date', 'state_event'))
    _list_filters = ('iids', 'state')


class ProjectLabel(SubscribableMixin, SaveMixin, ObjectDeleteMixin,
                   RESTObject):
    _id_attr = 'name'

    # Update without ID, but we need an ID to get from list.
    @exc.on_http_error(exc.GitlabUpdateError)
    def save(self, **kwargs):
        """Saves the changes made to the object to the server.

        The object is updated to match what the server returns.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct.
            GitlabUpdateError: If the server cannot perform the request.
        """
        updated_data = self._get_updated_data()

        # call the manager
        server_data = self.manager.update(None, updated_data, **kwargs)
        self._update_attrs(server_data)


class ProjectLabelManager(GetFromListMixin, CreateMixin, UpdateMixin,
                          DeleteMixin, RESTManager):
    _path = '/projects/%(project_id)s/labels'
    _obj_cls = ProjectLabel
    _from_parent_attrs = {'project_id': 'id'}
    _create_attrs = (('name', 'color'), ('description', 'priority'))
    _update_attrs = (('name', ),
                     ('new_name', 'color', 'description', 'priority'))

    # Delete without ID.
    @exc.on_http_error(exc.GitlabDeleteError)
    def delete(self, name, **kwargs):
        """Delete a Label on the server.

        Args:
            name: The name of the label
            **kwargs: Extra options to send to the Gitlab server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct.
            GitlabDeleteError: If the server cannot perform the request.
        """
        self.gitlab.http_delete(self.path, query_data={'name': name}, **kwargs)


class ProjectFile(SaveMixin, ObjectDeleteMixin, RESTObject):
    _id_attr = 'file_path'
    _short_print_attr = 'file_path'

    def decode(self):
        """Returns the decoded content of the file.

        Returns:
            (str): the decoded content.
        """
        return base64.b64decode(self.content)

    def save(self, branch, commit_message, **kwargs):
        """Save the changes made to the file to the server.

        The object is updated to match what the server returns.

        Args:
            branch (str): Branch in which the file will be updated
            commit_message (str): Message to send with the commit
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabUpdateError: If the server cannot perform the request
        """
        self.branch = branch
        self.commit_message = commit_message
        super(ProjectFile, self).save(**kwargs)

    def delete(self, branch, commit_message, **kwargs):
        """Delete the file from the server.

        Args:
            branch (str): Branch from which the file will be removed
            commit_message (str): Commit message for the deletion
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabDeleteError: If the server cannot perform the request
        """
        self.manager.delete(self.get_id(), branch, commit_message, **kwargs)


class ProjectFileManager(GetMixin, CreateMixin, UpdateMixin, DeleteMixin,
                         RESTManager):
    _path = '/projects/%(project_id)s/repository/files'
    _obj_cls = ProjectFile
    _from_parent_attrs = {'project_id': 'id'}
    _create_attrs = (('file_path', 'branch', 'content', 'commit_message'),
                     ('encoding', 'author_email', 'author_name'))
    _update_attrs = (('file_path', 'branch', 'content', 'commit_message'),
                     ('encoding', 'author_email', 'author_name'))

    @cli.register_custom_action('ProjectFileManager', ('file_path', 'ref'))
    def get(self, file_path, ref, **kwargs):
        """Retrieve a single file.

        Args:
            file_path (str): Path of the file to retrieve
            ref (str): Name of the branch, tag or commit
            **kwargs: Extra options to send to the Gitlab server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabGetError: If the file could not be retrieved

        Returns:
            object: The generated RESTObject
        """
        file_path = file_path.replace('/', '%2F')
        return GetMixin.get(self, file_path, ref=ref, **kwargs)

    @cli.register_custom_action('ProjectFileManager',
                                ('file_path', 'branch', 'content',
                                 'commit_message'),
                                ('encoding', 'author_email', 'author_name'))
    @exc.on_http_error(exc.GitlabCreateError)
    def create(self, data, **kwargs):
        """Create a new object.

        Args:
            data (dict): parameters to send to the server to create the
                         resource
            **kwargs: Extra options to send to the Gitlab server (e.g. sudo)

        Returns:
            RESTObject: a new instance of the managed object class built with
                the data sent by the server

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabCreateError: If the server cannot perform the request
        """

        self._check_missing_create_attrs(data)
        file_path = data.pop('file_path')
        path = '%s/%s' % (self.path, file_path)
        server_data = self.gitlab.http_post(path, post_data=data, **kwargs)
        return self._obj_cls(self, server_data)

    @cli.register_custom_action('ProjectFileManager', ('file_path', 'branch',
                                                       'commit_message'))
    @exc.on_http_error(exc.GitlabDeleteError)
    def delete(self, file_path, branch, commit_message, **kwargs):
        """Delete a file on the server.

        Args:
            file_path (str): Path of the file to remove
            branch (str): Branch from which the file will be removed
            commit_message (str): Commit message for the deletion
            **kwargs: Extra options to send to the Gitlab server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabDeleteError: If the server cannot perform the request
        """
        path = '%s/%s' % (self.path, file_path.replace('/', '%2F'))
        data = {'branch': branch, 'commit_message': commit_message}
        self.gitlab.http_delete(path, query_data=data, **kwargs)

    @cli.register_custom_action('ProjectFileManager', ('file_path', 'ref'))
    @exc.on_http_error(exc.GitlabGetError)
    def raw(self, file_path, ref, streamed=False, action=None, chunk_size=1024,
            **kwargs):
        """Return the content of a file for a commit.

        Args:
            ref (str): ID of the commit
            filepath (str): Path of the file to return
            streamed (bool): If True the data will be processed by chunks of
                `chunk_size` and each chunk is passed to `action` for
                treatment
            action (callable): Callable responsible of dealing with chunk of
                data
            chunk_size (int): Size of each chunk
            **kwargs: Extra options to send to the Gitlab server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabGetError: If the file could not be retrieved

        Returns:
            str: The file content
        """
        file_path = file_path.replace('/', '%2F').replace('.', '%2E')
        path = '%s/%s/raw' % (self.path, file_path)
        query_data = {'ref': ref}
        result = self.gitlab.http_get(path, query_data=query_data,
                                      streamed=streamed, **kwargs)
        return utils.response_content(result, streamed, action, chunk_size)


class ProjectPipeline(RESTObject):
    @cli.register_custom_action('ProjectPipeline')
    @exc.on_http_error(exc.GitlabPipelineCancelError)
    def cancel(self, **kwargs):
        """Cancel the job.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabPipelineCancelError: If the request failed
        """
        path = '%s/%s/cancel' % (self.manager.path, self.get_id())
        self.manager.gitlab.http_post(path)

    @cli.register_custom_action('ProjectPipeline')
    @exc.on_http_error(exc.GitlabPipelineRetryError)
    def retry(self, **kwargs):
        """Retry the job.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabPipelineRetryError: If the request failed
        """
        path = '%s/%s/retry' % (self.manager.path, self.get_id())
        self.manager.gitlab.http_post(path)


class ProjectPipelineManager(RetrieveMixin, CreateMixin, RESTManager):
    _path = '/projects/%(project_id)s/pipelines'
    _obj_cls = ProjectPipeline
    _from_parent_attrs = {'project_id': 'id'}
    _create_attrs = (('ref', ), tuple())

    def create(self, data, **kwargs):
        """Creates a new object.

        Args:
            data (dict): Parameters to send to the server to create the
                         resource
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabCreateError: If the server cannot perform the request

        Returns:
            RESTObject: A new instance of the managed object class build with
                the data sent by the server
        """
        path = self.path[:-1]  # drop the 's'
        return CreateMixin.create(self, data, path=path, **kwargs)


class ProjectSnippetNote(RESTObject):
    _constructor_types = {'author': 'User'}


class ProjectSnippetNoteManager(RetrieveMixin, CreateMixin, RESTManager):
    _path = '/projects/%(project_id)s/snippets/%(snippet_id)s/notes'
    _obj_cls = ProjectSnippetNote
    _from_parent_attrs = {'project_id': 'project_id',
                          'snippet_id': 'id'}
    _create_attrs = (('body', ), tuple())


class ProjectSnippet(SaveMixin, ObjectDeleteMixin, RESTObject):
    _url = '/projects/%(project_id)s/snippets'
    _constructor_types = {'author': 'User'}
    _short_print_attr = 'title'
    _managers = (('notes', 'ProjectSnippetNoteManager'), )

    @cli.register_custom_action('ProjectSnippet')
    @exc.on_http_error(exc.GitlabGetError)
    def content(self, streamed=False, action=None, chunk_size=1024, **kwargs):
        """Return the content of a snippet.

        Args:
            streamed (bool): If True the data will be processed by chunks of
                `chunk_size` and each chunk is passed to `action` for
                treatment.
            action (callable): Callable responsible of dealing with chunk of
                data
            chunk_size (int): Size of each chunk
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabGetError: If the content could not be retrieved

        Returns:
            str: The snippet content
        """
        path = "%s/%s/raw" % (self.manager.path, self.get_id())
        result = self.manager.gitlab.http_get(path, streamed=streamed,
                                              **kwargs)
        return utils.response_content(result, streamed, action, chunk_size)


class ProjectSnippetManager(CRUDMixin, RESTManager):
    _path = '/projects/%(project_id)s/snippets'
    _obj_cls = ProjectSnippet
    _from_parent_attrs = {'project_id': 'id'}
    _create_attrs = (('title', 'file_name', 'code'),
                     ('lifetime', 'visibility'))
    _update_attrs = (tuple(), ('title', 'file_name', 'code', 'visibility'))


class ProjectTrigger(SaveMixin, ObjectDeleteMixin, RESTObject):
    @cli.register_custom_action('ProjectTrigger')
    def take_ownership(self, **kwargs):
        """Update the owner of a trigger."""
        path = '%s/%s/take_ownership' % (self.manager.path, self.get_id())
        server_data = self.manager.gitlab.http_post(path, **kwargs)
        self._update_attrs(server_data)


class ProjectTriggerManager(CRUDMixin, RESTManager):
    _path = '/projects/%(project_id)s/triggers'
    _obj_cls = ProjectTrigger
    _from_parent_attrs = {'project_id': 'id'}
    _create_attrs = (('description', ), tuple())
    _update_attrs = (('description', ), tuple())


class ProjectVariable(SaveMixin, ObjectDeleteMixin, RESTObject):
    _id_attr = 'key'


class ProjectVariableManager(CRUDMixin, RESTManager):
    _path = '/projects/%(project_id)s/variables'
    _obj_cls = ProjectVariable
    _from_parent_attrs = {'project_id': 'id'}
    _create_attrs = (('key', 'value'), tuple())
    _update_attrs = (('key', 'value'), tuple())


class ProjectService(SaveMixin, ObjectDeleteMixin, RESTObject):
    pass


class ProjectServiceManager(GetMixin, UpdateMixin, DeleteMixin, RESTManager):
    _path = '/projects/%(project_id)s/services'
    _from_parent_attrs = {'project_id': 'id'}
    _obj_cls = ProjectService

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
        'jira': (('url', 'project_key'),
                 ('new_issue_url', 'project_url', 'issues_url', 'api_url',
                  'description', 'username', 'password',
                  'jira_issue_transition_id')),
        'pivotaltracker': (('token', ), tuple()),
        'pushover': (('api_key', 'user_key', 'priority'), ('device', 'sound')),
        'redmine': (('new_issue_url', 'project_url', 'issues_url'),
                    ('description', )),
        'slack': (('webhook', ), ('username', 'channel')),
        'teamcity': (('teamcity_url', 'build_type', 'username', 'password'),
                     tuple())
    }

    def get(self, id, **kwargs):
        """Retrieve a single object.

        Args:
            id (int or str): ID of the object to retrieve
            lazy (bool): If True, don't request the server, but create a
                         shallow object giving access to the managers. This is
                         useful if you want to avoid useless calls to the API.
            **kwargs: Extra options to send to the Gitlab server (e.g. sudo)

        Returns:
            object: The generated RESTObject.

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabGetError: If the server cannot perform the request
        """
        obj = super(ProjectServiceManager, self).get(id, **kwargs)
        obj.id = id
        return obj

    def update(self, id=None, new_data={}, **kwargs):
        """Update an object on the server.

        Args:
            id: ID of the object to update (can be None if not required)
            new_data: the update data for the object
            **kwargs: Extra options to send to the Gitlab server (e.g. sudo)

        Returns:
            dict: The new object data (*not* a RESTObject)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabUpdateError: If the server cannot perform the request
        """
        super(ProjectServiceManager, self).update(id, new_data, **kwargs)
        self.id = id

    @cli.register_custom_action('ProjectServiceManager')
    def available(self, **kwargs):
        """List the services known by python-gitlab.

        Returns:
            list (str): The list of service code names.
        """
        return list(self._service_attrs.keys())


class ProjectAccessRequest(AccessRequestMixin, ObjectDeleteMixin, RESTObject):
    pass


class ProjectAccessRequestManager(GetFromListMixin, CreateMixin, DeleteMixin,
                                  RESTManager):
    _path = '/projects/%(project_id)s/access_requests'
    _obj_cls = ProjectAccessRequest
    _from_parent_attrs = {'project_id': 'id'}


class ProjectDeployment(RESTObject):
    pass


class ProjectDeploymentManager(RetrieveMixin, RESTManager):
    _path = '/projects/%(project_id)s/deployments'
    _obj_cls = ProjectDeployment
    _from_parent_attrs = {'project_id': 'id'}


class ProjectProtectedBranch(ObjectDeleteMixin, RESTObject):
    _id_attr = 'name'


class ProjectProtectedBranchManager(NoUpdateMixin, RESTManager):
    _path = '/projects/%(project_id)s/protected_branches'
    _obj_cls = ProjectProtectedBranch
    _from_parent_attrs = {'project_id': 'id'}
    _create_attrs = (('name', ), ('push_access_level', 'merge_access_level'))


class ProjectRunner(ObjectDeleteMixin, RESTObject):
    pass


class ProjectRunnerManager(NoUpdateMixin, RESTManager):
    _path = '/projects/%(project_id)s/runners'
    _obj_cls = ProjectRunner
    _from_parent_attrs = {'project_id': 'id'}
    _create_attrs = (('runner_id', ), tuple())


class Project(SaveMixin, ObjectDeleteMixin, RESTObject):
    _constructor_types = {'owner': 'User', 'namespace': 'Group'}
    _short_print_attr = 'path'
    _managers = (
        ('accessrequests', 'ProjectAccessRequestManager'),
        ('boards', 'ProjectBoardManager'),
        ('branches', 'ProjectBranchManager'),
        ('jobs', 'ProjectJobManager'),
        ('commits', 'ProjectCommitManager'),
        ('deployments', 'ProjectDeploymentManager'),
        ('environments', 'ProjectEnvironmentManager'),
        ('events', 'ProjectEventManager'),
        ('files', 'ProjectFileManager'),
        ('forks', 'ProjectForkManager'),
        ('hooks', 'ProjectHookManager'),
        ('keys', 'ProjectKeyManager'),
        ('issues', 'ProjectIssueManager'),
        ('labels', 'ProjectLabelManager'),
        ('members', 'ProjectMemberManager'),
        ('mergerequests', 'ProjectMergeRequestManager'),
        ('milestones', 'ProjectMilestoneManager'),
        ('notes', 'ProjectNoteManager'),
        ('notificationsettings', 'ProjectNotificationSettingsManager'),
        ('pipelines', 'ProjectPipelineManager'),
        ('protectedbranches', 'ProjectProtectedBranchManager'),
        ('runners', 'ProjectRunnerManager'),
        ('services', 'ProjectServiceManager'),
        ('snippets', 'ProjectSnippetManager'),
        ('tags', 'ProjectTagManager'),
        ('triggers', 'ProjectTriggerManager'),
        ('variables', 'ProjectVariableManager'),
    )

    @cli.register_custom_action('Project', tuple(), ('path', 'ref'))
    @exc.on_http_error(exc.GitlabGetError)
    def repository_tree(self, path='', ref='', **kwargs):
        """Return a list of files in the repository.

        Args:
            path (str): Path of the top folder (/ by default)
            ref (str): Reference to a commit or branch
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabGetError: If the server failed to perform the request

        Returns:
            list: The representation of the tree
        """
        gl_path = '/projects/%s/repository/tree' % self.get_id()
        query_data = {}
        if path:
            query_data['path'] = path
        if ref:
            query_data['ref'] = ref
        return self.manager.gitlab.http_get(gl_path, query_data=query_data,
                                            **kwargs)

    @cli.register_custom_action('Project', ('sha', ))
    @exc.on_http_error(exc.GitlabGetError)
    def repository_blob(self, sha, **kwargs):
        """Return a blob by blob SHA.

        Args:
            sha(str): ID of the blob
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabGetError: If the server failed to perform the request

        Returns:
            str: The blob metadata
        """

        path = '/projects/%s/repository/blobs/%s' % (self.get_id(), sha)
        return self.manager.gitlab.http_get(path, **kwargs)

    @cli.register_custom_action('Project', ('sha', ))
    @exc.on_http_error(exc.GitlabGetError)
    def repository_raw_blob(self, sha, streamed=False, action=None,
                            chunk_size=1024, **kwargs):
        """Return the raw file contents for a blob.

        Args:
            sha(str): ID of the blob
            streamed (bool): If True the data will be processed by chunks of
                `chunk_size` and each chunk is passed to `action` for
                treatment
            action (callable): Callable responsible of dealing with chunk of
                data
            chunk_size (int): Size of each chunk
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabGetError: If the server failed to perform the request

        Returns:
            str: The blob content if streamed is False, None otherwise
        """
        path = '/projects/%s/repository/blobs/%s/raw' % (self.get_id(), sha)
        result = self.manager.gitlab.http_get(path, streamed=streamed,
                                              **kwargs)
        return utils.response_content(result, streamed, action, chunk_size)

    @cli.register_custom_action('Project', ('from_', 'to'))
    @exc.on_http_error(exc.GitlabGetError)
    def repository_compare(self, from_, to, **kwargs):
        """Return a diff between two branches/commits.

        Args:
            from_(str): Source branch/SHA
            to(str): Destination branch/SHA
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabGetError: If the server failed to perform the request

        Returns:
            str: The diff
        """
        path = '/projects/%s/repository/compare' % self.get_id()
        query_data = {'from': from_, 'to': to}
        return self.manager.gitlab.http_get(path, query_data=query_data,
                                            **kwargs)

    @cli.register_custom_action('Project')
    @exc.on_http_error(exc.GitlabGetError)
    def repository_contributors(self, **kwargs):
        """Return a list of contributors for the project.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabGetError: If the server failed to perform the request

        Returns:
            list: The contributors
        """
        path = '/projects/%s/repository/contributors' % self.get_id()
        return self.manager.gitlab.http_get(path, **kwargs)

    @cli.register_custom_action('Project', tuple(), ('sha', ))
    @exc.on_http_error(exc.GitlabListError)
    def repository_archive(self, sha=None, streamed=False, action=None,
                           chunk_size=1024, **kwargs):
        """Return a tarball of the repository.

        Args:
            sha (str): ID of the commit (default branch by default)
            streamed (bool): If True the data will be processed by chunks of
                `chunk_size` and each chunk is passed to `action` for
                treatment
            action (callable): Callable responsible of dealing with chunk of
                data
            chunk_size (int): Size of each chunk
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabListError: If the server failed to perform the request

        Returns:
            str: The binary data of the archive
        """
        path = '/projects/%s/repository/archive' % self.get_id()
        query_data = {}
        if sha:
            query_data['sha'] = sha
        result = self.manager.gitlab.http_get(path, query_data=query_data,
                                              streamed=streamed, **kwargs)
        return utils.response_content(result, streamed, action, chunk_size)

    @cli.register_custom_action('Project', ('forked_from_id', ))
    @exc.on_http_error(exc.GitlabCreateError)
    def create_fork_relation(self, forked_from_id, **kwargs):
        """Create a forked from/to relation between existing projects.

        Args:
            forked_from_id (int): The ID of the project that was forked from
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabCreateError: If the relation could not be created
        """
        path = '/projects/%s/fork/%s' % (self.get_id(), forked_from_id)
        self.manager.gitlab.http_post(path, **kwargs)

    @cli.register_custom_action('Project')
    @exc.on_http_error(exc.GitlabDeleteError)
    def delete_fork_relation(self, **kwargs):
        """Delete a forked relation between existing projects.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabDeleteError: If the server failed to perform the request
        """
        path = '/projects/%s/fork' % self.get_id()
        self.manager.gitlab.http_delete(path, **kwargs)

    @cli.register_custom_action('Project')
    @exc.on_http_error(exc.GitlabCreateError)
    def star(self, **kwargs):
        """Star a project.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabCreateError: If the server failed to perform the request
        """
        path = '/projects/%s/star' % self.get_id()
        server_data = self.manager.gitlab.http_post(path, **kwargs)
        self._update_attrs(server_data)

    @cli.register_custom_action('Project')
    @exc.on_http_error(exc.GitlabDeleteError)
    def unstar(self, **kwargs):
        """Unstar a project.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabDeleteError: If the server failed to perform the request
        """
        path = '/projects/%s/unstar' % self.get_id()
        server_data = self.manager.gitlab.http_post(path, **kwargs)
        self._update_attrs(server_data)

    @cli.register_custom_action('Project')
    @exc.on_http_error(exc.GitlabCreateError)
    def archive(self, **kwargs):
        """Archive a project.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabCreateError: If the server failed to perform the request
        """
        path = '/projects/%s/archive' % self.get_id()
        server_data = self.manager.gitlab.http_post(path, **kwargs)
        self._update_attrs(server_data)

    @cli.register_custom_action('Project')
    @exc.on_http_error(exc.GitlabDeleteError)
    def unarchive(self, **kwargs):
        """Unarchive a project.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabDeleteError: If the server failed to perform the request
        """
        path = '/projects/%s/unarchive' % self.get_id()
        server_data = self.manager.gitlab.http_post(path, **kwargs)
        self._update_attrs(server_data)

    @cli.register_custom_action('Project', ('group_id', 'group_access'),
                                ('expires_at', ))
    @exc.on_http_error(exc.GitlabCreateError)
    def share(self, group_id, group_access, expires_at=None, **kwargs):
        """Share the project with a group.

        Args:
            group_id (int): ID of the group.
            group_access (int): Access level for the group.
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabCreateError: If the server failed to perform the request
        """
        path = '/projects/%s/share' % self.get_id()
        data = {'group_id': group_id,
                'group_access': group_access,
                'expires_at': expires_at}
        self.manager.gitlab.http_post(path, post_data=data, **kwargs)

    # variables not supported in CLI
    @cli.register_custom_action('Project', ('ref', 'token'))
    @exc.on_http_error(exc.GitlabCreateError)
    def trigger_pipeline(self, ref, token, variables={}, **kwargs):
        """Trigger a CI build.

        See https://gitlab.com/help/ci/triggers/README.md#trigger-a-build

        Args:
            ref (str): Commit to build; can be a commit SHA, a branch name, ...
            token (str): The trigger token
            variables (dict): Variables passed to the build script
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabCreateError: If the server failed to perform the request
        """
        path = '/projects/%s/trigger/pipeline' % self.get_id()
        form = {r'variables[%s]' % k: v for k, v in six.iteritems(variables)}
        post_data = {'ref': ref, 'token': token}
        post_data.update(form)
        self.manager.gitlab.http_post(path, post_data=post_data, **kwargs)


class Runner(SaveMixin, ObjectDeleteMixin, RESTObject):
    pass


class RunnerManager(RetrieveMixin, UpdateMixin, DeleteMixin, RESTManager):
    _path = '/runners'
    _obj_cls = Runner
    _update_attrs = (tuple(), ('description', 'active', 'tag_list'))
    _list_filters = ('scope', )

    @cli.register_custom_action('RunnerManager', tuple(), ('scope', ))
    @exc.on_http_error(exc.GitlabListError)
    def all(self, scope=None, **kwargs):
        """List all the runners.

        Args:
            scope (str): The scope of runners to show, one of: specific,
                shared, active, paused, online
            all (bool): If True, return all the items, without pagination
            per_page (int): Number of items to retrieve per request
            page (int): ID of the page to return (starts with page 1)
            as_list (bool): If set to False and no pagination option is
                defined, return a generator instead of a list
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabListError: If the server failed to perform the request

        Returns:
            list(Runner): a list of runners matching the scope.
        """
        path = '/runners/all'
        query_data = {}
        if scope is not None:
            query_data['scope'] = scope
        return self.gitlab.http_list(path, query_data, **kwargs)


class Todo(ObjectDeleteMixin, RESTObject):
    @cli.register_custom_action('Todo')
    @exc.on_http_error(exc.GitlabTodoError)
    def mark_as_done(self, **kwargs):
        """Mark the todo as done.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabTodoError: If the server failed to perform the request
        """
        path = '%s/%s/mark_as_done' % (self.manager.path, self.id)
        server_data = self.manager.gitlab.http_post(path, **kwargs)
        self._update_attrs(server_data)


class TodoManager(GetFromListMixin, DeleteMixin, RESTManager):
    _path = '/todos'
    _obj_cls = Todo
    _list_filters = ('action', 'author_id', 'project_id', 'state', 'type')

    @cli.register_custom_action('TodoManager')
    @exc.on_http_error(exc.GitlabTodoError)
    def mark_all_as_done(self, **kwargs):
        """Mark all the todos as done.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabTodoError: If the server failed to perform the request

        Returns:
            int: The number of todos maked done
        """
        result = self.gitlab.http_post('/todos/mark_as_done', **kwargs)
        try:
            return int(result)
        except ValueError:
            return 0


class ProjectManager(CRUDMixin, RESTManager):
    _path = '/projects'
    _obj_cls = Project
    _create_attrs = (
        ('name', ),
        ('path', 'namespace_id', 'description', 'issues_enabled',
         'merge_requests_enabled', 'jobs_enabled', 'wiki_enabled',
         'snippets_enabled', 'container_registry_enabled',
         'shared_runners_enabled', 'visibility', 'import_url', 'public_jobs',
         'only_allow_merge_if_build_succeeds',
         'only_allow_merge_if_all_discussions_are_resolved', 'lfs_enabled',
         'request_access_enabled')
    )
    _update_attrs = (
        tuple(),
        ('name', 'path', 'default_branch', 'description', 'issues_enabled',
         'merge_requests_enabled', 'jobs_enabled', 'wiki_enabled',
         'snippets_enabled', 'container_registry_enabled',
         'shared_runners_enabled', 'visibility', 'import_url', 'public_jobs',
         'only_allow_merge_if_build_succeeds',
         'only_allow_merge_if_all_discussions_are_resolved', 'lfs_enabled',
         'request_access_enabled')
    )
    _list_filters = ('search', 'owned', 'starred', 'archived', 'visibility',
                     'order_by', 'sort', 'simple', 'membership', 'statistics',
                     'with_issues_enabled', 'with_merge_requests_enabled')


class GroupProject(Project):
    pass


class GroupProjectManager(GetFromListMixin, RESTManager):
    _path = '/groups/%(group_id)s/projects'
    _obj_cls = GroupProject
    _from_parent_attrs = {'group_id': 'id'}
    _list_filters = ('archived', 'visibility', 'order_by', 'sort', 'search',
                     'ci_enabled_first')


class GroupVariable(SaveMixin, ObjectDeleteMixin, RESTObject):
    _id_attr = 'key'


class GroupVariableManager(CRUDMixin, RESTManager):
    _path = '/groups/%(group_id)s/variables'
    _obj_cls = GroupVariable
    _from_parent_attrs = {'group_id': 'id'}
    _create_attrs = (('key', 'value'), ('protected',))
    _update_attrs = (('key', 'value'), ('protected',))


class Group(SaveMixin, ObjectDeleteMixin, RESTObject):
    _short_print_attr = 'name'
    _managers = (
        ('accessrequests', 'GroupAccessRequestManager'),
        ('members', 'GroupMemberManager'),
        ('notificationsettings', 'GroupNotificationSettingsManager'),
        ('projects', 'GroupProjectManager'),
        ('issues', 'GroupIssueManager'),
        ('variables', 'GroupVariableManager'),
    )

    @cli.register_custom_action('Group', ('to_project_id', ))
    @exc.on_http_error(exc.GitlabTransferProjectError)
    def transfer_project(self, to_project_id, **kwargs):
        """Transfer a project to this group.

        Args:
            to_project_id (int): ID of the project to transfer
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabTransferProjectError: If the project could not be transfered
        """
        path = '/groups/%d/projects/%d' % (self.id, to_project_id)
        self.manager.gitlab.http_post(path, **kwargs)


class GroupManager(CRUDMixin, RESTManager):
    _path = '/groups'
    _obj_cls = Group
    _create_attrs = (
        ('name', 'path'),
        ('description', 'visibility', 'parent_id', 'lfs_enabled',
         'request_access_enabled')
    )
    _update_attrs = (
        tuple(),
        ('name', 'path', 'description', 'visibility', 'lfs_enabled',
         'request_access_enabled')
    )

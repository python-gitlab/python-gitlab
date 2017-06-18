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

import six

from gitlab.base import *  # noqa
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
    def queue_metrics(self, **kwargs):
        """Returns the registred queues information."""
        return self.gitlab.http_get('/sidekiq/queue_metrics', **kwargs)

    def process_metrics(self, **kwargs):
        """Returns the registred sidekiq workers."""
        return self.gitlab.http_get('/sidekiq/process_metrics', **kwargs)

    def job_stats(self, **kwargs):
        """Returns statistics about the jobs performed."""
        return self.gitlab.http_get('/sidekiq/job_stats', **kwargs)

    def compound_metrics(self, **kwargs):
        """Returns all available metrics and statistics."""
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
    _path = '/users/%(user_id)s/emails'
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

    def block(self, **kwargs):
        """Blocks the user.

        Returns:
            bool: whether the user status has been changed.
        """
        path = '/users/%s/block' % self.id
        server_data = self.manager.gitlab.http_post(path, **kwargs)
        if server_data is True:
            self._attrs['state'] = 'blocked'
        return server_data

    def unblock(self, **kwargs):
        """Unblocks the user.

        Returns:
            bool: whether the user status has been changed.
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
                     'external')
    _create_attrs = (
        ('email', 'username', 'name'),
        ('password', 'reset_password', 'skype', 'linkedin', 'twitter',
         'projects_limit', 'extern_uid', 'provider', 'bio', 'admin',
         'can_create_group', 'website_url', 'skip_confirmation', 'external',
         'organization', 'location')
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

    def credentials_auth(self, email, password):
        data = {'email': email, 'password': password}
        server_data = self.gitlab.http_post('/session', post_data=data)
        return CurrentUser(self, server_data)


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

    def content(self, streamed=False, action=None, chunk_size=1024, **kwargs):
        """Return the content of a snippet.

        Args:
            streamed (bool): If True the data will be processed by chunks of
                `chunk_size` and each chunk is passed to `action` for
                treatment.
            action (callable): Callable responsible of dealing with chunk of
                data.
            chunk_size (int): Size of each chunk.

        Returns:
            str: The snippet content.
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

    def public(self, **kwargs):
        """List all the public snippets.

        Args:
            all (bool): If True, return all the items, without pagination
            **kwargs: Additional arguments to send to GitLab.

        Returns:
            list(gitlab.Gitlab.Snippet): The list of snippets.
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

    def protect(self, developers_can_push=False, developers_can_merge=False,
                **kwargs):
        """Protects the branch.

        Args:
            developers_can_push (bool): Set to True if developers are allowed
                                        to push to the branch
            developers_can_merge (bool): Set to True if developers are allowed
                                         to merge to the branch
        """
        path = '%s/%s/protect' % (self.manager.path, self.get_id())
        post_data = {'developers_can_push': developers_can_push,
                     'developers_can_merge': developers_can_merge}
        self.manager.gitlab.http_put(path, post_data=post_data, **kwargs)
        self._attrs['protected'] = True

    def unprotect(self, **kwargs):
        """Unprotects the branch."""
        path = '%s/%s/protect' % (self.manager.path, self.get_id())
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

    def cancel(self, **kwargs):
        """Cancel the job."""
        path = '%s/%s/cancel' % (self.manager.path, self.get_id())
        self.manager.gitlab.http_post(path)

    def retry(self, **kwargs):
        """Retry the job."""
        path = '%s/%s/retry' % (self.manager.path, self.get_id())
        self.manager.gitlab.http_post(path)

    def play(self, **kwargs):
        """Trigger a job explicitly."""
        path = '%s/%s/play' % (self.manager.path, self.get_id())
        self.manager.gitlab.http_post(path)

    def erase(self, **kwargs):
        """Erase the job (remove job artifacts and trace)."""
        path = '%s/%s/erase' % (self.manager.path, self.get_id())
        self.manager.gitlab.http_post(path)

    def keep_artifacts(self, **kwargs):
        """Prevent artifacts from being delete when expiration is set."""
        path = '%s/%s/artifacts/keep' % (self.manager.path, self.get_id())
        self.manager.gitlab.http_post(path)

    def artifacts(self, streamed=False, action=None, chunk_size=1024,
                  **kwargs):
        """Get the job artifacts.

        Args:
            streamed (bool): If True the data will be processed by chunks of
                `chunk_size` and each chunk is passed to `action` for
                treatment.
            action (callable): Callable responsible of dealing with chunk of
                data.
            chunk_size (int): Size of each chunk.

        Returns:
            str: The artifacts if `streamed` is False, None otherwise.
        """
        path = '%s/%s/artifacts' % (self.manager.path, self.get_id())
        result = self.manager.gitlab.get_http(path, streamed=streamed,
                                              **kwargs)
        return utils.response_content(result, streamed, action, chunk_size)

    def trace(self, streamed=False, action=None, chunk_size=1024, **kwargs):
        """Get the job trace.

        Args:
            streamed (bool): If True the data will be processed by chunks of
                `chunk_size` and each chunk is passed to `action` for
                treatment.
            action (callable): Callable responsible of dealing with chunk of
                data.
            chunk_size (int): Size of each chunk.

        Returns:
            str: The trace.
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


class ProjectCommitStatusManager(RetrieveMixin, CreateMixin, RESTManager):
    _path = ('/projects/%(project_id)s/repository/commits/%(commit_id)s'
             '/statuses')
    _obj_cls = ProjectCommitStatus
    _from_parent_attrs = {'project_id': 'project_id', 'commit_id': 'id'}
    _create_attrs = (('state', ),
                     ('description', 'name', 'context', 'ref', 'target_url'))

    def create(self, data, **kwargs):
        """Creates a new object.

        Args:
            data (dict): parameters to send to the server to create the
                         resource
            **kwargs: Extra data to send to the Gitlab server (e.g. sudo or
                      'ref_name', 'stage', 'name', 'all'.

        Returns:
            RESTObject: a new instance of the manage object class build with
                        the data sent by the server
        """
        path = '/projects/%(project_id)s/statuses/%(commit_id)s'
        computed_path = self._compute_path(path)
        return CreateMixin.create(self, data, path=computed_path, **kwargs)


class ProjectCommitComment(RESTObject):
    pass


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

    def diff(self, **kwargs):
        """Generate the commit diff."""
        path = '%s/%s/diff' % (self.manager.path, self.get_id())
        return self.manager.gitlab.http_get(path, **kwargs)

    def cherry_pick(self, branch, **kwargs):
        """Cherry-pick a commit into a branch.

        Args:
            branch (str): Name of target branch.
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

    def enable(self, key_id, **kwargs):
        """Enable a deploy key for a project.

        Args:
            key_id (int): The ID of the key to enable
        """
        path = '%s/%s/enable' % (self.manager.path, key_id)
        self.manager.gitlab.http_post(path, **kwargs)


class ProjectEvent(RESTObject):
    _short_print_attr = 'target_title'


class ProjectEventManager(GetFromListMixin, RESTManager):
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
    requiredUrlAttrs = ['project_id']
    requiredCreateAttrs = ['url']
    optionalCreateAttrs = ['push_events', 'issues_events', 'note_events',
                           'merge_requests_events', 'tag_push_events',
                           'build_events', 'enable_ssl_verification', 'token',
                           'pipeline_events', 'job_events', 'wiki_page_events']
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
    _create_attrs = (('body', ), ('created_at'))
    _update_attrs = (('body', ), tuple())


class ProjectIssue(SubscribableMixin, TodoMixin, TimeTrackingMixin, SaveMixin,
                   ObjectDeleteMixin, RESTObject):
    _constructor_types = {'author': 'User', 'assignee': 'User', 'milestone':
                          'ProjectMilestone'}
    _short_print_attr = 'title'
    _id_attr = 'iid'
    _managers = (('notes', 'ProjectIssueNoteManager'), )

    def move(self, to_project_id, **kwargs):
        """Move the issue to another project."""
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
    requiredCreateAttrs = ['access_level', 'user_id']
    optionalCreateAttrs = ['expires_at']
    requiredUpdateAttrs = ['access_level']
    optionalCreateAttrs = ['expires_at']
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

    def set_release_description(self, description, **kwargs):
        """Set the release notes on the tag.

        If the release doesn't exist yet, it will be created. If it already
        exists, its description will be updated.

        Args:
            description (str): Description of the release.
        """
        path = '%s/%s/release' % (self.manager.path, self.get_id())
        data = {'description': description}
        if self.release is None:
            result = self.manager.gitlab.http_post(path, post_data=data,
                                                   **kwargs)
        else:
            result = self.manager.gitlab.http_put(path, post_data=data,
                                                  **kwargs)
        self.release = result.json()


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

    def cancel_merge_when_pipeline_succeeds(self, **kwargs):
        """Cancel merge when build succeeds."""

        path = ('%s/%s/cancel_merge_when_pipeline_succeeds' %
                (self.manager.path, self.get_id()))
        server_data = self.manager.gitlab.http_put(path, **kwargs)
        self._update_attrs(server_data)

    def closes_issues(self, **kwargs):
        """List issues that will close on merge."

        Returns:
            list (ProjectIssue): List of issues
        """
        path = '%s/%s/closes_issues' % (self.manager.path, self.get_id())
        data_list = self.manager.gitlab.http_list(path, **kwargs)
        manager = ProjectIssueManager(self.manager.gitlab,
                                      parent=self.manager._parent)
        return RESTObjectList(manager, ProjectIssue, data_list)

    def commits(self, **kwargs):
        """List the merge request commits.

        Returns:
            list (ProjectCommit): List of commits
        """

        path = '%s/%s/commits' % (self.manager.path, self.get_id())
        data_list = self.manager.gitlab.http_list(path, **kwargs)
        manager = ProjectCommitManager(self.manager.gitlab,
                                       parent=self.manager._parent)
        return RESTObjectList(manager, ProjectCommit, data_list)

    def changes(self, **kwargs):
        """List the merge request changes.

        Returns:
            list (dict): List of changes
        """
        path = '%s/%s/changes' % (self.manager.path, self.get_id())
        return self.manager.gitlab.http_get(path, **kwargs)

    def merge(self, merge_commit_message=None,
              should_remove_source_branch=False,
              merged_when_build_succeeds=False,
              **kwargs):
        """Accept the merge request.

        Args:
            merge_commit_message (bool): Commit message
            should_remove_source_branch (bool): If True, removes the source
                                                branch
            merged_when_build_succeeds (bool): Wait for the build to succeed,
                                               then merge
        """
        path = '%s/%s/merge' % (self.manager.path, self.get_id())
        data = {}
        if merge_commit_message:
            data['merge_commit_message'] = merge_commit_message
        if should_remove_source_branch:
            data['should_remove_source_branch'] = True
        if merged_when_build_succeeds:
            data['merged_when_build_succeeds'] = True

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

    def issues(self, **kwargs):
        """List issues related to this milestone

        Returns:
            list (ProjectIssue): The list of issues
        """

        path = '%s/%s/issues' % (self.manager.path, self.get_id())
        data_list = self.manager.gitlab.http_list(path, **kwargs)
        manager = ProjectCommitManager(self.manager.gitlab,
                                       parent=self.manager._parent)
        # FIXME(gpocentek): the computed manager path is not correct
        return RESTObjectList(manager, ProjectIssue, data_list)

    def merge_requests(self, **kwargs):
        """List the merge requests related to this milestone

        Returns:
            list (ProjectMergeRequest): List of merge requests
        """
        path = '%s/%s/merge_requests' % (self.manager.path, self.get_id())
        data_list = self.manager.gitlab.http_list(path, **kwargs)
        manager = ProjectCommitManager(self.manager.gitlab,
                                       parent=self.manager._parent)
        # FIXME(gpocentek): the computed manager path is not correct
        return RESTObjectList(manager, ProjectMergeRequest, data_list)


class ProjectMilestoneManager(RetrieveMixin, CreateMixin, DeleteMixin,
                              RESTManager):
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


class ProjectLabelManager(GetFromListMixin, CreateMixin, UpdateMixin,
                          DeleteMixin, RESTManager):
    _path = '/projects/%(project_id)s/labels'
    _obj_cls = ProjectLabel
    _from_parent_attrs = {'project_id': 'id'}
    _create_attrs = (('name', 'color'), ('description', 'priority'))
    _update_attrs = (('name', ),
                     ('new_name', 'color', 'description', 'priority'))

    # Delete without ID.
    def delete(self, name, **kwargs):
        """Deletes a Label on the server.

        Args:
            name: The name of the label.
            **kwargs: Extra data to send to the Gitlab server (e.g. sudo)
        """
        self.gitlab.http_delete(path, query_data={'name': self.name}, **kwargs)

    # Update without ID, but we need an ID to get from list.
    def save(self, **kwargs):
        """Saves the changes made to the object to the server.

        Args:
            **kwargs: Extra option to send to the server (e.g. sudo)

        The object is updated to match what the server returns.
        """
        updated_data = self._get_updated_data()

        # call the manager
        server_data = self.manager.update(None, updated_data, **kwargs)
        self._update_attrs(server_data)


class ProjectFile(SaveMixin, ObjectDeleteMixin, RESTObject):
    _id_attr = 'file_path'
    _short_print_attr = 'file_path'

    def decode(self):
        """Returns the decoded content of the file.

        Returns:
            (str): the decoded content.
        """
        return base64.b64decode(self.content)


class ProjectFileManager(GetMixin, CreateMixin, UpdateMixin, DeleteMixin,
                         RESTManager):
    _path = '/projects/%(project_id)s/repository/files'
    _obj_cls = ProjectFile
    _from_parent_attrs = {'project_id': 'id'}
    _create_attrs = (('file_path', 'branch', 'content', 'commit_message'),
                     ('encoding', 'author_email', 'author_name'))
    _update_attrs = (('file_path', 'branch', 'content', 'commit_message'),
                     ('encoding', 'author_email', 'author_name'))

    def get(self, file_path, **kwargs):
        """Retrieve a single object.

        Args:
            id (int or str): ID of the object to retrieve
            **kwargs: Extra data to send to the Gitlab server (e.g. sudo)

        Returns:
            object: The generated RESTObject.
        """
        file_path = file_path.replace('/', '%2F')
        return GetMixin.get(self, file_path, **kwargs)

    def raw(self, file_path, ref, streamed=False, action=None, chunk_size=1024,
            **kwargs):
        """Return the content of a file for a commit.

        Args:
            ref (str): ID of the commit
            filepath (str): Path of the file to return
            streamed (bool): If True the data will be processed by chunks of
                `chunk_size` and each chunk is passed to `action` for
                treatment.
            action (callable): Callable responsible of dealing with chunk of
                data.
            chunk_size (int): Size of each chunk.

        Returns:
            str: The file content
        """
        file_path = file_path.replace('/', '%2F')
        path = '%s/%s/raw' % (self.path, file_path)
        query_data = {'ref': ref}
        result = self.gitlab.http_get(path, query_data=query_data,
                                      streamed=streamed, **kwargs)
        return utils.response_content(result, streamed, action, chunk_size)


class ProjectPipeline(RESTObject):
    def cancel(self, **kwargs):
        """Cancel the job."""
        path = '%s/%s/cancel' % (self.manager.path, self.get_id())
        self.manager.gitlab.http_post(path)

    def retry(self, **kwargs):
        """Retry the job."""
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
            data (dict): parameters to send to the server to create the
                         resource
            **kwargs: Extra data to send to the Gitlab server (e.g. sudo)

        Returns:
            RESTObject: a new instance of the manage object class build with
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
    _create_attrs = (('key', 'vaule'), tuple())
    _update_attrs = (('key', 'vaule'), tuple())


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


class ProjectRunner(ObjectDeleteMixin, RESTObject):
    canUpdate = False
    requiredCreateAttrs = ['runner_id']


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
        ('runners', 'ProjectRunnerManager'),
        ('services', 'ProjectServiceManager'),
        ('snippets', 'ProjectSnippetManager'),
        ('tags', 'ProjectTagManager'),
        ('triggers', 'ProjectTriggerManager'),
        ('variables', 'ProjectVariableManager'),
    )

    def repository_tree(self, path='', ref='', **kwargs):
        """Return a list of files in the repository.

        Args:
            path (str): Path of the top folder (/ by default)
            ref (str): Reference to a commit or branch

        Returns:
            str: The json representation of the tree.
        """
        gl_path = '/projects/%s/repository/tree' % self.get_id()
        query_data = {}
        if path:
            query_data['path'] = path
        if ref:
            query_data['ref'] = ref
        return self.manager.gitlab.http_get(gl_path, query_data=query_data,
                                            **kwargs)

    def repository_blob(self, sha, **kwargs):
        """Returns a blob by blob SHA.

        Args:
            sha(str): ID of the blob

        Returns:
            str: The blob as json
        """

        path = '/projects/%s/repository/blobs/%s' % (self.get_id(), sha)
        return self.manager.gitlab.http_get(path, **kwargs)

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
        """
        path = '/projects/%s/repository/blobs/%s/raw' % (self.get_id(), sha)
        result = self.manager.gitlab.http_get(path, streamed=streamed,
                                              **kwargs)
        return utils.response_content(result, streamed, action, chunk_size)

    def repository_compare(self, from_, to, **kwargs):
        """Returns a diff between two branches/commits.

        Args:
            from_(str): orig branch/SHA
            to(str): dest branch/SHA

        Returns:
            str: The diff
        """
        path = '/projects/%s/repository/compare' % self.get_id()
        query_data = {'from': from_, 'to': to}
        return self.manager.gitlab.http_get(path, query_data=query_data,
                                            **kwargs)

    def repository_contributors(self, **kwargs):
        """Returns a list of contributors for the project.

        Returns:
            list: The contributors
        """
        path = '/projects/%s/repository/contributors' % self.get_id()
        return self.manager.gitlab.http_get(path, **kwargs)

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
        """
        path = '/projects/%s/repository/archive' % self.get_id()
        query_data = {}
        if sha:
            query_data['sha'] = sha
        result = self.manager.gitlab.http_get(path, query_data=query_data,
                                              streamed=streamed, **kwargs)
        return utils.response_content(result, streamed, action, chunk_size)

    def create_fork_relation(self, forked_from_id, **kwargs):
        """Create a forked from/to relation between existing projects.

        Args:
            forked_from_id (int): The ID of the project that was forked from
        """
        path = '/projects/%s/fork/%s' % (self.get_id(), forked_from_id)
        self.manager.gitlab.http_post(path, **kwargs)

    def delete_fork_relation(self, **kwargs):
        """Delete a forked relation between existing projects."""
        path = '/projects/%s/fork' % self.get_id()
        self.manager.gitlab.http_delete(path, **kwargs)

    def star(self, **kwargs):
        """Star a project.

        Returns:
            Project: the updated Project
        """
        path = '/projects/%s/star' % self.get_id()
        server_data = self.manager.gitlab.http_post(path, **kwargs)
        self._update_attrs(server_data)

    def unstar(self, **kwargs):
        """Unstar a project.

        Returns:
            Project: the updated Project
        """
        path = '/projects/%s/unstar' % self.get_id()
        server_data = self.manager.gitlab.http_post(path, **kwargs)
        self._update_attrs(server_data)

    def archive(self, **kwargs):
        """Archive a project.

        Returns:
            Project: the updated Project
        """
        path = '/projects/%s/archive' % self.get_id()
        server_data = self.manager.gitlab.http_post(path, **kwargs)
        self._update_attrs(server_data)

    def unarchive(self, **kwargs):
        """Unarchive a project.

        Returns:
            Project: the updated Project
        """
        path = '/projects/%s/unarchive' % self.get_id()
        server_data = self.manager.gitlab.http_post(path, **kwargs)
        self._update_attrs(server_data)

    def share(self, group_id, group_access, expires_at=None, **kwargs):
        """Share the project with a group.

        Args:
            group_id (int): ID of the group.
            group_access (int): Access level for the group.
        """
        path = '/projects/%s/share' % self.get_id()
        data = {'group_id': group_id,
                'group_access': group_access,
                'expires_at': expires_at}
        self.manager.gitlab.http_post(path, post_data=data, **kwargs)

    def trigger_pipeline(self, ref, token, variables={}, **kwargs):
        """Trigger a CI build.

        See https://gitlab.com/help/ci/triggers/README.md#trigger-a-build

        Args:
            ref (str): Commit to build; can be a commit SHA, a branch name, ...
            token (str): The trigger token
            variables (dict): Variables passed to the build script
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

    def all(self, scope=None, **kwargs):
        """List all the runners.

        Args:
            scope (str): The scope of runners to show, one of: specific,
                shared, active, paused, online

        Returns:
            list(Runner): a list of runners matching the scope.
        """
        path = '/runners/all'
        query_data = {}
        if scope is not None:
            query_data['scope'] = scope
        return self.gitlab.http_list(path, query_data, **kwargs)


class Todo(ObjectDeleteMixin, RESTObject):
    def mark_as_done(self, **kwargs):
        """Mark the todo as done.

        Args:
            **kwargs: Additional data to send to the server (e.g. sudo)
        """
        path = '%s/%s/mark_as_done' % (self.manager.path, self.id)
        server_data = self.manager.gitlab.http_post(path, **kwargs)
        self._update_attrs(server_data)


class TodoManager(GetFromListMixin, DeleteMixin, RESTManager):
    _path = '/todos'
    _obj_cls = Todo
    _list_filters = ('action', 'author_id', 'project_id', 'state', 'type')

    def mark_all_as_done(self, **kwargs):
        """Mark all the todos as done.

        Returns:
            The number of todos maked done.
        """
        self.gitlab.http_post('/todos/mark_as_done', **kwargs)


class ProjectManager(CRUDMixin, RESTManager):
    _path = '/projects'
    _obj_cls = Project
    _create_attrs = (
        ('name', ),
        ('path', 'namespace_id', 'description', 'issues_enabled',
         'merge_requests_enabled', 'builds_enabled', 'wiki_enabled',
         'snippets_enabled', 'container_registry_enabled',
         'shared_runners_enabled', 'visibility', 'import_url', 'public_builds',
         'only_allow_merge_if_build_succeeds',
         'only_allow_merge_if_all_discussions_are_resolved', 'lfs_enabled',
         'request_access_enabled')
    )
    _update_attrs = (
        tuple(),
        ('name', 'path', 'default_branch', 'description', 'issues_enabled',
         'merge_requests_enabled', 'builds_enabled', 'wiki_enabled',
         'snippets_enabled', 'container_registry_enabled',
         'shared_runners_enabled', 'visibility', 'import_url', 'public_builds',
         'only_allow_merge_if_build_succeeds',
         'only_allow_merge_if_all_discussions_are_resolved', 'lfs_enabled',
         'request_access_enabled')
    )
    _list_filters = ('search', 'owned', 'starred', 'archived', 'visibility',
                     'order_by', 'sort', 'simple', 'membership', 'statistics')


class GroupProject(RESTObject):
    def __init__(self, *args, **kwargs):
        Project.__init__(self, *args, **kwargs)


class GroupProjectManager(GetFromListMixin, RESTManager):
    _path = '/groups/%(group_id)s/projects'
    _obj_cls = GroupProject
    _from_parent_attrs = {'group_id': 'id'}
    _list_filters = ('archived', 'visibility', 'order_by', 'sort', 'search',
                     'ci_enabled_first')


class Group(SaveMixin, ObjectDeleteMixin, RESTObject):
    _short_print_attr = 'name'
    _managers = (
        ('accessrequests', 'GroupAccessRequestManager'),
        ('members', 'GroupMemberManager'),
        ('notificationsettings', 'GroupNotificationSettingsManager'),
        ('projects', 'GroupProjectManager'),
        ('issues', 'GroupIssueManager'),
    )

    def transfer_project(self, id, **kwargs):
        """Transfers a project to this group.

        Attrs:
            id (int): ID of the project to transfer.
        """
        path = '/groups/%d/projects/%d' % (self.id, id)
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

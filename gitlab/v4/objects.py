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

from gitlab.base import *  # noqa
from gitlab import cli
from gitlab.exceptions import *  # noqa
from gitlab.mixins import *  # noqa
from gitlab import types
from gitlab import utils

VISIBILITY_PRIVATE = "private"
VISIBILITY_INTERNAL = "internal"
VISIBILITY_PUBLIC = "public"

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

    @cli.register_custom_action("SidekiqManager")
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
        return self.gitlab.http_get("/sidekiq/queue_metrics", **kwargs)

    @cli.register_custom_action("SidekiqManager")
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
        return self.gitlab.http_get("/sidekiq/process_metrics", **kwargs)

    @cli.register_custom_action("SidekiqManager")
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
        return self.gitlab.http_get("/sidekiq/job_stats", **kwargs)

    @cli.register_custom_action("SidekiqManager")
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
        return self.gitlab.http_get("/sidekiq/compound_metrics", **kwargs)


class Event(RESTObject):
    _id_attr = None
    _short_print_attr = "target_title"


class AuditEvent(RESTObject):
    _id_attr = "id"


class AuditEventManager(ListMixin, RESTManager):
    _path = "/audit_events"
    _obj_cls = AuditEvent
    _list_filters = ("created_after", "created_before", "entity_type", "entity_id")


class EventManager(ListMixin, RESTManager):
    _path = "/events"
    _obj_cls = Event
    _list_filters = ("action", "target_type", "before", "after", "sort")


class UserActivities(RESTObject):
    _id_attr = "username"


class UserStatus(RESTObject):
    _id_attr = None
    _short_print_attr = "message"


class UserStatusManager(GetWithoutIdMixin, RESTManager):
    _path = "/users/%(user_id)s/status"
    _obj_cls = UserStatus
    _from_parent_attrs = {"user_id": "id"}


class UserActivitiesManager(ListMixin, RESTManager):
    _path = "/user/activities"
    _obj_cls = UserActivities


class UserCustomAttribute(ObjectDeleteMixin, RESTObject):
    _id_attr = "key"


class UserCustomAttributeManager(RetrieveMixin, SetMixin, DeleteMixin, RESTManager):
    _path = "/users/%(user_id)s/custom_attributes"
    _obj_cls = UserCustomAttribute
    _from_parent_attrs = {"user_id": "id"}


class UserEmail(ObjectDeleteMixin, RESTObject):
    _short_print_attr = "email"


class UserEmailManager(RetrieveMixin, CreateMixin, DeleteMixin, RESTManager):
    _path = "/users/%(user_id)s/emails"
    _obj_cls = UserEmail
    _from_parent_attrs = {"user_id": "id"}
    _create_attrs = (("email",), tuple())


class UserEvent(Event):
    pass


class UserEventManager(EventManager):
    _path = "/users/%(user_id)s/events"
    _obj_cls = UserEvent
    _from_parent_attrs = {"user_id": "id"}


class UserGPGKey(ObjectDeleteMixin, RESTObject):
    pass


class UserGPGKeyManager(RetrieveMixin, CreateMixin, DeleteMixin, RESTManager):
    _path = "/users/%(user_id)s/gpg_keys"
    _obj_cls = UserGPGKey
    _from_parent_attrs = {"user_id": "id"}
    _create_attrs = (("key",), tuple())


class UserKey(ObjectDeleteMixin, RESTObject):
    pass


class UserKeyManager(ListMixin, CreateMixin, DeleteMixin, RESTManager):
    _path = "/users/%(user_id)s/keys"
    _obj_cls = UserKey
    _from_parent_attrs = {"user_id": "id"}
    _create_attrs = (("title", "key"), tuple())


class UserStatus(RESTObject):
    pass


class UserStatusManager(GetWithoutIdMixin, RESTManager):
    _path = "/users/%(user_id)s/status"
    _obj_cls = UserStatus
    _from_parent_attrs = {"user_id": "id"}


class UserImpersonationToken(ObjectDeleteMixin, RESTObject):
    pass


class UserImpersonationTokenManager(NoUpdateMixin, RESTManager):
    _path = "/users/%(user_id)s/impersonation_tokens"
    _obj_cls = UserImpersonationToken
    _from_parent_attrs = {"user_id": "id"}
    _create_attrs = (("name", "scopes"), ("expires_at",))
    _list_filters = ("state",)


class UserProject(RESTObject):
    pass


class UserProjectManager(ListMixin, CreateMixin, RESTManager):
    _path = "/projects/user/%(user_id)s"
    _obj_cls = UserProject
    _from_parent_attrs = {"user_id": "id"}
    _create_attrs = (
        ("name",),
        (
            "default_branch",
            "issues_enabled",
            "wall_enabled",
            "merge_requests_enabled",
            "wiki_enabled",
            "snippets_enabled",
            "public",
            "visibility",
            "description",
            "builds_enabled",
            "public_builds",
            "import_url",
            "only_allow_merge_if_build_succeeds",
        ),
    )
    _list_filters = (
        "archived",
        "visibility",
        "order_by",
        "sort",
        "search",
        "simple",
        "owned",
        "membership",
        "starred",
        "statistics",
        "with_issues_enabled",
        "with_merge_requests_enabled",
    )

    def list(self, **kwargs):
        """Retrieve a list of objects.

        Args:
            all (bool): If True, return all the items, without pagination
            per_page (int): Number of items to retrieve per request
            page (int): ID of the page to return (starts with page 1)
            as_list (bool): If set to False and no pagination option is
                defined, return a generator instead of a list
            **kwargs: Extra options to send to the server (e.g. sudo)

        Returns:
            list: The list of objects, or a generator if `as_list` is False

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabListError: If the server cannot perform the request
        """
        if self._parent:
            path = "/users/%s/projects" % self._parent.id
        else:
            path = "/users/%s/projects" % kwargs["user_id"]
        return ListMixin.list(self, path=path, **kwargs)


class User(SaveMixin, ObjectDeleteMixin, RESTObject):
    _short_print_attr = "username"
    _managers = (
        ("customattributes", "UserCustomAttributeManager"),
        ("emails", "UserEmailManager"),
        ("events", "UserEventManager"),
        ("gpgkeys", "UserGPGKeyManager"),
        ("impersonationtokens", "UserImpersonationTokenManager"),
        ("keys", "UserKeyManager"),
        ("projects", "UserProjectManager"),
        ("status", "UserStatusManager"),
    )

    @cli.register_custom_action("User")
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
        path = "/users/%s/block" % self.id
        server_data = self.manager.gitlab.http_post(path, **kwargs)
        if server_data is True:
            self._attrs["state"] = "blocked"
        return server_data

    @cli.register_custom_action("User")
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
        path = "/users/%s/unblock" % self.id
        server_data = self.manager.gitlab.http_post(path, **kwargs)
        if server_data is True:
            self._attrs["state"] = "active"
        return server_data

    @cli.register_custom_action("User")
    @exc.on_http_error(exc.GitlabDeactivateError)
    def deactivate(self, **kwargs):
        """Deactivate the user.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabDeactivateError: If the user could not be deactivated

        Returns:
            bool: Whether the user status has been changed
        """
        path = "/users/%s/deactivate" % self.id
        server_data = self.manager.gitlab.http_post(path, **kwargs)
        if server_data:
            self._attrs["state"] = "deactivated"
        return server_data

    @cli.register_custom_action("User")
    @exc.on_http_error(exc.GitlabActivateError)
    def activate(self, **kwargs):
        """Activate the user.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabActivateError: If the user could not be activated

        Returns:
            bool: Whether the user status has been changed
        """
        path = "/users/%s/activate" % self.id
        server_data = self.manager.gitlab.http_post(path, **kwargs)
        if server_data:
            self._attrs["state"] = "active"
        return server_data


class UserManager(CRUDMixin, RESTManager):
    _path = "/users"
    _obj_cls = User

    _list_filters = (
        "active",
        "blocked",
        "username",
        "extern_uid",
        "provider",
        "external",
        "search",
        "custom_attributes",
        "status",
    )
    _create_attrs = (
        tuple(),
        (
            "email",
            "username",
            "name",
            "password",
            "reset_password",
            "skype",
            "linkedin",
            "twitter",
            "projects_limit",
            "extern_uid",
            "provider",
            "bio",
            "admin",
            "can_create_group",
            "website_url",
            "skip_confirmation",
            "external",
            "organization",
            "location",
            "avatar",
        ),
    )
    _update_attrs = (
        ("email", "username", "name"),
        (
            "password",
            "skype",
            "linkedin",
            "twitter",
            "projects_limit",
            "extern_uid",
            "provider",
            "bio",
            "admin",
            "can_create_group",
            "website_url",
            "skip_confirmation",
            "external",
            "organization",
            "location",
            "avatar",
        ),
    )
    _types = {"confirm": types.LowercaseStringAttribute, "avatar": types.ImageAttribute}


class CurrentUserEmail(ObjectDeleteMixin, RESTObject):
    _short_print_attr = "email"


class CurrentUserEmailManager(RetrieveMixin, CreateMixin, DeleteMixin, RESTManager):
    _path = "/user/emails"
    _obj_cls = CurrentUserEmail
    _create_attrs = (("email",), tuple())


class CurrentUserGPGKey(ObjectDeleteMixin, RESTObject):
    pass


class CurrentUserGPGKeyManager(RetrieveMixin, CreateMixin, DeleteMixin, RESTManager):
    _path = "/user/gpg_keys"
    _obj_cls = CurrentUserGPGKey
    _create_attrs = (("key",), tuple())


class CurrentUserKey(ObjectDeleteMixin, RESTObject):
    _short_print_attr = "title"


class CurrentUserKeyManager(RetrieveMixin, CreateMixin, DeleteMixin, RESTManager):
    _path = "/user/keys"
    _obj_cls = CurrentUserKey
    _create_attrs = (("title", "key"), tuple())


class CurrentUserStatus(SaveMixin, RESTObject):
    _id_attr = None
    _short_print_attr = "message"


class CurrentUserStatusManager(GetWithoutIdMixin, UpdateMixin, RESTManager):
    _path = "/user/status"
    _obj_cls = CurrentUserStatus
    _update_attrs = (tuple(), ("emoji", "message"))


class CurrentUser(RESTObject):
    _id_attr = None
    _short_print_attr = "username"
    _managers = (
        ("status", "CurrentUserStatusManager"),
        ("emails", "CurrentUserEmailManager"),
        ("gpgkeys", "CurrentUserGPGKeyManager"),
        ("keys", "CurrentUserKeyManager"),
    )


class CurrentUserManager(GetWithoutIdMixin, RESTManager):
    _path = "/user"
    _obj_cls = CurrentUser


class ApplicationSettings(SaveMixin, RESTObject):
    _id_attr = None


class ApplicationSettingsManager(GetWithoutIdMixin, UpdateMixin, RESTManager):
    _path = "/application/settings"
    _obj_cls = ApplicationSettings
    _update_attrs = (
        tuple(),
        (
            "id",
            "default_projects_limit",
            "signup_enabled",
            "password_authentication_enabled_for_web",
            "gravatar_enabled",
            "sign_in_text",
            "created_at",
            "updated_at",
            "home_page_url",
            "default_branch_protection",
            "restricted_visibility_levels",
            "max_attachment_size",
            "session_expire_delay",
            "default_project_visibility",
            "default_snippet_visibility",
            "default_group_visibility",
            "outbound_local_requests_whitelist",
            "domain_whitelist",
            "domain_blacklist_enabled",
            "domain_blacklist",
            "external_authorization_service_enabled",
            "external_authorization_service_url",
            "external_authorization_service_default_label",
            "external_authorization_service_timeout",
            "user_oauth_applications",
            "after_sign_out_path",
            "container_registry_token_expire_delay",
            "repository_storages",
            "plantuml_enabled",
            "plantuml_url",
            "terminal_max_session_time",
            "polling_interval_multiplier",
            "rsa_key_restriction",
            "dsa_key_restriction",
            "ecdsa_key_restriction",
            "ed25519_key_restriction",
            "first_day_of_week",
            "enforce_terms",
            "terms",
            "performance_bar_allowed_group_id",
            "instance_statistics_visibility_private",
            "user_show_add_ssh_key_message",
            "file_template_project_id",
            "local_markdown_version",
            "asset_proxy_enabled",
            "asset_proxy_url",
            "asset_proxy_whitelist",
            "geo_node_allowed_ips",
            "allow_local_requests_from_hooks_and_services",
            "allow_local_requests_from_web_hooks_and_services",
            "allow_local_requests_from_system_hooks",
        ),
    )

    @exc.on_http_error(exc.GitlabUpdateError)
    def update(self, id=None, new_data=None, **kwargs):
        """Update an object on the server.

        Args:
            id: ID of the object to update (can be None if not required)
            new_data: the update data for the object
            **kwargs: Extra options to send to the server (e.g. sudo)

        Returns:
            dict: The new object data (*not* a RESTObject)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabUpdateError: If the server cannot perform the request
        """
        new_data = new_data or {}
        data = new_data.copy()
        if "domain_whitelist" in data and data["domain_whitelist"] is None:
            data.pop("domain_whitelist")
        super(ApplicationSettingsManager, self).update(id, data, **kwargs)


class BroadcastMessage(SaveMixin, ObjectDeleteMixin, RESTObject):
    pass


class BroadcastMessageManager(CRUDMixin, RESTManager):
    _path = "/broadcast_messages"
    _obj_cls = BroadcastMessage

    _create_attrs = (("message",), ("starts_at", "ends_at", "color", "font"))
    _update_attrs = (tuple(), ("message", "starts_at", "ends_at", "color", "font"))


class DeployKey(RESTObject):
    pass


class DeployKeyManager(ListMixin, RESTManager):
    _path = "/deploy_keys"
    _obj_cls = DeployKey


class NotificationSettings(SaveMixin, RESTObject):
    _id_attr = None


class NotificationSettingsManager(GetWithoutIdMixin, UpdateMixin, RESTManager):
    _path = "/notification_settings"
    _obj_cls = NotificationSettings

    _update_attrs = (
        tuple(),
        (
            "level",
            "notification_email",
            "new_note",
            "new_issue",
            "reopen_issue",
            "close_issue",
            "reassign_issue",
            "new_merge_request",
            "reopen_merge_request",
            "close_merge_request",
            "reassign_merge_request",
            "merge_merge_request",
        ),
    )


class Dockerfile(RESTObject):
    _id_attr = "name"


class DockerfileManager(RetrieveMixin, RESTManager):
    _path = "/templates/dockerfiles"
    _obj_cls = Dockerfile


class Feature(ObjectDeleteMixin, RESTObject):
    _id_attr = "name"


class FeatureManager(ListMixin, DeleteMixin, RESTManager):
    _path = "/features/"
    _obj_cls = Feature

    @exc.on_http_error(exc.GitlabSetError)
    def set(self, name, value, feature_group=None, user=None, **kwargs):
        """Create or update the object.

        Args:
            name (str): The value to set for the object
            value (bool/int): The value to set for the object
            feature_group (str): A feature group name
            user (str): A GitLab username
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabSetError: If an error occured

        Returns:
            obj: The created/updated attribute
        """
        path = "%s/%s" % (self.path, name.replace("/", "%2F"))
        data = {"value": value, "feature_group": feature_group, "user": user}
        server_data = self.gitlab.http_post(path, post_data=data, **kwargs)
        return self._obj_cls(self, server_data)


class Gitignore(RESTObject):
    _id_attr = "name"


class GitignoreManager(RetrieveMixin, RESTManager):
    _path = "/templates/gitignores"
    _obj_cls = Gitignore


class Gitlabciyml(RESTObject):
    _id_attr = "name"


class GitlabciymlManager(RetrieveMixin, RESTManager):
    _path = "/templates/gitlab_ci_ymls"
    _obj_cls = Gitlabciyml


class GroupAccessRequest(AccessRequestMixin, ObjectDeleteMixin, RESTObject):
    pass


class GroupAccessRequestManager(ListMixin, CreateMixin, DeleteMixin, RESTManager):
    _path = "/groups/%(group_id)s/access_requests"
    _obj_cls = GroupAccessRequest
    _from_parent_attrs = {"group_id": "id"}


class GroupBadge(SaveMixin, ObjectDeleteMixin, RESTObject):
    pass


class GroupBadgeManager(BadgeRenderMixin, CRUDMixin, RESTManager):
    _path = "/groups/%(group_id)s/badges"
    _obj_cls = GroupBadge
    _from_parent_attrs = {"group_id": "id"}
    _create_attrs = (("link_url", "image_url"), tuple())
    _update_attrs = (tuple(), ("link_url", "image_url"))


class GroupBoardList(SaveMixin, ObjectDeleteMixin, RESTObject):
    pass


class GroupBoardListManager(CRUDMixin, RESTManager):
    _path = "/groups/%(group_id)s/boards/%(board_id)s/lists"
    _obj_cls = GroupBoardList
    _from_parent_attrs = {"group_id": "group_id", "board_id": "id"}
    _create_attrs = (("label_id",), tuple())
    _update_attrs = (("position",), tuple())


class GroupBoard(SaveMixin, ObjectDeleteMixin, RESTObject):
    _managers = (("lists", "GroupBoardListManager"),)


class GroupBoardManager(CRUDMixin, RESTManager):
    _path = "/groups/%(group_id)s/boards"
    _obj_cls = GroupBoard
    _from_parent_attrs = {"group_id": "id"}
    _create_attrs = (("name",), tuple())


class GroupCluster(SaveMixin, ObjectDeleteMixin, RESTObject):
    pass


class GroupClusterManager(CRUDMixin, RESTManager):
    _path = "/groups/%(group_id)s/clusters"
    _obj_cls = GroupCluster
    _from_parent_attrs = {"group_id": "id"}
    _create_attrs = (
        ("name", "platform_kubernetes_attributes"),
        ("domain", "enabled", "managed", "environment_scope"),
    )
    _update_attrs = (
        tuple(),
        (
            "name",
            "domain",
            "management_project_id",
            "platform_kubernetes_attributes",
            "environment_scope",
        ),
    )

    @exc.on_http_error(exc.GitlabStopError)
    def create(self, data, **kwargs):
        """Create a new object.

        Args:
            data (dict): Parameters to send to the server to create the
                         resource
            **kwargs: Extra options to send to the server (e.g. sudo or
                      'ref_name', 'stage', 'name', 'all')

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabCreateError: If the server cannot perform the request

        Returns:
            RESTObject: A new instance of the manage object class build with
                        the data sent by the server
        """
        path = "%s/user" % (self.path)
        return CreateMixin.create(self, data, path=path, **kwargs)


class GroupCustomAttribute(ObjectDeleteMixin, RESTObject):
    _id_attr = "key"


class GroupCustomAttributeManager(RetrieveMixin, SetMixin, DeleteMixin, RESTManager):
    _path = "/groups/%(group_id)s/custom_attributes"
    _obj_cls = GroupCustomAttribute
    _from_parent_attrs = {"group_id": "id"}


class GroupEpicIssue(ObjectDeleteMixin, SaveMixin, RESTObject):
    _id_attr = "epic_issue_id"

    def save(self, **kwargs):
        """Save the changes made to the object to the server.

        The object is updated to match what the server returns.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raise:
            GitlabAuthenticationError: If authentication is not correct
            GitlabUpdateError: If the server cannot perform the request
        """
        updated_data = self._get_updated_data()
        # Nothing to update. Server fails if sent an empty dict.
        if not updated_data:
            return

        # call the manager
        obj_id = self.get_id()
        self.manager.update(obj_id, updated_data, **kwargs)


class GroupEpicIssueManager(
    ListMixin, CreateMixin, UpdateMixin, DeleteMixin, RESTManager
):
    _path = "/groups/%(group_id)s/epics/%(epic_iid)s/issues"
    _obj_cls = GroupEpicIssue
    _from_parent_attrs = {"group_id": "group_id", "epic_iid": "iid"}
    _create_attrs = (("issue_id",), tuple())
    _update_attrs = (tuple(), ("move_before_id", "move_after_id"))

    @exc.on_http_error(exc.GitlabCreateError)
    def create(self, data, **kwargs):
        """Create a new object.

        Args:
            data (dict): Parameters to send to the server to create the
                         resource
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabCreateError: If the server cannot perform the request

        Returns:
            RESTObject: A new instance of the manage object class build with
                        the data sent by the server
        """
        CreateMixin._check_missing_create_attrs(self, data)
        path = "%s/%s" % (self.path, data.pop("issue_id"))
        server_data = self.gitlab.http_post(path, **kwargs)
        # The epic_issue_id attribute doesn't exist when creating the resource,
        # but is used everywhere elese. Let's create it to be consistent client
        # side
        server_data["epic_issue_id"] = server_data["id"]
        return self._obj_cls(self, server_data)


class GroupEpicResourceLabelEvent(RESTObject):
    pass


class GroupEpicResourceLabelEventManager(RetrieveMixin, RESTManager):
    _path = "/groups/%(group_id)s/epics/%(epic_id)s/resource_label_events"
    _obj_cls = GroupEpicResourceLabelEvent
    _from_parent_attrs = {"group_id": "group_id", "epic_id": "id"}


class GroupEpic(ObjectDeleteMixin, SaveMixin, RESTObject):
    _id_attr = "iid"
    _managers = (
        ("issues", "GroupEpicIssueManager"),
        ("resourcelabelevents", "GroupEpicResourceLabelEventManager"),
    )


class GroupEpicManager(CRUDMixin, RESTManager):
    _path = "/groups/%(group_id)s/epics"
    _obj_cls = GroupEpic
    _from_parent_attrs = {"group_id": "id"}
    _list_filters = ("author_id", "labels", "order_by", "sort", "search")
    _create_attrs = (("title",), ("labels", "description", "start_date", "end_date"))
    _update_attrs = (
        tuple(),
        ("title", "labels", "description", "start_date", "end_date"),
    )
    _types = {"labels": types.ListAttribute}


class GroupIssue(RESTObject):
    pass


class GroupIssueManager(ListMixin, RESTManager):
    _path = "/groups/%(group_id)s/issues"
    _obj_cls = GroupIssue
    _from_parent_attrs = {"group_id": "id"}
    _list_filters = (
        "state",
        "labels",
        "milestone",
        "order_by",
        "sort",
        "iids",
        "author_id",
        "assignee_id",
        "my_reaction_emoji",
        "search",
        "created_after",
        "created_before",
        "updated_after",
        "updated_before",
    )
    _types = {"labels": types.ListAttribute}


class GroupLabel(SubscribableMixin, SaveMixin, ObjectDeleteMixin, RESTObject):
    _id_attr = "name"

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


class GroupLabelManager(ListMixin, CreateMixin, UpdateMixin, DeleteMixin, RESTManager):
    _path = "/groups/%(group_id)s/labels"
    _obj_cls = GroupLabel
    _from_parent_attrs = {"group_id": "id"}
    _create_attrs = (("name", "color"), ("description", "priority"))
    _update_attrs = (("name",), ("new_name", "color", "description", "priority"))

    # Update without ID.
    def update(self, name, new_data=None, **kwargs):
        """Update a Label on the server.

        Args:
            name: The name of the label
            **kwargs: Extra options to send to the server (e.g. sudo)
        """
        new_data = new_data or {}
        if name:
            new_data["name"] = name
        return super().update(id=None, new_data=new_data, **kwargs)

    # Delete without ID.
    @exc.on_http_error(exc.GitlabDeleteError)
    def delete(self, name, **kwargs):
        """Delete a Label on the server.

        Args:
            name: The name of the label
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabDeleteError: If the server cannot perform the request
        """
        self.gitlab.http_delete(self.path, query_data={"name": name}, **kwargs)


class GroupMember(SaveMixin, ObjectDeleteMixin, RESTObject):
    _short_print_attr = "username"


class GroupMemberManager(CRUDMixin, RESTManager):
    _path = "/groups/%(group_id)s/members"
    _obj_cls = GroupMember
    _from_parent_attrs = {"group_id": "id"}
    _create_attrs = (("access_level", "user_id"), ("expires_at",))
    _update_attrs = (("access_level",), ("expires_at",))

    @cli.register_custom_action("GroupMemberManager")
    @exc.on_http_error(exc.GitlabListError)
    def all(self, **kwargs):
        """List all the members, included inherited ones.

        Args:
            all (bool): If True, return all the items, without pagination
            per_page (int): Number of items to retrieve per request
            page (int): ID of the page to return (starts with page 1)
            as_list (bool): If set to False and no pagination option is
                defined, return a generator instead of a list
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabListError: If the list could not be retrieved

        Returns:
            RESTObjectList: The list of members
        """

        path = "%s/all" % self.path
        obj = self.gitlab.http_list(path, **kwargs)
        return [self._obj_cls(self, item) for item in obj]


class GroupMergeRequest(RESTObject):
    pass


class GroupMergeRequestManager(ListMixin, RESTManager):
    _path = "/groups/%(group_id)s/merge_requests"
    _obj_cls = GroupMergeRequest
    _from_parent_attrs = {"group_id": "id"}
    _list_filters = (
        "state",
        "order_by",
        "sort",
        "milestone",
        "view",
        "labels",
        "created_after",
        "created_before",
        "updated_after",
        "updated_before",
        "scope",
        "author_id",
        "assignee_id",
        "my_reaction_emoji",
        "source_branch",
        "target_branch",
        "search",
    )
    _types = {"labels": types.ListAttribute}


class GroupMilestone(SaveMixin, ObjectDeleteMixin, RESTObject):
    _short_print_attr = "title"

    @cli.register_custom_action("GroupMilestone")
    @exc.on_http_error(exc.GitlabListError)
    def issues(self, **kwargs):
        """List issues related to this milestone.

        Args:
            all (bool): If True, return all the items, without pagination
            per_page (int): Number of items to retrieve per request
            page (int): ID of the page to return (starts with page 1)
            as_list (bool): If set to False and no pagination option is
                defined, return a generator instead of a list
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabListError: If the list could not be retrieved

        Returns:
            RESTObjectList: The list of issues
        """

        path = "%s/%s/issues" % (self.manager.path, self.get_id())
        data_list = self.manager.gitlab.http_list(path, as_list=False, **kwargs)
        manager = GroupIssueManager(self.manager.gitlab, parent=self.manager._parent)
        # FIXME(gpocentek): the computed manager path is not correct
        return RESTObjectList(manager, GroupIssue, data_list)

    @cli.register_custom_action("GroupMilestone")
    @exc.on_http_error(exc.GitlabListError)
    def merge_requests(self, **kwargs):
        """List the merge requests related to this milestone.

        Args:
            all (bool): If True, return all the items, without pagination
            per_page (int): Number of items to retrieve per request
            page (int): ID of the page to return (starts with page 1)
            as_list (bool): If set to False and no pagination option is
                defined, return a generator instead of a list
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabListError: If the list could not be retrieved

        Returns:
            RESTObjectList: The list of merge requests
        """
        path = "%s/%s/merge_requests" % (self.manager.path, self.get_id())
        data_list = self.manager.gitlab.http_list(path, as_list=False, **kwargs)
        manager = GroupIssueManager(self.manager.gitlab, parent=self.manager._parent)
        # FIXME(gpocentek): the computed manager path is not correct
        return RESTObjectList(manager, GroupMergeRequest, data_list)


class GroupMilestoneManager(CRUDMixin, RESTManager):
    _path = "/groups/%(group_id)s/milestones"
    _obj_cls = GroupMilestone
    _from_parent_attrs = {"group_id": "id"}
    _create_attrs = (("title",), ("description", "due_date", "start_date"))
    _update_attrs = (
        tuple(),
        ("title", "description", "due_date", "start_date", "state_event"),
    )
    _list_filters = ("iids", "state", "search")


class GroupNotificationSettings(NotificationSettings):
    pass


class GroupNotificationSettingsManager(NotificationSettingsManager):
    _path = "/groups/%(group_id)s/notification_settings"
    _obj_cls = GroupNotificationSettings
    _from_parent_attrs = {"group_id": "id"}


class GroupProject(RESTObject):
    pass


class GroupProjectManager(ListMixin, RESTManager):
    _path = "/groups/%(group_id)s/projects"
    _obj_cls = GroupProject
    _from_parent_attrs = {"group_id": "id"}
    _list_filters = (
        "archived",
        "visibility",
        "order_by",
        "sort",
        "search",
        "ci_enabled_first",
        "simple",
        "owned",
        "starred",
        "with_custom_attributes",
        "include_subgroups",
    )


class GroupSubgroup(RESTObject):
    pass


class GroupSubgroupManager(ListMixin, RESTManager):
    _path = "/groups/%(group_id)s/subgroups"
    _obj_cls = GroupSubgroup
    _from_parent_attrs = {"group_id": "id"}
    _list_filters = (
        "skip_groups",
        "all_available",
        "search",
        "order_by",
        "sort",
        "statistics",
        "owned",
        "with_custom_attributes",
    )


class GroupVariable(SaveMixin, ObjectDeleteMixin, RESTObject):
    _id_attr = "key"


class GroupVariableManager(CRUDMixin, RESTManager):
    _path = "/groups/%(group_id)s/variables"
    _obj_cls = GroupVariable
    _from_parent_attrs = {"group_id": "id"}
    _create_attrs = (("key", "value"), ("protected", "variable_type"))
    _update_attrs = (("key", "value"), ("protected", "variable_type"))


class Group(SaveMixin, ObjectDeleteMixin, RESTObject):
    _short_print_attr = "name"
    _managers = (
        ("accessrequests", "GroupAccessRequestManager"),
        ("badges", "GroupBadgeManager"),
        ("boards", "GroupBoardManager"),
        ("customattributes", "GroupCustomAttributeManager"),
        ("epics", "GroupEpicManager"),
        ("issues", "GroupIssueManager"),
        ("labels", "GroupLabelManager"),
        ("members", "GroupMemberManager"),
        ("mergerequests", "GroupMergeRequestManager"),
        ("milestones", "GroupMilestoneManager"),
        ("notificationsettings", "GroupNotificationSettingsManager"),
        ("projects", "GroupProjectManager"),
        ("subgroups", "GroupSubgroupManager"),
        ("variables", "GroupVariableManager"),
        ("clusters", "GroupClusterManager"),
    )

    @cli.register_custom_action("Group", ("to_project_id",))
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
        path = "/groups/%s/projects/%s" % (self.id, to_project_id)
        self.manager.gitlab.http_post(path, **kwargs)

    @cli.register_custom_action("Group", ("scope", "search"))
    @exc.on_http_error(exc.GitlabSearchError)
    def search(self, scope, search, **kwargs):
        """Search the group resources matching the provided string.'

        Args:
            scope (str): Scope of the search
            search (str): Search string
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabSearchError: If the server failed to perform the request

        Returns:
            GitlabList: A list of dicts describing the resources found.
        """
        data = {"scope": scope, "search": search}
        path = "/groups/%s/search" % self.get_id()
        return self.manager.gitlab.http_list(path, query_data=data, **kwargs)

    @cli.register_custom_action("Group", ("cn", "group_access", "provider"))
    @exc.on_http_error(exc.GitlabCreateError)
    def add_ldap_group_link(self, cn, group_access, provider, **kwargs):
        """Add an LDAP group link.

        Args:
            cn (str): CN of the LDAP group
            group_access (int): Minimum access level for members of the LDAP
                group
            provider (str): LDAP provider for the LDAP group
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabCreateError: If the server cannot perform the request
        """
        path = "/groups/%s/ldap_group_links" % self.get_id()
        data = {"cn": cn, "group_access": group_access, "provider": provider}
        self.manager.gitlab.http_post(path, post_data=data, **kwargs)

    @cli.register_custom_action("Group", ("cn",), ("provider",))
    @exc.on_http_error(exc.GitlabDeleteError)
    def delete_ldap_group_link(self, cn, provider=None, **kwargs):
        """Delete an LDAP group link.

        Args:
            cn (str): CN of the LDAP group
            provider (str): LDAP provider for the LDAP group
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabDeleteError: If the server cannot perform the request
        """
        path = "/groups/%s/ldap_group_links" % self.get_id()
        if provider is not None:
            path += "/%s" % provider
        path += "/%s" % cn
        self.manager.gitlab.http_delete(path)

    @cli.register_custom_action("Group")
    @exc.on_http_error(exc.GitlabCreateError)
    def ldap_sync(self, **kwargs):
        """Sync LDAP groups.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabCreateError: If the server cannot perform the request
        """
        path = "/groups/%s/ldap_sync" % self.get_id()
        self.manager.gitlab.http_post(path, **kwargs)


class GroupManager(CRUDMixin, RESTManager):
    _path = "/groups"
    _obj_cls = Group
    _list_filters = (
        "skip_groups",
        "all_available",
        "search",
        "order_by",
        "sort",
        "statistics",
        "owned",
        "with_custom_attributes",
    )
    _create_attrs = (
        ("name", "path"),
        (
            "description",
            "visibility",
            "parent_id",
            "lfs_enabled",
            "request_access_enabled",
        ),
    )
    _update_attrs = (
        tuple(),
        (
            "name",
            "path",
            "description",
            "visibility",
            "lfs_enabled",
            "request_access_enabled",
        ),
    )


class Hook(ObjectDeleteMixin, RESTObject):
    _url = "/hooks"
    _short_print_attr = "url"


class HookManager(NoUpdateMixin, RESTManager):
    _path = "/hooks"
    _obj_cls = Hook
    _create_attrs = (("url",), tuple())


class Issue(RESTObject):
    _url = "/issues"
    _short_print_attr = "title"


class IssueManager(ListMixin, RESTManager):
    _path = "/issues"
    _obj_cls = Issue
    _list_filters = (
        "state",
        "labels",
        "milestone",
        "scope",
        "author_id",
        "assignee_id",
        "my_reaction_emoji",
        "iids",
        "order_by",
        "sort",
        "search",
        "created_after",
        "created_before",
        "updated_after",
        "updated_before",
    )
    _types = {"labels": types.ListAttribute}


class LDAPGroup(RESTObject):
    _id_attr = None


class LDAPGroupManager(RESTManager):
    _path = "/ldap/groups"
    _obj_cls = LDAPGroup
    _list_filters = ("search", "provider")

    @exc.on_http_error(exc.GitlabListError)
    def list(self, **kwargs):
        """Retrieve a list of objects.

        Args:
            all (bool): If True, return all the items, without pagination
            per_page (int): Number of items to retrieve per request
            page (int): ID of the page to return (starts with page 1)
            as_list (bool): If set to False and no pagination option is
                defined, return a generator instead of a list
            **kwargs: Extra options to send to the server (e.g. sudo)

        Returns:
            list: The list of objects, or a generator if `as_list` is False

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabListError: If the server cannot perform the request
        """
        data = kwargs.copy()
        if self.gitlab.per_page:
            data.setdefault("per_page", self.gitlab.per_page)

        if "provider" in data:
            path = "/ldap/%s/groups" % data["provider"]
        else:
            path = self._path

        obj = self.gitlab.http_list(path, **data)
        if isinstance(obj, list):
            return [self._obj_cls(self, item) for item in obj]
        else:
            return base.RESTObjectList(self, self._obj_cls, obj)


class License(RESTObject):
    _id_attr = "key"


class LicenseManager(RetrieveMixin, RESTManager):
    _path = "/templates/licenses"
    _obj_cls = License
    _list_filters = ("popular",)
    _optional_get_attrs = ("project", "fullname")


class MergeRequest(RESTObject):
    pass


class MergeRequestManager(ListMixin, RESTManager):
    _path = "/merge_requests"
    _obj_cls = MergeRequest
    _from_parent_attrs = {"group_id": "id"}
    _list_filters = (
        "state",
        "order_by",
        "sort",
        "milestone",
        "view",
        "labels",
        "created_after",
        "created_before",
        "updated_after",
        "updated_before",
        "scope",
        "author_id",
        "assignee_id",
        "my_reaction_emoji",
        "source_branch",
        "target_branch",
        "search",
    )
    _types = {"labels": types.ListAttribute}


class Snippet(UserAgentDetailMixin, SaveMixin, ObjectDeleteMixin, RESTObject):
    _short_print_attr = "title"

    @cli.register_custom_action("Snippet")
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
        path = "/snippets/%s/raw" % self.get_id()
        result = self.manager.gitlab.http_get(
            path, streamed=streamed, raw=True, **kwargs
        )
        return utils.response_content(result, streamed, action, chunk_size)


class SnippetManager(CRUDMixin, RESTManager):
    _path = "/snippets"
    _obj_cls = Snippet
    _create_attrs = (("title", "file_name", "content"), ("lifetime", "visibility"))
    _update_attrs = (tuple(), ("title", "file_name", "content", "visibility"))

    @cli.register_custom_action("SnippetManager")
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
        return self.list(path="/snippets/public", **kwargs)


class Namespace(RESTObject):
    pass


class NamespaceManager(RetrieveMixin, RESTManager):
    _path = "/namespaces"
    _obj_cls = Namespace
    _list_filters = ("search",)


class PagesDomain(RESTObject):
    _id_attr = "domain"


class PagesDomainManager(ListMixin, RESTManager):
    _path = "/pages/domains"
    _obj_cls = PagesDomain


class ProjectRegistryRepository(ObjectDeleteMixin, RESTObject):
    _managers = (("tags", "ProjectRegistryTagManager"),)


class ProjectRegistryRepositoryManager(DeleteMixin, ListMixin, RESTManager):
    _path = "/projects/%(project_id)s/registry/repositories"
    _obj_cls = ProjectRegistryRepository
    _from_parent_attrs = {"project_id": "id"}


class ProjectRegistryTag(ObjectDeleteMixin, RESTObject):
    _id_attr = "name"


class ProjectRegistryTagManager(DeleteMixin, RetrieveMixin, RESTManager):
    _obj_cls = ProjectRegistryTag
    _from_parent_attrs = {"project_id": "project_id", "repository_id": "id"}
    _path = "/projects/%(project_id)s/registry/repositories/%(repository_id)s/tags"

    @cli.register_custom_action(
        "ProjectRegistryTagManager", optional=("name_regex", "keep_n", "older_than")
    )
    @exc.on_http_error(exc.GitlabDeleteError)
    def delete_in_bulk(self, name_regex=".*", **kwargs):
        """Delete Tag in bulk

        Args:
            name_regex (string): The regex of the name to delete. To delete all
                                 tags specify .*.
            keep_n (integer):    The amount of latest tags of given name to keep.
            older_than (string): Tags to delete that are older than the given time,
                                 written in human readable form 1h, 1d, 1month.
            **kwargs:            Extra options to send to the server (e.g. sudo)
        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabDeleteError: If the server cannot perform the request
        """
        valid_attrs = ["keep_n", "older_than"]
        data = {"name_regex": name_regex}
        data.update({k: v for k, v in kwargs.items() if k in valid_attrs})
        self.gitlab.http_delete(self.path, query_data=data, **kwargs)


class ProjectBoardList(SaveMixin, ObjectDeleteMixin, RESTObject):
    pass


class ProjectBoardListManager(CRUDMixin, RESTManager):
    _path = "/projects/%(project_id)s/boards/%(board_id)s/lists"
    _obj_cls = ProjectBoardList
    _from_parent_attrs = {"project_id": "project_id", "board_id": "id"}
    _create_attrs = (("label_id",), tuple())
    _update_attrs = (("position",), tuple())


class ProjectBoard(SaveMixin, ObjectDeleteMixin, RESTObject):
    _managers = (("lists", "ProjectBoardListManager"),)


class ProjectBoardManager(CRUDMixin, RESTManager):
    _path = "/projects/%(project_id)s/boards"
    _obj_cls = ProjectBoard
    _from_parent_attrs = {"project_id": "id"}
    _create_attrs = (("name",), tuple())


class ProjectBranch(ObjectDeleteMixin, RESTObject):
    _id_attr = "name"

    @cli.register_custom_action(
        "ProjectBranch", tuple(), ("developers_can_push", "developers_can_merge")
    )
    @exc.on_http_error(exc.GitlabProtectError)
    def protect(self, developers_can_push=False, developers_can_merge=False, **kwargs):
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
        id = self.get_id().replace("/", "%2F")
        path = "%s/%s/protect" % (self.manager.path, id)
        post_data = {
            "developers_can_push": developers_can_push,
            "developers_can_merge": developers_can_merge,
        }
        self.manager.gitlab.http_put(path, post_data=post_data, **kwargs)
        self._attrs["protected"] = True

    @cli.register_custom_action("ProjectBranch")
    @exc.on_http_error(exc.GitlabProtectError)
    def unprotect(self, **kwargs):
        """Unprotect the branch.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabProtectError: If the branch could not be unprotected
        """
        id = self.get_id().replace("/", "%2F")
        path = "%s/%s/unprotect" % (self.manager.path, id)
        self.manager.gitlab.http_put(path, **kwargs)
        self._attrs["protected"] = False


class ProjectBranchManager(NoUpdateMixin, RESTManager):
    _path = "/projects/%(project_id)s/repository/branches"
    _obj_cls = ProjectBranch
    _from_parent_attrs = {"project_id": "id"}
    _create_attrs = (("branch", "ref"), tuple())


class ProjectCluster(SaveMixin, ObjectDeleteMixin, RESTObject):
    pass


class ProjectClusterManager(CRUDMixin, RESTManager):
    _path = "/projects/%(project_id)s/clusters"
    _obj_cls = ProjectCluster
    _from_parent_attrs = {"project_id": "id"}
    _create_attrs = (
        ("name", "platform_kubernetes_attributes"),
        ("domain", "enabled", "managed", "environment_scope"),
    )
    _update_attrs = (
        tuple(),
        (
            "name",
            "domain",
            "management_project_id",
            "platform_kubernetes_attributes",
            "environment_scope",
        ),
    )

    @exc.on_http_error(exc.GitlabStopError)
    def create(self, data, **kwargs):
        """Create a new object.

        Args:
            data (dict): Parameters to send to the server to create the
                         resource
            **kwargs: Extra options to send to the server (e.g. sudo or
                      'ref_name', 'stage', 'name', 'all')

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabCreateError: If the server cannot perform the request

        Returns:
            RESTObject: A new instance of the manage object class build with
                        the data sent by the server
        """
        path = "%s/user" % (self.path)
        return CreateMixin.create(self, data, path=path, **kwargs)


class ProjectCustomAttribute(ObjectDeleteMixin, RESTObject):
    _id_attr = "key"


class ProjectCustomAttributeManager(RetrieveMixin, SetMixin, DeleteMixin, RESTManager):
    _path = "/projects/%(project_id)s/custom_attributes"
    _obj_cls = ProjectCustomAttribute
    _from_parent_attrs = {"project_id": "id"}


class ProjectJob(RESTObject, RefreshMixin):
    @cli.register_custom_action("ProjectJob")
    @exc.on_http_error(exc.GitlabJobCancelError)
    def cancel(self, **kwargs):
        """Cancel the job.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabJobCancelError: If the job could not be canceled
        """
        path = "%s/%s/cancel" % (self.manager.path, self.get_id())
        self.manager.gitlab.http_post(path)

    @cli.register_custom_action("ProjectJob")
    @exc.on_http_error(exc.GitlabJobRetryError)
    def retry(self, **kwargs):
        """Retry the job.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabJobRetryError: If the job could not be retried
        """
        path = "%s/%s/retry" % (self.manager.path, self.get_id())
        self.manager.gitlab.http_post(path)

    @cli.register_custom_action("ProjectJob")
    @exc.on_http_error(exc.GitlabJobPlayError)
    def play(self, **kwargs):
        """Trigger a job explicitly.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabJobPlayError: If the job could not be triggered
        """
        path = "%s/%s/play" % (self.manager.path, self.get_id())
        self.manager.gitlab.http_post(path)

    @cli.register_custom_action("ProjectJob")
    @exc.on_http_error(exc.GitlabJobEraseError)
    def erase(self, **kwargs):
        """Erase the job (remove job artifacts and trace).

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabJobEraseError: If the job could not be erased
        """
        path = "%s/%s/erase" % (self.manager.path, self.get_id())
        self.manager.gitlab.http_post(path)

    @cli.register_custom_action("ProjectJob")
    @exc.on_http_error(exc.GitlabCreateError)
    def keep_artifacts(self, **kwargs):
        """Prevent artifacts from being deleted when expiration is set.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabCreateError: If the request could not be performed
        """
        path = "%s/%s/artifacts/keep" % (self.manager.path, self.get_id())
        self.manager.gitlab.http_post(path)

    @cli.register_custom_action("ProjectJob")
    @exc.on_http_error(exc.GitlabCreateError)
    def delete_artifacts(self, **kwargs):
        """Delete artifacts of a job.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabDeleteError: If the request could not be performed
        """
        path = "%s/%s/artifacts" % (self.manager.path, self.get_id())
        self.manager.gitlab.http_delete(path)

    @cli.register_custom_action("ProjectJob")
    @exc.on_http_error(exc.GitlabGetError)
    def artifacts(self, streamed=False, action=None, chunk_size=1024, **kwargs):
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
        path = "%s/%s/artifacts" % (self.manager.path, self.get_id())
        result = self.manager.gitlab.http_get(
            path, streamed=streamed, raw=True, **kwargs
        )
        return utils.response_content(result, streamed, action, chunk_size)

    @cli.register_custom_action("ProjectJob")
    @exc.on_http_error(exc.GitlabGetError)
    def artifact(self, path, streamed=False, action=None, chunk_size=1024, **kwargs):
        """Get a single artifact file from within the job's artifacts archive.

        Args:
            path (str): Path of the artifact
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
        path = "%s/%s/artifacts/%s" % (self.manager.path, self.get_id(), path)
        result = self.manager.gitlab.http_get(
            path, streamed=streamed, raw=True, **kwargs
        )
        return utils.response_content(result, streamed, action, chunk_size)

    @cli.register_custom_action("ProjectJob")
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
        path = "%s/%s/trace" % (self.manager.path, self.get_id())
        result = self.manager.gitlab.http_get(
            path, streamed=streamed, raw=True, **kwargs
        )
        return utils.response_content(result, streamed, action, chunk_size)


class ProjectJobManager(RetrieveMixin, RESTManager):
    _path = "/projects/%(project_id)s/jobs"
    _obj_cls = ProjectJob
    _from_parent_attrs = {"project_id": "id"}


class ProjectCommitStatus(RESTObject, RefreshMixin):
    pass


class ProjectCommitStatusManager(ListMixin, CreateMixin, RESTManager):
    _path = "/projects/%(project_id)s/repository/commits/%(commit_id)s" "/statuses"
    _obj_cls = ProjectCommitStatus
    _from_parent_attrs = {"project_id": "project_id", "commit_id": "id"}
    _create_attrs = (
        ("state",),
        ("description", "name", "context", "ref", "target_url", "coverage"),
    )

    @exc.on_http_error(exc.GitlabCreateError)
    def create(self, data, **kwargs):
        """Create a new object.

        Args:
            data (dict): Parameters to send to the server to create the
                         resource
            **kwargs: Extra options to send to the server (e.g. sudo or
                      'ref_name', 'stage', 'name', 'all')

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabCreateError: If the server cannot perform the request

        Returns:
            RESTObject: A new instance of the manage object class build with
                        the data sent by the server
        """
        # project_id and commit_id are in the data dict when using the CLI, but
        # they are missing when using only the API
        # See #511
        base_path = "/projects/%(project_id)s/statuses/%(commit_id)s"
        if "project_id" in data and "commit_id" in data:
            path = base_path % data
        else:
            path = self._compute_path(base_path)
        return CreateMixin.create(self, data, path=path, **kwargs)


class ProjectCommitComment(RESTObject):
    _id_attr = None
    _short_print_attr = "note"


class ProjectCommitCommentManager(ListMixin, CreateMixin, RESTManager):
    _path = "/projects/%(project_id)s/repository/commits/%(commit_id)s" "/comments"
    _obj_cls = ProjectCommitComment
    _from_parent_attrs = {"project_id": "project_id", "commit_id": "id"}
    _create_attrs = (("note",), ("path", "line", "line_type"))


class ProjectCommitDiscussionNote(SaveMixin, ObjectDeleteMixin, RESTObject):
    pass


class ProjectCommitDiscussionNoteManager(
    GetMixin, CreateMixin, UpdateMixin, DeleteMixin, RESTManager
):
    _path = (
        "/projects/%(project_id)s/repository/commits/%(commit_id)s/"
        "discussions/%(discussion_id)s/notes"
    )
    _obj_cls = ProjectCommitDiscussionNote
    _from_parent_attrs = {
        "project_id": "project_id",
        "commit_id": "commit_id",
        "discussion_id": "id",
    }
    _create_attrs = (("body",), ("created_at", "position"))
    _update_attrs = (("body",), tuple())


class ProjectCommitDiscussion(RESTObject):
    _managers = (("notes", "ProjectCommitDiscussionNoteManager"),)


class ProjectCommitDiscussionManager(RetrieveMixin, CreateMixin, RESTManager):
    _path = "/projects/%(project_id)s/repository/commits/%(commit_id)s/" "discussions"
    _obj_cls = ProjectCommitDiscussion
    _from_parent_attrs = {"project_id": "project_id", "commit_id": "id"}
    _create_attrs = (("body",), ("created_at",))


class ProjectCommit(RESTObject):
    _short_print_attr = "title"
    _managers = (
        ("comments", "ProjectCommitCommentManager"),
        ("discussions", "ProjectCommitDiscussionManager"),
        ("statuses", "ProjectCommitStatusManager"),
    )

    @cli.register_custom_action("ProjectCommit")
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
        path = "%s/%s/diff" % (self.manager.path, self.get_id())
        return self.manager.gitlab.http_get(path, **kwargs)

    @cli.register_custom_action("ProjectCommit", ("branch",))
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
        path = "%s/%s/cherry_pick" % (self.manager.path, self.get_id())
        post_data = {"branch": branch}
        self.manager.gitlab.http_post(path, post_data=post_data, **kwargs)

    @cli.register_custom_action("ProjectCommit", optional=("type",))
    @exc.on_http_error(exc.GitlabGetError)
    def refs(self, type="all", **kwargs):
        """List the references the commit is pushed to.

        Args:
            type (str): The scope of references ('branch', 'tag' or 'all')
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabGetError: If the references could not be retrieved

        Returns:
            list: The references the commit is pushed to.
        """
        path = "%s/%s/refs" % (self.manager.path, self.get_id())
        data = {"type": type}
        return self.manager.gitlab.http_get(path, query_data=data, **kwargs)

    @cli.register_custom_action("ProjectCommit")
    @exc.on_http_error(exc.GitlabGetError)
    def merge_requests(self, **kwargs):
        """List the merge requests related to the commit.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabGetError: If the references could not be retrieved

        Returns:
            list: The merge requests related to the commit.
        """
        path = "%s/%s/merge_requests" % (self.manager.path, self.get_id())
        return self.manager.gitlab.http_get(path, **kwargs)


class ProjectCommitManager(RetrieveMixin, CreateMixin, RESTManager):
    _path = "/projects/%(project_id)s/repository/commits"
    _obj_cls = ProjectCommit
    _from_parent_attrs = {"project_id": "id"}
    _create_attrs = (
        ("branch", "commit_message", "actions"),
        ("author_email", "author_name"),
    )


class ProjectEnvironment(SaveMixin, ObjectDeleteMixin, RESTObject):
    @cli.register_custom_action("ProjectEnvironment")
    @exc.on_http_error(exc.GitlabStopError)
    def stop(self, **kwargs):
        """Stop the environment.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabStopError: If the operation failed
        """
        path = "%s/%s/stop" % (self.manager.path, self.get_id())
        self.manager.gitlab.http_post(path, **kwargs)


class ProjectEnvironmentManager(
    RetrieveMixin, CreateMixin, UpdateMixin, DeleteMixin, RESTManager
):
    _path = "/projects/%(project_id)s/environments"
    _obj_cls = ProjectEnvironment
    _from_parent_attrs = {"project_id": "id"}
    _create_attrs = (("name",), ("external_url",))
    _update_attrs = (tuple(), ("name", "external_url"))


class ProjectKey(SaveMixin, ObjectDeleteMixin, RESTObject):
    pass


class ProjectKeyManager(CRUDMixin, RESTManager):
    _path = "/projects/%(project_id)s/deploy_keys"
    _obj_cls = ProjectKey
    _from_parent_attrs = {"project_id": "id"}
    _create_attrs = (("title", "key"), ("can_push",))
    _update_attrs = (tuple(), ("title", "can_push"))

    @cli.register_custom_action("ProjectKeyManager", ("key_id",))
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
        path = "%s/%s/enable" % (self.path, key_id)
        self.gitlab.http_post(path, **kwargs)


class ProjectBadge(SaveMixin, ObjectDeleteMixin, RESTObject):
    pass


class ProjectBadgeManager(BadgeRenderMixin, CRUDMixin, RESTManager):
    _path = "/projects/%(project_id)s/badges"
    _obj_cls = ProjectBadge
    _from_parent_attrs = {"project_id": "id"}
    _create_attrs = (("link_url", "image_url"), tuple())
    _update_attrs = (tuple(), ("link_url", "image_url"))


class ProjectEvent(Event):
    pass


class ProjectEventManager(EventManager):
    _path = "/projects/%(project_id)s/events"
    _obj_cls = ProjectEvent
    _from_parent_attrs = {"project_id": "id"}


class ProjectFork(RESTObject):
    pass


class ProjectForkManager(CreateMixin, ListMixin, RESTManager):
    _path = "/projects/%(project_id)s/forks"
    _obj_cls = ProjectFork
    _from_parent_attrs = {"project_id": "id"}
    _list_filters = (
        "archived",
        "visibility",
        "order_by",
        "sort",
        "search",
        "simple",
        "owned",
        "membership",
        "starred",
        "statistics",
        "with_custom_attributes",
        "with_issues_enabled",
        "with_merge_requests_enabled",
    )
    _create_attrs = (tuple(), ("namespace",))

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


class ProjectHook(SaveMixin, ObjectDeleteMixin, RESTObject):
    _short_print_attr = "url"


class ProjectHookManager(CRUDMixin, RESTManager):
    _path = "/projects/%(project_id)s/hooks"
    _obj_cls = ProjectHook
    _from_parent_attrs = {"project_id": "id"}
    _create_attrs = (
        ("url",),
        (
            "push_events",
            "issues_events",
            "confidential_issues_events",
            "merge_requests_events",
            "tag_push_events",
            "note_events",
            "job_events",
            "pipeline_events",
            "wiki_page_events",
            "enable_ssl_verification",
            "token",
        ),
    )
    _update_attrs = (
        ("url",),
        (
            "push_events",
            "issues_events",
            "confidential_issues_events",
            "merge_requests_events",
            "tag_push_events",
            "note_events",
            "job_events",
            "pipeline_events",
            "wiki_events",
            "enable_ssl_verification",
            "token",
        ),
    )


class ProjectIssueAwardEmoji(ObjectDeleteMixin, RESTObject):
    pass


class ProjectIssueAwardEmojiManager(NoUpdateMixin, RESTManager):
    _path = "/projects/%(project_id)s/issues/%(issue_iid)s/award_emoji"
    _obj_cls = ProjectIssueAwardEmoji
    _from_parent_attrs = {"project_id": "project_id", "issue_iid": "iid"}
    _create_attrs = (("name",), tuple())


class ProjectIssueNoteAwardEmoji(ObjectDeleteMixin, RESTObject):
    pass


class ProjectIssueNoteAwardEmojiManager(NoUpdateMixin, RESTManager):
    _path = (
        "/projects/%(project_id)s/issues/%(issue_iid)s" "/notes/%(note_id)s/award_emoji"
    )
    _obj_cls = ProjectIssueNoteAwardEmoji
    _from_parent_attrs = {
        "project_id": "project_id",
        "issue_iid": "issue_iid",
        "note_id": "id",
    }
    _create_attrs = (("name",), tuple())


class ProjectIssueNote(SaveMixin, ObjectDeleteMixin, RESTObject):
    _managers = (("awardemojis", "ProjectIssueNoteAwardEmojiManager"),)


class ProjectIssueNoteManager(CRUDMixin, RESTManager):
    _path = "/projects/%(project_id)s/issues/%(issue_iid)s/notes"
    _obj_cls = ProjectIssueNote
    _from_parent_attrs = {"project_id": "project_id", "issue_iid": "iid"}
    _create_attrs = (("body",), ("created_at",))
    _update_attrs = (("body",), tuple())


class ProjectIssueDiscussionNote(SaveMixin, ObjectDeleteMixin, RESTObject):
    pass


class ProjectIssueDiscussionNoteManager(
    GetMixin, CreateMixin, UpdateMixin, DeleteMixin, RESTManager
):
    _path = (
        "/projects/%(project_id)s/issues/%(issue_iid)s/"
        "discussions/%(discussion_id)s/notes"
    )
    _obj_cls = ProjectIssueDiscussionNote
    _from_parent_attrs = {
        "project_id": "project_id",
        "issue_iid": "issue_iid",
        "discussion_id": "id",
    }
    _create_attrs = (("body",), ("created_at",))
    _update_attrs = (("body",), tuple())


class ProjectIssueDiscussion(RESTObject):
    _managers = (("notes", "ProjectIssueDiscussionNoteManager"),)


class ProjectIssueDiscussionManager(RetrieveMixin, CreateMixin, RESTManager):
    _path = "/projects/%(project_id)s/issues/%(issue_iid)s/discussions"
    _obj_cls = ProjectIssueDiscussion
    _from_parent_attrs = {"project_id": "project_id", "issue_iid": "iid"}
    _create_attrs = (("body",), ("created_at",))


class ProjectIssueLink(ObjectDeleteMixin, RESTObject):
    _id_attr = "issue_link_id"


class ProjectIssueLinkManager(ListMixin, CreateMixin, DeleteMixin, RESTManager):
    _path = "/projects/%(project_id)s/issues/%(issue_iid)s/links"
    _obj_cls = ProjectIssueLink
    _from_parent_attrs = {"project_id": "project_id", "issue_iid": "iid"}
    _create_attrs = (("target_project_id", "target_issue_iid"), tuple())

    @exc.on_http_error(exc.GitlabCreateError)
    def create(self, data, **kwargs):
        """Create a new object.

        Args:
            data (dict): parameters to send to the server to create the
                         resource
            **kwargs: Extra options to send to the server (e.g. sudo)

        Returns:
            RESTObject, RESTObject: The source and target issues

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabCreateError: If the server cannot perform the request
        """
        self._check_missing_create_attrs(data)
        server_data = self.gitlab.http_post(self.path, post_data=data, **kwargs)
        source_issue = ProjectIssue(self._parent.manager, server_data["source_issue"])
        target_issue = ProjectIssue(self._parent.manager, server_data["target_issue"])
        return source_issue, target_issue


class ProjectIssueResourceLabelEvent(RESTObject):
    pass


class ProjectIssueResourceLabelEventManager(RetrieveMixin, RESTManager):
    _path = "/projects/%(project_id)s/issues/%(issue_iid)s" "/resource_label_events"
    _obj_cls = ProjectIssueResourceLabelEvent
    _from_parent_attrs = {"project_id": "project_id", "issue_iid": "iid"}


class ProjectIssue(
    UserAgentDetailMixin,
    SubscribableMixin,
    TodoMixin,
    TimeTrackingMixin,
    ParticipantsMixin,
    SaveMixin,
    ObjectDeleteMixin,
    RESTObject,
):
    _short_print_attr = "title"
    _id_attr = "iid"
    _managers = (
        ("awardemojis", "ProjectIssueAwardEmojiManager"),
        ("discussions", "ProjectIssueDiscussionManager"),
        ("links", "ProjectIssueLinkManager"),
        ("notes", "ProjectIssueNoteManager"),
        ("resourcelabelevents", "ProjectIssueResourceLabelEventManager"),
    )

    @cli.register_custom_action("ProjectIssue", ("to_project_id",))
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
        path = "%s/%s/move" % (self.manager.path, self.get_id())
        data = {"to_project_id": to_project_id}
        server_data = self.manager.gitlab.http_post(path, post_data=data, **kwargs)
        self._update_attrs(server_data)

    @cli.register_custom_action("ProjectIssue")
    @exc.on_http_error(exc.GitlabGetError)
    def related_merge_requests(self, **kwargs):
        """List merge requests related to the issue.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabGetErrot: If the merge requests could not be retrieved

        Returns:
            list: The list of merge requests.
        """
        path = "%s/%s/related_merge_requests" % (self.manager.path, self.get_id())
        return self.manager.gitlab.http_get(path, **kwargs)

    @cli.register_custom_action("ProjectIssue")
    @exc.on_http_error(exc.GitlabGetError)
    def closed_by(self, **kwargs):
        """List merge requests that will close the issue when merged.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabGetErrot: If the merge requests could not be retrieved

        Returns:
            list: The list of merge requests.
        """
        path = "%s/%s/closed_by" % (self.manager.path, self.get_id())
        return self.manager.gitlab.http_get(path, **kwargs)


class ProjectIssueManager(CRUDMixin, RESTManager):
    _path = "/projects/%(project_id)s/issues"
    _obj_cls = ProjectIssue
    _from_parent_attrs = {"project_id": "id"}
    _list_filters = (
        "iids",
        "state",
        "labels",
        "milestone",
        "scope",
        "author_id",
        "assignee_id",
        "my_reaction_emoji",
        "order_by",
        "sort",
        "search",
        "created_after",
        "created_before",
        "updated_after",
        "updated_before",
    )
    _create_attrs = (
        ("title",),
        (
            "description",
            "confidential",
            "assignee_ids",
            "assignee_id",
            "milestone_id",
            "labels",
            "created_at",
            "due_date",
            "merge_request_to_resolve_discussions_of",
            "discussion_to_resolve",
        ),
    )
    _update_attrs = (
        tuple(),
        (
            "title",
            "description",
            "confidential",
            "assignee_ids",
            "assignee_id",
            "milestone_id",
            "labels",
            "state_event",
            "updated_at",
            "due_date",
            "discussion_locked",
        ),
    )
    _types = {"labels": types.ListAttribute}


class ProjectMember(SaveMixin, ObjectDeleteMixin, RESTObject):
    _short_print_attr = "username"


class ProjectMemberManager(CRUDMixin, RESTManager):
    _path = "/projects/%(project_id)s/members"
    _obj_cls = ProjectMember
    _from_parent_attrs = {"project_id": "id"}
    _create_attrs = (("access_level", "user_id"), ("expires_at",))
    _update_attrs = (("access_level",), ("expires_at",))

    @cli.register_custom_action("ProjectMemberManager")
    @exc.on_http_error(exc.GitlabListError)
    def all(self, **kwargs):
        """List all the members, included inherited ones.

        Args:
            all (bool): If True, return all the items, without pagination
            per_page (int): Number of items to retrieve per request
            page (int): ID of the page to return (starts with page 1)
            as_list (bool): If set to False and no pagination option is
                defined, return a generator instead of a list
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabListError: If the list could not be retrieved

        Returns:
            RESTObjectList: The list of members
        """

        path = "%s/all" % self.path
        obj = self.gitlab.http_list(path, **kwargs)
        return [self._obj_cls(self, item) for item in obj]


class ProjectNote(RESTObject):
    pass


class ProjectNoteManager(RetrieveMixin, RESTManager):
    _path = "/projects/%(project_id)s/notes"
    _obj_cls = ProjectNote
    _from_parent_attrs = {"project_id": "id"}
    _create_attrs = (("body",), tuple())


class ProjectNotificationSettings(NotificationSettings):
    pass


class ProjectNotificationSettingsManager(NotificationSettingsManager):
    _path = "/projects/%(project_id)s/notification_settings"
    _obj_cls = ProjectNotificationSettings
    _from_parent_attrs = {"project_id": "id"}


class ProjectPagesDomain(SaveMixin, ObjectDeleteMixin, RESTObject):
    _id_attr = "domain"


class ProjectPagesDomainManager(CRUDMixin, RESTManager):
    _path = "/projects/%(project_id)s/pages/domains"
    _obj_cls = ProjectPagesDomain
    _from_parent_attrs = {"project_id": "id"}
    _create_attrs = (("domain",), ("certificate", "key"))
    _update_attrs = (tuple(), ("certificate", "key"))


class ProjectRelease(RESTObject):
    _id_attr = "tag_name"


class ProjectReleaseManager(NoUpdateMixin, RESTManager):
    _path = "/projects/%(project_id)s/releases"
    _obj_cls = ProjectRelease
    _from_parent_attrs = {"project_id": "id"}
    _create_attrs = (("name", "tag_name", "description"), ("ref", "assets"))


class ProjectTag(ObjectDeleteMixin, RESTObject):
    _id_attr = "name"
    _short_print_attr = "name"

    @cli.register_custom_action("ProjectTag", ("description",))
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
        id = self.get_id().replace("/", "%2F")
        path = "%s/%s/release" % (self.manager.path, id)
        data = {"description": description}
        if self.release is None:
            try:
                server_data = self.manager.gitlab.http_post(
                    path, post_data=data, **kwargs
                )
            except exc.GitlabHttpError as e:
                raise exc.GitlabCreateError(e.response_code, e.error_message)
        else:
            try:
                server_data = self.manager.gitlab.http_put(
                    path, post_data=data, **kwargs
                )
            except exc.GitlabHttpError as e:
                raise exc.GitlabUpdateError(e.response_code, e.error_message)
        self.release = server_data


class ProjectTagManager(NoUpdateMixin, RESTManager):
    _path = "/projects/%(project_id)s/repository/tags"
    _obj_cls = ProjectTag
    _from_parent_attrs = {"project_id": "id"}
    _create_attrs = (("tag_name", "ref"), ("message",))


class ProjectProtectedTag(ObjectDeleteMixin, RESTObject):
    _id_attr = "name"
    _short_print_attr = "name"


class ProjectProtectedTagManager(NoUpdateMixin, RESTManager):
    _path = "/projects/%(project_id)s/protected_tags"
    _obj_cls = ProjectProtectedTag
    _from_parent_attrs = {"project_id": "id"}
    _create_attrs = (("name",), ("create_access_level",))


class ProjectMergeRequestApproval(SaveMixin, RESTObject):
    _id_attr = None


class ProjectMergeRequestApprovalManager(GetWithoutIdMixin, UpdateMixin, RESTManager):
    _path = "/projects/%(project_id)s/merge_requests/%(mr_iid)s/approvals"
    _obj_cls = ProjectMergeRequestApproval
    _from_parent_attrs = {"project_id": "project_id", "mr_iid": "iid"}
    _update_attrs = (("approvals_required",), tuple())
    _update_uses_post = True

    @exc.on_http_error(exc.GitlabUpdateError)
    def set_approvers(self, approver_ids=None, approver_group_ids=None, **kwargs):
        """Change MR-level allowed approvers and approver groups.

        Args:
            approver_ids (list): User IDs that can approve MRs
            approver_group_ids (list): Group IDs whose members can approve MRs

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabUpdateError: If the server failed to perform the request
        """
        approver_ids = approver_ids or []
        approver_group_ids = approver_group_ids or []

        path = "%s/%s/approvers" % (self._parent.manager.path, self._parent.get_id())
        data = {"approver_ids": approver_ids, "approver_group_ids": approver_group_ids}
        self.gitlab.http_put(path, post_data=data, **kwargs)


class ProjectMergeRequestAwardEmoji(ObjectDeleteMixin, RESTObject):
    pass


class ProjectMergeRequestAwardEmojiManager(NoUpdateMixin, RESTManager):
    _path = "/projects/%(project_id)s/merge_requests/%(mr_iid)s/award_emoji"
    _obj_cls = ProjectMergeRequestAwardEmoji
    _from_parent_attrs = {"project_id": "project_id", "mr_iid": "iid"}
    _create_attrs = (("name",), tuple())


class ProjectMergeRequestDiff(RESTObject):
    pass


class ProjectMergeRequestDiffManager(RetrieveMixin, RESTManager):
    _path = "/projects/%(project_id)s/merge_requests/%(mr_iid)s/versions"
    _obj_cls = ProjectMergeRequestDiff
    _from_parent_attrs = {"project_id": "project_id", "mr_iid": "iid"}


class ProjectMergeRequestNoteAwardEmoji(ObjectDeleteMixin, RESTObject):
    pass


class ProjectMergeRequestNoteAwardEmojiManager(NoUpdateMixin, RESTManager):
    _path = (
        "/projects/%(project_id)s/merge_requests/%(mr_iid)s"
        "/notes/%(note_id)s/award_emoji"
    )
    _obj_cls = ProjectMergeRequestNoteAwardEmoji
    _from_parent_attrs = {
        "project_id": "project_id",
        "mr_iid": "mr_iid",
        "note_id": "id",
    }
    _create_attrs = (("name",), tuple())


class ProjectMergeRequestNote(SaveMixin, ObjectDeleteMixin, RESTObject):
    _managers = (("awardemojis", "ProjectMergeRequestNoteAwardEmojiManager"),)


class ProjectMergeRequestNoteManager(CRUDMixin, RESTManager):
    _path = "/projects/%(project_id)s/merge_requests/%(mr_iid)s/notes"
    _obj_cls = ProjectMergeRequestNote
    _from_parent_attrs = {"project_id": "project_id", "mr_iid": "iid"}
    _create_attrs = (("body",), tuple())
    _update_attrs = (("body",), tuple())


class ProjectMergeRequestDiscussionNote(SaveMixin, ObjectDeleteMixin, RESTObject):
    pass


class ProjectMergeRequestDiscussionNoteManager(
    GetMixin, CreateMixin, UpdateMixin, DeleteMixin, RESTManager
):
    _path = (
        "/projects/%(project_id)s/merge_requests/%(mr_iid)s/"
        "discussions/%(discussion_id)s/notes"
    )
    _obj_cls = ProjectMergeRequestDiscussionNote
    _from_parent_attrs = {
        "project_id": "project_id",
        "mr_iid": "mr_iid",
        "discussion_id": "id",
    }
    _create_attrs = (("body",), ("created_at",))
    _update_attrs = (("body",), tuple())


class ProjectMergeRequestDiscussion(SaveMixin, RESTObject):
    _managers = (("notes", "ProjectMergeRequestDiscussionNoteManager"),)


class ProjectMergeRequestDiscussionManager(
    RetrieveMixin, CreateMixin, UpdateMixin, RESTManager
):
    _path = "/projects/%(project_id)s/merge_requests/%(mr_iid)s/discussions"
    _obj_cls = ProjectMergeRequestDiscussion
    _from_parent_attrs = {"project_id": "project_id", "mr_iid": "iid"}
    _create_attrs = (("body",), ("created_at", "position"))
    _update_attrs = (("resolved",), tuple())


class ProjectMergeRequestResourceLabelEvent(RESTObject):
    pass


class ProjectMergeRequestResourceLabelEventManager(RetrieveMixin, RESTManager):
    _path = (
        "/projects/%(project_id)s/merge_requests/%(mr_iid)s" "/resource_label_events"
    )
    _obj_cls = ProjectMergeRequestResourceLabelEvent
    _from_parent_attrs = {"project_id": "project_id", "mr_iid": "iid"}


class ProjectMergeRequest(
    SubscribableMixin,
    TodoMixin,
    TimeTrackingMixin,
    ParticipantsMixin,
    SaveMixin,
    ObjectDeleteMixin,
    RESTObject,
):
    _id_attr = "iid"

    _managers = (
        ("approvals", "ProjectMergeRequestApprovalManager"),
        ("awardemojis", "ProjectMergeRequestAwardEmojiManager"),
        ("diffs", "ProjectMergeRequestDiffManager"),
        ("discussions", "ProjectMergeRequestDiscussionManager"),
        ("notes", "ProjectMergeRequestNoteManager"),
        ("resourcelabelevents", "ProjectMergeRequestResourceLabelEventManager"),
    )

    @cli.register_custom_action("ProjectMergeRequest")
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

        path = "%s/%s/cancel_merge_when_pipeline_succeeds" % (
            self.manager.path,
            self.get_id(),
        )
        server_data = self.manager.gitlab.http_put(path, **kwargs)
        self._update_attrs(server_data)

    @cli.register_custom_action("ProjectMergeRequest")
    @exc.on_http_error(exc.GitlabListError)
    def closes_issues(self, **kwargs):
        """List issues that will close on merge."

        Args:
            all (bool): If True, return all the items, without pagination
            per_page (int): Number of items to retrieve per request
            page (int): ID of the page to return (starts with page 1)
            as_list (bool): If set to False and no pagination option is
                defined, return a generator instead of a list
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabListError: If the list could not be retrieved

        Returns:
            RESTObjectList: List of issues
        """
        path = "%s/%s/closes_issues" % (self.manager.path, self.get_id())
        data_list = self.manager.gitlab.http_list(path, as_list=False, **kwargs)
        manager = ProjectIssueManager(self.manager.gitlab, parent=self.manager._parent)
        return RESTObjectList(manager, ProjectIssue, data_list)

    @cli.register_custom_action("ProjectMergeRequest")
    @exc.on_http_error(exc.GitlabListError)
    def commits(self, **kwargs):
        """List the merge request commits.

        Args:
            all (bool): If True, return all the items, without pagination
            per_page (int): Number of items to retrieve per request
            page (int): ID of the page to return (starts with page 1)
            as_list (bool): If set to False and no pagination option is
                defined, return a generator instead of a list
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabListError: If the list could not be retrieved

        Returns:
            RESTObjectList: The list of commits
        """

        path = "%s/%s/commits" % (self.manager.path, self.get_id())
        data_list = self.manager.gitlab.http_list(path, as_list=False, **kwargs)
        manager = ProjectCommitManager(self.manager.gitlab, parent=self.manager._parent)
        return RESTObjectList(manager, ProjectCommit, data_list)

    @cli.register_custom_action("ProjectMergeRequest")
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
        path = "%s/%s/changes" % (self.manager.path, self.get_id())
        return self.manager.gitlab.http_get(path, **kwargs)

    @cli.register_custom_action("ProjectMergeRequest")
    @exc.on_http_error(exc.GitlabListError)
    def pipelines(self, **kwargs):
        """List the merge request pipelines.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabListError: If the list could not be retrieved

        Returns:
            RESTObjectList: List of changes
        """

        path = "%s/%s/pipelines" % (self.manager.path, self.get_id())
        return self.manager.gitlab.http_get(path, **kwargs)

    @cli.register_custom_action("ProjectMergeRequest", tuple(), ("sha"))
    @exc.on_http_error(exc.GitlabMRApprovalError)
    def approve(self, sha=None, **kwargs):
        """Approve the merge request.

        Args:
            sha (str): Head SHA of MR
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabMRApprovalError: If the approval failed
        """
        path = "%s/%s/approve" % (self.manager.path, self.get_id())
        data = {}
        if sha:
            data["sha"] = sha

        server_data = self.manager.gitlab.http_post(path, post_data=data, **kwargs)
        self._update_attrs(server_data)

    @cli.register_custom_action("ProjectMergeRequest")
    @exc.on_http_error(exc.GitlabMRApprovalError)
    def unapprove(self, **kwargs):
        """Unapprove the merge request.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabMRApprovalError: If the unapproval failed
        """
        path = "%s/%s/unapprove" % (self.manager.path, self.get_id())
        data = {}

        server_data = self.manager.gitlab.http_post(path, post_data=data, **kwargs)
        self._update_attrs(server_data)

    @cli.register_custom_action("ProjectMergeRequest")
    @exc.on_http_error(exc.GitlabMRRebaseError)
    def rebase(self, **kwargs):
        """Attempt to rebase the source branch onto the target branch

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabMRRebaseError: If rebasing failed
        """
        path = "%s/%s/rebase" % (self.manager.path, self.get_id())
        data = {}
        return self.manager.gitlab.http_put(path, post_data=data, **kwargs)

    @cli.register_custom_action(
        "ProjectMergeRequest",
        tuple(),
        (
            "merge_commit_message",
            "should_remove_source_branch",
            "merge_when_pipeline_succeeds",
        ),
    )
    @exc.on_http_error(exc.GitlabMRClosedError)
    def merge(
        self,
        merge_commit_message=None,
        should_remove_source_branch=False,
        merge_when_pipeline_succeeds=False,
        **kwargs
    ):
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
        path = "%s/%s/merge" % (self.manager.path, self.get_id())
        data = {}
        if merge_commit_message:
            data["merge_commit_message"] = merge_commit_message
        if should_remove_source_branch:
            data["should_remove_source_branch"] = True
        if merge_when_pipeline_succeeds:
            data["merge_when_pipeline_succeeds"] = True

        server_data = self.manager.gitlab.http_put(path, post_data=data, **kwargs)
        self._update_attrs(server_data)


class ProjectMergeRequestManager(CRUDMixin, RESTManager):
    _path = "/projects/%(project_id)s/merge_requests"
    _obj_cls = ProjectMergeRequest
    _from_parent_attrs = {"project_id": "id"}
    _create_attrs = (
        ("source_branch", "target_branch", "title"),
        (
            "assignee_id",
            "description",
            "target_project_id",
            "labels",
            "milestone_id",
            "remove_source_branch",
            "allow_maintainer_to_push",
            "squash",
        ),
    )
    _update_attrs = (
        tuple(),
        (
            "target_branch",
            "assignee_id",
            "title",
            "description",
            "state_event",
            "labels",
            "milestone_id",
            "remove_source_branch",
            "discussion_locked",
            "allow_maintainer_to_push",
            "squash",
        ),
    )
    _list_filters = (
        "state",
        "order_by",
        "sort",
        "milestone",
        "view",
        "labels",
        "created_after",
        "created_before",
        "updated_after",
        "updated_before",
        "scope",
        "author_id",
        "assignee_id",
        "my_reaction_emoji",
        "source_branch",
        "target_branch",
        "search",
    )
    _types = {"labels": types.ListAttribute}


class ProjectMilestone(SaveMixin, ObjectDeleteMixin, RESTObject):
    _short_print_attr = "title"

    @cli.register_custom_action("ProjectMilestone")
    @exc.on_http_error(exc.GitlabListError)
    def issues(self, **kwargs):
        """List issues related to this milestone.

        Args:
            all (bool): If True, return all the items, without pagination
            per_page (int): Number of items to retrieve per request
            page (int): ID of the page to return (starts with page 1)
            as_list (bool): If set to False and no pagination option is
                defined, return a generator instead of a list
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabListError: If the list could not be retrieved

        Returns:
            RESTObjectList: The list of issues
        """

        path = "%s/%s/issues" % (self.manager.path, self.get_id())
        data_list = self.manager.gitlab.http_list(path, as_list=False, **kwargs)
        manager = ProjectIssueManager(self.manager.gitlab, parent=self.manager._parent)
        # FIXME(gpocentek): the computed manager path is not correct
        return RESTObjectList(manager, ProjectIssue, data_list)

    @cli.register_custom_action("ProjectMilestone")
    @exc.on_http_error(exc.GitlabListError)
    def merge_requests(self, **kwargs):
        """List the merge requests related to this milestone.

        Args:
            all (bool): If True, return all the items, without pagination
            per_page (int): Number of items to retrieve per request
            page (int): ID of the page to return (starts with page 1)
            as_list (bool): If set to False and no pagination option is
                defined, return a generator instead of a list
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabListError: If the list could not be retrieved

        Returns:
            RESTObjectList: The list of merge requests
        """
        path = "%s/%s/merge_requests" % (self.manager.path, self.get_id())
        data_list = self.manager.gitlab.http_list(path, as_list=False, **kwargs)
        manager = ProjectMergeRequestManager(
            self.manager.gitlab, parent=self.manager._parent
        )
        # FIXME(gpocentek): the computed manager path is not correct
        return RESTObjectList(manager, ProjectMergeRequest, data_list)


class ProjectMilestoneManager(CRUDMixin, RESTManager):
    _path = "/projects/%(project_id)s/milestones"
    _obj_cls = ProjectMilestone
    _from_parent_attrs = {"project_id": "id"}
    _create_attrs = (
        ("title",),
        ("description", "due_date", "start_date", "state_event"),
    )
    _update_attrs = (
        tuple(),
        ("title", "description", "due_date", "start_date", "state_event"),
    )
    _list_filters = ("iids", "state", "search")


class ProjectLabel(SubscribableMixin, SaveMixin, ObjectDeleteMixin, RESTObject):
    _id_attr = "name"

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


class ProjectLabelManager(
    ListMixin, CreateMixin, UpdateMixin, DeleteMixin, RESTManager
):
    _path = "/projects/%(project_id)s/labels"
    _obj_cls = ProjectLabel
    _from_parent_attrs = {"project_id": "id"}
    _create_attrs = (("name", "color"), ("description", "priority"))
    _update_attrs = (("name",), ("new_name", "color", "description", "priority"))

    # Update without ID.
    def update(self, name, new_data=None, **kwargs):
        """Update a Label on the server.

        Args:
            name: The name of the label
            **kwargs: Extra options to send to the server (e.g. sudo)
        """
        new_data = new_data or {}
        if name:
            new_data["name"] = name
        return super().update(id=None, new_data=new_data, **kwargs)

    # Delete without ID.
    @exc.on_http_error(exc.GitlabDeleteError)
    def delete(self, name, **kwargs):
        """Delete a Label on the server.

        Args:
            name: The name of the label
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabDeleteError: If the server cannot perform the request
        """
        self.gitlab.http_delete(self.path, query_data={"name": name}, **kwargs)


class ProjectFile(SaveMixin, ObjectDeleteMixin, RESTObject):
    _id_attr = "file_path"
    _short_print_attr = "file_path"

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
        self.file_path = self.file_path.replace("/", "%2F")
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
        file_path = self.get_id().replace("/", "%2F")
        self.manager.delete(file_path, branch, commit_message, **kwargs)


class ProjectFileManager(GetMixin, CreateMixin, UpdateMixin, DeleteMixin, RESTManager):
    _path = "/projects/%(project_id)s/repository/files"
    _obj_cls = ProjectFile
    _from_parent_attrs = {"project_id": "id"}
    _create_attrs = (
        ("file_path", "branch", "content", "commit_message"),
        ("encoding", "author_email", "author_name"),
    )
    _update_attrs = (
        ("file_path", "branch", "content", "commit_message"),
        ("encoding", "author_email", "author_name"),
    )

    @cli.register_custom_action("ProjectFileManager", ("file_path", "ref"))
    def get(self, file_path, ref, **kwargs):
        """Retrieve a single file.

        Args:
            file_path (str): Path of the file to retrieve
            ref (str): Name of the branch, tag or commit
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabGetError: If the file could not be retrieved

        Returns:
            object: The generated RESTObject
        """
        file_path = file_path.replace("/", "%2F")
        return GetMixin.get(self, file_path, ref=ref, **kwargs)

    @cli.register_custom_action(
        "ProjectFileManager",
        ("file_path", "branch", "content", "commit_message"),
        ("encoding", "author_email", "author_name"),
    )
    @exc.on_http_error(exc.GitlabCreateError)
    def create(self, data, **kwargs):
        """Create a new object.

        Args:
            data (dict): parameters to send to the server to create the
                         resource
            **kwargs: Extra options to send to the server (e.g. sudo)

        Returns:
            RESTObject: a new instance of the managed object class built with
                the data sent by the server

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabCreateError: If the server cannot perform the request
        """

        self._check_missing_create_attrs(data)
        new_data = data.copy()
        file_path = new_data.pop("file_path").replace("/", "%2F")
        path = "%s/%s" % (self.path, file_path)
        server_data = self.gitlab.http_post(path, post_data=new_data, **kwargs)
        return self._obj_cls(self, server_data)

    @exc.on_http_error(exc.GitlabUpdateError)
    def update(self, file_path, new_data=None, **kwargs):
        """Update an object on the server.

        Args:
            id: ID of the object to update (can be None if not required)
            new_data: the update data for the object
            **kwargs: Extra options to send to the server (e.g. sudo)

        Returns:
            dict: The new object data (*not* a RESTObject)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabUpdateError: If the server cannot perform the request
        """
        new_data = new_data or {}
        data = new_data.copy()
        file_path = file_path.replace("/", "%2F")
        data["file_path"] = file_path
        path = "%s/%s" % (self.path, file_path)
        self._check_missing_update_attrs(data)
        return self.gitlab.http_put(path, post_data=data, **kwargs)

    @cli.register_custom_action(
        "ProjectFileManager", ("file_path", "branch", "commit_message")
    )
    @exc.on_http_error(exc.GitlabDeleteError)
    def delete(self, file_path, branch, commit_message, **kwargs):
        """Delete a file on the server.

        Args:
            file_path (str): Path of the file to remove
            branch (str): Branch from which the file will be removed
            commit_message (str): Commit message for the deletion
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabDeleteError: If the server cannot perform the request
        """
        path = "%s/%s" % (self.path, file_path.replace("/", "%2F"))
        data = {"branch": branch, "commit_message": commit_message}
        self.gitlab.http_delete(path, query_data=data, **kwargs)

    @cli.register_custom_action("ProjectFileManager", ("file_path", "ref"))
    @exc.on_http_error(exc.GitlabGetError)
    def raw(
        self, file_path, ref, streamed=False, action=None, chunk_size=1024, **kwargs
    ):
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
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabGetError: If the file could not be retrieved

        Returns:
            str: The file content
        """
        file_path = file_path.replace("/", "%2F").replace(".", "%2E")
        path = "%s/%s/raw" % (self.path, file_path)
        query_data = {"ref": ref}
        result = self.gitlab.http_get(
            path, query_data=query_data, streamed=streamed, raw=True, **kwargs
        )
        return utils.response_content(result, streamed, action, chunk_size)

    @cli.register_custom_action("ProjectFileManager", ("file_path", "ref"))
    @exc.on_http_error(exc.GitlabListError)
    def blame(self, file_path, ref, **kwargs):
        """Return the content of a file for a commit.

        Args:
            file_path (str): Path of the file to retrieve
            ref (str): Name of the branch, tag or commit
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabListError:  If the server failed to perform the request

        Returns:
            list(blame): a list of commits/lines matching the file
        """
        file_path = file_path.replace("/", "%2F").replace(".", "%2E")
        path = "%s/%s/blame" % (self.path, file_path)
        query_data = {"ref": ref}
        return self.gitlab.http_list(path, query_data, **kwargs)


class ProjectPipelineJob(RESTObject):
    pass


class ProjectPipelineJobManager(ListMixin, RESTManager):
    _path = "/projects/%(project_id)s/pipelines/%(pipeline_id)s/jobs"
    _obj_cls = ProjectPipelineJob
    _from_parent_attrs = {"project_id": "project_id", "pipeline_id": "id"}
    _list_filters = ("scope",)


class ProjectPipelineVariable(RESTObject):
    _id_attr = "key"


class ProjectPipelineVariableManager(ListMixin, RESTManager):
    _path = "/projects/%(project_id)s/pipelines/%(pipeline_id)s/variables"
    _obj_cls = ProjectPipelineVariable
    _from_parent_attrs = {"project_id": "project_id", "pipeline_id": "id"}


class ProjectPipeline(RESTObject, RefreshMixin, ObjectDeleteMixin):
    _managers = (
        ("jobs", "ProjectPipelineJobManager"),
        ("variables", "ProjectPipelineVariableManager"),
    )

    @cli.register_custom_action("ProjectPipeline")
    @exc.on_http_error(exc.GitlabPipelineCancelError)
    def cancel(self, **kwargs):
        """Cancel the job.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabPipelineCancelError: If the request failed
        """
        path = "%s/%s/cancel" % (self.manager.path, self.get_id())
        self.manager.gitlab.http_post(path)

    @cli.register_custom_action("ProjectPipeline")
    @exc.on_http_error(exc.GitlabPipelineRetryError)
    def retry(self, **kwargs):
        """Retry the job.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabPipelineRetryError: If the request failed
        """
        path = "%s/%s/retry" % (self.manager.path, self.get_id())
        self.manager.gitlab.http_post(path)


class ProjectPipelineManager(RetrieveMixin, CreateMixin, DeleteMixin, RESTManager):
    _path = "/projects/%(project_id)s/pipelines"
    _obj_cls = ProjectPipeline
    _from_parent_attrs = {"project_id": "id"}
    _list_filters = (
        "scope",
        "status",
        "ref",
        "sha",
        "yaml_errors",
        "name",
        "username",
        "order_by",
        "sort",
    )
    _create_attrs = (("ref",), tuple())

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


class ProjectPipelineScheduleVariable(SaveMixin, ObjectDeleteMixin, RESTObject):
    _id_attr = "key"


class ProjectPipelineScheduleVariableManager(
    CreateMixin, UpdateMixin, DeleteMixin, RESTManager
):
    _path = (
        "/projects/%(project_id)s/pipeline_schedules/"
        "%(pipeline_schedule_id)s/variables"
    )
    _obj_cls = ProjectPipelineScheduleVariable
    _from_parent_attrs = {"project_id": "project_id", "pipeline_schedule_id": "id"}
    _create_attrs = (("key", "value"), tuple())
    _update_attrs = (("key", "value"), tuple())


class ProjectPipelineSchedule(SaveMixin, ObjectDeleteMixin, RESTObject):
    _managers = (("variables", "ProjectPipelineScheduleVariableManager"),)

    @cli.register_custom_action("ProjectPipelineSchedule")
    @exc.on_http_error(exc.GitlabOwnershipError)
    def take_ownership(self, **kwargs):
        """Update the owner of a pipeline schedule.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabOwnershipError: If the request failed
        """
        path = "%s/%s/take_ownership" % (self.manager.path, self.get_id())
        server_data = self.manager.gitlab.http_post(path, **kwargs)
        self._update_attrs(server_data)


class ProjectPipelineScheduleManager(CRUDMixin, RESTManager):
    _path = "/projects/%(project_id)s/pipeline_schedules"
    _obj_cls = ProjectPipelineSchedule
    _from_parent_attrs = {"project_id": "id"}
    _create_attrs = (("description", "ref", "cron"), ("cron_timezone", "active"))
    _update_attrs = (tuple(), ("description", "ref", "cron", "cron_timezone", "active"))


class ProjectPushRules(SaveMixin, ObjectDeleteMixin, RESTObject):
    _id_attr = None


class ProjectPushRulesManager(
    GetWithoutIdMixin, CreateMixin, UpdateMixin, DeleteMixin, RESTManager
):
    _path = "/projects/%(project_id)s/push_rule"
    _obj_cls = ProjectPushRules
    _from_parent_attrs = {"project_id": "id"}
    _create_attrs = (
        tuple(),
        (
            "deny_delete_tag",
            "member_check",
            "prevent_secrets",
            "commit_message_regex",
            "branch_name_regex",
            "author_email_regex",
            "file_name_regex",
            "max_file_size",
        ),
    )
    _update_attrs = (
        tuple(),
        (
            "deny_delete_tag",
            "member_check",
            "prevent_secrets",
            "commit_message_regex",
            "branch_name_regex",
            "author_email_regex",
            "file_name_regex",
            "max_file_size",
        ),
    )


class ProjectSnippetNoteAwardEmoji(ObjectDeleteMixin, RESTObject):
    pass


class ProjectSnippetNoteAwardEmojiManager(NoUpdateMixin, RESTManager):
    _path = (
        "/projects/%(project_id)s/snippets/%(snippet_id)s"
        "/notes/%(note_id)s/award_emoji"
    )
    _obj_cls = ProjectSnippetNoteAwardEmoji
    _from_parent_attrs = {
        "project_id": "project_id",
        "snippet_id": "snippet_id",
        "note_id": "id",
    }
    _create_attrs = (("name",), tuple())


class ProjectSnippetNote(SaveMixin, ObjectDeleteMixin, RESTObject):
    _managers = (("awardemojis", "ProjectSnippetNoteAwardEmojiManager"),)


class ProjectSnippetNoteManager(CRUDMixin, RESTManager):
    _path = "/projects/%(project_id)s/snippets/%(snippet_id)s/notes"
    _obj_cls = ProjectSnippetNote
    _from_parent_attrs = {"project_id": "project_id", "snippet_id": "id"}
    _create_attrs = (("body",), tuple())
    _update_attrs = (("body",), tuple())


class ProjectSnippetAwardEmoji(ObjectDeleteMixin, RESTObject):
    pass


class ProjectSnippetAwardEmojiManager(NoUpdateMixin, RESTManager):
    _path = "/projects/%(project_id)s/snippets/%(snippet_id)s/award_emoji"
    _obj_cls = ProjectSnippetAwardEmoji
    _from_parent_attrs = {"project_id": "project_id", "snippet_id": "id"}
    _create_attrs = (("name",), tuple())


class ProjectSnippetDiscussionNote(SaveMixin, ObjectDeleteMixin, RESTObject):
    pass


class ProjectSnippetDiscussionNoteManager(
    GetMixin, CreateMixin, UpdateMixin, DeleteMixin, RESTManager
):
    _path = (
        "/projects/%(project_id)s/snippets/%(snippet_id)s/"
        "discussions/%(discussion_id)s/notes"
    )
    _obj_cls = ProjectSnippetDiscussionNote
    _from_parent_attrs = {
        "project_id": "project_id",
        "snippet_id": "snippet_id",
        "discussion_id": "id",
    }
    _create_attrs = (("body",), ("created_at",))
    _update_attrs = (("body",), tuple())


class ProjectSnippetDiscussion(RESTObject):
    _managers = (("notes", "ProjectSnippetDiscussionNoteManager"),)


class ProjectSnippetDiscussionManager(RetrieveMixin, CreateMixin, RESTManager):
    _path = "/projects/%(project_id)s/snippets/%(snippet_id)s/discussions"
    _obj_cls = ProjectSnippetDiscussion
    _from_parent_attrs = {"project_id": "project_id", "snippet_id": "id"}
    _create_attrs = (("body",), ("created_at",))


class ProjectSnippet(UserAgentDetailMixin, SaveMixin, ObjectDeleteMixin, RESTObject):
    _url = "/projects/%(project_id)s/snippets"
    _short_print_attr = "title"
    _managers = (
        ("awardemojis", "ProjectSnippetAwardEmojiManager"),
        ("discussions", "ProjectSnippetDiscussionManager"),
        ("notes", "ProjectSnippetNoteManager"),
    )

    @cli.register_custom_action("ProjectSnippet")
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
        result = self.manager.gitlab.http_get(
            path, streamed=streamed, raw=True, **kwargs
        )
        return utils.response_content(result, streamed, action, chunk_size)


class ProjectSnippetManager(CRUDMixin, RESTManager):
    _path = "/projects/%(project_id)s/snippets"
    _obj_cls = ProjectSnippet
    _from_parent_attrs = {"project_id": "id"}
    _create_attrs = (("title", "file_name", "code"), ("lifetime", "visibility"))
    _update_attrs = (tuple(), ("title", "file_name", "code", "visibility"))


class ProjectTrigger(SaveMixin, ObjectDeleteMixin, RESTObject):
    @cli.register_custom_action("ProjectTrigger")
    @exc.on_http_error(exc.GitlabOwnershipError)
    def take_ownership(self, **kwargs):
        """Update the owner of a trigger.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabOwnershipError: If the request failed
        """
        path = "%s/%s/take_ownership" % (self.manager.path, self.get_id())
        server_data = self.manager.gitlab.http_post(path, **kwargs)
        self._update_attrs(server_data)


class ProjectTriggerManager(CRUDMixin, RESTManager):
    _path = "/projects/%(project_id)s/triggers"
    _obj_cls = ProjectTrigger
    _from_parent_attrs = {"project_id": "id"}
    _create_attrs = (("description",), tuple())
    _update_attrs = (("description",), tuple())


class ProjectUser(RESTObject):
    pass


class ProjectUserManager(ListMixin, RESTManager):
    _path = "/projects/%(project_id)s/users"
    _obj_cls = ProjectUser
    _from_parent_attrs = {"project_id": "id"}
    _list_filters = ("search",)


class ProjectVariable(SaveMixin, ObjectDeleteMixin, RESTObject):
    _id_attr = "key"


class ProjectVariableManager(CRUDMixin, RESTManager):
    _path = "/projects/%(project_id)s/variables"
    _obj_cls = ProjectVariable
    _from_parent_attrs = {"project_id": "id"}
    _create_attrs = (("key", "value"), ("protected", "variable_type"))
    _update_attrs = (("key", "value"), ("protected", "variable_type"))


class ProjectService(SaveMixin, ObjectDeleteMixin, RESTObject):
    pass


class ProjectServiceManager(GetMixin, UpdateMixin, DeleteMixin, RESTManager):
    _path = "/projects/%(project_id)s/services"
    _from_parent_attrs = {"project_id": "id"}
    _obj_cls = ProjectService

    _service_attrs = {
        "asana": (("api_key",), ("restrict_to_branch",)),
        "assembla": (("token",), ("subdomain",)),
        "bamboo": (("bamboo_url", "build_key", "username", "password"), tuple()),
        "buildkite": (("token", "project_url"), ("enable_ssl_verification",)),
        "campfire": (("token",), ("subdomain", "room")),
        "custom-issue-tracker": (
            ("new_issue_url", "issues_url", "project_url"),
            ("description", "title"),
        ),
        "drone-ci": (("token", "drone_url"), ("enable_ssl_verification",)),
        "emails-on-push": (
            ("recipients",),
            ("disable_diffs", "send_from_committer_email"),
        ),
        "builds-email": (("recipients",), ("add_pusher", "notify_only_broken_builds")),
        "pipelines-email": (
            ("recipients",),
            ("add_pusher", "notify_only_broken_builds"),
        ),
        "external-wiki": (("external_wiki_url",), tuple()),
        "flowdock": (("token",), tuple()),
        "gemnasium": (("api_key", "token"), tuple()),
        "hipchat": (("token",), ("color", "notify", "room", "api_version", "server")),
        "irker": (
            ("recipients",),
            ("default_irc_uri", "server_port", "server_host", "colorize_messages"),
        ),
        "jira": (
            ("url", "project_key"),
            (
                "new_issue_url",
                "project_url",
                "issues_url",
                "api_url",
                "description",
                "username",
                "password",
                "jira_issue_transition_id",
            ),
        ),
        "mattermost": (("webhook",), ("username", "channel")),
        "pivotaltracker": (("token",), tuple()),
        "pushover": (("api_key", "user_key", "priority"), ("device", "sound")),
        "redmine": (("new_issue_url", "project_url", "issues_url"), ("description",)),
        "slack": (("webhook",), ("username", "channel")),
        "teamcity": (("teamcity_url", "build_type", "username", "password"), tuple()),
    }

    def get(self, id, **kwargs):
        """Retrieve a single object.

        Args:
            id (int or str): ID of the object to retrieve
            lazy (bool): If True, don't request the server, but create a
                         shallow object giving access to the managers. This is
                         useful if you want to avoid useless calls to the API.
            **kwargs: Extra options to send to the server (e.g. sudo)

        Returns:
            object: The generated RESTObject.

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabGetError: If the server cannot perform the request
        """
        obj = super(ProjectServiceManager, self).get(id, **kwargs)
        obj.id = id
        return obj

    def update(self, id=None, new_data=None, **kwargs):
        """Update an object on the server.

        Args:
            id: ID of the object to update (can be None if not required)
            new_data: the update data for the object
            **kwargs: Extra options to send to the server (e.g. sudo)

        Returns:
            dict: The new object data (*not* a RESTObject)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabUpdateError: If the server cannot perform the request
        """
        new_data = new_data or {}
        super(ProjectServiceManager, self).update(id, new_data, **kwargs)
        self.id = id

    @cli.register_custom_action("ProjectServiceManager")
    def available(self, **kwargs):
        """List the services known by python-gitlab.

        Returns:
            list (str): The list of service code names.
        """
        return list(self._service_attrs.keys())


class ProjectAccessRequest(AccessRequestMixin, ObjectDeleteMixin, RESTObject):
    pass


class ProjectAccessRequestManager(ListMixin, CreateMixin, DeleteMixin, RESTManager):
    _path = "/projects/%(project_id)s/access_requests"
    _obj_cls = ProjectAccessRequest
    _from_parent_attrs = {"project_id": "id"}


class ProjectApproval(SaveMixin, RESTObject):
    _id_attr = None


class ProjectApprovalManager(GetWithoutIdMixin, UpdateMixin, RESTManager):
    _path = "/projects/%(project_id)s/approvals"
    _obj_cls = ProjectApproval
    _from_parent_attrs = {"project_id": "id"}
    _update_attrs = (
        tuple(),
        (
            "approvals_before_merge",
            "reset_approvals_on_push",
            "disable_overriding_approvers_per_merge_request",
            "merge_requests_author_approval",
            "merge_requests_disable_committers_approval",
        ),
    )
    _update_uses_post = True

    @exc.on_http_error(exc.GitlabUpdateError)
    def set_approvers(self, approver_ids=None, approver_group_ids=None, **kwargs):
        """Change project-level allowed approvers and approver groups.

        Args:
            approver_ids (list): User IDs that can approve MRs
            approver_group_ids (list): Group IDs whose members can approve MRs

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabUpdateError: If the server failed to perform the request
        """
        approver_ids = approver_ids or []
        approver_group_ids = approver_group_ids or []

        path = "/projects/%s/approvers" % self._parent.get_id()
        data = {"approver_ids": approver_ids, "approver_group_ids": approver_group_ids}
        self.gitlab.http_put(path, post_data=data, **kwargs)


class ProjectApprovalRule(SaveMixin, ObjectDeleteMixin, RESTObject):
    _id_attr = "id"


class ProjectApprovalRuleManager(
    ListMixin, CreateMixin, UpdateMixin, DeleteMixin, RESTManager
):
    _path = "/projects/%(project_id)s/approval_rules"
    _obj_cls = ProjectApprovalRule
    _from_parent_attrs = {"project_id": "id"}
    _create_attrs = (("name", "approvals_required"), ("user_ids", "group_ids"))


class ProjectDeployment(RESTObject, SaveMixin):
    pass


class ProjectDeploymentManager(RetrieveMixin, CreateMixin, UpdateMixin, RESTManager):
    _path = "/projects/%(project_id)s/deployments"
    _obj_cls = ProjectDeployment
    _from_parent_attrs = {"project_id": "id"}
    _list_filters = ("order_by", "sort")
    _create_attrs = (("sha", "ref", "tag", "status", "environment"), tuple())


class ProjectProtectedBranch(ObjectDeleteMixin, RESTObject):
    _id_attr = "name"


class ProjectProtectedBranchManager(NoUpdateMixin, RESTManager):
    _path = "/projects/%(project_id)s/protected_branches"
    _obj_cls = ProjectProtectedBranch
    _from_parent_attrs = {"project_id": "id"}
    _create_attrs = (
        ("name",),
        (
            "push_access_level",
            "merge_access_level",
            "unprotect_access_level",
            "allowed_to_push",
            "allowed_to_merge",
            "allowed_to_unprotect",
        ),
    )


class ProjectRunner(ObjectDeleteMixin, RESTObject):
    pass


class ProjectRunnerManager(NoUpdateMixin, RESTManager):
    _path = "/projects/%(project_id)s/runners"
    _obj_cls = ProjectRunner
    _from_parent_attrs = {"project_id": "id"}
    _create_attrs = (("runner_id",), tuple())


class ProjectWiki(SaveMixin, ObjectDeleteMixin, RESTObject):
    _id_attr = "slug"
    _short_print_attr = "slug"


class ProjectWikiManager(CRUDMixin, RESTManager):
    _path = "/projects/%(project_id)s/wikis"
    _obj_cls = ProjectWiki
    _from_parent_attrs = {"project_id": "id"}
    _create_attrs = (("title", "content"), ("format",))
    _update_attrs = (tuple(), ("title", "content", "format"))
    _list_filters = ("with_content",)


class ProjectExport(RefreshMixin, RESTObject):
    _id_attr = None

    @cli.register_custom_action("ProjectExport")
    @exc.on_http_error(exc.GitlabGetError)
    def download(self, streamed=False, action=None, chunk_size=1024, **kwargs):
        """Download the archive of a project export.

        Args:
            streamed (bool): If True the data will be processed by chunks of
                `chunk_size` and each chunk is passed to `action` for
                reatment
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
        path = "/projects/%s/export/download" % self.project_id
        result = self.manager.gitlab.http_get(
            path, streamed=streamed, raw=True, **kwargs
        )
        return utils.response_content(result, streamed, action, chunk_size)


class ProjectExportManager(GetWithoutIdMixin, CreateMixin, RESTManager):
    _path = "/projects/%(project_id)s/export"
    _obj_cls = ProjectExport
    _from_parent_attrs = {"project_id": "id"}
    _create_attrs = (tuple(), ("description",))


class ProjectImport(RefreshMixin, RESTObject):
    _id_attr = None


class ProjectImportManager(GetWithoutIdMixin, RESTManager):
    _path = "/projects/%(project_id)s/import"
    _obj_cls = ProjectImport
    _from_parent_attrs = {"project_id": "id"}


class ProjectAdditionalStatistics(RefreshMixin, RESTObject):
    _id_attr = None


class ProjectAdditionalStatisticsManager(GetWithoutIdMixin, RESTManager):
    _path = "/projects/%(project_id)s/statistics"
    _obj_cls = ProjectAdditionalStatistics
    _from_parent_attrs = {"project_id": "id"}


class ProjectIssuesStatistics(RefreshMixin, RESTObject):
    _id_attr = None


class ProjectIssuesStatisticsManager(GetWithoutIdMixin, RESTManager):
    _path = "/projects/%(project_id)s/issues_statistics"
    _obj_cls = ProjectIssuesStatistics
    _from_parent_attrs = {"project_id": "id"}


class Project(SaveMixin, ObjectDeleteMixin, RESTObject):
    _short_print_attr = "path"
    _managers = (
        ("accessrequests", "ProjectAccessRequestManager"),
        ("approvals", "ProjectApprovalManager"),
        ("approvalrules", "ProjectApprovalRuleManager"),
        ("badges", "ProjectBadgeManager"),
        ("boards", "ProjectBoardManager"),
        ("branches", "ProjectBranchManager"),
        ("jobs", "ProjectJobManager"),
        ("commits", "ProjectCommitManager"),
        ("customattributes", "ProjectCustomAttributeManager"),
        ("deployments", "ProjectDeploymentManager"),
        ("environments", "ProjectEnvironmentManager"),
        ("events", "ProjectEventManager"),
        ("exports", "ProjectExportManager"),
        ("files", "ProjectFileManager"),
        ("forks", "ProjectForkManager"),
        ("hooks", "ProjectHookManager"),
        ("keys", "ProjectKeyManager"),
        ("imports", "ProjectImportManager"),
        ("issues", "ProjectIssueManager"),
        ("labels", "ProjectLabelManager"),
        ("members", "ProjectMemberManager"),
        ("mergerequests", "ProjectMergeRequestManager"),
        ("milestones", "ProjectMilestoneManager"),
        ("notes", "ProjectNoteManager"),
        ("notificationsettings", "ProjectNotificationSettingsManager"),
        ("pagesdomains", "ProjectPagesDomainManager"),
        ("pipelines", "ProjectPipelineManager"),
        ("protectedbranches", "ProjectProtectedBranchManager"),
        ("protectedtags", "ProjectProtectedTagManager"),
        ("pipelineschedules", "ProjectPipelineScheduleManager"),
        ("pushrules", "ProjectPushRulesManager"),
        ("releases", "ProjectReleaseManager"),
        ("repositories", "ProjectRegistryRepositoryManager"),
        ("runners", "ProjectRunnerManager"),
        ("services", "ProjectServiceManager"),
        ("snippets", "ProjectSnippetManager"),
        ("tags", "ProjectTagManager"),
        ("users", "ProjectUserManager"),
        ("triggers", "ProjectTriggerManager"),
        ("variables", "ProjectVariableManager"),
        ("wikis", "ProjectWikiManager"),
        ("clusters", "ProjectClusterManager"),
        ("additionalstatistics", "ProjectAdditionalStatisticsManager"),
        ("issuesstatistics", "ProjectIssuesStatisticsManager"),
    )

    @cli.register_custom_action("Project", ("submodule", "branch", "commit_sha"))
    @exc.on_http_error(exc.GitlabUpdateError)
    def update_submodule(self, submodule, branch, commit_sha, **kwargs):
        """Update a project submodule

        Args:
            submodule (str): Full path to the submodule
            branch (str): Name of the branch to commit into
            commit_sha (str): Full commit SHA to update the submodule to
            commit_message (str): Commit message. If no message is provided, a default one will be set (optional)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabPutError: If the submodule could not be updated
        """

        submodule = submodule.replace("/", "%2F")  # .replace('.', '%2E')
        path = "/projects/%s/repository/submodules/%s" % (self.get_id(), submodule)
        data = {"branch": branch, "commit_sha": commit_sha}
        if "commit_message" in kwargs:
            data["commit_message"] = kwargs["commit_message"]
        return self.manager.gitlab.http_put(path, post_data=data)

    @cli.register_custom_action("Project", tuple(), ("path", "ref", "recursive"))
    @exc.on_http_error(exc.GitlabGetError)
    def repository_tree(self, path="", ref="", recursive=False, **kwargs):
        """Return a list of files in the repository.

        Args:
            path (str): Path of the top folder (/ by default)
            ref (str): Reference to a commit or branch
            recursive (bool): Whether to get the tree recursively
            all (bool): If True, return all the items, without pagination
            per_page (int): Number of items to retrieve per request
            page (int): ID of the page to return (starts with page 1)
            as_list (bool): If set to False and no pagination option is
                defined, return a generator instead of a list
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabGetError: If the server failed to perform the request

        Returns:
            list: The representation of the tree
        """
        gl_path = "/projects/%s/repository/tree" % self.get_id()
        query_data = {"recursive": recursive}
        if path:
            query_data["path"] = path
        if ref:
            query_data["ref"] = ref
        return self.manager.gitlab.http_list(gl_path, query_data=query_data, **kwargs)

    @cli.register_custom_action("Project", ("sha",))
    @exc.on_http_error(exc.GitlabGetError)
    def repository_blob(self, sha, **kwargs):
        """Return a file by blob SHA.

        Args:
            sha(str): ID of the blob
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabGetError: If the server failed to perform the request

        Returns:
            dict: The blob content and metadata
        """

        path = "/projects/%s/repository/blobs/%s" % (self.get_id(), sha)
        return self.manager.gitlab.http_get(path, **kwargs)

    @cli.register_custom_action("Project", ("sha",))
    @exc.on_http_error(exc.GitlabGetError)
    def repository_raw_blob(
        self, sha, streamed=False, action=None, chunk_size=1024, **kwargs
    ):
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
        path = "/projects/%s/repository/blobs/%s/raw" % (self.get_id(), sha)
        result = self.manager.gitlab.http_get(
            path, streamed=streamed, raw=True, **kwargs
        )
        return utils.response_content(result, streamed, action, chunk_size)

    @cli.register_custom_action("Project", ("from_", "to"))
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
        path = "/projects/%s/repository/compare" % self.get_id()
        query_data = {"from": from_, "to": to}
        return self.manager.gitlab.http_get(path, query_data=query_data, **kwargs)

    @cli.register_custom_action("Project")
    @exc.on_http_error(exc.GitlabGetError)
    def repository_contributors(self, **kwargs):
        """Return a list of contributors for the project.

        Args:
            all (bool): If True, return all the items, without pagination
            per_page (int): Number of items to retrieve per request
            page (int): ID of the page to return (starts with page 1)
            as_list (bool): If set to False and no pagination option is
                defined, return a generator instead of a list
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabGetError: If the server failed to perform the request

        Returns:
            list: The contributors
        """
        path = "/projects/%s/repository/contributors" % self.get_id()
        return self.manager.gitlab.http_list(path, **kwargs)

    @cli.register_custom_action("Project", tuple(), ("sha",))
    @exc.on_http_error(exc.GitlabListError)
    def repository_archive(
        self, sha=None, streamed=False, action=None, chunk_size=1024, **kwargs
    ):
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
        path = "/projects/%s/repository/archive" % self.get_id()
        query_data = {}
        if sha:
            query_data["sha"] = sha
        result = self.manager.gitlab.http_get(
            path, query_data=query_data, raw=True, streamed=streamed, **kwargs
        )
        return utils.response_content(result, streamed, action, chunk_size)

    @cli.register_custom_action("Project", ("forked_from_id",))
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
        path = "/projects/%s/fork/%s" % (self.get_id(), forked_from_id)
        self.manager.gitlab.http_post(path, **kwargs)

    @cli.register_custom_action("Project")
    @exc.on_http_error(exc.GitlabDeleteError)
    def delete_fork_relation(self, **kwargs):
        """Delete a forked relation between existing projects.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabDeleteError: If the server failed to perform the request
        """
        path = "/projects/%s/fork" % self.get_id()
        self.manager.gitlab.http_delete(path, **kwargs)

    @cli.register_custom_action("Project")
    @exc.on_http_error(exc.GitlabDeleteError)
    def delete_merged_branches(self, **kwargs):
        """Delete merged branches.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabDeleteError: If the server failed to perform the request
        """
        path = "/projects/%s/repository/merged_branches" % self.get_id()
        self.manager.gitlab.http_delete(path, **kwargs)

    @cli.register_custom_action("Project")
    @exc.on_http_error(exc.GitlabGetError)
    def languages(self, **kwargs):
        """Get languages used in the project with percentage value.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabGetError: If the server failed to perform the request
        """
        path = "/projects/%s/languages" % self.get_id()
        return self.manager.gitlab.http_get(path, **kwargs)

    @cli.register_custom_action("Project")
    @exc.on_http_error(exc.GitlabCreateError)
    def star(self, **kwargs):
        """Star a project.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabCreateError: If the server failed to perform the request
        """
        path = "/projects/%s/star" % self.get_id()
        server_data = self.manager.gitlab.http_post(path, **kwargs)
        self._update_attrs(server_data)

    @cli.register_custom_action("Project")
    @exc.on_http_error(exc.GitlabDeleteError)
    def unstar(self, **kwargs):
        """Unstar a project.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabDeleteError: If the server failed to perform the request
        """
        path = "/projects/%s/unstar" % self.get_id()
        server_data = self.manager.gitlab.http_post(path, **kwargs)
        self._update_attrs(server_data)

    @cli.register_custom_action("Project")
    @exc.on_http_error(exc.GitlabCreateError)
    def archive(self, **kwargs):
        """Archive a project.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabCreateError: If the server failed to perform the request
        """
        path = "/projects/%s/archive" % self.get_id()
        server_data = self.manager.gitlab.http_post(path, **kwargs)
        self._update_attrs(server_data)

    @cli.register_custom_action("Project")
    @exc.on_http_error(exc.GitlabDeleteError)
    def unarchive(self, **kwargs):
        """Unarchive a project.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabDeleteError: If the server failed to perform the request
        """
        path = "/projects/%s/unarchive" % self.get_id()
        server_data = self.manager.gitlab.http_post(path, **kwargs)
        self._update_attrs(server_data)

    @cli.register_custom_action(
        "Project", ("group_id", "group_access"), ("expires_at",)
    )
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
        path = "/projects/%s/share" % self.get_id()
        data = {
            "group_id": group_id,
            "group_access": group_access,
            "expires_at": expires_at,
        }
        self.manager.gitlab.http_post(path, post_data=data, **kwargs)

    @cli.register_custom_action("Project", ("group_id",))
    @exc.on_http_error(exc.GitlabDeleteError)
    def unshare(self, group_id, **kwargs):
        """Delete a shared project link within a group.

        Args:
            group_id (int): ID of the group.
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabDeleteError: If the server failed to perform the request
        """
        path = "/projects/%s/share/%s" % (self.get_id(), group_id)
        self.manager.gitlab.http_delete(path, **kwargs)

    # variables not supported in CLI
    @cli.register_custom_action("Project", ("ref", "token"))
    @exc.on_http_error(exc.GitlabCreateError)
    def trigger_pipeline(self, ref, token, variables=None, **kwargs):
        """Trigger a CI build.

        See https://gitlab.com/help/ci/triggers/README.md#trigger-a-build

        Args:
            ref (str): Commit to build; can be a branch name or a tag
            token (str): The trigger token
            variables (dict): Variables passed to the build script
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabCreateError: If the server failed to perform the request
        """
        variables = variables or {}
        path = "/projects/%s/trigger/pipeline" % self.get_id()
        post_data = {"ref": ref, "token": token, "variables": variables}
        attrs = self.manager.gitlab.http_post(path, post_data=post_data, **kwargs)
        return ProjectPipeline(self.pipelines, attrs)

    @cli.register_custom_action("Project")
    @exc.on_http_error(exc.GitlabHousekeepingError)
    def housekeeping(self, **kwargs):
        """Start the housekeeping task.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabHousekeepingError: If the server failed to perform the
                                     request
        """
        path = "/projects/%s/housekeeping" % self.get_id()
        self.manager.gitlab.http_post(path, **kwargs)

    # see #56 - add file attachment features
    @cli.register_custom_action("Project", ("filename", "filepath"))
    @exc.on_http_error(exc.GitlabUploadError)
    def upload(self, filename, filedata=None, filepath=None, **kwargs):
        """Upload the specified file into the project.

        .. note::

            Either ``filedata`` or ``filepath`` *MUST* be specified.

        Args:
            filename (str): The name of the file being uploaded
            filedata (bytes): The raw data of the file being uploaded
            filepath (str): The path to a local file to upload (optional)

        Raises:
            GitlabConnectionError: If the server cannot be reached
            GitlabUploadError: If the file upload fails
            GitlabUploadError: If ``filedata`` and ``filepath`` are not
                specified
            GitlabUploadError: If both ``filedata`` and ``filepath`` are
                specified

        Returns:
            dict: A ``dict`` with the keys:
                * ``alt`` - The alternate text for the upload
                * ``url`` - The direct url to the uploaded file
                * ``markdown`` - Markdown for the uploaded file
        """
        if filepath is None and filedata is None:
            raise GitlabUploadError("No file contents or path specified")

        if filedata is not None and filepath is not None:
            raise GitlabUploadError("File contents and file path specified")

        if filepath is not None:
            with open(filepath, "rb") as f:
                filedata = f.read()

        url = "/projects/%(id)s/uploads" % {"id": self.id}
        file_info = {"file": (filename, filedata)}
        data = self.manager.gitlab.http_post(url, files=file_info)

        return {"alt": data["alt"], "url": data["url"], "markdown": data["markdown"]}

    @cli.register_custom_action("Project", optional=("wiki",))
    @exc.on_http_error(exc.GitlabGetError)
    def snapshot(
        self, wiki=False, streamed=False, action=None, chunk_size=1024, **kwargs
    ):
        """Return a snapshot of the repository.

        Args:
            wiki (bool): If True return the wiki repository
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
            str: The uncompressed tar archive of the repository
        """
        path = "/projects/%s/snapshot" % self.get_id()
        result = self.manager.gitlab.http_get(
            path, streamed=streamed, raw=True, **kwargs
        )
        return utils.response_content(result, streamed, action, chunk_size)

    @cli.register_custom_action("Project", ("scope", "search"))
    @exc.on_http_error(exc.GitlabSearchError)
    def search(self, scope, search, **kwargs):
        """Search the project resources matching the provided string.'

        Args:
            scope (str): Scope of the search
            search (str): Search string
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabSearchError: If the server failed to perform the request

        Returns:
            GitlabList: A list of dicts describing the resources found.
        """
        data = {"scope": scope, "search": search}
        path = "/projects/%s/search" % self.get_id()
        return self.manager.gitlab.http_list(path, query_data=data, **kwargs)

    @cli.register_custom_action("Project")
    @exc.on_http_error(exc.GitlabCreateError)
    def mirror_pull(self, **kwargs):
        """Start the pull mirroring process for the project.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabCreateError: If the server failed to perform the request
        """
        path = "/projects/%s/mirror/pull" % self.get_id()
        self.manager.gitlab.http_post(path, **kwargs)

    @cli.register_custom_action("Project", ("to_namespace",))
    @exc.on_http_error(exc.GitlabTransferProjectError)
    def transfer_project(self, to_namespace, **kwargs):
        """Transfer a project to the given namespace ID

        Args:
            to_namespace (str): ID or path of the namespace to transfer the
            project to
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabTransferProjectError: If the project could not be transfered
        """
        path = "/projects/%s/transfer" % (self.id,)
        self.manager.gitlab.http_put(
            path, post_data={"namespace": to_namespace}, **kwargs
        )

    @cli.register_custom_action("Project", ("ref_name", "artifact_path", "job"))
    @exc.on_http_error(exc.GitlabGetError)
    def artifact(
        self,
        ref_name,
        artifact_path,
        job,
        streamed=False,
        action=None,
        chunk_size=1024,
        **kwargs
    ):
        """Download a single artifact file from a specific tag or branch from within the job’s artifacts archive.

        Args:
            ref_name (str): Branch or tag name in repository. HEAD or SHA references are not supported.
            artifact_path (str): Path to a file inside the artifacts archive.
            job (str): The name of the job.
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

        path = "/projects/%s/jobs/artifacts/%s/raw/%s?job=%s" % (
            self.get_id(),
            ref_name,
            artifact_path,
            job,
        )
        result = self.manager.gitlab.http_get(
            path, streamed=streamed, raw=True, **kwargs
        )
        return utils.response_content(result, streamed, action, chunk_size)


class ProjectManager(CRUDMixin, RESTManager):
    _path = "/projects"
    _obj_cls = Project
    _create_attrs = (
        tuple(),
        (
            "name",
            "path",
            "namespace_id",
            "description",
            "issues_enabled",
            "merge_requests_enabled",
            "jobs_enabled",
            "wiki_enabled",
            "snippets_enabled",
            "resolve_outdated_diff_discussions",
            "container_registry_enabled",
            "shared_runners_enabled",
            "visibility",
            "import_url",
            "public_jobs",
            "only_allow_merge_if_pipeline_succeeds",
            "only_allow_merge_if_all_discussions_are_resolved",
            "merge_method",
            "lfs_enabled",
            "request_access_enabled",
            "tag_list",
            "avatar",
            "printing_merge_request_link_enabled",
            "ci_config_path",
        ),
    )
    _update_attrs = (
        tuple(),
        (
            "name",
            "path",
            "default_branch",
            "description",
            "issues_enabled",
            "merge_requests_enabled",
            "jobs_enabled",
            "wiki_enabled",
            "snippets_enabled",
            "resolve_outdated_diff_discussions",
            "container_registry_enabled",
            "shared_runners_enabled",
            "visibility",
            "import_url",
            "public_jobs",
            "only_allow_merge_if_pipeline_succeeds",
            "only_allow_merge_if_all_discussions_are_resolved",
            "merge_method",
            "lfs_enabled",
            "request_access_enabled",
            "tag_list",
            "avatar",
            "ci_config_path",
        ),
    )
    _types = {"avatar": types.ImageAttribute}
    _list_filters = (
        "search",
        "owned",
        "starred",
        "archived",
        "visibility",
        "order_by",
        "sort",
        "simple",
        "membership",
        "statistics",
        "with_issues_enabled",
        "with_merge_requests_enabled",
        "with_custom_attributes",
    )

    def import_project(
        self,
        file,
        path,
        namespace=None,
        overwrite=False,
        override_params=None,
        **kwargs
    ):
        """Import a project from an archive file.

        Args:
            file: Data or file object containing the project
            path (str): Name and path for the new project
            namespace (str): The ID or path of the namespace that the project
                will be imported to
            overwrite (bool): If True overwrite an existing project with the
                same path
            override_params (dict): Set the specific settings for the project
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabListError: If the server failed to perform the request

        Returns:
            dict: A representation of the import status.
        """
        files = {"file": ("file.tar.gz", file)}
        data = {"path": path, "overwrite": overwrite}
        if override_params:
            for k, v in override_params.items():
                data["override_params[%s]" % k] = v
        if namespace:
            data["namespace"] = namespace
        return self.gitlab.http_post(
            "/projects/import", post_data=data, files=files, **kwargs
        )

    def import_github(
        self, personal_access_token, repo_id, target_namespace, new_name=None, **kwargs
    ):
        """Import a project from Github to Gitlab (schedule the import)

        This method will return when an import operation has been safely queued,
        or an error has occurred. After triggering an import, check the
        `import_status` of the newly created project to detect when the import
        operation has completed.

        NOTE: this request may take longer than most other API requests.
        So this method will specify a 60 second default timeout if none is specified.
        A timeout can be specified via kwargs to override this functionality.

        Args:
            personal_access_token (str): GitHub personal access token
            repo_id (int): Github repository ID
            target_namespace (str): Namespace to import repo into
            new_name (str): New repo name (Optional)
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabListError: If the server failed to perform the request

        Returns:
            dict: A representation of the import status.

        Example:
        ```
            gl = gitlab.Gitlab_from_config()
            print "Triggering import"
            result = gl.projects.import_github(ACCESS_TOKEN,
                                               123456,
                                               "my-group/my-subgroup")
            project = gl.projects.get(ret['id'])
            print "Waiting for import to complete"
            while project.import_status == u'started':
                time.sleep(1.0)
                project = gl.projects.get(project.id)
            print "Github import complete"
        ```
        """
        data = {
            "personal_access_token": personal_access_token,
            "repo_id": repo_id,
            "target_namespace": target_namespace,
        }
        if new_name:
            data["new_name"] = new_name
        if (
            "timeout" not in kwargs
            or self.gitlab.timeout is None
            or self.gitlab.timeout < 60.0
        ):
            # Ensure that this HTTP request has a longer-than-usual default timeout
            # The base gitlab object tends to have a default that is <10 seconds,
            # and this is too short for this API command, typically.
            # On the order of 24 seconds has been measured on a typical gitlab instance.
            kwargs["timeout"] = 60.0
        result = self.gitlab.http_post("/import/github", post_data=data, **kwargs)
        return result


class RunnerJob(RESTObject):
    pass


class RunnerJobManager(ListMixin, RESTManager):
    _path = "/runners/%(runner_id)s/jobs"
    _obj_cls = RunnerJob
    _from_parent_attrs = {"runner_id": "id"}
    _list_filters = ("status",)


class Runner(SaveMixin, ObjectDeleteMixin, RESTObject):
    _managers = (("jobs", "RunnerJobManager"),)


class RunnerManager(CRUDMixin, RESTManager):
    _path = "/runners"
    _obj_cls = Runner
    _list_filters = ("scope",)
    _create_attrs = (
        ("token",),
        (
            "description",
            "info",
            "active",
            "locked",
            "run_untagged",
            "tag_list",
            "maximum_timeout",
        ),
    )
    _update_attrs = (
        tuple(),
        (
            "description",
            "active",
            "tag_list",
            "run_untagged",
            "locked",
            "access_level",
            "maximum_timeout",
        ),
    )

    @cli.register_custom_action("RunnerManager", tuple(), ("scope",))
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
        path = "/runners/all"
        query_data = {}
        if scope is not None:
            query_data["scope"] = scope
        return self.gitlab.http_list(path, query_data, **kwargs)

    @cli.register_custom_action("RunnerManager", ("token",))
    @exc.on_http_error(exc.GitlabVerifyError)
    def verify(self, token, **kwargs):
        """Validates authentication credentials for a registered Runner.

        Args:
            token (str): The runner's authentication token
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabVerifyError: If the server failed to verify the token
        """
        path = "/runners/verify"
        post_data = {"token": token}
        self.gitlab.http_post(path, post_data=post_data, **kwargs)


class Todo(ObjectDeleteMixin, RESTObject):
    @cli.register_custom_action("Todo")
    @exc.on_http_error(exc.GitlabTodoError)
    def mark_as_done(self, **kwargs):
        """Mark the todo as done.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabTodoError: If the server failed to perform the request
        """
        path = "%s/%s/mark_as_done" % (self.manager.path, self.id)
        server_data = self.manager.gitlab.http_post(path, **kwargs)
        self._update_attrs(server_data)


class TodoManager(ListMixin, DeleteMixin, RESTManager):
    _path = "/todos"
    _obj_cls = Todo
    _list_filters = ("action", "author_id", "project_id", "state", "type")

    @cli.register_custom_action("TodoManager")
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
        result = self.gitlab.http_post("/todos/mark_as_done", **kwargs)


class GeoNode(SaveMixin, ObjectDeleteMixin, RESTObject):
    @cli.register_custom_action("GeoNode")
    @exc.on_http_error(exc.GitlabRepairError)
    def repair(self, **kwargs):
        """Repair the OAuth authentication of the geo node.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabRepairError: If the server failed to perform the request
        """
        path = "/geo_nodes/%s/repair" % self.get_id()
        server_data = self.manager.gitlab.http_post(path, **kwargs)
        self._update_attrs(server_data)

    @cli.register_custom_action("GeoNode")
    @exc.on_http_error(exc.GitlabGetError)
    def status(self, **kwargs):
        """Get the status of the geo node.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabGetError: If the server failed to perform the request

        Returns:
            dict: The status of the geo node
        """
        path = "/geo_nodes/%s/status" % self.get_id()
        return self.manager.gitlab.http_get(path, **kwargs)


class GeoNodeManager(RetrieveMixin, UpdateMixin, DeleteMixin, RESTManager):
    _path = "/geo_nodes"
    _obj_cls = GeoNode
    _update_attrs = (
        tuple(),
        ("enabled", "url", "files_max_capacity", "repos_max_capacity"),
    )

    @cli.register_custom_action("GeoNodeManager")
    @exc.on_http_error(exc.GitlabGetError)
    def status(self, **kwargs):
        """Get the status of all the geo nodes.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabGetError: If the server failed to perform the request

        Returns:
            list: The status of all the geo nodes
        """
        return self.gitlab.http_list("/geo_nodes/status", **kwargs)

    @cli.register_custom_action("GeoNodeManager")
    @exc.on_http_error(exc.GitlabGetError)
    def current_failures(self, **kwargs):
        """Get the list of failures on the current geo node.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabGetError: If the server failed to perform the request

        Returns:
            list: The list of failures
        """
        return self.gitlab.http_list("/geo_nodes/current/failures", **kwargs)

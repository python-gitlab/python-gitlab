from gitlab import cli
from gitlab import exceptions as exc
from gitlab import types
from gitlab.base import RequiredOptional, RESTManager, RESTObject
from gitlab.mixins import CRUDMixin, ListMixin, ObjectDeleteMixin, SaveMixin

from .access_requests import GroupAccessRequestManager  # noqa: F401
from .audit_events import GroupAuditEventManager  # noqa: F401
from .badges import GroupBadgeManager  # noqa: F401
from .boards import GroupBoardManager  # noqa: F401
from .clusters import GroupClusterManager  # noqa: F401
from .custom_attributes import GroupCustomAttributeManager  # noqa: F401
from .deploy_tokens import GroupDeployTokenManager  # noqa: F401
from .epics import GroupEpicManager  # noqa: F401
from .export_import import GroupExportManager, GroupImportManager  # noqa: F401
from .issues import GroupIssueManager  # noqa: F401
from .labels import GroupLabelManager  # noqa: F401
from .members import (  # noqa: F401
    GroupBillableMemberManager,
    GroupMemberAllManager,
    GroupMemberManager,
)
from .merge_requests import GroupMergeRequestManager  # noqa: F401
from .milestones import GroupMilestoneManager  # noqa: F401
from .notification_settings import GroupNotificationSettingsManager  # noqa: F401
from .packages import GroupPackageManager  # noqa: F401
from .projects import GroupProjectManager  # noqa: F401
from .runners import GroupRunnerManager  # noqa: F401
from .statistics import GroupIssuesStatisticsManager  # noqa: F401
from .variables import GroupVariableManager  # noqa: F401
from .wikis import GroupWikiManager  # noqa: F401

__all__ = [
    "Group",
    "GroupManager",
    "GroupDescendantGroup",
    "GroupDescendantGroupManager",
    "GroupSubgroup",
    "GroupSubgroupManager",
]


class Group(SaveMixin, ObjectDeleteMixin, RESTObject):
    _short_print_attr = "name"
    _managers = (
        ("accessrequests", "GroupAccessRequestManager"),
        ("audit_events", "GroupAuditEventManager"),
        ("badges", "GroupBadgeManager"),
        ("billable_members", "GroupBillableMemberManager"),
        ("boards", "GroupBoardManager"),
        ("customattributes", "GroupCustomAttributeManager"),
        ("descendant_groups", "GroupDescendantGroupManager"),
        ("exports", "GroupExportManager"),
        ("epics", "GroupEpicManager"),
        ("imports", "GroupImportManager"),
        ("issues", "GroupIssueManager"),
        ("issues_statistics", "GroupIssuesStatisticsManager"),
        ("labels", "GroupLabelManager"),
        ("members", "GroupMemberManager"),
        ("members_all", "GroupMemberAllManager"),
        ("mergerequests", "GroupMergeRequestManager"),
        ("milestones", "GroupMilestoneManager"),
        ("notificationsettings", "GroupNotificationSettingsManager"),
        ("packages", "GroupPackageManager"),
        ("projects", "GroupProjectManager"),
        ("runners", "GroupRunnerManager"),
        ("subgroups", "GroupSubgroupManager"),
        ("variables", "GroupVariableManager"),
        ("clusters", "GroupClusterManager"),
        ("deploytokens", "GroupDeployTokenManager"),
        ("wikis", "GroupWikiManager"),
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

    @cli.register_custom_action("Group", ("group_id", "group_access"), ("expires_at",))
    @exc.on_http_error(exc.GitlabCreateError)
    def share(self, group_id, group_access, expires_at=None, **kwargs):
        """Share the group with a group.

        Args:
            group_id (int): ID of the group.
            group_access (int): Access level for the group.
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabCreateError: If the server failed to perform the request
        """
        path = "/groups/%s/share" % self.get_id()
        data = {
            "group_id": group_id,
            "group_access": group_access,
            "expires_at": expires_at,
        }
        self.manager.gitlab.http_post(path, post_data=data, **kwargs)

    @cli.register_custom_action("Group", ("group_id",))
    @exc.on_http_error(exc.GitlabDeleteError)
    def unshare(self, group_id, **kwargs):
        """Delete a shared group link within a group.

        Args:
            group_id (int): ID of the group.
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabDeleteError: If the server failed to perform the request
        """
        path = "/groups/%s/share/%s" % (self.get_id(), group_id)
        self.manager.gitlab.http_delete(path, **kwargs)


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
        "min_access_level",
        "top_level_only",
    )
    _create_attrs = RequiredOptional(
        required=("name", "path"),
        optional=(
            "description",
            "membership_lock",
            "visibility",
            "share_with_group_lock",
            "require_two_factor_authentication",
            "two_factor_grace_period",
            "project_creation_level",
            "auto_devops_enabled",
            "subgroup_creation_level",
            "emails_disabled",
            "avatar",
            "mentions_disabled",
            "lfs_enabled",
            "request_access_enabled",
            "parent_id",
            "default_branch_protection",
            "shared_runners_minutes_limit",
            "extra_shared_runners_minutes_limit",
        ),
    )
    _update_attrs = RequiredOptional(
        optional=(
            "name",
            "path",
            "description",
            "membership_lock",
            "share_with_group_lock",
            "visibility",
            "require_two_factor_authentication",
            "two_factor_grace_period",
            "project_creation_level",
            "auto_devops_enabled",
            "subgroup_creation_level",
            "emails_disabled",
            "avatar",
            "mentions_disabled",
            "lfs_enabled",
            "request_access_enabled",
            "default_branch_protection",
            "file_template_project_id",
            "shared_runners_minutes_limit",
            "extra_shared_runners_minutes_limit",
            "prevent_forking_outside_group",
            "shared_runners_setting",
        ),
    )
    _types = {"avatar": types.ImageAttribute, "skip_groups": types.ListAttribute}

    @exc.on_http_error(exc.GitlabImportError)
    def import_group(self, file, path, name, parent_id=None, **kwargs):
        """Import a group from an archive file.

        Args:
            file: Data or file object containing the group
            path (str): The path for the new group to be imported.
            name (str): The name for the new group.
            parent_id (str): ID of a parent group that the group will
                be imported into.
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabImportError: If the server failed to perform the request

        Returns:
            dict: A representation of the import status.
        """
        files = {"file": ("file.tar.gz", file, "application/octet-stream")}
        data = {"path": path, "name": name}
        if parent_id is not None:
            data["parent_id"] = parent_id

        return self.gitlab.http_post(
            "/groups/import", post_data=data, files=files, **kwargs
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
        "min_access_level",
    )
    _types = {"skip_groups": types.ListAttribute}


class GroupDescendantGroup(RESTObject):
    pass


class GroupDescendantGroupManager(GroupSubgroupManager):
    """
    This manager inherits from GroupSubgroupManager as descendant groups
    share all attributes with subgroups, except the path and object class.
    """

    _path = "/groups/%(group_id)s/descendant_groups"
    _obj_cls = GroupDescendantGroup

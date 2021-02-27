from gitlab import cli, types
from gitlab import exceptions as exc
from gitlab.base import RESTObject
from gitlab.mixins import CRUDMixin, ListMixin, ObjectDeleteMixin, SaveMixin
from .access_requests import GroupAccessRequestManager
from .badges import GroupBadgeManager
from .boards import GroupBoardManager
from .custom_attributes import GroupCustomAttributeManager
from .export_import import GroupExportManager, GroupImportManager
from .epics import GroupEpicManager
from .issues import GroupIssueManager
from .labels import GroupLabelManager
from .members import GroupMemberManager
from .merge_requests import GroupMergeRequestManager
from .milestones import GroupMilestoneManager
from .notification_settings import GroupNotificationSettingsManager
from .packages import GroupPackageManager
from .projects import GroupProjectManager
from .runners import GroupRunnerManager
from .variables import GroupVariableManager
from .clusters import GroupClusterManager
from .deploy_tokens import GroupDeployTokenManager


__all__ = [
    "Group",
    "GroupManager",
    "GroupSubgroup",
    "GroupSubgroupManager",
]


class Group(SaveMixin, ObjectDeleteMixin):
    _short_print_attr = "name"
    _managers = (
        ("accessrequests", "GroupAccessRequestManager"),
        ("badges", "GroupBadgeManager"),
        ("boards", "GroupBoardManager"),
        ("customattributes", "GroupCustomAttributeManager"),
        ("exports", "GroupExportManager"),
        ("epics", "GroupEpicManager"),
        ("imports", "GroupImportManager"),
        ("issues", "GroupIssueManager"),
        ("labels", "GroupLabelManager"),
        ("members", "GroupMemberManager"),
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


class GroupManager(CRUDMixin):
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
    )
    _create_attrs = (
        ("name", "path"),
        (
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
        ),
    )
    _update_attrs = (
        tuple(),
        (
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
        ),
    )
    _types = {"avatar": types.ImageAttribute}

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


class GroupSubgroupManager(ListMixin):
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

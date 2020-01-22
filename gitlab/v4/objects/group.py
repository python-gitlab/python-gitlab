from gitlab.base import *  # noqa
from gitlab.exceptions import *  # noqa
from gitlab.mixins import *  # noqa
from gitlab import types
from gitlab.v4.objects.notification_settings import NotificationSettings, NotificationSettingsManager
from gitlab import utils


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

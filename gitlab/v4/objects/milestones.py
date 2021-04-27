from gitlab import cli, types
from gitlab import exceptions as exc
from gitlab.base import RequiredOptional, RESTManager, RESTObject, RESTObjectList
from gitlab.mixins import CRUDMixin, ObjectDeleteMixin, SaveMixin
from .issues import GroupIssue, GroupIssueManager, ProjectIssue, ProjectIssueManager
from .merge_requests import (
    ProjectMergeRequest,
    ProjectMergeRequestManager,
    GroupMergeRequest,
)


__all__ = [
    "GroupMilestone",
    "GroupMilestoneManager",
    "ProjectMilestone",
    "ProjectMilestoneManager",
]


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
    _create_attrs = RequiredOptional(
        required=("title",), optional=("description", "due_date", "start_date")
    )
    _update_attrs = RequiredOptional(
        optional=("title", "description", "due_date", "start_date", "state_event"),
    )
    _list_filters = ("iids", "state", "search")
    _types = {"iids": types.ListAttribute}


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
    _create_attrs = RequiredOptional(
        required=("title",),
        optional=("description", "due_date", "start_date", "state_event"),
    )
    _update_attrs = RequiredOptional(
        optional=("title", "description", "due_date", "start_date", "state_event"),
    )
    _list_filters = ("iids", "state", "search")
    _types = {"iids": types.ListAttribute}

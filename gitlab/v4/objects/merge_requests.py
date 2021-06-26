from gitlab import cli
from gitlab import exceptions as exc
from gitlab import types
from gitlab.base import RequiredOptional, RESTManager, RESTObject, RESTObjectList
from gitlab.mixins import (
    CRUDMixin,
    ListMixin,
    ObjectDeleteMixin,
    ParticipantsMixin,
    RetrieveMixin,
    SaveMixin,
    SubscribableMixin,
    TimeTrackingMixin,
    TodoMixin,
)

from .award_emojis import ProjectMergeRequestAwardEmojiManager  # noqa: F401
from .commits import ProjectCommit, ProjectCommitManager
from .discussions import ProjectMergeRequestDiscussionManager  # noqa: F401
from .events import (  # noqa: F401
    ProjectMergeRequestResourceLabelEventManager,
    ProjectMergeRequestResourceMilestoneEventManager,
    ProjectMergeRequestResourceStateEventManager,
)
from .issues import ProjectIssue, ProjectIssueManager
from .merge_request_approvals import (  # noqa: F401
    ProjectMergeRequestApprovalManager,
    ProjectMergeRequestApprovalRuleManager,
)
from .notes import ProjectMergeRequestNoteManager  # noqa: F401
from .pipelines import ProjectMergeRequestPipelineManager  # noqa: F401

__all__ = [
    "MergeRequest",
    "MergeRequestManager",
    "GroupMergeRequest",
    "GroupMergeRequestManager",
    "ProjectMergeRequest",
    "ProjectMergeRequestManager",
    "ProjectDeploymentMergeRequest",
    "ProjectDeploymentMergeRequestManager",
    "ProjectMergeRequestDiff",
    "ProjectMergeRequestDiffManager",
]


class MergeRequest(RESTObject):
    pass


class MergeRequestManager(ListMixin, RESTManager):
    _path = "/merge_requests"
    _obj_cls = MergeRequest
    _list_filters = (
        "state",
        "order_by",
        "sort",
        "milestone",
        "view",
        "labels",
        "with_labels_details",
        "with_merge_status_recheck",
        "created_after",
        "created_before",
        "updated_after",
        "updated_before",
        "scope",
        "author_id",
        "author_username",
        "assignee_id",
        "approver_ids",
        "approved_by_ids",
        "reviewer_id",
        "reviewer_username",
        "my_reaction_emoji",
        "source_branch",
        "target_branch",
        "search",
        "in",
        "wip",
        "not",
        "environment",
        "deployed_before",
        "deployed_after",
    )
    _types = {
        "approver_ids": types.ListAttribute,
        "approved_by_ids": types.ListAttribute,
        "in": types.ListAttribute,
        "labels": types.ListAttribute,
    }


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
        "approver_ids",
        "approved_by_ids",
        "my_reaction_emoji",
        "source_branch",
        "target_branch",
        "search",
        "wip",
    )
    _types = {
        "approver_ids": types.ListAttribute,
        "approved_by_ids": types.ListAttribute,
        "labels": types.ListAttribute,
    }


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
        ("approval_rules", "ProjectMergeRequestApprovalRuleManager"),
        ("awardemojis", "ProjectMergeRequestAwardEmojiManager"),
        ("diffs", "ProjectMergeRequestDiffManager"),
        ("discussions", "ProjectMergeRequestDiscussionManager"),
        ("notes", "ProjectMergeRequestNoteManager"),
        ("pipelines", "ProjectMergeRequestPipelineManager"),
        ("resourcelabelevents", "ProjectMergeRequestResourceLabelEventManager"),
        ("resourcemilestoneevents", "ProjectMergeRequestResourceMilestoneEventManager"),
        ("resourcestateevents", "ProjectMergeRequestResourceStateEventManager"),
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

    @cli.register_custom_action("ProjectMergeRequest", tuple(), ("sha",))
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
        if should_remove_source_branch is not None:
            data["should_remove_source_branch"] = should_remove_source_branch
        if merge_when_pipeline_succeeds:
            data["merge_when_pipeline_succeeds"] = True

        server_data = self.manager.gitlab.http_put(path, post_data=data, **kwargs)
        self._update_attrs(server_data)


class ProjectMergeRequestManager(CRUDMixin, RESTManager):
    _path = "/projects/%(project_id)s/merge_requests"
    _obj_cls = ProjectMergeRequest
    _from_parent_attrs = {"project_id": "id"}
    _create_attrs = RequiredOptional(
        required=("source_branch", "target_branch", "title"),
        optional=(
            "assignee_id",
            "description",
            "target_project_id",
            "labels",
            "milestone_id",
            "remove_source_branch",
            "allow_maintainer_to_push",
            "squash",
            "reviewer_ids",
        ),
    )
    _update_attrs = RequiredOptional(
        optional=(
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
            "reviewer_ids",
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
        "iids",
        "author_id",
        "assignee_id",
        "approver_ids",
        "approved_by_ids",
        "my_reaction_emoji",
        "source_branch",
        "target_branch",
        "search",
        "wip",
    )
    _types = {
        "approver_ids": types.ListAttribute,
        "approved_by_ids": types.ListAttribute,
        "iids": types.ListAttribute,
        "labels": types.ListAttribute,
    }


class ProjectDeploymentMergeRequest(MergeRequest):
    pass


class ProjectDeploymentMergeRequestManager(MergeRequestManager):
    _path = "/projects/%(project_id)s/deployments/%(deployment_id)s/merge_requests"
    _obj_cls = ProjectDeploymentMergeRequest
    _from_parent_attrs = {"deployment_id": "id", "project_id": "project_id"}


class ProjectMergeRequestDiff(RESTObject):
    pass


class ProjectMergeRequestDiffManager(RetrieveMixin, RESTManager):
    _path = "/projects/%(project_id)s/merge_requests/%(mr_iid)s/versions"
    _obj_cls = ProjectMergeRequestDiff
    _from_parent_attrs = {"project_id": "project_id", "mr_iid": "iid"}

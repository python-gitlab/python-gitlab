from typing import Any, cast, List, Optional, TYPE_CHECKING, Union

from gitlab import exceptions as exc
from gitlab.base import RESTManager, RESTObject
from gitlab.mixins import (
    CreateMixin,
    CRUDMixin,
    DeleteMixin,
    GetWithoutIdMixin,
    ObjectDeleteMixin,
    RetrieveMixin,
    SaveMixin,
    UpdateMethod,
    UpdateMixin,
)
from gitlab.types import RequiredOptional

__all__ = [
    "GroupApprovalRule",
    "GroupApprovalRuleManager",
    "ProjectApproval",
    "ProjectApprovalManager",
    "ProjectApprovalRule",
    "ProjectApprovalRuleManager",
    "ProjectMergeRequestApproval",
    "ProjectMergeRequestApprovalManager",
    "ProjectMergeRequestApprovalRule",
    "ProjectMergeRequestApprovalRuleManager",
    "ProjectMergeRequestApprovalState",
    "ProjectMergeRequestApprovalStateManager",
]


class GroupApprovalRule(SaveMixin, RESTObject):
    _id_attr = "id"
    _repr_attr = "name"


class GroupApprovalRuleManager(RetrieveMixin, CreateMixin, UpdateMixin, RESTManager):
    _path = "/groups/{group_id}/approval_rules"
    _obj_cls = GroupApprovalRule
    _from_parent_attrs = {"group_id": "id"}
    _create_attrs = RequiredOptional(
        required=("name", "approvals_required"),
        optional=("user_ids", "group_ids", "rule_type"),
    )

    def get(
        self, id: Union[str, int], lazy: bool = False, **kwargs: Any
    ) -> GroupApprovalRule:
        return cast(GroupApprovalRule, super().get(id=id, lazy=lazy, **kwargs))


class ProjectApproval(SaveMixin, RESTObject):
    _id_attr = None


class ProjectApprovalManager(GetWithoutIdMixin, UpdateMixin, RESTManager):
    _path = "/projects/{project_id}/approvals"
    _obj_cls = ProjectApproval
    _from_parent_attrs = {"project_id": "id"}
    _update_attrs = RequiredOptional(
        optional=(
            "approvals_before_merge",
            "reset_approvals_on_push",
            "disable_overriding_approvers_per_merge_request",
            "merge_requests_author_approval",
            "merge_requests_disable_committers_approval",
        ),
    )
    _update_method = UpdateMethod.POST

    def get(self, **kwargs: Any) -> ProjectApproval:
        return cast(ProjectApproval, super().get(**kwargs))


class ProjectApprovalRule(SaveMixin, ObjectDeleteMixin, RESTObject):
    _id_attr = "id"
    _repr_attr = "name"


class ProjectApprovalRuleManager(
    RetrieveMixin, CreateMixin, UpdateMixin, DeleteMixin, RESTManager
):
    _path = "/projects/{project_id}/approval_rules"
    _obj_cls = ProjectApprovalRule
    _from_parent_attrs = {"project_id": "id"}
    _create_attrs = RequiredOptional(
        required=("name", "approvals_required"),
        optional=("user_ids", "group_ids", "protected_branch_ids", "usernames"),
    )

    def get(
        self, id: Union[str, int], lazy: bool = False, **kwargs: Any
    ) -> ProjectApprovalRule:
        return cast(ProjectApprovalRule, super().get(id=id, lazy=lazy, **kwargs))


class ProjectMergeRequestApproval(SaveMixin, RESTObject):
    _id_attr = None


class ProjectMergeRequestApprovalManager(GetWithoutIdMixin, UpdateMixin, RESTManager):
    _path = "/projects/{project_id}/merge_requests/{mr_iid}/approvals"
    _obj_cls = ProjectMergeRequestApproval
    _from_parent_attrs = {"project_id": "project_id", "mr_iid": "iid"}
    _update_attrs = RequiredOptional(required=("approvals_required",))
    _update_method = UpdateMethod.POST

    def get(self, **kwargs: Any) -> ProjectMergeRequestApproval:
        return cast(ProjectMergeRequestApproval, super().get(**kwargs))

    @exc.on_http_error(exc.GitlabUpdateError)
    def set_approvers(
        self,
        approvals_required: int,
        approver_ids: Optional[List[int]] = None,
        approver_group_ids: Optional[List[int]] = None,
        approval_rule_name: str = "name",
        *,
        approver_usernames: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> RESTObject:
        """Change MR-level allowed approvers and approver groups.

        Args:
            approvals_required: The number of required approvals for this rule
            approver_ids: User IDs that can approve MRs
            approver_group_ids: Group IDs whose members can approve MRs

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabUpdateError: If the server failed to perform the request
        """
        approver_ids = approver_ids or []
        approver_group_ids = approver_group_ids or []
        approver_usernames = approver_usernames or []

        data = {
            "name": approval_rule_name,
            "approvals_required": approvals_required,
            "rule_type": "regular",
            "user_ids": approver_ids,
            "group_ids": approver_group_ids,
            "usernames": approver_usernames,
        }
        if TYPE_CHECKING:
            assert self._parent is not None
        approval_rules: ProjectMergeRequestApprovalRuleManager = (
            self._parent.approval_rules
        )
        # update any existing approval rule matching the name
        existing_approval_rules = approval_rules.list(iterator=True)
        for ar in existing_approval_rules:
            if ar.name == approval_rule_name:
                ar.user_ids = data["user_ids"]
                ar.approvals_required = data["approvals_required"]
                ar.group_ids = data["group_ids"]
                ar.usernames = data["usernames"]
                ar.save()
                return ar
        # if there was no rule matching the rule name, create a new one
        return approval_rules.create(data=data, **kwargs)


class ProjectMergeRequestApprovalRule(SaveMixin, ObjectDeleteMixin, RESTObject):
    _repr_attr = "name"


class ProjectMergeRequestApprovalRuleManager(CRUDMixin, RESTManager):
    _path = "/projects/{project_id}/merge_requests/{merge_request_iid}/approval_rules"
    _obj_cls = ProjectMergeRequestApprovalRule
    _from_parent_attrs = {"project_id": "project_id", "merge_request_iid": "iid"}
    _update_attrs = RequiredOptional(
        required=(
            "id",
            "merge_request_iid",
            "name",
            "approvals_required",
        ),
        optional=("user_ids", "group_ids", "usernames"),
    )
    # Important: When approval_project_rule_id is set, the name, users and
    # groups of project-level rule will be copied. The approvals_required
    # specified will be used.
    _create_attrs = RequiredOptional(
        required=("name", "approvals_required"),
        optional=("approval_project_rule_id", "user_ids", "group_ids", "usernames"),
    )

    def get(
        self, id: Union[str, int], lazy: bool = False, **kwargs: Any
    ) -> ProjectMergeRequestApprovalRule:
        return cast(
            ProjectMergeRequestApprovalRule, super().get(id=id, lazy=lazy, **kwargs)
        )


class ProjectMergeRequestApprovalState(RESTObject):
    pass


class ProjectMergeRequestApprovalStateManager(GetWithoutIdMixin, RESTManager):
    _path = "/projects/{project_id}/merge_requests/{mr_iid}/approval_state"
    _obj_cls = ProjectMergeRequestApprovalState
    _from_parent_attrs = {"project_id": "project_id", "mr_iid": "iid"}

    def get(self, **kwargs: Any) -> ProjectMergeRequestApprovalState:
        return cast(ProjectMergeRequestApprovalState, super().get(**kwargs))

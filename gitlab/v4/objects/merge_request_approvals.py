from typing import Any, cast, Dict, List, Optional, TYPE_CHECKING, Union

from gitlab import exceptions as exc
from gitlab.base import RequiredOptional, RESTManager, RESTObject
from gitlab.mixins import (
    CreateMixin,
    DeleteMixin,
    GetWithoutIdMixin,
    ListMixin,
    ObjectDeleteMixin,
    SaveMixin,
    UpdateMixin,
)

__all__ = [
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
    _update_uses_post = True

    def get(
        self, id: Optional[Union[int, str]] = None, **kwargs: Any
    ) -> Optional[ProjectApproval]:
        return cast(Optional[ProjectApproval], super().get(id=id, **kwargs))

    @exc.on_http_error(exc.GitlabUpdateError)
    def set_approvers(
        self,
        approver_ids: Optional[List[int]] = None,
        approver_group_ids: Optional[List[int]] = None,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """Change project-level allowed approvers and approver groups.

        Args:
            approver_ids: User IDs that can approve MRs
            approver_group_ids: Group IDs whose members can approve MRs

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabUpdateError: If the server failed to perform the request

        Returns:
            A dict value of the result
        """
        approver_ids = approver_ids or []
        approver_group_ids = approver_group_ids or []

        if TYPE_CHECKING:
            assert self._parent is not None
        path = f"/projects/{self._parent.encoded_id}/approvers"
        data = {"approver_ids": approver_ids, "approver_group_ids": approver_group_ids}
        result = self.gitlab.http_put(path, post_data=data, **kwargs)
        if TYPE_CHECKING:
            assert isinstance(result, dict)
        return result


class ProjectApprovalRule(SaveMixin, ObjectDeleteMixin, RESTObject):
    _id_attr = "id"


class ProjectApprovalRuleManager(
    ListMixin, CreateMixin, UpdateMixin, DeleteMixin, RESTManager
):
    _path = "/projects/{project_id}/approval_rules"
    _obj_cls = ProjectApprovalRule
    _from_parent_attrs = {"project_id": "id"}
    _create_attrs = RequiredOptional(
        required=("name", "approvals_required"),
        optional=("user_ids", "group_ids", "protected_branch_ids"),
    )


class ProjectMergeRequestApproval(SaveMixin, RESTObject):
    _id_attr = None


class ProjectMergeRequestApprovalManager(GetWithoutIdMixin, UpdateMixin, RESTManager):
    _path = "/projects/{project_id}/merge_requests/{mr_iid}/approvals"
    _obj_cls = ProjectMergeRequestApproval
    _from_parent_attrs = {"project_id": "project_id", "mr_iid": "iid"}
    _update_attrs = RequiredOptional(required=("approvals_required",))
    _update_uses_post = True

    def get(
        self, id: Optional[Union[int, str]] = None, **kwargs: Any
    ) -> Optional[ProjectMergeRequestApproval]:
        return cast(Optional[ProjectMergeRequestApproval], super().get(id=id, **kwargs))

    @exc.on_http_error(exc.GitlabUpdateError)
    def set_approvers(
        self,
        approvals_required: int,
        approver_ids: Optional[List[int]] = None,
        approver_group_ids: Optional[List[int]] = None,
        approval_rule_name: str = "name",
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

        data = {
            "name": approval_rule_name,
            "approvals_required": approvals_required,
            "rule_type": "regular",
            "user_ids": approver_ids,
            "group_ids": approver_group_ids,
        }
        if TYPE_CHECKING:
            assert self._parent is not None
        approval_rules: ProjectMergeRequestApprovalRuleManager = (
            self._parent.approval_rules
        )
        # update any existing approval rule matching the name
        existing_approval_rules = approval_rules.list()
        for ar in existing_approval_rules:
            if ar.name == approval_rule_name:
                ar.user_ids = data["user_ids"]
                ar.approvals_required = data["approvals_required"]
                ar.group_ids = data["group_ids"]
                ar.save()
                return ar
        # if there was no rule matching the rule name, create a new one
        return approval_rules.create(data=data)


class ProjectMergeRequestApprovalRule(SaveMixin, ObjectDeleteMixin, RESTObject):
    _id_attr = "approval_rule_id"
    _short_print_attr = "approval_rule"
    id: int

    @exc.on_http_error(exc.GitlabUpdateError)
    def save(self, **kwargs: Any) -> None:
        """Save the changes made to the object to the server.

        The object is updated to match what the server returns.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raise:
            GitlabAuthenticationError: If authentication is not correct
            GitlabUpdateError: If the server cannot perform the request
        """
        # There is a mismatch between the name of our id attribute and the put
        # REST API name for the project_id, so we override it here.
        self.approval_rule_id = self.id
        self.merge_request_iid = self._parent_attrs["mr_iid"]
        self.id = self._parent_attrs["project_id"]
        # save will update self.id with the result from the server, so no need
        # to overwrite with what it was before we overwrote it.
        SaveMixin.save(self, **kwargs)


class ProjectMergeRequestApprovalRuleManager(
    ListMixin, UpdateMixin, CreateMixin, DeleteMixin, RESTManager
):
    _path = "/projects/{project_id}/merge_requests/{mr_iid}/approval_rules"
    _obj_cls = ProjectMergeRequestApprovalRule
    _from_parent_attrs = {"project_id": "project_id", "mr_iid": "iid"}
    _list_filters = ("name", "rule_type")
    _update_attrs = RequiredOptional(
        required=(
            "id",
            "merge_request_iid",
            "approval_rule_id",
            "name",
            "approvals_required",
        ),
        optional=("user_ids", "group_ids"),
    )
    # Important: When approval_project_rule_id is set, the name, users and
    # groups of project-level rule will be copied. The approvals_required
    # specified will be used.
    _create_attrs = RequiredOptional(
        required=("id", "merge_request_iid", "name", "approvals_required"),
        optional=("approval_project_rule_id", "user_ids", "group_ids"),
    )

    def create(
        self, data: Optional[Dict[str, Any]] = None, **kwargs: Any
    ) -> RESTObject:
        """Create a new object.

        Args:
            data: Parameters to send to the server to create the
                         resource
            **kwargs: Extra options to send to the server (e.g. sudo or
                      'ref_name', 'stage', 'name', 'all')

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabCreateError: If the server cannot perform the request

        Returns:
            A new instance of the manage object class build with
                the data sent by the server
        """
        if TYPE_CHECKING:
            assert data is not None
        new_data = data.copy()
        new_data["id"] = self._from_parent_attrs["project_id"]
        new_data["merge_request_iid"] = self._from_parent_attrs["mr_iid"]
        return CreateMixin.create(self, new_data, **kwargs)


class ProjectMergeRequestApprovalState(RESTObject):
    pass


class ProjectMergeRequestApprovalStateManager(GetWithoutIdMixin, RESTManager):
    _path = "/projects/{project_id}/merge_requests/{mr_iid}/approval_state"
    _obj_cls = ProjectMergeRequestApprovalState
    _from_parent_attrs = {"project_id": "project_id", "mr_iid": "iid"}

    def get(
        self, id: Optional[Union[int, str]] = None, **kwargs: Any
    ) -> Optional[ProjectMergeRequestApprovalState]:
        return cast(
            Optional[ProjectMergeRequestApprovalState], super().get(id=id, **kwargs)
        )

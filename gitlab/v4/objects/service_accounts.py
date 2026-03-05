"""
GitLab API: https://docs.gitlab.com/api/service_accounts/
"""

from gitlab.base import RESTObject
from gitlab.mixins import (
    CreateMixin,
    DeleteMixin,
    ListMixin,
    ObjectDeleteMixin,
    ObjectRotateMixin,
    RotateMixin,
    SaveMixin,
    UpdateMethod,
    UpdateMixin,
)
from gitlab.types import ArrayAttribute, RequiredOptional

__all__ = [
    "ServiceAccount",
    "ServiceAccountManager",
    "GroupServiceAccount",
    "GroupServiceAccountManager",
    "GroupServiceAccountAccessToken",
    "GroupServiceAccountAccessTokenManager",
    "ProjectServiceAccount",
    "ProjectServiceAccountManager",
    "ProjectServiceAccountAccessToken",
    "ProjectServiceAccountAccessTokenManager",
]

_SA_ACCOUNT_ATTRS = RequiredOptional(optional=("name", "username", "email"))

_SA_TOKEN_CREATE_ATTRS = RequiredOptional(
    required=("name", "scopes"), optional=("description", "expires_at")
)

_SA_TOKEN_LIST_FILTERS = (
    "created_after",
    "created_before",
    "expires_after",
    "expires_before",
    "last_used_after",
    "last_used_before",
    "revoked",
    "search",
    "sort",
    "state",
)


# ---------------------------------------------------------------------------
# Instance-level service accounts
# ---------------------------------------------------------------------------


class ServiceAccount(SaveMixin, RESTObject):
    pass


class ServiceAccountManager(
    CreateMixin[ServiceAccount], ListMixin[ServiceAccount], UpdateMixin[ServiceAccount]
):
    _path = "/service_accounts"
    _obj_cls = ServiceAccount
    _create_attrs = _SA_ACCOUNT_ATTRS
    _update_attrs = _SA_ACCOUNT_ATTRS
    _update_method = UpdateMethod.PATCH
    _list_filters = ("order_by", "sort")


# ---------------------------------------------------------------------------
# Group-level service accounts
# ---------------------------------------------------------------------------


class GroupServiceAccountAccessToken(ObjectDeleteMixin, ObjectRotateMixin, RESTObject):
    pass


class GroupServiceAccountAccessTokenManager(
    CreateMixin[GroupServiceAccountAccessToken],
    DeleteMixin[GroupServiceAccountAccessToken],
    ListMixin[GroupServiceAccountAccessToken],
    RotateMixin[GroupServiceAccountAccessToken],
):
    _path = "/groups/{group_id}/service_accounts/{user_id}/personal_access_tokens"
    _obj_cls = GroupServiceAccountAccessToken
    _from_parent_attrs = {"group_id": "group_id", "user_id": "id"}
    _create_attrs = _SA_TOKEN_CREATE_ATTRS
    _types = {"scopes": ArrayAttribute}
    _list_filters = _SA_TOKEN_LIST_FILTERS


class GroupServiceAccount(SaveMixin, ObjectDeleteMixin, RESTObject):
    access_tokens: GroupServiceAccountAccessTokenManager


class GroupServiceAccountManager(
    CreateMixin[GroupServiceAccount],
    DeleteMixin[GroupServiceAccount],
    ListMixin[GroupServiceAccount],
    UpdateMixin[GroupServiceAccount],
):
    _path = "/groups/{group_id}/service_accounts"
    _obj_cls = GroupServiceAccount
    _from_parent_attrs = {"group_id": "id"}
    _create_attrs = _SA_ACCOUNT_ATTRS
    _update_attrs = _SA_ACCOUNT_ATTRS
    _update_method = UpdateMethod.PATCH
    _list_filters = ("order_by", "sort")


# ---------------------------------------------------------------------------
# Project-level service accounts
# ---------------------------------------------------------------------------


class ProjectServiceAccountAccessToken(
    ObjectDeleteMixin, ObjectRotateMixin, RESTObject
):
    pass


class ProjectServiceAccountAccessTokenManager(
    CreateMixin[ProjectServiceAccountAccessToken],
    DeleteMixin[ProjectServiceAccountAccessToken],
    ListMixin[ProjectServiceAccountAccessToken],
    RotateMixin[ProjectServiceAccountAccessToken],
):
    _path = "/projects/{project_id}/service_accounts/{user_id}/personal_access_tokens"
    _obj_cls = ProjectServiceAccountAccessToken
    _from_parent_attrs = {"project_id": "project_id", "user_id": "id"}
    _create_attrs = _SA_TOKEN_CREATE_ATTRS
    _types = {"scopes": ArrayAttribute}
    _list_filters = _SA_TOKEN_LIST_FILTERS


class ProjectServiceAccount(SaveMixin, ObjectDeleteMixin, RESTObject):
    access_tokens: ProjectServiceAccountAccessTokenManager


class ProjectServiceAccountManager(
    CreateMixin[ProjectServiceAccount],
    DeleteMixin[ProjectServiceAccount],
    ListMixin[ProjectServiceAccount],
    UpdateMixin[ProjectServiceAccount],
):
    _path = "/projects/{project_id}/service_accounts"
    _obj_cls = ProjectServiceAccount
    _from_parent_attrs = {"project_id": "id"}
    _create_attrs = _SA_ACCOUNT_ATTRS
    _update_attrs = _SA_ACCOUNT_ATTRS
    _update_method = UpdateMethod.PATCH
    _list_filters = ("order_by", "sort")

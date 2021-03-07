from gitlab.base import RequiredOptional, RESTManager, RESTObject
from gitlab.mixins import CreateMixin, DeleteMixin, ListMixin, ObjectDeleteMixin


__all__ = [
    "DeployToken",
    "DeployTokenManager",
    "GroupDeployToken",
    "GroupDeployTokenManager",
    "ProjectDeployToken",
    "ProjectDeployTokenManager",
]


class DeployToken(ObjectDeleteMixin, RESTObject):
    pass


class DeployTokenManager(ListMixin, RESTManager):
    _path = "/deploy_tokens"
    _obj_cls = DeployToken


class GroupDeployToken(ObjectDeleteMixin, RESTObject):
    pass


class GroupDeployTokenManager(ListMixin, CreateMixin, DeleteMixin, RESTManager):
    _path = "/groups/%(group_id)s/deploy_tokens"
    _from_parent_attrs = {"group_id": "id"}
    _obj_cls = GroupDeployToken
    _create_attrs = RequiredOptional(
        required=(
            "name",
            "scopes",
        ),
        optional=(
            "expires_at",
            "username",
        ),
    )


class ProjectDeployToken(ObjectDeleteMixin, RESTObject):
    pass


class ProjectDeployTokenManager(ListMixin, CreateMixin, DeleteMixin, RESTManager):
    _path = "/projects/%(project_id)s/deploy_tokens"
    _from_parent_attrs = {"project_id": "id"}
    _obj_cls = ProjectDeployToken
    _create_attrs = RequiredOptional(
        required=(
            "name",
            "scopes",
        ),
        optional=(
            "expires_at",
            "username",
        ),
    )

from gitlab.mixins import CreateMixin, DeleteMixin, ListMixin, ObjectDeleteMixin


__all__ = [
    "DeployToken",
    "DeployTokenManager",
    "GroupDeployToken",
    "GroupDeployTokenManager",
    "ProjectDeployToken",
    "ProjectDeployTokenManager",
]


class DeployToken(ObjectDeleteMixin):
    pass


class DeployTokenManager(ListMixin):
    _path = "/deploy_tokens"
    _obj_cls = DeployToken


class GroupDeployToken(ObjectDeleteMixin):
    pass


class GroupDeployTokenManager(ListMixin, CreateMixin, DeleteMixin):
    _path = "/groups/%(group_id)s/deploy_tokens"
    _from_parent_attrs = {"group_id": "id"}
    _obj_cls = GroupDeployToken
    _create_attrs = (
        (
            "name",
            "scopes",
        ),
        (
            "expires_at",
            "username",
        ),
    )


class ProjectDeployToken(ObjectDeleteMixin):
    pass


class ProjectDeployTokenManager(ListMixin, CreateMixin, DeleteMixin):
    _path = "/projects/%(project_id)s/deploy_tokens"
    _from_parent_attrs = {"project_id": "id"}
    _obj_cls = ProjectDeployToken
    _create_attrs = (
        (
            "name",
            "scopes",
        ),
        (
            "expires_at",
            "username",
        ),
    )

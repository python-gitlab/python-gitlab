from gitlab.mixins import CreateMixin, DeleteMixin, ListMixin, ObjectDeleteMixin


__all__ = [
    "ProjectAccessToken",
    "ProjectAccessTokenManager",
]


class ProjectAccessToken(ObjectDeleteMixin):
    pass


class ProjectAccessTokenManager(ListMixin, CreateMixin, DeleteMixin):
    _path = "/projects/%(project_id)s/access_tokens"
    _obj_cls = ProjectAccessToken
    _from_parent_attrs = {"project_id": "id"}

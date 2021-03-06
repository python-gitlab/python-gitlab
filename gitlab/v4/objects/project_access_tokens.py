from gitlab.base import RESTManager, RESTObject
from gitlab.mixins import CreateMixin, DeleteMixin, ListMixin, ObjectDeleteMixin


__all__ = [
    "ProjectAccessToken",
    "ProjectAccessTokenManager",
]


class ProjectAccessToken(ObjectDeleteMixin, RESTObject):
    pass


class ProjectAccessTokenManager(ListMixin, CreateMixin, DeleteMixin, RESTManager):
    _path = "/projects/%(project_id)s/access_tokens"
    _obj_cls = ProjectAccessToken
    _from_parent_attrs = {"project_id": "id"}

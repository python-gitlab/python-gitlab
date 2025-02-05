from gitlab.base import RESTObject
from gitlab.mixins import BadgeRenderMixin, CRUDMixin, ObjectDeleteMixin, SaveMixin
from gitlab.types import RequiredOptional

__all__ = ["GroupBadge", "GroupBadgeManager", "ProjectBadge", "ProjectBadgeManager"]


class GroupBadge(SaveMixin, ObjectDeleteMixin, RESTObject):
    pass


class GroupBadgeManager(BadgeRenderMixin[GroupBadge], CRUDMixin[GroupBadge]):
    _path = "/groups/{group_id}/badges"
    _obj_cls = GroupBadge
    _from_parent_attrs = {"group_id": "id"}
    _create_attrs = RequiredOptional(required=("link_url", "image_url"))
    _update_attrs = RequiredOptional(optional=("link_url", "image_url"))


class ProjectBadge(SaveMixin, ObjectDeleteMixin, RESTObject):
    pass


class ProjectBadgeManager(BadgeRenderMixin[ProjectBadge], CRUDMixin[ProjectBadge]):
    _path = "/projects/{project_id}/badges"
    _obj_cls = ProjectBadge
    _from_parent_attrs = {"project_id": "id"}
    _create_attrs = RequiredOptional(required=("link_url", "image_url"))
    _update_attrs = RequiredOptional(optional=("link_url", "image_url"))

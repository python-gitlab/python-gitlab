from gitlab.base import RequiredOptional, RESTManager, RESTObject
from gitlab.mixins import BadgeRenderMixin, CRUDMixin, ObjectDeleteMixin, SaveMixin


__all__ = [
    "GroupBadge",
    "GroupBadgeManager",
    "ProjectBadge",
    "ProjectBadgeManager",
]


class GroupBadge(SaveMixin, ObjectDeleteMixin, RESTObject):
    pass


class GroupBadgeManager(BadgeRenderMixin, CRUDMixin, RESTManager):
    _path = "/groups/%(group_id)s/badges"
    _obj_cls = GroupBadge
    _from_parent_attrs = {"group_id": "id"}
    _create_attrs = RequiredOptional(required=("link_url", "image_url"))
    _update_attrs = RequiredOptional(optional=("link_url", "image_url"))


class ProjectBadge(SaveMixin, ObjectDeleteMixin, RESTObject):
    pass


class ProjectBadgeManager(BadgeRenderMixin, CRUDMixin, RESTManager):
    _path = "/projects/%(project_id)s/badges"
    _obj_cls = ProjectBadge
    _from_parent_attrs = {"project_id": "id"}
    _create_attrs = RequiredOptional(required=("link_url", "image_url"))
    _update_attrs = RequiredOptional(optional=("link_url", "image_url"))

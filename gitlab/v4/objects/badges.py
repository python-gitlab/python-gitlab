from gitlab.base import *  # noqa
from gitlab.mixins import *  # noqa


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
    _create_attrs = (("link_url", "image_url"), tuple())
    _update_attrs = (tuple(), ("link_url", "image_url"))


class ProjectBadge(SaveMixin, ObjectDeleteMixin, RESTObject):
    pass


class ProjectBadgeManager(BadgeRenderMixin, CRUDMixin, RESTManager):
    _path = "/projects/%(project_id)s/badges"
    _obj_cls = ProjectBadge
    _from_parent_attrs = {"project_id": "id"}
    _create_attrs = (("link_url", "image_url"), tuple())
    _update_attrs = (tuple(), ("link_url", "image_url"))

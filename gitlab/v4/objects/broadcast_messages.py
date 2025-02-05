from gitlab.base import RESTObject
from gitlab.mixins import CRUDMixin, ObjectDeleteMixin, SaveMixin
from gitlab.types import ArrayAttribute, RequiredOptional

__all__ = ["BroadcastMessage", "BroadcastMessageManager"]


class BroadcastMessage(SaveMixin, ObjectDeleteMixin, RESTObject):
    pass


class BroadcastMessageManager(CRUDMixin[BroadcastMessage]):
    _path = "/broadcast_messages"
    _obj_cls = BroadcastMessage

    _create_attrs = RequiredOptional(
        required=("message",),
        optional=("starts_at", "ends_at", "color", "font", "target_access_levels"),
    )
    _update_attrs = RequiredOptional(
        optional=(
            "message",
            "starts_at",
            "ends_at",
            "color",
            "font",
            "target_access_levels",
        )
    )
    _types = {"target_access_levels": ArrayAttribute}

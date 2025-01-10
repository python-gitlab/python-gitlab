"""
GitLab API:
https://docs.gitlab.com/ee/api/audit_events.html
"""

from gitlab.base import RESTObject
from gitlab.mixins import RetrieveMixin

__all__ = [
    "AuditEvent",
    "AuditEventManager",
    "GroupAuditEvent",
    "GroupAuditEventManager",
    "ProjectAuditEvent",
    "ProjectAuditEventManager",
    "ProjectAudit",
    "ProjectAuditManager",
]


class AuditEvent(RESTObject):
    _id_attr = "id"


class AuditEventManager(RetrieveMixin[AuditEvent]):
    _path = "/audit_events"
    _obj_cls = AuditEvent
    _list_filters = ("created_after", "created_before", "entity_type", "entity_id")


class GroupAuditEvent(RESTObject):
    _id_attr = "id"


class GroupAuditEventManager(RetrieveMixin[GroupAuditEvent]):
    _path = "/groups/{group_id}/audit_events"
    _obj_cls = GroupAuditEvent
    _from_parent_attrs = {"group_id": "id"}
    _list_filters = ("created_after", "created_before")


class ProjectAuditEvent(RESTObject):
    _id_attr = "id"


class ProjectAuditEventManager(RetrieveMixin[ProjectAuditEvent]):
    _path = "/projects/{project_id}/audit_events"
    _obj_cls = ProjectAuditEvent
    _from_parent_attrs = {"project_id": "id"}
    _list_filters = ("created_after", "created_before")


class ProjectAudit(ProjectAuditEvent):
    pass


class ProjectAuditManager(ProjectAuditEventManager):
    pass

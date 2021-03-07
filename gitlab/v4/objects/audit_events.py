"""
GitLab API:
https://docs.gitlab.com/ee/api/audit_events.html
"""

from gitlab.base import RESTManager, RESTObject
from gitlab.mixins import RetrieveMixin

__all__ = [
    "AuditEvent",
    "AuditEventManager",
    "ProjectAudit",
    "ProjectAuditManager",
]


class AuditEvent(RESTObject):
    _id_attr = "id"


class AuditEventManager(RetrieveMixin, RESTManager):
    _path = "/audit_events"
    _obj_cls = AuditEvent
    _list_filters = ("created_after", "created_before", "entity_type", "entity_id")


class ProjectAudit(RESTObject):
    _id_attr = "id"


class ProjectAuditManager(RetrieveMixin, RESTManager):
    _path = "/projects/%(project_id)s/audit_events"
    _obj_cls = ProjectAudit
    _from_parent_attrs = {"project_id": "id"}
    _list_filters = ("created_after", "created_before")

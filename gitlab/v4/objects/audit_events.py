"""
GitLab API:
https://docs.gitlab.com/ee/api/audit_events.html#project-audit-events
"""

from gitlab.base import *  # noqa
from gitlab.mixins import *  # noqa

__all__ = [
    "ProjectAudit",
    "ProjectAuditManager",
]


class ProjectAudit(RESTObject):
    _id_attr = "id"


class ProjectAuditManager(RetrieveMixin, RESTManager):
    _path = "/projects/%(project_id)s/audit_events"
    _obj_cls = ProjectAudit
    _from_parent_attrs = {"project_id": "id"}
    _list_filters = ("created_after", "created_before")

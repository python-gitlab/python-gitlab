from gitlab import exceptions as exc
from gitlab.base import *  # noqa
from gitlab.mixins import *  # noqa


class Event(RESTObject):
    _id_attr = None
    _short_print_attr = "target_title"


class EventManager(ListMixin, RESTManager):
    _path = "/events"
    _obj_cls = Event
    _list_filters = ("action", "target_type", "before", "after", "sort")


class AuditEvent(RESTObject):
    _id_attr = "id"


class AuditEventManager(ListMixin, RESTManager):
    _path = "/audit_events"
    _obj_cls = AuditEvent
    _list_filters = ("created_after", "created_before", "entity_type", "entity_id")


class GroupEpicResourceLabelEvent(RESTObject):
    pass


class GroupEpicResourceLabelEventManager(RetrieveMixin, RESTManager):
    _path = "/groups/%(group_id)s/epics/%(epic_id)s/resource_label_events"
    _obj_cls = GroupEpicResourceLabelEvent
    _from_parent_attrs = {"group_id": "group_id", "epic_id": "id"}


class ProjectEvent(Event):
    pass


class ProjectEventManager(EventManager):
    _path = "/projects/%(project_id)s/events"
    _obj_cls = ProjectEvent
    _from_parent_attrs = {"project_id": "id"}


class ProjectIssueResourceLabelEvent(RESTObject):
    pass


class ProjectIssueResourceLabelEventManager(RetrieveMixin, RESTManager):
    _path = "/projects/%(project_id)s/issues/%(issue_iid)s" "/resource_label_events"
    _obj_cls = ProjectIssueResourceLabelEvent
    _from_parent_attrs = {"project_id": "project_id", "issue_iid": "iid"}


class ProjectIssueResourceMilestoneEvent(RESTObject):
    pass


class ProjectIssueResourceMilestoneEventManager(RetrieveMixin, RESTManager):
    _path = "/projects/%(project_id)s/issues/%(issue_iid)s/resource_milestone_events"
    _obj_cls = ProjectIssueResourceMilestoneEvent
    _from_parent_attrs = {"project_id": "project_id", "issue_iid": "iid"}


class ProjectMergeRequestResourceLabelEvent(RESTObject):
    pass


class ProjectMergeRequestResourceLabelEventManager(RetrieveMixin, RESTManager):
    _path = (
        "/projects/%(project_id)s/merge_requests/%(mr_iid)s" "/resource_label_events"
    )
    _obj_cls = ProjectMergeRequestResourceLabelEvent
    _from_parent_attrs = {"project_id": "project_id", "mr_iid": "iid"}


class ProjectMergeRequestResourceMilestoneEvent(RESTObject):
    pass


class ProjectMergeRequestResourceMilestoneEventManager(RetrieveMixin, RESTManager):
    _path = (
        "/projects/%(project_id)s/merge_requests/%(mr_iid)s/resource_milestone_events"
    )
    _obj_cls = ProjectMergeRequestResourceMilestoneEvent
    _from_parent_attrs = {"project_id": "project_id", "mr_iid": "iid"}


class UserEvent(Event):
    pass


class UserEventManager(EventManager):
    _path = "/users/%(user_id)s/events"
    _obj_cls = UserEvent
    _from_parent_attrs = {"user_id": "id"}

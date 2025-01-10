from gitlab.base import RESTObject
from gitlab.mixins import ListMixin, RetrieveMixin

__all__ = [
    "Event",
    "EventManager",
    "GroupEpicResourceLabelEvent",
    "GroupEpicResourceLabelEventManager",
    "ProjectEvent",
    "ProjectEventManager",
    "ProjectIssueResourceLabelEvent",
    "ProjectIssueResourceLabelEventManager",
    "ProjectIssueResourceMilestoneEvent",
    "ProjectIssueResourceMilestoneEventManager",
    "ProjectIssueResourceStateEvent",
    "ProjectIssueResourceIterationEventManager",
    "ProjectIssueResourceWeightEventManager",
    "ProjectIssueResourceIterationEvent",
    "ProjectIssueResourceWeightEvent",
    "ProjectIssueResourceStateEventManager",
    "ProjectMergeRequestResourceLabelEvent",
    "ProjectMergeRequestResourceLabelEventManager",
    "ProjectMergeRequestResourceMilestoneEvent",
    "ProjectMergeRequestResourceMilestoneEventManager",
    "ProjectMergeRequestResourceStateEvent",
    "ProjectMergeRequestResourceStateEventManager",
    "UserEvent",
    "UserEventManager",
]


class Event(RESTObject):
    _id_attr = None
    _repr_attr = "target_title"


class EventManager(ListMixin[Event]):
    _path = "/events"
    _obj_cls = Event
    _list_filters = ("action", "target_type", "before", "after", "sort", "scope")


class GroupEpicResourceLabelEvent(RESTObject):
    pass


class GroupEpicResourceLabelEventManager(RetrieveMixin[GroupEpicResourceLabelEvent]):
    _path = "/groups/{group_id}/epics/{epic_id}/resource_label_events"
    _obj_cls = GroupEpicResourceLabelEvent
    _from_parent_attrs = {"group_id": "group_id", "epic_id": "id"}


class ProjectEvent(Event):
    pass


class ProjectEventManager(EventManager):
    _path = "/projects/{project_id}/events"
    _obj_cls = ProjectEvent
    _from_parent_attrs = {"project_id": "id"}


class ProjectIssueResourceLabelEvent(RESTObject):
    pass


class ProjectIssueResourceLabelEventManager(
    RetrieveMixin[ProjectIssueResourceLabelEvent]
):
    _path = "/projects/{project_id}/issues/{issue_iid}/resource_label_events"
    _obj_cls = ProjectIssueResourceLabelEvent
    _from_parent_attrs = {"project_id": "project_id", "issue_iid": "iid"}


class ProjectIssueResourceMilestoneEvent(RESTObject):
    pass


class ProjectIssueResourceMilestoneEventManager(
    RetrieveMixin[ProjectIssueResourceMilestoneEvent]
):
    _path = "/projects/{project_id}/issues/{issue_iid}/resource_milestone_events"
    _obj_cls = ProjectIssueResourceMilestoneEvent
    _from_parent_attrs = {"project_id": "project_id", "issue_iid": "iid"}


class ProjectIssueResourceStateEvent(RESTObject):
    pass


class ProjectIssueResourceStateEventManager(
    RetrieveMixin[ProjectIssueResourceStateEvent]
):
    _path = "/projects/{project_id}/issues/{issue_iid}/resource_state_events"
    _obj_cls = ProjectIssueResourceStateEvent
    _from_parent_attrs = {"project_id": "project_id", "issue_iid": "iid"}


class ProjectIssueResourceIterationEvent(RESTObject):
    pass


class ProjectIssueResourceIterationEventManager(
    RetrieveMixin[ProjectIssueResourceIterationEvent]
):
    _path = "/projects/{project_id}/issues/{issue_iid}/resource_iteration_events"
    _obj_cls = ProjectIssueResourceIterationEvent
    _from_parent_attrs = {"project_id": "project_id", "issue_iid": "iid"}


class ProjectIssueResourceWeightEvent(RESTObject):
    pass


class ProjectIssueResourceWeightEventManager(
    RetrieveMixin[ProjectIssueResourceWeightEvent]
):
    _path = "/projects/{project_id}/issues/{issue_iid}/resource_weight_events"
    _obj_cls = ProjectIssueResourceWeightEvent
    _from_parent_attrs = {"project_id": "project_id", "issue_iid": "iid"}


class ProjectMergeRequestResourceLabelEvent(RESTObject):
    pass


class ProjectMergeRequestResourceLabelEventManager(
    RetrieveMixin[ProjectMergeRequestResourceLabelEvent]
):
    _path = "/projects/{project_id}/merge_requests/{mr_iid}/resource_label_events"
    _obj_cls = ProjectMergeRequestResourceLabelEvent
    _from_parent_attrs = {"project_id": "project_id", "mr_iid": "iid"}


class ProjectMergeRequestResourceMilestoneEvent(RESTObject):
    pass


class ProjectMergeRequestResourceMilestoneEventManager(
    RetrieveMixin[ProjectMergeRequestResourceMilestoneEvent]
):
    _path = "/projects/{project_id}/merge_requests/{mr_iid}/resource_milestone_events"
    _obj_cls = ProjectMergeRequestResourceMilestoneEvent
    _from_parent_attrs = {"project_id": "project_id", "mr_iid": "iid"}


class ProjectMergeRequestResourceStateEvent(RESTObject):
    pass


class ProjectMergeRequestResourceStateEventManager(
    RetrieveMixin[ProjectMergeRequestResourceStateEvent]
):
    _path = "/projects/{project_id}/merge_requests/{mr_iid}/resource_state_events"
    _obj_cls = ProjectMergeRequestResourceStateEvent
    _from_parent_attrs = {"project_id": "project_id", "mr_iid": "iid"}


class UserEvent(Event):
    pass


class UserEventManager(EventManager):
    _path = "/users/{user_id}/events"
    _obj_cls = UserEvent
    _from_parent_attrs = {"user_id": "id"}

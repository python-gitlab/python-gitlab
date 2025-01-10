from gitlab.base import RESTObject
from gitlab.mixins import NoUpdateMixin, ObjectDeleteMixin
from gitlab.types import RequiredOptional

__all__ = [
    "GroupEpicAwardEmoji",
    "GroupEpicAwardEmojiManager",
    "GroupEpicNoteAwardEmoji",
    "GroupEpicNoteAwardEmojiManager",
    "ProjectIssueAwardEmoji",
    "ProjectIssueAwardEmojiManager",
    "ProjectIssueNoteAwardEmoji",
    "ProjectIssueNoteAwardEmojiManager",
    "ProjectMergeRequestAwardEmoji",
    "ProjectMergeRequestAwardEmojiManager",
    "ProjectMergeRequestNoteAwardEmoji",
    "ProjectMergeRequestNoteAwardEmojiManager",
    "ProjectSnippetAwardEmoji",
    "ProjectSnippetAwardEmojiManager",
    "ProjectSnippetNoteAwardEmoji",
    "ProjectSnippetNoteAwardEmojiManager",
]


class GroupEpicAwardEmoji(ObjectDeleteMixin, RESTObject):
    pass


class GroupEpicAwardEmojiManager(NoUpdateMixin[GroupEpicAwardEmoji]):
    _path = "/groups/{group_id}/epics/{epic_iid}/award_emoji"
    _obj_cls = GroupEpicAwardEmoji
    _from_parent_attrs = {"group_id": "group_id", "epic_iid": "iid"}
    _create_attrs = RequiredOptional(required=("name",))


class GroupEpicNoteAwardEmoji(ObjectDeleteMixin, RESTObject):
    pass


class GroupEpicNoteAwardEmojiManager(NoUpdateMixin[GroupEpicNoteAwardEmoji]):
    _path = "/groups/{group_id}/epics/{epic_iid}/notes/{note_id}/award_emoji"
    _obj_cls = GroupEpicNoteAwardEmoji
    _from_parent_attrs = {
        "group_id": "group_id",
        "epic_iid": "epic_iid",
        "note_id": "id",
    }
    _create_attrs = RequiredOptional(required=("name",))


class ProjectIssueAwardEmoji(ObjectDeleteMixin, RESTObject):
    pass


class ProjectIssueAwardEmojiManager(NoUpdateMixin[ProjectIssueAwardEmoji]):
    _path = "/projects/{project_id}/issues/{issue_iid}/award_emoji"
    _obj_cls = ProjectIssueAwardEmoji
    _from_parent_attrs = {"project_id": "project_id", "issue_iid": "iid"}
    _create_attrs = RequiredOptional(required=("name",))


class ProjectIssueNoteAwardEmoji(ObjectDeleteMixin, RESTObject):
    pass


class ProjectIssueNoteAwardEmojiManager(NoUpdateMixin[ProjectIssueNoteAwardEmoji]):
    _path = "/projects/{project_id}/issues/{issue_iid}/notes/{note_id}/award_emoji"
    _obj_cls = ProjectIssueNoteAwardEmoji
    _from_parent_attrs = {
        "project_id": "project_id",
        "issue_iid": "issue_iid",
        "note_id": "id",
    }
    _create_attrs = RequiredOptional(required=("name",))


class ProjectMergeRequestAwardEmoji(ObjectDeleteMixin, RESTObject):
    pass


class ProjectMergeRequestAwardEmojiManager(
    NoUpdateMixin[ProjectMergeRequestAwardEmoji]
):
    _path = "/projects/{project_id}/merge_requests/{mr_iid}/award_emoji"
    _obj_cls = ProjectMergeRequestAwardEmoji
    _from_parent_attrs = {"project_id": "project_id", "mr_iid": "iid"}
    _create_attrs = RequiredOptional(required=("name",))


class ProjectMergeRequestNoteAwardEmoji(ObjectDeleteMixin, RESTObject):
    pass


class ProjectMergeRequestNoteAwardEmojiManager(
    NoUpdateMixin[ProjectMergeRequestNoteAwardEmoji]
):
    _path = "/projects/{project_id}/merge_requests/{mr_iid}/notes/{note_id}/award_emoji"
    _obj_cls = ProjectMergeRequestNoteAwardEmoji
    _from_parent_attrs = {
        "project_id": "project_id",
        "mr_iid": "mr_iid",
        "note_id": "id",
    }
    _create_attrs = RequiredOptional(required=("name",))


class ProjectSnippetAwardEmoji(ObjectDeleteMixin, RESTObject):
    pass


class ProjectSnippetAwardEmojiManager(NoUpdateMixin[ProjectSnippetAwardEmoji]):
    _path = "/projects/{project_id}/snippets/{snippet_id}/award_emoji"
    _obj_cls = ProjectSnippetAwardEmoji
    _from_parent_attrs = {"project_id": "project_id", "snippet_id": "id"}
    _create_attrs = RequiredOptional(required=("name",))


class ProjectSnippetNoteAwardEmoji(ObjectDeleteMixin, RESTObject):
    pass


class ProjectSnippetNoteAwardEmojiManager(NoUpdateMixin[ProjectSnippetNoteAwardEmoji]):
    _path = "/projects/{project_id}/snippets/{snippet_id}/notes/{note_id}/award_emoji"
    _obj_cls = ProjectSnippetNoteAwardEmoji
    _from_parent_attrs = {
        "project_id": "project_id",
        "snippet_id": "snippet_id",
        "note_id": "id",
    }
    _create_attrs = RequiredOptional(required=("name",))

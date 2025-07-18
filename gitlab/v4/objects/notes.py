from gitlab.base import RESTObject
from gitlab.mixins import (
    CreateMixin,
    CRUDMixin,
    DeleteMixin,
    GetMixin,
    ObjectDeleteMixin,
    RetrieveMixin,
    SaveMixin,
    UpdateMixin,
)
from gitlab.types import RequiredOptional

from .award_emojis import (  # noqa: F401
    GroupEpicNoteAwardEmojiManager,
    ProjectIssueNoteAwardEmojiManager,
    ProjectMergeRequestNoteAwardEmojiManager,
    ProjectSnippetNoteAwardEmojiManager,
)

__all__ = [
    "GroupEpicNote",
    "GroupEpicNoteManager",
    "GroupEpicDiscussionNote",
    "GroupEpicDiscussionNoteManager",
    "ProjectNote",
    "ProjectNoteManager",
    "ProjectCommitDiscussionNote",
    "ProjectCommitDiscussionNoteManager",
    "ProjectIssueNote",
    "ProjectIssueNoteManager",
    "ProjectIssueDiscussionNote",
    "ProjectIssueDiscussionNoteManager",
    "ProjectMergeRequestNote",
    "ProjectMergeRequestNoteManager",
    "ProjectMergeRequestDiscussionNote",
    "ProjectMergeRequestDiscussionNoteManager",
    "ProjectSnippetNote",
    "ProjectSnippetNoteManager",
    "ProjectSnippetDiscussionNote",
    "ProjectSnippetDiscussionNoteManager",
]


class GroupEpicNote(SaveMixin, ObjectDeleteMixin, RESTObject):
    awardemojis: GroupEpicNoteAwardEmojiManager


class GroupEpicNoteManager(CRUDMixin[GroupEpicNote]):
    _path = "/groups/{group_id}/epics/{epic_id}/notes"
    _obj_cls = GroupEpicNote
    _from_parent_attrs = {"group_id": "group_id", "epic_id": "id"}
    _create_attrs = RequiredOptional(required=("body",), optional=("created_at",))
    _update_attrs = RequiredOptional(required=("body",))


class GroupEpicDiscussionNote(SaveMixin, ObjectDeleteMixin, RESTObject):
    pass


class GroupEpicDiscussionNoteManager(
    GetMixin[GroupEpicDiscussionNote],
    CreateMixin[GroupEpicDiscussionNote],
    UpdateMixin[GroupEpicDiscussionNote],
    DeleteMixin[GroupEpicDiscussionNote],
):
    _path = "/groups/{group_id}/epics/{epic_id}/discussions/{discussion_id}/notes"
    _obj_cls = GroupEpicDiscussionNote
    _from_parent_attrs = {
        "group_id": "group_id",
        "epic_id": "epic_id",
        "discussion_id": "id",
    }
    _create_attrs = RequiredOptional(required=("body",), optional=("created_at",))
    _update_attrs = RequiredOptional(required=("body",))


class ProjectNote(RESTObject):
    pass


class ProjectNoteManager(RetrieveMixin[ProjectNote]):
    _path = "/projects/{project_id}/notes"
    _obj_cls = ProjectNote
    _from_parent_attrs = {"project_id": "id"}
    _create_attrs = RequiredOptional(required=("body",))


class ProjectCommitDiscussionNote(SaveMixin, ObjectDeleteMixin, RESTObject):
    pass


class ProjectCommitDiscussionNoteManager(
    GetMixin[ProjectCommitDiscussionNote],
    CreateMixin[ProjectCommitDiscussionNote],
    UpdateMixin[ProjectCommitDiscussionNote],
    DeleteMixin[ProjectCommitDiscussionNote],
):
    _path = (
        "/projects/{project_id}/repository/commits/{commit_id}/"
        "discussions/{discussion_id}/notes"
    )
    _obj_cls = ProjectCommitDiscussionNote
    _from_parent_attrs = {
        "project_id": "project_id",
        "commit_id": "commit_id",
        "discussion_id": "id",
    }
    _create_attrs = RequiredOptional(
        required=("body",), optional=("created_at", "position")
    )
    _update_attrs = RequiredOptional(required=("body",))


class ProjectIssueNote(SaveMixin, ObjectDeleteMixin, RESTObject):
    awardemojis: ProjectIssueNoteAwardEmojiManager


class ProjectIssueNoteManager(CRUDMixin[ProjectIssueNote]):
    _path = "/projects/{project_id}/issues/{issue_iid}/notes"
    _obj_cls = ProjectIssueNote
    _from_parent_attrs = {"project_id": "project_id", "issue_iid": "iid"}
    _create_attrs = RequiredOptional(required=("body",), optional=("created_at",))
    _update_attrs = RequiredOptional(required=("body",))


class ProjectIssueDiscussionNote(SaveMixin, ObjectDeleteMixin, RESTObject):
    pass


class ProjectIssueDiscussionNoteManager(CRUDMixin[ProjectIssueDiscussionNote]):
    _path = (
        "/projects/{project_id}/issues/{issue_iid}/discussions/{discussion_id}/notes"
    )
    _obj_cls = ProjectIssueDiscussionNote
    _from_parent_attrs = {
        "project_id": "project_id",
        "issue_iid": "issue_iid",
        "discussion_id": "id",
    }
    _create_attrs = RequiredOptional(required=("body",), optional=("created_at",))
    _update_attrs = RequiredOptional(required=("body",))


class ProjectMergeRequestNote(SaveMixin, ObjectDeleteMixin, RESTObject):
    awardemojis: ProjectMergeRequestNoteAwardEmojiManager


class ProjectMergeRequestNoteManager(CRUDMixin[ProjectMergeRequestNote]):
    _path = "/projects/{project_id}/merge_requests/{mr_iid}/notes"
    _obj_cls = ProjectMergeRequestNote
    _from_parent_attrs = {"project_id": "project_id", "mr_iid": "iid"}
    _create_attrs = RequiredOptional(required=("body",))
    _update_attrs = RequiredOptional(required=("body",))


class ProjectMergeRequestDiscussionNote(SaveMixin, ObjectDeleteMixin, RESTObject):
    pass


class ProjectMergeRequestDiscussionNoteManager(
    CRUDMixin[ProjectMergeRequestDiscussionNote]
):
    _path = (
        "/projects/{project_id}/merge_requests/{mr_iid}/"
        "discussions/{discussion_id}/notes"
    )
    _obj_cls = ProjectMergeRequestDiscussionNote
    _from_parent_attrs = {
        "project_id": "project_id",
        "mr_iid": "mr_iid",
        "discussion_id": "id",
    }
    _create_attrs = RequiredOptional(required=("body",), optional=("created_at",))
    _update_attrs = RequiredOptional(required=("body",))


class ProjectSnippetNote(SaveMixin, ObjectDeleteMixin, RESTObject):
    awardemojis: ProjectSnippetNoteAwardEmojiManager


class ProjectSnippetNoteManager(CRUDMixin[ProjectSnippetNote]):
    _path = "/projects/{project_id}/snippets/{snippet_id}/notes"
    _obj_cls = ProjectSnippetNote
    _from_parent_attrs = {"project_id": "project_id", "snippet_id": "id"}
    _create_attrs = RequiredOptional(required=("body",))
    _update_attrs = RequiredOptional(required=("body",))


class ProjectSnippetDiscussionNote(SaveMixin, ObjectDeleteMixin, RESTObject):
    pass


class ProjectSnippetDiscussionNoteManager(
    GetMixin[ProjectSnippetDiscussionNote],
    CreateMixin[ProjectSnippetDiscussionNote],
    UpdateMixin[ProjectSnippetDiscussionNote],
    DeleteMixin[ProjectSnippetDiscussionNote],
):
    _path = (
        "/projects/{project_id}/snippets/{snippet_id}/"
        "discussions/{discussion_id}/notes"
    )
    _obj_cls = ProjectSnippetDiscussionNote
    _from_parent_attrs = {
        "project_id": "project_id",
        "snippet_id": "snippet_id",
        "discussion_id": "id",
    }
    _create_attrs = RequiredOptional(required=("body",), optional=("created_at",))
    _update_attrs = RequiredOptional(required=("body",))

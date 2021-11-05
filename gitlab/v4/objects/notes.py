from gitlab.base import RequiredOptional, RESTManager, RESTObject
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

from .award_emojis import (  # noqa: F401
    ProjectIssueNoteAwardEmojiManager,
    ProjectMergeRequestNoteAwardEmojiManager,
    ProjectSnippetNoteAwardEmojiManager,
)

__all__ = [
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


class ProjectNote(RESTObject):
    pass


class ProjectNoteManager(RetrieveMixin, RESTManager):
    _path = "/projects/{project_id}/notes"
    _obj_cls = ProjectNote
    _from_parent_attrs = {"project_id": "id"}
    _create_attrs = RequiredOptional(required=("body",))


class ProjectCommitDiscussionNote(SaveMixin, ObjectDeleteMixin, RESTObject):
    pass


class ProjectCommitDiscussionNoteManager(
    GetMixin, CreateMixin, UpdateMixin, DeleteMixin, RESTManager
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


class ProjectIssueNoteManager(CRUDMixin, RESTManager):
    _path = "/projects/{project_id}/issues/{issue_iid}/notes"
    _obj_cls = ProjectIssueNote
    _from_parent_attrs = {"project_id": "project_id", "issue_iid": "iid"}
    _create_attrs = RequiredOptional(required=("body",), optional=("created_at",))
    _update_attrs = RequiredOptional(required=("body",))


class ProjectIssueDiscussionNote(SaveMixin, ObjectDeleteMixin, RESTObject):
    pass


class ProjectIssueDiscussionNoteManager(
    GetMixin, CreateMixin, UpdateMixin, DeleteMixin, RESTManager
):
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


class ProjectMergeRequestNoteManager(CRUDMixin, RESTManager):
    _path = "/projects/{project_id}/merge_requests/{mr_iid}/notes"
    _obj_cls = ProjectMergeRequestNote
    _from_parent_attrs = {"project_id": "project_id", "mr_iid": "iid"}
    _create_attrs = RequiredOptional(required=("body",))
    _update_attrs = RequiredOptional(required=("body",))


class ProjectMergeRequestDiscussionNote(SaveMixin, ObjectDeleteMixin, RESTObject):
    pass


class ProjectMergeRequestDiscussionNoteManager(
    GetMixin, CreateMixin, UpdateMixin, DeleteMixin, RESTManager
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
    awardemojis: ProjectMergeRequestNoteAwardEmojiManager


class ProjectSnippetNoteManager(CRUDMixin, RESTManager):
    _path = "/projects/{project_id}/snippets/{snippet_id}/notes"
    _obj_cls = ProjectSnippetNote
    _from_parent_attrs = {"project_id": "project_id", "snippet_id": "id"}
    _create_attrs = RequiredOptional(required=("body",))
    _update_attrs = RequiredOptional(required=("body",))


class ProjectSnippetDiscussionNote(SaveMixin, ObjectDeleteMixin, RESTObject):
    pass


class ProjectSnippetDiscussionNoteManager(
    GetMixin, CreateMixin, UpdateMixin, DeleteMixin, RESTManager
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

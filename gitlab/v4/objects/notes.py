from gitlab import cli
from gitlab import exceptions as exc
from gitlab.base import RESTObject
from gitlab.mixins import (
    CRUDMixin,
    CreateMixin,
    DeleteMixin,
    GetMixin,
    ObjectDeleteMixin,
    RetrieveMixin,
    SaveMixin,
    UpdateMixin,
)
from .award_emojis import (
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


class ProjectNoteManager(RetrieveMixin):
    _path = "/projects/%(project_id)s/notes"
    _obj_cls = ProjectNote
    _from_parent_attrs = {"project_id": "id"}
    _create_attrs = (("body",), tuple())


class ProjectCommitDiscussionNote(SaveMixin, ObjectDeleteMixin):
    pass


class ProjectCommitDiscussionNoteManager(
    GetMixin, CreateMixin, UpdateMixin, DeleteMixin
):
    _path = (
        "/projects/%(project_id)s/repository/commits/%(commit_id)s/"
        "discussions/%(discussion_id)s/notes"
    )
    _obj_cls = ProjectCommitDiscussionNote
    _from_parent_attrs = {
        "project_id": "project_id",
        "commit_id": "commit_id",
        "discussion_id": "id",
    }
    _create_attrs = (("body",), ("created_at", "position"))
    _update_attrs = (("body",), tuple())


class ProjectIssueNote(SaveMixin, ObjectDeleteMixin):
    _managers = (("awardemojis", "ProjectIssueNoteAwardEmojiManager"),)


class ProjectIssueNoteManager(CRUDMixin):
    _path = "/projects/%(project_id)s/issues/%(issue_iid)s/notes"
    _obj_cls = ProjectIssueNote
    _from_parent_attrs = {"project_id": "project_id", "issue_iid": "iid"}
    _create_attrs = (("body",), ("created_at",))
    _update_attrs = (("body",), tuple())


class ProjectIssueDiscussionNote(SaveMixin, ObjectDeleteMixin):
    pass


class ProjectIssueDiscussionNoteManager(
    GetMixin, CreateMixin, UpdateMixin, DeleteMixin
):
    _path = (
        "/projects/%(project_id)s/issues/%(issue_iid)s/"
        "discussions/%(discussion_id)s/notes"
    )
    _obj_cls = ProjectIssueDiscussionNote
    _from_parent_attrs = {
        "project_id": "project_id",
        "issue_iid": "issue_iid",
        "discussion_id": "id",
    }
    _create_attrs = (("body",), ("created_at",))
    _update_attrs = (("body",), tuple())


class ProjectMergeRequestNote(SaveMixin, ObjectDeleteMixin):
    _managers = (("awardemojis", "ProjectMergeRequestNoteAwardEmojiManager"),)


class ProjectMergeRequestNoteManager(CRUDMixin):
    _path = "/projects/%(project_id)s/merge_requests/%(mr_iid)s/notes"
    _obj_cls = ProjectMergeRequestNote
    _from_parent_attrs = {"project_id": "project_id", "mr_iid": "iid"}
    _create_attrs = (("body",), tuple())
    _update_attrs = (("body",), tuple())


class ProjectMergeRequestDiscussionNote(SaveMixin, ObjectDeleteMixin):
    pass


class ProjectMergeRequestDiscussionNoteManager(
    GetMixin, CreateMixin, UpdateMixin, DeleteMixin
):
    _path = (
        "/projects/%(project_id)s/merge_requests/%(mr_iid)s/"
        "discussions/%(discussion_id)s/notes"
    )
    _obj_cls = ProjectMergeRequestDiscussionNote
    _from_parent_attrs = {
        "project_id": "project_id",
        "mr_iid": "mr_iid",
        "discussion_id": "id",
    }
    _create_attrs = (("body",), ("created_at",))
    _update_attrs = (("body",), tuple())


class ProjectSnippetNote(SaveMixin, ObjectDeleteMixin):
    _managers = (("awardemojis", "ProjectSnippetNoteAwardEmojiManager"),)


class ProjectSnippetNoteManager(CRUDMixin):
    _path = "/projects/%(project_id)s/snippets/%(snippet_id)s/notes"
    _obj_cls = ProjectSnippetNote
    _from_parent_attrs = {"project_id": "project_id", "snippet_id": "id"}
    _create_attrs = (("body",), tuple())
    _update_attrs = (("body",), tuple())


class ProjectSnippetDiscussionNote(SaveMixin, ObjectDeleteMixin):
    pass


class ProjectSnippetDiscussionNoteManager(
    GetMixin, CreateMixin, UpdateMixin, DeleteMixin
):
    _path = (
        "/projects/%(project_id)s/snippets/%(snippet_id)s/"
        "discussions/%(discussion_id)s/notes"
    )
    _obj_cls = ProjectSnippetDiscussionNote
    _from_parent_attrs = {
        "project_id": "project_id",
        "snippet_id": "snippet_id",
        "discussion_id": "id",
    }
    _create_attrs = (("body",), ("created_at",))
    _update_attrs = (("body",), tuple())

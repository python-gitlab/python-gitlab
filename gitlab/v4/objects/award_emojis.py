from gitlab.base import RequiredOptional, RESTManager, RESTObject
from gitlab.mixins import NoUpdateMixin, ObjectDeleteMixin


__all__ = [
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


class ProjectIssueAwardEmoji(ObjectDeleteMixin, RESTObject):
    pass


class ProjectIssueAwardEmojiManager(NoUpdateMixin, RESTManager):
    _path = "/projects/%(project_id)s/issues/%(issue_iid)s/award_emoji"
    _obj_cls = ProjectIssueAwardEmoji
    _from_parent_attrs = {"project_id": "project_id", "issue_iid": "iid"}
    _create_attrs = RequiredOptional(required=("name",))


class ProjectIssueNoteAwardEmoji(ObjectDeleteMixin, RESTObject):
    pass


class ProjectIssueNoteAwardEmojiManager(NoUpdateMixin, RESTManager):
    _path = (
        "/projects/%(project_id)s/issues/%(issue_iid)s" "/notes/%(note_id)s/award_emoji"
    )
    _obj_cls = ProjectIssueNoteAwardEmoji
    _from_parent_attrs = {
        "project_id": "project_id",
        "issue_iid": "issue_iid",
        "note_id": "id",
    }
    _create_attrs = RequiredOptional(required=("name",))


class ProjectMergeRequestAwardEmoji(ObjectDeleteMixin, RESTObject):
    pass


class ProjectMergeRequestAwardEmojiManager(NoUpdateMixin, RESTManager):
    _path = "/projects/%(project_id)s/merge_requests/%(mr_iid)s/award_emoji"
    _obj_cls = ProjectMergeRequestAwardEmoji
    _from_parent_attrs = {"project_id": "project_id", "mr_iid": "iid"}
    _create_attrs = RequiredOptional(required=("name",))


class ProjectMergeRequestNoteAwardEmoji(ObjectDeleteMixin, RESTObject):
    pass


class ProjectMergeRequestNoteAwardEmojiManager(NoUpdateMixin, RESTManager):
    _path = (
        "/projects/%(project_id)s/merge_requests/%(mr_iid)s"
        "/notes/%(note_id)s/award_emoji"
    )
    _obj_cls = ProjectMergeRequestNoteAwardEmoji
    _from_parent_attrs = {
        "project_id": "project_id",
        "mr_iid": "mr_iid",
        "note_id": "id",
    }
    _create_attrs = RequiredOptional(required=("name",))


class ProjectSnippetAwardEmoji(ObjectDeleteMixin, RESTObject):
    pass


class ProjectSnippetAwardEmojiManager(NoUpdateMixin, RESTManager):
    _path = "/projects/%(project_id)s/snippets/%(snippet_id)s/award_emoji"
    _obj_cls = ProjectSnippetAwardEmoji
    _from_parent_attrs = {"project_id": "project_id", "snippet_id": "id"}
    _create_attrs = RequiredOptional(required=("name",))


class ProjectSnippetNoteAwardEmoji(ObjectDeleteMixin, RESTObject):
    pass


class ProjectSnippetNoteAwardEmojiManager(NoUpdateMixin, RESTManager):
    _path = (
        "/projects/%(project_id)s/snippets/%(snippet_id)s"
        "/notes/%(note_id)s/award_emoji"
    )
    _obj_cls = ProjectSnippetNoteAwardEmoji
    _from_parent_attrs = {
        "project_id": "project_id",
        "snippet_id": "snippet_id",
        "note_id": "id",
    }
    _create_attrs = RequiredOptional(required=("name",))

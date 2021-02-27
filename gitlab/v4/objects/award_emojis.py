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


class ProjectIssueAwardEmoji(ObjectDeleteMixin):
    pass


class ProjectIssueAwardEmojiManager(NoUpdateMixin):
    _path = "/projects/%(project_id)s/issues/%(issue_iid)s/award_emoji"
    _obj_cls = ProjectIssueAwardEmoji
    _from_parent_attrs = {"project_id": "project_id", "issue_iid": "iid"}
    _create_attrs = (("name",), tuple())


class ProjectIssueNoteAwardEmoji(ObjectDeleteMixin):
    pass


class ProjectIssueNoteAwardEmojiManager(NoUpdateMixin):
    _path = (
        "/projects/%(project_id)s/issues/%(issue_iid)s" "/notes/%(note_id)s/award_emoji"
    )
    _obj_cls = ProjectIssueNoteAwardEmoji
    _from_parent_attrs = {
        "project_id": "project_id",
        "issue_iid": "issue_iid",
        "note_id": "id",
    }
    _create_attrs = (("name",), tuple())


class ProjectMergeRequestAwardEmoji(ObjectDeleteMixin):
    pass


class ProjectMergeRequestAwardEmojiManager(NoUpdateMixin):
    _path = "/projects/%(project_id)s/merge_requests/%(mr_iid)s/award_emoji"
    _obj_cls = ProjectMergeRequestAwardEmoji
    _from_parent_attrs = {"project_id": "project_id", "mr_iid": "iid"}
    _create_attrs = (("name",), tuple())


class ProjectMergeRequestNoteAwardEmoji(ObjectDeleteMixin):
    pass


class ProjectMergeRequestNoteAwardEmojiManager(NoUpdateMixin):
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
    _create_attrs = (("name",), tuple())


class ProjectSnippetAwardEmoji(ObjectDeleteMixin):
    pass


class ProjectSnippetAwardEmojiManager(NoUpdateMixin):
    _path = "/projects/%(project_id)s/snippets/%(snippet_id)s/award_emoji"
    _obj_cls = ProjectSnippetAwardEmoji
    _from_parent_attrs = {"project_id": "project_id", "snippet_id": "id"}
    _create_attrs = (("name",), tuple())


class ProjectSnippetNoteAwardEmoji(ObjectDeleteMixin):
    pass


class ProjectSnippetNoteAwardEmojiManager(NoUpdateMixin):
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
    _create_attrs = (("name",), tuple())

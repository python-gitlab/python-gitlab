from gitlab.base import *  # noqa
from gitlab.mixins import *  # noqa
from .notes import (
    ProjectCommitDiscussionNoteManager,
    ProjectIssueDiscussionNoteManager,
    ProjectMergeRequestDiscussionNoteManager,
    ProjectSnippetDiscussionNoteManager,
)


class ProjectCommitDiscussion(RESTObject):
    _managers = (("notes", "ProjectCommitDiscussionNoteManager"),)


class ProjectCommitDiscussionManager(RetrieveMixin, CreateMixin, RESTManager):
    _path = "/projects/%(project_id)s/repository/commits/%(commit_id)s/" "discussions"
    _obj_cls = ProjectCommitDiscussion
    _from_parent_attrs = {"project_id": "project_id", "commit_id": "id"}
    _create_attrs = (("body",), ("created_at",))


class ProjectIssueDiscussion(RESTObject):
    _managers = (("notes", "ProjectIssueDiscussionNoteManager"),)


class ProjectIssueDiscussionManager(RetrieveMixin, CreateMixin, RESTManager):
    _path = "/projects/%(project_id)s/issues/%(issue_iid)s/discussions"
    _obj_cls = ProjectIssueDiscussion
    _from_parent_attrs = {"project_id": "project_id", "issue_iid": "iid"}
    _create_attrs = (("body",), ("created_at",))


class ProjectMergeRequestDiscussion(SaveMixin, RESTObject):
    _managers = (("notes", "ProjectMergeRequestDiscussionNoteManager"),)


class ProjectMergeRequestDiscussionManager(
    RetrieveMixin, CreateMixin, UpdateMixin, RESTManager
):
    _path = "/projects/%(project_id)s/merge_requests/%(mr_iid)s/discussions"
    _obj_cls = ProjectMergeRequestDiscussion
    _from_parent_attrs = {"project_id": "project_id", "mr_iid": "iid"}
    _create_attrs = (("body",), ("created_at", "position"))
    _update_attrs = (("resolved",), tuple())


class ProjectSnippetDiscussion(RESTObject):
    _managers = (("notes", "ProjectSnippetDiscussionNoteManager"),)


class ProjectSnippetDiscussionManager(RetrieveMixin, CreateMixin, RESTManager):
    _path = "/projects/%(project_id)s/snippets/%(snippet_id)s/discussions"
    _obj_cls = ProjectSnippetDiscussion
    _from_parent_attrs = {"project_id": "project_id", "snippet_id": "id"}
    _create_attrs = (("body",), ("created_at",))

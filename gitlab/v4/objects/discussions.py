from gitlab.base import RESTObject
from gitlab.mixins import CreateMixin, RetrieveMixin, SaveMixin, UpdateMixin
from gitlab.types import RequiredOptional

from .notes import (  # noqa: F401
    ProjectCommitDiscussionNoteManager,
    ProjectIssueDiscussionNoteManager,
    ProjectMergeRequestDiscussionNoteManager,
    ProjectSnippetDiscussionNoteManager,
)

__all__ = [
    "ProjectCommitDiscussion",
    "ProjectCommitDiscussionManager",
    "ProjectIssueDiscussion",
    "ProjectIssueDiscussionManager",
    "ProjectMergeRequestDiscussion",
    "ProjectMergeRequestDiscussionManager",
    "ProjectSnippetDiscussion",
    "ProjectSnippetDiscussionManager",
]


class ProjectCommitDiscussion(RESTObject):
    notes: ProjectCommitDiscussionNoteManager


class ProjectCommitDiscussionManager(
    RetrieveMixin[ProjectCommitDiscussion], CreateMixin[ProjectCommitDiscussion]
):
    _path = "/projects/{project_id}/repository/commits/{commit_id}/discussions"
    _obj_cls = ProjectCommitDiscussion
    _from_parent_attrs = {"project_id": "project_id", "commit_id": "id"}
    _create_attrs = RequiredOptional(required=("body",), optional=("created_at",))


class ProjectIssueDiscussion(RESTObject):
    notes: ProjectIssueDiscussionNoteManager


class ProjectIssueDiscussionManager(
    RetrieveMixin[ProjectIssueDiscussion], CreateMixin[ProjectIssueDiscussion]
):
    _path = "/projects/{project_id}/issues/{issue_iid}/discussions"
    _obj_cls = ProjectIssueDiscussion
    _from_parent_attrs = {"project_id": "project_id", "issue_iid": "iid"}
    _create_attrs = RequiredOptional(required=("body",), optional=("created_at",))


class ProjectMergeRequestDiscussion(SaveMixin, RESTObject):
    notes: ProjectMergeRequestDiscussionNoteManager


class ProjectMergeRequestDiscussionManager(
    RetrieveMixin[ProjectMergeRequestDiscussion],
    CreateMixin[ProjectMergeRequestDiscussion],
    UpdateMixin[ProjectMergeRequestDiscussion],
):
    _path = "/projects/{project_id}/merge_requests/{mr_iid}/discussions"
    _obj_cls = ProjectMergeRequestDiscussion
    _from_parent_attrs = {"project_id": "project_id", "mr_iid": "iid"}
    _create_attrs = RequiredOptional(
        required=("body",), optional=("created_at", "position")
    )
    _update_attrs = RequiredOptional(required=("resolved",))


class ProjectSnippetDiscussion(RESTObject):
    notes: ProjectSnippetDiscussionNoteManager


class ProjectSnippetDiscussionManager(
    RetrieveMixin[ProjectSnippetDiscussion], CreateMixin[ProjectSnippetDiscussion]
):
    _path = "/projects/{project_id}/snippets/{snippet_id}/discussions"
    _obj_cls = ProjectSnippetDiscussion
    _from_parent_attrs = {"project_id": "project_id", "snippet_id": "id"}
    _create_attrs = RequiredOptional(required=("body",), optional=("created_at",))

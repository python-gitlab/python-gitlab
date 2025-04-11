from typing import Any

from gitlab.base import RESTObject
from gitlab.mixins import CRUDMixin, ObjectDeleteMixin, SaveMixin
from gitlab.types import RequiredOptional

__all__ = ["ProjectMergeRequestDraftNote", "ProjectMergeRequestDraftNoteManager"]


class ProjectMergeRequestDraftNote(ObjectDeleteMixin, SaveMixin, RESTObject):
    def publish(self, **kwargs: Any) -> None:
        path = f"{self.manager.path}/{self.encoded_id}/publish"
        self.manager.gitlab.http_put(path, **kwargs)


class ProjectMergeRequestDraftNoteManager(CRUDMixin[ProjectMergeRequestDraftNote]):
    _path = "/projects/{project_id}/merge_requests/{mr_iid}/draft_notes"
    _obj_cls = ProjectMergeRequestDraftNote
    _from_parent_attrs = {"project_id": "project_id", "mr_iid": "iid"}
    _create_attrs = RequiredOptional(
        required=("note",),
        optional=(
            "commit_id",
            "in_reply_to_discussion_id",
            "position",
            "resolve_discussion",
        ),
    )
    _update_attrs = RequiredOptional(optional=("position",))

    def bulk_publish(self, **kwargs: Any) -> None:
        path = f"{self.path}/bulk_publish"
        self.gitlab.http_post(path, **kwargs)

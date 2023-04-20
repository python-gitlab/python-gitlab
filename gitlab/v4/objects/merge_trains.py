from gitlab.base import RESTManager, RESTObject
from gitlab.mixins import ListMixin
from gitlab import cli
from gitlab import exceptions as exc
from typing import Any, Dict, Optional, Union

import requests

__all__ = [
    "ProjectMergeTrain",
    "ProjectMergeTrainManager",
    "ProjectMergeTrainMergeRequest",
    "ProjectMergeTrainMergeRequestManager",
]


class ProjectMergeTrain(RESTObject):
    pass


class ProjectMergeTrainMergeRequest(RESTObject):
    _id_attr = "merge_request_iid"


class ProjectMergeTrainManager(ListMixin, RESTManager):
    _path = "/projects/{project_id}/merge_trains"
    _obj_cls = ProjectMergeTrain
    _from_parent_attrs = {"project_id": "id"}
    _list_filters = ("scope",)


class ProjectMergeTrainMergeRequestManager(RESTManager):
    _path = "/projects/{project_id}/merge_trains"
    _obj_cls = ProjectMergeTrainMergeRequest
    _from_parent_attrs = {"project_id": "id"}

    @cli.register_custom_action(
        "ProjectMergeTrainMergeRequestManager",
        (),
        (
            "when_pipeline_succeeds",
            "squash",
            "sha",
        )

    )
    @exc.on_http_error(exc.GitlabCreateError)
    def add(
            self,
            merge_request_iid: Union[str, int],
            when_pipeline_succeeds: Optional[bool] = None,
            squash: Optional[bool] = None,
            **kwargs: Any
    ) -> Union[Dict[str, Any], requests.Response]:
        """Attempt to merge changes between source and target branches into
            `/projects/:id/merge_trains/merge_requests/:merge_request_iid`.

        Args:
            merge_request_iid: merge request id of the MR
            when_pipeline_succeeds: if true, the merge request is added to the merge train when the pipeline succeeds.
                                    When false or unspecified, the merge request is added directly to the merge train.
            squash: If true, the commits are squashed into a single commit on merge.
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabCreateError: If cannot add mr to merge train
        """
        path = (
            f"{self.path}/merge_requests/{merge_request_iid}"
        )
        data: Dict[str, Any] = {}
        if when_pipeline_succeeds:
            data["when_pipeline_succeeds"] = True
        if squash:
            data["squash"] = True
        return self.gitlab.http_post(path, post_data=data, **kwargs)

    @cli.register_custom_action("ProjectMergeTrainMergeRequestManager")
    @exc.on_http_error(exc.GitlabGetError)
    def get_mr(self, merge_request_iid: Union[str, int],  **kwargs: Any) -> Union[Dict[str, Any], requests.Response]:
        """Attempt to merge changes between source and target branches into
            `/projects/:id/merge_trains/merge_requests/:merge_request_iid`.

        Args:
            merge_request_iid: merge request id of the MR
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabGetError: If cannot be merged
        """
        path = f"{self.path}/merge_requests/{merge_request_iid}"
        return self.gitlab.http_get(path, **kwargs)

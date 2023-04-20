from gitlab.base import RESTManager, RESTObject
from gitlab.mixins import ListMixin
from gitlab import cli
from gitlab import exceptions as exc
from typing import Any, cast, Dict, Optional, TYPE_CHECKING, Union
from gitlab.types import RequiredOptional

import requests

__all__ = [
    "ProjectMergeTrain",
    "ProjectMergeTrainManager",
    # "ProjectMergeTrainMergeRequest",
    # "ProjectMergeTrainMergeRequestManager",
]


class ProjectMergeTrain(RESTObject):
    _path = "/projects/{project_id}/merge_trains"

    @cli.register_custom_action("ProjectMergeTrain")
    def add(self,  **kwargs: Any) -> Union[Dict[str, Any], requests.Response]:
        """Attempt to merge changes between source and target branches into
            `/projects/:id/merge_trains/merge_requests/:merge_request_iid`.

        Args:
            merge_request_iid: merge request id of the MR
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabGetError: If cannot be merged
        """
        path = (
            f"{self.manager.path}/merge_requests/{self.encoded_id}"
        )
        data: Dict[str, Any] = {}
        data["when_pipeline_succeeds"] = True
        return self.manager.gitlab.http_post(path, post_data=data, **kwargs)

    @cli.register_custom_action("ProjectMergeTrain")
    def get_mr(self, **kwargs: Any) -> Union[Dict[str, Any], requests.Response]:
        """Attempt to merge changes between source and target branches into
            `/projects/:id/merge_trains/merge_requests/:merge_request_iid`.

        Args:
            merge_request_iid: merge request id of the MR
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabGetError: If cannot be merged
        """
        path = f"{self.manager.path}/merge_requests/{self.encoded_id}"
        return self.manager.gitlab.http_get(path, **kwargs)


# class ProjectMergeTrainMergeRequest(ListMixin, RESTObject, RESTManager):
#     _path = "/projects/{project_id}/merge_trains/merge_requests"
#     _from_parent_attrs = {"project_id": "id"}
#     _optional_get_attrs = (
#         "when_pipeline_succeeds",
#         "sha",
#         "squash"
#     )

class ProjectMergeTrainManager(ListMixin, RESTManager, ProjectMergeTrain):
    _path = "/projects/{project_id}/merge_trains"
    _obj_cls = ProjectMergeTrain
    _from_parent_attrs = {"project_id": "id"}
    _list_filters = ("scope",)
    _update_attrs = RequiredOptional(optional=("when_pipeline_succeeds", "squash",))
    _optional_get_attrs = (
                                      "when_pipeline_succeeds",
                                      "sha",
                                      "squash"
                                  )


#     @exc.on_http_error(exc.GitlabGetError)
#     def get(self, id: Union[str, int], **kwargs: Any) -> Union[Dict[str, Any], requests.Response]:
#         """Attempt to merge changes between source and target branches into
#             `/projects/:id/merge_trains/merge_requests/:merge_request_iid`.
#
#         Args:
#             merge_request_iid: merge request id of the MR
#             **kwargs: Extra options to send to the server (e.g. sudo)
#
#         Raises:
#             GitlabGetError: If cannot be merged
#         """
#         path = f"{self.manager.path}/merge_requests/{id}"
#         return self.manager.gitlab.http_get(path, **kwargs)
#
#     #@cli.register_custom_action("ProjectMergeTrain")
#     @exc.on_http_error(exc.GitlabGetError)
#     def add(self, id: Union[str, int],  **kwargs: Any) -> Union[Dict[str, Any], requests.Response]:
#         """Attempt to merge changes between source and target branches into
#             `/projects/:id/merge_trains/merge_requests/:merge_request_iid`.
#
#         Args:
#             merge_request_iid: merge request id of the MR
#             **kwargs: Extra options to send to the server (e.g. sudo)
#
#         Raises:
#             GitlabGetError: If cannot be merged
#         """
#         path = f"{self.manager.path}/merge_requests/{id}"
#         return self.manager.gitlab.http_post(path, **kwargs)
#
#
# # class ProjectMergeTrainMergeRequestManager(ProjectMergeTrainMergeRequest):
# #     pass
#
#
#
# #
# # class ProjectMergeTrainMergeRequestManager(ListMixin, RESTManager):
# #     _path = "/projects/{project_id}/merge_trains/merge_request"
# #
# #
# #
# #     @cli.register_custom_action("MergeTrain", ("merge_request_iid",))
#     @exc.on_http_error(exc.GitlabDeleteError)
#     def unshare(self, group_id: int, **kwargs: Any) -> None:
#         """Delete a shared project link within a group.
#
#         Args:
#             group_id: ID of the group.
#             **kwargs: Extra options to send to the server (e.g. sudo)
#
#         Raises:
#             GitlabAuthenticationError: If authentication is not correct
#             GitlabDeleteError: If the server failed to perform the request
#         """
#         path = f"/projects/{self.encoded_id}/share/{group_id}"
#         self.manager.gitlab.http_delete(path, **kwargs)

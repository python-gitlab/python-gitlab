from __future__ import annotations

from typing import Any, TYPE_CHECKING

import requests

from gitlab import cli
from gitlab import exceptions as exc
from gitlab.base import RESTObject
from gitlab.mixins import (
    CreateMixin,
    CRUDMixin,
    DeleteMixin,
    GetWithoutIdMixin,
    ListMixin,
    ObjectDeleteMixin,
    RefreshMixin,
    RetrieveMixin,
    SaveMixin,
    UpdateMixin,
)
from gitlab.types import ArrayAttribute, RequiredOptional

__all__ = [
    "ProjectMergeRequestPipeline",
    "ProjectMergeRequestPipelineManager",
    "ProjectPipeline",
    "ProjectPipelineManager",
    "ProjectPipelineJob",
    "ProjectPipelineJobManager",
    "ProjectPipelineBridge",
    "ProjectPipelineBridgeManager",
    "ProjectPipelineVariable",
    "ProjectPipelineVariableManager",
    "ProjectPipelineScheduleVariable",
    "ProjectPipelineScheduleVariableManager",
    "ProjectPipelineSchedulePipeline",
    "ProjectPipelineSchedulePipelineManager",
    "ProjectPipelineSchedule",
    "ProjectPipelineScheduleManager",
    "ProjectPipelineTestReport",
    "ProjectPipelineTestReportManager",
    "ProjectPipelineTestReportSummary",
    "ProjectPipelineTestReportSummaryManager",
]


class ProjectMergeRequestPipeline(RESTObject):
    pass


class ProjectMergeRequestPipelineManager(
    CreateMixin[ProjectMergeRequestPipeline], ListMixin[ProjectMergeRequestPipeline]
):
    _path = "/projects/{project_id}/merge_requests/{mr_iid}/pipelines"
    _obj_cls = ProjectMergeRequestPipeline
    _from_parent_attrs = {"project_id": "project_id", "mr_iid": "iid"}


class ProjectPipeline(RefreshMixin, ObjectDeleteMixin, RESTObject):
    bridges: ProjectPipelineBridgeManager
    jobs: ProjectPipelineJobManager
    test_report: ProjectPipelineTestReportManager
    test_report_summary: ProjectPipelineTestReportSummaryManager
    variables: ProjectPipelineVariableManager

    @cli.register_custom_action(cls_names="ProjectPipeline")
    @exc.on_http_error(exc.GitlabPipelineCancelError)
    def cancel(self, **kwargs: Any) -> dict[str, Any] | requests.Response:
        """Cancel the job.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabPipelineCancelError: If the request failed
        """
        path = f"{self.manager.path}/{self.encoded_id}/cancel"
        return self.manager.gitlab.http_post(path, **kwargs)

    @cli.register_custom_action(cls_names="ProjectPipeline")
    @exc.on_http_error(exc.GitlabPipelineRetryError)
    def retry(self, **kwargs: Any) -> dict[str, Any] | requests.Response:
        """Retry the job.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabPipelineRetryError: If the request failed
        """
        path = f"{self.manager.path}/{self.encoded_id}/retry"
        return self.manager.gitlab.http_post(path, **kwargs)


class ProjectPipelineManager(
    RetrieveMixin[ProjectPipeline],
    CreateMixin[ProjectPipeline],
    DeleteMixin[ProjectPipeline],
):
    _path = "/projects/{project_id}/pipelines"
    _obj_cls = ProjectPipeline
    _from_parent_attrs = {"project_id": "id"}
    _list_filters = (
        "scope",
        "status",
        "source",
        "ref",
        "sha",
        "yaml_errors",
        "name",
        "username",
        "order_by",
        "sort",
    )
    _create_attrs = RequiredOptional(required=("ref",))

    def create(
        self, data: dict[str, Any] | None = None, **kwargs: Any
    ) -> ProjectPipeline:
        """Creates a new object.

        Args:
            data: Parameters to send to the server to create the
                         resource
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabCreateError: If the server cannot perform the request

        Returns:
            A new instance of the managed object class build with
                the data sent by the server
        """
        path = self.path[:-1]  # drop the 's'
        return super().create(data, path=path, **kwargs)

    def latest(self, ref: str | None = None, lazy: bool = False) -> ProjectPipeline:
        """Get the latest pipeline for the most recent commit
                            on a specific ref in a project

        Args:
            ref: The branch or tag to check for the latest pipeline.
                            Defaults to the default branch when not specified.
        Returns:
            A Pipeline instance
        """
        data = {}
        if ref:
            data = {"ref": ref}
        server_data = self.gitlab.http_get(self.path + "/latest", query_data=data)
        if TYPE_CHECKING:
            assert not isinstance(server_data, requests.Response)
        return self._obj_cls(self, server_data, lazy=lazy)


class ProjectPipelineJob(RESTObject):
    pass


class ProjectPipelineJobManager(ListMixin[ProjectPipelineJob]):
    _path = "/projects/{project_id}/pipelines/{pipeline_id}/jobs"
    _obj_cls = ProjectPipelineJob
    _from_parent_attrs = {"project_id": "project_id", "pipeline_id": "id"}
    _list_filters = ("scope", "include_retried")
    _types = {"scope": ArrayAttribute}


class ProjectPipelineBridge(RESTObject):
    pass


class ProjectPipelineBridgeManager(ListMixin[ProjectPipelineBridge]):
    _path = "/projects/{project_id}/pipelines/{pipeline_id}/bridges"
    _obj_cls = ProjectPipelineBridge
    _from_parent_attrs = {"project_id": "project_id", "pipeline_id": "id"}
    _list_filters = ("scope",)


class ProjectPipelineVariable(RESTObject):
    _id_attr = "key"


class ProjectPipelineVariableManager(ListMixin[ProjectPipelineVariable]):
    _path = "/projects/{project_id}/pipelines/{pipeline_id}/variables"
    _obj_cls = ProjectPipelineVariable
    _from_parent_attrs = {"project_id": "project_id", "pipeline_id": "id"}


class ProjectPipelineScheduleVariable(SaveMixin, ObjectDeleteMixin, RESTObject):
    _id_attr = "key"


class ProjectPipelineScheduleVariableManager(
    CreateMixin[ProjectPipelineScheduleVariable],
    UpdateMixin[ProjectPipelineScheduleVariable],
    DeleteMixin[ProjectPipelineScheduleVariable],
):
    _path = "/projects/{project_id}/pipeline_schedules/{pipeline_schedule_id}/variables"
    _obj_cls = ProjectPipelineScheduleVariable
    _from_parent_attrs = {"project_id": "project_id", "pipeline_schedule_id": "id"}
    _create_attrs = RequiredOptional(required=("key", "value"))
    _update_attrs = RequiredOptional(required=("key", "value"))


class ProjectPipelineSchedulePipeline(RESTObject):
    pass


class ProjectPipelineSchedulePipelineManager(
    ListMixin[ProjectPipelineSchedulePipeline]
):
    _path = "/projects/{project_id}/pipeline_schedules/{pipeline_schedule_id}/pipelines"
    _obj_cls = ProjectPipelineSchedulePipeline
    _from_parent_attrs = {"project_id": "project_id", "pipeline_schedule_id": "id"}


class ProjectPipelineSchedule(SaveMixin, ObjectDeleteMixin, RESTObject):
    variables: ProjectPipelineScheduleVariableManager
    pipelines: ProjectPipelineSchedulePipelineManager

    @cli.register_custom_action(cls_names="ProjectPipelineSchedule")
    @exc.on_http_error(exc.GitlabOwnershipError)
    def take_ownership(self, **kwargs: Any) -> None:
        """Update the owner of a pipeline schedule.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabOwnershipError: If the request failed
        """
        path = f"{self.manager.path}/{self.encoded_id}/take_ownership"
        server_data = self.manager.gitlab.http_post(path, **kwargs)
        if TYPE_CHECKING:
            assert isinstance(server_data, dict)
        self._update_attrs(server_data)

    @cli.register_custom_action(cls_names="ProjectPipelineSchedule")
    @exc.on_http_error(exc.GitlabPipelinePlayError)
    def play(self, **kwargs: Any) -> dict[str, Any]:
        """Trigger a new scheduled pipeline, which runs immediately.
        The next scheduled run of this pipeline is not affected.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabPipelinePlayError: If the request failed
        """
        path = f"{self.manager.path}/{self.encoded_id}/play"
        server_data = self.manager.gitlab.http_post(path, **kwargs)
        if TYPE_CHECKING:
            assert isinstance(server_data, dict)
        self._update_attrs(server_data)
        return server_data


class ProjectPipelineScheduleManager(CRUDMixin[ProjectPipelineSchedule]):
    _path = "/projects/{project_id}/pipeline_schedules"
    _obj_cls = ProjectPipelineSchedule
    _from_parent_attrs = {"project_id": "id"}
    _create_attrs = RequiredOptional(
        required=("description", "ref", "cron"), optional=("cron_timezone", "active")
    )
    _update_attrs = RequiredOptional(
        optional=("description", "ref", "cron", "cron_timezone", "active")
    )


class ProjectPipelineTestReport(RESTObject):
    _id_attr = None


class ProjectPipelineTestReportManager(GetWithoutIdMixin[ProjectPipelineTestReport]):
    _path = "/projects/{project_id}/pipelines/{pipeline_id}/test_report"
    _obj_cls = ProjectPipelineTestReport
    _from_parent_attrs = {"project_id": "project_id", "pipeline_id": "id"}


class ProjectPipelineTestReportSummary(RESTObject):
    _id_attr = None


class ProjectPipelineTestReportSummaryManager(
    GetWithoutIdMixin[ProjectPipelineTestReportSummary]
):
    _path = "/projects/{project_id}/pipelines/{pipeline_id}/test_report_summary"
    _obj_cls = ProjectPipelineTestReportSummary
    _from_parent_attrs = {"project_id": "project_id", "pipeline_id": "id"}

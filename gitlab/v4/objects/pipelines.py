import warnings

from gitlab import cli
from gitlab import exceptions as exc
from gitlab.base import RequiredOptional, RESTManager, RESTObject
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
    "ProjectPipelineSchedule",
    "ProjectPipelineScheduleManager",
    "ProjectPipelineTestReport",
    "ProjectPipelineTestReportManager",
]


class ProjectMergeRequestPipeline(RESTObject):
    pass


class ProjectMergeRequestPipelineManager(CreateMixin, ListMixin, RESTManager):
    _path = "/projects/%(project_id)s/merge_requests/%(mr_iid)s/pipelines"
    _obj_cls = ProjectMergeRequestPipeline
    _from_parent_attrs = {"project_id": "project_id", "mr_iid": "iid"}

    # If the manager was called directly as a callable via
    # mr.pipelines(), execute the deprecated method for now.
    # TODO: in python-gitlab 3.0.0, remove this method entirely.

    @cli.register_custom_action("ProjectMergeRequest", custom_action="pipelines")
    @exc.on_http_error(exc.GitlabListError)
    def __call__(self, **kwargs):
        """List the merge request pipelines.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabListError: If the list could not be retrieved

        Returns:
            RESTObjectList: List of changes
        """
        warnings.warn(
            "Calling the ProjectMergeRequest.pipelines() method on "
            "merge request objects directly is deprecated and will be replaced "
            "by ProjectMergeRequest.pipelines.list() in python-gitlab 3.0.0.\n",
            DeprecationWarning,
        )
        return self.list(**kwargs)


class ProjectPipeline(RefreshMixin, ObjectDeleteMixin, RESTObject):
    bridges: "ProjectPipelineBridgeManager"
    jobs: "ProjectPipelineJobManager"
    test_report: "ProjectPipelineTestReportManager"
    variables: "ProjectPipelineVariableManager"
    _managers = (
        ("bridges", "ProjectPipelineBridgeManager"),
        ("jobs", "ProjectPipelineJobManager"),
        ("test_report", "ProjectPipelineTestReportManager"),
        ("variables", "ProjectPipelineVariableManager"),
    )

    @cli.register_custom_action("ProjectPipeline")
    @exc.on_http_error(exc.GitlabPipelineCancelError)
    def cancel(self, **kwargs):
        """Cancel the job.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabPipelineCancelError: If the request failed
        """
        path = "%s/%s/cancel" % (self.manager.path, self.get_id())
        return self.manager.gitlab.http_post(path)

    @cli.register_custom_action("ProjectPipeline")
    @exc.on_http_error(exc.GitlabPipelineRetryError)
    def retry(self, **kwargs):
        """Retry the job.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabPipelineRetryError: If the request failed
        """
        path = "%s/%s/retry" % (self.manager.path, self.get_id())
        return self.manager.gitlab.http_post(path)


class ProjectPipelineManager(RetrieveMixin, CreateMixin, DeleteMixin, RESTManager):
    _path = "/projects/%(project_id)s/pipelines"
    _obj_cls = ProjectPipeline
    _from_parent_attrs = {"project_id": "id"}
    _list_filters = (
        "scope",
        "status",
        "ref",
        "sha",
        "yaml_errors",
        "name",
        "username",
        "order_by",
        "sort",
    )
    _create_attrs = RequiredOptional(required=("ref",))

    def create(self, data, **kwargs):
        """Creates a new object.

        Args:
            data (dict): Parameters to send to the server to create the
                         resource
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabCreateError: If the server cannot perform the request

        Returns:
            RESTObject: A new instance of the managed object class build with
                the data sent by the server
        """
        path = self.path[:-1]  # drop the 's'
        return CreateMixin.create(self, data, path=path, **kwargs)


class ProjectPipelineJob(RESTObject):
    pass


class ProjectPipelineJobManager(ListMixin, RESTManager):
    _path = "/projects/%(project_id)s/pipelines/%(pipeline_id)s/jobs"
    _obj_cls = ProjectPipelineJob
    _from_parent_attrs = {"project_id": "project_id", "pipeline_id": "id"}
    _list_filters = ("scope", "include_retried")


class ProjectPipelineBridge(RESTObject):
    pass


class ProjectPipelineBridgeManager(ListMixin, RESTManager):
    _path = "/projects/%(project_id)s/pipelines/%(pipeline_id)s/bridges"
    _obj_cls = ProjectPipelineBridge
    _from_parent_attrs = {"project_id": "project_id", "pipeline_id": "id"}
    _list_filters = ("scope",)


class ProjectPipelineVariable(RESTObject):
    _id_attr = "key"


class ProjectPipelineVariableManager(ListMixin, RESTManager):
    _path = "/projects/%(project_id)s/pipelines/%(pipeline_id)s/variables"
    _obj_cls = ProjectPipelineVariable
    _from_parent_attrs = {"project_id": "project_id", "pipeline_id": "id"}


class ProjectPipelineScheduleVariable(SaveMixin, ObjectDeleteMixin, RESTObject):
    _id_attr = "key"


class ProjectPipelineScheduleVariableManager(
    CreateMixin, UpdateMixin, DeleteMixin, RESTManager
):
    _path = (
        "/projects/%(project_id)s/pipeline_schedules/"
        "%(pipeline_schedule_id)s/variables"
    )
    _obj_cls = ProjectPipelineScheduleVariable
    _from_parent_attrs = {"project_id": "project_id", "pipeline_schedule_id": "id"}
    _create_attrs = RequiredOptional(required=("key", "value"))
    _update_attrs = RequiredOptional(required=("key", "value"))


class ProjectPipelineSchedule(SaveMixin, ObjectDeleteMixin, RESTObject):
    variables: ProjectPipelineScheduleVariableManager
    _managers = (("variables", "ProjectPipelineScheduleVariableManager"),)

    @cli.register_custom_action("ProjectPipelineSchedule")
    @exc.on_http_error(exc.GitlabOwnershipError)
    def take_ownership(self, **kwargs):
        """Update the owner of a pipeline schedule.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabOwnershipError: If the request failed
        """
        path = "%s/%s/take_ownership" % (self.manager.path, self.get_id())
        server_data = self.manager.gitlab.http_post(path, **kwargs)
        self._update_attrs(server_data)

    @cli.register_custom_action("ProjectPipelineSchedule")
    @exc.on_http_error(exc.GitlabPipelinePlayError)
    def play(self, **kwargs):
        """Trigger a new scheduled pipeline, which runs immediately.
        The next scheduled run of this pipeline is not affected.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabPipelinePlayError: If the request failed
        """
        path = "%s/%s/play" % (self.manager.path, self.get_id())
        server_data = self.manager.gitlab.http_post(path, **kwargs)
        self._update_attrs(server_data)
        return server_data


class ProjectPipelineScheduleManager(CRUDMixin, RESTManager):
    _path = "/projects/%(project_id)s/pipeline_schedules"
    _obj_cls = ProjectPipelineSchedule
    _from_parent_attrs = {"project_id": "id"}
    _create_attrs = RequiredOptional(
        required=("description", "ref", "cron"), optional=("cron_timezone", "active")
    )
    _update_attrs = RequiredOptional(
        optional=("description", "ref", "cron", "cron_timezone", "active"),
    )


class ProjectPipelineTestReport(RESTObject):
    _id_attr = None


class ProjectPipelineTestReportManager(GetWithoutIdMixin, RESTManager):
    _path = "/projects/%(project_id)s/pipelines/%(pipeline_id)s/test_report"
    _obj_cls = ProjectPipelineTestReport
    _from_parent_attrs = {"project_id": "project_id", "pipeline_id": "id"}

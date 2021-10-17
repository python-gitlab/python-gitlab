from gitlab import cli
from gitlab import exceptions as exc
from gitlab import types
from gitlab.base import RequiredOptional, RESTManager, RESTObject
from gitlab.mixins import (
    CreateMixin,
    CRUDMixin,
    DeleteMixin,
    ListMixin,
    ObjectDeleteMixin,
    SaveMixin,
)

__all__ = [
    "RunnerJob",
    "RunnerJobManager",
    "Runner",
    "RunnerManager",
    "GroupRunner",
    "GroupRunnerManager",
    "ProjectRunner",
    "ProjectRunnerManager",
]


class RunnerJob(RESTObject):
    pass


class RunnerJobManager(ListMixin, RESTManager):
    _path = "/runners/%(runner_id)s/jobs"
    _obj_cls = RunnerJob
    _from_parent_attrs = {"runner_id": "id"}
    _list_filters = ("status",)


class Runner(SaveMixin, ObjectDeleteMixin, RESTObject):
    jobs: RunnerJobManager


class RunnerManager(CRUDMixin, RESTManager):
    _path = "/runners"
    _obj_cls = Runner
    _create_attrs = RequiredOptional(
        required=("token",),
        optional=(
            "description",
            "info",
            "active",
            "locked",
            "run_untagged",
            "tag_list",
            "access_level",
            "maximum_timeout",
        ),
    )
    _update_attrs = RequiredOptional(
        optional=(
            "description",
            "active",
            "tag_list",
            "run_untagged",
            "locked",
            "access_level",
            "maximum_timeout",
        ),
    )
    _list_filters = ("scope", "tag_list")
    _types = {"tag_list": types.ListAttribute}

    @cli.register_custom_action("RunnerManager", tuple(), ("scope",))
    @exc.on_http_error(exc.GitlabListError)
    def all(self, scope=None, **kwargs):
        """List all the runners.

        Args:
            scope (str): The scope of runners to show, one of: specific,
                shared, active, paused, online
            all (bool): If True, return all the items, without pagination
            per_page (int): Number of items to retrieve per request
            page (int): ID of the page to return (starts with page 1)
            as_list (bool): If set to False and no pagination option is
                defined, return a generator instead of a list
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabListError: If the server failed to perform the request

        Returns:
            list(Runner): a list of runners matching the scope.
        """
        path = "/runners/all"
        query_data = {}
        if scope is not None:
            query_data["scope"] = scope
        obj = self.gitlab.http_list(path, query_data, **kwargs)
        return [self._obj_cls(self, item) for item in obj]

    @cli.register_custom_action("RunnerManager", ("token",))
    @exc.on_http_error(exc.GitlabVerifyError)
    def verify(self, token, **kwargs):
        """Validates authentication credentials for a registered Runner.

        Args:
            token (str): The runner's authentication token
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabVerifyError: If the server failed to verify the token
        """
        path = "/runners/verify"
        post_data = {"token": token}
        self.gitlab.http_post(path, post_data=post_data, **kwargs)


class GroupRunner(RESTObject):
    pass


class GroupRunnerManager(ListMixin, RESTManager):
    _path = "/groups/%(group_id)s/runners"
    _obj_cls = GroupRunner
    _from_parent_attrs = {"group_id": "id"}
    _create_attrs = RequiredOptional(required=("runner_id",))
    _list_filters = ("scope", "tag_list")
    _types = {"tag_list": types.ListAttribute}


class ProjectRunner(ObjectDeleteMixin, RESTObject):
    pass


class ProjectRunnerManager(CreateMixin, DeleteMixin, ListMixin, RESTManager):
    _path = "/projects/%(project_id)s/runners"
    _obj_cls = ProjectRunner
    _from_parent_attrs = {"project_id": "id"}
    _create_attrs = RequiredOptional(required=("runner_id",))
    _list_filters = ("scope", "tag_list")
    _types = {"tag_list": types.ListAttribute}

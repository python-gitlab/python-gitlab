from gitlab import exceptions as exc
from gitlab.base import RESTObject
from gitlab.mixins import CRUDMixin, NoUpdateMixin, ObjectDeleteMixin, SaveMixin
from gitlab.types import RequiredOptional

__all__ = [
    "Hook",
    "HookManager",
    "ProjectHook",
    "ProjectHookManager",
    "GroupHook",
    "GroupHookManager",
]


class Hook(ObjectDeleteMixin, RESTObject):
    _url = "/hooks"
    _repr_attr = "url"


class HookManager(NoUpdateMixin[Hook]):
    _path = "/hooks"
    _obj_cls = Hook
    _create_attrs = RequiredOptional(required=("url",))


class ProjectHook(SaveMixin, ObjectDeleteMixin, RESTObject):
    _repr_attr = "url"

    @exc.on_http_error(exc.GitlabHookTestError)
    def test(self, trigger: str) -> None:
        """
        Test a Project Hook

        Args:
            trigger: Type of trigger event to test

        Raises:
            GitlabHookTestError: If the hook test attempt failed
        """
        path = f"{self.manager.path}/{self.encoded_id}/test/{trigger}"
        self.manager.gitlab.http_post(path)


class ProjectHookManager(CRUDMixin[ProjectHook]):
    _path = "/projects/{project_id}/hooks"
    _obj_cls = ProjectHook
    _from_parent_attrs = {"project_id": "id"}
    _create_attrs = RequiredOptional(
        required=("url",),
        optional=(
            "push_events",
            "issues_events",
            "confidential_issues_events",
            "merge_requests_events",
            "tag_push_events",
            "note_events",
            "job_events",
            "pipeline_events",
            "wiki_page_events",
            "enable_ssl_verification",
            "token",
        ),
    )
    _update_attrs = RequiredOptional(
        required=("url",),
        optional=(
            "push_events",
            "issues_events",
            "confidential_issues_events",
            "merge_requests_events",
            "tag_push_events",
            "note_events",
            "job_events",
            "pipeline_events",
            "wiki_events",
            "enable_ssl_verification",
            "token",
        ),
    )


class GroupHook(SaveMixin, ObjectDeleteMixin, RESTObject):
    _repr_attr = "url"

    @exc.on_http_error(exc.GitlabHookTestError)
    def test(self, trigger: str) -> None:
        """
        Test a Group Hook

        Args:
            trigger: Type of trigger event to test

        Raises:
            GitlabHookTestError: If the hook test attempt failed
        """
        path = f"{self.manager.path}/{self.encoded_id}/test/{trigger}"
        self.manager.gitlab.http_post(path)


class GroupHookManager(CRUDMixin[GroupHook]):
    _path = "/groups/{group_id}/hooks"
    _obj_cls = GroupHook
    _from_parent_attrs = {"group_id": "id"}
    _create_attrs = RequiredOptional(
        required=("url",),
        optional=(
            "push_events",
            "issues_events",
            "confidential_issues_events",
            "merge_requests_events",
            "tag_push_events",
            "note_events",
            "confidential_note_events",
            "job_events",
            "pipeline_events",
            "wiki_page_events",
            "deployment_events",
            "releases_events",
            "subgroup_events",
            "enable_ssl_verification",
            "token",
        ),
    )
    _update_attrs = RequiredOptional(
        required=("url",),
        optional=(
            "push_events",
            "issues_events",
            "confidential_issues_events",
            "merge_requests_events",
            "tag_push_events",
            "note_events",
            "confidential_note_events",
            "job_events",
            "pipeline_events",
            "wiki_page_events",
            "deployment_events",
            "releases_events",
            "subgroup_events",
            "enable_ssl_verification",
            "token",
        ),
    )

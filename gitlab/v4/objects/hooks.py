from gitlab.base import RequiredOptional, RESTManager, RESTObject
from gitlab.mixins import CRUDMixin, NoUpdateMixin, ObjectDeleteMixin, SaveMixin

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
    _short_print_attr = "url"


class HookManager(NoUpdateMixin, RESTManager):
    _path = "/hooks"
    _obj_cls = Hook
    _create_attrs = RequiredOptional(required=("url",))


class ProjectHook(SaveMixin, ObjectDeleteMixin, RESTObject):
    _short_print_attr = "url"


class ProjectHookManager(CRUDMixin, RESTManager):
    _path = "/projects/%(project_id)s/hooks"
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
    _short_print_attr = "url"


class GroupHookManager(CRUDMixin, RESTManager):
    _path = "/groups/%(group_id)s/hooks"
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

from gitlab.base import *  # noqa
from gitlab.mixins import *  # noqa


__all__ = [
    "Hook",
    "HookManager",
    "ProjectHook",
    "ProjectHookManager",
]


class Hook(ObjectDeleteMixin, RESTObject):
    _url = "/hooks"
    _short_print_attr = "url"


class HookManager(NoUpdateMixin, RESTManager):
    _path = "/hooks"
    _obj_cls = Hook
    _create_attrs = (("url",), tuple())


class ProjectHook(SaveMixin, ObjectDeleteMixin, RESTObject):
    _short_print_attr = "url"


class ProjectHookManager(CRUDMixin, RESTManager):
    _path = "/projects/%(project_id)s/hooks"
    _obj_cls = ProjectHook
    _from_parent_attrs = {"project_id": "id"}
    _create_attrs = (
        ("url",),
        (
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
    _update_attrs = (
        ("url",),
        (
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

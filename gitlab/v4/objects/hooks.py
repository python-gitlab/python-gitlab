from gitlab.mixins import CRUDMixin, NoUpdateMixin, ObjectDeleteMixin, SaveMixin


__all__ = [
    "Hook",
    "HookManager",
    "ProjectHook",
    "ProjectHookManager",
]


class Hook(ObjectDeleteMixin):
    _url = "/hooks"
    _short_print_attr = "url"


class HookManager(NoUpdateMixin):
    _path = "/hooks"
    _obj_cls = Hook
    _create_attrs = (("url",), tuple())


class ProjectHook(SaveMixin, ObjectDeleteMixin):
    _short_print_attr = "url"


class ProjectHookManager(CRUDMixin):
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

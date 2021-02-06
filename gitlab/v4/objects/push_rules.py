from gitlab.base import *  # noqa
from gitlab.mixins import *  # noqa


class ProjectPushRules(SaveMixin, ObjectDeleteMixin, RESTObject):
    _id_attr = None


class ProjectPushRulesManager(
    GetWithoutIdMixin, CreateMixin, UpdateMixin, DeleteMixin, RESTManager
):
    _path = "/projects/%(project_id)s/push_rule"
    _obj_cls = ProjectPushRules
    _from_parent_attrs = {"project_id": "id"}
    _create_attrs = (
        tuple(),
        (
            "deny_delete_tag",
            "member_check",
            "prevent_secrets",
            "commit_message_regex",
            "branch_name_regex",
            "author_email_regex",
            "file_name_regex",
            "max_file_size",
        ),
    )
    _update_attrs = (
        tuple(),
        (
            "deny_delete_tag",
            "member_check",
            "prevent_secrets",
            "commit_message_regex",
            "branch_name_regex",
            "author_email_regex",
            "file_name_regex",
            "max_file_size",
        ),
    )

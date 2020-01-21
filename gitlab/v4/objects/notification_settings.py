from gitlab.base import *  # noqa
from gitlab.exceptions import *  # noqa
from gitlab.mixins import *  # noqa
from gitlab import types
from gitlab import utils


class NotificationSettings(SaveMixin, RESTObject):
    _id_attr = None


class NotificationSettingsManager(GetWithoutIdMixin, UpdateMixin, RESTManager):
    _path = "/notification_settings"
    _obj_cls = NotificationSettings

    _update_attrs = (
        tuple(),
        (
            "level",
            "notification_email",
            "new_note",
            "new_issue",
            "reopen_issue",
            "close_issue",
            "reassign_issue",
            "new_merge_request",
            "reopen_merge_request",
            "close_merge_request",
            "reassign_merge_request",
            "merge_merge_request",
        ),
    )

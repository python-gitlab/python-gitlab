from gitlab.base import RESTObject
from gitlab.mixins import GetWithoutIdMixin, SaveMixin, UpdateMixin
from gitlab.types import RequiredOptional

__all__ = [
    "NotificationSettings",
    "NotificationSettingsManager",
    "GroupNotificationSettings",
    "GroupNotificationSettingsManager",
    "ProjectNotificationSettings",
    "ProjectNotificationSettingsManager",
]


class NotificationSettings(SaveMixin, RESTObject):
    _id_attr = None


class NotificationSettingsManager(
    GetWithoutIdMixin[NotificationSettings], UpdateMixin[NotificationSettings]
):
    _path = "/notification_settings"
    _obj_cls = NotificationSettings

    _update_attrs = RequiredOptional(
        optional=(
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
        )
    )


class GroupNotificationSettings(NotificationSettings):
    pass


class GroupNotificationSettingsManager(NotificationSettingsManager):
    _path = "/groups/{group_id}/notification_settings"
    _obj_cls = GroupNotificationSettings
    _from_parent_attrs = {"group_id": "id"}


class ProjectNotificationSettings(NotificationSettings):
    pass


class ProjectNotificationSettingsManager(NotificationSettingsManager):
    _path = "/projects/{project_id}/notification_settings"
    _obj_cls = ProjectNotificationSettings
    _from_parent_attrs = {"project_id": "id"}

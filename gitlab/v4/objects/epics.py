from gitlab import types
from gitlab import exceptions as exc
from gitlab.mixins import (
    CRUDMixin,
    CreateMixin,
    DeleteMixin,
    ListMixin,
    ObjectDeleteMixin,
    SaveMixin,
    UpdateMixin,
)
from .events import GroupEpicResourceLabelEventManager


__all__ = [
    "GroupEpic",
    "GroupEpicManager",
    "GroupEpicIssue",
    "GroupEpicIssueManager",
]


class GroupEpic(ObjectDeleteMixin, SaveMixin):
    _id_attr = "iid"
    _managers = (
        ("issues", "GroupEpicIssueManager"),
        ("resourcelabelevents", "GroupEpicResourceLabelEventManager"),
    )


class GroupEpicManager(CRUDMixin):
    _path = "/groups/%(group_id)s/epics"
    _obj_cls = GroupEpic
    _from_parent_attrs = {"group_id": "id"}
    _list_filters = ("author_id", "labels", "order_by", "sort", "search")
    _create_attrs = (("title",), ("labels", "description", "start_date", "end_date"))
    _update_attrs = (
        tuple(),
        ("title", "labels", "description", "start_date", "end_date"),
    )
    _types = {"labels": types.ListAttribute}


class GroupEpicIssue(ObjectDeleteMixin, SaveMixin):
    _id_attr = "epic_issue_id"

    def save(self, **kwargs):
        """Save the changes made to the object to the server.

        The object is updated to match what the server returns.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raise:
            GitlabAuthenticationError: If authentication is not correct
            GitlabUpdateError: If the server cannot perform the request
        """
        updated_data = self._get_updated_data()
        # Nothing to update. Server fails if sent an empty dict.
        if not updated_data:
            return

        # call the manager
        obj_id = self.get_id()
        self.manager.update(obj_id, updated_data, **kwargs)


class GroupEpicIssueManager(ListMixin, CreateMixin, UpdateMixin, DeleteMixin):
    _path = "/groups/%(group_id)s/epics/%(epic_iid)s/issues"
    _obj_cls = GroupEpicIssue
    _from_parent_attrs = {"group_id": "group_id", "epic_iid": "iid"}
    _create_attrs = (("issue_id",), tuple())
    _update_attrs = (tuple(), ("move_before_id", "move_after_id"))

    @exc.on_http_error(exc.GitlabCreateError)
    def create(self, data, **kwargs):
        """Create a new object.

        Args:
            data (dict): Parameters to send to the server to create the
                         resource
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabCreateError: If the server cannot perform the request

        Returns:
            RESTObject: A new instance of the manage object class build with
                        the data sent by the server
        """
        CreateMixin._check_missing_create_attrs(self, data)
        path = "%s/%s" % (self.path, data.pop("issue_id"))
        server_data = self.gitlab.http_post(path, **kwargs)
        # The epic_issue_id attribute doesn't exist when creating the resource,
        # but is used everywhere elese. Let's create it to be consistent client
        # side
        server_data["epic_issue_id"] = server_data["id"]
        return self._obj_cls(self, server_data)

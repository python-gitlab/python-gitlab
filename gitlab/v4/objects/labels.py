from gitlab import exceptions as exc
from gitlab.mixins import (
    CreateMixin,
    DeleteMixin,
    ListMixin,
    ObjectDeleteMixin,
    RetrieveMixin,
    SaveMixin,
    SubscribableMixin,
    UpdateMixin,
)


__all__ = [
    "GroupLabel",
    "GroupLabelManager",
    "ProjectLabel",
    "ProjectLabelManager",
]


class GroupLabel(SubscribableMixin, SaveMixin, ObjectDeleteMixin):
    _id_attr = "name"

    # Update without ID, but we need an ID to get from list.
    @exc.on_http_error(exc.GitlabUpdateError)
    def save(self, **kwargs):
        """Saves the changes made to the object to the server.

        The object is updated to match what the server returns.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct.
            GitlabUpdateError: If the server cannot perform the request.
        """
        updated_data = self._get_updated_data()

        # call the manager
        server_data = self.manager.update(None, updated_data, **kwargs)
        self._update_attrs(server_data)


class GroupLabelManager(ListMixin, CreateMixin, UpdateMixin, DeleteMixin):
    _path = "/groups/%(group_id)s/labels"
    _obj_cls = GroupLabel
    _from_parent_attrs = {"group_id": "id"}
    _create_attrs = (("name", "color"), ("description", "priority"))
    _update_attrs = (("name",), ("new_name", "color", "description", "priority"))

    # Update without ID.
    def update(self, name, new_data=None, **kwargs):
        """Update a Label on the server.

        Args:
            name: The name of the label
            **kwargs: Extra options to send to the server (e.g. sudo)
        """
        new_data = new_data or {}
        if name:
            new_data["name"] = name
        return super().update(id=None, new_data=new_data, **kwargs)

    # Delete without ID.
    @exc.on_http_error(exc.GitlabDeleteError)
    def delete(self, name, **kwargs):
        """Delete a Label on the server.

        Args:
            name: The name of the label
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabDeleteError: If the server cannot perform the request
        """
        self.gitlab.http_delete(self.path, query_data={"name": name}, **kwargs)


class ProjectLabel(SubscribableMixin, SaveMixin, ObjectDeleteMixin):
    _id_attr = "name"

    # Update without ID, but we need an ID to get from list.
    @exc.on_http_error(exc.GitlabUpdateError)
    def save(self, **kwargs):
        """Saves the changes made to the object to the server.

        The object is updated to match what the server returns.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct.
            GitlabUpdateError: If the server cannot perform the request.
        """
        updated_data = self._get_updated_data()

        # call the manager
        server_data = self.manager.update(None, updated_data, **kwargs)
        self._update_attrs(server_data)


class ProjectLabelManager(RetrieveMixin, CreateMixin, UpdateMixin, DeleteMixin):
    _path = "/projects/%(project_id)s/labels"
    _obj_cls = ProjectLabel
    _from_parent_attrs = {"project_id": "id"}
    _create_attrs = (("name", "color"), ("description", "priority"))
    _update_attrs = (("name",), ("new_name", "color", "description", "priority"))

    # Update without ID.
    def update(self, name, new_data=None, **kwargs):
        """Update a Label on the server.

        Args:
            name: The name of the label
            **kwargs: Extra options to send to the server (e.g. sudo)
        """
        new_data = new_data or {}
        if name:
            new_data["name"] = name
        return super().update(id=None, new_data=new_data, **kwargs)

    # Delete without ID.
    @exc.on_http_error(exc.GitlabDeleteError)
    def delete(self, name, **kwargs):
        """Delete a Label on the server.

        Args:
            name: The name of the label
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabDeleteError: If the server cannot perform the request
        """
        self.gitlab.http_delete(self.path, query_data={"name": name}, **kwargs)

from gitlab import exceptions as exc
from gitlab import utils
from gitlab.base import RESTManager, RESTObject
from gitlab.mixins import DeleteMixin, ListMixin, ObjectDeleteMixin

__all__ = [
    "Feature",
    "FeatureManager",
]


class Feature(ObjectDeleteMixin, RESTObject):
    _id_attr = "name"


class FeatureManager(ListMixin, DeleteMixin, RESTManager):
    _path = "/features/"
    _obj_cls = Feature

    @exc.on_http_error(exc.GitlabSetError)
    def set(
        self,
        name,
        value,
        feature_group=None,
        user=None,
        group=None,
        project=None,
        **kwargs
    ):
        """Create or update the object.

        Args:
            name (str): The value to set for the object
            value (bool/int): The value to set for the object
            feature_group (str): A feature group name
            user (str): A GitLab username
            group (str): A GitLab group
            project (str): A GitLab project in form group/project
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabSetError: If an error occurred

        Returns:
            obj: The created/updated attribute
        """
        path = "%s/%s" % (self.path, name.replace("/", "%2F"))
        data = {
            "value": value,
            "feature_group": feature_group,
            "user": user,
            "group": group,
            "project": project,
        }
        data = utils.remove_none_from_dict(data)
        server_data = self.gitlab.http_post(path, post_data=data, **kwargs)
        return self._obj_cls(self, server_data)

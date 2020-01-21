from gitlab.base import *  # noqa
from gitlab.exceptions import *  # noqa
from gitlab.mixins import *  # noqa
from gitlab import types
from gitlab import utils


class Feature(ObjectDeleteMixin, RESTObject):
    _id_attr = "name"


class FeatureManager(ListMixin, DeleteMixin, RESTManager):
    _path = "/features/"
    _obj_cls = Feature

    @exc.on_http_error(exc.GitlabSetError)
    def set(self, name, value, feature_group=None, user=None, **kwargs):
        """Create or update the object.

        Args:
            name (str): The value to set for the object
            value (bool/int): The value to set for the object
            feature_group (str): A feature group name
            user (str): A GitLab username
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabSetError: If an error occured

        Returns:
            obj: The created/updated attribute
        """
        path = "%s/%s" % (self.path, name.replace("/", "%2F"))
        data = {"value": value, "feature_group": feature_group, "user": user}
        server_data = self.gitlab.http_post(path, post_data=data, **kwargs)
        return self._obj_cls(self, server_data)

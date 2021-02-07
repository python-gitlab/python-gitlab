from gitlab.base import *  # noqa
from gitlab.mixins import *  # noqa


__all__ = [
    "ProjectDeployment",
    "ProjectDeploymentManager",
]


class ProjectDeployment(RESTObject, SaveMixin):
    pass


class ProjectDeploymentManager(RetrieveMixin, CreateMixin, UpdateMixin, RESTManager):
    _path = "/projects/%(project_id)s/deployments"
    _obj_cls = ProjectDeployment
    _from_parent_attrs = {"project_id": "id"}
    _list_filters = ("order_by", "sort")
    _create_attrs = (("sha", "ref", "tag", "status", "environment"), tuple())

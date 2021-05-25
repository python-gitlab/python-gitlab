from gitlab.base import RequiredOptional, RESTManager, RESTObject
from gitlab.mixins import CreateMixin, RetrieveMixin, SaveMixin, UpdateMixin

__all__ = [
    "ProjectDeployment",
    "ProjectDeploymentManager",
]


class ProjectDeployment(SaveMixin, RESTObject):
    pass


class ProjectDeploymentManager(RetrieveMixin, CreateMixin, UpdateMixin, RESTManager):
    _path = "/projects/%(project_id)s/deployments"
    _obj_cls = ProjectDeployment
    _from_parent_attrs = {"project_id": "id"}
    _list_filters = ("order_by", "sort")
    _create_attrs = RequiredOptional(
        required=("sha", "ref", "tag", "status", "environment")
    )

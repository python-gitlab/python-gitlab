from gitlab.base import RESTManager, RESTObject
from gitlab.mixins import CRUDMixin, ListMixin, ObjectDeleteMixin, SaveMixin


__all__ = [
    "PagesDomain",
    "PagesDomainManager",
    "ProjectPagesDomain",
    "ProjectPagesDomainManager",
]


class PagesDomain(RESTObject):
    _id_attr = "domain"


class PagesDomainManager(ListMixin, RESTManager):
    _path = "/pages/domains"
    _obj_cls = PagesDomain


class ProjectPagesDomain(SaveMixin, ObjectDeleteMixin, RESTObject):
    _id_attr = "domain"


class ProjectPagesDomainManager(CRUDMixin, RESTManager):
    _path = "/projects/%(project_id)s/pages/domains"
    _obj_cls = ProjectPagesDomain
    _from_parent_attrs = {"project_id": "id"}
    _create_attrs = (("domain",), ("certificate", "key"))
    _update_attrs = (tuple(), ("certificate", "key"))

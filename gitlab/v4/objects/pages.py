from gitlab.base import RESTObject
from gitlab.mixins import (
    CRUDMixin,
    DeleteMixin,
    GetWithoutIdMixin,
    ListMixin,
    ObjectDeleteMixin,
    RefreshMixin,
    SaveMixin,
    UpdateMethod,
    UpdateMixin,
)
from gitlab.types import RequiredOptional

__all__ = [
    "PagesDomain",
    "PagesDomainManager",
    "ProjectPagesDomain",
    "ProjectPagesDomainManager",
    "ProjectPages",
    "ProjectPagesManager",
]


class PagesDomain(RESTObject):
    _id_attr = "domain"


class PagesDomainManager(ListMixin[PagesDomain]):
    _path = "/pages/domains"
    _obj_cls = PagesDomain


class ProjectPagesDomain(SaveMixin, ObjectDeleteMixin, RESTObject):
    _id_attr = "domain"


class ProjectPagesDomainManager(CRUDMixin[ProjectPagesDomain]):
    _path = "/projects/{project_id}/pages/domains"
    _obj_cls = ProjectPagesDomain
    _from_parent_attrs = {"project_id": "id"}
    _create_attrs = RequiredOptional(
        required=("domain",), optional=("certificate", "key")
    )
    _update_attrs = RequiredOptional(optional=("certificate", "key"))


class ProjectPages(ObjectDeleteMixin, RefreshMixin, RESTObject):
    _id_attr = None


class ProjectPagesManager(
    DeleteMixin[ProjectPages],
    UpdateMixin[ProjectPages],
    GetWithoutIdMixin[ProjectPages],
):
    _path = "/projects/{project_id}/pages"
    _obj_cls = ProjectPages
    _from_parent_attrs = {"project_id": "id"}
    _update_attrs = RequiredOptional(
        optional=("pages_unique_domain_enabled", "pages_https_only")
    )
    _update_method: UpdateMethod = UpdateMethod.PATCH

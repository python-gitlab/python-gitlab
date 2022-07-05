"""
GitLab API:
https://docs.gitlab.com/ee/api/lint.html
"""

from typing import Any, cast

from gitlab.base import RESTManager, RESTObject
from gitlab.mixins import CreateMixin, GetWithoutIdMixin
from gitlab.types import RequiredOptional

__all__ = [
    "CiLint",
    "CiLintManager",
    "ProjectCiLint",
    "ProjectCiLintManager",
]


class CiLint(RESTObject):
    _id_attr = None


class CiLintManager(CreateMixin, RESTManager):
    _path = "/ci/lint"
    _obj_cls = CiLint
    _create_attrs = RequiredOptional(
        required=("content",), optional=("include_merged_yaml", "include_jobs")
    )


class ProjectCiLint(RESTObject):
    pass


class ProjectCiLintManager(GetWithoutIdMixin, CreateMixin, RESTManager):
    _path = "/projects/{project_id}/ci/lint"
    _obj_cls = ProjectCiLint
    _from_parent_attrs = {"project_id": "id"}
    _create_attrs = RequiredOptional(
        required=("content",), optional=("dry_run", "include_jobs", "ref")
    )

    def get(self, **kwargs: Any) -> ProjectCiLint:
        return cast(ProjectCiLint, super().get(**kwargs))

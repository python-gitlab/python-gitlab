"""
GitLab API:
https://docs.gitlab.com/ee/api/lint.html
"""

from typing import Any, cast

from gitlab.base import RESTManager, RESTObject
from gitlab.mixins import CreateMixin, GetWithoutIdMixin
from gitlab.types import RequiredOptional


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

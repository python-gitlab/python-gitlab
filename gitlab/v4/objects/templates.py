from typing import Any, cast, Union

from gitlab.base import RESTManager, RESTObject
from gitlab.mixins import RetrieveMixin

__all__ = [
    "Dockerfile",
    "DockerfileManager",
    "Gitignore",
    "GitignoreManager",
    "Gitlabciyml",
    "GitlabciymlManager",
    "License",
    "LicenseManager",
    "ProjectDockerfileTemplate",
    "ProjectDockerfileTemplateManager",
    "ProjectGitignoreTemplate",
    "ProjectGitignoreTemplateManager",
    "ProjectGitlabciymlTemplate",
    "ProjectGitlabciymlTemplateManager",
    "ProjectIssueTemplate",
    "ProjectIssueTemplateManager",
    "ProjectLicenseTemplate",
    "ProjectLicenseTemplateManager",
    "ProjectMergeRequestTemplate",
    "ProjectMergeRequestTemplateManager",
]


class Dockerfile(RESTObject):
    _id_attr = "name"


class DockerfileManager(RetrieveMixin, RESTManager):
    _path = "/templates/dockerfiles"
    _obj_cls = Dockerfile

    def get(self, id: Union[str, int], lazy: bool = False, **kwargs: Any) -> Dockerfile:
        return cast(Dockerfile, super().get(id=id, lazy=lazy, **kwargs))


class Gitignore(RESTObject):
    _id_attr = "name"


class GitignoreManager(RetrieveMixin, RESTManager):
    _path = "/templates/gitignores"
    _obj_cls = Gitignore

    def get(self, id: Union[str, int], lazy: bool = False, **kwargs: Any) -> Gitignore:
        return cast(Gitignore, super().get(id=id, lazy=lazy, **kwargs))


class Gitlabciyml(RESTObject):
    _id_attr = "name"


class GitlabciymlManager(RetrieveMixin, RESTManager):
    _path = "/templates/gitlab_ci_ymls"
    _obj_cls = Gitlabciyml

    def get(
        self, id: Union[str, int], lazy: bool = False, **kwargs: Any
    ) -> Gitlabciyml:
        return cast(Gitlabciyml, super().get(id=id, lazy=lazy, **kwargs))


class License(RESTObject):
    _id_attr = "key"


class LicenseManager(RetrieveMixin, RESTManager):
    _path = "/templates/licenses"
    _obj_cls = License
    _list_filters = ("popular",)
    _optional_get_attrs = ("project", "fullname")

    def get(self, id: Union[str, int], lazy: bool = False, **kwargs: Any) -> License:
        return cast(License, super().get(id=id, lazy=lazy, **kwargs))


class ProjectDockerfileTemplate(RESTObject):
    _id_attr = "name"


class ProjectDockerfileTemplateManager(RetrieveMixin, RESTManager):
    _path = "/projects/{project_id}/templates/dockerfiles"
    _obj_cls = ProjectDockerfileTemplate
    _from_parent_attrs = {"project_id": "id"}

    def get(
        self, id: Union[str, int], lazy: bool = False, **kwargs: Any
    ) -> ProjectDockerfileTemplate:
        return cast(ProjectDockerfileTemplate, super().get(id=id, lazy=lazy, **kwargs))


class ProjectGitignoreTemplate(RESTObject):
    _id_attr = "name"


class ProjectGitignoreTemplateManager(RetrieveMixin, RESTManager):
    _path = "/projects/{project_id}/templates/gitignores"
    _obj_cls = ProjectGitignoreTemplate
    _from_parent_attrs = {"project_id": "id"}

    def get(
        self, id: Union[str, int], lazy: bool = False, **kwargs: Any
    ) -> ProjectGitignoreTemplate:
        return cast(ProjectGitignoreTemplate, super().get(id=id, lazy=lazy, **kwargs))


class ProjectGitlabciymlTemplate(RESTObject):
    _id_attr = "name"


class ProjectGitlabciymlTemplateManager(RetrieveMixin, RESTManager):
    _path = "/projects/{project_id}/templates/gitlab_ci_ymls"
    _obj_cls = ProjectGitlabciymlTemplate
    _from_parent_attrs = {"project_id": "id"}

    def get(
        self, id: Union[str, int], lazy: bool = False, **kwargs: Any
    ) -> ProjectGitlabciymlTemplate:
        return cast(ProjectGitlabciymlTemplate, super().get(id=id, lazy=lazy, **kwargs))


class ProjectLicenseTemplate(RESTObject):
    _id_attr = "key"


class ProjectLicenseTemplateManager(RetrieveMixin, RESTManager):
    _path = "/projects/{project_id}/templates/licenses"
    _obj_cls = ProjectLicenseTemplate
    _from_parent_attrs = {"project_id": "id"}

    def get(
        self, id: Union[str, int], lazy: bool = False, **kwargs: Any
    ) -> ProjectLicenseTemplate:
        return cast(ProjectLicenseTemplate, super().get(id=id, lazy=lazy, **kwargs))


class ProjectIssueTemplate(RESTObject):
    _id_attr = "name"


class ProjectIssueTemplateManager(RetrieveMixin, RESTManager):
    _path = "/projects/{project_id}/templates/issues"
    _obj_cls = ProjectIssueTemplate
    _from_parent_attrs = {"project_id": "id"}

    def get(
        self, id: Union[str, int], lazy: bool = False, **kwargs: Any
    ) -> ProjectIssueTemplate:
        return cast(ProjectIssueTemplate, super().get(id=id, lazy=lazy, **kwargs))


class ProjectMergeRequestTemplate(RESTObject):
    _id_attr = "name"


class ProjectMergeRequestTemplateManager(RetrieveMixin, RESTManager):
    _path = "/projects/{project_id}/templates/merge_requests"
    _obj_cls = ProjectMergeRequestTemplate
    _from_parent_attrs = {"project_id": "id"}

    def get(
        self, id: Union[str, int], lazy: bool = False, **kwargs: Any
    ) -> ProjectMergeRequestTemplate:
        return cast(
            ProjectMergeRequestTemplate, super().get(id=id, lazy=lazy, **kwargs)
        )

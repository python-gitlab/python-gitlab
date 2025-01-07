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


class Gitignore(RESTObject):
    _id_attr = "name"


class GitignoreManager(RetrieveMixin, RESTManager):
    _path = "/templates/gitignores"
    _obj_cls = Gitignore


class Gitlabciyml(RESTObject):
    _id_attr = "name"


class GitlabciymlManager(RetrieveMixin, RESTManager):
    _path = "/templates/gitlab_ci_ymls"
    _obj_cls = Gitlabciyml


class License(RESTObject):
    _id_attr = "key"


class LicenseManager(RetrieveMixin, RESTManager):
    _path = "/templates/licenses"
    _obj_cls = License
    _list_filters = ("popular",)
    _optional_get_attrs = ("project", "fullname")


class ProjectDockerfileTemplate(RESTObject):
    _id_attr = "name"


class ProjectDockerfileTemplateManager(RetrieveMixin, RESTManager):
    _path = "/projects/{project_id}/templates/dockerfiles"
    _obj_cls = ProjectDockerfileTemplate
    _from_parent_attrs = {"project_id": "id"}


class ProjectGitignoreTemplate(RESTObject):
    _id_attr = "name"


class ProjectGitignoreTemplateManager(RetrieveMixin, RESTManager):
    _path = "/projects/{project_id}/templates/gitignores"
    _obj_cls = ProjectGitignoreTemplate
    _from_parent_attrs = {"project_id": "id"}


class ProjectGitlabciymlTemplate(RESTObject):
    _id_attr = "name"


class ProjectGitlabciymlTemplateManager(RetrieveMixin, RESTManager):
    _path = "/projects/{project_id}/templates/gitlab_ci_ymls"
    _obj_cls = ProjectGitlabciymlTemplate
    _from_parent_attrs = {"project_id": "id"}


class ProjectLicenseTemplate(RESTObject):
    _id_attr = "key"


class ProjectLicenseTemplateManager(RetrieveMixin, RESTManager):
    _path = "/projects/{project_id}/templates/licenses"
    _obj_cls = ProjectLicenseTemplate
    _from_parent_attrs = {"project_id": "id"}


class ProjectIssueTemplate(RESTObject):
    _id_attr = "name"


class ProjectIssueTemplateManager(RetrieveMixin, RESTManager):
    _path = "/projects/{project_id}/templates/issues"
    _obj_cls = ProjectIssueTemplate
    _from_parent_attrs = {"project_id": "id"}


class ProjectMergeRequestTemplate(RESTObject):
    _id_attr = "name"


class ProjectMergeRequestTemplateManager(RetrieveMixin, RESTManager):
    _path = "/projects/{project_id}/templates/merge_requests"
    _obj_cls = ProjectMergeRequestTemplate
    _from_parent_attrs = {"project_id": "id"}

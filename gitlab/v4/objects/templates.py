from gitlab.base import RESTObject
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


class DockerfileManager(RetrieveMixin[Dockerfile]):
    _path = "/templates/dockerfiles"
    _obj_cls = Dockerfile


class Gitignore(RESTObject):
    _id_attr = "name"


class GitignoreManager(RetrieveMixin[Gitignore]):
    _path = "/templates/gitignores"
    _obj_cls = Gitignore


class Gitlabciyml(RESTObject):
    _id_attr = "name"


class GitlabciymlManager(RetrieveMixin[Gitlabciyml]):
    _path = "/templates/gitlab_ci_ymls"
    _obj_cls = Gitlabciyml


class License(RESTObject):
    _id_attr = "key"


class LicenseManager(RetrieveMixin[License]):
    _path = "/templates/licenses"
    _obj_cls = License
    _list_filters = ("popular",)
    _optional_get_attrs = ("project", "fullname")


class ProjectDockerfileTemplate(RESTObject):
    _id_attr = "name"


class ProjectDockerfileTemplateManager(RetrieveMixin[ProjectDockerfileTemplate]):
    _path = "/projects/{project_id}/templates/dockerfiles"
    _obj_cls = ProjectDockerfileTemplate
    _from_parent_attrs = {"project_id": "id"}


class ProjectGitignoreTemplate(RESTObject):
    _id_attr = "name"


class ProjectGitignoreTemplateManager(RetrieveMixin[ProjectGitignoreTemplate]):
    _path = "/projects/{project_id}/templates/gitignores"
    _obj_cls = ProjectGitignoreTemplate
    _from_parent_attrs = {"project_id": "id"}


class ProjectGitlabciymlTemplate(RESTObject):
    _id_attr = "name"


class ProjectGitlabciymlTemplateManager(RetrieveMixin[ProjectGitlabciymlTemplate]):
    _path = "/projects/{project_id}/templates/gitlab_ci_ymls"
    _obj_cls = ProjectGitlabciymlTemplate
    _from_parent_attrs = {"project_id": "id"}


class ProjectLicenseTemplate(RESTObject):
    _id_attr = "key"


class ProjectLicenseTemplateManager(RetrieveMixin[ProjectLicenseTemplate]):
    _path = "/projects/{project_id}/templates/licenses"
    _obj_cls = ProjectLicenseTemplate
    _from_parent_attrs = {"project_id": "id"}


class ProjectIssueTemplate(RESTObject):
    _id_attr = "name"


class ProjectIssueTemplateManager(RetrieveMixin[ProjectIssueTemplate]):
    _path = "/projects/{project_id}/templates/issues"
    _obj_cls = ProjectIssueTemplate
    _from_parent_attrs = {"project_id": "id"}


class ProjectMergeRequestTemplate(RESTObject):
    _id_attr = "name"


class ProjectMergeRequestTemplateManager(RetrieveMixin[ProjectMergeRequestTemplate]):
    _path = "/projects/{project_id}/templates/merge_requests"
    _obj_cls = ProjectMergeRequestTemplate
    _from_parent_attrs = {"project_id": "id"}

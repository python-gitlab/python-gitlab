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
]


class Dockerfile(RESTObject):
    _id_attr = "name"


class DockerfileManager(RetrieveMixin):
    _path = "/templates/dockerfiles"
    _obj_cls = Dockerfile


class Gitignore(RESTObject):
    _id_attr = "name"


class GitignoreManager(RetrieveMixin):
    _path = "/templates/gitignores"
    _obj_cls = Gitignore


class Gitlabciyml(RESTObject):
    _id_attr = "name"


class GitlabciymlManager(RetrieveMixin):
    _path = "/templates/gitlab_ci_ymls"
    _obj_cls = Gitlabciyml


class License(RESTObject):
    _id_attr = "key"


class LicenseManager(RetrieveMixin):
    _path = "/templates/licenses"
    _obj_cls = License
    _list_filters = ("popular",)
    _optional_get_attrs = ("project", "fullname")

from gitlab.base import *  # noqa
from gitlab.mixins import *  # noqa


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

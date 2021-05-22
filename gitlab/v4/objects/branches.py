from gitlab import cli
from gitlab import exceptions as exc
from gitlab.base import RequiredOptional, RESTManager, RESTObject
from gitlab.mixins import NoUpdateMixin, ObjectDeleteMixin

__all__ = [
    "ProjectBranch",
    "ProjectBranchManager",
    "ProjectProtectedBranch",
    "ProjectProtectedBranchManager",
]


class ProjectBranch(ObjectDeleteMixin, RESTObject):
    _id_attr = "name"

    @cli.register_custom_action(
        "ProjectBranch", tuple(), ("developers_can_push", "developers_can_merge")
    )
    @exc.on_http_error(exc.GitlabProtectError)
    def protect(self, developers_can_push=False, developers_can_merge=False, **kwargs):
        """Protect the branch.

        Args:
            developers_can_push (bool): Set to True if developers are allowed
                                        to push to the branch
            developers_can_merge (bool): Set to True if developers are allowed
                                         to merge to the branch
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabProtectError: If the branch could not be protected
        """
        id = self.get_id().replace("/", "%2F")
        path = "%s/%s/protect" % (self.manager.path, id)
        post_data = {
            "developers_can_push": developers_can_push,
            "developers_can_merge": developers_can_merge,
        }
        self.manager.gitlab.http_put(path, post_data=post_data, **kwargs)
        self._attrs["protected"] = True

    @cli.register_custom_action("ProjectBranch")
    @exc.on_http_error(exc.GitlabProtectError)
    def unprotect(self, **kwargs):
        """Unprotect the branch.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabProtectError: If the branch could not be unprotected
        """
        id = self.get_id().replace("/", "%2F")
        path = "%s/%s/unprotect" % (self.manager.path, id)
        self.manager.gitlab.http_put(path, **kwargs)
        self._attrs["protected"] = False


class ProjectBranchManager(NoUpdateMixin, RESTManager):
    _path = "/projects/%(project_id)s/repository/branches"
    _obj_cls = ProjectBranch
    _from_parent_attrs = {"project_id": "id"}
    _create_attrs = RequiredOptional(required=("branch", "ref"))


class ProjectProtectedBranch(ObjectDeleteMixin, RESTObject):
    _id_attr = "name"


class ProjectProtectedBranchManager(NoUpdateMixin, RESTManager):
    _path = "/projects/%(project_id)s/protected_branches"
    _obj_cls = ProjectProtectedBranch
    _from_parent_attrs = {"project_id": "id"}
    _create_attrs = RequiredOptional(
        required=("name",),
        optional=(
            "push_access_level",
            "merge_access_level",
            "unprotect_access_level",
            "allowed_to_push",
            "allowed_to_merge",
            "allowed_to_unprotect",
            "code_owner_approval_required",
        ),
    )

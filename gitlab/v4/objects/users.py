from gitlab import cli, types
from gitlab import exceptions as exc
from gitlab.base import RESTObject
from gitlab.mixins import (
    CRUDMixin,
    CreateMixin,
    DeleteMixin,
    GetWithoutIdMixin,
    ListMixin,
    NoUpdateMixin,
    ObjectDeleteMixin,
    RetrieveMixin,
    SaveMixin,
    UpdateMixin,
)

from .custom_attributes import UserCustomAttributeManager
from .events import UserEventManager


__all__ = [
    "CurrentUserEmail",
    "CurrentUserEmailManager",
    "CurrentUserGPGKey",
    "CurrentUserGPGKeyManager",
    "CurrentUserKey",
    "CurrentUserKeyManager",
    "CurrentUserStatus",
    "CurrentUserStatusManager",
    "CurrentUser",
    "CurrentUserManager",
    "User",
    "UserManager",
    "ProjectUser",
    "ProjectUserManager",
    "UserEmail",
    "UserEmailManager",
    "UserActivities",
    "UserStatus",
    "UserStatusManager",
    "UserActivitiesManager",
    "UserGPGKey",
    "UserGPGKeyManager",
    "UserKey",
    "UserKeyManager",
    "UserIdentityProviderManager",
    "UserImpersonationToken",
    "UserImpersonationTokenManager",
    "UserMembership",
    "UserMembershipManager",
    "UserProject",
    "UserProjectManager",
]


class CurrentUserEmail(ObjectDeleteMixin):
    _short_print_attr = "email"


class CurrentUserEmailManager(RetrieveMixin, CreateMixin, DeleteMixin):
    _path = "/user/emails"
    _obj_cls = CurrentUserEmail
    _create_attrs = (("email",), tuple())


class CurrentUserGPGKey(ObjectDeleteMixin):
    pass


class CurrentUserGPGKeyManager(RetrieveMixin, CreateMixin, DeleteMixin):
    _path = "/user/gpg_keys"
    _obj_cls = CurrentUserGPGKey
    _create_attrs = (("key",), tuple())


class CurrentUserKey(ObjectDeleteMixin):
    _short_print_attr = "title"


class CurrentUserKeyManager(RetrieveMixin, CreateMixin, DeleteMixin):
    _path = "/user/keys"
    _obj_cls = CurrentUserKey
    _create_attrs = (("title", "key"), tuple())


class CurrentUserStatus(SaveMixin):
    _id_attr = None
    _short_print_attr = "message"


class CurrentUserStatusManager(GetWithoutIdMixin, UpdateMixin):
    _path = "/user/status"
    _obj_cls = CurrentUserStatus
    _update_attrs = (tuple(), ("emoji", "message"))


class CurrentUser(RESTObject):
    _id_attr = None
    _short_print_attr = "username"
    _managers = (
        ("status", "CurrentUserStatusManager"),
        ("emails", "CurrentUserEmailManager"),
        ("gpgkeys", "CurrentUserGPGKeyManager"),
        ("keys", "CurrentUserKeyManager"),
    )


class CurrentUserManager(GetWithoutIdMixin):
    _path = "/user"
    _obj_cls = CurrentUser


class User(SaveMixin, ObjectDeleteMixin):
    _short_print_attr = "username"
    _managers = (
        ("customattributes", "UserCustomAttributeManager"),
        ("emails", "UserEmailManager"),
        ("followers_users", "UserFollowersManager"),
        ("following_users", "UserFollowingManager"),
        ("events", "UserEventManager"),
        ("gpgkeys", "UserGPGKeyManager"),
        ("identityproviders", "UserIdentityProviderManager"),
        ("impersonationtokens", "UserImpersonationTokenManager"),
        ("keys", "UserKeyManager"),
        ("memberships", "UserMembershipManager"),
        ("projects", "UserProjectManager"),
        ("status", "UserStatusManager"),
    )

    @cli.register_custom_action("User")
    @exc.on_http_error(exc.GitlabBlockError)
    def block(self, **kwargs):
        """Block the user.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabBlockError: If the user could not be blocked

        Returns:
            bool: Whether the user status has been changed
        """
        path = "/users/%s/block" % self.id
        server_data = self.manager.gitlab.http_post(path, **kwargs)
        if server_data is True:
            self._attrs["state"] = "blocked"
        return server_data

    @cli.register_custom_action("User")
    @exc.on_http_error(exc.GitlabFollowError)
    def follow(self, **kwargs):
        """Follow the user.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabFollowError: If the user could not be followed

        Returns:
            dict: The new object data (*not* a RESTObject)
        """
        path = "/users/%s/follow" % self.id
        return self.manager.gitlab.http_post(path, **kwargs)

    @cli.register_custom_action("User")
    @exc.on_http_error(exc.GitlabUnfollowError)
    def unfollow(self, **kwargs):
        """Unfollow the user.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabUnfollowError: If the user could not be followed

        Returns:
            dict: The new object data (*not* a RESTObject)
        """
        path = "/users/%s/unfollow" % self.id
        return self.manager.gitlab.http_post(path, **kwargs)

    @cli.register_custom_action("User")
    @exc.on_http_error(exc.GitlabUnblockError)
    def unblock(self, **kwargs):
        """Unblock the user.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabUnblockError: If the user could not be unblocked

        Returns:
            bool: Whether the user status has been changed
        """
        path = "/users/%s/unblock" % self.id
        server_data = self.manager.gitlab.http_post(path, **kwargs)
        if server_data is True:
            self._attrs["state"] = "active"
        return server_data

    @cli.register_custom_action("User")
    @exc.on_http_error(exc.GitlabDeactivateError)
    def deactivate(self, **kwargs):
        """Deactivate the user.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabDeactivateError: If the user could not be deactivated

        Returns:
            bool: Whether the user status has been changed
        """
        path = "/users/%s/deactivate" % self.id
        server_data = self.manager.gitlab.http_post(path, **kwargs)
        if server_data:
            self._attrs["state"] = "deactivated"
        return server_data

    @cli.register_custom_action("User")
    @exc.on_http_error(exc.GitlabActivateError)
    def activate(self, **kwargs):
        """Activate the user.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabActivateError: If the user could not be activated

        Returns:
            bool: Whether the user status has been changed
        """
        path = "/users/%s/activate" % self.id
        server_data = self.manager.gitlab.http_post(path, **kwargs)
        if server_data:
            self._attrs["state"] = "active"
        return server_data


class UserManager(CRUDMixin):
    _path = "/users"
    _obj_cls = User

    _list_filters = (
        "active",
        "blocked",
        "username",
        "extern_uid",
        "provider",
        "external",
        "search",
        "custom_attributes",
        "status",
        "two_factor",
    )
    _create_attrs = (
        tuple(),
        (
            "email",
            "username",
            "name",
            "password",
            "reset_password",
            "skype",
            "linkedin",
            "twitter",
            "projects_limit",
            "extern_uid",
            "provider",
            "bio",
            "admin",
            "can_create_group",
            "website_url",
            "skip_confirmation",
            "external",
            "organization",
            "location",
            "avatar",
            "public_email",
            "private_profile",
            "color_scheme_id",
            "theme_id",
        ),
    )
    _update_attrs = (
        ("email", "username", "name"),
        (
            "password",
            "skype",
            "linkedin",
            "twitter",
            "projects_limit",
            "extern_uid",
            "provider",
            "bio",
            "admin",
            "can_create_group",
            "website_url",
            "skip_reconfirmation",
            "external",
            "organization",
            "location",
            "avatar",
            "public_email",
            "private_profile",
            "color_scheme_id",
            "theme_id",
        ),
    )
    _types = {"confirm": types.LowercaseStringAttribute, "avatar": types.ImageAttribute}


class ProjectUser(RESTObject):
    pass


class ProjectUserManager(ListMixin):
    _path = "/projects/%(project_id)s/users"
    _obj_cls = ProjectUser
    _from_parent_attrs = {"project_id": "id"}
    _list_filters = ("search",)


class UserEmail(ObjectDeleteMixin):
    _short_print_attr = "email"


class UserEmailManager(RetrieveMixin, CreateMixin, DeleteMixin):
    _path = "/users/%(user_id)s/emails"
    _obj_cls = UserEmail
    _from_parent_attrs = {"user_id": "id"}
    _create_attrs = (("email",), tuple())


class UserActivities(RESTObject):
    _id_attr = "username"


class UserStatus(RESTObject):
    _id_attr = None
    _short_print_attr = "message"


class UserStatusManager(GetWithoutIdMixin):
    _path = "/users/%(user_id)s/status"
    _obj_cls = UserStatus
    _from_parent_attrs = {"user_id": "id"}


class UserActivitiesManager(ListMixin):
    _path = "/user/activities"
    _obj_cls = UserActivities


class UserGPGKey(ObjectDeleteMixin):
    pass


class UserGPGKeyManager(RetrieveMixin, CreateMixin, DeleteMixin):
    _path = "/users/%(user_id)s/gpg_keys"
    _obj_cls = UserGPGKey
    _from_parent_attrs = {"user_id": "id"}
    _create_attrs = (("key",), tuple())


class UserKey(ObjectDeleteMixin):
    pass


class UserKeyManager(ListMixin, CreateMixin, DeleteMixin):
    _path = "/users/%(user_id)s/keys"
    _obj_cls = UserKey
    _from_parent_attrs = {"user_id": "id"}
    _create_attrs = (("title", "key"), tuple())


class UserIdentityProviderManager(DeleteMixin):
    """Manager for user identities.

    This manager does not actually manage objects but enables
    functionality for deletion of user identities by provider.
    """

    _path = "/users/%(user_id)s/identities"
    _from_parent_attrs = {"user_id": "id"}


class UserImpersonationToken(ObjectDeleteMixin):
    pass


class UserImpersonationTokenManager(NoUpdateMixin):
    _path = "/users/%(user_id)s/impersonation_tokens"
    _obj_cls = UserImpersonationToken
    _from_parent_attrs = {"user_id": "id"}
    _create_attrs = (("name", "scopes"), ("expires_at",))
    _list_filters = ("state",)


class UserMembership(RESTObject):
    _id_attr = "source_id"


class UserMembershipManager(RetrieveMixin):
    _path = "/users/%(user_id)s/memberships"
    _obj_cls = UserMembership
    _from_parent_attrs = {"user_id": "id"}
    _list_filters = ("type",)


# Having this outside projects avoids circular imports due to ProjectUser
class UserProject(RESTObject):
    pass


class UserProjectManager(ListMixin, CreateMixin):
    _path = "/projects/user/%(user_id)s"
    _obj_cls = UserProject
    _from_parent_attrs = {"user_id": "id"}
    _create_attrs = (
        ("name",),
        (
            "default_branch",
            "issues_enabled",
            "wall_enabled",
            "merge_requests_enabled",
            "wiki_enabled",
            "snippets_enabled",
            "public",
            "visibility",
            "description",
            "builds_enabled",
            "public_builds",
            "import_url",
            "only_allow_merge_if_build_succeeds",
        ),
    )
    _list_filters = (
        "archived",
        "visibility",
        "order_by",
        "sort",
        "search",
        "simple",
        "owned",
        "membership",
        "starred",
        "statistics",
        "with_issues_enabled",
        "with_merge_requests_enabled",
        "with_custom_attributes",
        "with_programming_language",
        "wiki_checksum_failed",
        "repository_checksum_failed",
        "min_access_level",
        "id_after",
        "id_before",
    )

    def list(self, **kwargs):
        """Retrieve a list of objects.

        Args:
            all (bool): If True, return all the items, without pagination
            per_page (int): Number of items to retrieve per request
            page (int): ID of the page to return (starts with page 1)
            as_list (bool): If set to False and no pagination option is
                defined, return a generator instead of a list
            **kwargs: Extra options to send to the server (e.g. sudo)

        Returns:
            list: The list of objects, or a generator if `as_list` is False

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabListError: If the server cannot perform the request
        """
        if self._parent:
            path = "/users/%s/projects" % self._parent.id
        else:
            path = "/users/%s/projects" % kwargs["user_id"]
        return ListMixin.list(self, path=path, **kwargs)


class UserFollowersManager(ListMixin):
    _path = "/users/%(user_id)s/followers"
    _obj_cls = User
    _from_parent_attrs = {"user_id": "id"}


class UserFollowingManager(ListMixin):
    _path = "/users/%(user_id)s/following"
    _obj_cls = User
    _from_parent_attrs = {"user_id": "id"}

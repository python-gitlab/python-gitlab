from gitlab import exceptions as exc
from gitlab.mixins import GetWithoutIdMixin, SaveMixin, UpdateMixin


__all__ = [
    "ApplicationSettings",
    "ApplicationSettingsManager",
]


class ApplicationSettings(SaveMixin):
    _id_attr = None


class ApplicationSettingsManager(GetWithoutIdMixin, UpdateMixin):
    _path = "/application/settings"
    _obj_cls = ApplicationSettings
    _update_attrs = (
        tuple(),
        (
            "id",
            "default_projects_limit",
            "signup_enabled",
            "password_authentication_enabled_for_web",
            "gravatar_enabled",
            "sign_in_text",
            "created_at",
            "updated_at",
            "home_page_url",
            "default_branch_protection",
            "restricted_visibility_levels",
            "max_attachment_size",
            "session_expire_delay",
            "default_project_visibility",
            "default_snippet_visibility",
            "default_group_visibility",
            "outbound_local_requests_whitelist",
            "domain_whitelist",
            "domain_blacklist_enabled",
            "domain_blacklist",
            "external_authorization_service_enabled",
            "external_authorization_service_url",
            "external_authorization_service_default_label",
            "external_authorization_service_timeout",
            "user_oauth_applications",
            "after_sign_out_path",
            "container_registry_token_expire_delay",
            "repository_storages",
            "plantuml_enabled",
            "plantuml_url",
            "terminal_max_session_time",
            "polling_interval_multiplier",
            "rsa_key_restriction",
            "dsa_key_restriction",
            "ecdsa_key_restriction",
            "ed25519_key_restriction",
            "first_day_of_week",
            "enforce_terms",
            "terms",
            "performance_bar_allowed_group_id",
            "instance_statistics_visibility_private",
            "user_show_add_ssh_key_message",
            "file_template_project_id",
            "local_markdown_version",
            "asset_proxy_enabled",
            "asset_proxy_url",
            "asset_proxy_whitelist",
            "geo_node_allowed_ips",
            "allow_local_requests_from_hooks_and_services",
            "allow_local_requests_from_web_hooks_and_services",
            "allow_local_requests_from_system_hooks",
        ),
    )

    @exc.on_http_error(exc.GitlabUpdateError)
    def update(self, id=None, new_data=None, **kwargs):
        """Update an object on the server.

        Args:
            id: ID of the object to update (can be None if not required)
            new_data: the update data for the object
            **kwargs: Extra options to send to the server (e.g. sudo)

        Returns:
            dict: The new object data (*not* a RESTObject)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabUpdateError: If the server cannot perform the request
        """
        new_data = new_data or {}
        data = new_data.copy()
        if "domain_whitelist" in data and data["domain_whitelist"] is None:
            data.pop("domain_whitelist")
        super(ApplicationSettingsManager, self).update(id, data, **kwargs)

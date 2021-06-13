from typing import Any, Callable, cast, Dict, List, Optional, TYPE_CHECKING, Union

import requests

from gitlab import cli, client
from gitlab import exceptions as exc
from gitlab import types, utils
from gitlab.base import RequiredOptional, RESTManager, RESTObject
from gitlab.mixins import (
    CreateMixin,
    CRUDMixin,
    ListMixin,
    ObjectDeleteMixin,
    RefreshMixin,
    SaveMixin,
    UpdateMixin,
)

from .access_requests import ProjectAccessRequestManager  # noqa: F401
from .audit_events import ProjectAuditEventManager  # noqa: F401
from .badges import ProjectBadgeManager  # noqa: F401
from .boards import ProjectBoardManager  # noqa: F401
from .branches import ProjectBranchManager, ProjectProtectedBranchManager  # noqa: F401
from .clusters import ProjectClusterManager  # noqa: F401
from .commits import ProjectCommitManager  # noqa: F401
from .container_registry import ProjectRegistryRepositoryManager  # noqa: F401
from .custom_attributes import ProjectCustomAttributeManager  # noqa: F401
from .deploy_keys import ProjectKeyManager  # noqa: F401
from .deploy_tokens import ProjectDeployTokenManager  # noqa: F401
from .deployments import ProjectDeploymentManager  # noqa: F401
from .environments import ProjectEnvironmentManager  # noqa: F401
from .events import ProjectEventManager  # noqa: F401
from .export_import import ProjectExportManager, ProjectImportManager  # noqa: F401
from .files import ProjectFileManager  # noqa: F401
from .hooks import ProjectHookManager  # noqa: F401
from .issues import ProjectIssueManager  # noqa: F401
from .jobs import ProjectJobManager  # noqa: F401
from .labels import ProjectLabelManager  # noqa: F401
from .members import ProjectMemberAllManager, ProjectMemberManager  # noqa: F401
from .merge_request_approvals import (  # noqa: F401
    ProjectApprovalManager,
    ProjectApprovalRuleManager,
)
from .merge_requests import ProjectMergeRequestManager  # noqa: F401
from .milestones import ProjectMilestoneManager  # noqa: F401
from .notes import ProjectNoteManager  # noqa: F401
from .notification_settings import ProjectNotificationSettingsManager  # noqa: F401
from .packages import GenericPackageManager, ProjectPackageManager  # noqa: F401
from .pages import ProjectPagesDomainManager  # noqa: F401
from .pipelines import (  # noqa: F401
    ProjectPipeline,
    ProjectPipelineManager,
    ProjectPipelineScheduleManager,
)
from .project_access_tokens import ProjectAccessTokenManager  # noqa: F401
from .push_rules import ProjectPushRulesManager  # noqa: F401
from .releases import ProjectReleaseManager  # noqa: F401
from .repositories import RepositoryMixin
from .runners import ProjectRunnerManager  # noqa: F401
from .services import ProjectServiceManager  # noqa: F401
from .snippets import ProjectSnippetManager  # noqa: F401
from .statistics import (  # noqa: F401
    ProjectAdditionalStatisticsManager,
    ProjectIssuesStatisticsManager,
)
from .tags import ProjectProtectedTagManager, ProjectTagManager  # noqa: F401
from .triggers import ProjectTriggerManager  # noqa: F401
from .users import ProjectUserManager  # noqa: F401
from .variables import ProjectVariableManager  # noqa: F401
from .wikis import ProjectWikiManager  # noqa: F401

__all__ = [
    "GroupProject",
    "GroupProjectManager",
    "Project",
    "ProjectManager",
    "ProjectFork",
    "ProjectForkManager",
    "ProjectRemoteMirror",
    "ProjectRemoteMirrorManager",
]


class GroupProject(RESTObject):
    pass


class GroupProjectManager(ListMixin, RESTManager):
    _path = "/groups/%(group_id)s/projects"
    _obj_cls = GroupProject
    _from_parent_attrs = {"group_id": "id"}
    _list_filters = (
        "archived",
        "visibility",
        "order_by",
        "sort",
        "search",
        "simple",
        "owned",
        "starred",
        "with_custom_attributes",
        "include_subgroups",
        "with_issues_enabled",
        "with_merge_requests_enabled",
        "with_shared",
        "min_access_level",
        "with_security_reports",
    )


class Project(RefreshMixin, SaveMixin, ObjectDeleteMixin, RepositoryMixin, RESTObject):
    _short_print_attr = "path"
    _managers = (
        ("access_tokens", "ProjectAccessTokenManager"),
        ("accessrequests", "ProjectAccessRequestManager"),
        ("approvals", "ProjectApprovalManager"),
        ("approvalrules", "ProjectApprovalRuleManager"),
        ("badges", "ProjectBadgeManager"),
        ("boards", "ProjectBoardManager"),
        ("branches", "ProjectBranchManager"),
        ("jobs", "ProjectJobManager"),
        ("commits", "ProjectCommitManager"),
        ("customattributes", "ProjectCustomAttributeManager"),
        ("deployments", "ProjectDeploymentManager"),
        ("environments", "ProjectEnvironmentManager"),
        ("events", "ProjectEventManager"),
        ("audit_events", "ProjectAuditEventManager"),
        ("exports", "ProjectExportManager"),
        ("files", "ProjectFileManager"),
        ("forks", "ProjectForkManager"),
        ("generic_packages", "GenericPackageManager"),
        ("hooks", "ProjectHookManager"),
        ("keys", "ProjectKeyManager"),
        ("imports", "ProjectImportManager"),
        ("issues", "ProjectIssueManager"),
        ("labels", "ProjectLabelManager"),
        ("members", "ProjectMemberManager"),
        ("members_all", "ProjectMemberAllManager"),
        ("mergerequests", "ProjectMergeRequestManager"),
        ("milestones", "ProjectMilestoneManager"),
        ("notes", "ProjectNoteManager"),
        ("notificationsettings", "ProjectNotificationSettingsManager"),
        ("packages", "ProjectPackageManager"),
        ("pagesdomains", "ProjectPagesDomainManager"),
        ("pipelines", "ProjectPipelineManager"),
        ("protectedbranches", "ProjectProtectedBranchManager"),
        ("protectedtags", "ProjectProtectedTagManager"),
        ("pipelineschedules", "ProjectPipelineScheduleManager"),
        ("pushrules", "ProjectPushRulesManager"),
        ("releases", "ProjectReleaseManager"),
        ("remote_mirrors", "ProjectRemoteMirrorManager"),
        ("repositories", "ProjectRegistryRepositoryManager"),
        ("runners", "ProjectRunnerManager"),
        ("services", "ProjectServiceManager"),
        ("snippets", "ProjectSnippetManager"),
        ("tags", "ProjectTagManager"),
        ("users", "ProjectUserManager"),
        ("triggers", "ProjectTriggerManager"),
        ("variables", "ProjectVariableManager"),
        ("wikis", "ProjectWikiManager"),
        ("clusters", "ProjectClusterManager"),
        ("additionalstatistics", "ProjectAdditionalStatisticsManager"),
        ("issues_statistics", "ProjectIssuesStatisticsManager"),
        ("issuesstatistics", "ProjectIssuesStatisticsManager"),  # Deprecated
        ("deploytokens", "ProjectDeployTokenManager"),
    )

    @cli.register_custom_action("Project", ("forked_from_id",))
    @exc.on_http_error(exc.GitlabCreateError)
    def create_fork_relation(self, forked_from_id: int, **kwargs: Any) -> None:
        """Create a forked from/to relation between existing projects.

        Args:
            forked_from_id (int): The ID of the project that was forked from
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabCreateError: If the relation could not be created
        """
        path = "/projects/%s/fork/%s" % (self.get_id(), forked_from_id)
        self.manager.gitlab.http_post(path, **kwargs)

    @cli.register_custom_action("Project")
    @exc.on_http_error(exc.GitlabDeleteError)
    def delete_fork_relation(self, **kwargs: Any) -> None:
        """Delete a forked relation between existing projects.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabDeleteError: If the server failed to perform the request
        """
        path = "/projects/%s/fork" % self.get_id()
        self.manager.gitlab.http_delete(path, **kwargs)

    @cli.register_custom_action("Project")
    @exc.on_http_error(exc.GitlabGetError)
    def languages(self, **kwargs: Any) -> Union[Dict[str, Any], requests.Response]:
        """Get languages used in the project with percentage value.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabGetError: If the server failed to perform the request
        """
        path = "/projects/%s/languages" % self.get_id()
        return self.manager.gitlab.http_get(path, **kwargs)

    @cli.register_custom_action("Project")
    @exc.on_http_error(exc.GitlabCreateError)
    def star(self, **kwargs: Any) -> None:
        """Star a project.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabCreateError: If the server failed to perform the request
        """
        path = "/projects/%s/star" % self.get_id()
        server_data = self.manager.gitlab.http_post(path, **kwargs)
        if TYPE_CHECKING:
            assert isinstance(server_data, dict)
        self._update_attrs(server_data)

    @cli.register_custom_action("Project")
    @exc.on_http_error(exc.GitlabDeleteError)
    def unstar(self, **kwargs: Any) -> None:
        """Unstar a project.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabDeleteError: If the server failed to perform the request
        """
        path = "/projects/%s/unstar" % self.get_id()
        server_data = self.manager.gitlab.http_post(path, **kwargs)
        if TYPE_CHECKING:
            assert isinstance(server_data, dict)
        self._update_attrs(server_data)

    @cli.register_custom_action("Project")
    @exc.on_http_error(exc.GitlabCreateError)
    def archive(self, **kwargs: Any) -> None:
        """Archive a project.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabCreateError: If the server failed to perform the request
        """
        path = "/projects/%s/archive" % self.get_id()
        server_data = self.manager.gitlab.http_post(path, **kwargs)
        if TYPE_CHECKING:
            assert isinstance(server_data, dict)
        self._update_attrs(server_data)

    @cli.register_custom_action("Project")
    @exc.on_http_error(exc.GitlabDeleteError)
    def unarchive(self, **kwargs: Any) -> None:
        """Unarchive a project.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabDeleteError: If the server failed to perform the request
        """
        path = "/projects/%s/unarchive" % self.get_id()
        server_data = self.manager.gitlab.http_post(path, **kwargs)
        if TYPE_CHECKING:
            assert isinstance(server_data, dict)
        self._update_attrs(server_data)

    @cli.register_custom_action(
        "Project", ("group_id", "group_access"), ("expires_at",)
    )
    @exc.on_http_error(exc.GitlabCreateError)
    def share(
        self,
        group_id: int,
        group_access: int,
        expires_at: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """Share the project with a group.

        Args:
            group_id (int): ID of the group.
            group_access (int): Access level for the group.
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabCreateError: If the server failed to perform the request
        """
        path = "/projects/%s/share" % self.get_id()
        data = {
            "group_id": group_id,
            "group_access": group_access,
            "expires_at": expires_at,
        }
        self.manager.gitlab.http_post(path, post_data=data, **kwargs)

    @cli.register_custom_action("Project", ("group_id",))
    @exc.on_http_error(exc.GitlabDeleteError)
    def unshare(self, group_id: int, **kwargs: Any) -> None:
        """Delete a shared project link within a group.

        Args:
            group_id (int): ID of the group.
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabDeleteError: If the server failed to perform the request
        """
        path = "/projects/%s/share/%s" % (self.get_id(), group_id)
        self.manager.gitlab.http_delete(path, **kwargs)

    # variables not supported in CLI
    @cli.register_custom_action("Project", ("ref", "token"))
    @exc.on_http_error(exc.GitlabCreateError)
    def trigger_pipeline(
        self,
        ref: str,
        token: str,
        variables: Optional[Dict[str, Any]] = None,
        **kwargs: Any
    ) -> ProjectPipeline:
        """Trigger a CI build.

        See https://gitlab.com/help/ci/triggers/README.md#trigger-a-build

        Args:
            ref (str): Commit to build; can be a branch name or a tag
            token (str): The trigger token
            variables (dict): Variables passed to the build script
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabCreateError: If the server failed to perform the request
        """
        variables = variables or {}
        path = "/projects/%s/trigger/pipeline" % self.get_id()
        post_data = {"ref": ref, "token": token, "variables": variables}
        attrs = self.manager.gitlab.http_post(path, post_data=post_data, **kwargs)
        if TYPE_CHECKING:
            assert isinstance(attrs, dict)
        return ProjectPipeline(self.pipelines, attrs)

    @cli.register_custom_action("Project")
    @exc.on_http_error(exc.GitlabHousekeepingError)
    def housekeeping(self, **kwargs: Any) -> None:
        """Start the housekeeping task.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabHousekeepingError: If the server failed to perform the
                                     request
        """
        path = "/projects/%s/housekeeping" % self.get_id()
        self.manager.gitlab.http_post(path, **kwargs)

    # see #56 - add file attachment features
    @cli.register_custom_action("Project", ("filename", "filepath"))
    @exc.on_http_error(exc.GitlabUploadError)
    def upload(
        self,
        filename: str,
        filedata: Optional[bytes] = None,
        filepath: Optional[str] = None,
        **kwargs: Any
    ) -> Dict[str, Any]:
        """Upload the specified file into the project.

        .. note::

            Either ``filedata`` or ``filepath`` *MUST* be specified.

        Args:
            filename (str): The name of the file being uploaded
            filedata (bytes): The raw data of the file being uploaded
            filepath (str): The path to a local file to upload (optional)

        Raises:
            GitlabConnectionError: If the server cannot be reached
            GitlabUploadError: If the file upload fails
            GitlabUploadError: If ``filedata`` and ``filepath`` are not
                specified
            GitlabUploadError: If both ``filedata`` and ``filepath`` are
                specified

        Returns:
            dict: A ``dict`` with the keys:
                * ``alt`` - The alternate text for the upload
                * ``url`` - The direct url to the uploaded file
                * ``markdown`` - Markdown for the uploaded file
        """
        if filepath is None and filedata is None:
            raise exc.GitlabUploadError("No file contents or path specified")

        if filedata is not None and filepath is not None:
            raise exc.GitlabUploadError("File contents and file path specified")

        if filepath is not None:
            with open(filepath, "rb") as f:
                filedata = f.read()

        url = "/projects/%(id)s/uploads" % {"id": self.id}
        file_info = {"file": (filename, filedata)}
        data = self.manager.gitlab.http_post(url, files=file_info)

        if TYPE_CHECKING:
            assert isinstance(data, dict)
        return {"alt": data["alt"], "url": data["url"], "markdown": data["markdown"]}

    @cli.register_custom_action("Project", optional=("wiki",))
    @exc.on_http_error(exc.GitlabGetError)
    def snapshot(
        self,
        wiki: bool = False,
        streamed: bool = False,
        action: Optional[Callable] = None,
        chunk_size: int = 1024,
        **kwargs: Any
    ) -> Optional[bytes]:
        """Return a snapshot of the repository.

        Args:
            wiki (bool): If True return the wiki repository
            streamed (bool): If True the data will be processed by chunks of
                `chunk_size` and each chunk is passed to `action` for
                treatment.
            action (callable): Callable responsible of dealing with chunk of
                data
            chunk_size (int): Size of each chunk
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabGetError: If the content could not be retrieved

        Returns:
            str: The uncompressed tar archive of the repository
        """
        path = "/projects/%s/snapshot" % self.get_id()
        result = self.manager.gitlab.http_get(
            path, streamed=streamed, raw=True, **kwargs
        )
        if TYPE_CHECKING:
            assert isinstance(result, requests.Response)
        return utils.response_content(result, streamed, action, chunk_size)

    @cli.register_custom_action("Project", ("scope", "search"))
    @exc.on_http_error(exc.GitlabSearchError)
    def search(
        self, scope: str, search: str, **kwargs: Any
    ) -> Union[client.GitlabList, List[Dict[str, Any]]]:
        """Search the project resources matching the provided string.'

        Args:
            scope (str): Scope of the search
            search (str): Search string
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabSearchError: If the server failed to perform the request

        Returns:
            GitlabList: A list of dicts describing the resources found.
        """
        data = {"scope": scope, "search": search}
        path = "/projects/%s/search" % self.get_id()
        return self.manager.gitlab.http_list(path, query_data=data, **kwargs)

    @cli.register_custom_action("Project")
    @exc.on_http_error(exc.GitlabCreateError)
    def mirror_pull(self, **kwargs: Any) -> None:
        """Start the pull mirroring process for the project.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabCreateError: If the server failed to perform the request
        """
        path = "/projects/%s/mirror/pull" % self.get_id()
        self.manager.gitlab.http_post(path, **kwargs)

    @cli.register_custom_action("Project", ("to_namespace",))
    @exc.on_http_error(exc.GitlabTransferProjectError)
    def transfer_project(self, to_namespace: str, **kwargs: Any) -> None:
        """Transfer a project to the given namespace ID

        Args:
            to_namespace (str): ID or path of the namespace to transfer the
            project to
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabTransferProjectError: If the project could not be transfered
        """
        path = "/projects/%s/transfer" % (self.id,)
        self.manager.gitlab.http_put(
            path, post_data={"namespace": to_namespace}, **kwargs
        )

    @cli.register_custom_action("Project", ("ref_name", "job"), ("job_token",))
    @exc.on_http_error(exc.GitlabGetError)
    def artifacts(
        self,
        ref_name: str,
        job: str,
        streamed: bool = False,
        action: Optional[Callable] = None,
        chunk_size: int = 1024,
        **kwargs: Any
    ) -> Optional[bytes]:
        """Get the job artifacts archive from a specific tag or branch.

        Args:
            ref_name (str): Branch or tag name in repository. HEAD or SHA references
            are not supported.
            artifact_path (str): Path to a file inside the artifacts archive.
            job (str): The name of the job.
            job_token (str): Job token for multi-project pipeline triggers.
            streamed (bool): If True the data will be processed by chunks of
                `chunk_size` and each chunk is passed to `action` for
                treatment
            action (callable): Callable responsible of dealing with chunk of
                data
            chunk_size (int): Size of each chunk
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabGetError: If the artifacts could not be retrieved

        Returns:
            str: The artifacts if `streamed` is False, None otherwise.
        """
        path = "/projects/%s/jobs/artifacts/%s/download" % (self.get_id(), ref_name)
        result = self.manager.gitlab.http_get(
            path, job=job, streamed=streamed, raw=True, **kwargs
        )
        if TYPE_CHECKING:
            assert isinstance(result, requests.Response)
        return utils.response_content(result, streamed, action, chunk_size)

    @cli.register_custom_action("Project", ("ref_name", "artifact_path", "job"))
    @exc.on_http_error(exc.GitlabGetError)
    def artifact(
        self,
        ref_name: str,
        artifact_path: str,
        job: str,
        streamed: bool = False,
        action: Optional[Callable] = None,
        chunk_size: int = 1024,
        **kwargs: Any
    ) -> Optional[bytes]:
        """Download a single artifact file from a specific tag or branch from within the job’s artifacts archive.

        Args:
            ref_name (str): Branch or tag name in repository. HEAD or SHA references are not supported.
            artifact_path (str): Path to a file inside the artifacts archive.
            job (str): The name of the job.
            streamed (bool): If True the data will be processed by chunks of
                `chunk_size` and each chunk is passed to `action` for
                treatment
            action (callable): Callable responsible of dealing with chunk of
                data
            chunk_size (int): Size of each chunk
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabGetError: If the artifacts could not be retrieved

        Returns:
            str: The artifacts if `streamed` is False, None otherwise.
        """

        path = "/projects/%s/jobs/artifacts/%s/raw/%s?job=%s" % (
            self.get_id(),
            ref_name,
            artifact_path,
            job,
        )
        result = self.manager.gitlab.http_get(
            path, streamed=streamed, raw=True, **kwargs
        )
        if TYPE_CHECKING:
            assert isinstance(result, requests.Response)
        return utils.response_content(result, streamed, action, chunk_size)


class ProjectManager(CRUDMixin, RESTManager):
    _path = "/projects"
    _obj_cls = Project
    # Please keep these _create_attrs in same order as they are at:
    # https://docs.gitlab.com/ee/api/projects.html#create-project
    _create_attrs = RequiredOptional(
        optional=(
            "name",
            "path",
            "allow_merge_on_skipped_pipeline",
            "analytics_access_level",
            "approvals_before_merge",
            "auto_cancel_pending_pipelines",
            "auto_devops_deploy_strategy",
            "auto_devops_enabled",
            "autoclose_referenced_issues",
            "avatar",
            "build_coverage_regex",
            "build_git_strategy",
            "build_timeout",
            "builds_access_level",
            "ci_config_path",
            "container_expiration_policy_attributes",
            "container_registry_enabled",
            "default_branch",
            "description",
            "emails_disabled",
            "external_authorization_classification_label",
            "forking_access_level",
            "group_with_project_templates_id",
            "import_url",
            "initialize_with_readme",
            "issues_access_level",
            "issues_enabled",
            "jobs_enabled",
            "lfs_enabled",
            "merge_method",
            "merge_requests_access_level",
            "merge_requests_enabled",
            "mirror_trigger_builds",
            "mirror",
            "namespace_id",
            "operations_access_level",
            "only_allow_merge_if_all_discussions_are_resolved",
            "only_allow_merge_if_pipeline_succeeds",
            "packages_enabled",
            "pages_access_level",
            "requirements_access_level",
            "printing_merge_request_link_enabled",
            "public_builds",
            "remove_source_branch_after_merge",
            "repository_access_level",
            "repository_storage",
            "request_access_enabled",
            "resolve_outdated_diff_discussions",
            "shared_runners_enabled",
            "show_default_award_emojis",
            "snippets_access_level",
            "snippets_enabled",
            "tag_list",
            "template_name",
            "template_project_id",
            "use_custom_template",
            "visibility",
            "wiki_access_level",
            "wiki_enabled",
        ),
    )
    # Please keep these _update_attrs in same order as they are at:
    # https://docs.gitlab.com/ee/api/projects.html#edit-project
    _update_attrs = RequiredOptional(
        optional=(
            "allow_merge_on_skipped_pipeline",
            "analytics_access_level",
            "approvals_before_merge",
            "auto_cancel_pending_pipelines",
            "auto_devops_deploy_strategy",
            "auto_devops_enabled",
            "autoclose_referenced_issues",
            "avatar",
            "build_coverage_regex",
            "build_git_strategy",
            "build_timeout",
            "builds_access_level",
            "ci_config_path",
            "ci_default_git_depth",
            "ci_forward_deployment_enabled",
            "container_expiration_policy_attributes",
            "container_registry_enabled",
            "default_branch",
            "description",
            "emails_disabled",
            "external_authorization_classification_label",
            "forking_access_level",
            "import_url",
            "issues_access_level",
            "issues_enabled",
            "jobs_enabled",
            "lfs_enabled",
            "merge_method",
            "merge_requests_access_level",
            "merge_requests_enabled",
            "mirror_overwrites_diverged_branches",
            "mirror_trigger_builds",
            "mirror_user_id",
            "mirror",
            "name",
            "operations_access_level",
            "only_allow_merge_if_all_discussions_are_resolved",
            "only_allow_merge_if_pipeline_succeeds",
            "only_mirror_protected_branches",
            "packages_enabled",
            "pages_access_level",
            "requirements_access_level",
            "restrict_user_defined_variables",
            "path",
            "public_builds",
            "remove_source_branch_after_merge",
            "repository_access_level",
            "repository_storage",
            "request_access_enabled",
            "resolve_outdated_diff_discussions",
            "service_desk_enabled",
            "shared_runners_enabled",
            "show_default_award_emojis",
            "snippets_access_level",
            "snippets_enabled",
            "suggestion_commit_message",
            "tag_list",
            "visibility",
            "wiki_access_level",
            "wiki_enabled",
            "issues_template",
            "merge_requests_template",
        ),
    )
    _list_filters = (
        "archived",
        "id_after",
        "id_before",
        "last_activity_after",
        "last_activity_before",
        "membership",
        "min_access_level",
        "order_by",
        "owned",
        "repository_checksum_failed",
        "repository_storage",
        "search_namespaces",
        "search",
        "simple",
        "sort",
        "starred",
        "statistics",
        "topic",
        "visibility",
        "wiki_checksum_failed",
        "with_custom_attributes",
        "with_issues_enabled",
        "with_merge_requests_enabled",
        "with_programming_language",
    )
    _types = {"avatar": types.ImageAttribute, "topic": types.ListAttribute}

    def get(self, id: Union[str, int], lazy: bool = False, **kwargs: Any) -> Project:
        return cast(Project, super().get(id=id, lazy=lazy, **kwargs))

    def import_project(
        self,
        file: str,
        path: str,
        name: Optional[str] = None,
        namespace: Optional[str] = None,
        overwrite: bool = False,
        override_params: Optional[Dict[str, Any]] = None,
        **kwargs: Any
    ) -> Union[Dict[str, Any], requests.Response]:
        """Import a project from an archive file.

        Args:
            file: Data or file object containing the project
            path (str): Name and path for the new project
            namespace (str): The ID or path of the namespace that the project
                will be imported to
            overwrite (bool): If True overwrite an existing project with the
                same path
            override_params (dict): Set the specific settings for the project
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabListError: If the server failed to perform the request

        Returns:
            dict: A representation of the import status.
        """
        files = {"file": ("file.tar.gz", file, "application/octet-stream")}
        data = {"path": path, "overwrite": str(overwrite)}
        if override_params:
            for k, v in override_params.items():
                data["override_params[%s]" % k] = v
        if name is not None:
            data["name"] = name
        if namespace:
            data["namespace"] = namespace
        return self.gitlab.http_post(
            "/projects/import", post_data=data, files=files, **kwargs
        )

    def import_bitbucket_server(
        self,
        bitbucket_server_url: str,
        bitbucket_server_username: str,
        personal_access_token: str,
        bitbucket_server_project: str,
        bitbucket_server_repo: str,
        new_name: Optional[str] = None,
        target_namespace: Optional[str] = None,
        **kwargs: Any
    ) -> Union[Dict[str, Any], requests.Response]:
        """Import a project from BitBucket Server to Gitlab (schedule the import)

        This method will return when an import operation has been safely queued,
        or an error has occurred. After triggering an import, check the
        ``import_status`` of the newly created project to detect when the import
        operation has completed.

        .. note::
            This request may take longer than most other API requests.
            So this method will specify a 60 second default timeout if none is specified.
            A timeout can be specified via kwargs to override this functionality.

        Args:
            bitbucket_server_url (str): Bitbucket Server URL
            bitbucket_server_username (str): Bitbucket Server Username
            personal_access_token (str): Bitbucket Server personal access
                token/password
            bitbucket_server_project (str): Bitbucket Project Key
            bitbucket_server_repo (str): Bitbucket Repository Name
            new_name (str): New repository name (Optional)
            target_namespace (str): Namespace to import repository into.
                Supports subgroups like /namespace/subgroup (Optional)
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabListError: If the server failed to perform the request

        Returns:
            dict: A representation of the import status.

        Example:

        .. code-block:: python

            gl = gitlab.Gitlab_from_config()
            print("Triggering import")
            result = gl.projects.import_bitbucket_server(
                bitbucket_server_url="https://some.server.url",
                bitbucket_server_username="some_bitbucket_user",
                personal_access_token="my_password_or_access_token",
                bitbucket_server_project="my_project",
                bitbucket_server_repo="my_repo",
                new_name="gl_project_name",
                target_namespace="gl_project_path"
            )
            project = gl.projects.get(ret['id'])
            print("Waiting for import to complete")
            while project.import_status == u'started':
                time.sleep(1.0)
                project = gl.projects.get(project.id)
            print("BitBucket import complete")

        """
        data = {
            "bitbucket_server_url": bitbucket_server_url,
            "bitbucket_server_username": bitbucket_server_username,
            "personal_access_token": personal_access_token,
            "bitbucket_server_project": bitbucket_server_project,
            "bitbucket_server_repo": bitbucket_server_repo,
        }
        if new_name:
            data["new_name"] = new_name
        if target_namespace:
            data["target_namespace"] = target_namespace
        if (
            "timeout" not in kwargs
            or self.gitlab.timeout is None
            or self.gitlab.timeout < 60.0
        ):
            # Ensure that this HTTP request has a longer-than-usual default timeout
            # The base gitlab object tends to have a default that is <10 seconds,
            # and this is too short for this API command, typically.
            # On the order of 24 seconds has been measured on a typical gitlab instance.
            kwargs["timeout"] = 60.0
        result = self.gitlab.http_post(
            "/import/bitbucket_server", post_data=data, **kwargs
        )
        return result

    def import_github(
        self,
        personal_access_token: str,
        repo_id: int,
        target_namespace: str,
        new_name: Optional[str] = None,
        **kwargs: Any
    ) -> Union[Dict[str, Any], requests.Response]:
        """Import a project from Github to Gitlab (schedule the import)

        This method will return when an import operation has been safely queued,
        or an error has occurred. After triggering an import, check the
        ``import_status`` of the newly created project to detect when the import
        operation has completed.

        .. note::
            This request may take longer than most other API requests.
            So this method will specify a 60 second default timeout if none is specified.
            A timeout can be specified via kwargs to override this functionality.

        Args:
            personal_access_token (str): GitHub personal access token
            repo_id (int): Github repository ID
            target_namespace (str): Namespace to import repo into
            new_name (str): New repo name (Optional)
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabListError: If the server failed to perform the request

        Returns:
            dict: A representation of the import status.

        Example:

        .. code-block:: python

            gl = gitlab.Gitlab_from_config()
            print("Triggering import")
            result = gl.projects.import_github(ACCESS_TOKEN,
                                               123456,
                                               "my-group/my-subgroup")
            project = gl.projects.get(ret['id'])
            print("Waiting for import to complete")
            while project.import_status == u'started':
                time.sleep(1.0)
                project = gl.projects.get(project.id)
            print("Github import complete")

        """
        data = {
            "personal_access_token": personal_access_token,
            "repo_id": repo_id,
            "target_namespace": target_namespace,
        }
        if new_name:
            data["new_name"] = new_name
        if (
            "timeout" not in kwargs
            or self.gitlab.timeout is None
            or self.gitlab.timeout < 60.0
        ):
            # Ensure that this HTTP request has a longer-than-usual default timeout
            # The base gitlab object tends to have a default that is <10 seconds,
            # and this is too short for this API command, typically.
            # On the order of 24 seconds has been measured on a typical gitlab instance.
            kwargs["timeout"] = 60.0
        result = self.gitlab.http_post("/import/github", post_data=data, **kwargs)
        return result


class ProjectFork(RESTObject):
    pass


class ProjectForkManager(CreateMixin, ListMixin, RESTManager):
    _path = "/projects/%(project_id)s/forks"
    _obj_cls = ProjectFork
    _from_parent_attrs = {"project_id": "id"}
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
        "with_custom_attributes",
        "with_issues_enabled",
        "with_merge_requests_enabled",
    )
    _create_attrs = RequiredOptional(optional=("namespace",))

    def create(
        self, data: Optional[Dict[str, Any]] = None, **kwargs: Any
    ) -> ProjectFork:
        """Creates a new object.

        Args:
            data (dict): Parameters to send to the server to create the
                         resource
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabCreateError: If the server cannot perform the request

        Returns:
            RESTObject: A new instance of the managed object class build with
                the data sent by the server
        """
        if TYPE_CHECKING:
            assert self.path is not None
        path = self.path[:-1]  # drop the 's'
        return cast(ProjectFork, CreateMixin.create(self, data, path=path, **kwargs))


class ProjectRemoteMirror(SaveMixin, RESTObject):
    pass


class ProjectRemoteMirrorManager(ListMixin, CreateMixin, UpdateMixin, RESTManager):
    _path = "/projects/%(project_id)s/remote_mirrors"
    _obj_cls = ProjectRemoteMirror
    _from_parent_attrs = {"project_id": "id"}
    _create_attrs = RequiredOptional(
        required=("url",), optional=("enabled", "only_protected_branches")
    )
    _update_attrs = RequiredOptional(optional=("enabled", "only_protected_branches"))

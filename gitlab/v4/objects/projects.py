from gitlab import cli, types, utils
from gitlab import exceptions as exc
from gitlab.base import *  # noqa
from gitlab.mixins import *  # noqa

from .access_requests import ProjectAccessRequestManager
from .badges import ProjectBadgeManager
from .boards import ProjectBoardManager
from .branches import ProjectBranchManager, ProjectProtectedBranchManager
from .clusters import ProjectClusterManager
from .commits import ProjectCommitManager
from .container_registry import ProjectRegistryRepositoryManager
from .custom_attributes import ProjectCustomAttributeManager
from .deploy_keys import ProjectKeyManager
from .deploy_tokens import ProjectDeployTokenManager
from .deployments import ProjectDeploymentManager
from .environments import ProjectEnvironmentManager
from .events import ProjectEventManager
from .audit_events import ProjectAuditManager
from .export_import import ProjectExportManager, ProjectImportManager
from .files import ProjectFileManager
from .hooks import ProjectHookManager
from .issues import ProjectIssueManager
from .jobs import ProjectJobManager
from .labels import ProjectLabelManager
from .members import ProjectMemberManager
from .merge_request_approvals import ProjectApprovalManager, ProjectApprovalRuleManager
from .merge_requests import ProjectMergeRequestManager
from .milestones import ProjectMilestoneManager
from .notes import ProjectNoteManager
from .notification_settings import ProjectNotificationSettingsManager
from .packages import ProjectPackageManager
from .pages import ProjectPagesDomainManager
from .pipelines import ProjectPipelineManager, ProjectPipelineScheduleManager
from .push_rules import ProjectPushRulesManager
from .releases import ProjectReleaseManager
from .runners import ProjectRunnerManager
from .services import ProjectServiceManager
from .snippets import ProjectSnippetManager
from .statistics import (
    ProjectAdditionalStatisticsManager,
    ProjectIssuesStatisticsManager,
)
from .tags import ProjectProtectedTagManager, ProjectTagManager
from .triggers import ProjectTriggerManager
from .users import ProjectUserManager
from .variables import ProjectVariableManager
from .wikis import ProjectWikiManager


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


class Project(RefreshMixin, SaveMixin, ObjectDeleteMixin, RESTObject):
    _short_print_attr = "path"
    _managers = (
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
        ("audit_events", "ProjectAuditManager"),
        ("exports", "ProjectExportManager"),
        ("files", "ProjectFileManager"),
        ("forks", "ProjectForkManager"),
        ("hooks", "ProjectHookManager"),
        ("keys", "ProjectKeyManager"),
        ("imports", "ProjectImportManager"),
        ("issues", "ProjectIssueManager"),
        ("labels", "ProjectLabelManager"),
        ("members", "ProjectMemberManager"),
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
        ("issuesstatistics", "ProjectIssuesStatisticsManager"),
        ("deploytokens", "ProjectDeployTokenManager"),
    )

    @cli.register_custom_action("Project", ("submodule", "branch", "commit_sha"))
    @exc.on_http_error(exc.GitlabUpdateError)
    def update_submodule(self, submodule, branch, commit_sha, **kwargs):
        """Update a project submodule

        Args:
            submodule (str): Full path to the submodule
            branch (str): Name of the branch to commit into
            commit_sha (str): Full commit SHA to update the submodule to
            commit_message (str): Commit message. If no message is provided, a default one will be set (optional)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabPutError: If the submodule could not be updated
        """

        submodule = submodule.replace("/", "%2F")  # .replace('.', '%2E')
        path = "/projects/%s/repository/submodules/%s" % (self.get_id(), submodule)
        data = {"branch": branch, "commit_sha": commit_sha}
        if "commit_message" in kwargs:
            data["commit_message"] = kwargs["commit_message"]
        return self.manager.gitlab.http_put(path, post_data=data)

    @cli.register_custom_action("Project", tuple(), ("path", "ref", "recursive"))
    @exc.on_http_error(exc.GitlabGetError)
    def repository_tree(self, path="", ref="", recursive=False, **kwargs):
        """Return a list of files in the repository.

        Args:
            path (str): Path of the top folder (/ by default)
            ref (str): Reference to a commit or branch
            recursive (bool): Whether to get the tree recursively
            all (bool): If True, return all the items, without pagination
            per_page (int): Number of items to retrieve per request
            page (int): ID of the page to return (starts with page 1)
            as_list (bool): If set to False and no pagination option is
                defined, return a generator instead of a list
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabGetError: If the server failed to perform the request

        Returns:
            list: The representation of the tree
        """
        gl_path = "/projects/%s/repository/tree" % self.get_id()
        query_data = {"recursive": recursive}
        if path:
            query_data["path"] = path
        if ref:
            query_data["ref"] = ref
        return self.manager.gitlab.http_list(gl_path, query_data=query_data, **kwargs)

    @cli.register_custom_action("Project", ("sha",))
    @exc.on_http_error(exc.GitlabGetError)
    def repository_blob(self, sha, **kwargs):
        """Return a file by blob SHA.

        Args:
            sha(str): ID of the blob
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabGetError: If the server failed to perform the request

        Returns:
            dict: The blob content and metadata
        """

        path = "/projects/%s/repository/blobs/%s" % (self.get_id(), sha)
        return self.manager.gitlab.http_get(path, **kwargs)

    @cli.register_custom_action("Project", ("sha",))
    @exc.on_http_error(exc.GitlabGetError)
    def repository_raw_blob(
        self, sha, streamed=False, action=None, chunk_size=1024, **kwargs
    ):
        """Return the raw file contents for a blob.

        Args:
            sha(str): ID of the blob
            streamed (bool): If True the data will be processed by chunks of
                `chunk_size` and each chunk is passed to `action` for
                treatment
            action (callable): Callable responsible of dealing with chunk of
                data
            chunk_size (int): Size of each chunk
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabGetError: If the server failed to perform the request

        Returns:
            str: The blob content if streamed is False, None otherwise
        """
        path = "/projects/%s/repository/blobs/%s/raw" % (self.get_id(), sha)
        result = self.manager.gitlab.http_get(
            path, streamed=streamed, raw=True, **kwargs
        )
        return utils.response_content(result, streamed, action, chunk_size)

    @cli.register_custom_action("Project", ("from_", "to"))
    @exc.on_http_error(exc.GitlabGetError)
    def repository_compare(self, from_, to, **kwargs):
        """Return a diff between two branches/commits.

        Args:
            from_(str): Source branch/SHA
            to(str): Destination branch/SHA
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabGetError: If the server failed to perform the request

        Returns:
            str: The diff
        """
        path = "/projects/%s/repository/compare" % self.get_id()
        query_data = {"from": from_, "to": to}
        return self.manager.gitlab.http_get(path, query_data=query_data, **kwargs)

    @cli.register_custom_action("Project")
    @exc.on_http_error(exc.GitlabGetError)
    def repository_contributors(self, **kwargs):
        """Return a list of contributors for the project.

        Args:
            all (bool): If True, return all the items, without pagination
            per_page (int): Number of items to retrieve per request
            page (int): ID of the page to return (starts with page 1)
            as_list (bool): If set to False and no pagination option is
                defined, return a generator instead of a list
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabGetError: If the server failed to perform the request

        Returns:
            list: The contributors
        """
        path = "/projects/%s/repository/contributors" % self.get_id()
        return self.manager.gitlab.http_list(path, **kwargs)

    @cli.register_custom_action("Project", tuple(), ("sha",))
    @exc.on_http_error(exc.GitlabListError)
    def repository_archive(
        self, sha=None, streamed=False, action=None, chunk_size=1024, **kwargs
    ):
        """Return a tarball of the repository.

        Args:
            sha (str): ID of the commit (default branch by default)
            streamed (bool): If True the data will be processed by chunks of
                `chunk_size` and each chunk is passed to `action` for
                treatment
            action (callable): Callable responsible of dealing with chunk of
                data
            chunk_size (int): Size of each chunk
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabListError: If the server failed to perform the request

        Returns:
            str: The binary data of the archive
        """
        path = "/projects/%s/repository/archive" % self.get_id()
        query_data = {}
        if sha:
            query_data["sha"] = sha
        result = self.manager.gitlab.http_get(
            path, query_data=query_data, raw=True, streamed=streamed, **kwargs
        )
        return utils.response_content(result, streamed, action, chunk_size)

    @cli.register_custom_action("Project", ("forked_from_id",))
    @exc.on_http_error(exc.GitlabCreateError)
    def create_fork_relation(self, forked_from_id, **kwargs):
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
    def delete_fork_relation(self, **kwargs):
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
    @exc.on_http_error(exc.GitlabDeleteError)
    def delete_merged_branches(self, **kwargs):
        """Delete merged branches.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabDeleteError: If the server failed to perform the request
        """
        path = "/projects/%s/repository/merged_branches" % self.get_id()
        self.manager.gitlab.http_delete(path, **kwargs)

    @cli.register_custom_action("Project")
    @exc.on_http_error(exc.GitlabGetError)
    def languages(self, **kwargs):
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
    def star(self, **kwargs):
        """Star a project.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabCreateError: If the server failed to perform the request
        """
        path = "/projects/%s/star" % self.get_id()
        server_data = self.manager.gitlab.http_post(path, **kwargs)
        self._update_attrs(server_data)

    @cli.register_custom_action("Project")
    @exc.on_http_error(exc.GitlabDeleteError)
    def unstar(self, **kwargs):
        """Unstar a project.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabDeleteError: If the server failed to perform the request
        """
        path = "/projects/%s/unstar" % self.get_id()
        server_data = self.manager.gitlab.http_post(path, **kwargs)
        self._update_attrs(server_data)

    @cli.register_custom_action("Project")
    @exc.on_http_error(exc.GitlabCreateError)
    def archive(self, **kwargs):
        """Archive a project.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabCreateError: If the server failed to perform the request
        """
        path = "/projects/%s/archive" % self.get_id()
        server_data = self.manager.gitlab.http_post(path, **kwargs)
        self._update_attrs(server_data)

    @cli.register_custom_action("Project")
    @exc.on_http_error(exc.GitlabDeleteError)
    def unarchive(self, **kwargs):
        """Unarchive a project.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabDeleteError: If the server failed to perform the request
        """
        path = "/projects/%s/unarchive" % self.get_id()
        server_data = self.manager.gitlab.http_post(path, **kwargs)
        self._update_attrs(server_data)

    @cli.register_custom_action(
        "Project", ("group_id", "group_access"), ("expires_at",)
    )
    @exc.on_http_error(exc.GitlabCreateError)
    def share(self, group_id, group_access, expires_at=None, **kwargs):
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
    def unshare(self, group_id, **kwargs):
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
    def trigger_pipeline(self, ref, token, variables=None, **kwargs):
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
        return ProjectPipeline(self.pipelines, attrs)

    @cli.register_custom_action("Project")
    @exc.on_http_error(exc.GitlabHousekeepingError)
    def housekeeping(self, **kwargs):
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
    def upload(self, filename, filedata=None, filepath=None, **kwargs):
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
            raise GitlabUploadError("No file contents or path specified")

        if filedata is not None and filepath is not None:
            raise GitlabUploadError("File contents and file path specified")

        if filepath is not None:
            with open(filepath, "rb") as f:
                filedata = f.read()

        url = "/projects/%(id)s/uploads" % {"id": self.id}
        file_info = {"file": (filename, filedata)}
        data = self.manager.gitlab.http_post(url, files=file_info)

        return {"alt": data["alt"], "url": data["url"], "markdown": data["markdown"]}

    @cli.register_custom_action("Project", optional=("wiki",))
    @exc.on_http_error(exc.GitlabGetError)
    def snapshot(
        self, wiki=False, streamed=False, action=None, chunk_size=1024, **kwargs
    ):
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
        return utils.response_content(result, streamed, action, chunk_size)

    @cli.register_custom_action("Project", ("scope", "search"))
    @exc.on_http_error(exc.GitlabSearchError)
    def search(self, scope, search, **kwargs):
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
    def mirror_pull(self, **kwargs):
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
    def transfer_project(self, to_namespace, **kwargs):
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
        self, ref_name, job, streamed=False, action=None, chunk_size=1024, **kwargs
    ):
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
        return utils.response_content(result, streamed, action, chunk_size)

    @cli.register_custom_action("Project", ("ref_name", "artifact_path", "job"))
    @exc.on_http_error(exc.GitlabGetError)
    def artifact(
        self,
        ref_name,
        artifact_path,
        job,
        streamed=False,
        action=None,
        chunk_size=1024,
        **kwargs
    ):
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
        return utils.response_content(result, streamed, action, chunk_size)


class ProjectManager(CRUDMixin, RESTManager):
    _path = "/projects"
    _obj_cls = Project
    _create_attrs = (
        tuple(),
        (
            "name",
            "path",
            "namespace_id",
            "default_branch",
            "description",
            "issues_enabled",
            "merge_requests_enabled",
            "jobs_enabled",
            "wiki_enabled",
            "snippets_enabled",
            "issues_access_level",
            "repository_access_level",
            "merge_requests_access_level",
            "forking_access_level",
            "builds_access_level",
            "wiki_access_level",
            "snippets_access_level",
            "pages_access_level",
            "emails_disabled",
            "resolve_outdated_diff_discussions",
            "container_registry_enabled",
            "container_expiration_policy_attributes",
            "shared_runners_enabled",
            "visibility",
            "import_url",
            "public_builds",
            "only_allow_merge_if_pipeline_succeeds",
            "only_allow_merge_if_all_discussions_are_resolved",
            "merge_method",
            "autoclose_referenced_issues",
            "remove_source_branch_after_merge",
            "lfs_enabled",
            "request_access_enabled",
            "tag_list",
            "avatar",
            "printing_merge_request_link_enabled",
            "build_git_strategy",
            "build_timeout",
            "auto_cancel_pending_pipelines",
            "build_coverage_regex",
            "ci_config_path",
            "auto_devops_enabled",
            "auto_devops_deploy_strategy",
            "repository_storage",
            "approvals_before_merge",
            "external_authorization_classification_label",
            "mirror",
            "mirror_trigger_builds",
            "initialize_with_readme",
            "template_name",
            "template_project_id",
            "use_custom_template",
            "group_with_project_templates_id",
            "packages_enabled",
        ),
    )
    _update_attrs = (
        tuple(),
        (
            "name",
            "path",
            "default_branch",
            "description",
            "issues_enabled",
            "merge_requests_enabled",
            "jobs_enabled",
            "wiki_enabled",
            "snippets_enabled",
            "issues_access_level",
            "repository_access_level",
            "merge_requests_access_level",
            "forking_access_level",
            "builds_access_level",
            "wiki_access_level",
            "snippets_access_level",
            "pages_access_level",
            "emails_disabled",
            "resolve_outdated_diff_discussions",
            "container_registry_enabled",
            "container_expiration_policy_attributes",
            "shared_runners_enabled",
            "visibility",
            "import_url",
            "public_builds",
            "only_allow_merge_if_pipeline_succeeds",
            "only_allow_merge_if_all_discussions_are_resolved",
            "merge_method",
            "autoclose_referenced_issues",
            "suggestion_commit_message",
            "remove_source_branch_after_merge",
            "lfs_enabled",
            "request_access_enabled",
            "tag_list",
            "avatar",
            "build_git_strategy",
            "build_timeout",
            "auto_cancel_pending_pipelines",
            "build_coverage_regex",
            "ci_config_path",
            "ci_default_git_depth",
            "auto_devops_enabled",
            "auto_devops_deploy_strategy",
            "repository_storage",
            "approvals_before_merge",
            "external_authorization_classification_label",
            "mirror",
            "mirror_user_id",
            "mirror_trigger_builds",
            "only_mirror_protected_branches",
            "mirror_overwrites_diverged_branches",
            "packages_enabled",
            "service_desk_enabled",
        ),
    )
    _types = {"avatar": types.ImageAttribute}
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
        "visibility",
        "wiki_checksum_failed",
        "with_custom_attributes",
        "with_issues_enabled",
        "with_merge_requests_enabled",
        "with_programming_language",
    )

    def import_project(
        self,
        file,
        path,
        name=None,
        namespace=None,
        overwrite=False,
        override_params=None,
        **kwargs
    ):
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
        bitbucket_server_url,
        bitbucket_server_username,
        personal_access_token,
        bitbucket_server_project,
        bitbucket_server_repo,
        new_name=None,
        target_namespace=None,
        **kwargs
    ):
        """Import a project from BitBucket Server to Gitlab (schedule the import)

        This method will return when an import operation has been safely queued,
        or an error has occurred. After triggering an import, check the
        `import_status` of the newly created project to detect when the import
        operation has completed.

        NOTE: this request may take longer than most other API requests.
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
        ```
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
        ```
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
        self, personal_access_token, repo_id, target_namespace, new_name=None, **kwargs
    ):
        """Import a project from Github to Gitlab (schedule the import)

        This method will return when an import operation has been safely queued,
        or an error has occurred. After triggering an import, check the
        `import_status` of the newly created project to detect when the import
        operation has completed.

        NOTE: this request may take longer than most other API requests.
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
        ```
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
        ```
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
    _create_attrs = (tuple(), ("namespace",))

    def create(self, data, **kwargs):
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
        path = self.path[:-1]  # drop the 's'
        return CreateMixin.create(self, data, path=path, **kwargs)


class ProjectRemoteMirror(SaveMixin, RESTObject):
    pass


class ProjectRemoteMirrorManager(ListMixin, CreateMixin, UpdateMixin, RESTManager):
    _path = "/projects/%(project_id)s/remote_mirrors"
    _obj_cls = ProjectRemoteMirror
    _from_parent_attrs = {"project_id": "id"}
    _create_attrs = (("url",), ("enabled", "only_protected_branches"))
    _update_attrs = (tuple(), ("enabled", "only_protected_branches"))

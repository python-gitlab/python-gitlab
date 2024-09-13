"""Wrapper for the GitLab API."""

from __future__ import annotations

import os
import re
from typing import (
    Any,
    BinaryIO,
    cast,
    Dict,
    List,
    Optional,
    Tuple,
    Type,
    TYPE_CHECKING,
    Union,
)
from urllib import parse

import requests

import gitlab
import gitlab.config
import gitlab.const
import gitlab.exceptions
from gitlab import _backends, utils

try:
    import gql
    import gql.transport.exceptions
    import graphql
    import httpx

    from ._backends.graphql import GitlabTransport

    _GQL_INSTALLED = True
except ImportError:  # pragma: no cover
    _GQL_INSTALLED = False


REDIRECT_MSG = (
    "python-gitlab detected a {status_code} ({reason!r}) redirection. You must update "
    "your GitLab URL to the correct URL to avoid issues. The redirection was from: "
    "{source!r} to {target!r}"
)


# https://docs.gitlab.com/ee/api/#offset-based-pagination
_PAGINATION_URL = (
    f"https://python-gitlab.readthedocs.io/en/v{gitlab.__version__}/"
    f"api-usage.html#pagination"
)


class Gitlab:
    """Represents a GitLab server connection.

    Args:
        url: The URL of the GitLab server (defaults to https://gitlab.com).
        private_token: The user private token
        oauth_token: An oauth token
        job_token: A CI job token
        ssl_verify: Whether SSL certificates should be validated. If
            the value is a string, it is the path to a CA file used for
            certificate validation.
        timeout: Timeout to use for requests to the GitLab server.
        http_username: Username for HTTP authentication
        http_password: Password for HTTP authentication
        api_version: Gitlab API version to use (support for 4 only)
        pagination: Can be set to 'keyset' to use keyset pagination
        order_by: Set order_by globally
        user_agent: A custom user agent to use for making HTTP requests.
        retry_transient_errors: Whether to retry after 500, 502, 503, 504
            or 52x responses. Defaults to False.
        keep_base_url: keep user-provided base URL for pagination if it
            differs from response headers

    Keyword Args:
        requests.Session session: HTTP Requests Session
        RequestsBackend backend: Backend that will be used to make http requests
    """

    def __init__(
        self,
        url: Optional[str] = None,
        private_token: Optional[str] = None,
        oauth_token: Optional[str] = None,
        job_token: Optional[str] = None,
        ssl_verify: Union[bool, str] = True,
        http_username: Optional[str] = None,
        http_password: Optional[str] = None,
        timeout: Optional[float] = None,
        api_version: str = "4",
        per_page: Optional[int] = None,
        pagination: Optional[str] = None,
        order_by: Optional[str] = None,
        user_agent: str = gitlab.const.USER_AGENT,
        retry_transient_errors: bool = False,
        keep_base_url: bool = False,
        **kwargs: Any,
    ) -> None:
        self._api_version = str(api_version)
        self._server_version: Optional[str] = None
        self._server_revision: Optional[str] = None
        self._base_url = utils.get_base_url(url)
        self._url = f"{self._base_url}/api/v{api_version}"
        #: Timeout to use for requests to gitlab server
        self.timeout = timeout
        self.retry_transient_errors = retry_transient_errors
        self.keep_base_url = keep_base_url
        #: Headers that will be used in request to GitLab
        self.headers = {"User-Agent": user_agent}

        #: Whether SSL certificates should be validated
        self.ssl_verify = ssl_verify

        self.private_token = private_token
        self.http_username = http_username
        self.http_password = http_password
        self.oauth_token = oauth_token
        self.job_token = job_token
        self._set_auth_info()

        #: Create a session object for requests
        _backend: Type[_backends.DefaultBackend] = kwargs.pop(
            "backend", _backends.DefaultBackend
        )
        self._backend = _backend(**kwargs)
        self.session = self._backend.client

        self.per_page = per_page
        self.pagination = pagination
        self.order_by = order_by

        # We only support v4 API at this time
        if self._api_version not in ("4",):
            raise ModuleNotFoundError(f"gitlab.v{self._api_version}.objects")
        # NOTE: We must delay import of gitlab.v4.objects until now or
        # otherwise it will cause circular import errors
        from gitlab.v4 import objects

        self._objects = objects
        self.user: Optional[objects.CurrentUser] = None

        self.broadcastmessages = objects.BroadcastMessageManager(self)
        """See :class:`~gitlab.v4.objects.BroadcastMessageManager`"""
        self.bulk_imports = objects.BulkImportManager(self)
        """See :class:`~gitlab.v4.objects.BulkImportManager`"""
        self.bulk_import_entities = objects.BulkImportAllEntityManager(self)
        """See :class:`~gitlab.v4.objects.BulkImportAllEntityManager`"""
        self.ci_lint = objects.CiLintManager(self)
        """See :class:`~gitlab.v4.objects.CiLintManager`"""
        self.deploykeys = objects.DeployKeyManager(self)
        """See :class:`~gitlab.v4.objects.DeployKeyManager`"""
        self.deploytokens = objects.DeployTokenManager(self)
        """See :class:`~gitlab.v4.objects.DeployTokenManager`"""
        self.geonodes = objects.GeoNodeManager(self)
        """See :class:`~gitlab.v4.objects.GeoNodeManager`"""
        self.gitlabciymls = objects.GitlabciymlManager(self)
        """See :class:`~gitlab.v4.objects.GitlabciymlManager`"""
        self.gitignores = objects.GitignoreManager(self)
        """See :class:`~gitlab.v4.objects.GitignoreManager`"""
        self.groups = objects.GroupManager(self)
        """See :class:`~gitlab.v4.objects.GroupManager`"""
        self.hooks = objects.HookManager(self)
        """See :class:`~gitlab.v4.objects.HookManager`"""
        self.issues = objects.IssueManager(self)
        """See :class:`~gitlab.v4.objects.IssueManager`"""
        self.issues_statistics = objects.IssuesStatisticsManager(self)
        """See :class:`~gitlab.v4.objects.IssuesStatisticsManager`"""
        self.keys = objects.KeyManager(self)
        """See :class:`~gitlab.v4.objects.KeyManager`"""
        self.ldapgroups = objects.LDAPGroupManager(self)
        """See :class:`~gitlab.v4.objects.LDAPGroupManager`"""
        self.licenses = objects.LicenseManager(self)
        """See :class:`~gitlab.v4.objects.LicenseManager`"""
        self.namespaces = objects.NamespaceManager(self)
        """See :class:`~gitlab.v4.objects.NamespaceManager`"""
        self.mergerequests = objects.MergeRequestManager(self)
        """See :class:`~gitlab.v4.objects.MergeRequestManager`"""
        self.notificationsettings = objects.NotificationSettingsManager(self)
        """See :class:`~gitlab.v4.objects.NotificationSettingsManager`"""
        self.projects = objects.ProjectManager(self)
        """See :class:`~gitlab.v4.objects.ProjectManager`"""
        self.registry_repositories = objects.RegistryRepositoryManager(self)
        """See :class:`~gitlab.v4.objects.RegistryRepositoryManager`"""
        self.runners = objects.RunnerManager(self)
        """See :class:`~gitlab.v4.objects.RunnerManager`"""
        self.runners_all = objects.RunnerAllManager(self)
        """See :class:`~gitlab.v4.objects.RunnerManager`"""
        self.settings = objects.ApplicationSettingsManager(self)
        """See :class:`~gitlab.v4.objects.ApplicationSettingsManager`"""
        self.appearance = objects.ApplicationAppearanceManager(self)
        """See :class:`~gitlab.v4.objects.ApplicationAppearanceManager`"""
        self.sidekiq = objects.SidekiqManager(self)
        """See :class:`~gitlab.v4.objects.SidekiqManager`"""
        self.snippets = objects.SnippetManager(self)
        """See :class:`~gitlab.v4.objects.SnippetManager`"""
        self.users = objects.UserManager(self)
        """See :class:`~gitlab.v4.objects.UserManager`"""
        self.todos = objects.TodoManager(self)
        """See :class:`~gitlab.v4.objects.TodoManager`"""
        self.dockerfiles = objects.DockerfileManager(self)
        """See :class:`~gitlab.v4.objects.DockerfileManager`"""
        self.events = objects.EventManager(self)
        """See :class:`~gitlab.v4.objects.EventManager`"""
        self.audit_events = objects.AuditEventManager(self)
        """See :class:`~gitlab.v4.objects.AuditEventManager`"""
        self.features = objects.FeatureManager(self)
        """See :class:`~gitlab.v4.objects.FeatureManager`"""
        self.pagesdomains = objects.PagesDomainManager(self)
        """See :class:`~gitlab.v4.objects.PagesDomainManager`"""
        self.user_activities = objects.UserActivitiesManager(self)
        """See :class:`~gitlab.v4.objects.UserActivitiesManager`"""
        self.applications = objects.ApplicationManager(self)
        """See :class:`~gitlab.v4.objects.ApplicationManager`"""
        self.variables = objects.VariableManager(self)
        """See :class:`~gitlab.v4.objects.VariableManager`"""
        self.personal_access_tokens = objects.PersonalAccessTokenManager(self)
        """See :class:`~gitlab.v4.objects.PersonalAccessTokenManager`"""
        self.topics = objects.TopicManager(self)
        """See :class:`~gitlab.v4.objects.TopicManager`"""
        self.statistics = objects.ApplicationStatisticsManager(self)
        """See :class:`~gitlab.v4.objects.ApplicationStatisticsManager`"""

    def __enter__(self) -> "Gitlab":
        return self

    def __exit__(self, *args: Any) -> None:
        self.session.close()

    def __getstate__(self) -> Dict[str, Any]:
        state = self.__dict__.copy()
        state.pop("_objects")
        return state

    def __setstate__(self, state: Dict[str, Any]) -> None:
        self.__dict__.update(state)
        # We only support v4 API at this time
        if self._api_version not in ("4",):
            raise ModuleNotFoundError(
                f"gitlab.v{self._api_version}.objects"
            )  # pragma: no cover, dead code currently
        # NOTE: We must delay import of gitlab.v4.objects until now or
        # otherwise it will cause circular import errors
        from gitlab.v4 import objects

        self._objects = objects

    @property
    def url(self) -> str:
        """The user-provided server URL."""
        return self._base_url

    @property
    def api_url(self) -> str:
        """The computed API base URL."""
        return self._url

    @property
    def api_version(self) -> str:
        """The API version used (4 only)."""
        return self._api_version

    @classmethod
    def from_config(
        cls,
        gitlab_id: Optional[str] = None,
        config_files: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> "Gitlab":
        """Create a Gitlab connection from configuration files.

        Args:
            gitlab_id: ID of the configuration section.
            config_files list[str]: List of paths to configuration files.

        kwargs:
            session requests.Session: Custom requests Session

        Returns:
            A Gitlab connection.

        Raises:
            gitlab.config.GitlabDataError: If the configuration is not correct.
        """
        config = gitlab.config.GitlabConfigParser(
            gitlab_id=gitlab_id, config_files=config_files
        )
        return cls(
            config.url,
            private_token=config.private_token,
            oauth_token=config.oauth_token,
            job_token=config.job_token,
            ssl_verify=config.ssl_verify,
            timeout=config.timeout,
            http_username=config.http_username,
            http_password=config.http_password,
            api_version=config.api_version,
            per_page=config.per_page,
            pagination=config.pagination,
            order_by=config.order_by,
            user_agent=config.user_agent,
            retry_transient_errors=config.retry_transient_errors,
            **kwargs,
        )

    @classmethod
    def merge_config(
        cls,
        options: Dict[str, Any],
        gitlab_id: Optional[str] = None,
        config_files: Optional[List[str]] = None,
    ) -> "Gitlab":
        """Create a Gitlab connection by merging configuration with
        the following precedence:

        1. Explicitly provided CLI arguments,
        2. Environment variables,
        3. Configuration files:
            a. explicitly defined config files:
                i. via the `--config-file` CLI argument,
                ii. via the `PYTHON_GITLAB_CFG` environment variable,
            b. user-specific config file,
            c. system-level config file,
        4. Environment variables always present in CI (CI_SERVER_URL, CI_JOB_TOKEN).

        Args:
            options: A dictionary of explicitly provided key-value options.
            gitlab_id: ID of the configuration section.
            config_files: List of paths to configuration files.
        Returns:
            (gitlab.Gitlab): A Gitlab connection.

        Raises:
            gitlab.config.GitlabDataError: If the configuration is not correct.
        """
        config = gitlab.config.GitlabConfigParser(
            gitlab_id=gitlab_id, config_files=config_files
        )
        url = (
            options.get("server_url")
            or config.url
            or os.getenv("CI_SERVER_URL")
            or gitlab.const.DEFAULT_URL
        )
        private_token, oauth_token, job_token = cls._merge_auth(options, config)

        return cls(
            url=url,
            private_token=private_token,
            oauth_token=oauth_token,
            job_token=job_token,
            ssl_verify=options.get("ssl_verify") or config.ssl_verify,
            timeout=options.get("timeout") or config.timeout,
            api_version=options.get("api_version") or config.api_version,
            per_page=options.get("per_page") or config.per_page,
            pagination=options.get("pagination") or config.pagination,
            order_by=options.get("order_by") or config.order_by,
            user_agent=options.get("user_agent") or config.user_agent,
        )

    @staticmethod
    def _merge_auth(
        options: Dict[str, Any], config: gitlab.config.GitlabConfigParser
    ) -> Tuple[Optional[str], Optional[str], Optional[str]]:
        """
        Return a tuple where at most one of 3 token types ever has a value.
        Since multiple types of tokens may be present in the environment,
        options, or config files, this precedence ensures we don't
        inadvertently cause errors when initializing the client.

        This is especially relevant when executed in CI where user and
        CI-provided values are both available.
        """
        private_token = options.get("private_token") or config.private_token
        oauth_token = options.get("oauth_token") or config.oauth_token
        job_token = (
            options.get("job_token") or config.job_token or os.getenv("CI_JOB_TOKEN")
        )

        if private_token:
            return (private_token, None, None)
        if oauth_token:
            return (None, oauth_token, None)
        if job_token:
            return (None, None, job_token)

        return (None, None, None)

    def auth(self) -> None:
        """Performs an authentication using private token. Warns the user if a
        potentially misconfigured URL is detected on the client or server side.

        The `user` attribute will hold a `gitlab.objects.CurrentUser` object on
        success.
        """
        self.user = self._objects.CurrentUserManager(self).get()

        if hasattr(self.user, "web_url") and hasattr(self.user, "username"):
            self._check_url(self.user.web_url, path=self.user.username)

    def version(self) -> Tuple[str, str]:
        """Returns the version and revision of the gitlab server.

        Note that self.version and self.revision will be set on the gitlab
        object.

        Returns:
            The server version and server revision.
                ('unknown', 'unknown') if the server doesn't perform as expected.
        """
        if self._server_version is None:
            try:
                data = self.http_get("/version")
                if isinstance(data, dict):
                    self._server_version = data["version"]
                    self._server_revision = data["revision"]
                else:
                    self._server_version = "unknown"
                    self._server_revision = "unknown"
            except Exception:
                self._server_version = "unknown"
                self._server_revision = "unknown"

        return cast(str, self._server_version), cast(str, self._server_revision)

    @gitlab.exceptions.on_http_error(gitlab.exceptions.GitlabMarkdownError)
    def markdown(
        self, text: str, gfm: bool = False, project: Optional[str] = None, **kwargs: Any
    ) -> str:
        """Render an arbitrary Markdown document.

        Args:
            text: The markdown text to render
            gfm: Render text using GitLab Flavored Markdown. Default is False
            project: Full path of a project used a context when `gfm` is True
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabMarkdownError: If the server cannot perform the request

        Returns:
            The HTML rendering of the markdown text.
        """
        post_data = {"text": text, "gfm": gfm}
        if project is not None:
            post_data["project"] = project
        data = self.http_post("/markdown", post_data=post_data, **kwargs)
        if TYPE_CHECKING:
            assert not isinstance(data, requests.Response)
            assert isinstance(data["html"], str)
        return data["html"]

    @gitlab.exceptions.on_http_error(gitlab.exceptions.GitlabLicenseError)
    def get_license(self, **kwargs: Any) -> Dict[str, Union[str, Dict[str, str]]]:
        """Retrieve information about the current license.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabGetError: If the server cannot perform the request

        Returns:
            The current license information
        """
        result = self.http_get("/license", **kwargs)
        if isinstance(result, dict):
            return result
        return {}

    @gitlab.exceptions.on_http_error(gitlab.exceptions.GitlabLicenseError)
    def set_license(self, license: str, **kwargs: Any) -> Dict[str, Any]:
        """Add a new license.

        Args:
            license: The license string
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabPostError: If the server cannot perform the request

        Returns:
            The new license information
        """
        data = {"license": license}
        result = self.http_post("/license", post_data=data, **kwargs)
        if TYPE_CHECKING:
            assert not isinstance(result, requests.Response)
        return result

    def _set_auth_info(self) -> None:
        tokens = [
            token
            for token in [self.private_token, self.oauth_token, self.job_token]
            if token
        ]
        if len(tokens) > 1:
            raise ValueError(
                "Only one of private_token, oauth_token or job_token should "
                "be defined"
            )
        if (self.http_username and not self.http_password) or (
            not self.http_username and self.http_password
        ):
            raise ValueError("Both http_username and http_password should be defined")
        if tokens and self.http_username:
            raise ValueError(
                "Only one of token authentications or http "
                "authentication should be defined"
            )

        self._auth: Optional[requests.auth.AuthBase] = None
        if self.private_token:
            self._auth = _backends.PrivateTokenAuth(self.private_token)

        if self.oauth_token:
            self._auth = _backends.OAuthTokenAuth(self.oauth_token)

        if self.job_token:
            self._auth = _backends.JobTokenAuth(self.job_token)

        if self.http_username and self.http_password:
            self._auth = requests.auth.HTTPBasicAuth(
                self.http_username, self.http_password
            )

    def enable_debug(self, mask_credentials: bool = True) -> None:
        import logging
        from http import client

        client.HTTPConnection.debuglevel = 1
        logging.basicConfig()
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)

        httpclient_log = logging.getLogger("http.client")
        httpclient_log.propagate = True
        httpclient_log.setLevel(logging.DEBUG)

        requests_log = logging.getLogger("requests.packages.urllib3")
        requests_log.setLevel(logging.DEBUG)
        requests_log.propagate = True

        # shadow http.client prints to log()
        # https://stackoverflow.com/a/16337639
        def print_as_log(*args: Any) -> None:
            httpclient_log.log(logging.DEBUG, " ".join(args))

        setattr(client, "print", print_as_log)

        if not mask_credentials:
            return

        token = self.private_token or self.oauth_token or self.job_token
        handler = logging.StreamHandler()
        handler.setFormatter(utils.MaskingFormatter(masked=token))
        logger.handlers.clear()
        logger.addHandler(handler)

    def _get_session_opts(self) -> Dict[str, Any]:
        return {
            "headers": self.headers.copy(),
            "auth": self._auth,
            "timeout": self.timeout,
            "verify": self.ssl_verify,
        }

    def _build_url(self, path: str) -> str:
        """Returns the full url from path.

        If path is already a url, return it unchanged. If it's a path, append
        it to the stored url.

        Returns:
            The full URL
        """
        if path.startswith("http://") or path.startswith("https://"):
            return path
        return f"{self._url}{path}"

    def _check_url(self, url: Optional[str], *, path: str = "api") -> Optional[str]:
        """
        Checks if ``url`` starts with a different base URL from the user-provided base
        URL and warns the user before returning it. If ``keep_base_url`` is set to
        ``True``, instead returns the URL massaged to match the user-provided base URL.
        """
        if not url or url.startswith(self.url):
            return url

        match = re.match(rf"(^.*?)/{path}", url)
        if not match:
            return url

        base_url = match.group(1)
        if self.keep_base_url:
            return url.replace(base_url, f"{self._base_url}")

        utils.warn(
            message=(
                f"The base URL in the server response differs from the user-provided "
                f"base URL ({self.url} -> {base_url}).\nThis is usually caused by a "
                f"misconfigured base URL on your side or a misconfigured external_url "
                f"on the server side, and can lead to broken pagination and unexpected "
                f"behavior. If this is intentional, use `keep_base_url=True` when "
                f"initializing the Gitlab instance to keep the user-provided base URL."
            ),
            category=UserWarning,
        )
        return url

    @staticmethod
    def _check_redirects(result: requests.Response) -> None:
        # Check the requests history to detect 301/302 redirections.
        # If the initial verb is POST or PUT, the redirected request will use a
        # GET request, leading to unwanted behaviour.
        # If we detect a redirection with a POST or a PUT request, we
        # raise an exception with a useful error message.
        if not result.history:
            return

        for item in result.history:
            if item.status_code not in (301, 302):
                continue
            # GET and HEAD methods can be redirected without issue
            if item.request.method in ("GET", "HEAD"):
                continue
            target = item.headers.get("location")
            raise gitlab.exceptions.RedirectError(
                REDIRECT_MSG.format(
                    status_code=item.status_code,
                    reason=item.reason,
                    source=item.url,
                    target=target,
                )
            )

    def http_request(
        self,
        verb: str,
        path: str,
        query_data: Optional[Dict[str, Any]] = None,
        post_data: Optional[Union[Dict[str, Any], bytes, BinaryIO]] = None,
        raw: bool = False,
        streamed: bool = False,
        files: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = None,
        obey_rate_limit: bool = True,
        retry_transient_errors: Optional[bool] = None,
        max_retries: int = 10,
        **kwargs: Any,
    ) -> requests.Response:
        """Make an HTTP request to the Gitlab server.

        Args:
            verb: The HTTP method to call ('get', 'post', 'put', 'delete')
            path: Path or full URL to query ('/projects' or
                        'http://whatever/v4/api/projecs')
            query_data: Data to send as query parameters
            post_data: Data to send in the body (will be converted to
                              json by default)
            raw: If True, do not convert post_data to json
            streamed: Whether the data should be streamed
            files: The files to send to the server
            timeout: The timeout, in seconds, for the request
            obey_rate_limit: Whether to obey 429 Too Many Request
                                    responses. Defaults to True.
            retry_transient_errors: Whether to retry after 500, 502, 503, 504
                or 52x responses. Defaults to False.
            max_retries: Max retries after 429 or transient errors,
                               set to -1 to retry forever. Defaults to 10.
            **kwargs: Extra options to send to the server (e.g. sudo)

        Returns:
            A requests result object.

        Raises:
            GitlabHttpError: When the return code is not 2xx
        """
        query_data = query_data or {}
        raw_url = self._build_url(path)

        # parse user-provided URL params to ensure we don't add our own duplicates
        parsed = parse.urlparse(raw_url)
        params = parse.parse_qs(parsed.query)
        utils.copy_dict(src=query_data, dest=params)

        url = parse.urlunparse(parsed._replace(query=""))

        # Deal with kwargs: by default a user uses kwargs to send data to the
        # gitlab server, but this generates problems (python keyword conflicts
        # and python-gitlab/gitlab conflicts).
        # So we provide a `query_parameters` key: if it's there we use its dict
        # value as arguments for the gitlab server, and ignore the other
        # arguments, except pagination ones (per_page and page)
        if "query_parameters" in kwargs:
            utils.copy_dict(src=kwargs["query_parameters"], dest=params)
            for arg in ("per_page", "page"):
                if arg in kwargs:
                    params[arg] = kwargs[arg]
        else:
            utils.copy_dict(src=kwargs, dest=params)

        opts = self._get_session_opts()

        verify = opts.pop("verify")
        opts_timeout = opts.pop("timeout")
        # If timeout was passed into kwargs, allow it to override the default
        if timeout is None:
            timeout = opts_timeout
        if retry_transient_errors is None:
            retry_transient_errors = self.retry_transient_errors

        # We need to deal with json vs. data when uploading files
        send_data = self._backend.prepare_send_data(files, post_data, raw)
        opts["headers"]["Content-type"] = send_data.content_type

        retry = utils.Retry(
            max_retries=max_retries,
            obey_rate_limit=obey_rate_limit,
            retry_transient_errors=retry_transient_errors,
        )

        while True:
            try:
                result = self._backend.http_request(
                    method=verb,
                    url=url,
                    json=send_data.json,
                    data=send_data.data,
                    params=params,
                    timeout=timeout,
                    verify=verify,
                    stream=streamed,
                    **opts,
                )
            except (requests.ConnectionError, requests.exceptions.ChunkedEncodingError):
                if retry.handle_retry():
                    continue
                raise

            self._check_redirects(result.response)

            if 200 <= result.status_code < 300:
                return result.response

            if retry.handle_retry_on_status(
                result.status_code, result.headers, result.reason
            ):
                continue

            error_message = result.content
            try:
                error_json = result.json()
                for k in ("message", "error"):
                    if k in error_json:
                        error_message = error_json[k]
            except (KeyError, ValueError, TypeError):
                pass

            if result.status_code == 401:
                raise gitlab.exceptions.GitlabAuthenticationError(
                    response_code=result.status_code,
                    error_message=error_message,
                    response_body=result.content,
                )

            raise gitlab.exceptions.GitlabHttpError(
                response_code=result.status_code,
                error_message=error_message,
                response_body=result.content,
            )

    def http_get(
        self,
        path: str,
        query_data: Optional[Dict[str, Any]] = None,
        streamed: bool = False,
        raw: bool = False,
        **kwargs: Any,
    ) -> Union[Dict[str, Any], requests.Response]:
        """Make a GET request to the Gitlab server.

        Args:
            path: Path or full URL to query ('/projects' or
                        'http://whatever/v4/api/projecs')
            query_data: Data to send as query parameters
            streamed: Whether the data should be streamed
            raw: If True do not try to parse the output as json
            **kwargs: Extra options to send to the server (e.g. sudo)

        Returns:
            A requests result object is streamed is True or the content type is
            not json.
            The parsed json data otherwise.

        Raises:
            GitlabHttpError: When the return code is not 2xx
            GitlabParsingError: If the json data could not be parsed
        """
        query_data = query_data or {}
        result = self.http_request(
            "get", path, query_data=query_data, streamed=streamed, **kwargs
        )
        content_type = utils.get_content_type(result.headers.get("Content-Type"))

        if content_type == "application/json" and not streamed and not raw:
            try:
                json_result = result.json()
                if TYPE_CHECKING:
                    assert isinstance(json_result, dict)
                return json_result
            except Exception as e:
                raise gitlab.exceptions.GitlabParsingError(
                    error_message="Failed to parse the server message"
                ) from e
        else:
            return result

    def http_head(
        self, path: str, query_data: Optional[Dict[str, Any]] = None, **kwargs: Any
    ) -> "requests.structures.CaseInsensitiveDict[Any]":
        """Make a HEAD request to the Gitlab server.

        Args:
            path: Path or full URL to query ('/projects' or
                        'http://whatever/v4/api/projecs')
            query_data: Data to send as query parameters
            **kwargs: Extra options to send to the server (e.g. sudo, page,
                      per_page)
        Returns:
            A requests.header object
        Raises:
            GitlabHttpError: When the return code is not 2xx
        """

        query_data = query_data or {}
        result = self.http_request("head", path, query_data=query_data, **kwargs)
        return result.headers

    def http_list(
        self,
        path: str,
        query_data: Optional[Dict[str, Any]] = None,
        *,
        iterator: Optional[bool] = None,
        message_details: Optional[utils.WarnMessageData] = None,
        **kwargs: Any,
    ) -> Union["GitlabList", List[Dict[str, Any]]]:
        """Make a GET request to the Gitlab server for list-oriented queries.

        Args:
            path: Path or full URL to query ('/projects' or
                        'http://whatever/v4/api/projects')
            query_data: Data to send as query parameters
            iterator: Indicate if should return a generator (True)
            **kwargs: Extra options to send to the server (e.g. sudo, page,
                      per_page)

        Returns:
            A list of the objects returned by the server. If `iterator` is
            True and no pagination-related arguments (`page`, `per_page`,
            `get_all`) are defined then a GitlabList object (generator) is returned
            instead. This object will make API calls when needed to fetch the
            next items from the server.

        Raises:
            GitlabHttpError: When the return code is not 2xx
            GitlabParsingError: If the json data could not be parsed
        """
        query_data = query_data or {}

        # Provide a `get_all`` param to avoid clashes with `all` API attributes.
        get_all = kwargs.pop("get_all", None)

        if get_all is None:
            # For now, keep `all` without deprecation.
            get_all = kwargs.pop("all", None)

        url = self._build_url(path)

        page = kwargs.get("page")

        if iterator and page is not None:
            arg_used_message = f"iterator={iterator}"
            utils.warn(
                message=(
                    f"`{arg_used_message}` and `page={page}` were both specified. "
                    f"`{arg_used_message}` will be ignored and a `list` will be "
                    f"returned."
                ),
                category=UserWarning,
            )

        if iterator and page is None:
            # Generator requested
            return GitlabList(self, url, query_data, **kwargs)

        if get_all is True:
            return list(GitlabList(self, url, query_data, **kwargs))

        # pagination requested, we return a list
        gl_list = GitlabList(self, url, query_data, get_next=False, **kwargs)
        items = list(gl_list)

        def should_emit_warning() -> bool:
            # No warning is emitted if any of the following conditions apply:
            # * `get_all=False` was set in the `list()` call.
            # * `page` was set in the `list()` call.
            # * GitLab did not return the `x-per-page` header.
            # * Number of items received is less than per-page value.
            # * Number of items received is >= total available.
            if get_all is False:
                return False
            if page is not None:
                return False
            if gl_list.per_page is None:
                return False
            if len(items) < gl_list.per_page:
                return False
            if gl_list.total is not None and len(items) >= gl_list.total:
                return False
            return True

        if not should_emit_warning():
            return items

        # Warn the user that they are only going to retrieve `per_page`
        # maximum items. This is a common cause of issues filed.
        total_items = "many" if gl_list.total is None else gl_list.total
        if message_details is not None:
            message = message_details.message.format_map(
                {
                    "len_items": len(items),
                    "per_page": gl_list.per_page,
                    "total_items": total_items,
                }
            )
            show_caller = message_details.show_caller
        else:
            message = (
                f"Calling a `list()` method without specifying `get_all=True` or "
                f"`iterator=True` will return a maximum of {gl_list.per_page} items. "
                f"Your query returned {len(items)} of {total_items} items. See "
                f"{_PAGINATION_URL} for more details. If this was done intentionally, "
                f"then this warning can be supressed by adding the argument "
                f"`get_all=False` to the `list()` call."
            )
            show_caller = True
        utils.warn(
            message=message,
            category=UserWarning,
            show_caller=show_caller,
        )
        return items

    def http_post(
        self,
        path: str,
        query_data: Optional[Dict[str, Any]] = None,
        post_data: Optional[Dict[str, Any]] = None,
        raw: bool = False,
        files: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Union[Dict[str, Any], requests.Response]:
        """Make a POST request to the Gitlab server.

        Args:
            path: Path or full URL to query ('/projects' or
                        'http://whatever/v4/api/projecs')
            query_data: Data to send as query parameters
            post_data: Data to send in the body (will be converted to
                              json by default)
            raw: If True, do not convert post_data to json
            files: The files to send to the server
            **kwargs: Extra options to send to the server (e.g. sudo)

        Returns:
            The parsed json returned by the server if json is return, else the
            raw content

        Raises:
            GitlabHttpError: When the return code is not 2xx
            GitlabParsingError: If the json data could not be parsed
        """
        query_data = query_data or {}
        post_data = post_data or {}

        result = self.http_request(
            "post",
            path,
            query_data=query_data,
            post_data=post_data,
            files=files,
            raw=raw,
            **kwargs,
        )
        content_type = utils.get_content_type(result.headers.get("Content-Type"))

        try:
            if content_type == "application/json":
                json_result = result.json()
                if TYPE_CHECKING:
                    assert isinstance(json_result, dict)
                return json_result
        except Exception as e:
            raise gitlab.exceptions.GitlabParsingError(
                error_message="Failed to parse the server message"
            ) from e
        return result

    def http_put(
        self,
        path: str,
        query_data: Optional[Dict[str, Any]] = None,
        post_data: Optional[Union[Dict[str, Any], bytes, BinaryIO]] = None,
        raw: bool = False,
        files: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Union[Dict[str, Any], requests.Response]:
        """Make a PUT request to the Gitlab server.

        Args:
            path: Path or full URL to query ('/projects' or
                        'http://whatever/v4/api/projecs')
            query_data: Data to send as query parameters
            post_data: Data to send in the body (will be converted to
                              json by default)
            raw: If True, do not convert post_data to json
            files: The files to send to the server
            **kwargs: Extra options to send to the server (e.g. sudo)

        Returns:
            The parsed json returned by the server.

        Raises:
            GitlabHttpError: When the return code is not 2xx
            GitlabParsingError: If the json data could not be parsed
        """
        query_data = query_data or {}
        post_data = post_data or {}

        result = self.http_request(
            "put",
            path,
            query_data=query_data,
            post_data=post_data,
            files=files,
            raw=raw,
            **kwargs,
        )
        if result.status_code in gitlab.const.NO_JSON_RESPONSE_CODES:
            return result
        try:
            json_result = result.json()
            if TYPE_CHECKING:
                assert isinstance(json_result, dict)
            return json_result
        except Exception as e:
            raise gitlab.exceptions.GitlabParsingError(
                error_message="Failed to parse the server message"
            ) from e

    def http_patch(
        self,
        path: str,
        *,
        query_data: Optional[Dict[str, Any]] = None,
        post_data: Optional[Union[Dict[str, Any], bytes]] = None,
        raw: bool = False,
        **kwargs: Any,
    ) -> Union[Dict[str, Any], requests.Response]:
        """Make a PATCH request to the Gitlab server.

        Args:
            path: Path or full URL to query ('/projects' or
                        'http://whatever/v4/api/projecs')
            query_data: Data to send as query parameters
            post_data: Data to send in the body (will be converted to
                              json by default)
            raw: If True, do not convert post_data to json
            **kwargs: Extra options to send to the server (e.g. sudo)

        Returns:
            The parsed json returned by the server.

        Raises:
            GitlabHttpError: When the return code is not 2xx
            GitlabParsingError: If the json data could not be parsed
        """
        query_data = query_data or {}
        post_data = post_data or {}

        result = self.http_request(
            "patch",
            path,
            query_data=query_data,
            post_data=post_data,
            raw=raw,
            **kwargs,
        )
        if result.status_code in gitlab.const.NO_JSON_RESPONSE_CODES:
            return result
        try:
            json_result = result.json()
            if TYPE_CHECKING:
                assert isinstance(json_result, dict)
            return json_result
        except Exception as e:
            raise gitlab.exceptions.GitlabParsingError(
                error_message="Failed to parse the server message"
            ) from e

    def http_delete(self, path: str, **kwargs: Any) -> requests.Response:
        """Make a DELETE request to the Gitlab server.

        Args:
            path: Path or full URL to query ('/projects' or
                        'http://whatever/v4/api/projecs')
            **kwargs: Extra options to send to the server (e.g. sudo)

        Returns:
            The requests object.

        Raises:
            GitlabHttpError: When the return code is not 2xx
        """
        return self.http_request("delete", path, **kwargs)

    @gitlab.exceptions.on_http_error(gitlab.exceptions.GitlabSearchError)
    def search(
        self, scope: str, search: str, **kwargs: Any
    ) -> Union["GitlabList", List[Dict[str, Any]]]:
        """Search GitLab resources matching the provided string.'

        Args:
            scope: Scope of the search
            search: Search string
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabSearchError: If the server failed to perform the request

        Returns:
            A list of dicts describing the resources found.
        """
        data = {"scope": scope, "search": search}
        return self.http_list("/search", query_data=data, **kwargs)


class GitlabList:
    """Generator representing a list of remote objects.

    The object handles the links returned by a query to the API, and will call
    the API again when needed.
    """

    def __init__(
        self,
        gl: Gitlab,
        url: str,
        query_data: Dict[str, Any],
        get_next: bool = True,
        **kwargs: Any,
    ) -> None:
        self._gl = gl

        # Preserve kwargs for subsequent queries
        self._kwargs = kwargs.copy()

        self._query(url, query_data, **self._kwargs)
        self._get_next = get_next

        # Remove query_parameters from kwargs, which are saved via the `next` URL
        self._kwargs.pop("query_parameters", None)

    def _query(
        self, url: str, query_data: Optional[Dict[str, Any]] = None, **kwargs: Any
    ) -> None:
        query_data = query_data or {}
        result = self._gl.http_request("get", url, query_data=query_data, **kwargs)
        try:
            next_url = result.links["next"]["url"]
        except KeyError:
            next_url = None

        self._next_url = self._gl._check_url(next_url)
        self._current_page: Optional[str] = result.headers.get("X-Page")
        self._prev_page: Optional[str] = result.headers.get("X-Prev-Page")
        self._next_page: Optional[str] = result.headers.get("X-Next-Page")
        self._per_page: Optional[str] = result.headers.get("X-Per-Page")
        self._total_pages: Optional[str] = result.headers.get("X-Total-Pages")
        self._total: Optional[str] = result.headers.get("X-Total")

        try:
            self._data: List[Dict[str, Any]] = result.json()
        except Exception as e:
            raise gitlab.exceptions.GitlabParsingError(
                error_message="Failed to parse the server message"
            ) from e

        self._current = 0

    @property
    def current_page(self) -> int:
        """The current page number."""
        if TYPE_CHECKING:
            assert self._current_page is not None
        return int(self._current_page)

    @property
    def prev_page(self) -> Optional[int]:
        """The previous page number.

        If None, the current page is the first.
        """
        return int(self._prev_page) if self._prev_page else None

    @property
    def next_page(self) -> Optional[int]:
        """The next page number.

        If None, the current page is the last.
        """
        return int(self._next_page) if self._next_page else None

    @property
    def per_page(self) -> Optional[int]:
        """The number of items per page."""
        return int(self._per_page) if self._per_page is not None else None

    # NOTE(jlvillal): When a query returns more than 10,000 items, GitLab doesn't return
    # the headers 'x-total-pages' and 'x-total'. In those cases we return None.
    # https://docs.gitlab.com/ee/user/gitlab_com/index.html#pagination-response-headers
    @property
    def total_pages(self) -> Optional[int]:
        """The total number of pages."""
        if self._total_pages is not None:
            return int(self._total_pages)
        return None

    @property
    def total(self) -> Optional[int]:
        """The total number of items."""
        if self._total is not None:
            return int(self._total)
        return None

    def __iter__(self) -> "GitlabList":
        return self

    def __len__(self) -> int:
        if self._total is None:
            return 0
        return int(self._total)

    def __next__(self) -> Dict[str, Any]:
        return self.next()

    def next(self) -> Dict[str, Any]:
        try:
            item = self._data[self._current]
            self._current += 1
            return item
        except IndexError:
            pass

        if self._next_url and self._get_next is True:
            self._query(self._next_url, **self._kwargs)
            return self.next()

        raise StopIteration


class GraphQL:
    def __init__(
        self,
        url: Optional[str] = None,
        *,
        token: Optional[str] = None,
        ssl_verify: Union[bool, str] = True,
        client: Optional[httpx.Client] = None,
        timeout: Optional[float] = None,
        user_agent: str = gitlab.const.USER_AGENT,
        fetch_schema_from_transport: bool = False,
        max_retries: int = 10,
        obey_rate_limit: bool = True,
        retry_transient_errors: bool = False,
    ) -> None:
        if not _GQL_INSTALLED:
            raise ImportError(
                "The GraphQL client could not be initialized because "
                "the gql dependencies are not installed. "
                "Install them with 'pip install python-gitlab[graphql]'"
            )
        self._base_url = utils.get_base_url(url)
        self._timeout = timeout
        self._token = token
        self._url = f"{self._base_url}/api/graphql"
        self._user_agent = user_agent
        self._ssl_verify = ssl_verify
        self._max_retries = max_retries
        self._obey_rate_limit = obey_rate_limit
        self._retry_transient_errors = retry_transient_errors

        opts = self._get_client_opts()
        self._http_client = client or httpx.Client(**opts)
        self._transport = GitlabTransport(self._url, client=self._http_client)
        self._client = gql.Client(
            transport=self._transport,
            fetch_schema_from_transport=fetch_schema_from_transport,
        )
        self._gql = gql.gql

    def __enter__(self) -> "GraphQL":
        return self

    def __exit__(self, *args: Any) -> None:
        self._http_client.close()

    def _get_client_opts(self) -> Dict[str, Any]:
        headers = {"User-Agent": self._user_agent}

        if self._token:
            headers["Authorization"] = f"Bearer {self._token}"

        return {
            "headers": headers,
            "timeout": self._timeout,
            "verify": self._ssl_verify,
        }

    def execute(
        self, request: Union[str, graphql.Source], *args: Any, **kwargs: Any
    ) -> Any:
        parsed_document = self._gql(request)
        retry = utils.Retry(
            max_retries=self._max_retries,
            obey_rate_limit=self._obey_rate_limit,
            retry_transient_errors=self._retry_transient_errors,
        )

        while True:
            try:
                result = self._client.execute(parsed_document, *args, **kwargs)
            except gql.transport.exceptions.TransportServerError as e:
                if retry.handle_retry_on_status(
                    status_code=e.code, headers=self._transport.response_headers
                ):
                    continue

                if e.code == 401:
                    raise gitlab.exceptions.GitlabAuthenticationError(
                        response_code=e.code,
                        error_message=str(e),
                    )

                raise gitlab.exceptions.GitlabHttpError(
                    response_code=e.code,
                    error_message=str(e),
                )

            return result

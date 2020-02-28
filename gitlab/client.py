# -*- coding: utf-8 -*-
#
# Copyright (C) 2013-2017 Gauvain Pocentek <gauvain@pocentek.net>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""Wrapper for the GitLab API."""

import importlib
import time
from typing import Union

import httpx

import gitlab
import gitlab.config
from gitlab import exceptions as exc
from gitlab import utils
from gitlab.exceptions import GitlabHttpError, GitlabParsingError, on_http_error
from gitlab.types import GitlabList

REDIRECT_MSG = (
    "python-gitlab detected an http to https redirection. You "
    "must update your GitLab URL to use https:// to avoid issues."
)


def _sanitize(value):
    if isinstance(value, dict):
        return dict((k, _sanitize(v)) for k, v in value.items())
    if isinstance(value, str):
        return value.replace("/", "%2F")
    return value


class BaseGitlab:
    _httpx_client_class: Union[httpx.Client, httpx.AsyncClient]

    """Represents a GitLab server connection.

    Args:
        url (str): The URL of the GitLab server.
        private_token (str): The user private token
        oauth_token (str): An oauth token
        job_token (str): A CI job token
        ssl_verify (bool|str): Whether SSL certificates should be validated. If
            the value is a string, it is the path to a CA file used for
            certificate validation.
        timeout (float): Timeout to use for requests to the GitLab server.
        http_username (str): Username for HTTP authentication
        http_password (str): Password for HTTP authentication
        api_version (str): Gitlab API version to use (support for 4 only)
        per_page (int): Number of items to retrieve per request
        pagination (str): Can be set to 'keyset' to use keyset pagination
        order_by (str): Set order_by globally
    """

    def __init__(
        self,
        url,
        private_token=None,
        oauth_token=None,
        job_token=None,
        ssl_verify=True,
        http_username=None,
        http_password=None,
        timeout=None,
        api_version="4",
        client=None,
        per_page=None,
        pagination=None,
        order_by=None,
    ):
        self._api_version = str(api_version)
        self._server_version = self._server_revision = None
        self._base_url = url.rstrip("/")
        self._url = "%s/api/v%s" % (self._base_url, api_version)
        #: Timeout to use for requests to gitlab server
        self.timeout = timeout
        #: Headers that will be used in request to GitLab
        self.headers = {"User-Agent": "%s/%s" % (gitlab.__title__, gitlab.__version__)}

        #: Whether SSL certificates should be validated
        self.ssl_verify = ssl_verify

        self.private_token = private_token
        self.http_username = http_username
        self.http_password = http_password
        self.oauth_token = oauth_token
        self.job_token = job_token
        self._set_auth_info()

        self.client = client or self._get_client()

        self.per_page = per_page
        self.pagination = pagination
        self.order_by = order_by

        objects = importlib.import_module("gitlab.v%s.objects" % self._api_version)
        self._objects = objects

        self.broadcastmessages = objects.BroadcastMessageManager(self)
        self.deploykeys = objects.DeployKeyManager(self)
        self.geonodes = objects.GeoNodeManager(self)
        self.gitlabciymls = objects.GitlabciymlManager(self)
        self.gitignores = objects.GitignoreManager(self)
        self.groups = objects.GroupManager(self)
        self.hooks = objects.HookManager(self)
        self.issues = objects.IssueManager(self)
        self.ldapgroups = objects.LDAPGroupManager(self)
        self.licenses = objects.LicenseManager(self)
        self.namespaces = objects.NamespaceManager(self)
        self.mergerequests = objects.MergeRequestManager(self)
        self.notificationsettings = objects.NotificationSettingsManager(self)
        self.projects = objects.ProjectManager(self)
        self.runners = objects.RunnerManager(self)
        self.settings = objects.ApplicationSettingsManager(self)
        self.appearance = objects.ApplicationAppearanceManager(self)
        self.sidekiq = objects.SidekiqManager(self)
        self.snippets = objects.SnippetManager(self)
        self.users = objects.UserManager(self)
        self.todos = objects.TodoManager(self)
        self.dockerfiles = objects.DockerfileManager(self)
        self.events = objects.EventManager(self)
        self.audit_events = objects.AuditEventManager(self)
        self.features = objects.FeatureManager(self)
        self.pagesdomains = objects.PagesDomainManager(self)
        self.user_activities = objects.UserActivitiesManager(self)

    def __enter__(self):
        return self

    async def __aenter__(self):
        return self

    def __exit__(self, *args):
        self.client.close()

    async def __aexit__(self, *args):
        await self.client.aclose()

    def _get_client(self) -> httpx.AsyncClient:
        if (self.http_username and not self.http_password) or (
            not self.http_username and self.http_password
        ):
            raise ValueError("Both http_username and http_password should be defined")

        auth = None
        if self.http_username:
            auth = httpx.auth.BasicAuth(self.http_username, self.http_password)

        return self._httpx_client_class(
            auth=auth, verify=self.ssl_verify, timeout=self.timeout,
        )

    def __getstate__(self):
        state = self.__dict__.copy()
        state.pop("_objects")
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        objects = importlib.import_module("gitlab.v%s.objects" % self._api_version)
        self._objects = objects

    @property
    def url(self):
        """The user-provided server URL."""
        return self._base_url

    @property
    def api_url(self):
        """The computed API base URL."""
        return self._url

    @property
    def api_version(self):
        """The API version used (4 only)."""
        return self._api_version

    @classmethod
    def from_config(cls, gitlab_id=None, config_files=None):
        """Create a Gitlab connection from configuration files.

        Args:
            gitlab_id (str): ID of the configuration section.
            config_files list[str]: List of paths to configuration files.

        Returns:
            (gitlab.Gitlab): A Gitlab connection.

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
        )

    def auth(self):
        """Performs an authentication using private token.

        The `user` attribute will hold a `gitlab.objects.CurrentUser` object on
        success.
        """
        raise NotImplemented

    def version(self):
        """Returns the version and revision of the gitlab server.

        Note that self.version and self.revision will be set on the gitlab
        object.

        Returns:
            tuple (str, str): The server version and server revision.
                              ('unknown', 'unknwown') if the server doesn't
                              perform as expected.
        """
        raise NotImplemented

    def lint(self, content, **kwargs):
        """Validate a gitlab CI configuration.

        Args:
            content (txt): The .gitlab-ci.yml content
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabVerifyError: If the validation could not be done

        Returns:
            tuple: (True, []) if the file is valid, (False, errors(list))
                otherwise
        """
        raise NotImplemented

    @on_http_error(exc.GitlabMarkdownError)
    def markdown(self, text, gfm=False, project=None, **kwargs):
        """Render an arbitrary Markdown document.

        Args:
            text (str): The markdown text to render
            gfm (bool): Render text using GitLab Flavored Markdown. Default is
                False
            project (str): Full path of a project used a context when `gfm` is
                True
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabMarkdownError: If the server cannot perform the request

        Returns:
            str: The HTML rendering of the markdown text.
        """
        raise NotImplemented

    @on_http_error(exc.GitlabLicenseError)
    def get_license(self, **kwargs):
        """Retrieve information about the current license.

        Args:
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabGetError: If the server cannot perform the request

        Returns:
            dict: The current license information
        """
        return self.http_get("/license", **kwargs)

    @on_http_error(exc.GitlabLicenseError)
    def set_license(self, license, **kwargs):
        """Add a new license.

        Args:
            license (str): The license string
            **kwargs: Extra options to send to the server (e.g. sudo)

        Raises:
            GitlabAuthenticationError: If authentication is not correct
            GitlabPostError: If the server cannot perform the request

        Returns:
            dict: The new license information
        """
        data = {"license": license}
        return self.http_post("/license", post_data=data, **kwargs)

    def _construct_url(self, id_, obj, parameters, action=None):
        if "next_url" in parameters:
            return parameters["next_url"]
        args = _sanitize(parameters)

        url_attr = "_url"
        if action is not None:
            attr = "_%s_url" % action
            if hasattr(obj, attr):
                url_attr = attr
        obj_url = getattr(obj, url_attr)
        url = obj_url % args

        if id_ is not None:
            return "%s/%s" % (url, str(id_))
        else:
            return url

    def _set_auth_info(self):
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
        if self.oauth_token and self.http_username:
            raise ValueError(
                "Only one of oauth authentication or http "
                "authentication should be defined"
            )

        if self.private_token:
            self.headers.pop("Authorization", None)
            self.headers["PRIVATE-TOKEN"] = self.private_token
            self.headers.pop("JOB-TOKEN", None)

        if self.oauth_token:
            self.headers["Authorization"] = "Bearer %s" % self.oauth_token
            self.headers.pop("PRIVATE-TOKEN", None)
            self.headers.pop("JOB-TOKEN", None)

        if self.job_token:
            self.headers.pop("Authorization", None)
            self.headers.pop("PRIVATE-TOKEN", None)
            self.headers["JOB-TOKEN"] = self.job_token

    def enable_debug(self):
        import logging

        from http.client import HTTPConnection  # noqa

        HTTPConnection.debuglevel = 1
        logging.basicConfig()
        logging.getLogger().setLevel(logging.DEBUG)
        requests_log = logging.getLogger("httpx")
        requests_log.setLevel(logging.DEBUG)
        requests_log.propagate = True

    def _create_headers(self, content_type=None):
        request_headers = self.headers.copy()
        if content_type is not None:
            request_headers["Content-type"] = content_type
        return request_headers

    def _build_url(self, path):
        """Returns the full url from path.

        If path is already a url, return it unchanged. If it's a path, append
        it to the stored url.

        Returns:
            str: The full URL
        """
        if path.startswith("http://") or path.startswith("https://"):
            return path
        else:
            return "%s%s" % (self._url, path)

    def _check_redirects(self, result):
        # Check the requests history to detect http to https redirections.
        # If the initial verb is POST, the next request will use a GET request,
        # leading to an unwanted behaviour.
        # If the initial verb is PUT, the data will not be send with the next
        # request.
        # If we detect a redirection to https with a POST or a PUT request, we
        # raise an exception with a useful error message.
        if result.history and self._base_url.startswith("http:"):
            for item in result.history:
                if item.status_code not in (301, 302):
                    continue
                # GET methods can be redirected without issue
                if item.request.method == "GET":
                    continue
                # Did we end-up with an https:// URL?
                location = item.headers.get("Location", None)
                if location and location.startswith("https://"):
                    raise RedirectError(REDIRECT_MSG)

    def http_request(
        self,
        verb,
        path,
        query_data=None,
        post_data=None,
        streamed=False,
        files=None,
        **kwargs
    ):
        """Make an HTTP request to the Gitlab server.

        Args:
            verb (str): The HTTP method to call ('get', 'post', 'put',
                        'delete')
            path (str): Path or full URL to query ('/projects' or
                        'http://whatever/v4/api/projecs')
            query_data (dict): Data to send as query parameters
            post_data (dict): Data to send in the body (will be converted to
                              json)
            streamed (bool): Whether the data should be streamed
            files (dict): The files to send to the server
            **kwargs: Extra options to send to the server (e.g. sudo)

        Returns:
            A requests result object.

        Raises:
            GitlabHttpError: When the return code is not 2xx
        """
        raise NotImplemented

    def http_get(self, path, query_data=None, streamed=False, raw=False, **kwargs):
        """Make a GET request to the Gitlab server.

        Args:
            path (str): Path or full URL to query ('/projects' or
                        'http://whatever/v4/api/projecs')
            query_data (dict): Data to send as query parameters
            streamed (bool): Whether the data should be streamed
            raw (bool): If True do not try to parse the output as json
            **kwargs: Extra options to send to the server (e.g. sudo)

        Returns:
            A requests result object is streamed is True or the content type is
            not json.
            The parsed json data otherwise.

        Raises:
            GitlabHttpError: When the return code is not 2xx
            GitlabParsingError: If the json data could not be parsed
        """
        raise NotImplemented

    def http_list(self, path, query_data=None, as_list=None, **kwargs):
        """Make a GET request to the Gitlab server for list-oriented queries.

        Args:
            path (str): Path or full URL to query ('/projects' or
                        'http://whatever/v4/api/projecs')
            query_data (dict): Data to send as query parameters
            **kwargs: Extra options to send to the server (e.g. sudo, page,
                      per_page)

        Returns:
            list: A list of the objects returned by the server. If `as_list` is
            False and no pagination-related arguments (`page`, `per_page`,
            `all`) are defined then a GitlabList object (generator) is returned
            instead. This object will make API calls when needed to fetch the
            next items from the server.

        Raises:
            GitlabHttpError: When the return code is not 2xx
            GitlabParsingError: If the json data could not be parsed
        """
        raise NotImplemented

    def http_post(self, path, query_data=None, post_data=None, files=None, **kwargs):
        """Make a POST request to the Gitlab server.

        Args:
            path (str): Path or full URL to query ('/projects' or
                        'http://whatever/v4/api/projecs')
            query_data (dict): Data to send as query parameters
            post_data (dict): Data to send in the body (will be converted to
                              json)
            files (dict): The files to send to the server
            **kwargs: Extra options to send to the server (e.g. sudo)

        Returns:
            The parsed json returned by the server if json is return, else the
            raw content

        Raises:
            GitlabHttpError: When the return code is not 2xx
            GitlabParsingError: If the json data could not be parsed
        """
        raise NotImplemented

    def http_put(self, path, query_data=None, post_data=None, files=None, **kwargs):
        """Make a PUT request to the Gitlab server.

        Args:
            path (str): Path or full URL to query ('/projects' or
                        'http://whatever/v4/api/projecs')
            query_data (dict): Data to send as query parameters
            post_data (dict): Data to send in the body (will be converted to
                              json)
            files (dict): The files to send to the server
            **kwargs: Extra options to send to the server (e.g. sudo)

        Returns:
            The parsed json returned by the server.

        Raises:
            GitlabHttpError: When the return code is not 2xx
            GitlabParsingError: If the json data could not be parsed
        """
        raise NotImplemented

    def http_delete(self, path, **kwargs):
        """Make a PUT request to the Gitlab server.

        Args:
            path (str): Path or full URL to query ('/projects' or
                        'http://whatever/v4/api/projecs')
            **kwargs: Extra options to send to the server (e.g. sudo)

        Returns:
            The requests object.

        Raises:
            GitlabHttpError: When the return code is not 2xx
        """
        return self.http_request("delete", path, **kwargs)

    @on_http_error(exc.GitlabSearchError)
    def search(self, scope, search, **kwargs):
        """Search GitLab resources matching the provided string.'

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
        return self.http_list("/search", query_data=data, **kwargs)


class Gitlab(BaseGitlab):
    _httpx_client_class = httpx.Client

    def auth(self):
        self.user = self._objects.CurrentUserManager(self).get()

    def version(self):
        if self._server_version is None:
            try:
                data = self.http_get("/version")
                self._server_version = data["version"]
                self._server_revision = data["revision"]
            except Exception:
                self._server_version = self._server_revision = "unknown"

        return self._server_version, self._server_revision

    @on_http_error(exc.GitlabVerifyError)
    def lint(self, content, **kwargs):
        post_data = {"content": content}
        data = self.http_post("/ci/lint", post_data=post_data, **kwargs)
        return (data["status"] == "valid", data["errors"])

    @on_http_error(exc.GitlabMarkdownError)
    def markdown(self, text, gfm=False, project=None, **kwargs):
        post_data = {"text": text, "gfm": gfm}
        if project is not None:
            post_data["project"] = project
        data = self.http_post("/markdown", post_data=post_data, **kwargs)
        return data["html"]

    def http_request(
        self,
        verb,
        path,
        query_data=None,
        post_data=None,
        streamed=False,
        files=None,
        **kwargs
    ):
        query_data = query_data or {}
        url = self._build_url(path)

        params = {}
        utils.copy_dict(params, query_data)

        # Deal with kwargs: by default a user uses kwargs to send data to the
        # gitlab server, but this generates problems (python keyword conflicts
        # and python-gitlab/gitlab conflicts).
        # So we provide a `query_parameters` key: if it's there we use its dict
        # value as arguments for the gitlab server, and ignore the other
        # arguments, except pagination ones (per_page and page)
        if "query_parameters" in kwargs:
            utils.copy_dict(params, kwargs["query_parameters"])
            for arg in ("per_page", "page"):
                if arg in kwargs:
                    params[arg] = kwargs[arg]
        else:
            utils.copy_dict(params, kwargs)

        opts = {"headers": self._create_headers("application/json")}

        # If timeout was passed into kwargs, allow it to override the default
        timeout = kwargs.get("timeout")

        # We need to deal with json vs. data when uploading files
        if files:
            data = post_data
            json = None
            del opts["headers"]["Content-type"]
        else:
            json = post_data
            data = None

        req = httpx.Request(
            verb, url, json=json, data=data, params=params, files=files, **opts
        )

        # obey the rate limit by default
        obey_rate_limit = kwargs.get("obey_rate_limit", True)
        # do not retry transient errors by default
        retry_transient_errors = kwargs.get("retry_transient_errors", False)

        # set max_retries to 10 by default, disable by setting it to -1
        max_retries = kwargs.get("max_retries", 10)
        cur_retries = 0

        while True:
            result = self.client.send(req, stream=streamed, timeout=timeout)

            self._check_redirects(result)

            if 200 <= result.status_code < 300:
                return result

            if (429 == result.status_code and obey_rate_limit) or (
                result.status_code in [500, 502, 503, 504] and retry_transient_errors
            ):
                if max_retries == -1 or cur_retries < max_retries:
                    wait_time = 2 ** cur_retries * 0.1
                    if "Retry-After" in result.headers:
                        wait_time = int(result.headers["Retry-After"])
                    cur_retries += 1
                    time.sleep(wait_time)
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
                raise GitlabAuthenticationError(
                    response_code=result.status_code,
                    error_message=error_message,
                    response_body=result.content,
                )

            raise GitlabHttpError(
                response_code=result.status_code,
                error_message=error_message,
                response_body=result.content,
            )

    def http_get(self, path, query_data=None, streamed=False, raw=False, **kwargs):
        query_data = query_data or {}
        result = self.http_request(
            "get", path, query_data=query_data, streamed=streamed, **kwargs
        )

        if (
            result.headers["Content-Type"] == "application/json"
            and not streamed
            and not raw
        ):
            try:
                return result.json()
            except Exception:
                raise GitlabParsingError(
                    error_message="Failed to parse the server message"
                )
        else:
            return result

    def http_list(self, path, query_data=None, as_list=None, **kwargs):
        query_data = query_data or {}

        # In case we want to change the default behavior at some point
        as_list = True if as_list is None else as_list

        get_all = kwargs.pop("all", False)
        url = self._build_url(path)

        if get_all is True and as_list is True:
            gitlab_list = GitlabList.create(self, url, query_data, **kwargs)
            return list(gitlab_list)

        if "page" in kwargs or as_list is True:
            # pagination requested, we return a list
            gitlab_list = GitlabList.create(
                self, url, query_data, get_next=False, **kwargs
            )
            return list(gitlab_list)

        # No pagination, generator requested
        return GitlabList.create(self, url, query_data, **kwargs)

    def http_post(self, path, query_data=None, post_data=None, files=None, **kwargs):
        query_data = query_data or {}
        post_data = post_data or {}

        result = self.http_request(
            "post",
            path,
            query_data=query_data,
            post_data=post_data,
            files=files,
            **kwargs
        )
        try:
            if result.headers.get("Content-Type", None) == "application/json":
                return result.json()
        except Exception:
            raise GitlabParsingError(error_message="Failed to parse the server message")
        return result

    def http_put(self, path, query_data=None, post_data=None, files=None, **kwargs):
        query_data = query_data or {}
        post_data = post_data or {}

        result = self.http_request(
            "put",
            path,
            query_data=query_data,
            post_data=post_data,
            files=files,
            **kwargs
        )
        try:
            return result.json()
        except Exception:
            raise GitlabParsingError(error_message="Failed to parse the server message")


class AsyncGitlab(BaseGitlab):
    _httpx_client_class = httpx.AsyncClient

    async def auth(self):
        self.user = await self._objects.CurrentUserManager(self).get()

    async def version(self):
        if self._server_version is None:
            try:
                data = await self.http_get("/version")
                self._server_version = data["version"]
                self._server_revision = data["revision"]
            except Exception:
                self._server_version = self._server_revision = "unknown"

        return self._server_version, self._server_revision

    @on_http_error(exc.GitlabVerifyError)
    async def lint(self, content, **kwargs):
        post_data = {"content": content}
        data = await self.http_post("/ci/lint", post_data=post_data, **kwargs)
        return (data["status"] == "valid", data["errors"])

    @on_http_error(exc.GitlabMarkdownError)
    async def markdown(self, text, gfm=False, project=None, **kwargs):
        post_data = {"text": text, "gfm": gfm}
        if project is not None:
            post_data["project"] = project
        data = await self.http_post("/markdown", post_data=post_data, **kwargs)
        return data["html"]

    async def http_request(
        self,
        verb,
        path,
        query_data=None,
        post_data=None,
        streamed=False,
        files=None,
        **kwargs
    ):
        query_data = query_data or {}
        url = self._build_url(path)

        params = {}
        utils.copy_dict(params, query_data)

        # Deal with kwargs: by default a user uses kwargs to send data to the
        # gitlab server, but this generates problems (python keyword conflicts
        # and python-gitlab/gitlab conflicts).
        # So we provide a `query_parameters` key: if it's there we use its dict
        # value as arguments for the gitlab server, and ignore the other
        # arguments, except pagination ones (per_page and page)
        if "query_parameters" in kwargs:
            utils.copy_dict(params, kwargs["query_parameters"])
            for arg in ("per_page", "page"):
                if arg in kwargs:
                    params[arg] = kwargs[arg]
        else:
            utils.copy_dict(params, kwargs)

        opts = {"headers": self._create_headers("application/json")}

        # If timeout was passed into kwargs, allow it to override the default
        timeout = kwargs.get("timeout")

        # We need to deal with json vs. data when uploading files
        if files:
            data = post_data
            json = None
            del opts["headers"]["Content-type"]
        else:
            json = post_data
            data = None

        req = httpx.Request(
            verb, url, json=json, data=data, params=params, files=files, **opts
        )

        # obey the rate limit by default
        obey_rate_limit = kwargs.get("obey_rate_limit", True)
        # do not retry transient errors by default
        retry_transient_errors = kwargs.get("retry_transient_errors", False)

        # set max_retries to 10 by default, disable by setting it to -1
        max_retries = kwargs.get("max_retries", 10)
        cur_retries = 0

        while True:
            result = await self.client.send(req, stream=streamed, timeout=timeout)

            self._check_redirects(result)

            if 200 <= result.status_code < 300:
                return result

            if (429 == result.status_code and obey_rate_limit) or (
                result.status_code in [500, 502, 503, 504] and retry_transient_errors
            ):
                if max_retries == -1 or cur_retries < max_retries:
                    wait_time = 2 ** cur_retries * 0.1
                    if "Retry-After" in result.headers:
                        wait_time = int(result.headers["Retry-After"])
                    cur_retries += 1
                    await asyncio.sleep(wait_time)
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
                raise GitlabAuthenticationError(
                    response_code=result.status_code,
                    error_message=error_message,
                    response_body=result.content,
                )

            raise GitlabHttpError(
                response_code=result.status_code,
                error_message=error_message,
                response_body=result.content,
            )

    async def http_get(
        self, path, query_data=None, streamed=False, raw=False, **kwargs
    ):
        query_data = query_data or {}
        result = await self.http_request(
            "get", path, query_data=query_data, streamed=streamed, **kwargs
        )

        if (
            result.headers["Content-Type"] == "application/json"
            and not streamed
            and not raw
        ):
            try:
                return result.json()
            except Exception:
                raise GitlabParsingError(
                    error_message="Failed to parse the server message"
                )
        else:
            return result

    async def http_list(self, path, query_data=None, as_list=None, **kwargs):
        query_data = query_data or {}

        # In case we want to change the default behavior at some point
        as_list = True if as_list is None else as_list

        get_all = kwargs.pop("all", False)
        url = self._build_url(path)

        if get_all is True and as_list is True:
            gitlab_list = await GitlabList.acreate(self, url, query_data, **kwargs)
            return await gitlab_list.as_list()

        if "page" in kwargs or as_list is True:
            # pagination requested, we return a list
            gitlab_list = await GitlabList.acreate(
                self, url, query_data, get_next=False, **kwargs
            )
            return await gitlab_list.as_list()

        # No pagination, generator requested
        return await GitlabList.acreate(self, url, query_data, **kwargs)

    async def http_post(
        self, path, query_data=None, post_data=None, files=None, **kwargs
    ):
        query_data = query_data or {}
        post_data = post_data or {}

        result = await self.http_request(
            "post",
            path,
            query_data=query_data,
            post_data=post_data,
            files=files,
            **kwargs
        )
        try:
            if result.headers.get("Content-Type", None) == "application/json":
                return result.json()
        except Exception:
            raise GitlabParsingError(error_message="Failed to parse the server message")
        return result

    async def http_put(
        self, path, query_data=None, post_data=None, files=None, **kwargs
    ):
        query_data = query_data or {}
        post_data = post_data or {}

        result = await self.http_request(
            "put",
            path,
            query_data=query_data,
            post_data=post_data,
            files=files,
            **kwargs
        )
        try:
            return result.json()
        except Exception:
            raise GitlabParsingError(error_message="Failed to parse the server message")

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

from __future__ import print_function
from __future__ import absolute_import
import importlib
import time
import warnings

import requests
import six

import gitlab.config
from gitlab.const import *  # noqa
from gitlab.exceptions import *  # noqa
from gitlab import utils  # noqa

__title__ = "python-gitlab"
__version__ = "1.15.0"
__author__ = "Gauvain Pocentek"
__email__ = "gauvainpocentek@gmail.com"
__license__ = "LGPL3"
__copyright__ = "Copyright 2013-2019 Gauvain Pocentek"

warnings.filterwarnings("default", category=DeprecationWarning, module="^gitlab")

REDIRECT_MSG = (
    "python-gitlab detected an http to https redirection. You "
    "must update your GitLab URL to use https:// to avoid issues."
)


def _sanitize(value):
    if isinstance(value, dict):
        return dict((k, _sanitize(v)) for k, v in six.iteritems(value))
    if isinstance(value, six.string_types):
        return value.replace("/", "%2F")
    return value


class Gitlab(object):
    """Represents a GitLab server connection.

    Args:
        url (str): The URL of the GitLab server.
        private_token (str): The user private token
        oauth_token (str): An oauth token
        job_token (str): A CI job token
        email (str): The user email or login.
        password (str): The user password (associated with email).
        ssl_verify (bool|str): Whether SSL certificates should be validated. If
            the value is a string, it is the path to a CA file used for
            certificate validation.
        timeout (float): Timeout to use for requests to the GitLab server.
        http_username (str): Username for HTTP authentication
        http_password (str): Password for HTTP authentication
        api_version (str): Gitlab API version to use (support for 4 only)
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
        session=None,
        per_page=None,
    ):

        self._api_version = str(api_version)
        self._server_version = self._server_revision = None
        self._base_url = url
        self._url = "%s/api/v%s" % (url, api_version)
        #: Timeout to use for requests to gitlab server
        self.timeout = timeout
        #: Headers that will be used in request to GitLab
        self.headers = {"User-Agent": "%s/%s" % (__title__, __version__)}

        #: Whether SSL certificates should be validated
        self.ssl_verify = ssl_verify

        self.private_token = private_token
        self.http_username = http_username
        self.http_password = http_password
        self.oauth_token = oauth_token
        self.job_token = job_token
        self._set_auth_info()

        #: Create a session object for requests
        self.session = session or requests.Session()

        self.per_page = per_page

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

    def __exit__(self, *args):
        self.session.close()

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
        )

    def auth(self):
        """Performs an authentication.

        Uses either the private token, or the email/password pair.

        The `user` attribute will hold a `gitlab.objects.CurrentUser` object on
        success.
        """
        self.user = self._objects.CurrentUserManager(self).get()

    def version(self):
        """Returns the version and revision of the gitlab server.

        Note that self.version and self.revision will be set on the gitlab
        object.

        Returns:
            tuple (str, str): The server version and server revision.
                              ('unknown', 'unknwown') if the server doesn't
                              perform as expected.
        """
        if self._server_version is None:
            try:
                data = self.http_get("/version")
                self._server_version = data["version"]
                self._server_revision = data["revision"]
            except Exception:
                self._server_version = self._server_revision = "unknown"

        return self._server_version, self._server_revision

    @on_http_error(GitlabVerifyError)
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
        post_data = {"content": content}
        data = self.http_post("/ci/lint", post_data=post_data, **kwargs)
        return (data["status"] == "valid", data["errors"])

    @on_http_error(GitlabMarkdownError)
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
        post_data = {"text": text, "gfm": gfm}
        if project is not None:
            post_data["project"] = project
        data = self.http_post("/markdown", post_data=post_data, **kwargs)
        return data["html"]

    @on_http_error(GitlabLicenseError)
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

    @on_http_error(GitlabLicenseError)
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
        if (self.http_username and not self.http_password) or (
            not self.http_username and self.http_password
        ):
            raise ValueError(
                "Both http_username and http_password should " "be defined"
            )
        if self.oauth_token and self.http_username:
            raise ValueError(
                "Only one of oauth authentication or http "
                "authentication should be defined"
            )

        self._http_auth = None
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

        if self.http_username:
            self._http_auth = requests.auth.HTTPBasicAuth(
                self.http_username, self.http_password
            )

    def enable_debug(self):
        import logging

        try:
            from http.client import HTTPConnection  # noqa
        except ImportError:
            from httplib import HTTPConnection  # noqa

        HTTPConnection.debuglevel = 1
        logging.basicConfig()
        logging.getLogger().setLevel(logging.DEBUG)
        requests_log = logging.getLogger("requests.packages.urllib3")
        requests_log.setLevel(logging.DEBUG)
        requests_log.propagate = True

    def _create_headers(self, content_type=None):
        request_headers = self.headers.copy()
        if content_type is not None:
            request_headers["Content-type"] = content_type
        return request_headers

    def _get_session_opts(self, content_type):
        return {
            "headers": self._create_headers(content_type),
            "auth": self._http_auth,
            "timeout": self.timeout,
            "verify": self.ssl_verify,
        }

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

        opts = self._get_session_opts(content_type="application/json")

        verify = opts.pop("verify")
        timeout = opts.pop("timeout")
        # If timeout was passed into kwargs, allow it to override the default
        timeout = kwargs.get("timeout", timeout)

        # We need to deal with json vs. data when uploading files
        if files:
            data = post_data
            json = None
            del opts["headers"]["Content-type"]
        else:
            json = post_data
            data = None

        # Requests assumes that `.` should not be encoded as %2E and will make
        # changes to urls using this encoding. Using a prepped request we can
        # get the desired behavior.
        # The Requests behavior is right but it seems that web servers don't
        # always agree with this decision (this is the case with a default
        # gitlab installation)
        req = requests.Request(
            verb, url, json=json, data=data, params=params, files=files, **opts
        )
        prepped = self.session.prepare_request(req)
        prepped.url = utils.sanitized_url(prepped.url)
        settings = self.session.merge_environment_settings(
            prepped.url, {}, streamed, verify, None
        )

        # obey the rate limit by default
        obey_rate_limit = kwargs.get("obey_rate_limit", True)
        # do not retry transient errors by default
        retry_transient_errors = kwargs.get("retry_transient_errors", False)

        # set max_retries to 10 by default, disable by setting it to -1
        max_retries = kwargs.get("max_retries", 10)
        cur_retries = 0

        while True:
            result = self.session.send(prepped, timeout=timeout, **settings)

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
        query_data = query_data or {}

        # In case we want to change the default behavior at some point
        as_list = True if as_list is None else as_list

        get_all = kwargs.pop("all", False)
        url = self._build_url(path)

        if get_all is True and as_list is True:
            return list(GitlabList(self, url, query_data, **kwargs))

        if "page" in kwargs or as_list is True:
            # pagination requested, we return a list
            return list(GitlabList(self, url, query_data, get_next=False, **kwargs))

        # No pagination, generator requested
        return GitlabList(self, url, query_data, **kwargs)

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

    @on_http_error(GitlabSearchError)
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


class GitlabList(object):
    """Generator representing a list of remote objects.

    The object handles the links returned by a query to the API, and will call
    the API again when needed.
    """

    def __init__(self, gl, url, query_data, get_next=True, **kwargs):
        self._gl = gl
        self._query(url, query_data, **kwargs)
        self._get_next = get_next

    def _query(self, url, query_data=None, **kwargs):
        query_data = query_data or {}
        result = self._gl.http_request("get", url, query_data=query_data, **kwargs)
        try:
            self._next_url = result.links["next"]["url"]
        except KeyError:
            self._next_url = None
        self._current_page = result.headers.get("X-Page")
        self._prev_page = result.headers.get("X-Prev-Page")
        self._next_page = result.headers.get("X-Next-Page")
        self._per_page = result.headers.get("X-Per-Page")
        self._total_pages = result.headers.get("X-Total-Pages")
        self._total = result.headers.get("X-Total")

        try:
            self._data = result.json()
        except Exception:
            raise GitlabParsingError(error_message="Failed to parse the server message")

        self._current = 0

    @property
    def current_page(self):
        """The current page number."""
        return int(self._current_page)

    @property
    def prev_page(self):
        """The next page number.

        If None, the current page is the last.
        """
        return int(self._prev_page) if self._prev_page else None

    @property
    def next_page(self):
        """The next page number.

        If None, the current page is the last.
        """
        return int(self._next_page) if self._next_page else None

    @property
    def per_page(self):
        """The number of items per page."""
        return int(self._per_page)

    @property
    def total_pages(self):
        """The total number of pages."""
        return int(self._total_pages)

    @property
    def total(self):
        """The total number of items."""
        return int(self._total)

    def __iter__(self):
        return self

    def __len__(self):
        return int(self._total)

    def __next__(self):
        return self.next()

    def next(self):
        try:
            item = self._data[self._current]
            self._current += 1
            return item
        except IndexError:
            pass

        if self._next_url and self._get_next is True:
            self._query(self._next_url)
            return self.next()

        raise StopIteration

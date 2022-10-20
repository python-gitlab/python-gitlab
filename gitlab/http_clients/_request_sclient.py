from __future__ import annotations

import time
from typing import Any, Dict, Optional, Tuple, TYPE_CHECKING, Union
from urllib import parse

import requests
import requests.utils
from requests_toolbelt.multipart.encoder import MultipartEncoder  # type: ignore

import gitlab
from gitlab import utils

RETRYABLE_TRANSIENT_ERROR_CODES = [500, 502, 503, 504] + list(range(520, 531))


class _Requests_Client:
    def __init__(
        self,
        url: Optional[str] = None,
        session: Optional[requests.Session] = None,
        retry_transient_errors: bool = False,
        ssl_verify: Union[bool, str] = True,
        timeout: Optional[float] = None,
        http_username: Optional[str] = None,
        http_password: Optional[str] = None,
        job_token: Optional[str] = None,
        user_agent: str = gitlab.const.USER_AGENT,
        oauth_token: Optional[str] = None,
        private_token: Optional[str] = None,
    ) -> None:
        self._session = session or requests.Session()
        self._base_url = self._get_base_url(url)
        self._url = f"{self._base_url}/api/v4"
        self.retry_transient_errors = retry_transient_errors
        self.ssl_verify = ssl_verify
        self.timeout = timeout
        self.http_username = http_username
        self.http_password = http_password
        self.job_token = job_token
        self.headers = {"User-Agent": user_agent}
        self.oauth_token = oauth_token
        self.private_token = private_token
        self._set_auth_info()

    @property
    def get_session(self: _Requests_Client) -> requests.Session:
        return self._session

    @property
    def get_headers(self) -> Dict[str, str]:
        return self.headers

    def __enter__(self: _Requests_Client) -> _Requests_Client:
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()

    def close(self: _Requests_Client) -> None:
        self._session.close()

    def http_head(
        self, path: str, query_data: Optional[Dict[str, Any]] = None, **kwargs: Any
    ) -> Any:
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

    def http_post(
        self,
        path: str,
        query_data: Optional[Dict[str, Any]] = None,
        post_data: Optional[Dict[str, Any]] = None,
        raw: bool = False,
        files: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Union[Dict[str, Any], Any]:
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
        try:
            if result.headers.get("Content-Type", None) == "application/json":
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
        post_data: Optional[Union[Dict[str, Any], bytes]] = None,
        raw: bool = False,
        files: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Union[Dict[str, Any], Any]:
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
        try:
            json_result = result.json()
            if TYPE_CHECKING:
                assert isinstance(json_result, dict)
            return json_result
        except Exception as e:
            raise gitlab.exceptions.GitlabParsingError(
                error_message="Failed to parse the server message"
            ) from e

    def http_delete(self, path: str, **kwargs: Any) -> Any:
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

    def http_request(
        self,
        verb: str,
        path: str,
        query_data: Optional[Dict[str, Any]] = None,
        post_data: Optional[Union[Dict[str, Any], bytes]] = None,
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
        json, data, content_type = self._prepare_send_data(files, post_data, raw)
        opts["headers"]["Content-type"] = content_type

        cur_retries = 0
        while True:
            try:
                result = self._session.request(
                    method=verb,
                    url=url,
                    json=json,
                    data=data,
                    params=params,
                    timeout=timeout,
                    verify=verify,
                    stream=streamed,
                    **opts,
                )
            except (requests.ConnectionError, requests.exceptions.ChunkedEncodingError):
                if retry_transient_errors and (
                    max_retries == -1 or cur_retries < max_retries
                ):
                    wait_time = 2**cur_retries * 0.1
                    cur_retries += 1
                    time.sleep(wait_time)
                    continue

                raise

            self._check_redirects(result)

            if 200 <= result.status_code < 300:
                return result

            if (429 == result.status_code and obey_rate_limit) or (
                result.status_code in RETRYABLE_TRANSIENT_ERROR_CODES
                and retry_transient_errors
            ):
                # Response headers documentation:
                # https://docs.gitlab.com/ee/user/admin_area/settings/user_and_ip_rate_limits.html#response-headers
                if max_retries == -1 or cur_retries < max_retries:
                    wait_time = 2**cur_retries * 0.1
                    if "Retry-After" in result.headers:
                        wait_time = int(result.headers["Retry-After"])
                    elif "RateLimit-Reset" in result.headers:
                        wait_time = int(result.headers["RateLimit-Reset"]) - time.time()
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

        if (
            result.headers["Content-Type"] == "application/json"
            and not streamed
            and not raw
        ):
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

    @staticmethod
    def _get_base_url(url: Optional[str] = None) -> str:
        """Return the base URL with the trailing slash stripped.
        If the URL is a Falsy value, return the default URL.
        Returns:
            The base URL
        """
        if not url:
            return gitlab.const.DEFAULT_URL

        return url.rstrip("/")

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
            # GET methods can be redirected without issue
            if item.request.method == "GET":
                continue
            target = item.headers.get("location")
            raise gitlab.exceptions.RedirectError(
                gitlab.const.REDIRECT_MSG.format(
                    status_code=item.status_code,
                    reason=item.reason,
                    source=item.url,
                    target=target,
                )
            )

    @staticmethod
    def _prepare_send_data(
        files: Optional[Dict[str, Any]] = None,
        post_data: Optional[Union[Dict[str, Any], bytes]] = None,
        raw: bool = False,
    ) -> Tuple[
        Optional[Union[Dict[str, Any], bytes]],
        Optional[Union[Dict[str, Any], MultipartEncoder]],
        str,
    ]:
        if files:
            if post_data is None:
                post_data = {}
            else:
                # booleans does not exists for data (neither for MultipartEncoder):
                # cast to string int to avoid: 'bool' object has no attribute 'encode'
                if TYPE_CHECKING:
                    assert isinstance(post_data, dict)
                for k, v in post_data.items():
                    if isinstance(v, bool):
                        post_data[k] = str(int(v))
            post_data["file"] = files.get("file")
            post_data["avatar"] = files.get("avatar")

            data = MultipartEncoder(post_data)
            return (None, data, data.content_type)

        if raw and post_data:
            return (None, post_data, "application/octet-stream")

        return (post_data, None, "application/json")

    def _get_session_opts(self) -> Dict[str, Any]:
        return {
            "headers": self.headers.copy(),
            "auth": self._http_auth,
            "timeout": self.timeout,
            "verify": self.ssl_verify,
        }

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
            self.headers["Authorization"] = f"Bearer {self.oauth_token}"
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

    def get_auth_info(self) -> requests.auth.HTTPBasicAuth | None:
        return self._http_auth

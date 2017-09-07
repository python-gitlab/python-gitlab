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
import inspect
import itertools
import json
import re
import warnings

import requests
import six

import gitlab.config
from gitlab.const import *  # noqa
from gitlab.exceptions import *  # noqa
from gitlab.v3.objects import *  # noqa

__title__ = 'python-gitlab'
__version__ = '1.0.0'
__author__ = 'Gauvain Pocentek'
__email__ = 'gauvain@pocentek.net'
__license__ = 'LGPL3'
__copyright__ = 'Copyright 2013-2017 Gauvain Pocentek'

warnings.filterwarnings('default', category=DeprecationWarning,
                        module='^gitlab')


def _sanitize(value):
    if isinstance(value, dict):
        return dict((k, _sanitize(v))
                    for k, v in six.iteritems(value))
    if isinstance(value, six.string_types):
        return value.replace('/', '%2F')
    return value


class Gitlab(object):
    """Represents a GitLab server connection.

    Args:
        url (str): The URL of the GitLab server.
        private_token (str): The user private token
        email (str): The user email or login.
        password (str): The user password (associated with email).
        ssl_verify (bool): Whether SSL certificates should be validated.
        timeout (float): Timeout to use for requests to the GitLab server.
        http_username (str): Username for HTTP authentication
        http_password (str): Password for HTTP authentication
        api_version (str): Gitlab API version to use (3 or 4)
    """

    def __init__(self, url, private_token=None, email=None, password=None,
                 ssl_verify=True, http_username=None, http_password=None,
                 timeout=None, api_version='3', session=None):

        self._api_version = str(api_version)
        self._server_version = self._server_revision = None
        self._url = '%s/api/v%s' % (url, api_version)
        #: Timeout to use for requests to gitlab server
        self.timeout = timeout
        #: Headers that will be used in request to GitLab
        self.headers = {}
        self._set_token(private_token)
        #: The user email
        self.email = email
        #: The user password (associated with email)
        self.password = password
        #: Whether SSL certificates should be validated
        self.ssl_verify = ssl_verify
        self.http_username = http_username
        self.http_password = http_password

        #: Create a session object for requests
        self.session = session or requests.Session()

        objects = importlib.import_module('gitlab.v%s.objects' %
                                          self._api_version)
        self._objects = objects

        self.broadcastmessages = objects.BroadcastMessageManager(self)
        self.deploykeys = objects.DeployKeyManager(self)
        self.gitlabciymls = objects.GitlabciymlManager(self)
        self.gitignores = objects.GitignoreManager(self)
        self.groups = objects.GroupManager(self)
        self.hooks = objects.HookManager(self)
        self.issues = objects.IssueManager(self)
        self.licenses = objects.LicenseManager(self)
        self.namespaces = objects.NamespaceManager(self)
        self.notificationsettings = objects.NotificationSettingsManager(self)
        self.projects = objects.ProjectManager(self)
        self.runners = objects.RunnerManager(self)
        self.settings = objects.ApplicationSettingsManager(self)
        self.sidekiq = objects.SidekiqManager(self)
        self.snippets = objects.SnippetManager(self)
        self.users = objects.UserManager(self)
        self.todos = objects.TodoManager(self)
        if self._api_version == '3':
            self.keys = objects.KeyManager(self)
            self.teams = objects.TeamManager(self)
        else:
            self.dockerfiles = objects.DockerfileManager(self)

        if self._api_version == '3':
            # build the "submanagers"
            for parent_cls in six.itervalues(vars(objects)):
                if (not inspect.isclass(parent_cls)
                    or not issubclass(parent_cls, objects.GitlabObject)
                        or parent_cls == objects.CurrentUser):
                    continue

                if not parent_cls.managers:
                    continue

                for var, cls_name, attrs in parent_cls.managers:
                    prefix = self._cls_to_manager_prefix(parent_cls)
                    var_name = '%s_%s' % (prefix, var)
                    manager = getattr(objects, cls_name)(self)
                    setattr(self, var_name, manager)

    @property
    def api_version(self):
        return self._api_version

    def _cls_to_manager_prefix(self, cls):
        # Manage bad naming decisions
        camel_case = (cls.__name__
                      .replace('NotificationSettings', 'Notificationsettings')
                      .replace('MergeRequest', 'Mergerequest')
                      .replace('AccessRequest', 'Accessrequest'))
        return re.sub(r'(.)([A-Z])', r'\1_\2', camel_case).lower()

    @staticmethod
    def from_config(gitlab_id=None, config_files=None):
        """Create a Gitlab connection from configuration files.

        Args:
            gitlab_id (str): ID of the configuration section.
            config_files list[str]: List of paths to configuration files.

        Returns:
            (gitlab.Gitlab): A Gitlab connection.

        Raises:
            gitlab.config.GitlabDataError: If the configuration is not correct.
        """
        config = gitlab.config.GitlabConfigParser(gitlab_id=gitlab_id,
                                                  config_files=config_files)
        return Gitlab(config.url, private_token=config.token,
                      ssl_verify=config.ssl_verify, timeout=config.timeout,
                      http_username=config.http_username,
                      http_password=config.http_password,
                      api_version=config.api_version)

    def auth(self):
        """Performs an authentication.

        Uses either the private token, or the email/password pair.

        The `user` attribute will hold a `gitlab.objects.CurrentUser` object on
        success.
        """
        if self.private_token:
            self._token_auth()
        else:
            self._credentials_auth()

    def credentials_auth(self):
        """Performs an authentication using email/password."""
        warnings.warn('credentials_auth() is deprecated and will be removed.',
                      DeprecationWarning)
        self._credentials_auth()

    def _credentials_auth(self):
        if not self.email or not self.password:
            raise GitlabAuthenticationError("Missing email/password")

        if self.api_version == '3':
            data = json.dumps({'email': self.email, 'password': self.password})
            r = self._raw_post('/session', data,
                               content_type='application/json')
            raise_error_from_response(r, GitlabAuthenticationError, 201)
            self.user = self._objects.CurrentUser(self, r.json())
        else:
            manager = self._objects.CurrentUserManager()
            self.user = manager.get(self.email, self.password)

        self._set_token(self.user.private_token)

    def token_auth(self):
        """Performs an authentication using the private token."""
        warnings.warn('token_auth() is deprecated and will be removed.',
                      DeprecationWarning)
        self._token_auth()

    def _token_auth(self):
        if self.api_version == '3':
            self.user = self._objects.CurrentUser(self)
        else:
            self.user = self._objects.CurrentUserManager(self).get()

    def version(self):
        """Returns the version and revision of the gitlab server.

        Note that self.version and self.revision will be set on the gitlab
        object.

        Returns:
            tuple (str, str): The server version and server revision, or
                              ('unknown', 'unknwown') if the server doesn't
                              support this API call (gitlab < 8.13.0)
        """
        if self._server_version is None:
            r = self._raw_get('/version')
            try:
                raise_error_from_response(r, GitlabGetError, 200)
                data = r.json()
                self._server_version = data['version']
                self._server_revision = data['revision']
            except GitlabGetError:
                self._server_version = self._server_revision = 'unknown'

        return self._server_version, self._server_revision

    def set_url(self, url):
        """Updates the GitLab URL.

        Args:
            url (str): Base URL of the GitLab server.
        """
        warnings.warn('set_url() is deprecated, create a new Gitlab instance '
                      'if you need an updated URL.',
                      DeprecationWarning)
        self._url = '%s/api/v%s' % (url, self._api_version)

    def _construct_url(self, id_, obj, parameters, action=None):
        if 'next_url' in parameters:
            return parameters['next_url']
        args = _sanitize(parameters)

        url_attr = '_url'
        if action is not None:
            attr = '_%s_url' % action
            if hasattr(obj, attr):
                url_attr = attr
        obj_url = getattr(obj, url_attr)

        # TODO(gpocentek): the following will need an update when we have
        # object with both urlPlural and _ACTION_url attributes
        if id_ is None and obj._urlPlural is not None:
            url = obj._urlPlural % args
        else:
            url = obj_url % args

        if id_ is not None:
            return '%s/%s' % (url, str(id_))
        else:
            return url

    def set_token(self, token):
        """Sets the private token for authentication.

        Args:
            token (str): The private token.
        """
        warnings.warn('set_token() is deprecated, use the private_token '
                      'argument of the Gitlab constructor.',
                      DeprecationWarning)
        self._set_token(token)

    def _set_token(self, token):
        self.private_token = token if token else None
        if token:
            self.headers["PRIVATE-TOKEN"] = token
        elif "PRIVATE-TOKEN" in self.headers:
            del self.headers["PRIVATE-TOKEN"]

    def set_credentials(self, email, password):
        """Sets the email/login and password for authentication.

        Args:
            email (str): The user email or login.
            password (str): The user password.
        """
        warnings.warn('set_credentials() is deprecated, use the email and '
                      'password arguments of the Gitlab constructor.',
                      DeprecationWarning)
        self.email = email
        self.password = password

    def enable_debug(self):
        import logging
        try:
            from http.client import HTTPConnection
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
            request_headers['Content-type'] = content_type
        return request_headers

    def _create_auth(self):
        if self.http_username and self.http_password:
            return requests.auth.HTTPBasicAuth(self.http_username,
                                               self.http_password)
        return None

    def _get_session_opts(self, content_type):
        return {
            'headers': self._create_headers(content_type),
            'auth': self._create_auth(),
            'timeout': self.timeout,
            'verify': self.ssl_verify
        }

    def _raw_get(self, path_, content_type=None, streamed=False, **kwargs):
        if path_.startswith('http://') or path_.startswith('https://'):
            url = path_
        else:
            url = '%s%s' % (self._url, path_)

        opts = self._get_session_opts(content_type)
        try:
            return self.session.get(url, params=kwargs, stream=streamed,
                                    **opts)
        except Exception as e:
            raise GitlabConnectionError(
                "Can't connect to GitLab server (%s)" % e)

    def _raw_list(self, path_, cls, **kwargs):
        params = kwargs.copy()

        catch_recursion_limit = kwargs.get('safe_all', False)
        get_all_results = (kwargs.get('all', False) is True
                           or catch_recursion_limit)

        # Remove these keys to avoid breaking the listing (urls will get too
        # long otherwise)
        for key in ['all', 'next_url', 'safe_all']:
            if key in params:
                del params[key]

        r = self._raw_get(path_, **params)
        raise_error_from_response(r, GitlabListError)

        # These attributes are not needed in the object
        for key in ['page', 'per_page', 'sudo']:
            if key in params:
                del params[key]

        # Add _from_api manually, because we are not creating objects
        # through normal path_
        params['_from_api'] = True

        results = [cls(self, item, **params) for item in r.json()
                   if item is not None]
        try:
            if ('next' in r.links and 'url' in r.links['next']
                    and get_all_results):
                args = kwargs.copy()
                args['next_url'] = r.links['next']['url']
                results.extend(self.list(cls, **args))
        except Exception as e:
            # Catch the recursion limit exception if the 'safe_all'
            # kwarg was provided
            if not (catch_recursion_limit and
                    "maximum recursion depth exceeded" in str(e)):
                raise e

        return results

    def _raw_post(self, path_, data=None, content_type=None, **kwargs):
        url = '%s%s' % (self._url, path_)
        opts = self._get_session_opts(content_type)
        try:
            return self.session.post(url, params=kwargs, data=data, **opts)
        except Exception as e:
            raise GitlabConnectionError(
                "Can't connect to GitLab server (%s)" % e)

    def _raw_put(self, path_, data=None, content_type=None, **kwargs):
        url = '%s%s' % (self._url, path_)
        opts = self._get_session_opts(content_type)
        try:
            return self.session.put(url, data=data, params=kwargs, **opts)
        except Exception as e:
            raise GitlabConnectionError(
                "Can't connect to GitLab server (%s)" % e)

    def _raw_delete(self, path_, content_type=None, **kwargs):
        url = '%s%s' % (self._url, path_)
        opts = self._get_session_opts(content_type)
        try:
            return self.session.delete(url, params=kwargs, **opts)
        except Exception as e:
            raise GitlabConnectionError(
                "Can't connect to GitLab server (%s)" % e)

    def list(self, obj_class, **kwargs):
        """Request the listing of GitLab resources.

        Args:
            obj_class (object): The class of resource to request.
            **kwargs: Additional arguments to send to GitLab.

        Returns:
            list(obj_class): A list of objects of class `obj_class`.

        Raises:
            GitlabConnectionError: If the server cannot be reached.
            GitlabListError: If the server fails to perform the request.
        """
        missing = []
        for k in itertools.chain(obj_class.requiredUrlAttrs,
                                 obj_class.requiredListAttrs):
            if k not in kwargs:
                missing.append(k)
        if missing:
            raise GitlabListError('Missing attribute(s): %s' %
                                  ", ".join(missing))

        url = self._construct_url(id_=None, obj=obj_class, parameters=kwargs)

        return self._raw_list(url, obj_class, **kwargs)

    def get(self, obj_class, id=None, **kwargs):
        """Request a GitLab resources.

        Args:
            obj_class (object): The class of resource to request.
            id: The object ID.
            **kwargs: Additional arguments to send to GitLab.

        Returns:
            obj_class: An object of class `obj_class`.

        Raises:
            GitlabConnectionError: If the server cannot be reached.
            GitlabGetError: If the server fails to perform the request.
        """
        missing = []
        for k in itertools.chain(obj_class.requiredUrlAttrs,
                                 obj_class.requiredGetAttrs):
            if k not in kwargs:
                missing.append(k)
        if missing:
            raise GitlabGetError('Missing attribute(s): %s' %
                                 ", ".join(missing))

        url = self._construct_url(id_=_sanitize(id), obj=obj_class,
                                  parameters=kwargs)

        r = self._raw_get(url, **kwargs)
        raise_error_from_response(r, GitlabGetError)
        return r.json()

    def delete(self, obj, id=None, **kwargs):
        """Delete an object on the GitLab server.

        Args:
            obj (object or id): The object, or the class of the object to
                delete. If it is the class, the id of the object must be
                specified as the `id` arguments.
            id: ID of the object to remove. Required if `obj` is a class.
            **kwargs: Additional arguments to send to GitLab.

        Returns:
            bool: True if the operation succeeds.

        Raises:
            GitlabConnectionError: If the server cannot be reached.
            GitlabDeleteError: If the server fails to perform the request.
        """
        if inspect.isclass(obj):
            if not issubclass(obj, GitlabObject):
                raise GitlabError("Invalid class: %s" % obj)

        params = {obj.idAttr: id if id else getattr(obj, obj.idAttr)}
        params.update(kwargs)

        missing = []
        for k in itertools.chain(obj.requiredUrlAttrs,
                                 obj.requiredDeleteAttrs):
            if k not in params:
                try:
                    params[k] = getattr(obj, k)
                except KeyError:
                    missing.append(k)
        if missing:
            raise GitlabDeleteError('Missing attribute(s): %s' %
                                    ", ".join(missing))

        obj_id = params[obj.idAttr] if obj._id_in_delete_url else None
        url = self._construct_url(id_=obj_id, obj=obj, parameters=params)

        if obj._id_in_delete_url:
            # The ID is already built, no need to add it as extra key in query
            # string
            params.pop(obj.idAttr)

        r = self._raw_delete(url, **params)
        raise_error_from_response(r, GitlabDeleteError,
                                  expected_code=[200, 202, 204])
        return True

    def create(self, obj, **kwargs):
        """Create an object on the GitLab server.

        The object class and attributes define the request to be made on the
        GitLab server.

        Args:
            obj (object): The object to create.
            **kwargs: Additional arguments to send to GitLab.

        Returns:
            str: A json representation of the object as returned by the GitLab
                server

        Raises:
            GitlabConnectionError: If the server cannot be reached.
            GitlabCreateError: If the server fails to perform the request.
        """
        params = obj.__dict__.copy()
        params.update(kwargs)
        missing = []
        for k in itertools.chain(obj.requiredUrlAttrs,
                                 obj.requiredCreateAttrs):
            if k not in params:
                missing.append(k)
        if missing:
            raise GitlabCreateError('Missing attribute(s): %s' %
                                    ", ".join(missing))

        url = self._construct_url(id_=None, obj=obj, parameters=params,
                                  action='create')

        # build data that can really be sent to server
        data = obj._data_for_gitlab(extra_parameters=kwargs)

        r = self._raw_post(url, data=data, content_type='application/json')
        raise_error_from_response(r, GitlabCreateError, 201)
        return r.json()

    def update(self, obj, **kwargs):
        """Update an object on the GitLab server.

        The object class and attributes define the request to be made on the
        GitLab server.

        Args:
            obj (object): The object to create.
            **kwargs: Additional arguments to send to GitLab.

        Returns:
            str: A json representation of the object as returned by the GitLab
                server

        Raises:
            GitlabConnectionError: If the server cannot be reached.
            GitlabUpdateError: If the server fails to perform the request.
        """
        params = obj.__dict__.copy()
        params.update(kwargs)
        missing = []
        if obj.requiredUpdateAttrs or obj.optionalUpdateAttrs:
            required_attrs = obj.requiredUpdateAttrs
        else:
            required_attrs = obj.requiredCreateAttrs
        for k in itertools.chain(obj.requiredUrlAttrs, required_attrs):
            if k not in params:
                missing.append(k)
        if missing:
            raise GitlabUpdateError('Missing attribute(s): %s' %
                                    ", ".join(missing))
        obj_id = params[obj.idAttr] if obj._id_in_update_url else None
        url = self._construct_url(id_=obj_id, obj=obj, parameters=params)

        # build data that can really be sent to server
        data = obj._data_for_gitlab(extra_parameters=kwargs, update=True)

        r = self._raw_put(url, data=data, content_type='application/json')
        raise_error_from_response(r, GitlabUpdateError)
        return r.json()

    def _build_url(self, path):
        """Returns the full url from path.

        If path is already a url, return it unchanged. If it's a path, append
        it to the stored url.

        This is a low-level method, different from _construct_url _build_url
        have no knowledge of GitlabObject's.

        Returns:
            str: The full URL
        """
        if path.startswith('http://') or path.startswith('https://'):
            return path
        else:
            return '%s%s' % (self._url, path)

    def http_request(self, verb, path, query_data={}, post_data={},
                     streamed=False, **kwargs):
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
            **kwargs: Extra data to make the query (e.g. sudo, per_page, page)

        Returns:
            A requests result object.

        Raises:
            GitlabHttpError: When the return code is not 2xx
        """

        def sanitized_url(url):
            parsed = six.moves.urllib.parse.urlparse(url)
            new_path = parsed.path.replace('.', '%2E')
            return parsed._replace(path=new_path).geturl()

        url = self._build_url(path)
        params = query_data.copy()
        params.update(kwargs)
        opts = self._get_session_opts(content_type='application/json')
        verify = opts.pop('verify')
        timeout = opts.pop('timeout')

        # Requests assumes that `.` should not be encoded as %2E and will make
        # changes to urls using this encoding. Using a prepped request we can
        # get the desired behavior.
        # The Requests behavior is right but it seems that web servers don't
        # always agree with this decision (this is the case with a default
        # gitlab installation)
        req = requests.Request(verb, url, json=post_data, params=params,
                               **opts)
        prepped = self.session.prepare_request(req)
        prepped.url = sanitized_url(prepped.url)
        result = self.session.send(prepped, stream=streamed, verify=verify,
                                   timeout=timeout)

        if 200 <= result.status_code < 300:
            return result

        if result.status_code == 401:
            raise GitlabAuthenticationError(response_code=result.status_code,
                                            error_message=result.content)

        raise GitlabHttpError(response_code=result.status_code,
                              error_message=result.content)

    def http_get(self, path, query_data={}, streamed=False, **kwargs):
        """Make a GET request to the Gitlab server.

        Args:
            path (str): Path or full URL to query ('/projects' or
                        'http://whatever/v4/api/projecs')
            query_data (dict): Data to send as query parameters
            streamed (bool): Whether the data should be streamed
            **kwargs: Extra data to make the query (e.g. sudo, per_page, page)

        Returns:
            A requests result object is streamed is True or the content type is
            not json.
            The parsed json data otherwise.

        Raises:
            GitlabHttpError: When the return code is not 2xx
            GitlabParsingError: If the json data could not be parsed
        """
        result = self.http_request('get', path, query_data=query_data,
                                   streamed=streamed, **kwargs)
        if (result.headers['Content-Type'] == 'application/json' and
           not streamed):
            try:
                return result.json()
            except Exception:
                raise GitlabParsingError(
                    error_message="Failed to parse the server message")
        else:
            return result

    def http_list(self, path, query_data={}, as_list=None, **kwargs):
        """Make a GET request to the Gitlab server for list-oriented queries.

        Args:
            path (str): Path or full URL to query ('/projects' or
                        'http://whatever/v4/api/projecs')
            query_data (dict): Data to send as query parameters
            **kwargs: Extra data to make the query (e.g. sudo, per_page, page,
                      all)

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

        # In case we want to change the default behavior at some point
        as_list = True if as_list is None else as_list

        get_all = kwargs.get('all', False)
        url = self._build_url(path)

        if get_all is True:
            return list(GitlabList(self, url, query_data, **kwargs))

        if 'page' in kwargs or 'per_page' in kwargs or as_list is True:
            # pagination requested, we return a list
            return list(GitlabList(self, url, query_data, get_next=False,
                                   **kwargs))

        # No pagination, generator requested
        return GitlabList(self, url, query_data, **kwargs)

    def http_post(self, path, query_data={}, post_data={}, **kwargs):
        """Make a POST request to the Gitlab server.

        Args:
            path (str): Path or full URL to query ('/projects' or
                        'http://whatever/v4/api/projecs')
            query_data (dict): Data to send as query parameters
            post_data (dict): Data to send in the body (will be converted to
                              json)
            **kwargs: Extra data to make the query (e.g. sudo, per_page, page)

        Returns:
            The parsed json returned by the server if json is return, else the
            raw content

        Raises:
            GitlabHttpError: When the return code is not 2xx
            GitlabParsingError: If the json data could not be parsed
        """
        result = self.http_request('post', path, query_data=query_data,
                                   post_data=post_data, **kwargs)
        try:
            if result.headers.get('Content-Type', None) == 'application/json':
                return result.json()
        except Exception:
            raise GitlabParsingError(
                error_message="Failed to parse the server message")
        return result

    def http_put(self, path, query_data={}, post_data={}, **kwargs):
        """Make a PUT request to the Gitlab server.

        Args:
            path (str): Path or full URL to query ('/projects' or
                        'http://whatever/v4/api/projecs')
            query_data (dict): Data to send as query parameters
            post_data (dict): Data to send in the body (will be converted to
                              json)
            **kwargs: Extra data to make the query (e.g. sudo, per_page, page)

        Returns:
            The parsed json returned by the server.

        Raises:
            GitlabHttpError: When the return code is not 2xx
            GitlabParsingError: If the json data could not be parsed
        """
        result = self.http_request('put', path, query_data=query_data,
                                   post_data=post_data, **kwargs)
        try:
            return result.json()
        except Exception:
            raise GitlabParsingError(
                error_message="Failed to parse the server message")

    def http_delete(self, path, **kwargs):
        """Make a PUT request to the Gitlab server.

        Args:
            path (str): Path or full URL to query ('/projects' or
                        'http://whatever/v4/api/projecs')
            **kwargs: Extra data to make the query (e.g. sudo, per_page, page)

        Returns:
            The requests object.

        Raises:
            GitlabHttpError: When the return code is not 2xx
        """
        return self.http_request('delete', path, **kwargs)


class GitlabList(object):
    """Generator representing a list of remote objects.

    The object handles the links returned by a query to the API, and will call
    the API again when needed.
    """

    def __init__(self, gl, url, query_data, get_next=True, **kwargs):
        self._gl = gl
        self._query(url, query_data, **kwargs)
        self._get_next = get_next

    def _query(self, url, query_data={}, **kwargs):
        result = self._gl.http_request('get', url, query_data=query_data,
                                       **kwargs)
        try:
            self._next_url = result.links['next']['url']
        except KeyError:
            self._next_url = None
        self._current_page = result.headers.get('X-Page')
        self._next_page = result.headers.get('X-Next-Page')
        self._per_page = result.headers.get('X-Per-Page')
        self._total_pages = result.headers.get('X-Total-Pages')
        self._total = result.headers.get('X-Total')

        try:
            self._data = result.json()
        except Exception:
            raise GitlabParsingError(
                error_message="Failed to parse the server message")

        self._current = 0

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
            if self._next_url and self._get_next is True:
                self._query(self._next_url)
                return self.next()

            raise StopIteration

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

import os

from six.moves import configparser

_DEFAULT_FILES = [
    '/etc/python-gitlab.cfg',
    os.path.expanduser('~/.python-gitlab.cfg')
]


class ConfigError(Exception):
    pass


class GitlabIDError(ConfigError):
    pass


class GitlabDataError(ConfigError):
    pass


class GitlabConfigParser(object):
    def __init__(self, gitlab_id=None, config_files=None):
        self.gitlab_id = gitlab_id
        _files = config_files or _DEFAULT_FILES
        self._config = configparser.ConfigParser()
        self._config.read(_files)

        if self.gitlab_id is None:
            try:
                self.gitlab_id = self._config.get('global', 'default')
            except Exception:
                raise GitlabIDError("Impossible to get the gitlab id "
                                    "(not specified in config file)")

        try:
            self.url = self._config.get(self.gitlab_id, 'url')
        except Exception:
            raise GitlabDataError("Impossible to get gitlab informations from "
                                  "configuration (%s)" % self.gitlab_id)

        self.ssl_verify = True
        try:
            self.ssl_verify = self._config.getboolean('global', 'ssl_verify')
        except ValueError:
            # Value Error means the option exists but isn't a boolean.
            # Get as a string instead as it should then be a local path to a
            # CA bundle.
            try:
                self.ssl_verify = self._config.get('global', 'ssl_verify')
            except Exception:
                pass
        except Exception:
            pass
        try:
            self.ssl_verify = self._config.getboolean(self.gitlab_id,
                                                      'ssl_verify')
        except ValueError:
            # Value Error means the option exists but isn't a boolean.
            # Get as a string instead as it should then be a local path to a
            # CA bundle.
            try:
                self.ssl_verify = self._config.get(self.gitlab_id,
                                                   'ssl_verify')
            except Exception:
                pass
        except Exception:
            pass

        self.timeout = 60
        try:
            self.timeout = self._config.getint('global', 'timeout')
        except Exception:
            pass
        try:
            self.timeout = self._config.getint(self.gitlab_id, 'timeout')
        except Exception:
            pass

        self.private_token = None
        try:
            self.private_token = self._config.get(self.gitlab_id,
                                                  'private_token')
        except Exception:
            pass

        self.oauth_token = None
        try:
            self.oauth_token = self._config.get(self.gitlab_id, 'oauth_token')
        except Exception:
            pass

        self.http_username = None
        self.http_password = None
        try:
            self.http_username = self._config.get(self.gitlab_id,
                                                  'http_username')
            self.http_password = self._config.get(self.gitlab_id,
                                                  'http_password')
        except Exception:
            pass

        self.http_username = None
        self.http_password = None
        try:
            self.http_username = self._config.get(self.gitlab_id,
                                                  'http_username')
            self.http_password = self._config.get(self.gitlab_id,
                                                  'http_password')
        except Exception:
            pass

        self.api_version = '4'
        try:
            self.api_version = self._config.get('global', 'api_version')
        except Exception:
            pass
        try:
            self.api_version = self._config.get(self.gitlab_id, 'api_version')
        except Exception:
            pass
        if self.api_version not in ('3', '4'):
            raise GitlabDataError("Unsupported API version: %s" %
                                  self.api_version)

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

import configparser
import os
import shlex
import subprocess
from os.path import expanduser, expandvars
from pathlib import Path
from typing import List, Optional, Union

from gitlab.const import USER_AGENT

_DEFAULT_FILES: List[str] = [
    "/etc/python-gitlab.cfg",
    str(Path.home() / ".python-gitlab.cfg"),
]

HELPER_PREFIX = "helper:"

HELPER_ATTRIBUTES = ["job_token", "http_password", "private_token", "oauth_token"]


def _resolve_file(filepath: Union[Path, str]) -> str:
    resolved = Path(filepath).resolve(strict=True)
    return str(resolved)


def _get_config_files(
    config_files: Optional[List[str]] = None,
) -> Union[str, List[str]]:
    """
    Return resolved path(s) to config files if they exist, with precedence:
    1. Files passed in config_files
    2. File defined in PYTHON_GITLAB_CFG
    3. User- and system-wide config files
    """
    resolved_files = []

    if config_files:
        for config_file in config_files:
            try:
                resolved = _resolve_file(config_file)
            except OSError as e:
                raise GitlabConfigMissingError(f"Cannot read config from file: {e}")
            resolved_files.append(resolved)

        return resolved_files

    try:
        env_config = os.environ["PYTHON_GITLAB_CFG"]
        return _resolve_file(env_config)
    except KeyError:
        pass
    except OSError as e:
        raise GitlabConfigMissingError(
            f"Cannot read config from PYTHON_GITLAB_CFG: {e}"
        )

    for config_file in _DEFAULT_FILES:
        try:
            resolved = _resolve_file(config_file)
        except OSError:
            continue
        resolved_files.append(resolved)

    return resolved_files


class ConfigError(Exception):
    pass


class GitlabIDError(ConfigError):
    pass


class GitlabDataError(ConfigError):
    pass


class GitlabConfigMissingError(ConfigError):
    pass


class GitlabConfigHelperError(ConfigError):
    pass


class GitlabConfigParser(object):
    def __init__(
        self, gitlab_id: Optional[str] = None, config_files: Optional[List[str]] = None
    ) -> None:
        self.gitlab_id = gitlab_id
        self.http_username: Optional[str] = None
        self.http_password: Optional[str] = None
        self.job_token: Optional[str] = None
        self.oauth_token: Optional[str] = None
        self.private_token: Optional[str] = None

        self.api_version: str = "4"
        self.order_by: Optional[str] = None
        self.pagination: Optional[str] = None
        self.per_page: Optional[int] = None
        self.retry_transient_errors: bool = False
        self.ssl_verify: Union[bool, str] = True
        self.timeout: int = 60
        self.url: Optional[str] = None
        self.user_agent: str = USER_AGENT

        self._files = _get_config_files(config_files)
        if self._files:
            self._parse_config()

    def _parse_config(self) -> None:
        _config = configparser.ConfigParser()
        _config.read(self._files)

        if self.gitlab_id is None:
            try:
                self.gitlab_id = _config.get("global", "default")
            except Exception as e:
                raise GitlabIDError(
                    "Impossible to get the gitlab id (not specified in config file)"
                ) from e

        try:
            self.url = _config.get(self.gitlab_id, "url")
        except Exception as e:
            raise GitlabDataError(
                "Impossible to get gitlab details from "
                f"configuration ({self.gitlab_id})"
            ) from e

        try:
            self.ssl_verify = _config.getboolean("global", "ssl_verify")
        except ValueError:
            # Value Error means the option exists but isn't a boolean.
            # Get as a string instead as it should then be a local path to a
            # CA bundle.
            try:
                self.ssl_verify = _config.get("global", "ssl_verify")
            except Exception:
                pass
        except Exception:
            pass
        try:
            self.ssl_verify = _config.getboolean(self.gitlab_id, "ssl_verify")
        except ValueError:
            # Value Error means the option exists but isn't a boolean.
            # Get as a string instead as it should then be a local path to a
            # CA bundle.
            try:
                self.ssl_verify = _config.get(self.gitlab_id, "ssl_verify")
            except Exception:
                pass
        except Exception:
            pass

        try:
            self.timeout = _config.getint("global", "timeout")
        except Exception:
            pass
        try:
            self.timeout = _config.getint(self.gitlab_id, "timeout")
        except Exception:
            pass

        try:
            self.private_token = _config.get(self.gitlab_id, "private_token")
        except Exception:
            pass

        try:
            self.oauth_token = _config.get(self.gitlab_id, "oauth_token")
        except Exception:
            pass

        try:
            self.job_token = _config.get(self.gitlab_id, "job_token")
        except Exception:
            pass

        try:
            self.http_username = _config.get(self.gitlab_id, "http_username")
            self.http_password = _config.get(self.gitlab_id, "http_password")
        except Exception:
            pass

        self._get_values_from_helper()

        try:
            self.api_version = _config.get("global", "api_version")
        except Exception:
            pass
        try:
            self.api_version = _config.get(self.gitlab_id, "api_version")
        except Exception:
            pass
        if self.api_version not in ("4",):
            raise GitlabDataError(f"Unsupported API version: {self.api_version}")

        for section in ["global", self.gitlab_id]:
            try:
                self.per_page = _config.getint(section, "per_page")
            except Exception:
                pass
        if self.per_page is not None and not 0 <= self.per_page <= 100:
            raise GitlabDataError(f"Unsupported per_page number: {self.per_page}")

        try:
            self.pagination = _config.get(self.gitlab_id, "pagination")
        except Exception:
            pass

        try:
            self.order_by = _config.get(self.gitlab_id, "order_by")
        except Exception:
            pass

        try:
            self.user_agent = _config.get("global", "user_agent")
        except Exception:
            pass
        try:
            self.user_agent = _config.get(self.gitlab_id, "user_agent")
        except Exception:
            pass

        try:
            self.retry_transient_errors = _config.getboolean(
                "global", "retry_transient_errors"
            )
        except Exception:
            pass
        try:
            self.retry_transient_errors = _config.getboolean(
                self.gitlab_id, "retry_transient_errors"
            )
        except Exception:
            pass

    def _get_values_from_helper(self) -> None:
        """Update attributes that may get values from an external helper program"""
        for attr in HELPER_ATTRIBUTES:
            value = getattr(self, attr)
            if not isinstance(value, str):
                continue

            if not value.lower().strip().startswith(HELPER_PREFIX):
                continue

            helper = value[len(HELPER_PREFIX) :].strip()
            commmand = [expanduser(expandvars(token)) for token in shlex.split(helper)]

            try:
                value = (
                    subprocess.check_output(commmand, stderr=subprocess.PIPE)
                    .decode("utf-8")
                    .strip()
                )
            except subprocess.CalledProcessError as e:
                stderr = e.stderr.decode().strip()
                raise GitlabConfigHelperError(
                    f"Failed to read {attr} value from helper "
                    f"for {self.gitlab_id}:\n{stderr}"
                ) from e

            setattr(self, attr, value)

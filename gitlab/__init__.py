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

import warnings
from typing import Any

from . import config as config  # noqa: F401
from . import const as const
from . import exceptions as exceptions  # noqa: F401
from .client import Gitlab as Gitlab  # noqa: F401
from .client import GitlabList as GitlabList  # noqa: F401
from .exceptions import *  # noqa: F401,F403
from .version import __author__ as __author__  # noqa: F401
from .version import __copyright__ as __copyright__  # noqa: F401
from .version import __email__ as __email__  # noqa: F401
from .version import __license__ as __license__  # noqa: F401
from .version import __title__ as __title__  # noqa: F401
from .version import __version__ as __version__  # noqa: F401

warnings.filterwarnings("default", category=DeprecationWarning, module="^gitlab")


# NOTE(jlvillal): We are deprecating access to the gitlab.const values which
# were previously imported into this namespace by the
# 'from gitlab.const import *' statement.
def __getattr__(name: str) -> Any:
    # Deprecate direct access to constants without namespace
    if name in const._DEPRECATED:
        warnings.warn(
            f"\nDirect access to 'gitlab.{name}' is deprecated and will be "
            f"removed in a future major python-gitlab release. Please "
            f"use 'gitlab.const.{name}' instead.",
            DeprecationWarning,
        )
        return getattr(const, name)
    raise AttributeError(f"module {__name__} has no attribute {name}")

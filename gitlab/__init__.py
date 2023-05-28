# -*- coding: utf-8 -*-
#
# Copyright (C) 2013-2019 Gauvain Pocentek, 2019-2023 python-gitlab team
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

import gitlab.config  # noqa: F401
from gitlab import utils as _utils
from gitlab._version import (  # noqa: F401
    __author__,
    __copyright__,
    __email__,
    __license__,
    __title__,
    __version__,
)
from gitlab.client import Gitlab, GitlabList  # noqa: F401
from gitlab.exceptions import *  # noqa: F401,F403

warnings.filterwarnings("default", category=DeprecationWarning, module="^gitlab")


# NOTE(jlvillal): We are deprecating access to the gitlab.const values which
# were previously imported into this namespace by the
# 'from gitlab.const import *' statement.
def __getattr__(name: str) -> Any:
    # Deprecate direct access to constants without namespace
    if name in gitlab.const._DEPRECATED:
        _utils.warn(
            message=(
                f"\nDirect access to constants as 'gitlab.{name}' is deprecated and "
                f"will be removed in a future major python-gitlab release. Please "
                f"see the usage of constants in the 'gitlab.const' module instead."
            ),
            category=DeprecationWarning,
        )
        return getattr(gitlab.const, name)
    raise AttributeError(f"module {__name__} has no attribute {name}")


__all__ = [
    "__author__",
    "__copyright__",
    "__email__",
    "__license__",
    "__title__",
    "__version__",
    "Gitlab",
    "GitlabList",
]
__all__.extend(gitlab.const._DEPRECATED)
__all__.extend(gitlab.exceptions.__all__)

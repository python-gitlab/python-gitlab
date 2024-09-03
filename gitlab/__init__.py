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

import gitlab.config  # noqa: F401
from gitlab._version import (  # noqa: F401
    __author__,
    __copyright__,
    __email__,
    __license__,
    __title__,
    __version__,
)
from gitlab.client import Gitlab, GitlabList, GraphQL  # noqa: F401
from gitlab.exceptions import *  # noqa: F401,F403

warnings.filterwarnings("default", category=DeprecationWarning, module="^gitlab")


__all__ = [
    "__author__",
    "__copyright__",
    "__email__",
    "__license__",
    "__title__",
    "__version__",
    "Gitlab",
    "GitlabList",
    "GraphQL",
]
__all__.extend(gitlab.exceptions.__all__)

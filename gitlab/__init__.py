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

import gitlab.config
from gitlab.__version__ import (
    __author__,
    __copyright__,
    __email__,
    __license__,
    __title__,
    __version__,
)
from gitlab.client import Gitlab, GitlabList
from gitlab.const import *  # noqa
from gitlab.exceptions import *  # noqa
from gitlab import utils  # noqa


warnings.filterwarnings("default", category=DeprecationWarning, module="^gitlab")

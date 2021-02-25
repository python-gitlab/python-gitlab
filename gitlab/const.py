# -*- coding: utf-8 -*-
#
# Copyright (C) 2016-2017 Gauvain Pocentek <gauvain@pocentek.net>
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

from gitlab.__version__ import __title__, __version__


NO_ACCESS: int = 0
MINIMAL_ACCESS: int = 5
GUEST_ACCESS: int = 10
REPORTER_ACCESS: int = 20
DEVELOPER_ACCESS: int = 30
MAINTAINER_ACCESS: int = 40
MASTER_ACCESS: int = MAINTAINER_ACCESS
OWNER_ACCESS: int = 50

VISIBILITY_PRIVATE: int = 0
VISIBILITY_INTERNAL: int = 10
VISIBILITY_PUBLIC: int = 20

NOTIFICATION_LEVEL_DISABLED: str = "disabled"
NOTIFICATION_LEVEL_PARTICIPATING: str = "participating"
NOTIFICATION_LEVEL_WATCH: str = "watch"
NOTIFICATION_LEVEL_GLOBAL: str = "global"
NOTIFICATION_LEVEL_MENTION: str = "mention"
NOTIFICATION_LEVEL_CUSTOM: str = "custom"

# Search scopes
# all scopes (global, group and  project)
SEARCH_SCOPE_PROJECTS: str = "projects"
SEARCH_SCOPE_ISSUES: str = "issues"
SEARCH_SCOPE_MERGE_REQUESTS: str = "merge_requests"
SEARCH_SCOPE_MILESTONES: str = "milestones"
SEARCH_SCOPE_WIKI_BLOBS: str = "wiki_blobs"
SEARCH_SCOPE_COMMITS: str = "commits"
SEARCH_SCOPE_BLOBS: str = "blobs"
SEARCH_SCOPE_USERS: str = "users"

# specific global scope
SEARCH_SCOPE_GLOBAL_SNIPPET_TITLES: str = "snippet_titles"

# specific project scope
SEARCH_SCOPE_PROJECT_NOTES: str = "notes"

USER_AGENT: str = "{}/{}".format(__title__, __version__)

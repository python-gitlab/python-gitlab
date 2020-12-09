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

NO_ACCESS = 0
MINIMAL_ACCESS = 5
GUEST_ACCESS = 10
REPORTER_ACCESS = 20
DEVELOPER_ACCESS = 30
MAINTAINER_ACCESS = 40
MASTER_ACCESS = MAINTAINER_ACCESS
OWNER_ACCESS = 50

VISIBILITY_PRIVATE = 0
VISIBILITY_INTERNAL = 10
VISIBILITY_PUBLIC = 20

NOTIFICATION_LEVEL_DISABLED = "disabled"
NOTIFICATION_LEVEL_PARTICIPATING = "participating"
NOTIFICATION_LEVEL_WATCH = "watch"
NOTIFICATION_LEVEL_GLOBAL = "global"
NOTIFICATION_LEVEL_MENTION = "mention"
NOTIFICATION_LEVEL_CUSTOM = "custom"

# Search scopes
# all scopes (global, group and  project)
SEARCH_SCOPE_PROJECTS = "projects"
SEARCH_SCOPE_ISSUES = "issues"
SEARCH_SCOPE_MERGE_REQUESTS = "merge_requests"
SEARCH_SCOPE_MILESTONES = "milestones"
SEARCH_SCOPE_WIKI_BLOBS = "wiki_blobs"
SEARCH_SCOPE_COMMITS = "commits"
SEARCH_SCOPE_BLOBS = "blobs"
SEARCH_SCOPE_USERS = "users"

# specific global scope
SEARCH_SCOPE_GLOBAL_SNIPPET_TITLES = "snippet_titles"

# specific project scope
SEARCH_SCOPE_PROJECT_NOTES = "notes"

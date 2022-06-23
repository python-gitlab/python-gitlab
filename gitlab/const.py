# -*- coding: utf-8 -*-
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

from typing import Any

from gitlab._version import __title__, __version__

# NOTE(jlvillal): '_DEPRECATED' only affects users accessing constants via the
# top-level gitlab.* namespace. See 'gitlab/__init__.py:__getattr__()' for the
# consumer of '_DEPRECATED' For example 'x = gitlab.NO_ACCESS'.  We want users
# to instead use constants by doing code like: gitlab.const.NO_ACCESS.
_DEPRECATED = [
    "ADMIN_ACCESS",
    "DEFAULT_URL",
    "DEVELOPER_ACCESS",
    "GUEST_ACCESS",
    "MAINTAINER_ACCESS",
    "MINIMAL_ACCESS",
    "NO_ACCESS",
    "NOTIFICATION_LEVEL_CUSTOM",
    "NOTIFICATION_LEVEL_DISABLED",
    "NOTIFICATION_LEVEL_GLOBAL",
    "NOTIFICATION_LEVEL_MENTION",
    "NOTIFICATION_LEVEL_PARTICIPATING",
    "NOTIFICATION_LEVEL_WATCH",
    "OWNER_ACCESS",
    "REPORTER_ACCESS",
    "SEARCH_SCOPE_BLOBS",
    "SEARCH_SCOPE_COMMITS",
    "SEARCH_SCOPE_GLOBAL_SNIPPET_TITLES",
    "SEARCH_SCOPE_ISSUES",
    "SEARCH_SCOPE_MERGE_REQUESTS",
    "SEARCH_SCOPE_MILESTONES",
    "SEARCH_SCOPE_PROJECT_NOTES",
    "SEARCH_SCOPE_PROJECTS",
    "SEARCH_SCOPE_USERS",
    "SEARCH_SCOPE_WIKI_BLOBS",
    "USER_AGENT",
    "VISIBILITY_INTERNAL",
    "VISIBILITY_PRIVATE",
    "VISIBILITY_PUBLIC",
]


class GitlabConstant:
    def __new__(cls, value: Any) -> str:  # type: ignore
        # This allows us to get a string representation of a value.
        # For example: AccessLevel(10)
        for attr, attr_value in cls.__dict__.items():
            if value == attr_value:
                return attr
        raise ValueError(f"{value!r} is not a valid {cls.__qualname__}")


# https://gitlab.com/gitlab-org/gitlab/-/blob/e97357824bedf007e75f8782259fe07435b64fbb/lib/gitlab/access.rb#L12-18
class AccessLevel(GitlabConstant):
    NO_ACCESS: int = 0
    MINIMAL_ACCESS: int = 5
    GUEST: int = 10
    REPORTER: int = 20
    DEVELOPER: int = 30
    MAINTAINER: int = 40
    OWNER: int = 50
    ADMIN: int = 60


# https://gitlab.com/gitlab-org/gitlab/-/blob/e97357824bedf007e75f8782259fe07435b64fbb/lib/gitlab/visibility_level.rb#L23-25
class Visibility(GitlabConstant):
    PRIVATE: str = "private"
    INTERNAL: str = "internal"
    PUBLIC: str = "public"


class NotificationLevel(GitlabConstant):
    DISABLED: str = "disabled"
    PARTICIPATING: str = "participating"
    WATCH: str = "watch"
    GLOBAL: str = "global"
    MENTION: str = "mention"
    CUSTOM: str = "custom"


# https://gitlab.com/gitlab-org/gitlab/-/blob/e97357824bedf007e75f8782259fe07435b64fbb/app/views/search/_category.html.haml#L10-37
class SearchScope(GitlabConstant):
    # all scopes (global, group and  project)
    PROJECTS: str = "projects"
    ISSUES: str = "issues"
    MERGE_REQUESTS: str = "merge_requests"
    MILESTONES: str = "milestones"
    WIKI_BLOBS: str = "wiki_blobs"
    COMMITS: str = "commits"
    BLOBS: str = "blobs"
    USERS: str = "users"

    # specific global scope
    GLOBAL_SNIPPET_TITLES: str = "snippet_titles"

    # specific project scope
    PROJECT_NOTES: str = "notes"


DEFAULT_URL: str = "https://gitlab.com"

NO_ACCESS = AccessLevel.NO_ACCESS
MINIMAL_ACCESS = AccessLevel.MINIMAL_ACCESS
GUEST_ACCESS = AccessLevel.GUEST
REPORTER_ACCESS = AccessLevel.REPORTER
DEVELOPER_ACCESS = AccessLevel.DEVELOPER
MAINTAINER_ACCESS = AccessLevel.MAINTAINER
OWNER_ACCESS = AccessLevel.OWNER
ADMIN_ACCESS = AccessLevel.ADMIN

VISIBILITY_PRIVATE = Visibility.PRIVATE
VISIBILITY_INTERNAL = Visibility.INTERNAL
VISIBILITY_PUBLIC = Visibility.PUBLIC

NOTIFICATION_LEVEL_DISABLED = NotificationLevel.DISABLED
NOTIFICATION_LEVEL_PARTICIPATING = NotificationLevel.PARTICIPATING
NOTIFICATION_LEVEL_WATCH = NotificationLevel.WATCH
NOTIFICATION_LEVEL_GLOBAL = NotificationLevel.GLOBAL
NOTIFICATION_LEVEL_MENTION = NotificationLevel.MENTION
NOTIFICATION_LEVEL_CUSTOM = NotificationLevel.CUSTOM

# Search scopes
# all scopes (global, group and  project)
SEARCH_SCOPE_PROJECTS = SearchScope.PROJECTS
SEARCH_SCOPE_ISSUES = SearchScope.ISSUES
SEARCH_SCOPE_MERGE_REQUESTS = SearchScope.MERGE_REQUESTS
SEARCH_SCOPE_MILESTONES = SearchScope.MILESTONES
SEARCH_SCOPE_WIKI_BLOBS = SearchScope.WIKI_BLOBS
SEARCH_SCOPE_COMMITS = SearchScope.COMMITS
SEARCH_SCOPE_BLOBS = SearchScope.BLOBS
SEARCH_SCOPE_USERS = SearchScope.USERS

# specific global scope
SEARCH_SCOPE_GLOBAL_SNIPPET_TITLES = SearchScope.GLOBAL_SNIPPET_TITLES

# specific project scope
SEARCH_SCOPE_PROJECT_NOTES = SearchScope.PROJECT_NOTES

USER_AGENT: str = f"{__title__}/{__version__}"

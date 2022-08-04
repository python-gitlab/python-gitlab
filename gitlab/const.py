from enum import Enum, IntEnum

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


class GitlabEnum(str, Enum):
    """An enum mixed in with str to make it JSON-serializable."""


# https://gitlab.com/gitlab-org/gitlab/-/blob/e97357824bedf007e75f8782259fe07435b64fbb/lib/gitlab/access.rb#L12-18
class AccessLevel(IntEnum):
    NO_ACCESS: int = 0
    MINIMAL_ACCESS: int = 5
    GUEST: int = 10
    REPORTER: int = 20
    DEVELOPER: int = 30
    MAINTAINER: int = 40
    OWNER: int = 50
    ADMIN: int = 60


# https://gitlab.com/gitlab-org/gitlab/-/blob/e97357824bedf007e75f8782259fe07435b64fbb/lib/gitlab/visibility_level.rb#L23-25
class Visibility(GitlabEnum):
    PRIVATE: str = "private"
    INTERNAL: str = "internal"
    PUBLIC: str = "public"


class NotificationLevel(GitlabEnum):
    DISABLED: str = "disabled"
    PARTICIPATING: str = "participating"
    WATCH: str = "watch"
    GLOBAL: str = "global"
    MENTION: str = "mention"
    CUSTOM: str = "custom"


# https://gitlab.com/gitlab-org/gitlab/-/blob/e97357824bedf007e75f8782259fe07435b64fbb/app/views/search/_category.html.haml#L10-37
class SearchScope(GitlabEnum):
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

NO_ACCESS = AccessLevel.NO_ACCESS.value
MINIMAL_ACCESS = AccessLevel.MINIMAL_ACCESS.value
GUEST_ACCESS = AccessLevel.GUEST.value
REPORTER_ACCESS = AccessLevel.REPORTER.value
DEVELOPER_ACCESS = AccessLevel.DEVELOPER.value
MAINTAINER_ACCESS = AccessLevel.MAINTAINER.value
OWNER_ACCESS = AccessLevel.OWNER.value
ADMIN_ACCESS = AccessLevel.ADMIN.value

VISIBILITY_PRIVATE = Visibility.PRIVATE.value
VISIBILITY_INTERNAL = Visibility.INTERNAL.value
VISIBILITY_PUBLIC = Visibility.PUBLIC.value

NOTIFICATION_LEVEL_DISABLED = NotificationLevel.DISABLED.value
NOTIFICATION_LEVEL_PARTICIPATING = NotificationLevel.PARTICIPATING.value
NOTIFICATION_LEVEL_WATCH = NotificationLevel.WATCH.value
NOTIFICATION_LEVEL_GLOBAL = NotificationLevel.GLOBAL.value
NOTIFICATION_LEVEL_MENTION = NotificationLevel.MENTION.value
NOTIFICATION_LEVEL_CUSTOM = NotificationLevel.CUSTOM.value

# Search scopes
# all scopes (global, group and  project)
SEARCH_SCOPE_PROJECTS = SearchScope.PROJECTS.value
SEARCH_SCOPE_ISSUES = SearchScope.ISSUES.value
SEARCH_SCOPE_MERGE_REQUESTS = SearchScope.MERGE_REQUESTS.value
SEARCH_SCOPE_MILESTONES = SearchScope.MILESTONES.value
SEARCH_SCOPE_WIKI_BLOBS = SearchScope.WIKI_BLOBS.value
SEARCH_SCOPE_COMMITS = SearchScope.COMMITS.value
SEARCH_SCOPE_BLOBS = SearchScope.BLOBS.value
SEARCH_SCOPE_USERS = SearchScope.USERS.value

# specific global scope
SEARCH_SCOPE_GLOBAL_SNIPPET_TITLES = SearchScope.GLOBAL_SNIPPET_TITLES.value

# specific project scope
SEARCH_SCOPE_PROJECT_NOTES = SearchScope.PROJECT_NOTES.value

USER_AGENT: str = f"{__title__}/{__version__}"

__all__ = [
    "AccessLevel",
    "Visibility",
    "NotificationLevel",
    "SearchScope",
]
__all__.extend(_DEPRECATED)

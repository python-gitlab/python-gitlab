from enum import Enum, IntEnum

from gitlab._version import __title__, __version__


class GitlabEnum(str, Enum):
    """An enum mixed in with str to make it JSON-serializable."""


# https://gitlab.com/gitlab-org/gitlab/-/blob/e97357824bedf007e75f8782259fe07435b64fbb/lib/gitlab/access.rb#L12-18
class AccessLevel(IntEnum):
    NO_ACCESS = 0
    MINIMAL_ACCESS = 5
    GUEST = 10
    PLANNER = 15
    REPORTER = 20
    DEVELOPER = 30
    MAINTAINER = 40
    OWNER = 50
    ADMIN = 60


# https://gitlab.com/gitlab-org/gitlab/-/blob/e97357824bedf007e75f8782259fe07435b64fbb/lib/gitlab/visibility_level.rb#L23-25
class Visibility(GitlabEnum):
    PRIVATE = "private"
    INTERNAL = "internal"
    PUBLIC = "public"


class NotificationLevel(GitlabEnum):
    DISABLED = "disabled"
    PARTICIPATING = "participating"
    WATCH = "watch"
    GLOBAL = "global"
    MENTION = "mention"
    CUSTOM = "custom"


# https://gitlab.com/gitlab-org/gitlab/-/blob/e97357824bedf007e75f8782259fe07435b64fbb/app/views/search/_category.html.haml#L10-37
class SearchScope(GitlabEnum):
    # all scopes (global, group and  project)
    PROJECTS = "projects"
    ISSUES = "issues"
    MERGE_REQUESTS = "merge_requests"
    MILESTONES = "milestones"
    WIKI_BLOBS = "wiki_blobs"
    COMMITS = "commits"
    BLOBS = "blobs"
    USERS = "users"

    # specific global scope
    GLOBAL_SNIPPET_TITLES = "snippet_titles"

    # specific project scope
    PROJECT_NOTES = "notes"


# https://docs.gitlab.com/ee/api/merge_requests.html#merge-status
class DetailedMergeStatus(GitlabEnum):
    # possible values for the detailed_merge_status field of Merge Requests
    BLOCKED_STATUS = "blocked_status"
    BROKEN_STATUS = "broken_status"
    CHECKING = "checking"
    UNCHECKED = "unchecked"
    CI_MUST_PASS = "ci_must_pass"
    CI_STILL_RUNNING = "ci_still_running"
    DISCUSSIONS_NOT_RESOLVED = "discussions_not_resolved"
    DRAFT_STATUS = "draft_status"
    EXTERNAL_STATUS_CHECKS = "external_status_checks"
    MERGEABLE = "mergeable"
    NOT_APPROVED = "not_approved"
    NOT_OPEN = "not_open"
    POLICIES_DENIED = "policies_denied"


# https://docs.gitlab.com/ee/api/pipelines.html
class PipelineStatus(GitlabEnum):
    CREATED = "created"
    WAITING_FOR_RESOURCE = "waiting_for_resource"
    PREPARING = "preparing"
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    CANCELED = "canceled"
    SKIPPED = "skipped"
    MANUAL = "manual"
    SCHEDULED = "scheduled"


DEFAULT_URL: str = "https://gitlab.com"

NO_ACCESS = AccessLevel.NO_ACCESS.value
MINIMAL_ACCESS = AccessLevel.MINIMAL_ACCESS.value
GUEST_ACCESS = AccessLevel.GUEST.value
PLANNER_ACCESS = AccessLevel.PLANNER.value
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

NO_JSON_RESPONSE_CODES = [204]
RETRYABLE_TRANSIENT_ERROR_CODES = [500, 502, 503, 504] + list(range(520, 531))

__all__ = [
    "AccessLevel",
    "Visibility",
    "NotificationLevel",
    "SearchScope",
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
    "PLANNER_ACCESS",
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

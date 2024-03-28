import logging
import time
from typing import Optional, TYPE_CHECKING

import pytest

import gitlab
import gitlab.base
import gitlab.exceptions

SLEEP_INTERVAL = 0.5
TIMEOUT = 60  # seconds before timeout will occur
MAX_ITERATIONS = int(TIMEOUT / SLEEP_INTERVAL)


def get_gitlab_plan(gl: gitlab.Gitlab) -> Optional[str]:
    """Determine the license available on the GitLab instance"""
    try:
        license = gl.get_license()
    except gitlab.exceptions.GitlabLicenseError:
        # Without a license we assume only Free features are available
        return None

    if TYPE_CHECKING:
        assert isinstance(license["plan"], str)
    return license["plan"]


def safe_delete(object: gitlab.base.RESTObject) -> None:
    """Ensure the object specified can not be retrieved. If object still exists after
    timeout period, fail the test"""
    manager = object.manager
    for index in range(MAX_ITERATIONS):
        try:
            object = manager.get(object.get_id())  # type: ignore[attr-defined]
        except gitlab.exceptions.GitlabGetError:
            return

        if index:
            logging.info(f"Attempt {index + 1} to delete {object!r}.")
        try:
            if isinstance(object, gitlab.v4.objects.User):
                # You can't use this option if the selected user is the sole owner of any groups
                # Use `hard_delete=True` or a 'Ghost User' may be created.
                # https://docs.gitlab.com/ee/api/users.html#user-deletion
                object.delete(hard_delete=True)
                if index > 1:
                    # If User is the sole owner of any group it won't be deleted,
                    # which combined with parents group never immediately deleting in GL 16
                    # we shouldn't cause test to fail if it still exists
                    return
            elif isinstance(object, gitlab.v4.objects.Project):
                # Immediately delete rather than waiting for at least 1day
                # https://docs.gitlab.com/ee/api/projects.html#delete-project
                object.delete(permanently_remove=True)
                pass
            else:
                # We only attempt to delete parent groups to prevent dangling sub-groups
                # However parent groups can only be deleted on a delay in Gl 16
                # https://docs.gitlab.com/ee/api/groups.html#remove-group
                object.delete()
        except gitlab.exceptions.GitlabDeleteError:
            logging.info(f"{object!r} already deleted or scheduled for deletion.")
            if isinstance(object, gitlab.v4.objects.Group):
                # Parent groups can never be immediately deleted in GL 16,
                # so don't cause test to fail if it still exists
                return
            pass

        time.sleep(SLEEP_INTERVAL)
    pytest.fail(f"{object!r} was not deleted")

from __future__ import annotations

import logging
import time
from typing import TYPE_CHECKING

import pytest

import gitlab
import gitlab.base
import gitlab.exceptions
import gitlab.v4.objects

SLEEP_INTERVAL = 0.5
TIMEOUT = 60  # seconds before timeout will occur
MAX_ITERATIONS = int(TIMEOUT / SLEEP_INTERVAL)


def get_gitlab_plan(gl: gitlab.Gitlab) -> str | None:
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
        # If object is already marked for deletion we have succeeded
        if getattr(object, "marked_for_deletion_on", None) is not None:
            # 'Group' and 'Project' objects have a 'marked_for_deletion_on' attribute
            logging.info(f"{object!r} is marked for deletion.")
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
                # Starting in GitLab 18, projects can't be immediately deleted.
                # So this will mark it for deletion.
                object.delete()
            else:
                # We only attempt to delete parent groups to prevent dangling sub-groups
                # However parent groups can only be deleted on a delay in GitLab 16
                # https://docs.gitlab.com/ee/api/groups.html#remove-group
                object.delete()
        except gitlab.exceptions.GitlabDeleteError:
            logging.exception(f"Error attempting to delete: {object.pformat()}")

        time.sleep(SLEEP_INTERVAL)
    pytest.fail(f"{object!r} was not deleted")

import logging
import time
from typing import Optional

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
        return

    return license["plan"]


def safe_delete(
    object: gitlab.base.RESTObject,
    *,
    hard_delete: bool = False,
) -> None:
    """Ensure the object specified can not be retrieved. If object still exists after
    timeout period, fail the test"""
    manager = object.manager
    for index in range(MAX_ITERATIONS):
        try:
            object = manager.get(object.get_id())
        except gitlab.exceptions.GitlabGetError:
            return

        if index:
            logging.info(f"Attempt {index+1} to delete {object!r}.")
        try:
            if hard_delete:
                object.delete(hard_delete=True)
            else:
                object.delete()
        except gitlab.exceptions.GitlabDeleteError:
            logging.info(f"{object!r} already deleted.")
            pass

        time.sleep(SLEEP_INTERVAL)
    pytest.fail(f"{object!r} was not deleted")

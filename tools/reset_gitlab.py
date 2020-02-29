#!/usr/bin/env python

import sys
import time

from gitlab import Gitlab


def main():
    with Gitlab.from_config(config_files=["/tmp/python-gitlab.cfg"]) as gl:
        for project in gl.projects.list(all=True):
            project.delete()
        for group in gl.groups.list(all=True):
            group.delete()

        # Gitlab needs time to delete resources; avoid 409 on user deletion
        while gl.projects.list(all=True) or gl.groups.list(all=True):
            time.sleep(0.1)

        for user in gl.users.list():
            if user.username != "root":
                user.delete(hard_delete=True)


if __name__ == "__main__":
    sys.exit(main())

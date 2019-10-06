#!/usr/bin/env python

import sys

from gitlab import Gitlab


def main():
    with Gitlab.from_config(config_files=["/tmp/python-gitlab.cfg"]) as gl:
        for project in gl.projects.list():
            project.delete()
        for group in gl.groups.list():
            group.delete()
        for user in gl.users.list():
            if user.username != "root":
                user.delete()


if __name__ == "__main__":
    sys.exit(main())

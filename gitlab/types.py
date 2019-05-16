# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 Gauvain Pocentek <gauvain@pocentek.net>
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


class GitlabAttribute(object):
    def __init__(self, value=None):
        self._value = value

    def get(self):
        return self._value

    def set_from_cli(self, cli_value):
        self._value = cli_value

    def get_for_api(self):
        return self._value


class ListAttribute(GitlabAttribute):
    def set_from_cli(self, cli_value):
        if not cli_value.strip():
            self._value = []
        else:
            self._value = [item.strip() for item in cli_value.split(",")]

    def get_for_api(self):
        return ",".join(self._value)


class LowercaseStringAttribute(GitlabAttribute):
    def get_for_api(self):
        return str(self._value).lower()


class FileAttribute(GitlabAttribute):
    def get_file_name(self, attr_name=None):
        return attr_name


class ImageAttribute(FileAttribute):
    def get_file_name(self, attr_name=None):
        return "%s.png" % attr_name if attr_name else "image.png"

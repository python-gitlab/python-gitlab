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

from typing import Any, Optional, TYPE_CHECKING


class GitlabAttribute:
    def __init__(self, value: Any = None) -> None:
        self._value = value

    def get(self) -> Any:
        return self._value

    def set_from_cli(self, cli_value: Any) -> None:
        self._value = cli_value

    def get_for_api(self) -> Any:
        return self._value


class ListAttribute(GitlabAttribute):
    def set_from_cli(self, cli_value: str) -> None:
        if not cli_value.strip():
            self._value = []
        else:
            self._value = [item.strip() for item in cli_value.split(",")]

    def get_for_api(self) -> str:
        # Do not comma-split single value passed as string
        if isinstance(self._value, str):
            return self._value

        if TYPE_CHECKING:
            assert isinstance(self._value, list)
        return ",".join([str(x) for x in self._value])


class LowercaseStringAttribute(GitlabAttribute):
    def get_for_api(self) -> str:
        return str(self._value).lower()


class FileAttribute(GitlabAttribute):
    def get_file_name(self, attr_name: Optional[str] = None) -> Optional[str]:
        return attr_name


class ImageAttribute(FileAttribute):
    def get_file_name(self, attr_name: Optional[str] = None) -> str:
        return f"{attr_name}.png" if attr_name else "image.png"

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


class GitlabAttribute:
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


class GitlabList:
    """Generator representing a list of remote objects.

    The object handles the links returned by a query to the API, and will call
    the API again when needed.
    """

    @property
    def current_page(self):
        """The current page number."""
        return int(self._current_page)

    @property
    def prev_page(self):
        """The next page number.

        If None, the current page is the last.
        """
        return int(self._prev_page) if self._prev_page else None

    @property
    def next_page(self):
        """The next page number.

        If None, the current page is the last.
        """
        return int(self._next_page) if self._next_page else None

    @property
    def per_page(self):
        """The number of items per page."""
        return int(self._per_page)

    @property
    def total_pages(self):
        """The total number of pages."""
        return int(self._total_pages)

    @property
    def total(self):
        """The total number of items."""
        return int(self._total)

    def __len__(self):
        return int(self._total)


class GitlabList:
    """Generator representing a list of remote objects.

    The object handles the links returned by a query to the API, and will call
    the API again when needed.
    """

    @classmethod
    def create(cls, gl, url, query_data, get_next=True, **kwargs):
        self = GitlabList()
        self._gl = gl
        self._query(url, query_data, **kwargs)
        self._get_next = get_next
        return self

    @classmethod
    async def acreate(cls, gl, url, query_data, get_next=True, **kwargs):
        """Create GitlabList with data

        Create is made in factory way since it's cleaner to use such way
        instead of make async __init__
        """
        self = GitlabList()
        self._gl = gl
        await self._aquery(url, query_data, **kwargs)
        self._get_next = get_next
        return self

    def _process_query_result(self, result):
        try:
            self._next_url = result.links["next"]["url"]
        except KeyError:
            self._next_url = None
        self._current_page = result.headers.get("X-Page")
        self._prev_page = result.headers.get("X-Prev-Page")
        self._next_page = result.headers.get("X-Next-Page")
        self._per_page = result.headers.get("X-Per-Page")
        self._total_pages = result.headers.get("X-Total-Pages")
        self._total = result.headers.get("X-Total")

        try:
            self._data = result.json()
        except Exception:
            raise GitlabParsingError(error_message="Failed to parse the server message")

        self._current = 0

    async def _aquery(self, url, query_data=None, **kwargs):
        query_data = query_data or {}
        result = await self._gl.http_request(
            "get", url, query_data=query_data, **kwargs
        )
        self._process_query_result(result)

    def _query(self, url, query_data=None, **kwargs):
        query_data = query_data or {}
        result = self._gl.http_request("get", url, query_data=query_data, **kwargs)
        return self._process_query_result(result)

    def __iter__(self):
        return self

    def __next__(self):
        return self.next()

    def next(self):
        try:
            item = self._data[self._current]
            self._current += 1
            return item
        except IndexError:
            pass

        if self._next_url and self._get_next is True:
            self._query(self._next_url)
            return self.next()

        raise StopIteration

    def __aiter__(self):
        return self

    async def __anext__(self):
        return await self.anext()

    async def anext(self):
        try:
            item = self._data[self._current]
            self._current += 1
            return item
        except IndexError:
            pass

        if self._next_url and self._get_next is True:
            await self._aquery(self._next_url)
            return await self.anext()

        raise StopAsyncIteration

    async def as_list(self):
        # since list() does not support async way
        return [o async for o in self]

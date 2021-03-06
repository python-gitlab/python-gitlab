# -*- coding: utf-8 -*-
#
# Copyright (C) 2016-2017 Gauvain Pocentek <gauvain@pocentek.net>
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

from typing import Any, Callable, Dict, Optional
from urllib.parse import urlparse

import requests


class _StdoutStream(object):
    def __call__(self, chunk: Any) -> None:
        print(chunk)


def response_content(
    response: requests.Response,
    streamed: bool,
    action: Optional[Callable],
    chunk_size: int,
) -> Optional[bytes]:
    if streamed is False:
        return response.content

    if action is None:
        action = _StdoutStream()

    for chunk in response.iter_content(chunk_size=chunk_size):
        if chunk:
            action(chunk)
    return None


def copy_dict(dest: Dict[str, Any], src: Dict[str, Any]) -> None:
    for k, v in src.items():
        if isinstance(v, dict):
            # Transform dict values to new attributes. For example:
            # custom_attributes: {'foo', 'bar'} =>
            #   "custom_attributes['foo']": "bar"
            for dict_k, dict_v in v.items():
                dest["%s[%s]" % (k, dict_k)] = dict_v
        else:
            dest[k] = v


def clean_str_id(id: str) -> str:
    return id.replace("/", "%2F").replace("#", "%23")


def sanitize_parameters(value):
    if isinstance(value, dict):
        return dict((k, sanitize_parameters(v)) for k, v in value.items())
    if isinstance(value, str):
        return value.replace("/", "%2F")
    return value


def sanitized_url(url: str) -> str:
    parsed = urlparse(url)
    new_path = parsed.path.replace(".", "%2E")
    return parsed._replace(path=new_path).geturl()


def remove_none_from_dict(data: Dict[str, Any]) -> Dict[str, Any]:
    return {k: v for k, v in data.items() if v is not None}

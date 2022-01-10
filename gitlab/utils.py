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

import urllib.parse
from typing import Any, Callable, Dict, Optional, overload, Union

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
                dest[f"{k}[{dict_k}]"] = dict_v
        else:
            dest[k] = v


@overload
def _url_encode(id: int) -> int:
    ...


@overload
def _url_encode(id: str) -> str:
    ...


def _url_encode(id: Union[int, str]) -> Union[int, str]:
    """Encode/quote the characters in the string so that they can be used in a path.

    Reference to documentation on why this is necessary.

    https://docs.gitlab.com/ee/api/index.html#namespaced-path-encoding

    If using namespaced API requests, make sure that the NAMESPACE/PROJECT_PATH is
    URL-encoded. For example, / is represented by %2F

    https://docs.gitlab.com/ee/api/index.html#path-parameters

    Path parameters that are required to be URL-encoded must be followed. If not, it
    doesn’t match an API endpoint and responds with a 404. If there’s something in front
    of the API (for example, Apache), ensure that it doesn’t decode the URL-encoded path
    parameters.

    """
    if isinstance(id, int):
        return id
    return urllib.parse.quote(id, safe="")


def remove_none_from_dict(data: Dict[str, Any]) -> Dict[str, Any]:
    return {k: v for k, v in data.items() if v is not None}

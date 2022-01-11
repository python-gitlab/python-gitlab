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


class EncodedId(str):
    """A custom `str` class that will return the URL-encoded value of the string.

      * Using it recursively will only url-encode the value once.
      * Can accept either `str` or `int` as input value.
      * Can be used in an f-string and output the URL-encoded string.

    Reference to documentation on why this is necessary.

    See::

        https://docs.gitlab.com/ee/api/index.html#namespaced-path-encoding
        https://docs.gitlab.com/ee/api/index.html#path-parameters
    """

    # `original_str` will contain the original string value that was used to create the
    # first instance of EncodedId. We will use this original value to generate the
    # URL-encoded value each time.
    original_str: str

    def __new__(cls, value: Union[str, int, "EncodedId"]) -> "EncodedId":
        # __new__() gets called before __init__()
        if isinstance(value, int):
            value = str(value)
        # Make sure isinstance() for `EncodedId` comes before check for `str` as
        # `EncodedId` is an instance of `str` and would pass that check.
        elif isinstance(value, EncodedId):
            # We use the original string value to URL-encode
            value = value.original_str
        elif isinstance(value, str):
            pass
        else:
            raise ValueError(f"Unsupported type received: {type(value)}")
        # Set the value our string will return
        value = urllib.parse.quote(value, safe="")
        return super().__new__(cls, value)

    def __init__(self, value: Union[int, str]) -> None:
        # At this point `super().__str__()` returns the URL-encoded value. Which means
        # when using this as a `str` it will return the URL-encoded value.
        #
        # But `value` contains the original value passed in `EncodedId(value)`. We use
        # this to always keep the original string that was received so that no matter
        # how many times we recurse we only URL-encode our original string once.
        if isinstance(value, int):
            value = str(value)
        # Make sure isinstance() for `EncodedId` comes before check for `str` as
        # `EncodedId` is an instance of `str` and would pass that check.
        elif isinstance(value, EncodedId):
            # This is the key part as we are always keeping the original string even
            # through multiple recursions.
            value = value.original_str
        elif isinstance(value, str):
            pass
        else:
            raise ValueError(f"Unsupported type received: {type(value)}")
        self.original_str = value
        super().__init__()


@overload
def _url_encode(id: int) -> int:
    ...


@overload
def _url_encode(id: Union[str, EncodedId]) -> EncodedId:
    ...


def _url_encode(id: Union[int, str, EncodedId]) -> Union[int, EncodedId]:
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
    if isinstance(id, (int, EncodedId)):
        return id
    return EncodedId(id)


def remove_none_from_dict(data: Dict[str, Any]) -> Dict[str, Any]:
    return {k: v for k, v in data.items() if v is not None}

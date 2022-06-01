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

import pathlib
import traceback
import urllib.parse
import warnings
from typing import Any, Callable, Dict, List, Optional, Tuple, Type, Union

import requests

from gitlab import types


class _StdoutStream:
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


def _transform_types(
    data: Dict[str, Any], custom_types: dict, *, transform_files: Optional[bool] = True
) -> Tuple[dict, dict]:
    """Copy the data dict with attributes that have custom types and transform them
    before being sent to the server.

    If ``transform_files`` is ``True`` (default), also populates the ``files`` dict for
    FileAttribute types with tuples to prepare fields for requests' MultipartEncoder:
    https://toolbelt.readthedocs.io/en/latest/user.html#multipart-form-data-encoder

    Returns:
        A tuple of the transformed data dict and files dict"""

    # Duplicate data to avoid messing with what the user sent us
    data = data.copy()
    files = {}

    for attr_name, type_cls in custom_types.items():
        if attr_name not in data:
            continue

        type_obj = type_cls(data[attr_name])

        # if the type if FileAttribute we need to pass the data as file
        if transform_files and isinstance(type_obj, types.FileAttribute):
            key = type_obj.get_file_name(attr_name)
            files[attr_name] = (key, data.pop(attr_name))
        else:
            data[attr_name] = type_obj.get_for_api()

    return data, files


def copy_dict(
    *,
    src: Dict[str, Any],
    dest: Dict[str, Any],
) -> None:
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

    def __new__(cls, value: Union[str, int, "EncodedId"]) -> "EncodedId":
        if isinstance(value, EncodedId):
            return value

        if not isinstance(value, (int, str)):
            raise TypeError(f"Unsupported type received: {type(value)}")
        if isinstance(value, str):
            value = urllib.parse.quote(value, safe="")
        return super().__new__(cls, value)


def remove_none_from_dict(data: Dict[str, Any]) -> Dict[str, Any]:
    return {k: v for k, v in data.items() if v is not None}


def warn(
    message: str,
    *,
    category: Optional[Type] = None,
    source: Optional[Any] = None,
) -> None:
    """This `warnings.warn` wrapper function attempts to show the location causing the
    warning in the user code that called the library.

    It does this by walking up the stack trace to find the first frame located outside
    the `gitlab/` directory. This is helpful to users as it shows them their code that
    is causing the warning.
    """
    # Get `stacklevel` for user code so we indicate where issue is in
    # their code.
    pg_dir = pathlib.Path(__file__).parent.resolve()
    stack = traceback.extract_stack()
    stacklevel = 1
    warning_from = ""
    for stacklevel, frame in enumerate(reversed(stack), start=1):
        if stacklevel == 2:
            warning_from = f" (python-gitlab: {frame.filename}:{frame.lineno})"
        frame_dir = str(pathlib.Path(frame.filename).parent.resolve())
        if not frame_dir.startswith(str(pg_dir)):
            break
    warnings.warn(
        message=message + warning_from,
        category=category,
        stacklevel=stacklevel,
        source=source,
    )


def _validate_attrs(
    data: Dict[str, Any],
    attributes: types.RequiredOptional,
    excludes: Optional[List[str]] = None,
) -> None:
    if excludes is None:
        excludes = []

    if attributes.required:
        required = [k for k in attributes.required if k not in excludes]
        missing = [attr for attr in required if attr not in data]
        if missing:
            raise AttributeError(f"Missing attributes: {', '.join(missing)}")

    if attributes.exclusive:
        exclusives = [attr for attr in data if attr in attributes.exclusive]
        if len(exclusives) > 1:
            raise AttributeError(
                f"Provide only one of these attributes: {', '.join(exclusives)}"
            )
        if not exclusives:
            raise AttributeError(
                f"Must provide one of these attributes: "
                f"{', '.join(attributes.exclusive)}"
            )

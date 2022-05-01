import email.message
import logging
import pathlib
import traceback
import urllib.parse
import warnings
from typing import Any, Callable, Dict, Iterator, Literal, Optional, Tuple, Type, Union

import requests

from gitlab import types


class _StdoutStream:
    def __call__(self, chunk: Any) -> None:
        print(chunk)


def get_content_type(content_type: Optional[str]) -> str:
    message = email.message.Message()
    message["content-type"] = content_type

    return message.get_content_type()


class MaskingFormatter(logging.Formatter):
    """A logging formatter that can mask credentials"""

    def __init__(
        self,
        fmt: Optional[str] = logging.BASIC_FORMAT,
        datefmt: Optional[str] = None,
        style: Literal["%", "{", "$"] = "%",
        validate: bool = True,
        masked: Optional[str] = None,
    ) -> None:
        super().__init__(fmt, datefmt, style, validate)
        self.masked = masked

    def _filter(self, entry: str) -> str:
        if not self.masked:
            return entry

        return entry.replace(self.masked, "[MASKED]")

    def format(self, record: logging.LogRecord) -> str:
        original = logging.Formatter.format(self, record)
        return self._filter(original)


def response_content(
    response: requests.Response,
    streamed: bool,
    action: Optional[Callable[[bytes], None]],
    chunk_size: int,
    *,
    iterator: bool,
) -> Optional[Union[bytes, Iterator[Any]]]:
    if iterator:
        return response.iter_content(chunk_size=chunk_size)

    if streamed is False:
        return response.content

    if action is None:
        action = _StdoutStream()

    for chunk in response.iter_content(chunk_size=chunk_size):
        if chunk:
            action(chunk)
    return None


def _transform_types(
    data: Dict[str, Any],
    custom_types: Dict[str, Any],
    *,
    transform_data: bool,
    transform_files: Optional[bool] = True,
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """Copy the data dict with attributes that have custom types and transform them
    before being sent to the server.

    ``transform_files``: If ``True`` (default), also populates the ``files`` dict for
    FileAttribute types with tuples to prepare fields for requests' MultipartEncoder:
    https://toolbelt.readthedocs.io/en/latest/user.html#multipart-form-data-encoder

    ``transform_data``: If ``True`` transforms the ``data`` dict with fields
    suitable for encoding as query parameters for GitLab's API:
    https://docs.gitlab.com/ee/api/#encoding-api-parameters-of-array-and-hash-types

    Returns:
        A tuple of the transformed data dict and files dict"""

    # Duplicate data to avoid messing with what the user sent us
    data = data.copy()
    if not transform_files and not transform_data:
        return data, {}

    files = {}

    for attr_name, attr_class in custom_types.items():
        if attr_name not in data:
            continue

        gitlab_attribute = attr_class(data[attr_name])

        # if the type is FileAttribute we need to pass the data as file
        if isinstance(gitlab_attribute, types.FileAttribute) and transform_files:
            key = gitlab_attribute.get_file_name(attr_name)
            files[attr_name] = (key, data.pop(attr_name))
            continue

        if not transform_data:
            continue

        if isinstance(gitlab_attribute, types.GitlabAttribute):
            key, value = gitlab_attribute.get_for_api(key=attr_name)
            if key != attr_name:
                del data[attr_name]
            data[key] = value

    return data, files


def copy_dict(
    *,
    src: Dict[str, Any],
    dest: Dict[str, Any],
) -> None:
    for k, v in src.items():
        if isinstance(v, dict):
            # NOTE(jlvillal): This provides some support for the `hash` type
            # https://docs.gitlab.com/ee/api/#hash
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
    category: Optional[Type[Warning]] = None,
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

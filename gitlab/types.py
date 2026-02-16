from __future__ import annotations

import dataclasses
import json
from typing import Any, TYPE_CHECKING

from gitlab import exceptions


@dataclasses.dataclass(frozen=True)
class RequiredOptional:
    required: tuple[str, ...] = ()
    optional: tuple[str, ...] = ()
    exclusive: tuple[str, ...] = ()

    def validate_attrs(
        self, *, data: dict[str, Any], excludes: list[str] | None = None
    ) -> None:
        if excludes is None:
            excludes = []

        if self.required:
            required = [k for k in self.required if k not in excludes]
            missing = [attr for attr in required if attr not in data]
            if missing:
                raise AttributeError(f"Missing attributes: {', '.join(missing)}")

        if self.exclusive:
            exclusives = [attr for attr in data if attr in self.exclusive]
            if len(exclusives) > 1:
                raise AttributeError(
                    f"Provide only one of these attributes: {', '.join(exclusives)}"
                )
            if not exclusives:
                raise AttributeError(
                    f"Must provide one of these attributes: "
                    f"{', '.join(self.exclusive)}"
                )


class GitlabAttribute:
    # Used in utils._transform_types() to decide if we should call get_for_api()
    # on the attribute when transform_data is False (e.g. for POST/PUT/PATCH).
    #
    # This allows us to force transformation of data even when sending JSON bodies,
    # which is useful for types like CommaSeparatedStringAttribute.
    transform_in_body = False

    def __init__(self, value: Any = None) -> None:
        self._value = value

    def get(self) -> Any:
        return self._value

    def set_from_cli(self, cli_value: Any) -> None:
        self._value = cli_value

    def get_for_api(self, *, key: str) -> tuple[str, Any]:
        return (key, self._value)


class JsonAttribute(GitlabAttribute):
    def set_from_cli(self, cli_value: str) -> None:
        try:
            self._value = json.loads(cli_value)
        except (ValueError, TypeError) as e:
            raise exceptions.GitlabParsingError(
                f"Could not parse JSON data: {e}"
            ) from e


class _ListArrayAttribute(GitlabAttribute):
    """Helper class to support `list` / `array` types."""

    def set_from_cli(self, cli_value: str) -> None:
        if not cli_value.strip():
            self._value = []
        else:
            self._value = [item.strip() for item in cli_value.split(",")]

    def get_for_api(self, *, key: str) -> tuple[str, str]:
        # Do not comma-split single value passed as string
        if isinstance(self._value, str):
            return (key, self._value)

        if TYPE_CHECKING:
            assert isinstance(self._value, list)
        return (key, ",".join([str(x) for x in self._value]))


class ArrayAttribute(_ListArrayAttribute):
    """To support `array` types as documented in
    https://docs.gitlab.com/ee/api/#array"""

    def get_for_api(self, *, key: str) -> tuple[str, Any]:
        if isinstance(self._value, str):
            return (f"{key}[]", self._value)

        if TYPE_CHECKING:
            assert isinstance(self._value, list)
        return (f"{key}[]", self._value)


class CommaSeparatedListAttribute(_ListArrayAttribute):
    """
    For values which are sent to the server as a Comma Separated Values (CSV) string
    in query parameters (GET), but as a list/array in JSON bodies (POST/PUT).
    """


class CommaSeparatedStringAttribute(_ListArrayAttribute):
    """
    For values which are sent to the server as a Comma Separated Values (CSV) string.
    Unlike CommaSeparatedListAttribute, this type ensures the value is converted
    to a string even in JSON bodies (POST/PUT requests).
    """

    # Used in utils._transform_types() to ensure the value is converted to a string
    # via get_for_api() even when transform_data is False (e.g. for POST/PUT/PATCH).
    # This is needed because some APIs require a CSV string instead of a JSON array.
    transform_in_body = True


class LowercaseStringAttribute(GitlabAttribute):
    def get_for_api(self, *, key: str) -> tuple[str, str]:
        return (key, str(self._value).lower())


class FileAttribute(GitlabAttribute):
    @staticmethod
    def get_file_name(attr_name: str | None = None) -> str | None:
        return attr_name


class ImageAttribute(FileAttribute):
    @staticmethod
    def get_file_name(attr_name: str | None = None) -> str:
        return f"{attr_name}.png" if attr_name else "image.png"

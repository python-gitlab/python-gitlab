import dataclasses
from typing import Any, Dict, List, Optional, Tuple, TYPE_CHECKING


@dataclasses.dataclass(frozen=True)
class RequiredOptional:
    required: Tuple[str, ...] = ()
    optional: Tuple[str, ...] = ()
    exclusive: Tuple[str, ...] = ()

    def validate_attrs(
        self,
        *,
        data: Dict[str, Any],
        excludes: Optional[List[str]] = None,
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
    def __init__(self, value: Any = None) -> None:
        self._value = value

    def get(self) -> Any:
        return self._value

    def set_from_cli(self, cli_value: Any) -> None:
        self._value = cli_value

    def get_for_api(self, *, key: str) -> Tuple[str, Any]:
        return (key, self._value)


class _ListArrayAttribute(GitlabAttribute):
    """Helper class to support `list` / `array` types."""

    def set_from_cli(self, cli_value: str) -> None:
        if not cli_value.strip():
            self._value = []
        else:
            self._value = [item.strip() for item in cli_value.split(",")]

    def get_for_api(self, *, key: str) -> Tuple[str, str]:
        # Do not comma-split single value passed as string
        if isinstance(self._value, str):
            return (key, self._value)

        if TYPE_CHECKING:
            assert isinstance(self._value, list)
        return (key, ",".join([str(x) for x in self._value]))


class ArrayAttribute(_ListArrayAttribute):
    """To support `array` types as documented in
    https://docs.gitlab.com/ee/api/#array"""

    def get_for_api(self, *, key: str) -> Tuple[str, Any]:
        if isinstance(self._value, str):
            return (f"{key}[]", self._value)

        if TYPE_CHECKING:
            assert isinstance(self._value, list)
        return (f"{key}[]", self._value)


class CommaSeparatedListAttribute(_ListArrayAttribute):
    """For values which are sent to the server as a Comma Separated Values
    (CSV) string.  We allow them to be specified as a list and we convert it
    into a CSV"""


class LowercaseStringAttribute(GitlabAttribute):
    def get_for_api(self, *, key: str) -> Tuple[str, str]:
        return (key, str(self._value).lower())


class FileAttribute(GitlabAttribute):
    @staticmethod
    def get_file_name(attr_name: Optional[str] = None) -> Optional[str]:
        return attr_name


class ImageAttribute(FileAttribute):
    @staticmethod
    def get_file_name(attr_name: Optional[str] = None) -> str:
        return f"{attr_name}.png" if attr_name else "image.png"

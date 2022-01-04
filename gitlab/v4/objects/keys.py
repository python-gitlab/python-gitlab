from typing import Any, cast, Optional, TYPE_CHECKING, Union

from ...base import RESTManager, RESTObject
from ...mixins import GetMixin

__all__ = [
    "Key",
    "KeyManager",
]


class Key(RESTObject):
    pass


class KeyManager(GetMixin, RESTManager):
    _path = "/keys"
    _obj_cls = Key

    def get(
        self, id: Optional[Union[int, str]] = None, lazy: bool = False, **kwargs: Any
    ) -> Key:
        if id is not None:
            return cast(Key, super(KeyManager, self).get(id, lazy=lazy, **kwargs))

        if "fingerprint" not in kwargs:
            raise AttributeError("Missing attribute: id or fingerprint")

        if TYPE_CHECKING:
            assert self.path is not None
        server_data = self.gitlab.http_get(self.path, **kwargs)
        if TYPE_CHECKING:
            assert isinstance(server_data, dict)
        return self._obj_cls(self, server_data)

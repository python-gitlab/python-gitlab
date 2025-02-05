from __future__ import annotations

from typing import Any, TYPE_CHECKING

from gitlab.base import RESTObject
from gitlab.mixins import GetMixin

__all__ = ["Key", "KeyManager"]


class Key(RESTObject):
    pass


class KeyManager(GetMixin[Key]):
    _path = "/keys"
    _obj_cls = Key

    def get(
        self, id: int | str | None = None, lazy: bool = False, **kwargs: Any
    ) -> Key:
        if id is not None:
            return super().get(id, lazy=lazy, **kwargs)

        if "fingerprint" not in kwargs:
            raise AttributeError("Missing attribute: id or fingerprint")

        server_data = self.gitlab.http_get(self.path, **kwargs)
        if TYPE_CHECKING:
            assert isinstance(server_data, dict)
        return self._obj_cls(self, server_data)

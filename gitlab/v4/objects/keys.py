from gitlab.base import RESTManager, RESTObject
from gitlab.mixins import GetMixin

__all__ = [
    "Key",
    "KeyManager",
]


class Key(RESTObject):
    pass


class KeyManager(GetMixin, RESTManager):
    _path = "/keys"
    _obj_cls = Key

    def get(self, id=None, **kwargs):
        if id is not None:
            return super(KeyManager, self).get(id, **kwargs)

        if "fingerprint" not in kwargs:
            raise AttributeError("Missing attribute: id or fingerprint")

        server_data = self.gitlab.http_get(self.path, **kwargs)
        return self._obj_cls(self, server_data)

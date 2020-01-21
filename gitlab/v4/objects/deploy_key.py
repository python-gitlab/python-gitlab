from gitlab.base import *  # noqa
from gitlab.exceptions import *  # noqa
from gitlab.mixins import *  # noqa
from gitlab import types
from gitlab import utils


class DeployKey(RESTObject):
    pass


class DeployKeyManager(ListMixin, RESTManager):
    _path = "/deploy_keys"
    _obj_cls = DeployKey

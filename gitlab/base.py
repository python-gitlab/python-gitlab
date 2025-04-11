from __future__ import annotations

import copy
import importlib
import json
import pprint
import textwrap
from collections.abc import Iterable
from types import ModuleType
from typing import Any, ClassVar, Generic, TYPE_CHECKING, TypeVar

import gitlab
from gitlab import types as g_types
from gitlab.exceptions import GitlabParsingError

from .client import Gitlab, GitlabList

__all__ = ["RESTObject", "RESTObjectList", "RESTManager"]


_URL_ATTRIBUTE_ERROR = (
    f"https://python-gitlab.readthedocs.io/en/v{gitlab.__version__}/"
    f"faq.html#attribute-error-list"
)


class RESTObject:
    """Represents an object built from server data.

    It holds the attributes know from the server, and the updated attributes in
    another. This allows smart updates, if the object allows it.

    You can redefine ``_id_attr`` in child classes to specify which attribute
    must be used as the unique ID. ``None`` means that the object can be updated
    without ID in the url.

    Likewise, you can define a ``_repr_attr`` in subclasses to specify which
    attribute should be added as a human-readable identifier when called in the
    object's ``__repr__()`` method.
    """

    _id_attr: str | None = "id"
    _attrs: dict[str, Any]
    _created_from_list: bool  # Indicates if object was created from a list() action
    _module: ModuleType
    _parent_attrs: dict[str, Any]
    _repr_attr: str | None = None
    _updated_attrs: dict[str, Any]
    _lazy: bool
    manager: RESTManager[Any]

    def __init__(
        self,
        manager: RESTManager[Any],
        attrs: dict[str, Any],
        *,
        created_from_list: bool = False,
        lazy: bool = False,
    ) -> None:
        if not isinstance(attrs, dict):
            raise GitlabParsingError(
                f"Attempted to initialize RESTObject with a non-dictionary value: "
                f"{attrs!r}\nThis likely indicates an incorrect or malformed server "
                f"response."
            )
        self.__dict__.update(
            {
                "manager": manager,
                "_attrs": attrs,
                "_updated_attrs": {},
                "_module": importlib.import_module(self.__module__),
                "_created_from_list": created_from_list,
                "_lazy": lazy,
            }
        )
        self.__dict__["_parent_attrs"] = self.manager.parent_attrs
        self._create_managers()

    def __getstate__(self) -> dict[str, Any]:
        state = self.__dict__.copy()
        module = state.pop("_module")
        state["_module_name"] = module.__name__
        return state

    def __setstate__(self, state: dict[str, Any]) -> None:
        module_name = state.pop("_module_name")
        self.__dict__.update(state)
        self.__dict__["_module"] = importlib.import_module(module_name)

    def __getattr__(self, name: str) -> Any:
        if name in self.__dict__["_updated_attrs"]:
            return self.__dict__["_updated_attrs"][name]

        if name in self.__dict__["_attrs"]:
            value = self.__dict__["_attrs"][name]
            # If the value is a list, we copy it in the _updated_attrs dict
            # because we are not able to detect changes made on the object
            # (append, insert, pop, ...). Without forcing the attr
            # creation __setattr__ is never called, the list never ends up
            # in the _updated_attrs dict, and the update() and save()
            # method never push the new data to the server.
            # See https://github.com/python-gitlab/python-gitlab/issues/306
            #
            # note: _parent_attrs will only store simple values (int) so we
            # don't make this check in the next block.
            if isinstance(value, list):
                self.__dict__["_updated_attrs"][name] = value[:]
                return self.__dict__["_updated_attrs"][name]

            return value

        if name in self.__dict__["_parent_attrs"]:
            return self.__dict__["_parent_attrs"][name]

        message = f"{type(self).__name__!r} object has no attribute {name!r}"
        if self._created_from_list:
            message = (
                f"{message}\n\n"
                + textwrap.fill(
                    f"{self.__class__!r} was created via a list() call and "
                    f"only a subset of the data may be present. To ensure "
                    f"all data is present get the object using a "
                    f"get(object.id) call. For more details, see:"
                )
                + f"\n\n{_URL_ATTRIBUTE_ERROR}"
            )
        elif self._lazy:
            message = f"{message}\n\n" + textwrap.fill(
                f"If you tried to access object attributes returned from the server, "
                f"note that {self.__class__!r} was created as a `lazy` object and was "
                f"not initialized with any data."
            )
        raise AttributeError(message)

    def __setattr__(self, name: str, value: Any) -> None:
        self.__dict__["_updated_attrs"][name] = value

    def asdict(self, *, with_parent_attrs: bool = False) -> dict[str, Any]:
        data = {}
        if with_parent_attrs:
            data.update(copy.deepcopy(self._parent_attrs))
        data.update(copy.deepcopy(self._attrs))
        data.update(copy.deepcopy(self._updated_attrs))
        return data

    @property
    def attributes(self) -> dict[str, Any]:
        return self.asdict(with_parent_attrs=True)

    def to_json(self, *, with_parent_attrs: bool = False, **kwargs: Any) -> str:
        return json.dumps(self.asdict(with_parent_attrs=with_parent_attrs), **kwargs)

    def __str__(self) -> str:
        return f"{type(self)} => {self.asdict()}"

    def pformat(self) -> str:
        return f"{type(self)} => \n{pprint.pformat(self.asdict())}"

    def pprint(self) -> None:
        print(self.pformat())

    def __repr__(self) -> str:
        name = self.__class__.__name__

        if (self._id_attr and self._repr_value) and (self._id_attr != self._repr_attr):
            return (
                f"<{name} {self._id_attr}:{self.get_id()} "
                f"{self._repr_attr}:{self._repr_value}>"
            )
        if self._id_attr:
            return f"<{name} {self._id_attr}:{self.get_id()}>"
        if self._repr_value:
            return f"<{name} {self._repr_attr}:{self._repr_value}>"

        return f"<{name}>"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, RESTObject):
            return NotImplemented
        if self.get_id() and other.get_id():
            return self.get_id() == other.get_id()
        return super() == other

    def __ne__(self, other: object) -> bool:
        if not isinstance(other, RESTObject):
            return NotImplemented
        if self.get_id() and other.get_id():
            return self.get_id() != other.get_id()
        return super() != other

    def __dir__(self) -> Iterable[str]:
        return set(self.attributes).union(super().__dir__())

    def __hash__(self) -> int:
        if not self.get_id():
            return super().__hash__()
        return hash(self.get_id())

    def _create_managers(self) -> None:
        # NOTE(jlvillal): We are creating our managers by looking at the class
        # annotations. If an attribute is annotated as being a *Manager type
        # then we create the manager and assign it to the attribute.
        for attr, annotation in sorted(self.__class__.__annotations__.items()):
            # We ignore creating a manager for the 'manager' attribute as that
            # is done in the self.__init__() method
            if attr in ("manager",):
                continue
            if not isinstance(annotation, (type, str)):  # pragma: no cover
                continue
            if isinstance(annotation, type):
                cls_name = annotation.__name__
            else:
                cls_name = annotation
            # All *Manager classes are used except for the base "RESTManager" class
            if cls_name == "RESTManager" or not cls_name.endswith("Manager"):
                continue
            cls = getattr(self._module, cls_name)
            manager = cls(self.manager.gitlab, parent=self)
            # Since we have our own __setattr__ method, we can't use setattr()
            self.__dict__[attr] = manager

    def _update_attrs(self, new_attrs: dict[str, Any]) -> None:
        self.__dict__["_updated_attrs"] = {}
        self.__dict__["_attrs"] = new_attrs

    def get_id(self) -> int | str | None:
        """Returns the id of the resource."""
        if self._id_attr is None or not hasattr(self, self._id_attr):
            return None
        id_val = getattr(self, self._id_attr)
        if TYPE_CHECKING:
            assert id_val is None or isinstance(id_val, (int, str))
        return id_val

    @property
    def _repr_value(self) -> str | None:
        """Safely returns the human-readable resource name if present."""
        if self._repr_attr is None or not hasattr(self, self._repr_attr):
            return None
        repr_val = getattr(self, self._repr_attr)
        if TYPE_CHECKING:
            assert isinstance(repr_val, str)
        return repr_val

    @property
    def encoded_id(self) -> int | str | None:
        """Ensure that the ID is url-encoded so that it can be safely used in a URL
        path"""
        obj_id = self.get_id()
        if isinstance(obj_id, str):
            obj_id = gitlab.utils.EncodedId(obj_id)
        return obj_id


TObjCls = TypeVar("TObjCls", bound=RESTObject)


class RESTObjectList(Generic[TObjCls]):
    """Generator object representing a list of RESTObject's.

    This generator uses the Gitlab pagination system to fetch new data when
    required.

    Note: you should not instantiate such objects, they are returned by calls
    to RESTManager.list()

    Args:
        manager: Manager to attach to the created objects
        obj_cls: Type of objects to create from the json data
        _list: A GitlabList object
    """

    def __init__(
        self, manager: RESTManager[TObjCls], obj_cls: type[TObjCls], _list: GitlabList
    ) -> None:
        """Creates an objects list from a GitlabList.

        You should not create objects of this type, but use managers list()
        methods instead.

        Args:
            manager: the RESTManager to attach to the objects
            obj_cls: the class of the created objects
            _list: the GitlabList holding the data
        """
        self.manager = manager
        self._obj_cls = obj_cls
        self._list = _list

    def __iter__(self) -> RESTObjectList[TObjCls]:
        return self

    def __len__(self) -> int:
        return len(self._list)

    def __next__(self) -> TObjCls:
        return self.next()

    def next(self) -> TObjCls:
        data = self._list.next()
        return self._obj_cls(self.manager, data, created_from_list=True)

    @property
    def current_page(self) -> int:
        """The current page number."""
        return self._list.current_page

    @property
    def prev_page(self) -> int | None:
        """The previous page number.

        If None, the current page is the first.
        """
        return self._list.prev_page

    @property
    def next_page(self) -> int | None:
        """The next page number.

        If None, the current page is the last.
        """
        return self._list.next_page

    @property
    def per_page(self) -> int | None:
        """The number of items per page."""
        return self._list.per_page

    @property
    def total_pages(self) -> int | None:
        """The total number of pages."""
        return self._list.total_pages

    @property
    def total(self) -> int | None:
        """The total number of items."""
        return self._list.total


class RESTManager(Generic[TObjCls]):
    """Base class for CRUD operations on objects.

    Derived class must define ``_path`` and ``_obj_cls``.

    ``_path``: Base URL path on which requests will be sent (e.g. '/projects')
    ``_obj_cls``: The class of objects that will be created
    """

    _create_attrs: g_types.RequiredOptional = g_types.RequiredOptional()
    _update_attrs: g_types.RequiredOptional = g_types.RequiredOptional()
    _path: ClassVar[str]
    _obj_cls: type[TObjCls]
    _from_parent_attrs: dict[str, Any] = {}
    _types: dict[str, type[g_types.GitlabAttribute]] = {}

    _computed_path: str
    _parent: RESTObject | None
    _parent_attrs: dict[str, Any]
    gitlab: Gitlab

    def __init__(self, gl: Gitlab, parent: RESTObject | None = None) -> None:
        """REST manager constructor.

        Args:
            gl: :class:`~gitlab.Gitlab` connection to use to make requests.
            parent: REST object to which the manager is attached.
        """
        self.gitlab = gl
        self._parent = parent  # for nested managers
        self._computed_path = self._compute_path()

    @property
    def parent_attrs(self) -> dict[str, Any] | None:
        return self._parent_attrs

    def _compute_path(self, path: str | None = None) -> str:
        self._parent_attrs = {}
        if path is None:
            path = self._path
        if self._parent is None or not self._from_parent_attrs:
            return path

        data: dict[str, gitlab.utils.EncodedId | None] = {}
        for self_attr, parent_attr in self._from_parent_attrs.items():
            if not hasattr(self._parent, parent_attr):
                data[self_attr] = None
                continue
            data[self_attr] = gitlab.utils.EncodedId(getattr(self._parent, parent_attr))
        self._parent_attrs = data
        return path.format(**data)

    @property
    def path(self) -> str:
        return self._computed_path

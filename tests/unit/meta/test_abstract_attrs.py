"""
Ensure that RESTManager subclasses exported to gitlab.v4.objects
are defining the _path and _obj_cls attributes.

Only check using `hasattr` as if incorrect type is assigned the type
checker will raise an error.
"""

from __future__ import annotations

from inspect import getmembers

import gitlab.v4.objects
from gitlab.base import RESTManager


def test_rest_manager_abstract_attrs() -> None:
    without_path: list[str] = []
    without_obj_cls: list[str] = []

    for key, member in getmembers(gitlab.v4.objects):
        if not isinstance(member, type):
            continue

        if not issubclass(member, RESTManager):
            continue

        if not hasattr(member, "_path"):
            without_path.append(key)

        if not hasattr(member, "_obj_cls"):
            without_obj_cls.append(key)

    assert not without_path, (
        "RESTManager subclasses missing '_path' attribute: "
        f"{', '.join(without_path)}"
    )
    assert not without_obj_cls, (
        "RESTManager subclasses missing '_obj_cls' attribute: "
        f"{', '.join(without_obj_cls)}"
    )

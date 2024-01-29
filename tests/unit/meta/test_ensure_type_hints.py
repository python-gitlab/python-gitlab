"""
Ensure type-hints are setup correctly and detect if missing functions.

Original notes by John L. Villalovos

"""

import dataclasses
import functools
import inspect
from typing import Optional, Type

import pytest

import gitlab.mixins
import gitlab.v4.objects


@functools.total_ordering
@dataclasses.dataclass(frozen=True)
class ClassInfo:
    name: str
    type: Type  # type: ignore[type-arg]

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, ClassInfo):
            return NotImplemented
        return (self.type.__module__, self.name) < (other.type.__module__, other.name)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ClassInfo):
            return NotImplemented
        return (self.type.__module__, self.name) == (other.type.__module__, other.name)


def pytest_generate_tests(metafunc: pytest.Metafunc) -> None:
    """Find all of the classes in gitlab.v4.objects and pass them to our test
    function"""

    class_info_set = set()
    for _, module_value in inspect.getmembers(gitlab.v4.objects):
        if not inspect.ismodule(module_value):
            # We only care about the modules
            continue
        # Iterate through all the classes in our module
        for class_name, class_value in inspect.getmembers(module_value):
            if not inspect.isclass(class_value):
                continue

            module_name = class_value.__module__
            # Ignore imported classes from gitlab.base
            if module_name == "gitlab.base":
                continue

            if not class_name.endswith("Manager"):
                continue

            class_info_set.add(ClassInfo(name=class_name, type=class_value))

    metafunc.parametrize("class_info", sorted(class_info_set))


GET_ID_METHOD_TEMPLATE = """
def get(
    self, id: Union[str, int], lazy: bool = False, **kwargs: Any
) -> {obj_cls.__name__}:
    return cast({obj_cls.__name__}, super().get(id=id, lazy=lazy, **kwargs))

You may also need to add the following imports:
from typing import Any, cast, Union"
"""

GET_WITHOUT_ID_METHOD_TEMPLATE = """
def get(self, **kwargs: Any) -> {obj_cls.__name__}:
    return cast({obj_cls.__name__}, super().get(**kwargs))

You may also need to add the following imports:
from typing import Any, cast"
"""


class TestTypeHints:
    def test_check_get_function_type_hints(self, class_info: ClassInfo) -> None:
        """Ensure classes derived from GetMixin have defined a 'get()' method with
        correct type-hints.
        """
        self.get_check_helper(
            base_type=gitlab.mixins.GetMixin,
            class_info=class_info,
            method_template=GET_ID_METHOD_TEMPLATE,
            optional_return=False,
        )

    def test_check_get_without_id_function_type_hints(
        self, class_info: ClassInfo
    ) -> None:
        """Ensure classes derived from GetMixin have defined a 'get()' method with
        correct type-hints.
        """
        self.get_check_helper(
            base_type=gitlab.mixins.GetWithoutIdMixin,
            class_info=class_info,
            method_template=GET_WITHOUT_ID_METHOD_TEMPLATE,
            optional_return=False,
        )

    def get_check_helper(
        self,
        *,
        base_type: Type,  # type: ignore[type-arg]
        class_info: ClassInfo,
        method_template: str,
        optional_return: bool,
    ) -> None:
        if not class_info.name.endswith("Manager"):
            return
        mro = class_info.type.mro()
        # The class needs to be derived from GetMixin or we ignore it
        if base_type not in mro:
            return

        obj_cls = class_info.type._obj_cls
        signature = inspect.signature(class_info.type.get)
        filename = inspect.getfile(class_info.type)

        fail_message = (
            f"class definition for {class_info.name!r} in file {filename!r} "
            f"must have defined a 'get' method with a return annotation of "
            f"{obj_cls} but found {signature.return_annotation}\n"
            f"Recommend adding the following method:\n"
        )
        fail_message += method_template.format(obj_cls=obj_cls)
        check_type = obj_cls
        if optional_return:
            check_type = Optional[obj_cls]
        assert check_type == signature.return_annotation, fail_message

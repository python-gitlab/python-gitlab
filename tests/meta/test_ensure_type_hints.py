"""
Ensure type-hints are setup correctly and detect if missing functions.

Original notes by John L. Villalovos

"""
import inspect
from typing import Tuple, Type

import _pytest
import toml

import gitlab.mixins
import gitlab.v4.objects


def pytest_generate_tests(metafunc: _pytest.python.Metafunc) -> None:
    """Find all of the classes in gitlab.v4.objects and pass them to our test
    function"""

    # Ignore any modules that we are ignoring in our pyproject.toml
    excluded_modules = set()
    with open("pyproject.toml", "r") as in_file:
        pyproject = toml.load(in_file)
    overrides = pyproject.get("tool", {}).get("mypy", {}).get("overrides", [])
    for override in overrides:
        if not override.get("ignore_errors"):
            continue
        for module in override.get("module", []):
            if module.startswith("gitlab.v4.objects"):
                excluded_modules.add(module)

    class_info_list = []
    for module_name, module_value in inspect.getmembers(gitlab.v4.objects):
        if not inspect.ismodule(module_value):
            # We only care about the modules
            continue
        # Iterate through all the classes in our module
        for class_name, class_value in inspect.getmembers(module_value):
            if not inspect.isclass(class_value):
                continue

            module_name = class_value.__module__
            # Ignore modules that mypy is ignoring
            if module_name in excluded_modules:
                continue

            # Ignore imported classes from gitlab.base
            if module_name == "gitlab.base":
                continue

            class_info_list.append((class_name, class_value))

    metafunc.parametrize("class_info", class_info_list)


class TestTypeHints:
    def test_check_get_function_type_hints(self, class_info: Tuple[str, Type]) -> None:
        """Ensure classes derived from GetMixin have defined a 'get()' method with
        correct type-hints.
        """
        class_name, class_value = class_info
        if not class_name.endswith("Manager"):
            return

        mro = class_value.mro()
        # The class needs to be derived from GetMixin or we ignore it
        if gitlab.mixins.GetMixin not in mro:
            return

        obj_cls = class_value._obj_cls
        signature = inspect.signature(class_value.get)
        filename = inspect.getfile(class_value)

        fail_message = (
            f"class definition for {class_name!r} in file {filename!r} "
            f"must have defined a 'get' method with a return annotation of "
            f"{obj_cls} but found {signature.return_annotation}\n"
            f"Recommend adding the followinng method:\n"
            f"def get(\n"
            f"     self, id: Union[str, int], lazy: bool = False, **kwargs: Any\n"
            f" ) -> {obj_cls.__name__}:\n"
            f"     return cast({obj_cls.__name__}, super().get(id=id, lazy=lazy, "
            f"**kwargs))\n"
        )
        assert obj_cls == signature.return_annotation, fail_message

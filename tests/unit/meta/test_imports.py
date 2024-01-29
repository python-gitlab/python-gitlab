"""
Ensure objects defined in gitlab.v4.objects are imported in
`gitlab/v4/objects/__init__.py`

"""

import pkgutil
from typing import Set

import gitlab.exceptions
import gitlab.v4.objects


def test_all_exceptions_imports_are_exported() -> None:
    assert gitlab.exceptions.__all__ == sorted(
        [
            name
            for name in dir(gitlab.exceptions)
            if name.endswith("Error") and not name.startswith("_")
        ]
    )


def test_all_v4_objects_are_imported() -> None:
    assert len(gitlab.v4.objects.__path__) == 1

    init_files: Set[str] = set()
    with open(gitlab.v4.objects.__file__, "r", encoding="utf-8") as in_file:
        for line in in_file.readlines():
            if line.startswith("from ."):
                init_files.add(line.rstrip())

    object_files = set()
    for module in pkgutil.iter_modules(gitlab.v4.objects.__path__):
        object_files.add(f"from .{module.name} import *")

    missing_in_init = object_files - init_files
    error_message = (
        f"\nThe file {gitlab.v4.objects.__file__!r} is missing the following imports:"
    )
    for missing in sorted(missing_in_init):
        error_message += f"\n    {missing}"

    assert not missing_in_init, error_message

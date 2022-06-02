import importlib
import os
import sys

import pytest

import gitlab


def test__main__():
    # From Python 3 documentation on "Importing a source file directly"
    # https://docs.python.org/3/library/importlib.html#importing-a-source-file-directly
    main_py_path = os.path.join(
        os.path.abspath(os.path.dirname(gitlab.__file__)), "__main__.py"
    )
    # Make the `name` be `__main__` so the if condition will be met
    spec = importlib.util.spec_from_file_location(
        name="__main__", location=main_py_path
    )
    module = importlib.util.module_from_spec(spec=spec)
    sys.modules["gitlab.__main__"] = module
    with pytest.raises(SystemExit) as exc:
        spec.loader.exec_module(module)
    caught_exception = exc.value
    assert caught_exception.code == 2

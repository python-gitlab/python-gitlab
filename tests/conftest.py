import pathlib

import _pytest.config
import pytest


@pytest.fixture(scope="session")
def test_dir(pytestconfig: _pytest.config.Config) -> pathlib.Path:
    return pytestconfig.rootdir / "tests"  # type: ignore

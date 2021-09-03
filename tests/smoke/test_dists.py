import tarfile
import zipfile
from pathlib import Path
from sys import version_info

import pytest
from setuptools import sandbox

from gitlab import __title__, __version__

DIST_DIR = Path("dist")
TEST_DIR = "tests"
SDIST_FILE = f"{__title__}-{__version__}.tar.gz"
WHEEL_FILE = (
    f"{__title__.replace('-', '_')}-{__version__}-py{version_info.major}-none-any.whl"
)


@pytest.fixture(scope="function")
def build():
    sandbox.run_setup("setup.py", ["clean", "--all"])
    return sandbox.run_setup("setup.py", ["sdist", "bdist_wheel"])


def test_sdist_includes_tests(build):
    sdist = tarfile.open(DIST_DIR / SDIST_FILE, "r:gz")
    test_dir = sdist.getmember(f"{__title__}-{__version__}/{TEST_DIR}")
    assert test_dir.isdir()


def test_wheel_excludes_tests(build):
    wheel = zipfile.ZipFile(DIST_DIR / WHEEL_FILE)
    assert [not file.startswith(TEST_DIR) for file in wheel.namelist()]

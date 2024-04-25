import subprocess
import sys
import tarfile
import zipfile
from pathlib import Path

import pytest

from gitlab._version import __title__, __version__

DOCS_DIR = "docs"
TEST_DIR = "tests"
DIST_NORMALIZED_TITLE = f"{__title__.replace('-', '_')}-{__version__}"
SDIST_FILE = f"{DIST_NORMALIZED_TITLE}.tar.gz"
WHEEL_FILE = f"{DIST_NORMALIZED_TITLE}-py{sys.version_info.major}-none-any.whl"
PY_TYPED = "gitlab/py.typed"


@pytest.fixture(scope="session")
def build(tmp_path_factory: pytest.TempPathFactory):
    temp_dir = tmp_path_factory.mktemp("build")
    subprocess.run([sys.executable, "-m", "build", "--outdir", temp_dir], check=True)
    return temp_dir


def test_sdist_includes_correct_files(build: Path) -> None:
    sdist = tarfile.open(build / SDIST_FILE, "r:gz")

    docs_dir = sdist.getmember(f"{DIST_NORMALIZED_TITLE}/{DOCS_DIR}")
    test_dir = sdist.getmember(f"{DIST_NORMALIZED_TITLE}/{TEST_DIR}")
    readme = sdist.getmember(f"{DIST_NORMALIZED_TITLE}/README.rst")
    py_typed = sdist.getmember(f"{DIST_NORMALIZED_TITLE}/{PY_TYPED}")

    assert docs_dir.isdir()
    assert test_dir.isdir()
    assert py_typed.isfile()
    assert readme.isfile()


def test_wheel_includes_correct_files(build: Path) -> None:
    wheel = zipfile.ZipFile(build / WHEEL_FILE)
    assert PY_TYPED in wheel.namelist()


def test_wheel_excludes_docs_and_tests(build: Path) -> None:
    wheel = zipfile.ZipFile(build / WHEEL_FILE)
    assert not any(file.startswith((DOCS_DIR, TEST_DIR)) for file in wheel.namelist())

import tarfile
import zipfile
from pathlib import Path
from subprocess import CompletedProcess, run
from sys import executable, version_info

import pytest

from gitlab._version import __title__, __version__

DOCS_DIR = "docs"
TEST_DIR = "tests"
SDIST_FILE = f"{__title__}-{__version__}.tar.gz"
WHEEL_FILE = (
    f"{__title__.replace('-', '_')}-{__version__}-py{version_info.major}-none-any.whl"
)


@pytest.fixture(scope="function")
def build(tmpdir: Path):
    return run([executable, "-m", "build", "--outdir", str(tmpdir)], check=True)


def test_sdist_includes_tests(build: CompletedProcess, tmpdir: Path) -> None:
    sdist = tarfile.open(tmpdir / SDIST_FILE, "r:gz")
    test_dir = sdist.getmember(f"{__title__}-{__version__}/{TEST_DIR}")
    assert test_dir.isdir()


def test_wheel_excludes_docs_and_tests(build: CompletedProcess, tmpdir: Path) -> None:
    wheel = zipfile.ZipFile(tmpdir / WHEEL_FILE)
    assert not any(file.startswith((DOCS_DIR, TEST_DIR)) for file in wheel.namelist())

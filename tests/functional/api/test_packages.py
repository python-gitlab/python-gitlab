"""
GitLab API:
https://docs.gitlab.com/ce/api/packages.html
https://docs.gitlab.com/ee/user/packages/generic_packages
"""

from collections.abc import Iterator

import pytest

from gitlab import Gitlab
from gitlab.v4.objects import GenericPackage, Project, ProjectPackageProtectionRule

package_name = "hello-world"
package_version = "v1.0.0"
file_name = "hello.tar.gz"
file_name2 = "hello2.tar.gz"
file_content = "package content"


@pytest.fixture(scope="module", autouse=True)
def protected_package_feature(gl: Gitlab):
    gl.features.set(name="packages_protected_packages", value=True)


def test_list_project_packages(project):
    packages = project.packages.list()
    assert isinstance(packages, list)


def test_list_group_packages(group):
    packages = group.packages.list()
    assert isinstance(packages, list)


def test_upload_generic_package(tmp_path, project):
    path = tmp_path / file_name
    path.write_text(file_content)
    package = project.generic_packages.upload(
        package_name=package_name,
        package_version=package_version,
        file_name=file_name,
        path=path,
    )

    assert isinstance(package, GenericPackage)
    assert package.message == "201 Created"


def test_upload_generic_package_as_bytes(tmp_path, project):
    path = tmp_path / file_name

    path.write_text(file_content)

    package = project.generic_packages.upload(
        package_name=package_name,
        package_version=package_version,
        file_name=file_name,
        data=path.read_bytes(),
    )

    assert isinstance(package, GenericPackage)
    assert package.message == "201 Created"


def test_upload_generic_package_as_file(tmp_path, project):
    path = tmp_path / file_name

    path.write_text(file_content)

    package = project.generic_packages.upload(
        package_name=package_name,
        package_version=package_version,
        file_name=file_name,
        data=path.open(mode="rb"),
    )

    assert isinstance(package, GenericPackage)
    assert package.message == "201 Created"


def test_upload_generic_package_select(tmp_path, project):
    path = tmp_path / file_name2
    path.write_text(file_content)
    package = project.generic_packages.upload(
        package_name=package_name,
        package_version=package_version,
        file_name=file_name2,
        path=path,
        select="package_file",
    )

    assert isinstance(package, GenericPackage)
    assert package.file_name == file_name2
    assert package.size == path.stat().st_size


def test_download_generic_package(project):
    package = project.generic_packages.download(
        package_name=package_name,
        package_version=package_version,
        file_name=file_name,
    )

    assert isinstance(package, bytes)
    assert package.decode("utf-8") == file_content


def test_stream_generic_package(project):
    bytes_iterator = project.generic_packages.download(
        package_name=package_name,
        package_version=package_version,
        file_name=file_name,
        iterator=True,
    )

    assert isinstance(bytes_iterator, Iterator)

    package = bytes()
    for chunk in bytes_iterator:
        package += chunk

    assert isinstance(package, bytes)
    assert package.decode("utf-8") == file_content


def test_download_generic_package_to_file(tmp_path, project):
    path = tmp_path / file_name

    with open(path, "wb") as f:
        project.generic_packages.download(
            package_name=package_name,
            package_version=package_version,
            file_name=file_name,
            streamed=True,
            action=f.write,
        )

    with open(path, "r") as f:
        assert f.read() == file_content


def test_stream_generic_package_to_file(tmp_path, project):
    path = tmp_path / file_name

    bytes_iterator = project.generic_packages.download(
        package_name=package_name,
        package_version=package_version,
        file_name=file_name,
        iterator=True,
    )

    with open(path, "wb") as f:
        for chunk in bytes_iterator:
            f.write(chunk)

    with open(path, "r") as f:
        assert f.read() == file_content


def test_list_project_protected_packages(project: Project):
    rules = project.package_protection_rules.list()
    assert isinstance(rules, list)


@pytest.mark.skip(reason="Not released yet")
def test_create_project_protected_packages(project: Project):
    protected_package = project.package_protection_rules.create(
        {
            "package_name_pattern": "v*",
            "package_type": "npm",
            "minimum_access_level_for_push": "maintainer",
        }
    )
    assert isinstance(protected_package, ProjectPackageProtectionRule)
    assert protected_package.package_type == "npm"

    protected_package.minimum_access_level_for_push = "owner"
    protected_package.save()

    protected_package.delete()

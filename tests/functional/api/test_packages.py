"""
GitLab API:
https://docs.gitlab.com/ce/api/packages.html
https://docs.gitlab.com/ee/user/packages/generic_packages
"""
from gitlab.v4.objects import GenericPackage

package_name = "hello-world"
package_version = "v1.0.0"
file_name = "hello.tar.gz"
file_content = "package content"


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


def test_download_generic_package(project):
    package = project.generic_packages.download(
        package_name=package_name,
        package_version=package_version,
        file_name=file_name,
    )

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

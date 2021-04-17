package_name = "hello-world"
package_version = "v1.0.0"
file_name = "hello.tar.gz"
file_content = "package content"


def test_list_project_packages(gitlab_cli, project):
    cmd = ["project-package", "list", "--project-id", project.id]
    ret = gitlab_cli(cmd)

    assert ret.success


def test_list_group_packages(gitlab_cli, group):
    cmd = ["group-package", "list", "--group-id", group.id]
    ret = gitlab_cli(cmd)

    assert ret.success


def test_upload_generic_package(tmp_path, gitlab_cli, project):
    path = tmp_path / file_name
    path.write_text(file_content)

    cmd = [
        "-v",
        "generic-package",
        "upload",
        "--project-id",
        project.id,
        "--package-name",
        package_name,
        "--path",
        path,
        "--package-version",
        package_version,
        "--file-name",
        file_name,
    ]
    ret = gitlab_cli(cmd)

    assert "201 Created" in ret.stdout


def test_download_generic_package(gitlab_cli, project):
    cmd = [
        "generic-package",
        "download",
        "--project-id",
        project.id,
        "--package-name",
        package_name,
        "--package-version",
        package_version,
        "--file-name",
        file_name,
    ]
    ret = gitlab_cli(cmd)

    assert ret.stdout == file_content

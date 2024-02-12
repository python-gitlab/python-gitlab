import time

import pytest

import gitlab


# https://github.com/python-gitlab/python-gitlab/pull/2790#pullrequestreview-1873617123
def test_group_import_export(gl, group, temp_dir):
    export = group.exports.create()
    assert export.message == "202 Accepted"

    # We cannot check for export_status with group export API
    time.sleep(10)

    import_archive = temp_dir / "gitlab-group-export.tgz"
    import_path = "imported_group"
    import_name = "Imported Group"

    with open(import_archive, "wb") as f:
        export.download(streamed=True, action=f.write)

    with open(import_archive, "rb") as f:
        output = gl.groups.import_group(f, import_path, import_name)
    assert output["message"] == "202 Accepted"

    # We cannot check for returned ID with group import API
    time.sleep(10)
    group_import = gl.groups.get(import_path)

    assert group_import.path == import_path
    assert group_import.name == import_name


# https://github.com/python-gitlab/python-gitlab/pull/2790#pullrequestreview-1873617123
@pytest.mark.xfail(reason="test_project_import_export to be worked on in a follow up")
def test_project_import_export(gl, project, temp_dir):
    export = project.exports.create()
    assert export.message == "202 Accepted"

    export = project.exports.get()
    assert isinstance(export, gitlab.v4.objects.ProjectExport)

    count = 0
    while export.export_status != "finished":
        time.sleep(1)
        export.refresh()
        count += 1
        if count == 15:
            raise Exception("Project export taking too much time")

    with open(temp_dir / "gitlab-export.tgz", "wb") as f:
        export.download(streamed=True, action=f.write)  # type: ignore[arg-type]

    output = gl.projects.import_project(
        open(temp_dir / "gitlab-export.tgz", "rb"),
        "imported_project",
        name="Imported Project",
    )
    project_import = gl.projects.get(output["id"], lazy=True).imports.get()

    assert project_import.path == "imported_project"
    assert project_import.name == "Imported Project"

    count = 0
    while project_import.import_status != "finished":
        time.sleep(1)
        project_import.refresh()
        count += 1
        if count == 15:
            raise Exception("Project import taking too much time")


# https://github.com/python-gitlab/python-gitlab/pull/2790#pullrequestreview-1873617123
@pytest.mark.xfail(reason="test_project_remote_import to be worked on in a follow up")
def test_project_remote_import(gl):
    with pytest.raises(gitlab.exceptions.GitlabImportError) as err_info:
        gl.projects.remote_import(
            "ftp://whatever.com/url", "remote-project", "remote-project", "root"
        )
    assert err_info.value.response_code == 400
    assert (
        "File url is blocked: Only allowed schemes are https"
        in err_info.value.error_message
    )


# https://github.com/python-gitlab/python-gitlab/pull/2790#pullrequestreview-1873617123
@pytest.mark.xfail(
    reason="test_project_remote_import_s3 to be worked on in a follow up"
)
def test_project_remote_import_s3(gl):
    gl.features.set("import_project_from_remote_file_s3", True)
    with pytest.raises(gitlab.exceptions.GitlabImportError) as err_info:
        gl.projects.remote_import_s3(
            "remote-project",
            "aws-region",
            "aws-bucket-name",
            "aws-file-key",
            "aws-access-key-id",
            "secret-access-key",
            "remote-project",
            "root",
        )
    assert err_info.value.response_code == 400
    assert (
        "Failed to open 'aws-file-key' in 'aws-bucket-name'"
        in err_info.value.error_message
    )

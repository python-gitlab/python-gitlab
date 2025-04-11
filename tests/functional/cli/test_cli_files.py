def test_project_file_raw(gitlab_cli, project, project_file):
    cmd = ["project-file", "raw", "--project-id", project.id, "--file-path", "README"]
    ret = gitlab_cli(cmd)
    assert ret.success
    assert "Initial content" in ret.stdout


def test_project_file_raw_ref(gitlab_cli, project, project_file):
    cmd = [
        "project-file",
        "raw",
        "--project-id",
        project.id,
        "--file-path",
        "README",
        "--ref",
        "main",
    ]
    ret = gitlab_cli(cmd)
    assert ret.success
    assert "Initial content" in ret.stdout

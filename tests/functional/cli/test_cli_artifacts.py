import subprocess
import textwrap
import time
from io import BytesIO
from zipfile import is_zipfile

import pytest

content = textwrap.dedent(
    """\
    test-artifact:
      script: echo "test" > artifact.txt
      artifacts:
        untracked: true
    """
)
data = {
    "file_path": ".gitlab-ci.yml",
    "branch": "main",
    "content": content,
    "commit_message": "Initial commit",
}


@pytest.fixture(scope="module")
def job_with_artifacts(gitlab_runner, project):
    project.files.create(data)

    jobs = None
    while not jobs:
        time.sleep(0.5)
        jobs = project.jobs.list(scope="success")

    return project.jobs.get(jobs[0].id)


def test_cli_job_artifacts(capsysbinary, gitlab_config, job_with_artifacts):
    cmd = [
        "gitlab",
        "--config-file",
        gitlab_config,
        "project-job",
        "artifacts",
        "--id",
        str(job_with_artifacts.id),
        "--project-id",
        str(job_with_artifacts.pipeline["project_id"]),
    ]

    with capsysbinary.disabled():
        artifacts = subprocess.check_output(cmd)
    assert isinstance(artifacts, bytes)

    artifacts_zip = BytesIO(artifacts)
    assert is_zipfile(artifacts_zip)


def test_cli_project_artifact_download(gitlab_config, job_with_artifacts):
    cmd = [
        "gitlab",
        "--config-file",
        gitlab_config,
        "project-artifact",
        "download",
        "--project-id",
        str(job_with_artifacts.pipeline["project_id"]),
        "--ref-name",
        job_with_artifacts.ref,
        "--job",
        job_with_artifacts.name,
    ]

    artifacts = subprocess.run(cmd, capture_output=True, check=True)
    assert isinstance(artifacts.stdout, bytes)

    artifacts_zip = BytesIO(artifacts.stdout)
    assert is_zipfile(artifacts_zip)


def test_cli_project_artifact_raw(gitlab_config, job_with_artifacts):
    cmd = [
        "gitlab",
        "--config-file",
        gitlab_config,
        "project-artifact",
        "raw",
        "--project-id",
        str(job_with_artifacts.pipeline["project_id"]),
        "--ref-name",
        job_with_artifacts.ref,
        "--job",
        job_with_artifacts.name,
        "--artifact-path",
        "artifact.txt",
    ]

    artifacts = subprocess.run(cmd, capture_output=True, check=True)
    assert isinstance(artifacts.stdout, bytes)
    assert artifacts.stdout == b"test\n"

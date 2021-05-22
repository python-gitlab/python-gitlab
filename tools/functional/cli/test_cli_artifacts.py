import subprocess
import sys
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
    "branch": "master",
    "content": content,
    "commit_message": "Initial commit",
}


@pytest.mark.skipif(sys.version_info < (3, 8), reason="I am the walrus")
def test_cli_artifacts(capsysbinary, gitlab_config, gitlab_runner, project):
    project.files.create(data)

    while not (jobs := project.jobs.list(scope="success")):
        time.sleep(0.5)

    job = project.jobs.get(jobs[0].id)
    cmd = [
        "gitlab",
        "--config-file",
        gitlab_config,
        "project-job",
        "artifacts",
        "--id",
        str(job.id),
        "--project-id",
        str(project.id),
    ]

    with capsysbinary.disabled():
        artifacts = subprocess.check_output(cmd)
    assert isinstance(artifacts, bytes)

    artifacts_zip = BytesIO(artifacts)
    assert is_zipfile(artifacts_zip)

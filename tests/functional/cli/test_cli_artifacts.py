import subprocess
import textwrap
import time
from io import BytesIO
from zipfile import is_zipfile

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


def test_cli_artifacts(capsysbinary, gitlab_config, gitlab_runner, project):
    project.files.create(data)

    jobs = None
    while not jobs:
        jobs = project.jobs.list(scope="success")
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

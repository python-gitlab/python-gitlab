import json
import time


def test_project_create_file(gitlab_cli, project):
    file_path = "README"
    branch = "main"
    content = "CONTENT"
    commit_message = "Initial commit"

    cmd = [
        "project-file",
        "create",
        "--project-id",
        project.id,
        "--file-path",
        file_path,
        "--branch",
        branch,
        "--content",
        content,
        "--commit-message",
        commit_message,
    ]
    ret = gitlab_cli(cmd)

    assert ret.success


def test_list_all_commits(gitlab_cli, project):
    data = {
        "branch": "new-branch",
        "start_branch": "main",
        "commit_message": "New commit on new branch",
        "actions": [
            {"action": "create", "file_path": "new-file", "content": "new content"}
        ],
    }
    commit = project.commits.create(data)

    cmd = ["project-commit", "list", "--project-id", project.id, "--get-all"]
    ret = gitlab_cli(cmd)
    assert commit.id not in ret.stdout

    # Listing commits on other branches requires `all` parameter passed to the API
    cmd = ["project-commit", "list", "--project-id", project.id, "--get-all", "--all"]
    ret_all = gitlab_cli(cmd)
    assert commit.id in ret_all.stdout
    assert len(ret_all.stdout) > len(ret.stdout)


def test_commit_merge_requests(gitlab_cli, project, merge_request, wait_for_sidekiq):
    """This tests the `project-commit merge-requests` command and also tests
    that we can print the result using the `json` formatter"""
    # create and then merge a merge-request
    mr = merge_request(source_branch="test_commit_merge_requests")
    merge_result = mr.merge(should_remove_source_branch=True)
    wait_for_sidekiq(timeout=60)
    # Wait until it is merged
    mr_iid = mr.iid
    for _ in range(60):
        mr = project.mergerequests.get(mr_iid)
        if mr.merged_at is not None:
            break
        time.sleep(0.5)
    assert mr.merged_at is not None
    time.sleep(0.5)
    wait_for_sidekiq(timeout=60)

    commit_sha = merge_result["sha"]
    cmd = [
        "-o",
        "json",
        "project-commit",
        "merge-requests",
        "--project-id",
        project.id,
        "--id",
        commit_sha,
    ]
    ret = gitlab_cli(cmd)
    assert ret.success

    json_list = json.loads(ret.stdout)
    assert isinstance(json_list, list)
    assert len(json_list) == 1
    mr_dict = json_list[0]
    assert mr_dict["id"] == mr.id
    assert mr_dict["iid"] == mr.iid


def test_revert_commit(gitlab_cli, project):
    commit = project.commits.list()[0]

    cmd = [
        "project-commit",
        "revert",
        "--project-id",
        project.id,
        "--id",
        commit.id,
        "--branch",
        "main",
    ]
    ret = gitlab_cli(cmd)

    assert ret.success


def test_get_commit_signature_not_found(gitlab_cli, project):
    commit = project.commits.list()[0]

    cmd = ["project-commit", "signature", "--project-id", project.id, "--id", commit.id]
    ret = gitlab_cli(cmd)

    assert not ret.success
    assert "404 Signature Not Found" in ret.stderr

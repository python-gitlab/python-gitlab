import base64
import os
import sys
import tarfile
import time
import zipfile
from io import BytesIO

import pytest

import gitlab


def test_repository_files(project):
    project.files.create(
        {
            "file_path": "README.md",
            "branch": "main",
            "content": "Initial content",
            "commit_message": "Initial commit",
        }
    )
    readme = project.files.get(file_path="README.md", ref="main")
    readme.content = base64.b64encode(b"Improved README").decode()

    time.sleep(2)
    readme.save(branch="main", commit_message="new commit")
    readme.delete(commit_message="Removing README", branch="main")

    project.files.create(
        {
            "file_path": "README.rst",
            "branch": "main",
            "content": "Initial content",
            "commit_message": "New commit",
        }
    )
    readme = project.files.get(file_path="README.rst", ref="main")
    # The first decode() is the ProjectFile method, the second one is the bytes
    # object method
    assert readme.decode().decode() == "Initial content"

    headers = project.files.head("README.rst", ref="main")
    assert headers["X-Gitlab-File-Path"] == "README.rst"

    blame = project.files.blame(file_path="README.rst", ref="main")
    assert blame

    raw_file = project.files.raw(file_path="README.rst", ref="main")
    assert os.fsdecode(raw_file) == "Initial content"

    raw_file = project.files.raw(file_path="README.rst")
    assert os.fsdecode(raw_file) == "Initial content"


def test_repository_tree(project):
    tree = project.repository_tree()
    assert tree
    assert tree[0]["name"] == "README.rst"

    blob_id = tree[0]["id"]
    blob = project.repository_raw_blob(blob_id)
    assert blob.decode() == "Initial content"

    snapshot = project.snapshot()
    assert isinstance(snapshot, bytes)


def test_repository_archive(project):
    archive = project.repository_archive()
    assert isinstance(archive, bytes)

    archive2 = project.repository_archive("main")
    assert archive == archive2


# NOTE(jlvillal): Support for using tarfile.is_tarfile() on a file or file-like object
# was added in Python 3.9
@pytest.mark.skipif(sys.version_info < (3, 9), reason="requires python3.9 or higher")
@pytest.mark.parametrize(
    "format,assertion",
    [
        ("tbz", tarfile.is_tarfile),
        ("tbz2", tarfile.is_tarfile),
        ("tb2", tarfile.is_tarfile),
        ("bz2", tarfile.is_tarfile),
        ("tar", tarfile.is_tarfile),
        ("tar.gz", tarfile.is_tarfile),
        ("tar.bz2", tarfile.is_tarfile),
        ("zip", zipfile.is_zipfile),
    ],
)
def test_repository_archive_formats(project, format, assertion):
    archive = project.repository_archive(format=format)
    assert assertion(BytesIO(archive))


def test_create_commit(project):
    data = {
        "branch": "main",
        "commit_message": "blah blah blah",
        "actions": [{"action": "create", "file_path": "blah", "content": "blah"}],
    }
    commit = project.commits.create(data)

    assert "@@" in project.commits.list()[0].diff()[0]["diff"]
    assert isinstance(commit.refs(), list)
    assert isinstance(commit.merge_requests(), list)


def test_list_all_commits(project):
    data = {
        "branch": "new-branch",
        "start_branch": "main",
        "commit_message": "New commit on new branch",
        "actions": [
            {"action": "create", "file_path": "new-file", "content": "new content"}
        ],
    }
    commit = project.commits.create(data)

    commits = project.commits.list(all=True)
    assert commit not in commits

    # Listing commits on other branches requires `all` parameter passed to the API
    all_commits = project.commits.list(get_all=True, all=True)
    assert commit in all_commits
    assert len(all_commits) > len(commits)


def test_create_commit_status(project):
    commit = project.commits.list()[0]
    status = commit.statuses.create({"state": "success", "sha": commit.id})
    assert status in commit.statuses.list()


def test_commit_signature(project):
    commit = project.commits.list()[0]

    with pytest.raises(gitlab.GitlabGetError) as e:
        commit.signature()

    assert "404 Signature Not Found" in str(e.value)


def test_commit_comment(project):
    commit = project.commits.list()[0]

    commit.comments.create({"note": "This is a commit comment"})
    assert len(commit.comments.list()) == 1


def test_commit_discussion(project):
    commit = project.commits.list()[0]

    discussion = commit.discussions.create({"body": "Discussion body"})
    assert discussion in commit.discussions.list()

    note = discussion.notes.create({"body": "first note"})
    note_from_get = discussion.notes.get(note.id)
    note_from_get.body = "updated body"
    note_from_get.save()
    discussion = commit.discussions.get(discussion.id)

    note_from_get.delete()


def test_revert_commit(project):
    commit = project.commits.list()[0]
    revert_commit = commit.revert(branch="main")

    expected_message = f'Revert "{commit.message}"\n\nThis reverts commit {commit.id}'
    assert revert_commit["message"] == expected_message

    with pytest.raises(gitlab.GitlabRevertError):
        # Two revert attempts should raise GitlabRevertError
        commit.revert(branch="main")


def test_repository_merge_base(project):
    refs = [commit.id for commit in project.commits.list(all=True)]

    commit = project.repository_merge_base(refs)
    assert commit["id"] in refs

    with pytest.raises(gitlab.GitlabGetError, match="Provide at least 2 refs"):
        commit = project.repository_merge_base(refs[0])

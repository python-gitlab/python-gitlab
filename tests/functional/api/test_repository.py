import base64
import tarfile
import time
import zipfile
from io import BytesIO

import pytest

import gitlab


def test_repository_files(project):
    project.files.create(
        {
            "file_path": "README",
            "branch": "main",
            "content": "Initial content",
            "commit_message": "Initial commit",
        }
    )
    readme = project.files.get(file_path="README", ref="main")
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

    blame = project.files.blame(file_path="README.rst", ref="main")
    assert blame


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


def test_create_commit_status(project):
    commit = project.commits.list()[0]
    size = len(commit.statuses.list())
    commit.statuses.create({"state": "success", "sha": commit.id})
    assert len(commit.statuses.list()) == size + 1


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
    count = len(commit.discussions.list())

    discussion = commit.discussions.create({"body": "Discussion body"})
    assert len(commit.discussions.list()) == (count + 1)

    note = discussion.notes.create({"body": "first note"})
    note_from_get = discussion.notes.get(note.id)
    note_from_get.body = "updated body"
    note_from_get.save()
    discussion = commit.discussions.get(discussion.id)
    # assert discussion.attributes["notes"][-1]["body"] == "updated body"
    note_from_get.delete()
    discussion = commit.discussions.get(discussion.id)
    # assert len(discussion.attributes["notes"]) == 1


def test_revert_commit(project):
    commit = project.commits.list()[0]
    revert_commit = commit.revert(branch="main")

    expected_message = f'Revert "{commit.message}"\n\nThis reverts commit {commit.id}'
    assert revert_commit["message"] == expected_message

    with pytest.raises(gitlab.GitlabRevertError):
        # Two revert attempts should raise GitlabRevertError
        commit.revert(branch="main")

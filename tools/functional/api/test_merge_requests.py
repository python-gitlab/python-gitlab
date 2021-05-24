import time

import pytest

import gitlab
import gitlab.v4.objects


def test_merge_requests(project):
    project.files.create(
        {
            "file_path": "README.rst",
            "branch": "master",
            "content": "Initial content",
            "commit_message": "Initial commit",
        }
    )

    source_branch = "branch1"
    project.branches.create({"branch": source_branch, "ref": "master"})

    project.files.create(
        {
            "file_path": "README2.rst",
            "branch": source_branch,
            "content": "Initial content",
            "commit_message": "New commit in new branch",
        }
    )
    project.mergerequests.create(
        {"source_branch": "branch1", "target_branch": "master", "title": "MR readme2"}
    )


def test_merge_request_discussion(project):
    mr = project.mergerequests.list()[0]
    size = len(mr.discussions.list())

    discussion = mr.discussions.create({"body": "Discussion body"})
    assert len(mr.discussions.list()) == size + 1

    note = discussion.notes.create({"body": "first note"})
    note_from_get = discussion.notes.get(note.id)
    note_from_get.body = "updated body"
    note_from_get.save()

    discussion = mr.discussions.get(discussion.id)
    assert discussion.attributes["notes"][-1]["body"] == "updated body"

    note_from_get.delete()
    discussion = mr.discussions.get(discussion.id)
    assert len(discussion.attributes["notes"]) == 1


def test_merge_request_labels(project):
    mr = project.mergerequests.list()[0]
    mr.labels = ["label2"]
    mr.save()

    events = mr.resourcelabelevents.list()
    assert events

    event = mr.resourcelabelevents.get(events[0].id)
    assert event


def test_merge_request_milestone_events(project, milestone):
    mr = project.mergerequests.list()[0]
    mr.milestone_id = milestone.id
    mr.save()

    milestones = mr.resourcemilestoneevents.list()
    assert milestones

    milestone = mr.resourcemilestoneevents.get(milestones[0].id)
    assert milestone


def test_merge_request_basic(project):
    mr = project.mergerequests.list()[0]
    # basic testing: only make sure that the methods exist
    mr.commits()
    mr.changes()
    assert mr.participants()


def test_merge_request_rebase(project):
    mr = project.mergerequests.list()[0]
    assert mr.rebase()


@pytest.mark.skip(reason="flaky test")
def test_merge_request_merge(project):
    mr = project.mergerequests.list()[0]
    mr.merge()
    project.branches.delete(mr.source_branch)

    with pytest.raises(gitlab.GitlabMRClosedError):
        # Two merge attempts should raise GitlabMRClosedError
        mr.merge()


def merge_request_create_helper(
    *,
    project: gitlab.v4.objects.Project,
    source_branch: str,
    wait_for_sidekiq,
    branch_will_be_deleted: bool,
    **kwargs,
):
    # Wait for processes to be done before we start...
    # NOTE(jlvillal): Sometimes the CI would give a "500 Internal Server
    # Error". Hoping that waiting until all other processes are done will help
    # with that.
    result = wait_for_sidekiq(timeout=60)
    assert result is True, "sidekiq process should have terminated but did not"

    project.branches.create({"branch": source_branch, "ref": "master"})

    # NOTE(jlvillal): Must create a commit in the new branch before we can
    # create an MR that will work.
    project.files.create(
        {
            "file_path": f"README.{source_branch}",
            "branch": source_branch,
            "content": "Initial content",
            "commit_message": "New commit in new branch",
        }
    )

    mr = project.mergerequests.create(
        {
            "source_branch": source_branch,
            "target_branch": "master",
            "title": "Should remove source branch",
            "remove_source_branch": True,
        }
    )

    result = wait_for_sidekiq(timeout=60)
    assert result is True, "sidekiq process should have terminated but did not"

    mr_iid = mr.iid
    for _ in range(60):
        mr = project.mergerequests.get(mr_iid)
        if mr.merge_status != "checking":
            break
        time.sleep(0.5)
    assert mr.merge_status != "checking"

    # Ensure we can get the MR branch
    project.branches.get(source_branch)

    mr.merge(**kwargs)

    result = wait_for_sidekiq(timeout=60)
    assert result is True, "sidekiq process should have terminated but did not"

    # Wait until it is merged
    mr_iid = mr.iid
    for _ in range(60):
        mr = project.mergerequests.get(mr_iid)
        if mr.merged_at is not None:
            break
        time.sleep(0.5)
    assert mr.merged_at is not None
    time.sleep(0.5)

    if branch_will_be_deleted:
        # Ensure we can NOT get the MR branch
        with pytest.raises(gitlab.exceptions.GitlabGetError):
            project.branches.get(source_branch)


def test_merge_request_should_remove_source_branch(
    project: gitlab.v4.objects.Project, wait_for_sidekiq
):
    """Test to ensure
    https://github.com/python-gitlab/python-gitlab/issues/1120 is fixed.
    Bug reported that they could not use 'should_remove_source_branch' in
    mr.merge() call"""

    source_branch = "remove_source_branch"

    merge_request_create_helper(
        project=project,
        source_branch=source_branch,
        wait_for_sidekiq=wait_for_sidekiq,
        branch_will_be_deleted=True,
        should_remove_source_branch=True,
    )


def test_merge_request_large_commit_message(
    project: gitlab.v4.objects.Project, wait_for_sidekiq
):
    """Test to ensure https://github.com/python-gitlab/python-gitlab/issues/1452
    is fixed.
    Bug reported that very long 'merge_commit_message' in mr.merge() would
    cause an error: 414 Request too large
    """
    source_branch = "large_commit_message"

    merge_commit_message = "large_message\r\n" * 1_000
    assert len(merge_commit_message) > 10_000

    merge_request_create_helper(
        project=project,
        source_branch=source_branch,
        wait_for_sidekiq=wait_for_sidekiq,
        branch_will_be_deleted=False,
        merge_commit_message=merge_commit_message,
    )

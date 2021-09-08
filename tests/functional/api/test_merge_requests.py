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


def test_merge_request_should_remove_source_branch(
    project, merge_request, wait_for_sidekiq
) -> None:
    """Test to ensure
    https://github.com/python-gitlab/python-gitlab/issues/1120 is fixed.
    Bug reported that they could not use 'should_remove_source_branch' in
    mr.merge() call"""

    source_branch = "remove_source_branch"
    mr = merge_request(source_branch=source_branch)

    mr.merge(should_remove_source_branch=True)

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
    result = wait_for_sidekiq(timeout=60)
    assert result is True, "sidekiq process should have terminated but did not"

    # Ensure we can NOT get the MR branch
    with pytest.raises(gitlab.exceptions.GitlabGetError):
        result = project.branches.get(source_branch)
        # Help to debug in case the expected exception doesn't happen.
        import pprint

        print("mr:", pprint.pformat(mr))
        print("mr.merged_at:", pprint.pformat(mr.merged_at))
        print("result:", pprint.pformat(result))


def test_merge_request_large_commit_message(
    project, merge_request, wait_for_sidekiq
) -> None:
    """Test to ensure https://github.com/python-gitlab/python-gitlab/issues/1452
    is fixed.
    Bug reported that very long 'merge_commit_message' in mr.merge() would
    cause an error: 414 Request too large
    """

    source_branch = "large_commit_message"
    mr = merge_request(source_branch=source_branch)

    merge_commit_message = "large_message\r\n" * 1_000
    assert len(merge_commit_message) > 10_000

    mr.merge(merge_commit_message=merge_commit_message)

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

    # Ensure we can get the MR branch
    project.branches.get(source_branch)


def test_merge_request_merge_ref(merge_request) -> None:
    source_branch = "merge_ref_test"
    mr = merge_request(source_branch=source_branch)

    response = mr.merge_ref()
    assert response and "commit_id" in response


def test_merge_request_merge_ref_should_fail(
    project, merge_request, wait_for_sidekiq
) -> None:
    source_branch = "merge_ref_test2"
    mr = merge_request(source_branch=source_branch)

    # Create conflict
    project.files.create(
        {
            "file_path": f"README.{source_branch}",
            "branch": project.default_branch,
            "content": "Different initial content",
            "commit_message": "Another commit in main branch",
        }
    )
    result = wait_for_sidekiq(timeout=60)
    assert result is True, "sidekiq process should have terminated but did not"

    # Check for non-existing merge_ref for MR with conflicts
    with pytest.raises(gitlab.exceptions.GitlabGetError):
        response = mr.merge_ref()
        assert "commit_id" not in response

import pytest

import gitlab


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
    branch = project.branches.create({"branch": source_branch, "ref": "master"})

    project.files.create(
        {
            "file_path": "README2.rst",
            "branch": source_branch,
            "content": "Initial content",
            "commit_message": "New commit in new branch",
        }
    )
    mr = project.mergerequests.create(
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

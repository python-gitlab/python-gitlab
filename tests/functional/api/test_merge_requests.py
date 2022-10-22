import time

import pytest

import gitlab
import gitlab.v4.objects


def test_merge_requests(project):
    project.files.create(
        {
            "file_path": "README.rst",
            "branch": "main",
            "content": "Initial content",
            "commit_message": "Initial commit",
        }
    )

    source_branch = "branch1"
    project.branches.create({"branch": source_branch, "ref": "main"})

    project.files.create(
        {
            "file_path": "README2.rst",
            "branch": source_branch,
            "content": "Initial content",
            "commit_message": "New commit in new branch",
        }
    )
    project.mergerequests.create(
        {"source_branch": "branch1", "target_branch": "main", "title": "MR readme2"}
    )


def test_merge_requests_get(project, merge_request):
    new_mr = merge_request(source_branch="test_get")
    mr_iid = new_mr.iid
    mr = project.mergerequests.get(mr_iid)
    assert mr.iid == mr_iid
    mr = project.mergerequests.get(str(mr_iid))
    assert mr.iid == mr_iid


@pytest.mark.gitlab_premium
def test_merge_requests_list_approver_ids(project):
    # show https://github.com/python-gitlab/python-gitlab/issues/1698 is now
    # fixed
    project.mergerequests.list(
        all=True,
        state="opened",
        author_id=423,
        approver_ids=[423],
    )


def test_merge_requests_get_lazy(project, merge_request):
    new_mr = merge_request(source_branch="test_get")
    mr_iid = new_mr.iid
    mr = project.mergerequests.get(mr_iid, lazy=True)
    assert mr.iid == mr_iid


def test_merge_request_discussion(project):
    mr = project.mergerequests.list()[0]

    discussion = mr.discussions.create({"body": "Discussion body"})
    assert discussion in mr.discussions.list()

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


@pytest.mark.gitlab_premium
@pytest.mark.xfail(reason="project /approvers endpoint is gone")
def test_project_approvals(project):
    mr = project.mergerequests.list()[0]
    approval = project.approvals.get()

    reset_value = approval.reset_approvals_on_push
    approval.reset_approvals_on_push = not reset_value
    approval.save()

    approval = project.approvals.get()
    assert reset_value != approval.reset_approvals_on_push

    project.approvals.set_approvers([1], [])
    approval = project.approvals.get()
    assert approval.approvers[0]["user"]["id"] == 1

    approval = mr.approvals.get()
    approval.approvals_required = 2
    approval.save()
    approval = mr.approvals.get()
    assert approval.approvals_required == 2

    approval.approvals_required = 3
    approval.save()
    approval = mr.approvals.get()
    assert approval.approvals_required == 3

    mr.approvals.set_approvers(1, [1], [])
    approval = mr.approvals.get()
    assert approval.approvers[0]["user"]["id"] == 1


@pytest.mark.gitlab_premium
def test_project_merge_request_approval_rules(group, project):
    approval_rules = project.approvalrules.list(get_all=True)
    assert not approval_rules

    project.approvalrules.create(
        {"name": "approval-rule", "approvals_required": 2, "group_ids": [group.id]}
    )
    approval_rules = project.approvalrules.list(get_all=True)
    assert len(approval_rules) == 1
    assert approval_rules[0].approvals_required == 2

    approval_rules[0].save()
    approval_rules = project.approvalrules.list(get_all=True)
    assert len(approval_rules) == 1
    assert approval_rules[0].approvals_required == 2

    approval_rules[0].delete()
    ars = project.approvalrules.list(get_all=True)
    assert len(ars) == 0


def test_merge_request_reset_approvals(gitlab_url, project, wait_for_sidekiq):
    bot = project.access_tokens.create({"name": "bot", "scopes": ["api"]})
    bot_gitlab = gitlab.Gitlab(gitlab_url, private_token=bot.token)
    bot_project = bot_gitlab.projects.get(project.id, lazy=True)

    wait_for_sidekiq(timeout=60)
    mr = bot_project.mergerequests.list()[0]  # type: ignore[index]
    assert mr.reset_approvals()


def test_merge_request_merge(project, merge_request, wait_for_sidekiq):
    mr = merge_request(source_branch="test_merge_request_merge")
    mr.merge()
    wait_for_sidekiq(timeout=60)

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

    mr.merge(
        merge_commit_message=merge_commit_message, should_remove_source_branch=False
    )

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
    wait_for_sidekiq(timeout=60)

    # Check for non-existing merge_ref for MR with conflicts
    with pytest.raises(gitlab.exceptions.GitlabGetError):
        response = mr.merge_ref()
        assert "commit_id" not in response

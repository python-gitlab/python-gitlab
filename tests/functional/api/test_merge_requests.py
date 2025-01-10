import datetime
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

    source_branch = "branch-merge-request-api"
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
        {"source_branch": source_branch, "target_branch": "main", "title": "MR readme2"}
    )


def test_merge_requests_get(project, merge_request):
    mr = project.mergerequests.get(merge_request.iid)
    assert mr.iid == merge_request.iid

    mr = project.mergerequests.get(str(merge_request.iid))
    assert mr.iid == merge_request.iid


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
    mr = project.mergerequests.get(merge_request.iid, lazy=True)
    assert mr.iid == merge_request.iid


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
    participants = mr.participants()
    assert participants
    assert isinstance(participants, list)


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


def test_merge_request_reset_approvals(gitlab_url, project):
    today = datetime.date.today()
    future_date = today + datetime.timedelta(days=4)
    bot = project.access_tokens.create(
        {"name": "bot", "scopes": ["api"], "expires_at": future_date.isoformat()}
    )

    bot_gitlab = gitlab.Gitlab(gitlab_url, private_token=bot.token)
    bot_project = bot_gitlab.projects.get(project.id, lazy=True)

    # Pause to let GL catch up (happens on hosted too, sometimes takes a while for server to be ready to merge)
    time.sleep(5)

    mr = bot_project.mergerequests.list()[0]  # type: ignore[index]

    assert mr.reset_approvals()


def test_cancel_merge_when_pipeline_succeeds(project, merge_request_with_pipeline):
    # Pause to let GL catch up (happens on hosted too, sometimes takes a while for server to be ready to merge)
    time.sleep(5)
    # Set to merge when the pipeline succeeds, which should never happen
    merge_request_with_pipeline.merge(merge_when_pipeline_succeeds=True)
    # Pause to let GL catch up (happens on hosted too, sometimes takes a while for server to be ready to merge)
    time.sleep(5)

    mr = project.mergerequests.get(merge_request_with_pipeline.iid)
    assert mr.merged_at is None
    assert mr.merge_when_pipeline_succeeds is True
    cancel = mr.cancel_merge_when_pipeline_succeeds()
    assert cancel == {"status": "success"}


def test_merge_request_merge(project, merge_request):
    merge_request.merge()
    # Pause to let GL catch up (happens on hosted too, sometimes takes a while for server to be ready to merge)
    time.sleep(5)

    mr = project.mergerequests.get(merge_request.iid)
    assert mr.merged_at is not None
    assert mr.merge_when_pipeline_succeeds is False
    with pytest.raises(gitlab.GitlabMRClosedError):
        # Two merge attempts should raise GitlabMRClosedError
        mr.merge()


def test_merge_request_should_remove_source_branch(project, merge_request) -> None:
    """Test to ensure
    https://github.com/python-gitlab/python-gitlab/issues/1120 is fixed.
    Bug reported that they could not use 'should_remove_source_branch' in
    mr.merge() call"""
    merge_request.merge(should_remove_source_branch=True)
    # Pause to let GL catch up (happens on hosted too, sometimes takes a while for server to be ready to merge)
    time.sleep(5)

    # Wait until it is merged
    mr = None
    mr_iid = merge_request.iid
    for _ in range(60):
        mr = project.mergerequests.get(mr_iid)
        if mr.merged_at is not None:
            break
        time.sleep(0.5)

    assert mr is not None
    assert mr.merged_at is not None
    time.sleep(0.5)
    # Pause to let GL catch up (happens on hosted too, sometimes takes a while for server to be ready to merge)
    time.sleep(5)

    # Ensure we can NOT get the MR branch
    with pytest.raises(gitlab.exceptions.GitlabGetError):
        result = project.branches.get(merge_request.source_branch)
        # Help to debug in case the expected exception doesn't happen.
        import pprint

        print("mr:", pprint.pformat(mr))
        print("mr.merged_at:", pprint.pformat(mr.merged_at))
        print("result:", pprint.pformat(result))


def test_merge_request_large_commit_message(project, merge_request) -> None:
    """Test to ensure https://github.com/python-gitlab/python-gitlab/issues/1452
    is fixed.
    Bug reported that very long 'merge_commit_message' in mr.merge() would
    cause an error: 414 Request too large
    """
    merge_commit_message = "large_message\r\n" * 1_000
    assert len(merge_commit_message) > 10_000

    merge_request.merge(
        merge_commit_message=merge_commit_message, should_remove_source_branch=False
    )

    # Pause to let GL catch up (happens on hosted too, sometimes takes a while for server to be ready to merge)
    time.sleep(5)

    # Wait until it is merged
    mr = None
    mr_iid = merge_request.iid
    for _ in range(60):
        mr = project.mergerequests.get(mr_iid)
        if mr.merged_at is not None:
            break
        time.sleep(0.5)

    assert mr is not None
    assert mr.merged_at is not None
    time.sleep(0.5)

    # Ensure we can get the MR branch
    project.branches.get(merge_request.source_branch)


def test_merge_request_merge_ref(merge_request) -> None:
    response = merge_request.merge_ref()
    assert response and "commit_id" in response


def test_merge_request_merge_ref_should_fail(project, merge_request) -> None:
    # Create conflict
    project.files.create(
        {
            "file_path": f"README.{merge_request.source_branch}",
            "branch": project.default_branch,
            "content": "Different initial content",
            "commit_message": "Another commit in main branch",
        }
    )
    # Pause to let GL catch up (happens on hosted too, sometimes takes a while for server to be ready to merge)
    time.sleep(5)

    # Check for non-existing merge_ref for MR with conflicts
    with pytest.raises(gitlab.exceptions.GitlabGetError):
        response = merge_request.merge_ref()
        assert "commit_id" not in response

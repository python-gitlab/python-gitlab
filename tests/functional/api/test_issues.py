import gitlab


def test_create_issue(project):
    issue = project.issues.create({"title": "my issue 1"})
    issue2 = project.issues.create({"title": "my issue 2"})
    issue_iids = [issue.iid for issue in project.issues.list()]
    assert len(issue_iids) == 2

    # Test 'iids' as a list
    assert len(project.issues.list(iids=issue_iids)) == 2

    issue2.state_event = "close"
    issue2.save()
    assert len(project.issues.list(state="closed")) == 1
    assert len(project.issues.list(state="opened")) == 1

    assert isinstance(issue.user_agent_detail(), dict)
    assert issue.user_agent_detail()["user_agent"]
    assert issue.participants()
    assert type(issue.closed_by()) == list
    assert type(issue.related_merge_requests()) == list


def test_issue_notes(issue):
    size = len(issue.notes.list())

    note = issue.notes.create({"body": "This is an issue note"})
    assert len(issue.notes.list()) == size + 1

    emoji = note.awardemojis.create({"name": "tractor"})
    assert len(note.awardemojis.list()) == 1

    emoji.delete()
    assert len(note.awardemojis.list()) == 0

    note.delete()
    assert len(issue.notes.list()) == size


def test_issue_labels(project, issue):
    project.labels.create({"name": "label2", "color": "#aabbcc"})
    issue.labels = ["label2"]
    issue.save()

    assert issue in project.issues.list(labels=["label2"])
    assert issue in project.issues.list(labels="label2")
    assert issue in project.issues.list(labels="Any")
    assert issue not in project.issues.list(labels="None")


def test_issue_events(issue):
    events = issue.resourcelabelevents.list()
    assert isinstance(events, list)

    event = issue.resourcelabelevents.get(events[0].id)
    assert isinstance(event, gitlab.v4.objects.ProjectIssueResourceLabelEvent)


def test_issue_milestones(project, milestone):
    data = {"title": "my issue 1", "milestone_id": milestone.id}
    issue = project.issues.create(data)
    assert milestone.issues().next().title == "my issue 1"

    milestone_events = issue.resourcemilestoneevents.list()
    assert isinstance(milestone_events, list)

    milestone_event = issue.resourcemilestoneevents.get(milestone_events[0].id)
    assert isinstance(
        milestone_event, gitlab.v4.objects.ProjectIssueResourceMilestoneEvent
    )

    milestone_issues = project.issues.list(milestone=milestone.title)
    assert len(milestone_issues) == 1


def test_issue_discussions(issue):
    size = len(issue.discussions.list())

    discussion = issue.discussions.create({"body": "Discussion body"})
    assert len(issue.discussions.list()) == size + 1

    d_note = discussion.notes.create({"body": "first note"})
    d_note_from_get = discussion.notes.get(d_note.id)
    d_note_from_get.body = "updated body"
    d_note_from_get.save()

    discussion = issue.discussions.get(discussion.id)
    assert discussion.attributes["notes"][-1]["body"] == "updated body"

    d_note_from_get.delete()
    discussion = issue.discussions.get(discussion.id)
    assert len(discussion.attributes["notes"]) == 1

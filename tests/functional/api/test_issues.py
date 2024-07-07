import gitlab


def test_create_issue(project):
    issue = project.issues.create({"title": "my issue 1"})
    issue2 = project.issues.create({"title": "my issue 2"})

    issues = project.issues.list()
    issue_iids = [issue.iid for issue in issues]
    assert {issue, issue2} <= set(issues)

    # Test 'iids' as a list
    filtered_issues = project.issues.list(iids=issue_iids)
    assert {issue, issue2} == set(filtered_issues)

    issue2.state_event = "close"
    issue2.save()
    assert issue in project.issues.list(state="opened")
    assert issue2 in project.issues.list(state="closed")

    participants = issue.participants()
    assert participants
    assert isinstance(participants, list)
    assert type(issue.closed_by()) == list
    assert type(issue.related_merge_requests()) == list


def test_issue_notes(issue):
    note = issue.notes.create({"body": "This is an issue note"})
    assert note in issue.notes.list()

    emoji = note.awardemojis.create({"name": "tractor"})
    assert emoji in note.awardemojis.list()

    emoji.delete()
    note.delete()


def test_issue_labels(project, issue):
    project.labels.create({"name": "label2", "color": "#aabbcc"})
    issue.labels = ["label2"]
    issue.save()

    assert issue in project.issues.list(labels=["label2"])
    assert issue in project.issues.list(labels="label2")
    assert issue in project.issues.list(labels="Any")
    assert issue not in project.issues.list(labels="None")


def test_issue_links(project, issue):
    linked_issue = project.issues.create({"title": "Linked issue"})
    source_issue, target_issue = issue.links.create(
        {"target_project_id": project.id, "target_issue_iid": linked_issue.iid}
    )
    assert source_issue == issue
    assert target_issue == linked_issue

    links = issue.links.list()
    assert links

    link_id = links[0].issue_link_id

    issue.links.delete(link_id)


def test_issue_label_events(issue):
    events = issue.resourcelabelevents.list()
    assert isinstance(events, list)

    event = issue.resourcelabelevents.get(events[0].id)
    assert isinstance(event, gitlab.v4.objects.ProjectIssueResourceLabelEvent)


def test_issue_weight_events(issue):
    issue.weight = 13
    issue.save()

    events = issue.resource_weight_events.list()
    assert isinstance(events, list)

    event = issue.resource_weight_events.get(events[0].id)
    assert isinstance(event, gitlab.v4.objects.ProjectIssueResourceWeightEvent)


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

    assert issue in project.issues.list(milestone=milestone.title)


def test_issue_discussions(issue):
    discussion = issue.discussions.create({"body": "Discussion body"})
    assert discussion in issue.discussions.list()

    d_note = discussion.notes.create({"body": "first note"})
    d_note_from_get = discussion.notes.get(d_note.id)
    d_note_from_get.body = "updated body"
    d_note_from_get.save()

    discussion = issue.discussions.get(discussion.id)
    assert discussion.attributes["notes"][-1]["body"] == "updated body"

    d_note_from_get.delete()

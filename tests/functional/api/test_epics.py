import pytest

pytestmark = pytest.mark.gitlab_premium


def test_epics(group):
    epic = group.epics.create({"title": "Test epic"})
    epic.title = "Fixed title"
    epic.labels = ["label1", "label2"]
    epic.save()

    epic = group.epics.get(epic.iid)
    assert epic.title == "Fixed title"
    assert epic.labels == ["label1", "label2"]
    assert group.epics.list()


def test_epic_issues(epic, issue):
    assert not epic.issues.list()

    # FYI: Creating an issue causes a note to be created
    epic_issue = epic.issues.create({"issue_id": issue.id})
    assert epic.issues.list()

    # FYI: Deleting an issue causes a note to be created
    epic_issue.delete()


def test_epic_notes(epic):
    notes = epic.notes.list(get_all=True)

    epic.notes.create({"body": "Test note"})
    new_notes = epic.notes.list(get_all=True)
    assert len(new_notes) == (len(notes) + 1), f"{new_notes} {notes}"

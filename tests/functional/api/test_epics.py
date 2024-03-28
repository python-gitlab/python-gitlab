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


@pytest.mark.xfail(reason="404 on issue.id")
def test_epic_issues(epic, issue):
    assert not epic.issues.list()

    epic_issue = epic.issues.create({"issue_id": issue.id})
    assert epic.issues.list()

    epic_issue.delete()


def test_epic_notes(epic):
    assert not epic.notes.list()

    epic.notes.create({"body": "Test note"})
    assert epic.notes.list()

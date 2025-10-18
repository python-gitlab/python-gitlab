import uuid

import pytest

from tests.functional import helpers

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


def test_epic_save_from_parent_group_updates_subgroup_epic(group):
    subgroup_id = uuid.uuid4().hex
    subgroup = group.subgroups.create(
        {"name": f"subgroup-{subgroup_id}", "path": f"sg-{subgroup_id}"}
    )

    nested_epic = subgroup.epics.create(
        {"title": f"Nested epic {subgroup_id}", "description": "Nested epic"}
    )

    try:
        fetched_epics = group.epics.list(search=nested_epic.title)
        assert fetched_epics, "Expected to discover nested epic via parent group list"

        fetched_epic = next(
            (epic for epic in fetched_epics if epic.id == nested_epic.id), None
        )
        assert (
            fetched_epic is not None
        ), "Parent group listing did not include nested epic"

        new_label = f"nested-{subgroup_id}"
        fetched_epic.labels = [new_label]
        fetched_epic.save()

        refreshed_epic = subgroup.epics.get(nested_epic.iid)
        assert new_label in refreshed_epic.labels
    finally:
        helpers.safe_delete(nested_epic)
        helpers.safe_delete(subgroup)

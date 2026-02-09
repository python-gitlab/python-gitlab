import uuid

import pytest

import gitlab.exceptions
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


def test_epic_save_from_parent_group_updates_subgroup_epic(gl, group):
    subgroup_id = uuid.uuid4().hex
    subgroup = gl.groups.create(
        {
            "name": f"subgroup-{subgroup_id}",
            "path": f"sg-{subgroup_id}",
            "parent_id": group.id,
        }
    )

    nested_epic = subgroup.epics.create(
        {"title": f"Nested epic {subgroup_id}", "description": "Nested epic"}
    )

    try:
        fetched_epics = group.epics.list(search=nested_epic.title)
        assert fetched_epics, "Expected to discover nested epic via parent group list"
        subgroup.epics.get(nested_epic.iid)

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
        with pytest.raises(gitlab.exceptions.GitlabGetError):
            subgroup.epics.get(nested_epic.iid)
        helpers.safe_delete(subgroup)

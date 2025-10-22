import pytest
import responses

from gitlab.v4.objects.epics import GroupEpic


def _build_epic(manager, iid=3, group_id=2, title="Epic"):
    data = {"iid": iid, "group_id": group_id, "title": title}
    return GroupEpic(manager, data)


def test_group_epic_save_uses_actual_group_path(group):
    epic_manager = group.epics
    epic = _build_epic(epic_manager, title="Original")
    epic.title = "Updated"

    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.PUT,
            url="http://localhost/api/v4/groups/2/epics/3",
            json={"iid": 3, "group_id": 2, "title": "Updated"},
            content_type="application/json",
            status=200,
            match=[responses.matchers.json_params_matcher({"title": "Updated"})],
        )

        epic.save()

    assert epic.title == "Updated"


def test_group_epic_delete_uses_actual_group_path(group):
    epic_manager = group.epics
    epic = _build_epic(epic_manager)

    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.DELETE,
            url="http://localhost/api/v4/groups/2/epics/3",
            status=204,
        )

        epic.delete()

    assert len(epic._updated_attrs) == 0


def test_group_epic_path_requires_group_id(fake_manager):
    epic = GroupEpic(manager=fake_manager, attrs={"iid": 5})

    with pytest.raises(AttributeError):
        epic._epic_path()

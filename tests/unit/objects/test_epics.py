from typing import Any

import pytest
import responses

import gitlab.base
import gitlab.v4.objects.epics
import gitlab.v4.objects.groups


def _build_epic(
    manager: gitlab.v4.objects.epics.GroupEpicManager,
    iid: int = 3,
    group_id: int = 2,
    title: str = "Epic",
) -> gitlab.v4.objects.epics.GroupEpic:
    data: dict[str, int | str] = {"iid": iid, "group_id": group_id, "title": title}
    return gitlab.v4.objects.epics.GroupEpic(manager, data)


def test_group_epic_save_uses_actual_group_path(
    group: gitlab.v4.objects.groups.Group,
) -> None:
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


def test_group_epic_delete_uses_actual_group_path(
    group: gitlab.v4.objects.groups.Group,
) -> None:
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


def test_group_epic_path_requires_group_id(
    fake_manager: gitlab.base.RESTManager[Any],
) -> None:
    epic = gitlab.v4.objects.epics.GroupEpic(manager=fake_manager, attrs={"iid": 5})

    with pytest.raises(AttributeError):
        epic._epic_path()


def test_group_epic_path_requires_real_group_id_for_lazy_epic(
    group: gitlab.v4.objects.groups.Group,
) -> None:
    epic = group.epics.get(3, lazy=True)

    with pytest.raises(AttributeError, match="lazy epic"):
        epic._epic_path()

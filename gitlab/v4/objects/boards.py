from gitlab.base import RESTObject
from gitlab.mixins import CRUDMixin, ObjectDeleteMixin, SaveMixin
from gitlab.types import RequiredOptional

__all__ = [
    "GroupBoardList",
    "GroupBoardListManager",
    "GroupBoard",
    "GroupBoardManager",
    "ProjectBoardList",
    "ProjectBoardListManager",
    "ProjectBoard",
    "ProjectBoardManager",
]


class GroupBoardList(SaveMixin, ObjectDeleteMixin, RESTObject):
    pass


class GroupBoardListManager(CRUDMixin[GroupBoardList]):
    _path = "/groups/{group_id}/boards/{board_id}/lists"
    _obj_cls = GroupBoardList
    _from_parent_attrs = {"group_id": "group_id", "board_id": "id"}
    _create_attrs = RequiredOptional(
        exclusive=("label_id", "assignee_id", "milestone_id", "iteration_id")
    )
    _update_attrs = RequiredOptional(required=("position",))


class GroupBoard(SaveMixin, ObjectDeleteMixin, RESTObject):
    lists: GroupBoardListManager


class GroupBoardManager(CRUDMixin[GroupBoard]):
    _path = "/groups/{group_id}/boards"
    _obj_cls = GroupBoard
    _from_parent_attrs = {"group_id": "id"}
    _create_attrs = RequiredOptional(required=("name",))


class ProjectBoardList(SaveMixin, ObjectDeleteMixin, RESTObject):
    pass


class ProjectBoardListManager(CRUDMixin[ProjectBoardList]):
    _path = "/projects/{project_id}/boards/{board_id}/lists"
    _obj_cls = ProjectBoardList
    _from_parent_attrs = {"project_id": "project_id", "board_id": "id"}
    _create_attrs = RequiredOptional(
        exclusive=("label_id", "assignee_id", "milestone_id", "iteration_id")
    )
    _update_attrs = RequiredOptional(required=("position",))


class ProjectBoard(SaveMixin, ObjectDeleteMixin, RESTObject):
    lists: ProjectBoardListManager


class ProjectBoardManager(CRUDMixin[ProjectBoard]):
    _path = "/projects/{project_id}/boards"
    _obj_cls = ProjectBoard
    _from_parent_attrs = {"project_id": "id"}
    _create_attrs = RequiredOptional(required=("name",))

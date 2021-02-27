from gitlab.mixins import CRUDMixin, ObjectDeleteMixin, SaveMixin


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


class GroupBoardList(SaveMixin, ObjectDeleteMixin):
    pass


class GroupBoardListManager(CRUDMixin):
    _path = "/groups/%(group_id)s/boards/%(board_id)s/lists"
    _obj_cls = GroupBoardList
    _from_parent_attrs = {"group_id": "group_id", "board_id": "id"}
    _create_attrs = (("label_id",), tuple())
    _update_attrs = (("position",), tuple())


class GroupBoard(SaveMixin, ObjectDeleteMixin):
    _managers = (("lists", "GroupBoardListManager"),)


class GroupBoardManager(CRUDMixin):
    _path = "/groups/%(group_id)s/boards"
    _obj_cls = GroupBoard
    _from_parent_attrs = {"group_id": "id"}
    _create_attrs = (("name",), tuple())


class ProjectBoardList(SaveMixin, ObjectDeleteMixin):
    pass


class ProjectBoardListManager(CRUDMixin):
    _path = "/projects/%(project_id)s/boards/%(board_id)s/lists"
    _obj_cls = ProjectBoardList
    _from_parent_attrs = {"project_id": "project_id", "board_id": "id"}
    _create_attrs = (("label_id",), tuple())
    _update_attrs = (("position",), tuple())


class ProjectBoard(SaveMixin, ObjectDeleteMixin):
    _managers = (("lists", "ProjectBoardListManager"),)


class ProjectBoardManager(CRUDMixin):
    _path = "/projects/%(project_id)s/boards"
    _obj_cls = ProjectBoard
    _from_parent_attrs = {"project_id": "id"}
    _create_attrs = (("name",), tuple())

def test_project_boards(project):
    assert not project.boards.list()

    board = project.boards.create({"name": "testboard"})
    board = project.boards.get(board.id)

    project.boards.delete(board.id)


def test_group_boards(group):
    assert not group.boards.list()

    board = group.boards.create({"name": "testboard"})
    board = group.boards.get(board.id)

    group.boards.delete(board.id)

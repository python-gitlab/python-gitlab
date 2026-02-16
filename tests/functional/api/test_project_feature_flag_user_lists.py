import pytest

from gitlab import exceptions


@pytest.fixture
def user_list(project, user):
    user_list = project.feature_flags_user_lists.create(
        {"name": "test_user_list", "user_xids": str(user.id)}
    )
    yield user_list
    try:
        user_list.delete()
    except exceptions.GitlabDeleteError:
        pass


def test_create_user_list(project, user):
    user_list = project.feature_flags_user_lists.create(
        {"name": "created_user_list", "user_xids": str(user.id)}
    )
    assert user_list.name == "created_user_list"
    assert str(user.id) in user_list.user_xids
    user_list.delete()


def test_list_user_lists(project, user_list):
    ff_user_lists = project.feature_flags_user_lists.list()
    assert len(ff_user_lists) >= 1
    assert user_list.iid in [ff_user.iid for ff_user in ff_user_lists]


def test_get_user_list(project, user_list, user):
    retrieved_list = project.feature_flags_user_lists.get(user_list.iid)
    assert retrieved_list.name == user_list.name
    assert str(user.id) in retrieved_list.user_xids


def test_update_user_list(project, user_list):
    user_list.name = "updated_user_list"
    user_list.save()

    updated_list = project.feature_flags_user_lists.get(user_list.iid)
    assert updated_list.name == "updated_user_list"


def test_delete_user_list(project, user_list):
    user_list.delete()
    with pytest.raises(exceptions.GitlabGetError):
        project.feature_flags_user_lists.get(user_list.iid)


def test_search_user_list(project, user_list):
    ff_user_lists = project.feature_flags_user_lists.list(search=user_list.name)
    assert len(ff_user_lists) >= 1
    assert user_list.iid in [ff_user.iid for ff_user in ff_user_lists]

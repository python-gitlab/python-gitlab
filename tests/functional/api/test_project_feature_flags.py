import pytest

from gitlab import exceptions


@pytest.fixture
def feature_flag(project):
    flag_name = "test_flag_fixture"
    flag = project.feature_flags.create(
        {"name": flag_name, "version": "new_version_flag"}
    )
    yield flag
    try:
        flag.delete()
    except exceptions.GitlabDeleteError:
        pass


def test_create_feature_flag(project):
    flag_name = "test_flag_create"
    flag = project.feature_flags.create(
        {"name": flag_name, "version": "new_version_flag"}
    )
    assert flag.name == flag_name
    assert flag.active is True
    flag.delete()


def test_create_feature_flag_with_strategies(project):
    flag_name = "test_flag_strategies"
    strategies = [{"name": "userWithId", "parameters": {"userIds": "user1"}}]
    flag = project.feature_flags.create(
        {"name": flag_name, "version": "new_version_flag", "strategies": strategies}
    )
    assert len(flag.strategies) == 1
    assert flag.strategies[0]["name"] == "userWithId"
    assert flag.strategies[0]["parameters"]["userIds"] == "user1"
    flag.delete()


def test_list_feature_flags(project, feature_flag):
    flags = project.feature_flags.list()
    assert len(flags) >= 1
    assert feature_flag.name in [f.name for f in flags]


def test_update_feature_flag(project, feature_flag):
    feature_flag.active = False
    feature_flag.save()

    updated_flag = project.feature_flags.get(feature_flag.name)
    assert updated_flag.active is False


def test_delete_feature_flag(project, feature_flag):
    feature_flag.delete()
    with pytest.raises(exceptions.GitlabGetError):
        project.feature_flags.get(feature_flag.name)

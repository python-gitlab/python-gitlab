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


def test_rename_feature_flag(project, feature_flag):
    # Rename via save()
    new_name = "renamed_flag"
    feature_flag.name = new_name
    feature_flag.save()

    updated_flag = project.feature_flags.get(new_name)
    assert updated_flag.name == new_name

    # Rename via update()
    newer_name = "renamed_flag_2"
    project.feature_flags.update(new_name, {"name": newer_name})

    updated_flag_2 = project.feature_flags.get(newer_name)
    assert updated_flag_2.name == newer_name

    # Update the fixture object so teardown can delete the correct flag
    feature_flag.name = newer_name


def test_delete_feature_flag(project, feature_flag):
    feature_flag.delete()
    with pytest.raises(exceptions.GitlabGetError):
        project.feature_flags.get(feature_flag.name)


def test_delete_feature_flag_strategy(project, feature_flag):
    strategies = [
        {"name": "default", "parameters": {}},
        {"name": "userWithId", "parameters": {"userIds": "user1"}},
    ]
    feature_flag.strategies = strategies
    feature_flag.save()

    feature_flag = project.feature_flags.get(feature_flag.name)
    assert len(feature_flag.strategies) == 2

    # Remove strategy using _destroy
    strategies = feature_flag.strategies
    for strategy in strategies:
        if strategy["name"] == "userWithId":
            strategy["_destroy"] = True
    feature_flag.save()

    feature_flag = project.feature_flags.get(feature_flag.name)
    assert len(feature_flag.strategies) == 1
    assert feature_flag.strategies[0]["name"] == "default"


def test_delete_feature_flag_scope(project, feature_flag):
    strategies = [
        {
            "name": "default",
            "parameters": {},
            "scopes": [{"environment_scope": "*"}, {"environment_scope": "production"}],
        }
    ]
    feature_flag.strategies = strategies
    feature_flag.save()

    feature_flag = project.feature_flags.get(feature_flag.name)
    assert len(feature_flag.strategies[0]["scopes"]) == 2

    # Remove scope using _destroy
    strategies = feature_flag.strategies
    for scope in strategies[0]["scopes"]:
        if scope["environment_scope"] == "production":
            scope["_destroy"] = True
    feature_flag.save()

    feature_flag = project.feature_flags.get(feature_flag.name)
    assert len(feature_flag.strategies[0]["scopes"]) == 1
    assert feature_flag.strategies[0]["scopes"][0]["environment_scope"] == "*"

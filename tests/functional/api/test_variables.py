"""
GitLab API:
https://docs.gitlab.com/ee/api/instance_level_ci_variables.html
https://docs.gitlab.com/ee/api/project_level_variables.html
https://docs.gitlab.com/ee/api/group_level_variables.html
"""


def test_instance_variables(gl):
    variable = gl.variables.create({"key": "key1", "value": "value1"})
    assert variable.value == "value1"
    assert variable in gl.variables.list()

    variable.value = "new_value1"
    variable.save()
    variable = gl.variables.get(variable.key)
    assert variable.value == "new_value1"

    variable.delete()


def test_group_variables(group):
    variable = group.variables.create({"key": "key1", "value": "value1"})
    assert variable.value == "value1"
    assert variable in group.variables.list()

    variable.value = "new_value1"
    variable.save()
    variable = group.variables.get(variable.key)
    assert variable.value == "new_value1"

    variable.delete()


def test_project_variables(project):
    variable = project.variables.create({"key": "key1", "value": "value1"})
    assert variable.value == "value1"
    assert variable in project.variables.list()

    variable.value = "new_value1"
    variable.save()
    variable = project.variables.get(variable.key)
    assert variable.value == "new_value1"

    variable.delete()


def test_hidden_group_variables(group):
    variable = group.variables.create(
        {"key": "key1", "value": "secret_value", "masked_and_hidden": True}
    )

    variable = group.variables.get(variable.key)
    assert variable.value is None
    assert variable.description is None
    assert variable in group.variables.list()

    variable.description = "new_description"
    variable.save()
    variable = group.variables.get(variable.key)
    assert variable.description == "new_description"

    variable.delete()


def test_hidden_project_variables(project):
    variable = project.variables.create(
        {"key": "key1", "value": "secret_value", "masked_and_hidden": True}
    )

    variable = project.variables.get(variable.key)
    assert variable.value is None
    assert variable.description is None
    assert variable in project.variables.list()

    variable.description = "new_description"
    variable.save()
    variable = project.variables.get(variable.key)
    assert variable.description == "new_description"

    variable.delete()

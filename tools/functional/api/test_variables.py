"""
GitLab API:
https://docs.gitlab.com/ee/api/instance_level_ci_variables.html
https://docs.gitlab.com/ee/api/project_level_variables.html
https://docs.gitlab.com/ee/api/group_level_variables.html
"""


def test_instance_variables(gl):
    variable = gl.variables.create({"key": "key1", "value": "value1"})
    assert variable.value == "value1"
    assert len(gl.variables.list()) == 1

    variable.value = "new_value1"
    variable.save()
    variable = gl.variables.get(variable.key)
    assert variable.value == "new_value1"

    variable.delete()
    assert len(gl.variables.list()) == 0


def test_group_variables(group):
    variable = group.variables.create({"key": "key1", "value": "value1"})
    assert variable.value == "value1"
    assert len(group.variables.list()) == 1

    variable.value = "new_value1"
    variable.save()
    variable = group.variables.get(variable.key)
    assert variable.value == "new_value1"

    variable.delete()
    assert len(group.variables.list()) == 0


def test_project_variables(project):
    variable = project.variables.create({"key": "key1", "value": "value1"})
    assert variable.value == "value1"
    assert len(project.variables.list()) == 1

    variable.value = "new_value1"
    variable.save()
    variable = project.variables.get(variable.key)
    assert variable.value == "new_value1"

    variable.delete()
    assert len(project.variables.list()) == 0

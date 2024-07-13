###############
CI/CD Variables
###############

You can configure variables at the instance-level (admin only), or associate
variables to projects and groups, to modify pipeline/job scripts behavior.

.. warning::

    Please always follow GitLab's `rules for CI/CD variables`_, especially for values
    in masked variables. If you do not, your variables may silently fail to save.

.. _rules for CI/CD variables: https://docs.gitlab.com/ee/ci/variables/#add-a-cicd-variable-to-a-project

Instance-level variables
========================

This endpoint requires admin access.

Reference
---------

* v4 API

  + :class:`gitlab.v4.objects.Variable`
  + :class:`gitlab.v4.objects.VariableManager`
  + :attr:`gitlab.Gitlab.variables`

* GitLab API

  + https://docs.gitlab.com/ce/api/instance_level_ci_variables.html

Examples
--------

List all instance variables::

    variables = gl.variables.list()

Get an instance variable by key::

    variable = gl.variables.get('key_name')

Create an instance variable::

    variable = gl.variables.create({'key': 'key1', 'value': 'value1'})

Update a variable value::

    variable.value = 'new_value'
    variable.save()

Remove a variable::

    gl.variables.delete('key_name')
    # or
    variable.delete()

Projects and groups variables
=============================

Reference
---------

* v4 API

  + :class:`gitlab.v4.objects.ProjectVariable`
  + :class:`gitlab.v4.objects.ProjectVariableManager`
  + :attr:`gitlab.v4.objects.Project.variables`
  + :class:`gitlab.v4.objects.GroupVariable`
  + :class:`gitlab.v4.objects.GroupVariableManager`
  + :attr:`gitlab.v4.objects.Group.variables`

* GitLab API

  + https://docs.gitlab.com/ce/api/instance_level_ci_variables.html
  + https://docs.gitlab.com/ce/api/project_level_variables.html
  + https://docs.gitlab.com/ce/api/group_level_variables.html

Examples
--------

List variables::

    p_variables = project.variables.list()
    g_variables = group.variables.list()

Get a variable::

    p_var = project.variables.get('key_name')
    g_var = group.variables.get('key_name')

.. note::

   If there are multiple variables with the same key, use ``filter`` to select
   the correct ``environment_scope``. See the GitLab API docs for more
   information.

Create a variable::

    var = project.variables.create({'key': 'key1', 'value': 'value1'})
    var = group.variables.create({'key': 'key1', 'value': 'value1'})

.. note::

   If a variable with the same key already exists, the new variable must have a
   different ``environment_scope``. Otherwise, GitLab returns a message similar
   to: ``VARIABLE_NAME has already been taken``. See the GitLab API docs for
   more information.

Update a variable value::

    var.value = 'new_value'
    var.save()
    # or
    project.variables.update("key1", {"value": "new_value"})

.. note::

   If there are multiple variables with the same key, use ``filter`` to select
   the correct ``environment_scope``. See the GitLab API docs for more
   information.

Remove a variable::

    project.variables.delete('key_name')
    group.variables.delete('key_name')
    # or
    var.delete()

.. note::

   If there are multiple variables with the same key, use ``filter`` to select
   the correct ``environment_scope``. See the GitLab API docs for more
   information.

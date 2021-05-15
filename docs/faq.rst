###
FAQ
###

I cannot edit the merge request / issue I've just retrieved
    It is likely that you used a ``MergeRequest``, ``GroupMergeRequest``,
    ``Issue`` or ``GroupIssue`` object. These objects cannot be edited. But you
    can create a new ``ProjectMergeRequest`` or ``ProjectIssue`` object to
    apply changes. For example::

        issue = gl.issues.list()[0]
        project = gl.projects.get(issue.project_id, lazy=True)
        editable_issue = project.issues.get(issue.iid, lazy=True)
        # you can now edit the object

    See the :ref:`merge requests example <merge_requests_examples>` and the
    :ref:`issues examples <issues_examples>`.

.. _attribute_error_list:

I get an ``AttributeError`` when accessing attributes of an object retrieved via a ``list()`` call.
    Fetching a list of objects, doesn’t always include all attributes in the
    objects. To retrieve an object with all attributes use a ``get()`` call.

    Example with projects::

        for projects in gl.projects.list():
            # Retrieve project object with all attributes
            project = gl.projects.get(project.id)

How can I clone the repository of a project?
    python-gitlab doesn't provide an API to clone a project. You have to use a
    git library or call the ``git`` command.

    The git URI is exposed in the ``ssh_url_to_repo`` attribute of ``Project``
    objects.

    Example::

        import subprocess

        project = gl.projects.create(data)  # or gl.projects.get(project_id)
        print(project.attributes)  # displays all the attributes
        git_url = project.ssh_url_to_repo
        subprocess.call(['git', 'clone', git_url])

I get an ``AttributeError`` when accessing attributes after ``save()`` or ``refresh()``.
    You are most likely trying to access an attribute that was not returned
    by the server on the second request. Please look at the documentation in
    :ref:`object_attributes` to see how to avoid this.

I passed ``all=True`` (or ``--all`` via the CLI) to the API and I still cannot see all items returned.
    Use ``get_all=True`` (or ``--get-all`` via the CLI). See :ref:`pagination` for more details.

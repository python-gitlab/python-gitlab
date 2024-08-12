###
FAQ
###

General
-------

I cannot edit the merge request / issue I've just retrieved.
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

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

How can I clone the repository of a project?
""""""""""""""""""""""""""""""""""""""""""""

python-gitlab does not provide an API to clone a project. You have to use a
git library or call the ``git`` command.

The git URI is exposed in the ``ssh_url_to_repo`` attribute of ``Project``
objects.

Example::

    import subprocess

    project = gl.projects.create(data)  # or gl.projects.get(project_id)
    print(project.attributes)  # displays all the attributes
    git_url = project.ssh_url_to_repo
    subprocess.call(['git', 'clone', git_url])

Not all items are returned from the API
"""""""""""""""""""""""""""""""""""""""

If you've passed ``all=True`` to the API and still cannot see all items returned,
use ``get_all=True`` (or ``--get-all`` via the CLI) instead. See :ref:`pagination` for more details.

Common errors
-------------

.. _attribute_error_list:

``AttributeError`` when accessing object attributes retrieved via ``list()``
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

Fetching a list of objects does not always include all attributes in the objects.
To retrieve an object with all attributes, use a ``get()`` call.

Example with projects::

    for project in gl.projects.list():
        # Retrieve project object with all attributes
        project = gl.projects.get(project.id)

``AttributeError`` when accessing attributes after ``save()`` or ``refresh()``
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

You are most likely trying to access an attribute that was not returned
by the server on the second request. Please look at the documentation in
:ref:`object_attributes` to see how to avoid this.

``TypeError`` when accessing object attributes
""""""""""""""""""""""""""""""""""""""""""""""

When you encounter errors such as ``object is not iterable`` or ``object is not subscriptable``
when trying to access object attributes returned from the server, you are most likely trying to
access an attribute that is shadowed by python-gitlab's own methods or managers.

You can use the object's ``attributes`` dictionary to access it directly instead.
See the :ref:`objects` section for more details on how attributes are exposed.

.. _conflicting_parameters_faq:

I cannot use the parameter ``path`` (or some other parameter) as it conflicts with the library
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

``path`` is used by the python-gitlab library and cannot be used as a parameter
if wanting to send it to the GitLab instance.  You can use the
``query_parameters`` argument to send arguments that would conflict with python
or python-gitlab when using them as kwargs:

.. code-block:: python

   ## invalid, as ``path`` is interpreted by python-gitlab as the Path or full
   ## URL to query ('/projects' or 'http://whatever/v4/api/projects')
   project.commits.list(path='some_file_path', iterator=True)

   project.commits.list(query_parameters={'path': 'some_file_path'}, iterator=True)  # OK

See :ref:`Conflicting Parameters <conflicting_parameters>` for more information.

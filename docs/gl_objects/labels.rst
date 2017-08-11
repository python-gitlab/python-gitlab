######
Labels
######

Reference
---------

* v4 API:

  + :class:`gitlab.v4.objects.ProjectLabel`
  + :class:`gitlab.v4.objects.ProjectLabelManager`
  + :attr:`gitlab.v4.objects.Project.labels`

* v3 API:

  + :class:`gitlab.v3.objects.ProjectLabel`
  + :class:`gitlab.v3.objects.ProjectLabelManager`
  + :attr:`gitlab.v3.objects.Project.labels`
  + :attr:`gitlab.Gitlab.project_labels`

* GitLab API: https://docs.gitlab.com/ce/api/labels.html

Examples
--------

List labels for a project:

.. literalinclude:: labels.py
   :start-after: # list
   :end-before: # end list

Get a single label:

.. literalinclude:: labels.py
   :start-after: # get
   :end-before: # end get

Create a label for a project:

.. literalinclude:: labels.py
   :start-after: # create
   :end-before: # end create

Update a label for a project:

.. literalinclude:: labels.py
   :start-after: # update
   :end-before: # end update

Delete a label for a project:

.. literalinclude:: labels.py
   :start-after: # delete
   :end-before: # end delete

######
Labels
######

Use :class:`~gitlab.objects.ProjectLabel` objects to manipulate labels for
projects. The :attr:`gitlab.Gitlab.project_labels` and :attr:`Project.labels
<gitlab.objects.Project.labels>` manager objects provide helper functions.

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

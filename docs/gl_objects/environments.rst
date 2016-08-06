############
Environments
############

Use :class:`~gitlab.objects.ProjectEnvironment` objects to manipulate
environments for projects. The :attr:`gitlab.Gitlab.project_environments` and
:attr:`Project.environments <gitlab.objects.Project.environments>` manager
objects provide helper functions.

Examples
--------

List environments for a project:

.. literalinclude:: environments.py
   :start-after: # list
   :end-before: # end list

Get a single environment:

.. literalinclude:: environments.py
   :start-after: # get
   :end-before: # end get

Create an environment for a project:

.. literalinclude:: environments.py
   :start-after: # create
   :end-before: # end create

Update an environment for a project:

.. literalinclude:: environments.py
   :start-after: # update
   :end-before: # end update

Delete an environment for a project:

.. literalinclude:: environments.py
   :start-after: # delete
   :end-before: # end delete

############
Environments
############

Reference
---------

* v4 API:

  + :class:`gitlab.v4.objects.ProjectEnvironment`
  + :class:`gitlab.v4.objects.ProjectEnvironmentManager`
  + :attr:`gitlab.v4.objects.Project.environments`

* v3 API:

  + :class:`gitlab.v3.objects.ProjectEnvironment`
  + :class:`gitlab.v3.objects.ProjectEnvironmentManager`
  + :attr:`gitlab.v3.objects.Project.environments`
  + :attr:`gitlab.Gitlab.project_environments`

* GitLab API: https://docs.gitlab.com/ce/api/environments.html

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

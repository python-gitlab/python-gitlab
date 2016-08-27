###########
Deployments
###########

Use :class:`~gitlab.objects.ProjectDeployment` objects to manipulate project
deployments. The :attr:`gitlab.Gitlab.project_deployments`, and
:attr:`Project.deployments <gitlab.objects.Project.deployments>` manager
objects provide helper functions.

Examples
--------

List deployments for a project:

.. literalinclude:: deployments.py
   :start-after: # list
   :end-before: # end list

Get a single deployment:

.. literalinclude:: deployments.py
   :start-after: # get
   :end-before: # end get

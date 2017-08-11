###########
Deployments
###########

Reference
---------

* v4 API:

  + :class:`gitlab.v4.objects.ProjectDeployment`
  + :class:`gitlab.v4.objects.ProjectDeploymentManager`
  + :attr:`gitlab.v4.objects.Project.deployments`

* v3 API:

  + :class:`gitlab.v3.objects.ProjectDeployment`
  + :class:`gitlab.v3.objects.ProjectDeploymentManager`
  + :attr:`gitlab.v3.objects.Project.deployments`
  + :attr:`gitlab.Gitlab.project_deployments`

* GitLab API: https://docs.gitlab.com/ce/api/deployments.html

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

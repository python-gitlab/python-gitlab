###########
Deployments
###########

Reference
---------

* v4 API:

  + :class:`gitlab.v4.objects.ProjectDeployment`
  + :class:`gitlab.v4.objects.ProjectDeploymentManager`
  + :attr:`gitlab.v4.objects.Project.deployments`

* GitLab API: https://docs.gitlab.com/ce/api/deployments.html

Examples
--------

List deployments for a project::

    deployments = project.deployments.list()

Get a single deployment::

    deployment = project.deployments.get(deployment_id)

Create a new deployment::

    deployment = project.deployments.create({
        "environment": "Test",
        "sha": "1agf4gs",
        "ref": "main",
        "tag": False,
        "status": "created",
    })

Update a deployment::

    deployment = project.deployments.get(42)
    deployment.status = "failed"
    deployment.save()

Merge requests associated with a deployment
===========================================

Reference
----------

* v4 API:

  + :class:`gitlab.v4.objects.ProjectDeploymentMergeRequest`
  + :class:`gitlab.v4.objects.ProjectDeploymentMergeRequestManager`
  + :attr:`gitlab.v4.objects.ProjectDeployment.mergerequests`

* GitLab API: https://docs.gitlab.com/ee/api/deployments.html#list-of-merge-requests-associated-with-a-deployment

Examples
--------

List the merge requests associated with a deployment::

    deployment = project.deployments.get(42, lazy=True)
    mrs = deployment.mergerequests.list()

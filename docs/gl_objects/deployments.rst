###########
Deployments
###########

Reference
---------

* v4 API:

  + :class:`gitlab.v4.objects.ProjectDeployment`
  + :class:`gitlab.v4.objects.ProjectDeploymentManager`
  + :attr:`gitlab.v4.objects.Project.deployments`

* GitLab API: https://docs.gitlab.com/api/deployments

Examples
--------

List deployments for a project::

    deployments = project.deployments.list(get_all=True)

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

Approve a deployment::

    deployment = project.deployments.get(42)
    # `status` must be either "approved" or "rejected".
    deployment.approval(status="approved")

Reject a deployment::

    deployment = project.deployments.get(42)
    # Using the optional `comment` and `represented_as` arguments
    deployment.approval(status="rejected", comment="Fails CI", represented_as="security")

Merge requests associated with a deployment
===========================================

Reference
----------

* v4 API:

  + :class:`gitlab.v4.objects.ProjectDeploymentMergeRequest`
  + :class:`gitlab.v4.objects.ProjectDeploymentMergeRequestManager`
  + :attr:`gitlab.v4.objects.ProjectDeployment.mergerequests`

* GitLab API: https://docs.gitlab.com/api/deployments#list-of-merge-requests-associated-with-a-deployment

Examples
--------

List the merge requests associated with a deployment::

    deployment = project.deployments.get(42, lazy=True)
    mrs = deployment.mergerequests.list(get_all=True)

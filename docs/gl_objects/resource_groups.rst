###############
Resource Groups
###############

Reference
---------

* v4 API:

  + :class:`gitlab.v4.objects.ProjectResourceGroup`
  + :class:`gitlab.v4.objects.ProjectResourceGroupManager`
  + :attr:`gitlab.v4.objects.Project.resource_groups`
  + :class:`gitlab.v4.objects.ProjectResourceGroupUpcomingJob`
  + :class:`gitlab.v4.objects.ProjectResourceGroupUpcomingJobManager`
  + :attr:`gitlab.v4.objects.ProjectResourceGroup.upcoming_jobs`

* Gitlab API: https://docs.gitlab.com/ee/api/resource_groups.html

Examples
--------

List resource groups for a project::

    project = gl.projects.get(project_id, lazy=True)
    resource_group = project.resource_groups.list()

Get a single resource group::

    resource_group = project.resource_groups.get("production")

Edit a resource group::

    resource_group.process_mode = "oldest_first"
    resource_group.save()

List upcoming jobs for a resource group::

    upcoming_jobs = resource_group.upcoming_jobs.list()

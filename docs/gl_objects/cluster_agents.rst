##############
Cluster agents
##############

You can list and manage project cluster agents with the GitLab agent for Kubernetes.

.. warning::
   Check the GitLab API documentation linked below for project permissions
   required to access specific cluster agent endpoints.

Reference
---------

* v4 API:

  + :class:`gitlab.v4.objects.ProjectClusterAgent`
  + :class:`gitlab.v4.objects.ProjectClusterAgentManager`
  + :attr:`gitlab.v4.objects.Project.cluster_agents`

* GitLab API: https://docs.gitlab.com/ee/api/cluster_agents.html

Examples
--------

List cluster agents for a project::

    cluster_agents = project.cluster_agents.list()

Register a cluster agent with a project::

    cluster_agent = project.cluster_agents.create({"name": "Agent 1"})

Retrieve a specific cluster agent for a project::

    cluster_agent = project.cluster_agents.get(cluster_agent.id)

Delete a registered cluster agent from a project::

    cluster_agent = project.cluster_agents.delete(cluster_agent.id)
    # or
    cluster.delete()

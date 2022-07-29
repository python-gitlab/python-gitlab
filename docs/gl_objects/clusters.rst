#####################
Clusters (DEPRECATED) 
#####################

.. warning::
   Cluster support was deprecated in GitLab 14.5 and disabled by default as of
   GitLab 15.0


Reference
---------

* v4 API:

  + :class:`gitlab.v4.objects.ProjectCluster`
  + :class:`gitlab.v4.objects.ProjectClusterManager`
  + :attr:`gitlab.v4.objects.Project.clusters`
  + :class:`gitlab.v4.objects.GroupCluster`
  + :class:`gitlab.v4.objects.GroupClusterManager`
  + :attr:`gitlab.v4.objects.Group.clusters`

* GitLab API: https://docs.gitlab.com/ee/api/project_clusters.html
* GitLab API: https://docs.gitlab.com/ee/api/group_clusters.html

Examples
--------

List clusters for a project::

    clusters = project.clusters.list()

Create an cluster for a project::

    cluster = project.clusters.create(
    {
        "name": "cluster1",
        "platform_kubernetes_attributes": {
            "api_url": "http://url",
            "token": "tokenval",
        },
    })

Retrieve a specific cluster for a project::

    cluster = project.clusters.get(cluster_id)

Update an cluster for a project::

    cluster.platform_kubernetes_attributes = {"api_url": "http://newurl"}
    cluster.save()

Delete an cluster for a project::

    cluster = project.clusters.delete(cluster_id)
    # or
    cluster.delete()


List clusters for a group::

    clusters = group.clusters.list()

Create an cluster for a group::

    cluster = group.clusters.create(
    {
        "name": "cluster1",
        "platform_kubernetes_attributes": {
            "api_url": "http://url",
            "token": "tokenval",
        },
    })

Retrieve a specific cluster for a group::

    cluster = group.clusters.get(cluster_id)

Update an cluster for a group::

    cluster.platform_kubernetes_attributes = {"api_url": "http://newurl"}
    cluster.save()

Delete an cluster for a group::

    cluster = group.clusters.delete(cluster_id)
    # or
    cluster.delete()

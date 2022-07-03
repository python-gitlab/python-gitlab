def test_project_clusters(project):
    cluster = project.clusters.create(
        {
            "name": "cluster1",
            "platform_kubernetes_attributes": {
                "api_url": "http://url",
                "token": "tokenval",
            },
        }
    )
    clusters = project.clusters.list()
    assert cluster in clusters

    cluster.platform_kubernetes_attributes = {"api_url": "http://newurl"}
    cluster.save()

    cluster = project.clusters.list()[0]
    assert cluster.platform_kubernetes["api_url"] == "http://newurl"

    cluster.delete()
    assert cluster not in project.clusters.list()


def test_group_clusters(group):
    cluster = group.clusters.create(
        {
            "name": "cluster1",
            "platform_kubernetes_attributes": {
                "api_url": "http://url",
                "token": "tokenval",
            },
        }
    )
    clusters = group.clusters.list()
    assert cluster in clusters

    cluster.platform_kubernetes_attributes = {"api_url": "http://newurl"}
    cluster.save()

    cluster = group.clusters.list()[0]
    assert cluster.platform_kubernetes["api_url"] == "http://newurl"

    cluster.delete()
    assert cluster not in group.clusters.list()

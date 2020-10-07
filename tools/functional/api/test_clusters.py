def test_project_clusters(project):
    project.clusters.create(
        {
            "name": "cluster1",
            "platform_kubernetes_attributes": {
                "api_url": "http://url",
                "token": "tokenval",
            },
        }
    )
    clusters = project.clusters.list()
    assert len(clusters) == 1

    cluster = clusters[0]
    cluster.platform_kubernetes_attributes = {"api_url": "http://newurl"}
    cluster.save()

    cluster = project.clusters.list()[0]
    assert cluster.platform_kubernetes["api_url"] == "http://newurl"

    cluster.delete()
    assert len(project.clusters.list()) == 0


def test_group_clusters(group):
    group.clusters.create(
        {
            "name": "cluster1",
            "platform_kubernetes_attributes": {
                "api_url": "http://url",
                "token": "tokenval",
            },
        }
    )
    clusters = group.clusters.list()
    assert len(clusters) == 1

    cluster = clusters[0]
    cluster.platform_kubernetes_attributes = {"api_url": "http://newurl"}
    cluster.save()

    cluster = group.clusters.list()[0]
    assert cluster.platform_kubernetes["api_url"] == "http://newurl"

    cluster.delete()
    assert len(group.clusters.list()) == 0

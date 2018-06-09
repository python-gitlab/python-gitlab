#########
Geo nodes
#########

Reference
---------

* v4 API:

  + :class:`gitlab.v4.objects.GeoNode`
  + :class:`gitlab.v4.objects.GeoNodeManager`
  + :attr:`gitlab.Gitlab.geonodes`

* GitLab API: https://docs.gitlab.com/ee/api/geo_nodes.html (EE feature)

Examples
--------

List the geo nodes::

    nodes = gl.geonodes.list()

Get the status of all the nodes::

    status = gl.geonodes.status()

Get a specific node and its status::

    node = gl.geonodes.get(node_id)
    node.status()

Edit a node configuration::

    node.url = 'https://secondary.mygitlab.domain'
    node.save()

Delete a node::

    node.delete()

List the sync failure on the current node::

    failures = gl.geonodes.current_failures()

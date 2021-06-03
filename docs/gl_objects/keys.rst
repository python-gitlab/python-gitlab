####
Keys
####

Keys
====

Reference
---------

* v4 API

  + :class:`gitlab.v4.objects.Key`
  + :class:`gitlab.v4.objects.KeyManager`
  + :attr:`gitlab.Gitlab.keys`

* GitLab API: https://docs.gitlab.com/ce/api/keys.html

Examples
--------

Get an ssh key by its id (requires admin access)::

    key = gl.keys.get(key_id)

Get an ssh key (requires admin access) or a deploy key by its fingerprint::

    key = gl.keys.get(fingerprint="SHA256:ERJJ/OweAM6jA8OjJ/gXs4N5fqUaREEJnz/EyfywfXY")

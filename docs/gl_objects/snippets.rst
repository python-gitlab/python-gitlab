########
Snippets
########

Reference
=========

* v4 API:

  + :class:`gitlab.v4.objects.Snippet`
  + :class:`gitlab.v4.objects.SnipptManager`
  + :attr:`gilab.Gitlab.snippets`

* GitLab API: https://docs.gitlab.com/ce/api/snippets.html

Examples
========

List snippets owned by the current user::

    snippets = gl.snippets.list()

List the public snippets::

    public_snippets = gl.snippets.public()

Get a snippet::

    snippet = gl.snippets.get(snippet_id)
    # get the content
    content = snippet.content()

.. warning::

   Blobs are entirely stored in memory unless you use the streaming feature.
   See :ref:`the artifacts example <streaming_example>`.


Create a snippet::

    snippet = gl.snippets.create({'title': 'snippet1',
                                  'file_name': 'snippet1.py',
                                  'content': open('snippet1.py').read()})

Update a snippet::

    snippet.visibility_level = gitlab.Project.VISIBILITY_PUBLIC
    snippet.save()

Delete a snippet::

    gl.snippets.delete(snippet_id)
    # or
    snippet.delete()

Get user agent detail (admin only)::

    detail = snippet.user_agent_detail()

########
Snippets
########

Reference
=========

* v4 API:

  + :class:`gitlab.v4.objects.Snippet`
  + :class:`gitlab.v4.objects.SnipptManager`
  + :attr:`gitlab.Gitlab.snippets`

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

Update the snippet attributes::

    snippet.visibility_level = gitlab.const.Visibility.PUBLIC
    snippet.save()

To update a snippet code you need to create a ``ProjectSnippet`` object::

    snippet = gl.snippets.get(snippet_id)
    project = gl.projects.get(snippet.projec_id, lazy=True)
    editable_snippet = project.snippets.get(snippet.id)
    editable_snippet.code = new_snippet_content
    editable_snippet.save()

Delete a snippet::

    gl.snippets.delete(snippet_id)
    # or
    snippet.delete()

Get user agent detail (admin only)::

    detail = snippet.user_agent_detail()

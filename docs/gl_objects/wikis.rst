##########
Wiki pages
##########


References
==========

* v4 API:

  + :class:`gitlab.v4.objects.ProjectWiki`
  + :class:`gitlab.v4.objects.ProjectWikiManager`
  + :attr:`gitlab.v4.objects.Project.wikis`

* GitLab API: https://docs.gitlab.com/ce/api/wikis.html

Examples
--------

Get the list of wiki pages for a project::

    pages = project.wikis.list()

Get a single wiki page::

    page = project.wikis.get(page_slug)

Create a wiki page::

    page = project.wikis.create({'title': 'Wiki Page 1',
                                 'content': open(a_file).read()})

Update a wiki page::

    page.content = 'My new content'
    page.save()

Delete a wiki page::

    page.delete()

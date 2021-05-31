##########
Wiki pages
##########


References
==========

* v4 API:

  + :class:`gitlab.v4.objects.ProjectWiki`
  + :class:`gitlab.v4.objects.ProjectWikiManager`
  + :attr:`gitlab.v4.objects.Project.wikis`
  + :class:`gitlab.v4.objects.GroupWiki`
  + :class:`gitlab.v4.objects.GroupWikiManager`
  + :attr:`gitlab.v4.objects.Group.wikis`

* GitLab API for Projects: https://docs.gitlab.com/ce/api/wikis.html
* GitLab API for Groups: https://docs.gitlab.com/ee/api/group_wikis.html

Examples
--------

Get the list of wiki pages for a project. These do not contain the contents of the wiki page. You will need to call get(slug) to retrieve the content by accessing the content attribute::

    pages = project.wikis.list()

Get the list of wiki pages for a group. These do not contain the contents of the wiki page. You will need to call get(slug) to retrieve the content by accessing the content attribute::

    pages = group.wikis.list()

Get a single wiki page for a project::

    page = project.wikis.get(page_slug)

Get a single wiki page for a group::

    page = group.wikis.get(page_slug)

Get the contents of a wiki page::

    print(page.content)

Create a wiki page on a project level::

    page = project.wikis.create({'title': 'Wiki Page 1',
                                 'content': open(a_file).read()})

Update a wiki page::

    page.content = 'My new content'
    page.save()

Delete a wiki page::

    page.delete()

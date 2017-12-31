#############
Pages domains
#############

Admin
=====

References
----------

* v4 API:

  + :class:`gitlab.v4.objects.PagesDomain`
  + :class:`gitlab.v4.objects.PagesDomainManager`
  + :attr:`gitlab.Gitlab.pagesdomains`

* GitLab API: https://docs.gitlab.com/ce/api/pages_domains.html#list-all-pages-domains

Examples
--------

List all the existing domains (admin only)::

    domains = gl.pagesdomains.list()

Project pages domain
====================

References
----------

* v4 API:

  + :class:`gitlab.v4.objects.ProjectPagesDomain`
  + :class:`gitlab.v4.objects.ProjectPagesDomainManager`
  + :attr:`gitlab.v4.objects.Project.pagesdomains`

* GitLab API: https://docs.gitlab.com/ce/api/pages_domains.html#list-pages-domains

Examples
--------

List domains for a project::

    domains = project.pagesdomains.list()

Get a single domain::

    domain = project.pagesdomains.get('d1.example.com')

Create a new domain::

    domain = project.pagesdomains.create({'domain': 'd2.example.com})

Update an existing domain::

    domain.certificate = open('d2.crt').read()
    domain.key = open('d2.key').read()
    domain.save()

Delete an existing domain::

    domain.delete
    # or
    project.pagesdomains.delete('d2.example.com')

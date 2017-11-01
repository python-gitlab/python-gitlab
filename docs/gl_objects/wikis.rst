##########
Wiki pages
##########


References
==========

* v4 API:

  + :class:`gitlab.v4.objects.ProjectWiki`
  + :class:`gitlab.v4.objects.ProjectWikiManager`
  + :attr:`gitlab.v4.objects.Project.wikis`

Examples
--------

Get the list of wiki pages for a project:

.. literalinclude:: wikis.py
   :start-after: # list
   :end-before: # end list

Get a single wiki page:

.. literalinclude:: wikis.py
   :start-after: # get
   :end-before: # end get

Create a wiki page:

.. literalinclude:: wikis.py
   :start-after: # create
   :end-before: # end create

Update a wiki page:

.. literalinclude:: wikis.py
   :start-after: # update
   :end-before: # end update

Delete a wiki page:

.. literalinclude:: wikis.py
   :start-after: # delete
   :end-before: # end delete

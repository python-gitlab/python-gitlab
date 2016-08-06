########
Licenses
########

Use :class:`~gitlab.objects.License` objects to manipulate licenses. The
:attr:`gitlab.Gitlab.licenses` manager object provides helper functions.

Examples
--------

List known licenses:

.. literalinclude:: licenses.py
   :start-after: # list
   :end-before: # end list

Generate a license content for a project:

.. literalinclude:: licenses.py
   :start-after: # get
   :end-before: # end get

#########
Templates
#########

You can request templates for different type of files:

* License files
* .gitignore files
* GitLab CI configuration files

License templates
=================

* Object class: :class:`~gitlab.objects.License`
* Manager object: :attr:`gitlab.Gitlab.licenses`

Examples
--------

List known license templates:

.. literalinclude:: templates.py
   :start-after: # license list
   :end-before: # end license list

Generate a license content for a project:

.. literalinclude:: templates.py
   :start-after: # license get
   :end-before: # end license get

.gitignore templates
====================

* Object class: :class:`~gitlab.objects.Gitignore`
* Manager object: :attr:`gitlab.Gitlab.gitognores`

Examples
--------

List known gitignore templates:

.. literalinclude:: templates.py
   :start-after: # gitignore list
   :end-before: # end gitignore list

Get a gitignore template:

.. literalinclude:: templates.py
   :start-after: # gitignore get
   :end-before: # end gitignore get

GitLab CI templates
===================

* Object class: :class:`~gitlab.objects.Gitlabciyml`
* Manager object: :attr:`gitlab.Gitlab.gitlabciymls`

Examples
--------

List known GitLab CI templates:

.. literalinclude:: templates.py
   :start-after: # gitlabciyml list
   :end-before: # end gitlabciyml list

Get a GitLab CI template:

.. literalinclude:: templates.py
   :start-after: # gitlabciyml get
   :end-before: # end gitlabciyml get

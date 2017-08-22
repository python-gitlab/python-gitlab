#########
Templates
#########

You can request templates for different type of files:

* License files
* .gitignore files
* GitLab CI configuration files
* Dockerfiles

License templates
=================

Reference
---------

* v4 API:

  + :class:`gitlab.v4.objects.License`
  + :class:`gitlab.v4.objects.LicenseManager`
  + :attr:`gitlab.Gitlab.licenses`

* v3 API:

  + :class:`gitlab.v3.objects.License`
  + :class:`gitlab.v3.objects.LicenseManager`
  + :attr:`gitlab.Gitlab.licenses`

* GitLab API: https://docs.gitlab.com/ce/api/templates/licenses.html

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

Reference
---------

* v4 API:

  + :class:`gitlab.v4.objects.Gitignore`
  + :class:`gitlab.v4.objects.GitignoreManager`
  + :attr:`gitlab.Gitlab.gitignores`

* v3 API:

  + :class:`gitlab.v3.objects.Gitignore`
  + :class:`gitlab.v3.objects.GitignoreManager`
  + :attr:`gitlab.Gitlab.gitignores`

* GitLab API: https://docs.gitlab.com/ce/api/templates/gitignores.html

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

Reference
---------

* v4 API:

  + :class:`gitlab.v4.objects.Gitlabciyml`
  + :class:`gitlab.v4.objects.GitlabciymlManager`
  + :attr:`gitlab.Gitlab.gitlabciymls`

* v3 API:

  + :class:`gitlab.v3.objects.Gitlabciyml`
  + :class:`gitlab.v3.objects.GitlabciymlManager`
  + :attr:`gitlab.Gitlab.gitlabciymls`

* GitLab API: https://docs.gitlab.com/ce/api/templates/gitlab_ci_ymls.html

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

Dockerfile templates
====================

Reference
---------

* v4 API:

  + :class:`gitlab.v4.objects.Dockerfile`
  + :class:`gitlab.v4.objects.DockerfileManager`
  + :attr:`gitlab.Gitlab.gitlabciymls`

* GitLab API: Not documented.

Examples
--------

List known Dockerfile templates:

.. literalinclude:: templates.py
   :start-after: # dockerfile list
   :end-before: # end dockerfile list

Get a Dockerfile template:

.. literalinclude:: templates.py
   :start-after: # dockerfile get
   :end-before: # end dockerfile get

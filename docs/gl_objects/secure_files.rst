############
Secure Files
############

secure files
============

References
----------

* v4 API:

  + :class:`gitlab.v4.objects.ProjectSecureFile`
  + :class:`gitlab.v4.objects.ProjectSecureFileManager`
  + :attr:`gitlab.v4.objects.Project.secure_files`

* GitLab API: https://docs.gitlab.com/ee/api/secure_files.html

Examples
--------

Get a project secure file::

    secure_files = gl.projects.get(1, lazy=True).secure_files.get(1)
    print(secure_files.name)

List project secure files::

    secure_files = gl.projects.get(1, lazy=True).secure_files.list()
    print(secure_files[0].name)

Create project secure file::

    secure_file = gl.projects.get(1).secure_files.create({"name": "test", "file": "secure.txt"})

Download a project secure file::

    content = secure_file.download()
    print(content)
    with open("/tmp/secure.txt", "wb") as f:
        secure_file.download(streamed=True, action=f.write)

Remove a project secure file::

    gl.projects.get(1).secure_files.delete(1)
    # or
    secure_file.delete()

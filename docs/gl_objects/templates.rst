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

* GitLab API: https://docs.gitlab.com/ce/api/templates/licenses.html

Examples
--------

List known license templates::

    licenses = gl.licenses.list()

Generate a license content for a project::

    license = gl.licenses.get('apache-2.0', project='foobar', fullname='John Doe')
    print(license.content)

.gitignore templates
====================

Reference
---------

* v4 API:

  + :class:`gitlab.v4.objects.Gitignore`
  + :class:`gitlab.v4.objects.GitignoreManager`
  + :attr:`gitlab.Gitlab.gitignores`

* GitLab API: https://docs.gitlab.com/ce/api/templates/gitignores.html

Examples
--------

List known gitignore templates::

    gitignores = gl.gitignores.list()

Get a gitignore template::

    gitignore = gl.gitignores.get('Python')
    print(gitignore.content)

GitLab CI templates
===================

Reference
---------

* v4 API:

  + :class:`gitlab.v4.objects.Gitlabciyml`
  + :class:`gitlab.v4.objects.GitlabciymlManager`
  + :attr:`gitlab.Gitlab.gitlabciymls`

* GitLab API: https://docs.gitlab.com/ce/api/templates/gitlab_ci_ymls.html

Examples
--------

List known GitLab CI templates::

    gitlabciymls = gl.gitlabciymls.list()

Get a GitLab CI template::

    gitlabciyml = gl.gitlabciymls.get('Pelican')
    print(gitlabciyml.content)

Dockerfile templates
====================

Reference
---------

* v4 API:

  + :class:`gitlab.v4.objects.Dockerfile`
  + :class:`gitlab.v4.objects.DockerfileManager`
  + :attr:`gitlab.Gitlab.gitlabciymls`

* GitLab API: https://docs.gitlab.com/ce/api/templates/dockerfiles.html

Examples
--------

List known Dockerfile templates::

    dockerfiles = gl.dockerfiles.list()

Get a Dockerfile template::

    dockerfile = gl.dockerfiles.get('Python')
    print(dockerfile.content)

Project templates
=========================

These templates are project-specific versions of the templates above, as
well as issue and merge request templates.

Reference
---------

* v4 API:

  + :class:`gitlab.v4.objects.ProjectLicenseTemplate`
  + :class:`gitlab.v4.objects.ProjectLicenseTemplateManager`
  + :attr:`gitlab.v4.objects.Project.license_templates`
  + :class:`gitlab.v4.objects.ProjectGitignoreTemplate`
  + :class:`gitlab.v4.objects.ProjectGitignoreTemplateManager`
  + :attr:`gitlab.v4.objects.Project.gitignore_templates`
  + :class:`gitlab.v4.objects.ProjectGitlabciymlTemplate`
  + :class:`gitlab.v4.objects.ProjectGitlabciymlTemplateManager`
  + :attr:`gitlab.v4.objects.Project.gitlabciyml_templates`
  + :class:`gitlab.v4.objects.ProjectDockerfileTemplate`
  + :class:`gitlab.v4.objects.ProjectDockerfileTemplateManager`
  + :attr:`gitlab.v4.objects.Project.dockerfile_templates`
  + :class:`gitlab.v4.objects.ProjectIssueTemplate`
  + :class:`gitlab.v4.objects.ProjectIssueTemplateManager`
  + :attr:`gitlab.v4.objects.Project.issue_templates`
  + :class:`gitlab.v4.objects.ProjectMergeRequestTemplate`
  + :class:`gitlab.v4.objects.ProjectMergeRequestTemplateManager`
  + :attr:`gitlab.v4.objects.Project.merge_request_templates`

* GitLab API: https://docs.gitlab.com/ce/api/project_templates.html

Examples
--------

List known project templates::

    license_templates = project.license_templates.list()
    gitignore_templates = project.gitignore_templates.list()
    gitlabciyml_templates = project.gitlabciyml_templates.list()
    dockerfile_templates = project.dockerfile_templates.list()
    issue_templates = project.issue_templates.list()
    merge_request_templates = project.merge_request_templates.list()

Get project templates::
  
      license_template = project.license_templates.get('apache-2.0')
      gitignore_template = project.gitignore_templates.get('Python')
      gitlabciyml_template = project.gitlabciyml_templates.get('Pelican')
      dockerfile_template = project.dockerfile_templates.get('Python')
      issue_template = project.issue_templates.get('Default')
      merge_request_template = project.merge_request_templates.get('Default')

      print(license_template.content)
      print(gitignore_template.content)
      print(gitlabciyml_template.content)
      print(dockerfile_template.content)
      print(issue_template.content)
      print(merge_request_template.content)

Create an issue or merge request using a description template::

      issue = project.issues.create({'title': 'I have a bug',
                                     'description': issue_template.content})
      mr = project.mergerequests.create({'source_branch': 'cool_feature',
                                        'target_branch': 'main',
                                        'title': 'merge cool feature',
                                        'description': merge_request_template.content})
                          
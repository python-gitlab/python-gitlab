########
Projects
########

Projects
========

Reference
---------

* v4 API:

  + :class:`gitlab.v4.objects.Project`
  + :class:`gitlab.v4.objects.ProjectManager`
  + :attr:`gitlab.Gitlab.projects`

* GitLab API: https://docs.gitlab.com/ce/api/projects.html

Examples
--------

List projects::

    projects = gl.projects.list()

The API provides several filtering parameters for the listing methods:

* ``archived``: if ``True`` only archived projects will be returned
* ``visibility``: returns only projects with the specified visibility (can be
  ``public``, ``internal`` or ``private``)
* ``search``: returns project matching the given pattern

Results can also be sorted using the following parameters:

* ``order_by``: sort using the given argument. Valid values are ``id``,
  ``name``, ``path``, ``created_at``, ``updated_at`` and ``last_activity_at``.
  The default is to sort by ``created_at``
* ``sort``: sort order (``asc`` or ``desc``)

::

    # List all projects (default 20)
    projects = gl.projects.list(get_all=True)
    # Archived projects
    projects = gl.projects.list(archived=1)
    # Limit to projects with a defined visibility
    projects = gl.projects.list(visibility='public')

    # List owned projects
    projects = gl.projects.list(owned=True)

    # List starred projects
    projects = gl.projects.list(starred=True)

    # Search projects
    projects = gl.projects.list(search='keyword')

.. note::

   To list the starred projects of another user, see the
   :ref:`Users API docs <users_examples>`.

.. note::

   Fetching a list of projects, doesn't include all attributes of all projects.
   To retrieve all attributes, you'll need to fetch a single project

Get a single project::

    # Get a project by ID
    project_id = 851
    project = gl.projects.get(project_id)

    # Get a project by name with namespace
    project_name_with_namespace = "namespace/project_name"
    project = gl.projects.get(project_name_with_namespace)

Create a project::

    project = gl.projects.create({'name': 'project1'})

Create a project for a user (admin only)::

    alice = gl.users.list(username='alice')[0]
    user_project = alice.projects.create({'name': 'project'})
    user_projects = alice.projects.list()

Create a project in a group::

    # You need to get the id of the group, then use the namespace_id attribute
    # to create the group
    group_id = gl.groups.list(search='my-group')[0].id
    project = gl.projects.create({'name': 'myrepo', 'namespace_id': group_id})

List a project's groups::

    # Get a list of ancestor/parent groups for a project.
    groups = project.groups.list()

Update a project::

    project.snippets_enabled = 1
    project.save()

Set the avatar image for a project::

    # the avatar image can be passed as data (content of the file) or as a file
    # object opened in binary mode
    project.avatar = open('path/to/file.png', 'rb')
    project.save()

Delete a project::

    gl.projects.delete(project_id)
    # or
    project.delete()

Restore a project marked for deletion (Premium only)::

    project.restore()

Fork a project::

    fork = project.forks.create({})

    # fork to a specific namespace
    fork = project.forks.create({'namespace': 'myteam'})

Get a list of forks for the project::

    forks = project.forks.list()

Create/delete a fork relation between projects (requires admin permissions)::

    project.create_fork_relation(source_project.id)
    project.delete_fork_relation()

Get languages used in the project with percentage value::

    languages = project.languages()

Star/unstar a project::

    project.star()
    project.unstar()

Archive/unarchive a project::

    project.archive()
    project.unarchive()

Start the housekeeping job::

    project.housekeeping()

List the repository tree::

    # list the content of the root directory for the default branch
    items = project.repository_tree()

    # list the content of a subdirectory on a specific branch
    items = project.repository_tree(path='docs', ref='branch1')

Get the content and metadata of a file for a commit, using a blob sha::

    items = project.repository_tree(path='docs', ref='branch1')
    file_info = p.repository_blob(items[0]['id'])
    content = base64.b64decode(file_info['content'])
    size = file_info['size']

Update a project submodule::

    items = project.update_submodule(
        submodule="foo/bar",
        branch="main",
        commit_sha="4c3674f66071e30b3311dac9b9ccc90502a72664",
        commit_message="Message",  # optional
    )

Get the repository archive::

    tgz = project.repository_archive()

    # get the archive for a branch/tag/commit
    tgz = project.repository_archive(sha='4567abc')

    # get the archive in a different format
    zip = project.repository_archive(format='zip')

.. note::

   For the formats available, refer to
   https://docs.gitlab.com/ce/api/repositories.html#get-file-archive

.. warning::

   Archives are entirely stored in memory unless you use the streaming feature.
   See :ref:`the artifacts example <streaming_example>`.

Get the content of a file using the blob id::

    # find the id for the blob (simple search)
    id = [d['id'] for d in p.repository_tree() if d['name'] == 'README.rst'][0]

    # get the content
    file_content = p.repository_raw_blob(id)

.. warning::

   Blobs are entirely stored in memory unless you use the streaming feature.
   See :ref:`the artifacts example <streaming_example>`.

Get a snapshot of the repository::

    tar_file = project.snapshot()

.. warning::

   Snapshots are entirely stored in memory unless you use the streaming
   feature.  See :ref:`the artifacts example <streaming_example>`.

Compare two branches, tags or commits::

    result = project.repository_compare('main', 'branch1')

    # get the commits
    for commit in result['commits']:
        print(commit)

    # get the diffs
    for file_diff in result['diffs']:
        print(file_diff)

Get the merge base for two or more branches, tags or commits::

    commit = project.repository_merge_base(['main', 'v1.2.3', 'bd1324e2f'])

Get a list of contributors for the repository::

    contributors = project.repository_contributors()

Get a list of users for the repository::

    users = p.users.list()

    # search for users
    users = p.users.list(search='pattern')

Start the pull mirroring process (EE edition)::

    project.mirror_pull()

Get a project’s pull mirror details (EE edition)::

    mirror_pull_details = project.mirror_pull_details()

Import / Export
===============

You can export projects from gitlab, and re-import them to create new projects
or overwrite existing ones.

Reference
---------

* v4 API:

  + :class:`gitlab.v4.objects.ProjectExport`
  + :class:`gitlab.v4.objects.ProjectExportManager`
  + :attr:`gitlab.v4.objects.Project.exports`
  + :class:`gitlab.v4.objects.ProjectImport`
  + :class:`gitlab.v4.objects.ProjectImportManager`
  + :attr:`gitlab.v4.objects.Project.imports`
  + :attr:`gitlab.v4.objects.ProjectManager.import_project`

* GitLab API: https://docs.gitlab.com/ce/api/project_import_export.html

.. _project_import_export:

Examples
--------

A project export is an asynchronous operation. To retrieve the archive
generated by GitLab you need to:

#. Create an export using the API
#. Wait for the export to be done
#. Download the result

::

    # Create the export
    p = gl.projects.get(my_project)
    export = p.exports.create()

    # Wait for the 'finished' status
    export.refresh()
    while export.export_status != 'finished':
        time.sleep(1)
        export.refresh()

    # Download the result
    with open('/tmp/export.tgz', 'wb') as f:
        export.download(streamed=True, action=f.write)

You can export and upload a project to an external URL (see upstream documentation
for more details)::

    project.exports.create(
        {
            "upload":
                {
                    "url": "http://localhost:8080",
                    "method": "POST"
                }
        }
    )

You can also get the status of an existing export, regardless of
whether it was created via the API or the Web UI::

    project = gl.projects.get(my_project)

    # Gets the current export status
    export = project.exports.get()

Import the project into the current user's namespace::

    with open('/tmp/export.tgz', 'rb') as f:
        output = gl.projects.import_project(
            f, path='my_new_project', name='My New Project'
        )

    # Get a ProjectImport object to track the import status
    project_import = gl.projects.get(output['id'], lazy=True).imports.get()
    while project_import.import_status != 'finished':
        time.sleep(1)
        project_import.refresh()

Import the project into a namespace and override parameters::

    with open('/tmp/export.tgz', 'rb') as f:
        output = gl.projects.import_project(
            f,
            path='my_new_project',
            name='My New Project',
            namespace='my-group',
            override_params={'visibility': 'private'},
        )

Import the project using file stored on a remote URL::

    output = gl.projects.remote_import(
        url="https://whatever.com/url/file.tar.gz",
        path="my_new_remote_project",
        name="My New Remote Project",
        namespace="my-group",
        override_params={'visibility': 'private'},
    )

Import the project using file stored on AWS S3::

    output = gl.projects.remote_import_s3(
        path="my_new_remote_project",
        region="aws-region",
        bucket_name="aws-bucket-name",
        file_key="aws-file-key",
        access_key_id="aws-access-key-id",
        secret_access_key="secret-access-key",
        name="My New Remote Project",
        namespace="my-group",
        override_params={'visibility': 'private'},
    )

Project custom attributes
=========================

Reference
---------

* v4 API:

  + :class:`gitlab.v4.objects.ProjectCustomAttribute`
  + :class:`gitlab.v4.objects.ProjectCustomAttributeManager`
  + :attr:`gitlab.v4.objects.Project.customattributes`

* GitLab API: https://docs.gitlab.com/ce/api/custom_attributes.html

Examples
--------

List custom attributes for a project::

    attrs = project.customattributes.list()

Get a custom attribute for a project::

    attr = project.customattributes.get(attr_key)

Set (create or update) a custom attribute for a project::

    attr = project.customattributes.set(attr_key, attr_value)

Delete a custom attribute for a project::

    attr.delete()
    # or
    project.customattributes.delete(attr_key)

Search projects by custom attribute::

    project.customattributes.set('type', 'internal')
    gl.projects.list(custom_attributes={'type': 'internal'})

Project files
=============

Reference
---------

* v4 API:

  + :class:`gitlab.v4.objects.ProjectFile`
  + :class:`gitlab.v4.objects.ProjectFileManager`
  + :attr:`gitlab.v4.objects.Project.files`

* GitLab API: https://docs.gitlab.com/ce/api/repository_files.html

Examples
--------

Get a file::

    f = project.files.get(file_path='README.rst', ref='main')

    # get the base64 encoded content
    print(f.content)

    # get the decoded content
    print(f.decode())

Get file details from headers, without fetching its entire content::

    headers = project.files.head('README.rst', ref='main')

    # Get the file size:
    # For a full list of headers returned, see upstream documentation.
    # https://docs.gitlab.com/ee/api/repository_files.html#get-file-from-repository
    print(headers["X-Gitlab-Size"])

Get a raw file::

    raw_content = project.files.raw(file_path='README.rst', ref='main')
    print(raw_content)
    with open('/tmp/raw-download.txt', 'wb') as f:
        project.files.raw(file_path='README.rst', ref='main', streamed=True, action=f.write)

Create a new file::

    f = project.files.create({'file_path': 'testfile.txt',
                              'branch': 'main',
                              'content': file_content,
                              'author_email': 'test@example.com',
                              'author_name': 'yourname',
                              'commit_message': 'Create testfile'})

Update a file. The entire content must be uploaded, as plain text or as base64
encoded text::

    f.content = 'new content'
    f.save(branch='main', commit_message='Update testfile')

    # or for binary data
    # Note: decode() is required with python 3 for data serialization. You can omit
    # it with python 2
    f.content = base64.b64encode(open('image.png').read()).decode()
    f.save(branch='main', commit_message='Update testfile', encoding='base64')

Delete a file::

    f.delete(commit_message='Delete testfile', branch='main')
    # or
    project.files.delete(file_path='testfile.txt', commit_message='Delete testfile', branch='main')

Get file blame::

    b = project.files.blame(file_path='README.rst', ref='main')

Project tags
============

Reference
---------

* v4 API:

  + :class:`gitlab.v4.objects.ProjectTag`
  + :class:`gitlab.v4.objects.ProjectTagManager`
  + :attr:`gitlab.v4.objects.Project.tags`

* GitLab API: https://docs.gitlab.com/ce/api/tags.html

Examples
--------

List the project tags::

    tags = project.tags.list()

Get a tag::

    tag = project.tags.get('1.0')

Create a tag::

    tag = project.tags.create({'tag_name': '1.0', 'ref': 'main'})

Delete a tag::

    project.tags.delete('1.0')
    # or
    tag.delete()

.. _project_snippets:

Project snippets
================

The snippet visibility can be defined using the following constants:

* ``gitlab.const.Visibility.PRIVATE``
* ``gitlab.const.Visibility.INTERNAL``
* ``gitlab.const.Visibility.PUBLIC``

Reference
---------

* v4 API:

  + :class:`gitlab.v4.objects.ProjectSnippet`
  + :class:`gitlab.v4.objects.ProjectSnippetManager`
  + :attr:`gitlab.v4.objects.Project.files`

* GitLab API: https://docs.gitlab.com/ce/api/project_snippets.html

Examples
--------

List the project snippets::

    snippets = project.snippets.list()

Get a snippet::

    snippet = project.snippets.get(snippet_id)

Get the content of a snippet::

    print(snippet.content())

.. warning::

   The snippet content is entirely stored in memory unless you use the
   streaming feature. See :ref:`the artifacts example <streaming_example>`.

Create a snippet::

    snippet = project.snippets.create({'title': 'sample 1',
                                       'files': [{
                                            'file_path': 'foo.py',
                                            'content': 'import gitlab'
                                        }],
                                       'visibility_level':
                                       gitlab.const.Visibility.PRIVATE})

Update a snippet::

    snippet.code = 'import gitlab\nimport whatever'
    snippet.save

Delete a snippet::

    project.snippets.delete(snippet_id)
    # or
    snippet.delete()

Get user agent detail (admin only)::

    detail = snippet.user_agent_detail()

Notes
=====

See :ref:`project-notes`.

Project members
===============

Reference
---------

* v4 API:

  + :class:`gitlab.v4.objects.ProjectMember`
  + :class:`gitlab.v4.objects.ProjectMemberManager`
  + :class:`gitlab.v4.objects.ProjectMemberAllManager`
  + :attr:`gitlab.v4.objects.Project.members`
  + :attr:`gitlab.v4.objects.Project.members_all`

* GitLab API: https://docs.gitlab.com/ce/api/members.html

Examples
--------

List only direct project members::

    members = project.members.list()

List the project members recursively (including inherited members through
ancestor groups)::

    members = project.members_all.list(get_all=True)

Search project members matching a query string::

    members = project.members.list(query='bar')

Get only direct project member::

    member = project.members.get(user_id)

Get a member of a project, including members inherited through ancestor groups::

    members = project.members_all.get(member_id)


Add a project member::

    member = project.members.create({'user_id': user.id, 'access_level':
                                     gitlab.const.AccessLevel.DEVELOPER})

Modify a project member (change the access level)::

    member.access_level = gitlab.const.AccessLevel.MAINTAINER
    member.save()

Remove a member from the project team::

    project.members.delete(user.id)
    # or
    member.delete()

Share/unshare the project with a group::

    project.share(group.id, gitlab.const.AccessLevel.DEVELOPER)
    project.unshare(group.id)

Project hooks
=============

Reference
---------

* v4 API:

  + :class:`gitlab.v4.objects.ProjectHook`
  + :class:`gitlab.v4.objects.ProjectHookManager`
  + :attr:`gitlab.v4.objects.Project.hooks`

* GitLab API: https://docs.gitlab.com/ce/api/projects.html#hooks

Examples
--------

List the project hooks::

    hooks = project.hooks.list()

Get a project hook::

    hook = project.hooks.get(hook_id)

Create a project hook::

    hook = project.hooks.create({'url': 'http://my/action/url', 'push_events': 1})

Update a project hook::

    hook.push_events = 0
    hook.save()

Test a project hook::

    hook.test("push_events")

Delete a project hook::

    project.hooks.delete(hook_id)
    # or
    hook.delete()

Project Integrations
====================

Reference
---------

* v4 API:

  + :class:`gitlab.v4.objects.ProjectIntegration`
  + :class:`gitlab.v4.objects.ProjectIntegrationManager`
  + :attr:`gitlab.v4.objects.Project.integrations`

* GitLab API: https://docs.gitlab.com/ce/api/integrations.html

Examples
---------

.. danger::

    Since GitLab 13.12, ``get()`` calls to project integrations return a
    ``404 Not Found`` response until they have been activated the first time.

    To avoid this, we recommend using `lazy=True` to prevent making
    the initial call when activating new integrations unless they have
    previously already been activated.

Configure and enable an integration for the first time::

    integration = project.integrations.get('asana', lazy=True)

    integration.api_key = 'randomkey'
    integration.save()

Get an existing integration::

    integration = project.integrations.get('asana')
    # display its status (enabled/disabled)
    print(integration.active)

List active project integrations::

    integration = project.integrations.list()

List the code names of available integrations (doesn't return objects)::

    integrations = project.integrations.available()

Disable an integration::

    integration.delete()

File uploads
============

Reference
---------

* v4 API:

  + :attr:`gitlab.v4.objects.Project.upload`

* Gitlab API: https://docs.gitlab.com/ce/api/projects.html#upload-a-file

Examples
--------

Upload a file into a project using a filesystem path::

    project.upload("filename.txt", filepath="/some/path/filename.txt")

Upload a file into a project without a filesystem path::

    project.upload("filename.txt", filedata="Raw data")

Upload a file and comment on an issue using the uploaded file's
markdown::

    uploaded_file = project.upload("filename.txt", filedata="data")
    issue = project.issues.get(issue_id)
    issue.notes.create({
        "body": "See the attached file: {}".format(uploaded_file["markdown"])
    })

Upload a file and comment on an issue while using custom
markdown to reference the uploaded file::

    uploaded_file = project.upload("filename.txt", filedata="data")
    issue = project.issues.get(issue_id)
    issue.notes.create({
        "body": "See the [attached file]({})".format(uploaded_file["url"])
    })

Project push rules
==================

Reference
---------

* v4 API:

  + :class:`gitlab.v4.objects.ProjectPushRules`
  + :class:`gitlab.v4.objects.ProjectPushRulesManager`
  + :attr:`gitlab.v4.objects.Project.pushrules`

* GitLab API: https://docs.gitlab.com/ee/api/projects.html#push-rules

Examples
---------

Create project push rules (at least one rule is necessary)::

    project.pushrules.create({'deny_delete_tag': True})

Get project push rules::

    pr = project.pushrules.get()

Edit project push rules::

    pr.branch_name_regex = '^(main|develop|support-\d+|release-\d+\..+|hotfix-.+|feature-.+)$'
    pr.save()

Delete project push rules::

    pr.delete()

Project protected tags
======================

Reference
---------

* v4 API:

  + :class:`gitlab.v4.objects.ProjectProtectedTag`
  + :class:`gitlab.v4.objects.ProjectProtectedTagManager`
  + :attr:`gitlab.v4.objects.Project.protectedtags`

* GitLab API: https://docs.gitlab.com/ce/api/protected_tags.html

Examples
---------

Get a list of protected tags from a project::

    protected_tags = project.protectedtags.list()

Get a single protected tag or wildcard protected tag::

    protected_tag = project.protectedtags.get('v*')

Protect a single repository tag or several project repository tags using a wildcard protected tag::

    project.protectedtags.create({'name': 'v*', 'create_access_level': '40'})

Unprotect the given protected tag or wildcard protected tag.::

    protected_tag.delete()

Additional project statistics
=============================

Reference
---------

* v4 API:

  + :class:`gitlab.v4.objects.ProjectAdditionalStatistics`
  + :class:`gitlab.v4.objects.ProjectAdditionalStatisticsManager`
  + :attr:`gitlab.v4.objects.Project.additionalstatistics`

* GitLab API: https://docs.gitlab.com/ce/api/project_statistics.html

Examples
---------

Get all additional statistics of a project::

    statistics = project.additionalstatistics.get()

Get total fetches in last 30 days of a project::

    total_fetches = project.additionalstatistics.get().fetches['total']

Project storage
=============================

This endpoint requires admin access.

Reference
---------

* v4 API:

  + :class:`gitlab.v4.objects.ProjectStorage`
  + :class:`gitlab.v4.objects.ProjectStorageManager`
  + :attr:`gitlab.v4.objects.Project.storage`

* GitLab API: https://docs.gitlab.com/ee/api/projects.html#get-the-path-to-repository-storage

Examples
---------

Get the repository storage details for a project::

    storage = project.storage.get()

Get the repository storage disk path::

    disk_path = project.storage.get().disk_path

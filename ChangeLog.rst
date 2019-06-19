ChangeLog
=========

Version 1.9.0_ - 2019-06-19
---------------------------

Features
^^^^^^^^

-  implement artifacts deletion
-  add endpoint to get the variables of a pipeline
-  delete ProjectPipeline
-  implement __eq__ and __hash__ methods
-  Allow runpy invocation of CLI tool (python -m gitlab)
-  add project releases api
-  merged new release & registry apis

Bug Fixes
^^^^^^^^^

-  convert # to %23 in URLs
-  pep8 errors
-  use python2 compatible syntax for super
-  Make MemberManager.all() return a list of objects
-  %d replaced by %s
-  Re-enable command specific help messages
-  dont ask for id attr if this is *Manager originating custom action
-  fix -/_ replacament for *Manager custom actions
-  fix repository_id marshaling in cli
-  register cli action for delete_in_bulk

Version 1.8.0_ - 2019-02-22
---------------------------

* docs(setup): use proper readme on PyPI
* docs(readme): provide commit message guidelines
* fix(api): make reset_time_estimate() work again
* fix: handle empty 'Retry-After' header from GitLab
* fix: remove decode() on error_message string
* chore: release tags to PyPI automatically
* fix(api): avoid parameter conflicts with python and gitlab
* fix(api): Don't try to parse raw downloads
* feat: Added approve & unapprove method for Mergerequests
* fix all kwarg behaviour

Version 1.7.0_ - 2018-12-09
---------------------------

* [docs] Fix the owned/starred usage documentation
* [docs] Add a warning about http to https redirects
* Fix the https redirection test
* [docs] Add a note about GroupProject limited API
* Add missing comma in ProjectIssueManager _create_attrs
* More flexible docker image
* Add project protected tags management
* [cli] Print help and usage without config file
* Rename MASTER_ACCESS to MAINTAINER_ACCESS
* [docs] Add docs build information
* Use docker image with current sources
* [docs] Add PyYAML requirement notice
* Add Gitter badge to README
* [docs] Add an example of pipeline schedule vars listing
* [cli] Exit on config parse error, instead of crashing
* Add support for resource label events
* [docs] Fix the milestone filetring doc (iid -> iids)
* [docs] Fix typo in custom attributes example
* Improve error message handling in exceptions
* Add support for members all() method
* Add access control options to protected branch creation

Version 1.6.0_ - 2018-08-25
---------------------------

* [docs] Don't use hardcoded values for ids
* [docs] Improve the snippets examples
* [cli] Output: handle bytes in API responses
* [cli] Fix the case where we have nothing to print
* Project import: fix the override_params parameter
* Support group and global MR listing
* Implement MR.pipelines()
* MR: add the squash attribute for create/update
* Added support for listing forks of a project
* [docs] Add/update notes about read-only objects
* Raise an exception on https redirects for PUT/POST
* [docs] Add a FAQ
* [cli] Fix the project-export download

Version 1.5.1_ - 2018-06-23
---------------------------

* Fix the ProjectPipelineJob base class (regression)

Version 1.5.0_ - 2018-06-22
---------------------------

* Drop API v3 support
* Drop GetFromListMixin
* Update the sphinx extension for v4 objects
* Add support for user avatar upload
* Add support for project import/export
* Add support for the search API
* Add a global per_page config option
* Add support for the discussions API
* Add support for merged branches deletion
* Add support for Project badges
* Implement user_agent_detail for snippets
* Implement commit.refs()
* Add commit.merge_requests() support
* Deployment: add list filters
* Deploy key: add missing attributes
* Add support for environment stop()
* Add feature flags deletion support
* Update some group attributes
* Issues: add missing attributes and methods
* Fix the participants() decorator
* Add support for group boards
* Implement the markdown rendering API
* Update MR attributes
* Add pipeline listing filters
* Add missing project attributes
* Implement runner jobs listing
* Runners can be created (registered)
* Implement runner token validation
* Update the settings attributes
* Add support for the gitlab CI lint API
* Add support for group badges
* Fix the IssueManager path to avoid redirections
* time_stats(): use an existing attribute if available
* Make ProjectCommitStatus.create work with CLI
* Tests: default to python 3
* ProjectPipelineJob was defined twice
* Silence logs/warnings in unittests
* Add support for MR approval configuration (EE)
* Change post_data default value to None
* Add geo nodes API support (EE)
* Add support for issue links (EE)
* Add support for LDAP groups (EE)
* Add support for board creation/deletion (EE)
* Add support for Project.pull_mirror (EE)
* Add project push rules configuration (EE)
* Add support for the EE license API
* Add support for the LDAP groups API (EE)
* Add support for epics API (EE)
* Fix the non-verbose output of ProjectCommitComment

Version 1.4.0_ - 2018-05-19
---------------------------

* Require requests>=2.4.2
* ProjectKeys can be updated
* Add support for unsharing projects (v3/v4)
* [cli] fix listing for json and yaml output
* Fix typos in documentation
* Introduce RefreshMixin
* [docs] Fix the time tracking examples
* [docs] Commits: add an example of binary file creation
* [cli] Allow to read args from files
* Add support for recursive tree listing
* [cli] Restore the --help option behavior
* Add basic unit tests for v4 CLI
* [cli] Fix listing of strings
* Support downloading a single artifact file
* Update docs copyright years
* Implement attribute types to handle special cases
* [docs] fix GitLab reference for notes
* Expose additional properties for Gitlab objects
* Fix the impersonation token deletion example
* feat: obey the rate limit
* Fix URL encoding on branch methods
* [docs] add a code example for listing commits of a MR
* [docs] update service.available() example for API v4
* [tests] fix functional tests for python3
* api-usage: bit more detail for listing with `all`
* More efficient .get() for group members
* Add docs for the `files` arg in http_*
* Deprecate GetFromListMixin

Version 1.3.0_ - 2018-02-18
---------------------------

* Add support for pipeline schedules and schedule variables
* Clarify information about supported python version
* Add manager for jobs within a pipeline
* Fix wrong tag example
* Update the groups documentation
* Add support for MR participants API
* Add support for getting list of user projects
* Add Gitlab and User events support
* Make trigger_pipeline return the pipeline
* Config: support api_version in the global section
* Gitlab can be used as context manager
* Default to API v4
* Add a simplified example for streamed artifacts
* Add documentation about labels update

Version 1.2.0_ - 2018-01-01
---------------------------

* Add mattermost service support
* Add users custom attributes support
* [doc] Fix project.triggers.create example with v4 API
* Oauth token support
* Remove deprecated objects/methods
* Rework authentication args handling
* Add support for oauth and anonymous auth in config/CLI
* Add support for impersonation tokens API
* Add support for user activities
* Update user docs with gitlab URLs
* [docs] Bad arguments in projects file documentation
* Add support for user_agent_detail (issues)
* Add a SetMixin
* Add support for project housekeeping
* Expected HTTP response for subscribe is 201
* Update pagination docs for ProjectCommit
* Add doc to get issue from iid
* Make todo() raise GitlabTodoError on error
* Add support for award emojis
* Update project services docs for v4
* Avoid sending empty update data to issue.save
* [docstrings] Explicitly document pagination arguments
* [docs] Add a note about password auth being removed from GitLab
* Submanagers: allow having undefined parameters
* ProjectFile.create(): don't modify the input data
* Update testing tools for /session removal
* Update groups tests
* Allow per_page to be used with generators
* Add groups listing attributes
* Add support for subgroups listing
* Add supported python versions in setup.py
* Add support for pagesdomains
* Add support for features flags
* Add support for project and group custom variables
* Add support for user/group/project filter by custom attribute
* Respect content of REQUESTS_CA_BUNDLE and *_proxy envvars

Version 1.1.0_ - 2017-11-03
---------------------------

* Fix trigger variables in v4 API
* Make the delete() method handle / in ids
* [docs] update the file upload samples
* Tags release description: support / in tag names
* [docs] improve the labels usage documentation
* Add support for listing project users
* ProjectFileManager.create: handle / in file paths
* Change ProjectUser and GroupProject base class
* [docs] document `get_create_attrs` in the API tutorial
* Document the Gitlab session parameter
* ProjectFileManager: custom update() method
* Project: add support for printing_merge_request_link_enabled attr
* Update the ssl_verify docstring
* Add support for group milestones
* Add support for GPG keys
* Add support for wiki pages
* Update the repository_blob documentation
* Fix the CLI for objects without ID (API v4)
* Add a contributed Dockerfile
* Pagination generators: expose more information
* Module's base objects serialization
* [doc] Add sample code for client-side certificates

Version 1.0.2_ - 2017-09-29
---------------------------

* [docs] remove example usage of submanagers
* Properly handle the labels attribute in ProjectMergeRequest
* ProjectFile: handle / in path for delete() and save()

Version 1.0.1_ - 2017-09-21
---------------------------

* Tags can be retrieved by ID
* Add the server response in GitlabError exceptions
* Add support for project file upload
* Minor typo fix in "Switching to v4" documentation
* Fix password authentication for v4
* Fix the labels attrs on MR and issues
* Exceptions: use a proper error message
* Fix http_get method in get artifacts and job trace
* CommitStatus: `sha` is parent attribute
* Fix a couple listing calls to allow proper pagination
* Add missing doc file

Version 1.0.0_ - 2017-09-08
---------------------------

* Support for API v4. See
  http://python-gitlab.readthedocs.io/en/master/switching-to-v4.html
* Support SSL verification via internal CA bundle
* Docs: Add link to gitlab docs on obtaining a token
* Added dependency injection support for Session
* Fixed repository_compare examples
* Fix changelog and release notes inclusion in sdist
* Missing expires_at in GroupMembers update
* Add lower-level methods for Gitlab()

Version 0.21.2_ - 2017-06-11
----------------------------

* Install doc: use sudo for system commands
* [v4] Make MR work properly
* Remove extra_attrs argument from _raw_list
* [v4] Make project issues work properly
* Fix urlencode() usage (python 2/3) (#268)
* Fixed spelling mistake (#269)
* Add new event types to ProjectHook

Version 0.21.1_ - 2017-05-25
----------------------------

* Fix the manager name for jobs in the Project class
* Fix the docs

Version 0.21_ - 2017-05-24
--------------------------

* Add time_stats to ProjectMergeRequest
* Update User options for creation and update (#246)
* Add milestone.merge_requests() API
* Fix docs typo (s/correspnding/corresponding/)
* Support milestone start date (#251)
* Add support for priority attribute in labels (#256)
* Add support for nested groups (#257)
* Make GroupProjectManager a subclass of ProjectManager (#255)
* Available services: return a list instead of JSON (#258)
* MR: add support for time tracking features (#248)
* Fixed repository_tree and repository_blob path encoding (#265)
* Add 'search' attribute to projects.list()
* Initial gitlab API v4 support
* Reorganise the code to handle v3 and v4 objects
* Allow 202 as delete return code
* Deprecate parameter related methods in gitlab.Gitlab

Version 0.20_ - 2017-03-25
---------------------------

* Add time tracking support (#222)
* Improve changelog (#229, #230)
* Make sure that manager objects are never overwritten (#209)
* Include chanlog and release notes in docs
* Add DeployKey{,Manager} classes (#212)
* Add support for merge request notes deletion (#227)
* Properly handle extra args when listing with all=True (#233)
* Implement pipeline creation API (#237)
* Fix spent_time methods
* Add 'delete source branch' option when creating MR (#241)
* Provide API wrapper for cherry picking commits (#236)
* Stop listing if recursion limit is hit (#234)

Version 0.19_ - 2017-02-21
---------------------------

* Update project.archive() docs
* Support the scope attribute in runners.list()
* Add support for project runners
* Add support for commit creation
* Fix install doc
* Add builds-email and pipelines-email services
* Deploy keys: rework enable/disable
* Document the dynamic aspect of objects
* Add pipeline_events to ProjectHook attrs
* Add due_date attribute to ProjectIssue
* Handle settings.domain_whitelist, partly
* {Project,Group}Member: support expires_at attribute

Version 0.18_ - 2016-12-27
---------------------------

* Fix JIRA service editing for GitLab 8.14+
* Add jira_issue_transition_id to the JIRA service optional fields
* Added support for Snippets (new API in Gitlab 8.15)
* [docs] update pagination section
* [docs] artifacts example: open file in wb mode
* [CLI] ignore empty arguments
* [CLI] Fix wrong use of arguments
* [docs] Add doc for snippets
* Fix duplicated data in API docs
* Update known attributes for projects
* sudo: always use strings

Version 0.17_ - 2016-12-02
---------------------------

* README: add badges for pypi and RTD
* Fix ProjectBuild.play (raised error on success)
* Pass kwargs to the object factory
* Add .tox to ignore to respect default tox settings
* Convert response list to single data source for iid requests
* Add support for boards API
* Add support for Gitlab.version()
* Add support for broadcast messages API
* Add support for the notification settings API
* Don't overwrite attributes returned by the server
* Fix bug when retrieving changes for merge request
* Feature: enable / disable the deploy key in a project
* Docs: add a note for python 3.5 for file content update
* ProjectHook: support the token attribute
* Rework the API documentation
* Fix docstring for http_{username,password}
* Build managers on demand on GitlabObject's
* API docs: add managers doc in GitlabObject's
* Sphinx ext: factorize the build methods
* Implement __repr__ for gitlab objects
* Add a 'report a bug' link on doc
* Remove deprecated methods
* Implement merge requests diff support
* Make the manager objects creation more dynamic
* Add support for templates API
* Add attr 'created_at' to ProjectIssueNote
* Add attr 'updated_at' to ProjectIssue
* CLI: add support for project all --all
* Add support for triggering a new build
* Rework requests arguments (support latest requests release)
* Fix `should_remove_source_branch`

Version 0.16_ - 2016-10-16
---------------------------

* Add the ability to fork to a specific namespace
* JIRA service - add api_url to optional attributes
* Fix bug: Missing coma concatenates array values
* docs: branch protection notes
* Create a project in a group
* Add only_allow_merge_if_build_succeeds option to project objects
* Add support for --all in CLI
* Fix examples for file modification
* Use the plural merge_requests URL everywhere
* Rework travis and tox setup
* Workaround gitlab setup failure in tests
* Add ProjectBuild.erase()
* Implement ProjectBuild.play()

Version 0.15.1_ - 2016-10-16
-----------------------------

* docs: improve the pagination section
* Fix and test pagination
* 'path' is an existing gitlab attr, don't use it as method argument

Version 0.15_ - 2016-08-28
---------------------------

* Add a basic HTTP debug method
* Run more tests in travis
* Fix fork creation documentation
* Add more API examples in docs
* Update the ApplicationSettings attributes
* Implement the todo API
* Add sidekiq metrics support
* Move the constants at the gitlab root level
* Remove methods marked as deprecated 7 months ago
* Refactor the Gitlab class
* Remove _get_list_or_object() and its tests
* Fix canGet attribute (typo)
* Remove unused ProjectTagReleaseManager class
* Add support for project services API
* Add support for project pipelines
* Add support for access requests
* Add support for project deployments

Version 0.14_ - 2016-08-07
---------------------------

* Remove 'next_url' from kwargs before passing it to the cls constructor.
* List projects under group
* Add support for subscribe and unsubscribe in issues
* Project issue: doc and CLI for (un)subscribe
* Added support for HTTP basic authentication
* Add support for build artifacts and trace
* --title is a required argument for ProjectMilestone
* Commit status: add optional context url
* Commit status: optional get attrs
* Add support for commit comments
* Issues: add optional listing parameters
* Issues: add missing optional listing parameters
* Project issue: proper update attributes
* Add support for project-issue move
* Update ProjectLabel attributes
* Milestone: optional listing attrs
* Add support for namespaces
* Add support for label (un)subscribe
* MR: add (un)subscribe support
* Add `note_events` to project hooks attributes
* Add code examples for a bunch of resources
* Implement user emails support
* Project: add VISIBILITY_* constants
* Fix the Project.archive call
* Implement archive/unarchive for a projet
* Update ProjectSnippet attributes
* Fix ProjectMember update
* Implement sharing project with a group
* Implement CLI for project archive/unarchive/share
* Implement runners global API
* Gitlab: add managers for build-related resources
* Implement ProjectBuild.keep_artifacts
* Allow to stream the downloads when appropriate
* Groups can be updated
* Replace Snippet.Content() with a new content() method
* CLI: refactor _die()
* Improve commit statuses and comments
* Add support from listing group issues
* Added a new project attribute to enable the container registry.
* Add a contributing section in README
* Add support for global deploy key listing
* Add support for project environments
* MR: get list of changes and commits
* Fix the listing of some resources
* MR: fix updates
* Handle empty messages from server in exceptions
* MR (un)subscribe: don't fail if state doesn't change
* MR merge(): update the object

Version 0.13_ - 2016-05-16
---------------------------

* Add support for MergeRequest validation
* MR: add support for cancel_merge_when_build_succeeds
* MR: add support for closes_issues
* Add "external" parameter for users
* Add deletion support for issues and MR
* Add missing group creation parameters
* Add a Session instance for all HTTP requests
* Enable updates on ProjectIssueNotes
* Add support for Project raw_blob
* Implement project compare
* Implement project contributors
* Drop the next_url attribute when listing
* Remove unnecessary canUpdate property from ProjectIssuesNote
* Add new optional attributes for projects
* Enable deprecation warnings for gitlab only
* Rework merge requests update
* Rework the Gitlab.delete method
* ProjectFile: file_path is required for deletion
* Rename some methods to better match the API URLs
* Deprecate the file_* methods in favor of the files manager
* Implement star/unstar for projects
* Implement list/get licenses
* Manage optional parameters for list() and get()

Version 0.12.2_ - 2016-03-19
-----------------------------

* Add new `ProjectHook` attributes
* Add support for user block/unblock
* Fix GitlabObject creation in _custom_list
* Add support for more CLI subcommands
* Add some unit tests for CLI
* Add a coverage tox env
* Define GitlabObject.as_dict() to dump object as a dict
* Define GitlabObject.__eq__() and __ne__() equivalence methods
* Define UserManager.search() to search for users
* Define UserManager.get_by_username() to get a user by username
* Implement "user search" CLI
* Improve the doc for UserManager
* CLI: implement user get-by-username
* Re-implement _custom_list in the Gitlab class
* Fix the 'invalid syntax' error on Python 3.2
* Gitlab.update(): use the proper attributes if defined

Version 0.12.1_ - 2016-02-03
-----------------------------

* Fix a broken upload to pypi

Version 0.12_ - 2016-02-03
---------------------------

* Improve documentation
* Improve unit tests
* Improve test scripts
* Skip BaseManager attributes when encoding to JSON
* Fix the json() method for python 3
* Add Travis CI support
* Add a decode method for ProjectFile
* Make connection exceptions more explicit
* Fix ProjectLabel get and delete
* Implement ProjectMilestone.issues()
* ProjectTag supports deletion
* Implement setting release info on a tag
* Implement project triggers support
* Implement project variables support
* Add support for application settings
* Fix the 'password' requirement for User creation
* Add sudo support
* Fix project update
* Fix Project.tree()
* Add support for project builds

Version 0.11.1_ - 2016-01-17
-----------------------------

* Fix discovery of parents object attrs for managers
* Support setting commit status
* Support deletion without getting the object first
* Improve the documentation

Version 0.11_ - 2016-01-09
---------------------------

* functional_tests.sh: support python 2 and 3
* Add a get method for GitlabObject
* CLI: Add the -g short option for --gitlab
* Provide a create method for GitlabObject's
* Rename the _created attribute _from_api
* More unit tests
* CLI: fix error when arguments are missing (python 3)
* Remove deprecated methods
* Implement managers to get access to resources
* Documentation improvements
* Add fork project support
* Deprecate the "old" Gitlab methods
* Add support for groups search

Version 0.10_ - 2015-12-29
---------------------------

* Implement pagination for list() (#63)
* Fix url when fetching a single MergeRequest
* Add support to update MergeRequestNotes
* API: Provide a Gitlab.from_config method
* setup.py: require requests>=1 (#69)
* Fix deletion of object not using 'id' as ID (#68)
* Fix GET/POST for project files
* Make 'confirm' an optional attribute for user creation
* Python 3 compatibility fixes
* Add support for group members update (#73)

Version 0.9.2_ - 2015-07-11
----------------------------

* CLI: fix the update and delete subcommands (#62)

Version 0.9.1_ - 2015-05-15
----------------------------

* Fix the setup.py script

Version 0.9_ - 2015-05-15
--------------------------

* Implement argparse library for parsing argument on CLI
* Provide unit tests and (a few) functional tests
* Provide PEP8 tests
* Use tox to run the tests
* CLI: provide a --config-file option
* Turn the gitlab module into a proper package
* Allow projects to be updated
* Use more pythonic names for some methods
* Deprecate some Gitlab object methods:
   - raw* methods should never have been exposed; replace them with _raw_*
     methods
   - setCredentials and setToken are replaced with set_credentials and
     set_token
* Sphinx: don't hardcode the version in conf.py

Version 0.8_ - 2014-10-26
--------------------------

* Better python 2.6 and python 3 support
* Timeout support in HTTP requests
* Gitlab.get() raised GitlabListError instead of GitlabGetError
* Support api-objects which don't have id in api response
* Add ProjectLabel and ProjectFile classes
* Moved url attributes to separate list
* Added list for delete attributes

Version 0.7_ - 2014-08-21
--------------------------

* Fix license classifier in setup.py
* Fix encoding error when printing to redirected output
* Fix encoding error when updating with redirected output
* Add support for UserKey listing and deletion
* Add support for branches creation and deletion
* Support state_event in ProjectMilestone (#30)
* Support namespace/name for project id (#28)
* Fix handling of boolean values (#22)

Version 0.6_ - 2014-01-16
--------------------------

* IDs can be unicode (#15)
* ProjectMember: constructor should not create a User object
* Add support for extra parameters when listing all projects (#12)
* Projects listing: explicitly define arguments for pagination

Version 0.5_ - 2013-12-26
--------------------------

* Add SSH key for user
* Fix comments
* Add support for project events
* Support creation of projects for users
* Project: add methods for create/update/delete files
* Support projects listing: search, all, owned
* System hooks can't be updated
* Project.archive(): download tarball of the project
* Define new optional attributes for user creation
* Provide constants for access permissions in groups

Version 0.4_ - 2013-09-26
--------------------------

* Fix strings encoding (Closes #6)
* Allow to get a project commit (GitLab 6.1)
* ProjectMergeRequest: fix Note() method
* Gitlab 6.1 methods: diff, blob (commit), tree, blob (project)
* Add support for Gitlab 6.1 group members

Version 0.3_ - 2013-08-27
--------------------------

* Use PRIVATE-TOKEN header for passing the auth token
* provide an AUTHORS file
* cli: support ssl_verify config option
* Add ssl_verify option to Gitlab object. Defaults to True
* Correct url for merge requests API.

Version 0.2_ - 2013-08-08
--------------------------

* provide a pip requirements.txt
* drop some debug statements

Version 0.1 - 2013-07-08
------------------------

* Initial release

.. _1.9.0: https://github.com/python-gitlab/python-gitlab/compare/1.8.0...1.9.0
.. _1.8.0: https://github.com/python-gitlab/python-gitlab/compare/1.7.0...1.8.0
.. _1.7.0: https://github.com/python-gitlab/python-gitlab/compare/1.6.0...1.7.0
.. _1.6.0: https://github.com/python-gitlab/python-gitlab/compare/1.5.1...1.6.0
.. _1.5.1: https://github.com/python-gitlab/python-gitlab/compare/1.5.0...1.5.1
.. _1.5.0: https://github.com/python-gitlab/python-gitlab/compare/1.4.0...1.5.0
.. _1.4.0: https://github.com/python-gitlab/python-gitlab/compare/1.3.0...1.4.0
.. _1.3.0: https://github.com/python-gitlab/python-gitlab/compare/1.2.0...1.3.0
.. _1.2.0: https://github.com/python-gitlab/python-gitlab/compare/1.1.0...1.2.0
.. _1.1.0: https://github.com/python-gitlab/python-gitlab/compare/1.0.2...1.1.0
.. _1.0.2: https://github.com/python-gitlab/python-gitlab/compare/1.0.1...1.0.2
.. _1.0.1: https://github.com/python-gitlab/python-gitlab/compare/1.0.0...1.0.1
.. _1.0.0: https://github.com/python-gitlab/python-gitlab/compare/0.21.2...1.0.0
.. _0.21.2: https://github.com/python-gitlab/python-gitlab/compare/0.21.1...0.21.2
.. _0.21.1: https://github.com/python-gitlab/python-gitlab/compare/0.21...0.21.1
.. _0.21: https://github.com/python-gitlab/python-gitlab/compare/0.20...0.21
.. _0.20: https://github.com/python-gitlab/python-gitlab/compare/0.19...0.20
.. _0.19: https://github.com/python-gitlab/python-gitlab/compare/0.18...0.19
.. _0.18: https://github.com/python-gitlab/python-gitlab/compare/0.17...0.18
.. _0.17: https://github.com/python-gitlab/python-gitlab/compare/0.16...0.17
.. _0.16: https://github.com/python-gitlab/python-gitlab/compare/0.15.1...0.16
.. _0.15.1: https://github.com/python-gitlab/python-gitlab/compare/0.15...0.15.1
.. _0.15: https://github.com/python-gitlab/python-gitlab/compare/0.14...0.15
.. _0.14: https://github.com/python-gitlab/python-gitlab/compare/0.13...0.14
.. _0.13: https://github.com/python-gitlab/python-gitlab/compare/0.12.2...0.13
.. _0.12.2: https://github.com/python-gitlab/python-gitlab/compare/0.12.1...0.12.2
.. _0.12.1: https://github.com/python-gitlab/python-gitlab/compare/0.12...0.12.1
.. _0.12: https://github.com/python-gitlab/python-gitlab/compare/0.11.1...0.12
.. _0.11.1: https://github.com/python-gitlab/python-gitlab/compare/0.11...0.11.1
.. _0.11: https://github.com/python-gitlab/python-gitlab/compare/0.10...0.11
.. _0.10: https://github.com/python-gitlab/python-gitlab/compare/0.9.2...0.10
.. _0.9.2: https://github.com/python-gitlab/python-gitlab/compare/0.9.1...0.9.2
.. _0.9.1: https://github.com/python-gitlab/python-gitlab/compare/0.9...0.9.1
.. _0.9: https://github.com/python-gitlab/python-gitlab/compare/0.8...0.9
.. _0.8: https://github.com/python-gitlab/python-gitlab/compare/0.7...0.8
.. _0.7: https://github.com/python-gitlab/python-gitlab/compare/0.6...0.7
.. _0.6: https://github.com/python-gitlab/python-gitlab/compare/0.5...0.6
.. _0.5: https://github.com/python-gitlab/python-gitlab/compare/0.4...0.5
.. _0.4: https://github.com/python-gitlab/python-gitlab/compare/0.3...0.4
.. _0.3: https://github.com/python-gitlab/python-gitlab/compare/0.2...0.3
.. _0.2: https://github.com/python-gitlab/python-gitlab/compare/0.1...0.2

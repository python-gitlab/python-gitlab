##########
Search API
##########

You can search for resources at the top level, in a project or in a group.
Searches are based on a scope (issues, merge requests, and so on) and a search
string. The following constants are provided to represent the possible scopes:


* Shared scopes (global, group and project):

  + ``gitlab.const.SearchScope.PROJECTS``: ``projects``
  + ``gitlab.const.SearchScope.ISSUES``: ``issues``
  + ``gitlab.const.SearchScope.MERGE_REQUESTS``: ``merge_requests``
  + ``gitlab.const.SearchScope.MILESTONES``: ``milestones``
  + ``gitlab.const.SearchScope.WIKI_BLOBS``: ``wiki_blobs``
  + ``gitlab.const.SearchScope.COMMITS``: ``commits``
  + ``gitlab.const.SearchScope.BLOBS``: ``blobs``
  + ``gitlab.const.SearchScope.USERS``: ``users``


* specific global scope:

  + ``gitlab.const.SearchScope.GLOBAL_SNIPPET_TITLES``: ``snippet_titles``


* specific project scope:

  + ``gitlab.const.SearchScope.PROJECT_NOTES``: ``notes``


Reference
---------

* v4 API:

  + :attr:`gitlab.Gitlab.search`
  + :attr:`gitlab.v4.objects.Group.search`
  + :attr:`gitlab.v4.objects.Project.search`

* GitLab API: https://docs.gitlab.com/ce/api/search.html

Examples
--------

Search for issues matching a specific string::

    # global search
    gl.search(gitlab.const.SearchScope.ISSUES, 'regression')

    # group search
    group = gl.groups.get('mygroup')
    group.search(gitlab.const.SearchScope.ISSUES, 'regression')

    # project search
    project = gl.projects.get('myproject')
    project.search(gitlab.const.SearchScope.ISSUES, 'regression')

The ``search()`` methods implement the pagination support::

    # get lists of 10 items, and start at page 2
    gl.search(gitlab.const.SearchScope.ISSUES, search_str, page=2, per_page=10)

    # get a generator that will automatically make required API calls for
    # pagination
    for item in gl.search(gitlab.const.SearchScope.ISSUES, search_str, iterator=True):
        do_something(item)

The search API doesn't return objects, but dicts. If you need to act on
objects, you need to create them explicitly::

    for item in gl.search(gitlab.const.SearchScope.ISSUES, search_str, iterator=True):
        issue_project = gl.projects.get(item['project_id'], lazy=True)
        issue = issue_project.issues.get(item['iid'])
        issue.state = 'closed'
        issue.save()


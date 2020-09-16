##########
Search API
##########

You can search for resources at the top level, in a project or in a group.
Searches are based on a scope (issues, merge requests, and so on) and a search
string. The following constants are provided to represent the possible scopes:


* global scopes:

  + ``gitlab.SEARCH_SCOPE_GLOBAL_PROJECTS``: ``projects``
  + ``gitlab.SEARCH_SCOPE_GLOBAL_ISSUES``: ``issues``
  + ``gitlab.SEARCH_SCOPE_GLOBAL_MERGE_REQUESTS``: ``merge_requests``
  + ``gitlab.SEARCH_SCOPE_GLOBAL_MILESTONES``: ``milestones``
  + ``gitlab.SEARCH_SCOPE_GLOBAL_SNIPPET_TITLES``: ``snippet_titles``
  + ``gitlab.SEARCH_SCOPE_GLOBAL_WIKI_BLOBS``: ``wiki_blobs``
  + ``gitlab.SEARCH_SCOPE_GLOBAL_COMMITS``: ``commits``
  + ``gitlab.SEARCH_SCOPE_GLOBAL_BLOBS``: ``blobs``
  + ``gitlab.SEARCH_SCOPE_GLOBAL_USERS``: ``users``


* group scopes:

  + ``gitlab.SEARCH_SCOPE_GROUP_PROJECTS``: ``projects``
  + ``gitlab.SEARCH_SCOPE_GROUP_ISSUES``: ``issues``
  + ``gitlab.SEARCH_SCOPE_GROUP_MERGE_REQUESTS``: ``merge_requests``
  + ``gitlab.SEARCH_SCOPE_GROUP_MILESTONES``: ``milestones``
  + ``gitlab.SEARCH_SCOPE_GROUP_WIKI_BLOBS``: ``wiki_blobs``
  + ``gitlab.SEARCH_SCOPE_GROUP_COMMITS``: ``commits``
  + ``gitlab.SEARCH_SCOPE_GROUP_BLOBS``: ``blobs``
  + ``gitlab.SEARCH_SCOPE_GROUP_USERS``: ``users``


* project scopes:

  + ``gitlab.SEARCH_SCOPE_PROJECT_ISSUES``: ``issues``
  + ``gitlab.SEARCH_SCOPE_PROJECT_MERGE_REQUESTS``: ``merge_requests``
  + ``gitlab.SEARCH_SCOPE_PROJECT_MILESTONES``: ``milestones``
  + ``gitlab.SEARCH_SCOPE_PROJECT_NOTES``: ``notes``
  + ``gitlab.SEARCH_SCOPE_PROJECT_WIKI_BLOBS``: ``wiki_blobs``
  + ``gitlab.SEARCH_SCOPE_PROJECT_COMMITS``: ``commits``
  + ``gitlab.SEARCH_SCOPE_PROJECT_BLOBS``: ``blobs``
  + ``gitlab.SEARCH_SCOPE_PROJECT_USERS``: ``users``


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
    gl.search(gitlab.SEARCH_SCOPE_GLOBAL_ISSUES, 'regression')

    # group search
    group = gl.groups.get('mygroup')
    group.search(gitlab.SEARCH_SCOPE_GROUP_ISSUES, 'regression')

    # project search
    project = gl.projects.get('myproject')
    project.search(gitlab.SEARCH_SCOPE_PROJECT_ISSUES, 'regression')

The ``search()`` methods implement the pagination support::

    # get lists of 10 items, and start at page 2
    gl.search(gitlab.SEARCH_SCOPE_GLOBAL_ISSUES, search_str, page=2, per_page=10)

    # get a generator that will automatically make required API calls for
    # pagination
    for item in gl.search(gitlab.SEARCH_SCOPE_GLOBAL_ISSUES, search_str, as_list=False):
        do_something(item)

The search API doesn't return objects, but dicts. If you need to act on
objects, you need to create them explicitly::

    for item in gl.search(gitlab.SEARCH_SCOPE_GLOBAL_ISSUES, search_str, as_list=False):
        issue_project = gl.projects.get(item['project_id'], lazy=True)
        issue = issue_project.issues.get(item['iid'])
        issue.state = 'closed'
        issue.save()


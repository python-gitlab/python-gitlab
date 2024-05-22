##########
Iterations
##########


Reference
---------

* v4 API:

  + :class:`gitlab.v4.objects.GroupIteration`
  + :class:`gitlab.v4.objects.GroupIterationManager`
  + :attr:`gitlab.v4.objects.Group.iterations`
  + :class:`gitlab.v4.objects.ProjectIterationManager`
  + :attr:`gitlab.v4.objects.Project.iterations`

* GitLab API: https://docs.gitlab.com/ee/api/iterations.html

Examples
--------

.. note::

    GitLab no longer has project iterations. Using a project endpoint returns
    the ancestor groups' iterations. 

List iterations for a project's ancestor groups::

    iterations = project.iterations.list()

List iterations for a group::

    iterations = group.iterations.list()

Unavailable filters or keyword conflicts::
    
    In case you are trying to pass a parameter that collides with a python
    keyword (i.e. `in`) or with python-gitlab's internal arguments, you'll have
    to use the `query_parameters` argument:

    ```
    group.iterations.list(query_parameters={"in": "title"}) 
    ```

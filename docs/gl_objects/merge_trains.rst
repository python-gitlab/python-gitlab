############
Merge Trains
############

Reference
---------

* v4 API:

  + :class:`gitlab.v4.objects.ProjectMergeTrain`
  + :class:`gitlab.v4.objects.ProjectMergeTrainManager`
  + :attr:`gitlab.v4.objects.Project.merge_trains`

* GitLab API: https://docs.gitlab.com/ee/api/merge_trains.html

Examples
--------

List merge trains for a project::

    merge_trains = project.merge_trains.list()

List active merge trains for a project::

    merge_trains = project.merge_trains.list(scope="active")

List completed (have been merged) merge trains for a project::

    merge_trains = project.merge_trains.list(scope="complete")
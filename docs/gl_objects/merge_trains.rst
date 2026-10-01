############
Merge Trains
############

Reference
---------

* v4 API:

  + :class:`gitlab.v4.objects.ProjectMergeTrain`
  + :class:`gitlab.v4.objects.ProjectMergeTrainManager`
  + :class:`gitlab.v4.objects.ProjectMergeTrainMergeRequest`
  + :class:`gitlab.v4.objects.ProjectMergeTrainMergeRequestManager`
  + :attr:`gitlab.v4.objects.Project.merge_trains`

* GitLab API: https://docs.gitlab.com/api/merge_trains

Examples
--------

List merge trains for a project::

    merge_trains = project.merge_trains.list(get_all=True)

List active merge trains for a project::

    merge_trains = project.merge_trains.list(scope="active")

List completed (have been merged) merge trains for a project::

    merge_trains = project.merge_trains.list(scope="complete")

Get Merge Request Status for a Merge Train::

    merge_train_mr = project.merge_trains.get(1, lazy=True).merge_requests.get(1)
    merge_train_mr_status = merge_train_mr.pipeline.get("status")

Add Merge Request to a Merge Train::

    merge_train_to_update = project.merge_trains.get(1, lazy=True)
    merge_requests_update = merge_train_to_update.merge_requests.update(5, new_data={"sha": "cd22awr721ssds"})

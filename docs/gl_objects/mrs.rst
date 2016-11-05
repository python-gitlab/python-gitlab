##############
Merge requests
##############

You can use merge requests to notify a project that a branch is ready for
merging. The owner of the target projet can accept the merge request.

* Object class: :class:`~gitlab.objects.ProjectMergeRequest`
* Manager objects: :attr:`gitlab.Gitlab.project_mergerequests`,
  :attr:`Project.mergerequests <gitlab.objects.Project.mergerequests>`

Examples
--------

List MRs for a project:

.. literalinclude:: mrs.py
   :start-after: # list
   :end-before: # end list

You can filter and sort the returned list with the following parameters:

* ``iid``: iid (unique ID for the project) of the MR
* ``state``: state of the MR. It can be one of ``all``, ``merged``, '``opened``
  or ``closed``
* ``order_by``: sort by ``created_at`` or ``updated_at``
* ``sort``: sort order (``asc`` or ``desc``)

For example:

.. literalinclude:: mrs.py
   :start-after: # list
   :end-before: # end list

Get a single MR:

.. literalinclude:: mrs.py
   :start-after: # get
   :end-before: # end get

Create a MR:

.. literalinclude:: mrs.py
   :start-after: # create
   :end-before: # end create

Update a MR:

.. literalinclude:: mrs.py
   :start-after: # update
   :end-before: # end update

Change the state of a MR (close or reopen):

.. literalinclude:: mrs.py
   :start-after: # state
   :end-before: # end state

Delete a MR:

.. literalinclude:: mrs.py
   :start-after: # delete
   :end-before: # end delete

Accept a MR:

.. literalinclude:: mrs.py
   :start-after: # merge
   :end-before: # end merge

Cancel a MR when the build succeeds:

.. literalinclude:: mrs.py
   :start-after: # cancel
   :end-before: # end cancel

List issues that will close on merge:

.. literalinclude:: mrs.py
   :start-after: # issues
   :end-before: # end issues

Subscribe/unsubscribe a MR:

.. literalinclude:: mrs.py
   :start-after: # subscribe
   :end-before: # end subscribe

Mark a MR as todo:

.. literalinclude:: mrs.py
   :start-after: # todo
   :end-before: # end todo

List the diffs for a merge request:

.. literalinclude:: mrs.py
   :start-after: # diff list
   :end-before: # end diff list

Get a diff for a merge request:

.. literalinclude:: mrs.py
   :start-after: # diff get
   :end-before: # end diff get

###############
Sidekiq metrics
###############

Reference
---------

* v4 API:

  + :class:`gitlab.v4.objects.SidekiqManager`
  + :attr:`gitlab.Gitlab.sidekiq`

* GitLab API: https://docs.gitlab.com/ce/api/sidekiq_metrics.html

Examples
--------

.. code-block:: python

   gl.sidekiq.queue_metrics()
   gl.sidekiq.process_metrics()
   gl.sidekiq.job_stats()
   gl.sidekiq.compound_metrics()

###############
Sidekiq metrics
###############

Use the :attr:`gitlab.Gitlab.sideqik` manager object to access Gitlab Sidekiq
server metrics.

Examples
--------

.. code-block:: python

   gl.sidekiq.queue_metrics()
   gl.sidekiq.process_metrics()
   gl.sidekiq.job_stats()
   gl.sidekiq.compound_metrics()

##########
Statistics
##########

Reference
---------

* v4 API:

  + :class:`gitlab.v4.objects.ApplicationStatistics`
  + :class:`gitlab.v4.objects.ApplicationStatisticsManager`
  + :attr:`gitlab.Gitlab.statistics`

* GitLab API: https://docs.gitlab.com/ee/api/statistics.html

Examples
--------

Get the statistics::

    statistics = gl.statistics.get()

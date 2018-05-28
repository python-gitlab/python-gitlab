##############
Features flags
##############

Reference
---------

* v4 API:

  + :class:`gitlab.v4.objects.Feature`
  + :class:`gitlab.v4.objects.FeatureManager`
  + :attr:`gitlab.Gitlab.features`

* GitLab API: https://docs.gitlab.com/ce/api/features.html

Examples
--------

List features::

    features = gl.features.list()

Create or set a feature::

    feature = gl.features.set(feature_name, True)
    feature = gl.features.set(feature_name, 30)

Delete a feature::

    feature.delete()

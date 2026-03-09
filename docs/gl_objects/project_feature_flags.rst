#####################
Project Feature Flags
#####################

Reference
---------

* v4 API:

  + :class:`gitlab.v4.objects.ProjectFeatureFlag`
  + :class:`gitlab.v4.objects.ProjectFeatureFlagManager`
  + :attr:`gitlab.v4.objects.Project.feature_flags`

* GitLab API: https://docs.gitlab.com/ee/api/feature_flags.html

Examples
--------

List feature flags::

    flags = project.feature_flags.list()

Get a feature flag::

    flag = project.feature_flags.get('my_feature_flag')

Create a feature flag::

    flag = project.feature_flags.create({'name': 'my_feature_flag', 'version': 'new_version_flag'})

Create a feature flag with strategies::

    flag = project.feature_flags.create({
        'name': 'my_complex_flag',
        'version': 'new_version_flag',
        'strategies': [{
            'name': 'userWithId',
            'parameters': {'userIds': 'user1,user2'}
        }]
    })

Update a feature flag::

    flag.description = 'Updated description'
    flag.save()

Rename a feature flag::

    # You can rename a flag by changing its name attribute and calling save()
    flag.name = 'new_flag_name'
    flag.save()

    # Alternatively, you can use the manager's update method
    project.feature_flags.update('old_flag_name', {'name': 'new_flag_name'})

Delete a feature flag::

    flag.delete()

See also
--------

* :doc:`project_feature_flag_user_lists`

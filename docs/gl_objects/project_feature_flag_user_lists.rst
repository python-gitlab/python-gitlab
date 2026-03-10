###############################
Project Feature Flag User Lists
###############################

Reference
---------

* v4 API:

  + :class:`gitlab.v4.objects.ProjectFeatureFlagUserList`
  + :class:`gitlab.v4.objects.ProjectFeatureFlagUserListManager`
  + :attr:`gitlab.v4.objects.Project.feature_flags_user_lists`

* GitLab API: https://docs.gitlab.com/ee/api/feature_flag_user_lists.html

Examples
--------

List user lists::

    user_lists = project.feature_flags_user_lists.list()

Get a user list::

    user_list = project.feature_flags_user_lists.get(list_iid)

Create a user list::

    user_list = project.feature_flags_user_lists.create({
        'name': 'my_user_list',
        'user_xids': 'user1,user2,user3'
    })

Update a user list::

    user_list.name = 'updated_list_name'
    user_list.user_xids = 'user1,user2'
    user_list.save()

Delete a user list::

    user_list.delete()

Search for a user list::

    user_lists = project.feature_flags_user_lists.list(search='my_list')

See also
--------

* :doc:`project_feature_flags`

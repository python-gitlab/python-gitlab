######
Badges
######

Badges can be associated with groups and projects.

Reference
---------

* v4 API:

  + :class:`gitlab.v4.objects.GroupBadge`
  + :class:`gitlab.v4.objects.GroupBadgeManager`
  + :attr:`gitlab.v4.objects.Group.badges`
  + :class:`gitlab.v4.objects.ProjectBadge`
  + :class:`gitlab.v4.objects.ProjectBadgeManager`
  + :attr:`gitlab.v4.objects.Project.badges`

* GitLab API:

  + https://docs.gitlab.com/ce/api/group_badges.html
  + https://docs.gitlab.com/ce/api/project_badges.html

Examples
--------

List badges::

    badges = group_or_project.badges.list()

Get a badge::

    badge = group_or_project.badges.get(badge_id)

Create a badge::

    badge = group_or_project.badges.create({'link_url': link, 'image_url': image_link})

Update a badge::

    badge.image_url = new_image_url
    badge.link_url = new_link_url
    badge.save()

Delete a badge::

    badge.delete()

Render a badge (preview the generate URLs)::

    output = group_or_project.badges.render(link, image_link)
    print(output['rendered_link_url'])
    print(output['rendered_image_url'])

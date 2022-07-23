###########
Invitations
###########

Invitations let you invite or add users to a group or project.

Reference
---------

* v4 API:

  + :class:`gitlab.v4.objects.GroupInvitation`
  + :class:`gitlab.v4.objects.GroupInvitationManager`
  + :attr:`gitlab.v4.objects.Group.invitations`
  + :class:`gitlab.v4.objects.ProjectInvitation`
  + :class:`gitlab.v4.objects.ProjectInvitationManager`
  + :attr:`gitlab.v4.objects.Project.invitations`

* GitLab API: https://docs.gitlab.com/ce/api/invitations.html

Examples
--------

.. danger::

    Creating an invitation with ``create()`` returns a status response,
    rather than invitation details, because it allows sending multiple
    invitations at the same time.
    
    Thus when using several emails, you do not create a real invitation
    object you can manipulate, because python-gitlab cannot know which email
    to track as the ID.
    
    In that case, use a **lazy** ``get()`` method shown below using a specific
    email address to create an invitation object you can manipulate.

Create an invitation::

    invitation = group_or_project.invitations.create(
        {
            "email": "email@example.com",
            "access_level": gitlab.const.AccessLevel.DEVELOPER,
        }
    )

List invitations for a group or project::

    invitations = group_or_project.invitations.list()

.. warning::

    As mentioned above, GitLab does not provide a real GET endpoint for a single
    invitation. We can create a lazy object to later manipulate it.

Update an invitation::

    invitation = group_or_project.invitations.get("email@example.com", lazy=True)
    invitation.access_level = gitlab.const.AccessLevel.DEVELOPER
    invitation.save()

    # or
    group_or_project.invitations.update(
        "email@example.com",
        {"access_level": gitlab.const.AccessLevel.DEVELOPER}
    )

Delete an invitation::

    invitation = group_or_project.invitations.get("email@example.com", lazy=True)
    invitation.delete()

    # or
    group_or_project.invitations.delete("email@example.com")

################################
Protected container repositories
################################

You can list and manage container registry protection rules in a project.

References
----------

* v4 API:

  + :class:`gitlab.v4.objects.ProjectRegistryRepositoryProtectionRuleRule`
  + :class:`gitlab.v4.objects.ProjectRegistryRepositoryProtectionRuleRuleManager`
  + :attr:`gitlab.v4.objects.Project.registry_repository_protection_rules`

* GitLab API: https://docs.gitlab.com/ee/api/container_repository_protection_rules.html

Examples
--------

List the container registry protection rules for a project::

    registry_rules = project.registry_repository_protection_rules.list()

Create a container registry protection rule::

    registry_rule = project.registry_repository_protection_rules.create(
        {
            'repository_path_pattern': 'test/image',
            'minimum_access_level_for_push': 'maintainer',
            'minimum_access_level_for_delete': 'maintainer',
        }
    )

Update a container registry protection rule::

    registry_rule.minimum_access_level_for_push = 'owner'
    registry_rule.save()

Delete a container registry protection rule::

    registry_rule = project.registry_repository_protection_rules.delete(registry_rule.id)
    # or
    registry_rule.delete()

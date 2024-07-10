##################
Protected packages
##################

You can list and manage package protection rules in a project.

References
----------

* v4 API:

  + :class:`gitlab.v4.objects.ProjectPackageProtectionRule`
  + :class:`gitlab.v4.objects.ProjectPackageProtectionRuleManager`
  + :attr:`gitlab.v4.objects.Project.package_protection_rules`

* GitLab API: https://docs.gitlab.com/ee/api/project_packages_protection_rules.html

Examples
--------

List the package protection rules for a project::

    package_rules = project.package_protection_rules.list()

Create a package protection rule::

    package_rule = project.package_protection_rules.create(
        {
            'package_name_pattern': 'v*',
            'package_type': 'npm',
            'minimum_access_level_for_push': 'maintainer'
        }
    )

Update a package protection rule::

    package_rule.minimum_access_level_for_push = 'developer'
    package_rule.save()

Delete a package protection rule::

    package_rule = project.package_protection_rules.delete(package_rule.id)
    # or
    package_rule.delete()

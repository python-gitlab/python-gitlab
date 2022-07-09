#######
CI Lint
#######

Reference
---------

* v4 API:

  + :class:`gitlab.v4.objects.CiLint`
  + :class:`gitlab.v4.objects.CiLintManager`
  + :attr:`gitlab.Gitlab.ci_lint`
  + :class:`gitlab.v4.objects.ProjectCiLint`
  + :class:`gitlab.v4.objects.ProjectCiLintManager`
  + :attr:`gitlab.v4.objects.Project.ci_lint`

* GitLab API: https://docs.gitlab.com/ee/api/lint.html

Examples
---------

Lint a CI YAML configuration::

    gitlab_ci_yml = """.api_test:
      rules:
        - if: $CI_PIPELINE_SOURCE=="merge_request_event"
          changes:
            - src/api/*
    deploy:
      extends:
        - .api_test
      rules:
        - when: manual
          allow_failure: true
      script:
        - echo "hello world"
    """
    lint_result = gl.ci_lint.create({"content": gitlab_ci_yml})

    print(lint_result.status)  # Print the status of the CI YAML
    print(lint_result.merged_yaml)  # Print the merged YAML file

Lint a project's CI configuration::

    lint_result = project.ci_lint.get()
    assert lint_result.valid is True  # Test that the .gitlab-ci.yml is valid
    print(lint_result.merged_yaml)    # Print the merged YAML file

Lint a CI YAML configuration with a namespace::

    lint_result = project.ci_lint.create({"content": gitlab_ci_yml})
    assert lint_result.valid is True  # Test that the .gitlab-ci.yml is valid
    print(lint_result.merged_yaml)    # Print the merged YAML file

Validate a CI YAML configuration (raises ``GitlabCiLintError`` on failures)::

    # returns None
    gl.ci_lint.validate({"content": gitlab_ci_yml})

    # raises GitlabCiLintError
    gl.ci_lint.validate({"content": "invalid"})

Validate a CI YAML configuration with a namespace::

    # returns None
    project.ci_lint.validate({"content": gitlab_ci_yml})

    # raises GitlabCiLintError
    project.ci_lint.validate({"content": "invalid"})

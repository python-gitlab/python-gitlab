######################
Personal Access Tokens
######################

Get a list of personal access tokens

References
----------

* v4 API:

  + :class:`gitlab.v4.objects.PersonalAccessToken`
  + :class:`gitlab.v4.objects.PersonalAcessTokenManager`
  + :attr:`gitlab.Gitlab.personal_access_tokens`

* GitLab API: https://docs.gitlab.com/ee/api/personal_access_tokens.html

Examples
--------

List personal access tokens::

    access_tokens = gl.personal_access_tokens.list()
    print(access_tokens[0].name)

List personal access tokens from other user_id (admin only)::

    access_tokens = gl.personal_access_tokens.list(user_id=25)

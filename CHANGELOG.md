# CHANGELOG

## v4.8.0 (2024-07-16)

### Chore

* chore(deps): update gitlab/gitlab-ee docker tag to v17.1.2-ee.0 ([`6fedfa5`](https://github.com/python-gitlab/python-gitlab/commit/6fedfa546120942757ea48337ce7446914eb3813))

* chore(deps): update all non-major dependencies ([`4a2b213`](https://github.com/python-gitlab/python-gitlab/commit/4a2b2133b52dac102d6f623bf028bdef6dd5a92f))

* chore(ci): specify name of &#34;stale&#34; label

Saw the following error in the log:
  [#2618] Removing the label &#34;Stale&#34; from this issue...
  ##[error][#2618] Error when removing the label: &#34;Label does not exist&#34;

My theory is that the case doesn&#39;t match (&#34;Stale&#34; != &#34;stale&#34;) and that
is why it failed.  Our label is &#34;stale&#34; so update this to match.
Thought of changing the label name on GitHub but then would also
require a change here to the &#34;any-of-labels&#34;. So it seemed simpler to
just change it here.

It is confusing though that it detected the label &#34;stale&#34;, but then
couldn&#39;t delete it. ([`44f62c4`](https://github.com/python-gitlab/python-gitlab/commit/44f62c49106abce2099d5bb1f3f97b64971da406))

* chore(ci): stale: allow issues/PRs that have stale label to be closed

If a `stale` label is manually applied, allow the issue or PR to be
closed by the stale job.

Previously it would require the `stale` label and to also have one of
&#39;need info&#39; or &#39;Waiting for response&#39; labels added. ([`2ab88b2`](https://github.com/python-gitlab/python-gitlab/commit/2ab88b25a64bd8e028cee2deeb842476de54b109))

* chore(ci): use codecov token when available ([`b74a6fb`](https://github.com/python-gitlab/python-gitlab/commit/b74a6fb5157e55d3e4471a0c5c8378fed8075edc))

* chore(deps): update python-semantic-release/upload-to-gh-release digest to fe6cc89 ([`3f3ad80`](https://github.com/python-gitlab/python-gitlab/commit/3f3ad80ef5bb2ed837adceae061291b2b5545ed3))

* chore(deps): update all non-major dependencies ([`0f59069`](https://github.com/python-gitlab/python-gitlab/commit/0f59069420f403a17f67a5c36c81485c9016b59b))

* chore: add `show_caller` argument to `utils.warn()`

This allows us to not add the caller&#39;s location to the UserWarning
message. ([`7d04315`](https://github.com/python-gitlab/python-gitlab/commit/7d04315d7d9641d88b0649e42bf24dd160629af5))

* chore: use correct type-hint for `die()` ([`9358640`](https://github.com/python-gitlab/python-gitlab/commit/93586405fbfa61317dc75e186799549573bc0bbb))

* chore(deps): update gitlab/gitlab-ee docker tag to v17.1.1-ee.0 ([`5e98510`](https://github.com/python-gitlab/python-gitlab/commit/5e98510a6c918b33c0db0a7756e8a43a8bdd868a))

* chore(deps): update python-semantic-release/upload-to-gh-release digest to c7c3b69 ([`23393fa`](https://github.com/python-gitlab/python-gitlab/commit/23393faa0642c66a991fd88f1d2d68aed1d2f172))

* chore(deps): update all non-major dependencies ([`cf87226`](https://github.com/python-gitlab/python-gitlab/commit/cf87226a81108fbed4f58751f1c03234cc57bcf1))

### Documentation

* docs: document how to use `sudo` if modifying an object

Add a warning about using `sudo` when saving.

Give an example of how to `get` an object, modify it, and then `save`
it using `sudo`

Closes: #532 ([`d509da6`](https://github.com/python-gitlab/python-gitlab/commit/d509da60155e9470dee197d91926850ea9548de9))

* docs: variables: add note about `filter` for updating

Add a note about using `filter` when updating a variable.

Closes: #2835
Closes: #1387
Closes: #1125 ([`c378817`](https://github.com/python-gitlab/python-gitlab/commit/c378817389a9510ef508b5a3c90282e5fb60049f))

### Feature

* feat(api): add support for project cluster agents ([`32dbc6f`](https://github.com/python-gitlab/python-gitlab/commit/32dbc6f2bee5b22d18c4793f135223d9b9824d15))

* feat(api): add support for container registry protection rules ([`6d31649`](https://github.com/python-gitlab/python-gitlab/commit/6d31649190279a844bfa591a953b0556cd6fc492))

* feat(api): add support for package protection rules ([`6b37811`](https://github.com/python-gitlab/python-gitlab/commit/6b37811c3060620afd8b81e54a99d96e4e094ce9))

* feat(api): add support for commit sequence ([`1f97be2`](https://github.com/python-gitlab/python-gitlab/commit/1f97be2a540122cb872ff59500d85a35031cab5f))

### Fix

* fix: issues `closed_by()/related_merge_requests()` use `http_list`

The `closed_by()` and `related_merge_requests()` API calls return
lists. So use the `http_list()` method.

This will also warn the user if only a subset of the data is returned. ([`de2e4dd`](https://github.com/python-gitlab/python-gitlab/commit/de2e4dd7e80c7b84fd41458117a85558fcbac32d))

* fix: Have `participants()` method use `http_list()`

Previously it was using `http_get()` but the `participants` API
returns a list of participants. Also by using this then we will warn
if only a subset of the participants are returned.

Closes: #2913 ([`d065275`](https://github.com/python-gitlab/python-gitlab/commit/d065275f2fe296dd00e9bbd0f676d1596f261a85))

* fix(files): CR: add explicit comparison to `None`

Co-authored-by: Nejc Habjan &lt;hab.nejc@gmail.com&gt; ([`51d8f88`](https://github.com/python-gitlab/python-gitlab/commit/51d8f888aca469cff1c5ee5e158fb259d2862017))

* fix(files): make `ref` parameter optional in get raw file api

The `ref` parameter was made optional in gitlab v13.11.0. ([`00640ac`](https://github.com/python-gitlab/python-gitlab/commit/00640ac11f77e338919d7e9a1457d111c82af371))

* fix(cli): generate UserWarning if `list` does not return all entries

Previously in the CLI, calls to `list()` would have `get_all=False` by
default. Therefore hiding the fact that not all items are being
returned if there were more than 20 items.

Added `--no-get-all` option to `list` actions. Along with the already
existing `--get-all`.

Closes: #2900 ([`e5a4379`](https://github.com/python-gitlab/python-gitlab/commit/e5a43799b5039261d7034af909011444718a5814))

### Refactor

* refactor(package_protection_rules): add missing attributes ([`c307dd2`](https://github.com/python-gitlab/python-gitlab/commit/c307dd20e3df61b118b3b1a8191c0f1880bc9ed6))

### Test

* test(registry): disable functional tests for unavailable endpoints ([`ee393a1`](https://github.com/python-gitlab/python-gitlab/commit/ee393a16e1aa6dbf2f9785eb3ef486f7d5b9276f))

* test(files): test with and without `ref` parameter in test case ([`f316b46`](https://github.com/python-gitlab/python-gitlab/commit/f316b466c04f8ff3c0cca06d0e18ddf2d62d033c))

* test(files): omit optional `ref` parameter in test case ([`9cb3396`](https://github.com/python-gitlab/python-gitlab/commit/9cb3396d3bd83e82535a2a173b6e52b4f8c020f4))

* test(fixtures): remove deprecated config option ([`2156949`](https://github.com/python-gitlab/python-gitlab/commit/2156949866ce95af542c127ba4b069e83fcc8104))

## v4.7.0 (2024-06-28)

### Chore

* chore(deps): update all non-major dependencies ([`88de2f0`](https://github.com/python-gitlab/python-gitlab/commit/88de2f0fc52f4f02e1d44139f4404acf172624d7))

* chore(deps): update all non-major dependencies ([`a510f43`](https://github.com/python-gitlab/python-gitlab/commit/a510f43d990c3a3fd169854218b64d4eb9491628))

* chore(deps): update gitlab/gitlab-ee docker tag to v17.0.2-ee.0 ([`51779c6`](https://github.com/python-gitlab/python-gitlab/commit/51779c63e6a58e1ae68e9b1c3ffff998211d4e66))

* chore(deps): update python-semantic-release/upload-to-gh-release digest to 6b7558f ([`fd0f0b0`](https://github.com/python-gitlab/python-gitlab/commit/fd0f0b0338623a98e9368c30b600d603b966f8b7))

* chore(deps): update all non-major dependencies ([`d4fdf90`](https://github.com/python-gitlab/python-gitlab/commit/d4fdf90655c2cb5124dc2ecd8b449e1e16d0add5))

* chore(deps): update dependency types-setuptools to v70 ([`7767514`](https://github.com/python-gitlab/python-gitlab/commit/7767514a1ad4269a92a6610aa71aa8c595565a7d))

* chore(deps): update gitlab/gitlab-ee docker tag to v17.0.1-ee.0 ([`df0ff4c`](https://github.com/python-gitlab/python-gitlab/commit/df0ff4c4c1497d6449488b8577ad7188b55c41a9))

* chore(deps): update python-semantic-release/upload-to-gh-release digest to 477a404 ([`02a551d`](https://github.com/python-gitlab/python-gitlab/commit/02a551d82327b879b7a903b56b7962da552d1089))

* chore(deps): update all non-major dependencies ([`d5de288`](https://github.com/python-gitlab/python-gitlab/commit/d5de28884f695a79e49605a698c4f17b868ddeb8))

* chore: add a help message for `gitlab project-key enable`

Add some help text for `gitlab project-key enable`. This both adds
help text and shows how to use the new `help` feature.

Example:

$ gitlab project-key --help
usage: gitlab project-key [-h] {list,get,create,update,delete,enable} ...

options:
  -h, --help            show this help message and exit

action:
  {list,get,create,update,delete,enable}
                        Action to execute on the GitLab resource.
    list                List the GitLab resources
    get                 Get a GitLab resource
    create              Create a GitLab resource
    update              Update a GitLab resource
    delete              Delete a GitLab resource
    enable              Enable a deploy key for the project ([`1291dbb`](https://github.com/python-gitlab/python-gitlab/commit/1291dbb588d3a5a54ee54d9bb93c444ce23efa8c))

* chore: sort CLI behavior-related args to remove

Sort the list of CLI behavior-related args that are to be removed. ([`9b4b0ef`](https://github.com/python-gitlab/python-gitlab/commit/9b4b0efa1ccfb155aee8384de9e00f922b989850))

### Feature

* feat(api): add support for latest pipeline ([`635f5a7`](https://github.com/python-gitlab/python-gitlab/commit/635f5a7128c780880824f69a9aba23af148dfeb4))

* feat: add `--no-mask-credentials` CLI argument

This gives the ability to not mask credentials when using the
`--debug` argument. ([`18aa1fc`](https://github.com/python-gitlab/python-gitlab/commit/18aa1fc074b9f477cf0826933184bd594b63b489))

### Fix

* fix: add ability to add help to custom_actions

Now when registering a custom_action can add help text if desired.

Also delete the VerticalHelpFormatter as no longer needed. When the
help value is set to `None` or some other value, the actions will get
printed vertically. Before when the help value was not set the actions
would all get put onto one line. ([`9acd2d2`](https://github.com/python-gitlab/python-gitlab/commit/9acd2d23dd8c87586aa99c70b4b47fa47528472b))

## v4.6.0 (2024-05-28)

### Chore

* chore(deps): update python-semantic-release/upload-to-gh-release digest to 673709c ([`1b550ac`](https://github.com/python-gitlab/python-gitlab/commit/1b550ac706c8c31331a7a9dac607aed49f5e1fcf))

* chore(deps): update all non-major dependencies ([`4c7014c`](https://github.com/python-gitlab/python-gitlab/commit/4c7014c13ed63f994e05b498d63b93dc8ab90c2e))

* chore: update commit reference in git-blame-ignore-revs ([`d0fd5ad`](https://github.com/python-gitlab/python-gitlab/commit/d0fd5ad5a70e7eb70aedba5a0d3082418c5ffa34))

* chore(cli): add ability to not add `_id_attr` as an argument

In some cases we don&#39;t want to have `_id_attr` as an argument.

Add ability to have it not be added as an argument. ([`2037352`](https://github.com/python-gitlab/python-gitlab/commit/20373525c1a1f98c18b953dbef896b2570d3d191))

* chore: create a CustomAction dataclass ([`61d8679`](https://github.com/python-gitlab/python-gitlab/commit/61d867925772cf38f20360c9b40140ac3203efb9))

* chore: add an initial .git-blame-ignore-revs

This adds the `.git-blame-ignore-revs` file which allows ignoring
certain commits when doing a `git blame --ignore-revs`

Ignore the commit that requires keyword arguments for
`register_custom_action()`

https://docs.github.com/en/repositories/working-with-files/using-files/viewing-a-file#ignore-commits-in-the-blame-view ([`74db84c`](https://github.com/python-gitlab/python-gitlab/commit/74db84ca878ec7029643ff7b00db55f9ea085e9b))

* chore: require keyword arguments for register_custom_action

This makes it more obvious when reading the code what each argument is
for. ([`7270523`](https://github.com/python-gitlab/python-gitlab/commit/7270523ad89a463c3542e072df73ba2255a49406))

* chore: remove typing-extensions from requirements.txt

We no longer support Python versions before 3.8. So it isn&#39;t needed
anymore. ([`d569128`](https://github.com/python-gitlab/python-gitlab/commit/d56912835360a1b5a03a20390fb45cb5e8b49ce4))

* chore(deps): update dependency requests to v2.32.0 [security] ([`1bc788c`](https://github.com/python-gitlab/python-gitlab/commit/1bc788ca979a36eeff2e35241bdefc764cf335ce))

* chore(deps): update all non-major dependencies ([`ba1eec4`](https://github.com/python-gitlab/python-gitlab/commit/ba1eec49556ee022de471aae8d15060189f816e3))

* chore(deps): update gitlab/gitlab-ee docker tag to v17 ([`5070d07`](https://github.com/python-gitlab/python-gitlab/commit/5070d07d13b9c87588dbfde3750340e322118779))

* chore(cli): on the CLI help show the API endpoint of resources

This makes it easier for people to map CLI command names to the API.

Looks like this:
    $ gitlab --help
    &lt;snip&gt;
                            The GitLab resource to manipulate.
        application         API endpoint: /applications
        application-appearance
                            API endpoint: /application/appearance
        application-settings
                            API endpoint: /application/settings
        application-statistics
                            API endpoint: /application/statistics
    &lt;snip&gt; ([`f1ef565`](https://github.com/python-gitlab/python-gitlab/commit/f1ef5650c3201f3883eb04ad90a874e8adcbcde2))

* chore(cli): add some simple help for the standard operations

Add help for the following standard operations:
  * list: List the GitLab resources
  * get: Get a GitLab resource
  * create: Create a GitLab resource
  * update: Update a GitLab resource
  * delete: Delete a GitLab resource

For example:
  $ gitlab project-key --help
  usage: gitlab project-key [-h] {list,get,create,update,delete,enable} ...

  options:
    -h, --help            show this help message and exit

  action:
    list
    get
    create
    update
    delete
    enable
                          Action to execute on the GitLab resource.
      list                List the GitLab resources
      get                 Get a GitLab resource
      create              Create a GitLab resource
      update              Update a GitLab resource
      delete              Delete a GitLab resource ([`5a4a940`](https://github.com/python-gitlab/python-gitlab/commit/5a4a940f42e43ed066838503638fe612813e504f))

* chore: correct type-hint for `job.trace()`

Closes: #2808 ([`840572e`](https://github.com/python-gitlab/python-gitlab/commit/840572e4fa36581405b604a985d0e130fe43f4ce))

* chore: add type info for ProjectFile.content

Closes: #2821 ([`62fa271`](https://github.com/python-gitlab/python-gitlab/commit/62fa2719ea129b3428e5e67d3d3a493f9aead863))

### Feature

* feat(api):  add additional parameter to project/group iteration search (#2796)

Co-authored-by: Cristiano Casella &lt;cristiano.casella@seacom.it&gt;
Co-authored-by: Nejc Habjan &lt;hab.nejc@gmail.com&gt; ([`623dac9`](https://github.com/python-gitlab/python-gitlab/commit/623dac9c8363c61dbf53f72af58835743e96656b))

* feat(api): add support for gitlab service account (#2851)


Co-authored-by: Nejc Habjan &lt;hab.nejc@siemens.com&gt; ([`b187dea`](https://github.com/python-gitlab/python-gitlab/commit/b187deadabbfdf0326ecd79a3ee64c9de10c53e0))

* feat: more usernames support for MR approvals

I don&#39;t think commit a2b8c8ccfb5d went far enough to enable usernames
support. We create and edit a lot of approval rules based on an external
service (similar to CODE_OWNERS), but only have the usernames available,
and currently, have to look up each user to get their user ID to populate
user_ids for .set_approvers() calls. Would very much like to skip the
lookup and just send the usernames, which this change should allow.

See: https://docs.gitlab.com/ee/api/merge_request_approvals.html#create-project-level-rule

Signed-off-by: Jarod Wilson &lt;jarod@redhat.com&gt; ([`12d195a`](https://github.com/python-gitlab/python-gitlab/commit/12d195a35a1bd14947fbd6688a8ad1bd3fc21617))

### Fix

* fix(deps): update minimum dependency versions in pyproject.toml

Update the minimum versions of the dependencies in the pyproject.toml
file.

This is related to PR #2878 ([`37b5a70`](https://github.com/python-gitlab/python-gitlab/commit/37b5a704ef6b94774e54110ba3746a950e733986))

* fix(cli): don&#39;t require `--id` when enabling a deploy key

No longer require `--id` when doing:
  gitlab project-key enable

Now only the --project-id and --key-id are required. ([`98fc578`](https://github.com/python-gitlab/python-gitlab/commit/98fc5789d39b81197351660b7a3f18903c2b91ba))

* fix: don&#39;t raise `RedirectError` for redirected `HEAD` requests ([`8fc13b9`](https://github.com/python-gitlab/python-gitlab/commit/8fc13b91d63d57c704d03b98920522a6469c96d7))

* fix: handle large number of approval rules

Use `iterator=True` when going through the list of current approval
rules. This allows it to handle more than the default of 20 approval
rules.

Closes: #2825 ([`ef8f0e1`](https://github.com/python-gitlab/python-gitlab/commit/ef8f0e190b1add3bbba9a7b194aba2f3c1a83b2e))

* fix(projects): fix &#39;import_project&#39; file argument type for typings

Signed-off-by: Adrian DC &lt;radian.dc@gmail.com&gt; ([`33fbc14`](https://github.com/python-gitlab/python-gitlab/commit/33fbc14ea8432df7e637462379e567f4d0ad6c18))

## v4.5.0 (2024-05-13)

### Build

* build: Add &#34;--no-cache-dir&#34; to pip commands in Dockerfile

This would not leave cache files in the built docker image.

Additionally, also only build the wheel in the build phase.

On my machine, before this PR, size is 74845395; after this PR, size is
72617713. ([`4ef94c8`](https://github.com/python-gitlab/python-gitlab/commit/4ef94c8260e958873bb626e86d3241daa22f7ce6))

### Chore

* chore(deps): update all non-major dependencies ([`4f338ae`](https://github.com/python-gitlab/python-gitlab/commit/4f338aed9c583a20ff5944e6ccbba5737c18b0f4))

* chore(deps): update gitlab/gitlab-ee docker tag to v16.11.2-ee.0 ([`9be48f0`](https://github.com/python-gitlab/python-gitlab/commit/9be48f0bcc2d32b5e8489f62f963389d5d54b2f2))

* chore(deps): update dependency myst-parser to v3 ([`9289189`](https://github.com/python-gitlab/python-gitlab/commit/92891890eb4730bc240213a212d392bcb869b800))

* chore(deps): update all non-major dependencies ([`65d0e65`](https://github.com/python-gitlab/python-gitlab/commit/65d0e6520dcbcf5a708a87960c65fdcaf7e44bf3))

* chore(deps): update dependency jinja2 to v3.1.4 [security] ([`8ea10c3`](https://github.com/python-gitlab/python-gitlab/commit/8ea10c360175453c721ad8e27386e642c2b68d88))

* chore(deps): update all non-major dependencies ([`1f0343c`](https://github.com/python-gitlab/python-gitlab/commit/1f0343c1154ca8ae5b1f61de1db2343a2ad652ec))

* chore(deps): update gitlab/gitlab-ee docker tag to v16.11.1-ee.0 ([`1ed8d6c`](https://github.com/python-gitlab/python-gitlab/commit/1ed8d6c21d3463b2ad09eb553871042e98090ffd))

* chore(deps): update all non-major dependencies ([`0e9f4da`](https://github.com/python-gitlab/python-gitlab/commit/0e9f4da30cea507fcf83746008d9de2ee5a3bb9d))

* chore(deps): update gitlab/gitlab-ee docker tag to v16 ([`ea8c4c2`](https://github.com/python-gitlab/python-gitlab/commit/ea8c4c2bc9f17f510415a697e0fb19cabff4135e))

* chore(deps): update all non-major dependencies ([`d5b5fb0`](https://github.com/python-gitlab/python-gitlab/commit/d5b5fb00d8947ed9733cbb5a273e2866aecf33bf))

* chore(deps): update dependency pytest-cov to v5 ([`db32000`](https://github.com/python-gitlab/python-gitlab/commit/db3200089ea83588ea7ad8bd5a7175d81f580630))

* chore: update `mypy` to 1.9.0 and resolve one issue

mypy 1.9.0 flagged one issue in the code. Resolve the issue. Current
unit tests already check that a `None` value returns `text/plain`. So
function is still working as expected. ([`dd00bfc`](https://github.com/python-gitlab/python-gitlab/commit/dd00bfc9c832aba0ed377573fe2e9120b296548d))

* chore(deps): update dependency black to v24.3.0 [security] ([`f6e8692`](https://github.com/python-gitlab/python-gitlab/commit/f6e8692cfc84b5af2eb6deec4ae1c4935b42e91c))

* chore(deps): update all non-major dependencies ([`14a3ffe`](https://github.com/python-gitlab/python-gitlab/commit/14a3ffe4cc161be51a39c204350b5cd45c602335))

* chore(deps): update all non-major dependencies ([`3c4dcca`](https://github.com/python-gitlab/python-gitlab/commit/3c4dccaf51695334a5057b85d5ff4045739d1ad1))

* chore(deps): update all non-major dependencies ([`04c569a`](https://github.com/python-gitlab/python-gitlab/commit/04c569a2130d053e35c1f2520ef8bab09f2f9651))

* chore: add tox `labels` to enable running groups of environments

tox now has a feature of `labels` which allows running groups of
environments using the command `tox -m LABEL_NAME`. For example
`tox -m lint` which has been setup to run the linters.

Bumped the minimum required version of tox to be 4.0, which was
released over a year ago. ([`d7235c7`](https://github.com/python-gitlab/python-gitlab/commit/d7235c74f8605f4abfb11eb257246864c7dcf709))

* chore: add py312 &amp; py313 to tox environment list

Even though there isn&#39;t a Python 3.13 at this time, this is done for
the future.  tox is already configured to just warn about missing
Python versions, but not fail if they don&#39;t exist. ([`679ddc7`](https://github.com/python-gitlab/python-gitlab/commit/679ddc7587d2add676fd2398cb9673bd1ca272e3))

* chore(deps): update python-semantic-release/python-semantic-release action to v9 ([`e11d889`](https://github.com/python-gitlab/python-gitlab/commit/e11d889cd19ec1555b2bbee15355a8cdfad61d5f))

* chore(deps): update all non-major dependencies ([`3c4b27e`](https://github.com/python-gitlab/python-gitlab/commit/3c4b27e64f4b51746b866f240a1291c2637355cc))

* chore(deps): update dependency furo to v2024 ([`f6fd02d`](https://github.com/python-gitlab/python-gitlab/commit/f6fd02d956529e2c4bce261fe7b3da1442aaea12))

* chore(deps): update dependency pytest to v8 ([`253babb`](https://github.com/python-gitlab/python-gitlab/commit/253babb9a7f8a7d469440fcfe1b2741ddcd8475e))

* chore(deps): update dependency pytest-docker to v3 ([`35d2aec`](https://github.com/python-gitlab/python-gitlab/commit/35d2aec04532919d6dd7b7090bc4d5209eddd10d))

* chore: update version of `black` for `pre-commit`

The version of `black` needs to be updated to be in sync with what is
in `requirements-lint.txt` ([`3501716`](https://github.com/python-gitlab/python-gitlab/commit/35017167a80809a49351f9e95916fafe61c7bfd5))

* chore(deps): update all non-major dependencies ([`7dc2fa6`](https://github.com/python-gitlab/python-gitlab/commit/7dc2fa6e632ed2c9adeb6ed32c4899ec155f6622))

* chore(deps): update codecov/codecov-action action to v4 ([`d2be1f7`](https://github.com/python-gitlab/python-gitlab/commit/d2be1f7608acadcc2682afd82d16d3706b7f7461))

* chore: adapt style for black v24 ([`4e68d32`](https://github.com/python-gitlab/python-gitlab/commit/4e68d32c77ed587ab42d229d9f44c3bc40d1d0e5))

* chore(deps): update dependency black to v24 ([`f59aee3`](https://github.com/python-gitlab/python-gitlab/commit/f59aee3ddcfaeeb29fcfab4cc6768dff6b5558cb))

* chore(deps): update all non-major dependencies ([`48726fd`](https://github.com/python-gitlab/python-gitlab/commit/48726fde9b3c2424310ff590b366b9fdefa4a146))

### Documentation

* docs: add FAQ about conflicting parameters

We have received multiple issues lately about this. Add it to the FAQ. ([`683ce72`](https://github.com/python-gitlab/python-gitlab/commit/683ce723352cc09e1a4b65db28be981ae6bb9f71))

* docs(README): tweak GitLab CI usage docs ([`d9aaa99`](https://github.com/python-gitlab/python-gitlab/commit/d9aaa994568ad4896a1e8a0533ef0d1d2ba06bfa))

* docs: how to run smoke tests

Signed-off-by: Tim Knight &lt;tim.knight1@engineering.digital.dwp.gov.uk&gt; ([`2d1f487`](https://github.com/python-gitlab/python-gitlab/commit/2d1f4872390df10174f865f7a935bc73f7865fec))

* docs(objects): minor rst formatting typo

To correctly format a code block have to use `::` ([`57dfd17`](https://github.com/python-gitlab/python-gitlab/commit/57dfd1769b4e22b43dc0936aa3600cd7e78ba289))

* docs: correct rotate token example

Rotate token returns a dict. Change example to print the entire dict.

Closes: #2836 ([`c53e695`](https://github.com/python-gitlab/python-gitlab/commit/c53e6954f097ed10d52b40660d2fba73c2e0e300))

* docs: Note how to use the Docker image from within GitLab CI

Ref: #2823 ([`6d4bffb`](https://github.com/python-gitlab/python-gitlab/commit/6d4bffb5aaa676d32fc892ef1ac002973bc040cb))

* docs(artifacts): Fix argument indentation ([`c631eeb`](https://github.com/python-gitlab/python-gitlab/commit/c631eeb55556920f5975b1fa2b1a0354478ce3c0))

### Feature

* feat(job_token_scope): support Groups in job token allowlist API  (#2816)

* feat(job_token_scope): support job token access allowlist API

Signed-off-by: Tim Knight &lt;tim.knight1@engineering.digital.dwp.gov.uk&gt;
l.dwp.gov.uk&gt;
Co-authored-by: Nejc Habjan &lt;nejc.habjan@siemens.com&gt; ([`2d1b749`](https://github.com/python-gitlab/python-gitlab/commit/2d1b7499a93db2c9600b383e166f7463a5f22085))

* feat(cli): allow skipping initial auth calls ([`001e596`](https://github.com/python-gitlab/python-gitlab/commit/001e59675f4a417a869f813d79c298a14268b87d))

* feat(api): allow updating protected branches (#2771)

* feat(api): allow updating protected branches

Closes #2390 ([`a867c48`](https://github.com/python-gitlab/python-gitlab/commit/a867c48baa6f10ffbfb785e624a6e3888a859571))

### Fix

* fix: Consider `scope` an ArrayAttribute in PipelineJobManager

List query params like &#39;scope&#39; were not being handled correctly for
pipeline/jobs endpoint.
This change ensures multiple values are appended with &#39;[]&#39;, resulting in
the correct URL structure.

Signed-off-by: Guilherme Gallo &lt;guilherme.gallo@collabora.com&gt;

---

Background:
If one queries for pipeline jobs with `scope=[&#34;failed&#34;, &#34;success&#34;]`

One gets:
GET /api/v4/projects/176/pipelines/1113028/jobs?scope=success&amp;scope=failed

But it is supposed to get:
GET /api/v4/projects/176/pipelines/1113028/jobs?scope[]=success&amp;scope[]=failed

The current version only considers the last element of the list argument.

Signed-off-by: Guilherme Gallo &lt;guilherme.gallo@collabora.com&gt; ([`c5d0404`](https://github.com/python-gitlab/python-gitlab/commit/c5d0404ac9edfbfd328e7b4f07f554366377df3f))

* fix(test): use different ids for merge request, approval rule, project

The original bug was that the merge request identifier was used instead of the
approval rule identifier. The test didn&#39;t notice that because it used `1` for
all identifiers. Make these identifiers different so that a mixup will become
apparent. ([`c23e6bd`](https://github.com/python-gitlab/python-gitlab/commit/c23e6bd5785205f0f4b4c80321153658fc23fb98))

* fix(api): fix saving merge request approval rules

Closes #2548 ([`b8b3849`](https://github.com/python-gitlab/python-gitlab/commit/b8b3849b2d4d3f2d9e81e5cf4f6b53368f7f0127))

* fix: user.warn() to show correct filename of issue

Previously would only go to the 2nd level of the stack for determining
the offending filename and line number. When it should be showing the
first filename outside of the python-gitlab source code. As we want it
to show the warning for the user of the libraries code.

Update test to show it works as expected. ([`529f1fa`](https://github.com/python-gitlab/python-gitlab/commit/529f1faacee46a88cb0a542306309eb835516796))

* fix(api): update manual job status when playing it ([`9440a32`](https://github.com/python-gitlab/python-gitlab/commit/9440a3255018d6a6e49269caf4c878d80db508a8))

* fix(cli): allow exclusive arguments as optional (#2770)

* fix(cli): allow exclusive arguments as optional

The CLI takes its arguments from the RequiredOptional, which has three fields: required, optional, and exclusive. In practice, the exclusive options are not defined as either required or optional, and would not be allowed in the CLI. This changes that, so that exclusive options are also added to the argument parser.

  * fix(cli): inform argument parser that options are mutually exclusive

  * fix(cli): use correct exclusive options, add unit test

Closes #2769 ([`7ec3189`](https://github.com/python-gitlab/python-gitlab/commit/7ec3189d6eacdb55925e8be886a44d7ee09eb9ca))

### Test

* test: remove approve step

Signed-off-by: Tim Knight &lt;tim.knight1@engineering.digital.dwp.gov.uk&gt; ([`48a6705`](https://github.com/python-gitlab/python-gitlab/commit/48a6705558c5ab6fb08c62a18de350a5985099f8))

* test: tidy up functional tests

Signed-off-by: Tim Knight &lt;tim.knight1@engineering.digital.dwp.gov.uk&gt; ([`06266ea`](https://github.com/python-gitlab/python-gitlab/commit/06266ea5966c601c035ad8ce5840729e5f9baa57))

* test: update api tests for GL 16.10

- Make sure we&#39;re testing python-gitlab functionality,
make sure we&#39;re not awaiting on Gitlab Async functions
- Decouple and improve test stability

Signed-off-by: Tim Knight &lt;tim.knight1@engineering.digital.dwp.gov.uk&gt; ([`4bef473`](https://github.com/python-gitlab/python-gitlab/commit/4bef47301342703f87c1ce1d2920d54f9927a66a))

* test(functional): enable bulk import feature flag before test ([`b81da2e`](https://github.com/python-gitlab/python-gitlab/commit/b81da2e66ce385525730c089dbc2a5a85ba23287))

* test: don&#39;t use weak passwords

Newer versions of GitLab will refuse to create a user with a weak
password. In order for us to move to a newer GitLab version in testing
use a stronger password for the tests that create a user. ([`c64d126`](https://github.com/python-gitlab/python-gitlab/commit/c64d126142cc77eae4297b8deec27bb1d68b7a13))

* test: update tests for gitlab 16.8 functionality

- use programmatic dates for expires_at in tokens tests
- set PAT for 16.8 into tests

Signed-off-by: Tim Knight &lt;tim.knight1@engineering.digital.dwp.gov.uk&gt; ([`f8283ae`](https://github.com/python-gitlab/python-gitlab/commit/f8283ae69efd86448ae60d79dd8321af3f19ba1b))

* test(smoke): normalize all dist titles for smoke tests ([`ee013fe`](https://github.com/python-gitlab/python-gitlab/commit/ee013fe1579b001b4b30bae33404e827c7bdf8c1))

## v4.4.0 (2024-01-15)

### Chore

* chore(deps): update all non-major dependencies ([`550f935`](https://github.com/python-gitlab/python-gitlab/commit/550f9355d29a502bb022f68dab6c902bf6913552))

* chore(deps): update pre-commit hook pycqa/flake8 to v7 ([`9a199b6`](https://github.com/python-gitlab/python-gitlab/commit/9a199b6089152e181e71a393925e0ec581bc55ca))

* chore(deps): update dependency jinja2 to v3.1.3 [security] ([`880913b`](https://github.com/python-gitlab/python-gitlab/commit/880913b67cce711d96e89ce6813e305e4ba10908))

* chore(deps): update dependency flake8 to v7 ([`20243c5`](https://github.com/python-gitlab/python-gitlab/commit/20243c532a8a6d28eee0caff5b9c30cc7376a162))

* chore(deps): update all non-major dependencies ([`cbc13a6`](https://github.com/python-gitlab/python-gitlab/commit/cbc13a61e0f15880b49a3d0208cc603d7d0b57e3))

* chore(ci): align upload and download action versions ([`dcca59d`](https://github.com/python-gitlab/python-gitlab/commit/dcca59d1a5966283c1120cfb639c01a76214d2b2))

* chore(deps): update actions/upload-artifact action to v4 ([`7114af3`](https://github.com/python-gitlab/python-gitlab/commit/7114af341dd12b7fb63ffc08650c455ead18ab70))

* chore(ci): add Python 3.13 development CI job

Add a job to test the development versions of Python 3.13. ([`ff0c11b`](https://github.com/python-gitlab/python-gitlab/commit/ff0c11b7b75677edd85f846a4dbdab08491a6bd7))

* chore(deps): update all non-major dependencies ([`369a595`](https://github.com/python-gitlab/python-gitlab/commit/369a595a8763109a2af8a95a8e2423ebb30b9320))

### Feature

* feat(api): add reviewer_details manager for mergrequest to get reviewers of merge request

Those changes implements &#39;GET /projects/:id/merge_requests/:merge_request_iid/reviewers&#39; gitlab API call.
Naming for call is not reviewers because reviewers atribute already presen in merge request response ([`adbd90c`](https://github.com/python-gitlab/python-gitlab/commit/adbd90cadffe1d9e9716a6e3826f30664866ad3f))

* feat(api): support access token rotate API ([`b13971d`](https://github.com/python-gitlab/python-gitlab/commit/b13971d5472cb228f9e6a8f2fa05a7cc94d03ebe))

* feat(api): support single resource access token get API ([`dae9e52`](https://github.com/python-gitlab/python-gitlab/commit/dae9e522a26041f5b3c6461cc8a5e284f3376a79))

### Fix

* fix(cli): support binary files with `@` notation

Support binary files being used in the CLI with arguments using the
`@` notation. For example `--avatar @/path/to/avatar.png`

Also explicitly catch the common OSError exception, which is the
parent exception for things like: FileNotFoundError, PermissionError
and more exceptions.

Remove the bare exception handling. We would rather have the full
traceback of any exceptions that we don&#39;t know about and add them
later if needed.

Closes: #2752 ([`57749d4`](https://github.com/python-gitlab/python-gitlab/commit/57749d46de1d975aacb82758c268fc26e5e6ed8b))

## v4.3.0 (2023-12-28)

### Chore

* chore(deps): update all non-major dependencies ([`d7bdb02`](https://github.com/python-gitlab/python-gitlab/commit/d7bdb0257a5587455c3722f65c4a632f24d395be))

* chore(deps): update actions/stale action to v9 ([`c01988b`](https://github.com/python-gitlab/python-gitlab/commit/c01988b12c7745929d0c591f2fa265df2929a859))

* chore(deps): update all non-major dependencies ([`9e067e5`](https://github.com/python-gitlab/python-gitlab/commit/9e067e5c67dcf9f5e6c3408b30d9e2525c768e0a))

* chore(deps): update actions/setup-python action to v5 ([`fad1441`](https://github.com/python-gitlab/python-gitlab/commit/fad14413f4f27f1b6f902703b5075528aac52451))

* chore(deps): update all non-major dependencies ([`bb2af7b`](https://github.com/python-gitlab/python-gitlab/commit/bb2af7bfe8aa59ea8b9ad7ca2d6e56f4897b704a))

* chore(deps): update all non-major dependencies ([`5ef1b4a`](https://github.com/python-gitlab/python-gitlab/commit/5ef1b4a6c8edd34c381c6e08cd3893ef6c0685fd))

* chore(deps): update dependency types-setuptools to v69 ([`de11192`](https://github.com/python-gitlab/python-gitlab/commit/de11192455f1c801269ecb3bdcbc7c5b769ff354))

### Documentation

* docs: fix rst link typo in CONTRIBUTING.rst ([`2b6da6e`](https://github.com/python-gitlab/python-gitlab/commit/2b6da6e63c82a61b8e21d193cfd46baa3fcf8937))

### Feature

* feat(api): add support for the Draft notes API (#2728)

* feat(api): add support for the Draft notes API

* fix(client): handle empty 204 reponses in PUT requests ([`ebf9d82`](https://github.com/python-gitlab/python-gitlab/commit/ebf9d821cfc36071fca05d38b82c641ae30c974c))

### Fix

* fix(cli): add ability to disable SSL verification

Add a `--no-ssl-verify` option to disable SSL verification

Closes: #2714 ([`3fe9fa6`](https://github.com/python-gitlab/python-gitlab/commit/3fe9fa64d9a38bc77950046f2950660d8d7e27a6))

## v4.2.0 (2023-11-28)

### Chore

* chore(deps): update all non-major dependencies ([`8aeb853`](https://github.com/python-gitlab/python-gitlab/commit/8aeb8531ebd3ddf0d1da3fd74597356ef65c00b3))

* chore(deps): update dessant/lock-threads action to v5 ([`f4ce867`](https://github.com/python-gitlab/python-gitlab/commit/f4ce86770befef77c7c556fd5cfe25165f59f515))

* chore(deps): update all non-major dependencies ([`9fe2335`](https://github.com/python-gitlab/python-gitlab/commit/9fe2335b9074feaabdb683b078ff8e12edb3959e))

* chore(deps): update all non-major dependencies ([`91e66e9`](https://github.com/python-gitlab/python-gitlab/commit/91e66e9b65721fa0e890a6664178d77ddff4272a))

* chore(deps): update all non-major dependencies ([`d0546e0`](https://github.com/python-gitlab/python-gitlab/commit/d0546e043dfeb988a161475de53d4ec7d756bdd9))

### Feature

* feat: add pipeline status as Enum

https://docs.gitlab.com/ee/api/pipelines.html ([`4954bbc`](https://github.com/python-gitlab/python-gitlab/commit/4954bbcd7e8433aac672405f3f4741490cb4561a))

* feat(api): add support for wiki attachments (#2722)

Added UploadMixin in mixin module
Added UploadMixin dependency for Project, ProjectWiki, GroupWiki
Added api tests for wiki upload
Added unit test for mixin
Added docs sections to wikis.rst ([`7b864b8`](https://github.com/python-gitlab/python-gitlab/commit/7b864b81fd348c6a42e32ace846d1acbcfc43998))

## v4.1.1 (2023-11-03)

### Chore

* chore(ci): add release id to workflow step ([`9270e10`](https://github.com/python-gitlab/python-gitlab/commit/9270e10d94101117bec300c756889e4706f41f36))

* chore(deps): update all non-major dependencies ([`32954fb`](https://github.com/python-gitlab/python-gitlab/commit/32954fb95dcc000100b48c4b0b137ebe2eca85a3))

### Documentation

* docs(users): add missing comma in v4 API create runner examples

The examples which show usage of new runner registration api endpoint
are missing commas. This change adds the missing commas. ([`b1b2edf`](https://github.com/python-gitlab/python-gitlab/commit/b1b2edfa05be8b957c796dc6d111f40c9f753dcf))

### Fix

* fix(build): include py.typed in dists ([`b928639`](https://github.com/python-gitlab/python-gitlab/commit/b928639f7ca252e0abb8ded8f9f142316a4dc823))

## v4.1.0 (2023-10-28)

### Chore

* chore(deps): update all non-major dependencies ([`bf68485`](https://github.com/python-gitlab/python-gitlab/commit/bf68485613756e9916de1bb10c8c4096af4ffd1e))

* chore(CHANGELOG): re-add v4.0.0 changes using old format ([`258a751`](https://github.com/python-gitlab/python-gitlab/commit/258a751049c8860e39097b26d852d1d889892d7a))

* chore(CHANGELOG): revert python-semantic-release format change ([`b5517e0`](https://github.com/python-gitlab/python-gitlab/commit/b5517e07da5109b1a43db876507d8000d87070fe))

* chore: add source label to container image ([`7b19278`](https://github.com/python-gitlab/python-gitlab/commit/7b19278ac6b7a106bc518f264934c7878ffa49fb))

* chore(rtd): revert to python 3.11 (#2694) ([`1113742`](https://github.com/python-gitlab/python-gitlab/commit/1113742d55ea27da121853130275d4d4de45fd8f))

### Ci

* ci: remove unneeded GitLab auth ([`fd7bbfc`](https://github.com/python-gitlab/python-gitlab/commit/fd7bbfcb9500131e5d3a263d7b97c8b59f80b7e2))

### Feature

* feat: add Merge Request merge_status and detailed_merge_status values as constants ([`e18a424`](https://github.com/python-gitlab/python-gitlab/commit/e18a4248068116bdcb7af89897a0c4c500f7ba57))

### Fix

* fix: remove depricated MergeStatus ([`c6c012b`](https://github.com/python-gitlab/python-gitlab/commit/c6c012b9834b69f1fe45689519fbcd92928cfbad))

## v4.0.0 (2023-10-17)

### Breaking

* docs(advanced): document new netrc behavior

BREAKING CHANGE: python-gitlab now explicitly passes auth to requests, meaning
it will only read netrc credentials if no token is provided, fixing a bug where
netrc credentials took precedence over OAuth tokens. This also affects the CLI,
where all environment variables now take precedence over netrc files. ([`45b8930`](https://github.com/python-gitlab/python-gitlab/commit/45b89304d9745be1b87449805bf53d45bf740e90))

* refactor(build): build project using PEP 621

BREAKING CHANGE: python-gitlab now stores metadata in pyproject.toml
as per PEP 621, with setup.py removed. pip version v21.1 or higher is
required if you want to perform an editable install. ([`71fca8c`](https://github.com/python-gitlab/python-gitlab/commit/71fca8c8f5c7f3d6ab06dd4e6c0d91003705be09))

* refactor(const): remove deprecated global constant import

BREAKING CHANGE: Constants defined in `gitlab.const` can no longer be imported globally from `gitlab`.
Import them from `gitlab.const` instead. ([`e4a1f6e`](https://github.com/python-gitlab/python-gitlab/commit/e4a1f6e2d1c4e505f38f9fd948d0fea9520aa909))

* refactor(list): `as_list` support is removed.

In `list()` calls support for the `as_list` argument has been removed.
`as_list` was previously deprecated and now the use of `iterator` will
be required if wanting to have same functionality as using `as_list`

BREAKING CHANGE: Support for the deprecated `as_list` argument in
`list()` calls has been removed. Use `iterator` instead. ([`9b6d89e`](https://github.com/python-gitlab/python-gitlab/commit/9b6d89edad07979518a399229c6f55bffeb9af08))

* refactor(lint): remove deprecated `lint()`in favor of `ci_lint.create()`

BREAKING CHANGE: The deprecated `lint()` method is no longer available.
Use `ci_lint.create()` instead. ([`0b17a2d`](https://github.com/python-gitlab/python-gitlab/commit/0b17a2d24a3f9463dfbcab6b4fddfba2aced350b))

* refactor(artifacts): remove deprecated `artifact()`in favor of `artifacts.raw()`

BREAKING CHANGE: The deprecated `project.artifact()` method is no longer available.
Use `project.artifacts.raw()` instead. ([`90134c9`](https://github.com/python-gitlab/python-gitlab/commit/90134c949b38c905f9cacf3b4202c25dec0282f3))

* refactor(artifacts): remove deprecated `artifacts()`in favor of `artifacts.download()`

BREAKING CHANGE: The deprecated `project.artifacts()` method is no longer available.
Use `project.artifacts.download()` instead. ([`42639f3`](https://github.com/python-gitlab/python-gitlab/commit/42639f3ec88f3a3be32e36b97af55240e98c1d9a))

* refactor(groups): remove deprecated LDAP group link add/delete methods

BREAKING CHANGE: The deprecated `group.add_ldap_group_link()` and `group.delete_ldap_group_link()`
methods are no longer available. Use `group.ldap_group_links.create()` and `group.ldap_group_links.delete()`
instead. ([`5c8b7c1`](https://github.com/python-gitlab/python-gitlab/commit/5c8b7c1369a28d75261002e7cb6d804f7d5658c6))

* refactor(projects): remove deprecated `project.transfer_project()` in favor of `project.transfer()`

BREAKING CHANGE: The deprecated `project.transfer_project()` method is no longer available.
Use `project.transfer()` instead. ([`27ed490`](https://github.com/python-gitlab/python-gitlab/commit/27ed490c22008eef383e1a346ad0c721cdcc6198))

* fix(cli): remove deprecated `--all` option in favor of `--get-all`

BREAKING CHANGE: The `--all` option is no longer available in the CLI. Use `--get-all` instead. ([`e9d48cf`](https://github.com/python-gitlab/python-gitlab/commit/e9d48cf69e0dbe93f917e6f593d31327cd99f917))

* feat: remove support for Python 3.7, require 3.8 or higher

Python 3.8 is End-of-Life (EOL) as of 2023-06-27 as stated in
https://devguide.python.org/versions/ and
https://peps.python.org/pep-0537/

By dropping support for Python 3.7 and requiring Python 3.8 or higher
it allows python-gitlab to take advantage of new features in Python
3.8, which are documented at:
https://docs.python.org/3/whatsnew/3.8.html

BREAKING CHANGE: As of python-gitlab 4.0.0, Python 3.7 is no longer
supported. Python 3.8 or higher is required. ([`058d5a5`](https://github.com/python-gitlab/python-gitlab/commit/058d5a56c284c771f1fb5fad67d4ef2eeb4d1916))

### Chore

* chore(ci): follow upstream config for release build_command ([`3e20a76`](https://github.com/python-gitlab/python-gitlab/commit/3e20a76fdfc078a03190939bda303577b2ef8614))

* chore(ci): update release build for python-semantic-release v8 (#2692) ([`bf050d1`](https://github.com/python-gitlab/python-gitlab/commit/bf050d19508978cbaf3e89d49f42162273ac2241))

* chore(deps): update pre-commit hook pycqa/pylint to v3 ([`0f4a346`](https://github.com/python-gitlab/python-gitlab/commit/0f4a34606f4df643a5dbae1900903bcf1d47b740))

* chore(deps): update all non-major dependencies ([`1348a04`](https://github.com/python-gitlab/python-gitlab/commit/1348a040207fc30149c664ac0776e698ceebe7bc))

* chore: add package pipelines API link ([`2a2404f`](https://github.com/python-gitlab/python-gitlab/commit/2a2404fecdff3483a68f538c8cd6ba4d4fc6538c))

* chore(ci): fix pre-commit deps and python version ([`1e7f257`](https://github.com/python-gitlab/python-gitlab/commit/1e7f257e79a7adf1e6f2bc9222fd5031340d26c3))

* chore(ci): remove Python 3.13 dev job ([`e8c50f2`](https://github.com/python-gitlab/python-gitlab/commit/e8c50f28da7e3879f0dc198533041348a14ddc68))

* chore(helpers): fix previously undetected flake8 issue ([`bf8bd73`](https://github.com/python-gitlab/python-gitlab/commit/bf8bd73e847603e8ac5d70606f9393008eee1683))

* chore: fix test names ([`f1654b8`](https://github.com/python-gitlab/python-gitlab/commit/f1654b8065a7c8349777780e673aeb45696fccd0))

* chore: make linters happy ([`3b83d5d`](https://github.com/python-gitlab/python-gitlab/commit/3b83d5d13d136f9a45225929a0c2031dc28cdbed))

* chore: change `_update_uses` to `_update_method` and use an Enum

Change the name of the `_update_uses` attribute to `_update_method`
and store an Enum in the attribute to indicate which type of HTTP
method to use. At the moment it supports `POST` and `PUT`. But can in
the future support `PATCH`. ([`7073a2d`](https://github.com/python-gitlab/python-gitlab/commit/7073a2dfa3a4485d2d3a073d40122adbeff42b5c))

* chore(deps): update all non-major dependencies ([`ff45124`](https://github.com/python-gitlab/python-gitlab/commit/ff45124e657c4ac4ec843a13be534153a8b10a20))

* chore(deps): update dependency pylint to v3 ([`491350c`](https://github.com/python-gitlab/python-gitlab/commit/491350c40a74bbb4945dfb9f2618bcc5420a4603))

* chore(deps): update pre-commit hook maxbrunet/pre-commit-renovate to v37 ([`b4951cd`](https://github.com/python-gitlab/python-gitlab/commit/b4951cd273d599e6d93b251654808c6eded2a960))

* chore(deps): update all non-major dependencies ([`0d49164`](https://github.com/python-gitlab/python-gitlab/commit/0d491648d16f52f5091b23d0e3e5be2794461ade))

* chore(deps): update dependency commitizen to v3.10.0 ([`becd8e2`](https://github.com/python-gitlab/python-gitlab/commit/becd8e20eb66ce4e606f22c15abf734a712c20c3))

* chore(deps): update pre-commit hook commitizen-tools/commitizen to v3.10.0 ([`626c2f8`](https://github.com/python-gitlab/python-gitlab/commit/626c2f8879691e5dd4ce43118668e6a88bf6f7ad))

* chore(deps): update all non-major dependencies ([`6093dbc`](https://github.com/python-gitlab/python-gitlab/commit/6093dbcf07b9edf35379142ea58a190050cf7fe7))

* chore(deps): update all non-major dependencies ([`bb728b1`](https://github.com/python-gitlab/python-gitlab/commit/bb728b1c259dba5699467c9ec7a51b298a9e112e))

* chore(deps): update all non-major dependencies to v23.9.1 ([`a16b732`](https://github.com/python-gitlab/python-gitlab/commit/a16b73297a3372ce4f3ada3b4ea99680dbd511f6))

* chore(deps): update actions/checkout action to v4 ([`af13914`](https://github.com/python-gitlab/python-gitlab/commit/af13914e41f60cc2c4ef167afb8f1a10095e8a00))

* chore(deps): update all non-major dependencies ([`9083787`](https://github.com/python-gitlab/python-gitlab/commit/9083787f0855d94803c633b0491db70f39a9867a))

* chore(deps): update dependency build to v1 ([`2e856f2`](https://github.com/python-gitlab/python-gitlab/commit/2e856f24567784ddc35ca6895d11bcca78b58ca4))

* chore(deps): update all non-major dependencies ([`b6a3db1`](https://github.com/python-gitlab/python-gitlab/commit/b6a3db1a2b465a34842d1a544a5da7eee6430708))

* chore(rtd): use readthedocs v2 syntax ([`6ce2149`](https://github.com/python-gitlab/python-gitlab/commit/6ce214965685a3e73c02e9b93446ad8d9a29262e))

* chore(rtd): fix docs build on readthedocs.io (#2654) ([`3d7139b`](https://github.com/python-gitlab/python-gitlab/commit/3d7139b64853cb0da46d0ef6a4bccc0175f616c2))

* chore(ci): adapt release workflow and config for v8 ([`827fefe`](https://github.com/python-gitlab/python-gitlab/commit/827fefeeb7bf00e5d8fa142d7686ead97ca4b763))

* chore(deps): update relekang/python-semantic-release action to v8 ([`c57c85d`](https://github.com/python-gitlab/python-gitlab/commit/c57c85d0fc6543ab5a2322fc58ec1854afc4f54f))

* chore(deps): update all non-major dependencies ([`16f2d34`](https://github.com/python-gitlab/python-gitlab/commit/16f2d3428e673742a035856b1fb741502287cc1d))

* chore(deps): update all non-major dependencies ([`5b33ade`](https://github.com/python-gitlab/python-gitlab/commit/5b33ade92152e8ccb9db3eb369b003a688447cd6))

* chore(deps): update pre-commit hook maxbrunet/pre-commit-renovate to v36 ([`db58cca`](https://github.com/python-gitlab/python-gitlab/commit/db58cca2e2b7d739b069904cb03f42c9bc1d3810))

* chore(deps): update dependency ubuntu to v22 ([`8865552`](https://github.com/python-gitlab/python-gitlab/commit/88655524ac2053f5b7016457f8c9d06a4b888660))

* chore(deps): update all non-major dependencies ([`3732841`](https://github.com/python-gitlab/python-gitlab/commit/37328416d87f50f64c9bdbdcb49e9b9a96d2d0ef))

* chore(deps): update dependency pytest-docker to v2 ([`b87bb0d`](https://github.com/python-gitlab/python-gitlab/commit/b87bb0db1441d1345048664b15bd8122e6b95be4))

* chore: switch to docker-compose v2

Closes: #2625 ([`713b5ca`](https://github.com/python-gitlab/python-gitlab/commit/713b5ca272f56b0fd7340ca36746e9649a416aa2))

* chore: update PyYAML to 6.0.1

Fixes issue with CI having error:
  `AttributeError: cython_sources`

Closes: #2624 ([`3b8939d`](https://github.com/python-gitlab/python-gitlab/commit/3b8939d7669f391a5a7e36d623f8ad6303ba7712))

* chore(deps): update all non-major dependencies ([`511f45c`](https://github.com/python-gitlab/python-gitlab/commit/511f45cda08d457263f1011b0d2e013e9f83babc))

* chore(deps): update all non-major dependencies ([`d4a7410`](https://github.com/python-gitlab/python-gitlab/commit/d4a7410e55c6a98a15f4d7315cc3d4fde0190bce))

* chore(deps): update all non-major dependencies ([`12846cf`](https://github.com/python-gitlab/python-gitlab/commit/12846cfe4a0763996297bb0a43aa958fe060f029))

* chore(deps): update all non-major dependencies ([`33d2aa2`](https://github.com/python-gitlab/python-gitlab/commit/33d2aa21035515711738ac192d8be51fd6106863))

* chore(deps): update dependency types-setuptools to v68 ([`bdd4eb6`](https://github.com/python-gitlab/python-gitlab/commit/bdd4eb694f8b56d15d33956cb982a71277ca907f))

* chore(deps): update actions/upload-artifact action to v3 ([`b78d6bf`](https://github.com/python-gitlab/python-gitlab/commit/b78d6bfd18630fa038f5f5bd8e473ec980495b10))

* chore(deps): update dependency setuptools to v68 ([`0f06082`](https://github.com/python-gitlab/python-gitlab/commit/0f06082272f7dbcfd79f895de014cafed3205ff6))

* chore(deps): bring myst-parser up to date with sphinx 7 ([`da03e9c`](https://github.com/python-gitlab/python-gitlab/commit/da03e9c7dc1c51978e51fedfc693f0bce61ddaf1))

* chore(deps): bring furo up to date with sphinx ([`a15c927`](https://github.com/python-gitlab/python-gitlab/commit/a15c92736f0cf78daf78f77fb318acc6c19036a0))

* chore(deps): update dependency sphinx to v7 ([`2918dfd`](https://github.com/python-gitlab/python-gitlab/commit/2918dfd78f562e956c5c53b79f437a381e51ebb7))

* chore(deps): update actions/checkout action to v3 ([`e2af1e8`](https://github.com/python-gitlab/python-gitlab/commit/e2af1e8a964fe8603dddef90a6df62155f25510d))

* chore(deps): update actions/setup-python action to v4 ([`e0d6783`](https://github.com/python-gitlab/python-gitlab/commit/e0d6783026784bf1e6590136da3b35051e7edbb3))

* chore(deps): update all non-major dependencies ([`5ff56d8`](https://github.com/python-gitlab/python-gitlab/commit/5ff56d866c6fdac524507628cf8baf2c498347af))

* chore(deps): pin pytest-console-scripts for 3.7 ([`6d06630`](https://github.com/python-gitlab/python-gitlab/commit/6d06630cac1a601bc9a17704f55dcdc228285e88))

* chore(deps): update all non-major dependencies ([`7586a5c`](https://github.com/python-gitlab/python-gitlab/commit/7586a5c80847caf19b16282feb25be470815729b))

### Documentation

* docs: correct error with back-ticks (#2653)

New linting package update detected the issue. ([`0b98dd3`](https://github.com/python-gitlab/python-gitlab/commit/0b98dd3e92179652806a7ae8ccc7ec5cddd2b260))

* docs(access_token): adopt token docs to 16.1

expires_at is now required
Upstream MR: https://gitlab.com/gitlab-org/gitlab/-/merge_requests/124964 ([`fe7a971`](https://github.com/python-gitlab/python-gitlab/commit/fe7a971ad3ea1e66ffc778936296e53825c69f8f))

* docs(files): fix minor typo in variable declaration ([`118ce42`](https://github.com/python-gitlab/python-gitlab/commit/118ce4282abc4397c4e9370407b1ab6866de9f97))

### Feature

* feat(client): mask tokens by default when logging ([`1611d78`](https://github.com/python-gitlab/python-gitlab/commit/1611d78263284508326347843f634d2ca8b41215))

* feat(api): add ProjectPackagePipeline

Add ProjectPackagePipeline, which is scheduled to be included in GitLab
16.0 ([`5b4addd`](https://github.com/python-gitlab/python-gitlab/commit/5b4addda59597a5f363974e59e5ea8463a0806ae))

* feat: officially support Python 3.12 ([`2a69c0e`](https://github.com/python-gitlab/python-gitlab/commit/2a69c0ee0a86315a3ed4750f59bd6ab3e4199b8e))

* feat(packages): Allow uploading bytes and files

This commit adds a keyword argument to GenericPackageManager.upload() to
allow uploading bytes and file-like objects to the generic package
registry. That necessitates changing file path to be a keyword argument
as well, which then cascades into a whole slew of checks to not allow
passing both and to not allow uploading file-like objects as JSON data.

Closes https://github.com/python-gitlab/python-gitlab/issues/1815 ([`61e0fae`](https://github.com/python-gitlab/python-gitlab/commit/61e0faec2014919e0a2e79106089f6838be8ad0e))

* feat: Use requests AuthBase classes ([`5f46cfd`](https://github.com/python-gitlab/python-gitlab/commit/5f46cfd235dbbcf80678e45ad39a2c3b32ca2e39))

* feat(api): add support for job token scope settings ([`59d6a88`](https://github.com/python-gitlab/python-gitlab/commit/59d6a880aacd7cf6f443227071bb8288efb958c4))

* feat(api): support project remote mirror deletion ([`d900910`](https://github.com/python-gitlab/python-gitlab/commit/d9009100ec762c307b46372243d93f9bc2de7a2b))

* feat(api): add optional GET attrs for /projects/:id/ci/lint ([`40a102d`](https://github.com/python-gitlab/python-gitlab/commit/40a102d4f5c8ff89fae56cd9b7c8030c5070112c))

* feat(api): add support for new runner creation API (#2635)

Co-authored-by: Nejc Habjan &lt;hab.nejc@gmail.com&gt; ([`4abcd17`](https://github.com/python-gitlab/python-gitlab/commit/4abcd1719066edf9ecc249f2da4a16c809d7b181))

* feat(releases): Add support for direct_asset_path

This commit adds support for the “new” alias for `filepath`:
`direct_asset_path` (added in 15.10) in release links API. ([`d054917`](https://github.com/python-gitlab/python-gitlab/commit/d054917ccb3bbcc9973914409b9e34ba9301663a))

* feat: Added iteration to issue and group filters ([`8d2d297`](https://github.com/python-gitlab/python-gitlab/commit/8d2d2971c3909fb5461a9f7b2d07508866cd456c))

### Fix

* fix(cli): add _from_parent_attrs to user-project manager (#2558) ([`016d90c`](https://github.com/python-gitlab/python-gitlab/commit/016d90c3c22bfe6fc4e866d120d2c849764ef9d2))

* fix(cli): fix action display in --help when there are few actions

fixes #2656 ([`b22d662`](https://github.com/python-gitlab/python-gitlab/commit/b22d662a4fd8fb8a9726760b645d4da6197bfa9a))

* fix(client): support empty 204 responses in http_patch ([`e15349c`](https://github.com/python-gitlab/python-gitlab/commit/e15349c9a796f2d82f72efbca289740016c47716))

* fix(snippets): allow passing list of files ([`31c3c5e`](https://github.com/python-gitlab/python-gitlab/commit/31c3c5ea7cbafb4479825ec40bc34e3b8cb427fd))

### Test

* test: add tests for token masking ([`163bfcf`](https://github.com/python-gitlab/python-gitlab/commit/163bfcf6c2c1ccc4710c91e6f75b51e630dfb719))

* test(cli): add test for user-project list ([`a788cff`](https://github.com/python-gitlab/python-gitlab/commit/a788cff7c1c651c512f15a9a1045c1e4d449d854))

* test: correct calls to `script_runner.run()`

Warnings were being raised. Resolve those warnings. ([`cd04315`](https://github.com/python-gitlab/python-gitlab/commit/cd04315de86aca2bb471865b2754bb66e96f0119))

* test: fix failing tests that use 204 (No Content) plus content

urllib3&gt;=2 now checks for expected content length. Also codes 204 and
304 are set to expect a content length of 0 [1]

So in the unit tests stop setting content to return in these
situations.

[1] https://github.com/urllib3/urllib3/blob/88a707290b655394aade060a8b7eaee83152dc8b/src/urllib3/response.py#L691-L693 ([`3074f52`](https://github.com/python-gitlab/python-gitlab/commit/3074f522551b016451aa968f22a3dc5715db281b))

### Unknown

*  chore(deps): update dependency requests to v2.31.0 [security]

Also update dependency `responses==0.23.3` as it provides support for
`urllib3&gt;=2`

Closes: #2626 ([`988a6e7`](https://github.com/python-gitlab/python-gitlab/commit/988a6e7eff5d24b2432d3d85f1e750f4f95563f7))

## v3.15.0 (2023-06-09)

### Chore

* chore(deps): update pre-commit hook maxbrunet/pre-commit-renovate to v35 ([`8202e3f`](https://github.com/python-gitlab/python-gitlab/commit/8202e3fe01b34da3ff29a7f4189d80a2153f08a4))

* chore: update sphinx from 5.3.0 to 6.2.1 ([`c44a290`](https://github.com/python-gitlab/python-gitlab/commit/c44a29016b13e535621e71ec4f5392b4c9a93552))

* chore: update copyright year to include 2023 ([`511c6e5`](https://github.com/python-gitlab/python-gitlab/commit/511c6e507e4161531732ce4c323aeb4481504b08))

* chore(deps): update all non-major dependencies ([`e3de6ba`](https://github.com/python-gitlab/python-gitlab/commit/e3de6bac98edd8a4cb87229e639212b9fb1500f9))

* chore(deps): update pre-commit hook commitizen-tools/commitizen to v3 ([`1591e33`](https://github.com/python-gitlab/python-gitlab/commit/1591e33f0b315c7eb544dc98a6567c33c2ac143f))

* chore(deps): update dependency types-setuptools to v67 ([`c562424`](https://github.com/python-gitlab/python-gitlab/commit/c56242413e0eb36e41981f577162be8b69e53b67))

* chore(deps): update dependency requests-toolbelt to v1 ([`86eba06`](https://github.com/python-gitlab/python-gitlab/commit/86eba06736b7610d8c4e77cd96ae6071c40067d5))

* chore(deps): update dependency myst-parser to v1 ([`9c39848`](https://github.com/python-gitlab/python-gitlab/commit/9c3984896c243ad082469ae69342e09d65b5b5ef))

* chore(deps): update dependency commitizen to v3 ([`784d59e`](https://github.com/python-gitlab/python-gitlab/commit/784d59ef46703c9afc0b1e390f8c4194ee10bb0a))

* chore(ci): use OIDC trusted publishing for pypi.org (#2559)

* chore(ci): use OIDC trusted publishing for pypi.org

* chore(ci): explicitly install setuptools in tests ([`7be09e5`](https://github.com/python-gitlab/python-gitlab/commit/7be09e52d75ed8ab723d7a65f5e99d98fe6f52b0))

### Documentation

* docs: remove exclusive EE about issue links ([`e0f6f18`](https://github.com/python-gitlab/python-gitlab/commit/e0f6f18f14c8c17ea038a7741063853c105e7fa3))

### Feature

* feat: add support for `select=&#34;package_file&#34;` in package upload

Add ability to use `select=&#34;package_file&#34;` when uploading a generic
package as described in:
https://docs.gitlab.com/ee/user/packages/generic_packages/index.html

Closes: #2557 ([`3a49f09`](https://github.com/python-gitlab/python-gitlab/commit/3a49f099d54000089e217b61ffcf60b6a28b4420))

* feat(api): add support for events scope parameter ([`348f56e`](https://github.com/python-gitlab/python-gitlab/commit/348f56e8b95c43a7f140f015d303131665b21772))

* feat: usernames support for MR approvals

This can be used instead of &#39;user_ids&#39;

See: https://docs.gitlab.com/ee/api/merge_request_approvals.html#create-project-level-rule ([`a2b8c8c`](https://github.com/python-gitlab/python-gitlab/commit/a2b8c8ccfb5d4fa4d134300861a3bfb0b10246ca))

## v3.14.0 (2023-04-11)

### Chore

* chore(ci): wait for all coverage reports in CI status ([`511764d`](https://github.com/python-gitlab/python-gitlab/commit/511764d2fc4e524eff0d7cf0987d451968e817d3))

* chore(setup): depend on typing-extensions for 3.7 until EOL ([`3abc557`](https://github.com/python-gitlab/python-gitlab/commit/3abc55727d4d52307b9ce646fee172f94f7baf8d))

* chore: add Contributor Covenant 2.1 as Code of Conduct

See https://www.contributor-covenant.org/version/2/1/code_of_conduct/ ([`fe334c9`](https://github.com/python-gitlab/python-gitlab/commit/fe334c91fcb6450f5b3b424c925bf48ec2a3c150))

* chore(deps): update all non-major dependencies ([`8b692e8`](https://github.com/python-gitlab/python-gitlab/commit/8b692e825d95cd338e305196d9ca4e6d87173a84))

* chore(deps): update dependency furo to v2023 ([`7a1545d`](https://github.com/python-gitlab/python-gitlab/commit/7a1545d52ed0ac8e2e42a2f260e8827181e94d88))

* chore(deps): update actions/stale action to v8 ([`7ac4b86`](https://github.com/python-gitlab/python-gitlab/commit/7ac4b86fe3d24c3347a1c44bd3db561d62a7bd3f))

* chore(pre-commit): Bumping versions ([`e973729`](https://github.com/python-gitlab/python-gitlab/commit/e973729e007f664aa4fde873654ef68c21be03c8))

* chore(.github): actually make PR template the default ([`7a8a862`](https://github.com/python-gitlab/python-gitlab/commit/7a8a86278543a1419d07dd022196e4cb3db12d31))

* chore: use a dataclass to return values from `prepare_send_data`

I found the tuple of three values confusing. So instead use a
dataclass to return the three values. It is still confusing but a
little bit less so.

Also add some unit tests ([`f2b5e4f`](https://github.com/python-gitlab/python-gitlab/commit/f2b5e4fa375e88d6102a8d023ae2fe8206042545))

* chore(contributing): refresh development docs ([`d387d91`](https://github.com/python-gitlab/python-gitlab/commit/d387d91401fdf933b1832ea2593614ea6b7d8acf))

* chore(github): add default pull request template ([`bf46c67`](https://github.com/python-gitlab/python-gitlab/commit/bf46c67db150f0657b791d94e6699321c9985f57))

* chore(deps): update all non-major dependencies (#2493)

* chore(deps): update all non-major dependencies
* chore(fixtures): downgrade GitLab for now
* chore(deps): ungroup typing deps, group gitlab instead
* chore(deps): downgrade argcomplete for now

---------

Co-authored-by: renovate[bot] &lt;29139614+renovate[bot]@users.noreply.github.com&gt;
Co-authored-by: Nejc Habjan &lt;nejc.habjan@siemens.com&gt; ([`07d03dc`](https://github.com/python-gitlab/python-gitlab/commit/07d03dc959128e05d21e8dfd79aa8e916ab5b150))

* chore(deps): update dependency pre-commit to v3 (#2508)

Co-authored-by: renovate[bot] &lt;29139614+renovate[bot]@users.noreply.github.com&gt; ([`7d779c8`](https://github.com/python-gitlab/python-gitlab/commit/7d779c85ffe09623c5d885b5a429b0242ad82f93))

* chore(deps): update dependency coverage to v7 (#2501)

Co-authored-by: renovate[bot] &lt;29139614+renovate[bot]@users.noreply.github.com&gt; ([`aee73d0`](https://github.com/python-gitlab/python-gitlab/commit/aee73d05c8c9bd94fb7f01dfefd1bb6ad19c4eb2))

* chore(deps): update dependency flake8 to v6 (#2502)

Co-authored-by: renovate[bot] &lt;29139614+renovate[bot]@users.noreply.github.com&gt; ([`3d4596e`](https://github.com/python-gitlab/python-gitlab/commit/3d4596e8cdebbc0ea214d63556b09eac40d42a9c))

* chore(renovate): swith to gitlab-ee ([`8da48ee`](https://github.com/python-gitlab/python-gitlab/commit/8da48ee0f32c293b4788ebd0ddb24018401ef7ad))

* chore(renovate): bring back custom requirements pattern ([`ae0b21c`](https://github.com/python-gitlab/python-gitlab/commit/ae0b21c1c2b74bf012e099ae1ff35ce3f40c6480))

* chore(deps): update mypy (1.0.0) and responses (0.22.0)

Update the `requirements-*` files.

In order to update mypy==1.0.0 we need to also update
responses==0.22.0

Fix one issue found by `mypy`

Leaving updates for `precommit` to be done in a separate commit by
someone. ([`9c24657`](https://github.com/python-gitlab/python-gitlab/commit/9c2465759386b60a478bd8f43e967182ed97d39d))

* chore(renovate): do not ignore tests dir ([`5b8744e`](https://github.com/python-gitlab/python-gitlab/commit/5b8744e9c2241e0fdcdef03184afcb48effea90f))

* chore(deps): update all non-major dependencies ([`2f06999`](https://github.com/python-gitlab/python-gitlab/commit/2f069999c5dfd637f17d1ded300ea7628c0566c3))

* chore(deps): update pre-commit hook psf/black to v23 ([`217a787`](https://github.com/python-gitlab/python-gitlab/commit/217a78780c3ae6e41fb9d76d4d841c5d576de45f))

* chore(deps): update black (23.1.0) and commitizen (2.40.0) (#2479)

Update the dependency versions:
  black: 23.1.0
  commitizen: 2.40.0

They needed to be updated together as just updating `black` caused a
dependency conflict.

Updated files by running `black` and committing the changes. ([`44786ef`](https://github.com/python-gitlab/python-gitlab/commit/44786efad1dbb66c8242e61cf0830d58dfaff196))

* chore: add SECURITY.md ([`572ca3b`](https://github.com/python-gitlab/python-gitlab/commit/572ca3b6bfe190f8681eef24e72b15c1f8ba6da8))

* chore: remove `pre-commit` as a default `tox` environment (#2470)

For users who use `tox` having `pre-commit` as part of the default
environment list is redundant as it will run the same tests again that
are being run in other environments. For example: black, flake8,
pylint, and more. ([`fde2495`](https://github.com/python-gitlab/python-gitlab/commit/fde2495dd1e97fd2f0e91063946bb08490b3952c))

* chore: add Python 3.12 testing

Add a unit test for Python 3.12. This will use the latest version of
Python 3.12 that is available from
https://github.com/actions/python-versions/

At this time it is 3.12.0-alpha.4 but will move forward over time
until the final 3.12 release and updates. So 3.12.0, 3.12.1, ... will
be matched. ([`0867564`](https://github.com/python-gitlab/python-gitlab/commit/08675643e6b306d3ae101b173609a6c363c9f3df))

### Documentation

* docs(objects): fix typo in pipeline schedules ([`3057f45`](https://github.com/python-gitlab/python-gitlab/commit/3057f459765d1482986f2086beb9227acc7fd15f))

* docs(advanced): clarify netrc, proxy behavior with requests ([`1da7c53`](https://github.com/python-gitlab/python-gitlab/commit/1da7c53fd3476a1ce94025bb15265f674af40e1a))

* docs: fix update badge behaviour

docs: fix update badge behaviour

Earlier:
badge.image_link = new_link

Now:
badge.image_url = new_image_url
badge.link_url = new_link_url ([`3d7ca1c`](https://github.com/python-gitlab/python-gitlab/commit/3d7ca1caac5803c2e6d60a3e5eba677957b3cfc6))

* docs(advanced): fix typo in Gitlab examples ([`1992790`](https://github.com/python-gitlab/python-gitlab/commit/19927906809c329788822f91d0abd8761a85c5c3))

### Feature

* feat(projects): allow importing additional items from GitHub ([`ce84f2e`](https://github.com/python-gitlab/python-gitlab/commit/ce84f2e64a640e0d025a7ba3a436f347ad25e88e))

* feat(objects): support fetching PATs via id or `self` endpoint ([`19b38bd`](https://github.com/python-gitlab/python-gitlab/commit/19b38bd481c334985848be204eafc3f1ea9fe8a6))

* feat: add resource_weight_event for ProjectIssue ([`6e5ef55`](https://github.com/python-gitlab/python-gitlab/commit/6e5ef55747ddeabe6d212aec50d66442054c2352))

* feat(backends): use PEP544 protocols for structural subtyping (#2442)

The purpose of this change is to track API changes described in
https://github.com/python-gitlab/python-gitlab/blob/main/docs/api-levels.rst,
for example, for package versioning and breaking change announcements
in case of protocol changes.

This is MVP implementation to be used by #2435. ([`4afeaff`](https://github.com/python-gitlab/python-gitlab/commit/4afeaff0361a966254a7fbf0120e93583d460361))

* feat(client): add http_patch method (#2471)

In order to support some new API calls we need to support the HTTP `PATCH` method.

Closes: #2469 ([`f711d9e`](https://github.com/python-gitlab/python-gitlab/commit/f711d9e2bf78f58cee6a7c5893d4acfd2f980397))

* feat(cli): add setting of `allow_force_push` for protected branch

For the CLI: add `allow_force_push` as an optional argument for
creating a protected branch.

API reference:
https://docs.gitlab.com/ee/api/protected_branches.html#protect-repository-branches

Closes: #2466 ([`929e07d`](https://github.com/python-gitlab/python-gitlab/commit/929e07d94d9a000e6470f530bfde20bb9c0f2637))

### Fix

* fix(cli): warn user when no fields are displayed ([`8bf53c8`](https://github.com/python-gitlab/python-gitlab/commit/8bf53c8b31704bdb31ffc5cf107cc5fba5dad457))

* fix(client): properly parse content-type when charset is present ([`76063c3`](https://github.com/python-gitlab/python-gitlab/commit/76063c386ef9caf84ba866515cb053f6129714d9))

* fix: support int for `parent_id` in `import_group`

This will also fix other use cases where an integer is passed in to
MultipartEncoder.

Added unit tests to show it works.

Closes: #2506 ([`90f96ac`](https://github.com/python-gitlab/python-gitlab/commit/90f96acf9e649de9874cec612fc1b49c4a843447))

* fix(cli): add ability to escape at-prefixed parameter (#2513)

* fix(cli): Add ability to escape at-prefixed parameter (#2511)

---------

Co-authored-by: Nejc Habjan &lt;hab.nejc@gmail.com&gt; ([`4f7c784`](https://github.com/python-gitlab/python-gitlab/commit/4f7c78436e62bfd21745c5289117e03ed896bc66))

* fix(cli): display items when iterator is returned ([`33a04e7`](https://github.com/python-gitlab/python-gitlab/commit/33a04e74fc42d720c7be32172133a614f7268ec1))

### Refactor

* refactor(client): let mypy know http_password is set ([`2dd177b`](https://github.com/python-gitlab/python-gitlab/commit/2dd177bf83fdf62f0e9bdcb3bc41d5e4f5631504))

### Test

* test(unit): increase V4 CLI coverage ([`5748d37`](https://github.com/python-gitlab/python-gitlab/commit/5748d37365fdac105341f94eaccde8784d6f57e3))

* test(unit): split the last remaining unittest-based classes into modules&#34; ([`14e0f65`](https://github.com/python-gitlab/python-gitlab/commit/14e0f65a3ff05563df4977d792272f8444bf4312))

* test(unit): remove redundant package ([`4a9e3ee`](https://github.com/python-gitlab/python-gitlab/commit/4a9e3ee70f784f99f373f2fddde0155649ebe859))

* test(unit): consistently use inline fixtures ([`1bc56d1`](https://github.com/python-gitlab/python-gitlab/commit/1bc56d164a7692cf3aaeedfa1ed2fb869796df03))

* test(meta): move meta suite into unit tests

They&#39;re always run with it anyway, so it makes no difference. ([`847004b`](https://github.com/python-gitlab/python-gitlab/commit/847004be021b4a514e41bf28afb9d87e8643ddba))

* test(functional): clarify MR fixture factory name ([`d8fd1a8`](https://github.com/python-gitlab/python-gitlab/commit/d8fd1a83b588f4e5e61ca46a28f4935220c5b8c4))

### Unknown

* Merge pull request #2465 from valentingregoire/typos

docs: fix typo in issue docs ([`43f5ac5`](https://github.com/python-gitlab/python-gitlab/commit/43f5ac5b12b9d17292b65e3d1322f0211c31780d))

* Merge branch &#39;main&#39; into typos ([`3cfd390`](https://github.com/python-gitlab/python-gitlab/commit/3cfd3903757bf61386972a18f3225665145324eb))

## v3.13.0 (2023-01-30)

### Chore

* chore: make backends private ([`1e629af`](https://github.com/python-gitlab/python-gitlab/commit/1e629af73e312fea39522334869c3a9b7e6085b9))

* chore(deps): update all non-major dependencies ([`ea7010b`](https://github.com/python-gitlab/python-gitlab/commit/ea7010b17cc2c29c2a5adeaf81f2d0064523aa39))

* chore: add a UserWarning if both `iterator=True` and `page=X` are used (#2462)

If a caller calls a `list()` method with both `iterator=True` (or
`as_list=False`) and `page=X` then emit a `UserWarning` as the options
are mutually exclusive. ([`8e85791`](https://github.com/python-gitlab/python-gitlab/commit/8e85791c315822cd26d56c0c0f329cffae879644))

* chore: remove tox `envdir` values

tox &gt; 4 no longer will re-use the tox directory :(  What this means is
that with the previous config if you ran:
    $ tox -e mypy; tox -e isort; tox -e mypy
It would recreate the tox environment each time :(

By removing the `envdir` values it will have the tox environments in
separate directories and not recreate them.

The have an FAQ entry about this:
https://tox.wiki/en/latest/upgrading.html#re-use-of-environments ([`3c7c7fc`](https://github.com/python-gitlab/python-gitlab/commit/3c7c7fc9d2375d3219fb078e18277d7476bae5e0))

* chore: update attributes for create and update projects ([`aa44f2a`](https://github.com/python-gitlab/python-gitlab/commit/aa44f2aed8150f8c891837e06296c7bbef17c292))

* chore(deps): update all non-major dependencies ([`122988c`](https://github.com/python-gitlab/python-gitlab/commit/122988ceb329d7162567cb4a325f005ea2013ef2))

* chore(deps): update all non-major dependencies ([`49c0233`](https://github.com/python-gitlab/python-gitlab/commit/49c023387970abea7688477c8ef3ff3a1b31b0bc))

* chore(deps): update all non-major dependencies ([`10c4f31`](https://github.com/python-gitlab/python-gitlab/commit/10c4f31ad1480647a6727380db68f67a4c645af9))

* chore(deps): update all non-major dependencies ([`bbd01e8`](https://github.com/python-gitlab/python-gitlab/commit/bbd01e80326ea9829b2f0278fedcb4464be64389))

* chore(deps): update actions/stale action to v7 ([`76eb024`](https://github.com/python-gitlab/python-gitlab/commit/76eb02439c0ae0f7837e3408948840c800fd93a7))

* chore(ci): complete all unit tests even if one has failed (#2438) ([`069c6c3`](https://github.com/python-gitlab/python-gitlab/commit/069c6c30ff989f89356898b72835b4f4a792305c))

* chore: add test, docs, and helper for 409 retries ([`3e1c625`](https://github.com/python-gitlab/python-gitlab/commit/3e1c625133074ccd2fb88c429ea151bfda96aebb))

* chore(deps): update all non-major dependencies ([`6682808`](https://github.com/python-gitlab/python-gitlab/commit/6682808034657b73c4b72612aeb009527c25bfa2))

* chore(deps): update all non-major dependencies ([`1816107`](https://github.com/python-gitlab/python-gitlab/commit/1816107b8d87614e7947837778978d8de8da450f))

* chore(deps): update pre-commit hook pycqa/flake8 to v6 ([`82c61e1`](https://github.com/python-gitlab/python-gitlab/commit/82c61e1d2c3a8102c320558f46e423b09c6957aa))

* chore: add docs for schedule pipelines ([`9a9a6a9`](https://github.com/python-gitlab/python-gitlab/commit/9a9a6a98007df2992286a721507b02c48800bfed))

* chore(tox): ensure test envs have all dependencies ([`63cf4e4`](https://github.com/python-gitlab/python-gitlab/commit/63cf4e4fa81d6c5bf6cf74284321bc3ce19bab62))

* chore(deps): update pre-commit hook maxbrunet/pre-commit-renovate to v34.48.4 ([`985b971`](https://github.com/python-gitlab/python-gitlab/commit/985b971cf6d69692379805622a1bb1ff29ae308d))

* chore(deps): update dessant/lock-threads action to v4 ([`337b25c`](https://github.com/python-gitlab/python-gitlab/commit/337b25c6fc1f40110ef7a620df63ff56a45579f1))

* chore: Use SPDX license expression in project metadata ([`acb3a4a`](https://github.com/python-gitlab/python-gitlab/commit/acb3a4ad1fa23c21b1d7f50e95913136beb61402))

* chore(deps): update actions/download-artifact action to v3 ([`64ca597`](https://github.com/python-gitlab/python-gitlab/commit/64ca5972468ab3b7e3a01e88ab9bb8e8bb9a3de1))

* chore(deps): update all non-major dependencies ([`21e767d`](https://github.com/python-gitlab/python-gitlab/commit/21e767d8719372daadcea446f835f970210a6b6b))

### Documentation

* docs(faq): describe and group common errors ([`4c9a072`](https://github.com/python-gitlab/python-gitlab/commit/4c9a072b053f12f8098e4ea6fc47e3f6ab4f8b07))

### Feature

* feat(group): add support for group restore API ([`9322db6`](https://github.com/python-gitlab/python-gitlab/commit/9322db663ecdaecf399e3192810d973c6a9a4020))

* feat(client): automatically retry on HTTP 409 Resource lock

Fixes: #2325 ([`dced76a`](https://github.com/python-gitlab/python-gitlab/commit/dced76a9900c626c9f0b90b85a5e371101a24fb4))

* feat(api): add support for bulk imports API ([`043de2d`](https://github.com/python-gitlab/python-gitlab/commit/043de2d265e0e5114d1cd901f82869c003413d9b))

* feat(api): add support for resource groups ([`5f8b8f5`](https://github.com/python-gitlab/python-gitlab/commit/5f8b8f5be901e944dfab2257f9e0cc4b2b1d2cd5))

* feat(api): support listing pipelines triggered by pipeline schedules ([`865fa41`](https://github.com/python-gitlab/python-gitlab/commit/865fa417a20163b526596549b9afbce679fc2817))

* feat: allow filtering pipelines by source

See:
https://docs.gitlab.com/ee/api/pipelines.html#list-project-pipelines
Added in GitLab 14.3 ([`b6c0872`](https://github.com/python-gitlab/python-gitlab/commit/b6c08725042380d20ef5f09979bc29f2f6c1ab6f))

* feat(client): bootstrap the http backends concept (#2391) ([`91a665f`](https://github.com/python-gitlab/python-gitlab/commit/91a665f331c3ffc260db3470ad71fde0d3b56aa2))

* feat: add resource iteration events (see https://docs.gitlab.com/ee/api/resource_iteration_events.html) ([`ef5feb4`](https://github.com/python-gitlab/python-gitlab/commit/ef5feb4d07951230452a2974da729a958bdb9d6a))

* feat: allow passing kwargs to Gitlab class when instantiating with `from_config` (#2392) ([`e88d34e`](https://github.com/python-gitlab/python-gitlab/commit/e88d34e38dd930b00d7bb48f0e1c39420e09fa0f))

* feat: add keep_base_url when getting configuration from file ([`50a0301`](https://github.com/python-gitlab/python-gitlab/commit/50a03017f2ba8ec3252911dd1cf0ed7df42cfe50))

### Fix

* fix(client): regression - do not automatically get_next if page=# and
iterator=True/as_list=False are used

This fix a regression introduced on commit
https://github.com/python-gitlab/python-gitlab/commit/1339d645ce58a2e1198b898b9549ba5917b1ff12

If page is used, then get_next should be false.

This was found on the mesa ci project, after upgrading the python-gitlab
version, the script that monitors the ci was getting killed by consuming
too much memory. ([`585e3a8`](https://github.com/python-gitlab/python-gitlab/commit/585e3a86c4cafa9ee73ed38676a78f3c34dbe6b2))

* fix: change return value to &#34;None&#34; in case getattr returns None to prevent error ([`3f86d36`](https://github.com/python-gitlab/python-gitlab/commit/3f86d36218d80b293b346b37f8be5efa6455d10c))

* fix(deps): bump requests-toolbelt to fix deprecation warning ([`faf842e`](https://github.com/python-gitlab/python-gitlab/commit/faf842e97d4858ff5ebd8ae6996e0cb3ca29881c))

* fix: typo fixed in docs ([`ee5f444`](https://github.com/python-gitlab/python-gitlab/commit/ee5f444b16e4d2f645499ac06f5d81f22867f050))

* fix: Use the ProjectIterationManager within the Project object

The Project object was previously using the GroupIterationManager
resulting in the incorrect API endpoint being used. Utilize the correct
ProjectIterationManager instead.

Resolves #2403 ([`44f05dc`](https://github.com/python-gitlab/python-gitlab/commit/44f05dc017c5496e14db82d9650c6a0110b95cf9))

* fix(api): Make description optional for releases ([`5579750`](https://github.com/python-gitlab/python-gitlab/commit/5579750335245011a3acb9456cb488f0fa1cda61))

### Refactor

* refactor: add reason property to RequestsResponse (#2439) ([`b59b7bd`](https://github.com/python-gitlab/python-gitlab/commit/b59b7bdb221ac924b5be4227ef7201d79b40c98f))

* refactor: remove unneeded requests.utils import (#2426) ([`6fca651`](https://github.com/python-gitlab/python-gitlab/commit/6fca6512a32e9e289f988900e1157dfe788f54be))

* refactor: Migrate MultipartEncoder to RequestsBackend (#2421) ([`43b369f`](https://github.com/python-gitlab/python-gitlab/commit/43b369f28cb9009e02bc23e772383d9ea1ded46b))

* refactor: move Response object to backends (#2420) ([`7d9ce0d`](https://github.com/python-gitlab/python-gitlab/commit/7d9ce0dfb9f5a71aaa7f9c78d815d7c7cbd21c1c))

* refactor: move the request call to the backend (#2413) ([`283e7cc`](https://github.com/python-gitlab/python-gitlab/commit/283e7cc04ce61aa456be790a503ed64089a2c2b6))

* refactor: Moving RETRYABLE_TRANSIENT_ERROR_CODES to const ([`887852d`](https://github.com/python-gitlab/python-gitlab/commit/887852d7ef02bed6dff5204ace73d8e43a66e32f))

### Test

* test(functional): do not require config file ([`43c2dda`](https://github.com/python-gitlab/python-gitlab/commit/43c2dda7aa8b167a451b966213e83d88d1baa1df))

* test(unit): expand tests for pipeline schedules ([`c7cf0d1`](https://github.com/python-gitlab/python-gitlab/commit/c7cf0d1f172c214a11b30622fbccef57d9c86e93))

## v3.12.0 (2022-11-28)

### Chore

* chore: validate httpx package is not installed by default ([`0ecf3bb`](https://github.com/python-gitlab/python-gitlab/commit/0ecf3bbe28c92fd26a7d132bf7f5ae9481cbad30))

* chore(deps): update all non-major dependencies ([`d8a657b`](https://github.com/python-gitlab/python-gitlab/commit/d8a657b2b391e9ba3c20d46af6ad342a9b9a2f93))

* chore(deps): update pre-commit hook maxbrunet/pre-commit-renovate to v34.24.0 ([`a0553c2`](https://github.com/python-gitlab/python-gitlab/commit/a0553c29899f091209afe6366e8fb75fb9edef40))

* chore: correct website for pylint

Use https://github.com/PyCQA/pylint as the website for pylint. ([`fcd72fe`](https://github.com/python-gitlab/python-gitlab/commit/fcd72fe243daa0623abfde267c7ab1c6866bcd52))

* chore(deps): update pre-commit hook maxbrunet/pre-commit-renovate to v34.20.0 ([`e6f1bd6`](https://github.com/python-gitlab/python-gitlab/commit/e6f1bd6333a884433f808b2a84670079f9a70f0a))

* chore(deps): update all non-major dependencies ([`b2c6d77`](https://github.com/python-gitlab/python-gitlab/commit/b2c6d774b3f8fa72c5607bfa4fa0918283bbdb82))

* chore(deps): update pre-commit hook maxbrunet/pre-commit-renovate to v34 ([`623e768`](https://github.com/python-gitlab/python-gitlab/commit/623e76811a16f0a8ae58dbbcebfefcfbef97c8d1))

### Documentation

* docs: Use the term &#34;log file&#34; for getting a job log file

The GitLab docs refer to it as a log file:
https://docs.gitlab.com/ee/api/jobs.html#get-a-log-file

&#34;trace&#34; is the endpoint name but not a common term people will think
of for a &#34;log file&#34; ([`9d2b1ad`](https://github.com/python-gitlab/python-gitlab/commit/9d2b1ad10aaa78a5c28ece334293641c606291b5))

* docs(groups): describe GitLab.com group creation limitation ([`9bd433a`](https://github.com/python-gitlab/python-gitlab/commit/9bd433a3eb508b53fbca59f3f445da193522646a))

* docs(api): pushrules remove saying `None` is returned when not found

In `groups.pushrules.get()`, GitLab does not return `None` when no
rules are found. GitLab returns a 404.

Update docs to not say it will return `None`

Also update docs in `project.pushrules.get()` to be consistent. Not
100% sure if it returns `None` or returns a 404, but we don&#39;t need to
document that.

Closes: #2368 ([`c3600b4`](https://github.com/python-gitlab/python-gitlab/commit/c3600b49e4d41b1c4f2748dd6f2a331c331d8706))

### Feature

* feat: add support for SAML group links (#2367) ([`1020ce9`](https://github.com/python-gitlab/python-gitlab/commit/1020ce965ff0cd3bfc283d4f0ad40e41e4d1bcee))

* feat(groups): add LDAP link manager and deprecate old API endpoints ([`3a61f60`](https://github.com/python-gitlab/python-gitlab/commit/3a61f601adaec7751cdcfbbcb88aa544326b1730))

* feat(groups): add support for listing ldap_group_links (#2371) ([`ad7c8fa`](https://github.com/python-gitlab/python-gitlab/commit/ad7c8fafd56866002aa6723ceeba4c4bc071ca0d))

* feat: implement secure files API ([`d0a0348`](https://github.com/python-gitlab/python-gitlab/commit/d0a034878fabfd8409134aa8b7ffeeb40219683c))

* feat(ci): Re-Run Tests on PR Comment workflow ([`034cde3`](https://github.com/python-gitlab/python-gitlab/commit/034cde31c7017923923be29c3f34783937febc0f))

* feat(api): add support for getting a project&#39;s pull mirror details

Add the ability to get a project&#39;s pull mirror details. This was added
in GitLab 15.5 and is a PREMIUM feature.

https://docs.gitlab.com/ee/api/projects.html#get-a-projects-pull-mirror-details ([`060cfe1`](https://github.com/python-gitlab/python-gitlab/commit/060cfe1465a99657c5f832796ab3aa03aad934c7))

* feat(api): add support for remote project import from AWS S3 (#2357) ([`892281e`](https://github.com/python-gitlab/python-gitlab/commit/892281e35e3d81c9e43ff6a974f920daa83ea8b2))

* feat(api): add support for remote project import (#2348) ([`e5dc72d`](https://github.com/python-gitlab/python-gitlab/commit/e5dc72de9b3cdf0a7944ee0961fbdc6784c7f315))

* feat(api): add application statistics ([`6fcf3b6`](https://github.com/python-gitlab/python-gitlab/commit/6fcf3b68be095e614b969f5922ad8a67978cd4db))

### Fix

* fix(cli): Enable debug before doing auth

Authentication issues are currently hard to debug since `--debug` only
has effect after `gl.auth()` has been called.

For example, a 401 error is printed without any details about the actual
HTTP request being sent:

    $ gitlab --debug --server-url https://gitlab.com current-user get
    401: 401 Unauthorized

By moving the call to `gl.enable_debug()` the usual debug logs get
printed before the final error message.

Signed-off-by: Emanuele Aina &lt;emanuele.aina@collabora.com&gt; ([`65abb85`](https://github.com/python-gitlab/python-gitlab/commit/65abb85be7fc8ef57b295296111dac0a97ed1c49))

* fix(cli): expose missing mr_default_target_self project attribute

Example::

   gitlab project update --id 616 --mr-default-target-self 1

References:

* https://gitlab.com/gitlab-org/gitlab/-/merge_requests/58093
* https://gitlab.com/gitlab-org/gitlab/-/blob/v13.11.0-ee/doc/user/project/merge_requests/creating_merge_requests.md#new-merge-request-from-a-fork
* https://gitlab.com/gitlab-org/gitlab/-/blob/v14.7.0-ee/doc/api/projects.md#get-single-project ([`12aea32`](https://github.com/python-gitlab/python-gitlab/commit/12aea32d1c0f7e6eac0d19da580bf6efde79d3e2))

* fix: use POST method and return dict in `cancel_merge_when_pipeline_succeeds()` (#2350)

* Call was incorrectly using a `PUT` method when should have used a
    `POST` method.
  * Changed return type to a `dict` as GitLab only returns
    {&#39;status&#39;: &#39;success&#39;} on success. Since the function didn&#39;t work
    previously, this should not impact anyone.
  * Updated the test fixture `merge_request` to add ability to create
    a pipeline.
  * Added functional test for `mr.cancel_merge_when_pipeline_succeeds()`

Fixes: #2349 ([`bd82d74`](https://github.com/python-gitlab/python-gitlab/commit/bd82d745c8ea9ff6ff078a4c961a2d6e64a2f63c))

### Refactor

* refactor: explicitly use ProjectSecureFile ([`0c98b2d`](https://github.com/python-gitlab/python-gitlab/commit/0c98b2d8f4b8c1ac6a4b496282f307687b652759))

### Test

* test(api): fix flaky test `test_cancel_merge_when_pipeline_succeeds`

This is an attempt to fix the flaky test
`test_cancel_merge_when_pipeline_succeeds`.
Were seeing a: 405 Method Not Allowed error when setting the MR to
merge_when_pipeline_succeeds.

Closes: #2383 ([`6525c17`](https://github.com/python-gitlab/python-gitlab/commit/6525c17b8865ead650a6e09f9bf625ca9881911b))

### Unknown

* Merge pull request #2347 from Shreya-7/issue-2264-add-application-statistics

feat(api): add application statistics ([`31ec146`](https://github.com/python-gitlab/python-gitlab/commit/31ec1469211875a9c2b16b4d891a8b7fe1043af1))

* Merge pull request #2351 from python-gitlab/renovate/all-minor-patch

chore(deps): update all non-major dependencies ([`2974966`](https://github.com/python-gitlab/python-gitlab/commit/29749660b9ca97dda1e7ad104d79266d5ed24d7b))

* Merge pull request #2352 from python-gitlab/renovate/maxbrunet-pre-commit-renovate-34.x

chore(deps): update pre-commit hook maxbrunet/pre-commit-renovate to v34 ([`c3d9820`](https://github.com/python-gitlab/python-gitlab/commit/c3d982096d0ce562e63716decbce8185e61bc2f1))

## v3.11.0 (2022-10-28)

### Chore

* chore: add responses to pre-commit deps ([`4b8ddc7`](https://github.com/python-gitlab/python-gitlab/commit/4b8ddc74c8f7863631005e8eb9861f1e2f0a4cbc))

* chore: add basic type checks to functional/api tests ([`5b642a5`](https://github.com/python-gitlab/python-gitlab/commit/5b642a5d4c934f0680fa99079484176d36641861))

* chore: add basic typing to functional tests ([`ee143c9`](https://github.com/python-gitlab/python-gitlab/commit/ee143c9d6df0f1498483236cc228e12132bef132))

* chore: narrow type hints for license API ([`50731c1`](https://github.com/python-gitlab/python-gitlab/commit/50731c173083460f249b1718cbe2288fc3c46c1a))

* chore: add basic type checks to meta tests ([`545d6d6`](https://github.com/python-gitlab/python-gitlab/commit/545d6d60673c7686ec873a343b6afd77ec9062ec))

* chore: add basic typing to smoke tests ([`64e8c31`](https://github.com/python-gitlab/python-gitlab/commit/64e8c31e1d35082bc2e52582205157ae1a6c4605))

* chore: add basic typing to test root ([`0b2f6bc`](https://github.com/python-gitlab/python-gitlab/commit/0b2f6bcf454685786a89138b36b10fba649663dd))

* chore(deps): update pre-commit hook maxbrunet/pre-commit-renovate to v33 ([`932bbde`](https://github.com/python-gitlab/python-gitlab/commit/932bbde7ff10dd0f73bc81b7e91179b93a64602b))

* chore(deps): update all non-major dependencies ([`dde3642`](https://github.com/python-gitlab/python-gitlab/commit/dde3642bcd41ea17c4f301188cb571db31fe4da8))

* chore: add `not-callable` to pylint ignore list

The `not-callable` error started showing up. Ignore this error as
it is invalid. Also `mypy` tests for these issues.

Closes: #2334 ([`f0c02a5`](https://github.com/python-gitlab/python-gitlab/commit/f0c02a553da05ea3fdca99798998f40cfd820983))

* chore: revert compose upgrade

This reverts commit f825d70e25feae8cd9da84e768ec6075edbc2200. ([`dd04e8e`](https://github.com/python-gitlab/python-gitlab/commit/dd04e8ef7eee2793fba38a1eec019b00b3bb616e))

* chore(deps): update all non-major dependencies ([`2966234`](https://github.com/python-gitlab/python-gitlab/commit/296623410ae0b21454ac11e48e5991329c359c4d))

* chore: use kwargs for http_request docs ([`124abab`](https://github.com/python-gitlab/python-gitlab/commit/124abab483ab6be71dbed91b8d518ae27355b9ae))

* chore(deps): pin GitHub Actions ([`8dbaa5c`](https://github.com/python-gitlab/python-gitlab/commit/8dbaa5cddef6d7527ded686553121173e33d2973))

* chore(deps): group non-major upgrades to reduce noise ([`37d14bd`](https://github.com/python-gitlab/python-gitlab/commit/37d14bd9fd399a498d72a03b536701678af71702))

* chore(deps): pin and clean up test dependencies ([`60b9197`](https://github.com/python-gitlab/python-gitlab/commit/60b9197dfe327eb2310523bae04c746d34458fa3))

* chore(deps): pin dependencies ([`953f38d`](https://github.com/python-gitlab/python-gitlab/commit/953f38dcc7ccb2a9ad0ea8f1b9a9e06bd16b9133))

* chore: topic functional tests ([`d542eba`](https://github.com/python-gitlab/python-gitlab/commit/d542eba2de95f2cebcc6fc7d343b6daec95e4219))

* chore: renovate and precommit cleanup ([`153d373`](https://github.com/python-gitlab/python-gitlab/commit/153d3739021d2375438fe35ce819c77142914567))

* chore(deps): update black to v22.10.0 ([`531ee05`](https://github.com/python-gitlab/python-gitlab/commit/531ee05bdafbb6fee8f6c9894af15fc89c67d610))

* chore(deps): update dependency types-requests to v2.28.11.2 ([`d47c0f0`](https://github.com/python-gitlab/python-gitlab/commit/d47c0f06317d6a63af71bb261d6bb4e83325f261))

* chore: fix flaky test ([`fdd4114`](https://github.com/python-gitlab/python-gitlab/commit/fdd4114097ca69bbb4fd9c3117b83063b242f8f2))

* chore: update the issue templates

* Have an option to go to the discussions
* Have an option to go to the Gitter chat
* Move the bug/issue template into the .github/ISSUE_TEMPLATE/
  directory ([`c15bd33`](https://github.com/python-gitlab/python-gitlab/commit/c15bd33f45fbd9d064f1e173c6b3ca1b216def2f))

* chore: simplify `wait_for_sidekiq` usage

Simplify usage of `wait_for_sidekiq` by putting the assert if it timed
out inside the function rather than after calling it. ([`196538b`](https://github.com/python-gitlab/python-gitlab/commit/196538ba3e233ba2acf6f816f436888ba4b1f52a))

* chore(deps): update dependency pylint to v2.15.3 ([`6627a60`](https://github.com/python-gitlab/python-gitlab/commit/6627a60a12471f794cb308e76e449b463b9ce37a))

* chore(deps): update dependency mypy to v0.981 ([`da48849`](https://github.com/python-gitlab/python-gitlab/commit/da48849a303beb0d0292bccd43d54aacfb0c316b))

* chore(deps): update dependency commitizen to v2.35.0 ([`4ce9559`](https://github.com/python-gitlab/python-gitlab/commit/4ce95594695d2e19a215719d535bc713cf381729))

* chore(deps): update typing dependencies ([`81285fa`](https://github.com/python-gitlab/python-gitlab/commit/81285fafd2b3c643d130a84550a666d4cc480b51))

### Documentation

* docs(advanced): add hint on type narrowing ([`a404152`](https://github.com/python-gitlab/python-gitlab/commit/a40415290923d69d087dd292af902efbdfb5c258))

* docs: add minimal docs about the `enable_debug()` method

Add some minimal documentation about the `enable_debug()` method. ([`b4e9ab7`](https://github.com/python-gitlab/python-gitlab/commit/b4e9ab7ee395e575f17450c2dc0d519f7192e58e))

* docs(commits): fix commit create example for binary content ([`bcc1eb4`](https://github.com/python-gitlab/python-gitlab/commit/bcc1eb4571f76b3ca0954adb5525b26f05958e3f))

* docs(readme): add a basic feature list ([`b4d53f1`](https://github.com/python-gitlab/python-gitlab/commit/b4d53f1abb264cd9df8e4ac6560ab0895080d867))

* docs(api): describe use of lower-level methods ([`b7a6874`](https://github.com/python-gitlab/python-gitlab/commit/b7a687490d2690e6bd4706391199135e658e1dc6))

* docs(api): describe the list() and all() runners&#39; functions ([`b6cc3f2`](https://github.com/python-gitlab/python-gitlab/commit/b6cc3f255532521eb259b42780354e03ce51458e))

* docs(api): Update `merge_requests.rst`: `mr_id` to `mr_iid`

Typo: Author probably meant `mr_iid` (i.e. project-specific MR ID)
and **not** `mr_id` (i.e. server-wide MR ID)

Closes: https://github.com/python-gitlab/python-gitlab/issues/2295

Signed-off-by: Stavros Ntentos &lt;133706+stdedos@users.noreply.github.com&gt; ([`b32234d`](https://github.com/python-gitlab/python-gitlab/commit/b32234d1f8c4492b6b2474f91be9479ad23115bb))

### Feature

* feat(build): officially support Python 3.11 ([`74f66c7`](https://github.com/python-gitlab/python-gitlab/commit/74f66c71f3974cf68f5038f4fc3995e53d44aebe))

* feat(api): add support for topics merge API ([`9a6d197`](https://github.com/python-gitlab/python-gitlab/commit/9a6d197f9d2a88bdba8dab1f9abaa4e081a14792))

### Fix

* fix: remove `project.approvals.set_approvals()` method

The `project.approvals.set_approvals()` method used the
`/projects/:id/approvers` end point. That end point was removed from
GitLab in the 13.11 release, on 2-Apr-2021 in commit
27dc2f2fe81249bbdc25f7bd8fe799752aac05e6 via merge commit
e482597a8cf1bae8e27abd6774b684fb90491835. It was deprecated on
19-Aug-2019.

See merge request:
https://gitlab.com/gitlab-org/gitlab/-/merge_requests/57473 ([`91f08f0`](https://github.com/python-gitlab/python-gitlab/commit/91f08f01356ca5e38d967700a5da053f05b6fab0))

* fix: use epic id instead of iid for epic notes ([`97cae38`](https://github.com/python-gitlab/python-gitlab/commit/97cae38a315910972279f2d334e91fa54d9ede0c))

* fix(cli): handle list response for json/yaml output

Handle the case with the CLI where a list response is returned from
GitLab and json/yaml output is requested.

Add a functional CLI test to validate it works.

Closes: #2287 ([`9b88132`](https://github.com/python-gitlab/python-gitlab/commit/9b88132078ed37417c2a45369b4976c9c67f7882))

* fix: intermittent failure in test_merge_request_reset_approvals

Have been seeing intermittent failures in the test:
tests/functional/api/test_merge_requests.py::test_merge_request_reset_approvals

Also saw a failure in:
tests/functional/cli/test_cli_v4.py::test_accept_request_merge[subprocess]

Add a call to `wait_for_sidekiq()` to hopefully resolve the issues. ([`3dde36e`](https://github.com/python-gitlab/python-gitlab/commit/3dde36eab40406948adca633f7197beb32b29552))

### Refactor

* refactor: pre-commit trigger from tox ([`6e59c12`](https://github.com/python-gitlab/python-gitlab/commit/6e59c12fe761e8deea491d1507beaf00ca381cdc))

* refactor: migrate legacy EE tests to pytest ([`88c2505`](https://github.com/python-gitlab/python-gitlab/commit/88c2505b05dbcfa41b9e0458d4f2ec7dcc6f8169))

* refactor: pytest-docker fixtures ([`3e4781a`](https://github.com/python-gitlab/python-gitlab/commit/3e4781a66577a6ded58f721739f8e9422886f9cd))

* refactor(deps): drop compose v1 dependency in favor of v2 ([`f825d70`](https://github.com/python-gitlab/python-gitlab/commit/f825d70e25feae8cd9da84e768ec6075edbc2200))

### Test

* test: fix `test_project_push_rules` test

Make the `test_project_push_rules` test work. ([`8779cf6`](https://github.com/python-gitlab/python-gitlab/commit/8779cf672af1abd1a1f67afef20a61ae5876a724))

* test: enable skipping tests per GitLab plan ([`01d5f68`](https://github.com/python-gitlab/python-gitlab/commit/01d5f68295b62c0a8bd431a9cd31bf9e4e91e7d9))

* test: use false instead of /usr/bin/false

On Debian systems false is located at /bin/false (coreutils package).
This fixes unit test failure on Debian system:

FileNotFoundError: [Errno 2] No such file or directory: &#39;/usr/bin/false&#39;
/usr/lib/python3.10/subprocess.py:1845: FileNotFoundError ([`51964b3`](https://github.com/python-gitlab/python-gitlab/commit/51964b3142d4d19f44705fde8e7e721233c53dd2))

### Unknown

* Merge pull request #2345 from python-gitlab/jlvillal/enable_debug

docs: add minimal docs about the `enable_debug()` method ([`8f74a33`](https://github.com/python-gitlab/python-gitlab/commit/8f74a333ada3d819187dec5905aeca1352fba270))

* Merge pull request #2343 from python-gitlab/feat/python-3-11

feat(build): officially support Python 3.11 ([`a3b4824`](https://github.com/python-gitlab/python-gitlab/commit/a3b482459d1e2325bf9352a0ee952b35a38f7e32))

* Merge pull request #2341 from python-gitlab/renovate/maxbrunet-pre-commit-renovate-33.x

chore(deps): update pre-commit hook maxbrunet/pre-commit-renovate to v33 ([`31a39e1`](https://github.com/python-gitlab/python-gitlab/commit/31a39e1fda848227c15c2e535fa68eabf80f3468))

* Merge pull request #2320 from lmilbaum/refactoring

refactor: pre-commit triggered from tox ([`eec6c02`](https://github.com/python-gitlab/python-gitlab/commit/eec6c021bb26aeade48e4882cd4fed70c867d731))

* Merge pull request #2333 from python-gitlab/jlvillal/remove_approvers_endpoint

fix: remove `project.approvals.set_approvals()` method ([`eb54adf`](https://github.com/python-gitlab/python-gitlab/commit/eb54adf2fe7d3c68dcb6021065e51ba33b7bbc04))

* Merge pull request #2332 from python-gitlab/jlvillal/fix_test

test: fix `test_project_push_rules` test ([`c676b43`](https://github.com/python-gitlab/python-gitlab/commit/c676b43dc4a5dd7dc0797f5bcf7db830db7645e7))

* Merge pull request #2322 from AndreySV/fix-test-with-false

test: use false instead of /usr/bin/false ([`4eca9b9`](https://github.com/python-gitlab/python-gitlab/commit/4eca9b9db8a05f379e1750a53f84f67e8710095a))

* Merge pull request #2318 from python-gitlab/renovate/all-minor-patch

chore(deps): update all non-major dependencies ([`9410acb`](https://github.com/python-gitlab/python-gitlab/commit/9410acb79a65420c344bdf3b9c06eb92c7ad10a1))

## v3.10.0 (2022-09-28)

### Chore

* chore: bump GitLab docker image to 15.4.0-ee.0

 * Use `settings.delayed_group_deletion=False` as that is the
   recommended method to turn off the delayed group deletion now.
 * Change test to look for `default` as `pages` is not mentioned in
   the docs[1]

[1] https://docs.gitlab.com/ee/api/sidekiq_metrics.html#get-the-current-queue-metrics ([`b87a2bc`](https://github.com/python-gitlab/python-gitlab/commit/b87a2bc7cfacd3a3c4a18342c07b89356bf38d50))

* chore(deps): update black to v22.8.0 ([`86b0e40`](https://github.com/python-gitlab/python-gitlab/commit/86b0e4015a258433528de0a5b063defa3eeb3e26))

* chore(deps): update dependency types-requests to v2.28.10 ([`5dde7d4`](https://github.com/python-gitlab/python-gitlab/commit/5dde7d41e48310ff70a4cef0b6bfa2df00fd8669))

* chore(deps): update dependency pytest to v7.1.3 ([`ec7f26c`](https://github.com/python-gitlab/python-gitlab/commit/ec7f26cd0f61a3cbadc3a1193c43b54d5b71c82b))

* chore(deps): update dependency commitizen to v2.32.5 ([`e180f14`](https://github.com/python-gitlab/python-gitlab/commit/e180f14309fa728e612ad6259c2e2c1f328a140c))

* chore(deps): update dependency commitizen to v2.32.2 ([`31aea28`](https://github.com/python-gitlab/python-gitlab/commit/31aea286e0767148498af300e78db7dbdf715bda))

* chore(deps): update pre-commit hook commitizen-tools/commitizen to v2.32.2 ([`31ba64f`](https://github.com/python-gitlab/python-gitlab/commit/31ba64f2849ce85d434cd04ec7b837ca8f659e03))

### Feature

* feat: Add reset_approvals api

Added the newly added reset_approvals merge request api.

Signed-off-by: Lucas Zampieri &lt;lzampier@redhat.com&gt; ([`88693ff`](https://github.com/python-gitlab/python-gitlab/commit/88693ff2d6f4eecf3c79d017df52738886e2d636))

* feat: add support for deployment approval endpoint

Add support for the deployment approval endpoint[1]

[1] https://docs.gitlab.com/ee/api/deployments.html#approve-or-reject-a-blocked-deployment
Closes: #2253 ([`9c9eeb9`](https://github.com/python-gitlab/python-gitlab/commit/9c9eeb901b1f3acd3fb0c4f24014ae2ed7c975ec))

### Fix

* fix(cli): add missing attributes for creating MRs ([`1714d0a`](https://github.com/python-gitlab/python-gitlab/commit/1714d0a980afdb648d203751dedf95ee95ac326e))

* fix(cli): add missing attribute for MR changes ([`20c46a0`](https://github.com/python-gitlab/python-gitlab/commit/20c46a0572d962f405041983e38274aeb79a12e4))

### Unknown

* Merge pull request #2280 from python-gitlab/jlvillal/docker_image

chore: bump GitLab docker image to 15.4.0-ee.0 ([`fceeebc`](https://github.com/python-gitlab/python-gitlab/commit/fceeebc441d4d3a4c0443fd9dbfcb188fd4f910d))

* Merge pull request #2261 from python-gitlab/renovate/commitizen-2.x

chore(deps): update dependency commitizen to v2.32.2 ([`336ee21`](https://github.com/python-gitlab/python-gitlab/commit/336ee21779a55a1371c94e0cd2af0b047b457a7d))

* Merge pull request #2262 from python-gitlab/renovate/commitizen-tools-commitizen-2.x

chore(deps): update pre-commit hook commitizen-tools/commitizen to v2.32.2 ([`89bf581`](https://github.com/python-gitlab/python-gitlab/commit/89bf581fd9f69e860cca57c9e8b9750a5b864551))

* Merge pull request #2254 from python-gitlab/jlvillal/deploy_approve

feat: add support for deployment approval endpoint ([`56fbe02`](https://github.com/python-gitlab/python-gitlab/commit/56fbe022e11b3b47fef0bd45b41543c9d73ec94e))

## v3.9.0 (2022-08-28)

### Chore

* chore: Only check for our UserWarning

The GitHub CI is showing a ResourceWarning, causing our test to fail.

Update test to only look for our UserWarning which should not appear.

What was seen when debugging the GitHub CI:
{message:
    ResourceWarning(
        &#34;unclosed &lt;socket.socket fd=12, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=6, laddr=(&#39;127.0.0.1&#39;, 50862), raddr=(&#39;127.0.0.1&#39;, 8080)&gt;&#34;
    ),
    category: &#39;ResourceWarning&#39;,
    filename: &#39;/home/runner/work/python-gitlab/python-gitlab/.tox/api_func_v4/lib/python3.10/site-packages/urllib3/poolmanager.py&#39;,
    lineno: 271,
    line: None
} ([`bd4dfb4`](https://github.com/python-gitlab/python-gitlab/commit/bd4dfb4729377bf64c552ef6052095aa0b5658b8))

* chore: fix issue if only run test_gitlab.py func test

Make it so can run just the test_gitlab.py functional test.

For example:
$ tox -e api_func_v4 -- -k test_gitlab.py ([`98f1956`](https://github.com/python-gitlab/python-gitlab/commit/98f19564c2a9feb108845d33bf3631fa219e51c6))

* chore(ci): make pytest annotations work ([`f67514e`](https://github.com/python-gitlab/python-gitlab/commit/f67514e5ffdbe0141b91c88366ff5233e0293ca2))

* chore(deps): update pre-commit hook commitizen-tools/commitizen to v2.32.1 ([`cdd6efe`](https://github.com/python-gitlab/python-gitlab/commit/cdd6efef596a1409d6d8a9ea13e04c943b8c4b6a))

* chore(deps): update dependency commitizen to v2.32.1 ([`9787c5c`](https://github.com/python-gitlab/python-gitlab/commit/9787c5cf01a518164b5951ec739abb1d410ff64c))

* chore(deps): update dependency types-requests to v2.28.9 ([`be932f6`](https://github.com/python-gitlab/python-gitlab/commit/be932f6dde5f47fb3d30e654b82563cd719ae8ce))

* chore(deps): update pre-commit hook pycqa/flake8 to v5 ([`835d884`](https://github.com/python-gitlab/python-gitlab/commit/835d884e702f1ee48575b3154136f1ef4b2f2ff2))

* chore(deps): update pre-commit hook commitizen-tools/commitizen to v2.31.0 ([`71d37d9`](https://github.com/python-gitlab/python-gitlab/commit/71d37d98721c0813b096124ed2ccf5487ab463b9))

* chore(deps): update dependency commitizen to v2.31.0 ([`4ff0894`](https://github.com/python-gitlab/python-gitlab/commit/4ff0894870977f07657e80bfaa06387f2af87d10))

* chore(deps): update dependency types-setuptools to v64 ([`4c97f26`](https://github.com/python-gitlab/python-gitlab/commit/4c97f26287cc947ab5ee228a5862f2a20535d2ae))

* chore(deps): update dependency types-requests to v2.28.8 ([`8e5b86f`](https://github.com/python-gitlab/python-gitlab/commit/8e5b86fcc72bf30749228519f1b4a6e29a8dbbe9))

### Feature

* feat: add support for merge_base API ([`dd4fbd5`](https://github.com/python-gitlab/python-gitlab/commit/dd4fbd5e43adbbc502624a8de0d30925d798dec0))

### Unknown

* Merge pull request #2255 from python-gitlab/jlvillal/noop

chore: fix issue if only run test_gitlab.py func test ([`e095735`](https://github.com/python-gitlab/python-gitlab/commit/e095735e02867f433fdff388212785379d43b89b))

* Merge pull request #2241 from python-gitlab/renovate/pycqa-flake8-5.x

chore(deps): update pre-commit hook pycqa/flake8 to v5 ([`13d4927`](https://github.com/python-gitlab/python-gitlab/commit/13d49279d28c55239f8c3e22b056d76df0f1ef7f))

* Merge pull request #2239 from python-gitlab/renovate/commitizen-tools-commitizen-2.x

chore(deps): update pre-commit hook commitizen-tools/commitizen to v2.31.0 ([`9381a44`](https://github.com/python-gitlab/python-gitlab/commit/9381a44c8dea892e164aaca2218f1d7a3cddf125))

* Merge pull request #2238 from python-gitlab/renovate/commitizen-2.x

chore(deps): update dependency commitizen to v2.31.0 ([`b432e47`](https://github.com/python-gitlab/python-gitlab/commit/b432e47d2e05d36a308d513007e8aecbd10ac001))

## v3.8.1 (2022-08-10)

### Chore

* chore(deps): update dependency commitizen to v2.29.5 ([`181390a`](https://github.com/python-gitlab/python-gitlab/commit/181390a4e07e3c62b86ade11d9815d36440f5817))

* chore(deps): update dependency flake8 to v5.0.4 ([`50a4fec`](https://github.com/python-gitlab/python-gitlab/commit/50a4feca96210e890d8ff824c2c6bf3d57f21799))

* chore(deps): update dependency sphinx to v5 ([`3f3396e`](https://github.com/python-gitlab/python-gitlab/commit/3f3396ee383c8e6f2deeb286f04184a67edb6d1d))

* chore: remove broad Exception catching from `config.py`

Change &#34;except Exception:&#34; catching to more granular exceptions.

A step in enabling the &#34;broad-except&#34; check in pylint. ([`0abc90b`](https://github.com/python-gitlab/python-gitlab/commit/0abc90b7b456d75869869618097f8fcb0f0d9e8d))

* chore: add license badge to readme ([`9aecc9e`](https://github.com/python-gitlab/python-gitlab/commit/9aecc9e5ae1e2e254b8a27283a0744fe6fd05fb6))

* chore: consolidate license and authors ([`366665e`](https://github.com/python-gitlab/python-gitlab/commit/366665e89045eb24d47f730e2a5dea6229839e20))

### Fix

* fix(client): do not assume user attrs returned for auth()

This is mostly relevant for people mocking the API in tests. ([`a07547c`](https://github.com/python-gitlab/python-gitlab/commit/a07547cba981380935966dff2c87c2c27d6b18d9))

### Unknown

* Merge pull request #2233 from python-gitlab/fix/do-not-require-web-url ([`99d580a`](https://github.com/python-gitlab/python-gitlab/commit/99d580ab9c56933c82d975e24170c3a9b27de423))

* Merge pull request #2153 from python-gitlab/renovate/sphinx-5.x

chore(deps): update dependency sphinx to v5 ([`1e12eaf`](https://github.com/python-gitlab/python-gitlab/commit/1e12eaf22ae46a641688c1b611769aa14e695445))

* Merge pull request #2212 from python-gitlab/jlvillal/config

chore: remove broad Exception catching from `config.py` ([`70e67bf`](https://github.com/python-gitlab/python-gitlab/commit/70e67bfec915a9404acdedf615e7548d75317ea3))

## v3.8.0 (2022-08-04)

### Chore

* chore: use `urlunparse` instead of string replace

Use the `urlunparse()` function to reconstruct the URL without the
query parameters. ([`6d1b62d`](https://github.com/python-gitlab/python-gitlab/commit/6d1b62d4b248c4c021a59cd234c3a2b19e6fad07))

* chore(ci): bump semantic-release for fixed commit parser ([`1e063ae`](https://github.com/python-gitlab/python-gitlab/commit/1e063ae1c4763c176be3c5e92da4ffc61cb5d415))

* chore: enable mypy check `disallow_any_generics` ([`24d17b4`](https://github.com/python-gitlab/python-gitlab/commit/24d17b43da16dd11ab37b2cee561d9392c90f32e))

* chore(deps): update pre-commit hook commitizen-tools/commitizen to v2.29.2 ([`4988c02`](https://github.com/python-gitlab/python-gitlab/commit/4988c029e0dda89ff43375d1cd2f407abdbe3dc7))

* chore: enable mypy check `no_implicit_optional` ([`64b208e`](https://github.com/python-gitlab/python-gitlab/commit/64b208e0e91540af2b645da595f0ef79ee7522e1))

* chore(deps): update dependency flake8 to v5 ([`cdc384b`](https://github.com/python-gitlab/python-gitlab/commit/cdc384b8a2096e31aff12ea98383e2b1456c5731))

* chore(deps): update dependency types-requests to v2.28.6 ([`54dd4c3`](https://github.com/python-gitlab/python-gitlab/commit/54dd4c3f857f82aa8781b0daf22fa2dd3c60c2c4))

* chore(deps): update dependency commitizen to v2.29.2 ([`30274ea`](https://github.com/python-gitlab/python-gitlab/commit/30274ead81205946a5a7560e592f346075035e0e))

* chore: change `_repr_attr` for Project to be `path_with_namespace`

Previously `_repr_attr` was `path` but that only gives the basename of
the path.  So https://gitlab.com/gitlab-org/gitlab would only show
&#34;gitlab&#34;. Using `path_with_namespace` it will now show
&#34;gitlab-org/gitlab&#34; ([`7cccefe`](https://github.com/python-gitlab/python-gitlab/commit/7cccefe6da0e90391953734d95debab2fe07ea49))

* chore: enable mypy check `warn_return_any`

Update code so that the `warn_return_any` check passes. ([`76ec4b4`](https://github.com/python-gitlab/python-gitlab/commit/76ec4b481fa931ea36a195ac474812c11babef7b))

* chore: make code PEP597 compliant

Use `encoding=&#34;utf-8&#34;` in `open()` and open-like functions.

https://peps.python.org/pep-0597/ ([`433dba0`](https://github.com/python-gitlab/python-gitlab/commit/433dba02e0d4462ae84a73d8699fe7f3e07aa410))

* chore(clusters): deprecate clusters support

Cluster support was deprecated in GitLab 14.5 [1]. And disabled by
default in GitLab 15.0 [2]

  * Update docs to mark clusters as deprecated
  * Remove testing of clusters

[1] https://docs.gitlab.com/ee/api/project_clusters.html
[2] https://gitlab.com/groups/gitlab-org/configure/-/epics/8 ([`b46b379`](https://github.com/python-gitlab/python-gitlab/commit/b46b3791707ac76d501d6b7b829d1370925fd614))

* chore(topics): &#39;title&#39; is required when creating a topic

In GitLab &gt;= 15.0 `title` is required when creating a topic. ([`271f688`](https://github.com/python-gitlab/python-gitlab/commit/271f6880dbb15b56305efc1fc73924ac26fb97ad))

### Documentation

* docs: describe self-revoking personal access tokens ([`5ea48fc`](https://github.com/python-gitlab/python-gitlab/commit/5ea48fc3c28f872dd1184957a6f2385da075281c))

### Feature

* feat(client): warn user on misconfigured URL in `auth()` ([`0040b43`](https://github.com/python-gitlab/python-gitlab/commit/0040b4337bae815cfe1a06f8371a7a720146f271))

* feat: Support downloading archive subpaths ([`cadb0e5`](https://github.com/python-gitlab/python-gitlab/commit/cadb0e55347cdac149e49f611c99b9d53a105520))

### Fix

* fix(client): ensure encoded query params are never duplicated ([`1398426`](https://github.com/python-gitlab/python-gitlab/commit/1398426cd748fdf492fe6184b03ac2fcb7e4fd6e))

* fix: optionally keep user-provided base URL for pagination (#2149) ([`e2ea8b8`](https://github.com/python-gitlab/python-gitlab/commit/e2ea8b89a7b0aebdb1eb3b99196d7c0034076df8))

### Refactor

* refactor(client): factor out URL check into a helper ([`af21a18`](https://github.com/python-gitlab/python-gitlab/commit/af21a1856aa904f331859983493fe966d5a2969b))

* refactor(client): remove handling for incorrect link header

This was a quirk only present in GitLab 13.0 and fixed with 13.1.
See
https://gitlab.com/gitlab-org/gitlab/-/merge_requests/33714 and
https://gitlab.com/gitlab-org/gitlab/-/issues/218504 for more
context. ([`77c04b1`](https://github.com/python-gitlab/python-gitlab/commit/77c04b1acb2815290bcd6f50c37d75329409e9d3))

### Test

* test(unit): reproduce duplicate encoded query params ([`6f71c66`](https://github.com/python-gitlab/python-gitlab/commit/6f71c663a302b20632558b4c94be428ba831ee7f))

* test: attempt to make functional test startup more reliable

The functional tests have been erratic. Current theory is that we are
starting the tests before the GitLab container is fully up and
running.

  * Add checking of the Health Check[1] endpoints.
  * Add a 20 second delay after we believe it is up and running.
  * Increase timeout from 300 to 400 seconds

[1] https://docs.gitlab.com/ee/user/admin_area/monitoring/health_check.html ([`67508e8`](https://github.com/python-gitlab/python-gitlab/commit/67508e8100be18ce066016dcb8e39fa9f0c59e51))

* test(functional): bump GitLab docker image to 15.2.0-ee.0

Use the GitLab docker image 15.2.0-ee.0 in the functional testing. ([`69014e9`](https://github.com/python-gitlab/python-gitlab/commit/69014e9be3a781be6742478af820ea097d004791))

### Unknown

* Merge pull request #2221 from python-gitlab/jlvillal/unparse

chore: use `urlunparse` instead of string replace ([`9e0b60f`](https://github.com/python-gitlab/python-gitlab/commit/9e0b60fb36c64d57c14926c0801ecf91215707bf))

* Merge pull request #2219 from python-gitlab/fix/no-duplicate-params

fix(client): ensure encoded query params are never duplicated ([`d263f57`](https://github.com/python-gitlab/python-gitlab/commit/d263f57a34a58d44531e3abbdbfedf354b0c70ca))

* Merge pull request #2220 from python-gitlab/chore/bump-semantic-release

chore(ci): bump semantic-release for fixed commit parser ([`2ebfc70`](https://github.com/python-gitlab/python-gitlab/commit/2ebfc7096ddbf2386029536acef1858985f3f257))

* Merge pull request #2211 from python-gitlab/jlvillal/mypy_step_step

chore: enable mypy check `disallow_any_generics` ([`1136b17`](https://github.com/python-gitlab/python-gitlab/commit/1136b17f4e5f36c66c3a67292e508b43ded9ca3e))

* Merge pull request #2208 from python-gitlab/renovate/commitizen-tools-commitizen-2.x

chore(deps): update pre-commit hook commitizen-tools/commitizen to v2.29.2 ([`6cedbc8`](https://github.com/python-gitlab/python-gitlab/commit/6cedbc8f4808f795332d0d4642b7469681a4bf48))

* Merge pull request #2210 from python-gitlab/jlvillal/mypy_step_by_step

chore: enable mypy check `no_implicit_optional` ([`1c91b24`](https://github.com/python-gitlab/python-gitlab/commit/1c91b24dac47b82f4621566fad4933b999d1503c))

* Merge pull request #2209 from python-gitlab/renovate/flake8-5.x

chore(deps): update dependency flake8 to v5 ([`d81cec3`](https://github.com/python-gitlab/python-gitlab/commit/d81cec36136d8425767adaa144abfc513fcb8285))

* Merge pull request #2203 from python-gitlab/jlvillal/project_repr

chore: change `_repr_attr` for Project to be `path_with_namespace` ([`98bdb98`](https://github.com/python-gitlab/python-gitlab/commit/98bdb9891313f176e7071c1e43f4b6306c8f30dc))

* Merge pull request #2188 from python-gitlab/jlvillal/fix_functional_ci

test: attempt to make functional test startup more reliable ([`17414f7`](https://github.com/python-gitlab/python-gitlab/commit/17414f787a70a0d916193ac71bccce0297c4e4e8))

* Merge pull request #2199 from orf/patch-1

Support downloading archive subpaths ([`5e1df65`](https://github.com/python-gitlab/python-gitlab/commit/5e1df653e22cfbd1a2c1054d1c9b684f90e8c283))

* Merge pull request #2157 from python-gitlab/jlvillal/mypy_step_by_step

chore: enable mypy check `warn_return_any` ([`b8be32a`](https://github.com/python-gitlab/python-gitlab/commit/b8be32ae17fb59c5df080a9f7948fdff34b7d421))

* Merge pull request #2201 from python-gitlab/jlvillal/encoding_warning

chore: make code PEP597 compliant ([`1b7cd31`](https://github.com/python-gitlab/python-gitlab/commit/1b7cd31dc9a4a15623ac168eaa355422634e2876))

* Merge pull request #2194 from python-gitlab/jlvillal/update-gitlab

test(functional): bump GitLab docker image to 15.2.0-ee.0 ([`7a53c69`](https://github.com/python-gitlab/python-gitlab/commit/7a53c6950bb7df90e2a3f4e6d0436cb5d06c3b46))

## v3.7.0 (2022-07-28)

### Chore

* chore: revert &#34;test(functional): simplify token creation&#34;

This reverts commit 67ab24fe5ae10a9f8cc9122b1a08848e8927635d. ([`4b798fc`](https://github.com/python-gitlab/python-gitlab/commit/4b798fc2fdc44b73790c493c329147013464de14))

* chore: enable using GitLab EE in functional tests

Enable using GitLab Enterprise Edition (EE) in the functional tests.
This will allow us to add functional tests for EE only features in the
functional tests. ([`17c01ea`](https://github.com/python-gitlab/python-gitlab/commit/17c01ea55806c722523f2f9aef0175455ec942c5))

* chore(deps): update pre-commit hook commitizen-tools/commitizen to v2.29.0 ([`ad8d62a`](https://github.com/python-gitlab/python-gitlab/commit/ad8d62ae9612c173a749d413f7a84e5b8c0167cf))

* chore(deps): update dependency commitizen to v2.29.0 ([`c365be1`](https://github.com/python-gitlab/python-gitlab/commit/c365be1b908c5e4fda445680c023607bdf6c6281))

* chore(deps): update dependency mypy to v0.971 ([`7481d27`](https://github.com/python-gitlab/python-gitlab/commit/7481d271512eaa234315bcdbaf329026589bfda7))

* chore(deps): update typing dependencies ([`f2209a0`](https://github.com/python-gitlab/python-gitlab/commit/f2209a0ea084eaf7fbc89591ddfea138d99527a6))

* chore(authors): fix email and do the ABC ([`9833632`](https://github.com/python-gitlab/python-gitlab/commit/98336320a66d1859ba73e084a5e86edc3aa1643c))

* chore: make reset_gitlab() better

Saw issues in the CI where reset_gitlab() would fail. It would fail to
delete the group that is created when GitLab starts up. Extending the
timeout didn&#39;t fix the issue.

Changed the code to use the new `helpers.safe_delete()` function.
Which will delete the resource and then make sure it is deleted before
returning.

Also added some logging functionality that can be seen if logging is
turned on in pytest. ([`d87d6b1`](https://github.com/python-gitlab/python-gitlab/commit/d87d6b12fd3d73875559924cda3fd4b20402d336))

* chore: fixtures: after delete() wait to verify deleted

In our fixtures that create:
  - groups
  - project merge requests
  - projects
  - users

They delete the created objects after use. Now wait to ensure the
objects are deleted before continuing as having unexpected objects
existing can impact some of our tests. ([`1f73b6b`](https://github.com/python-gitlab/python-gitlab/commit/1f73b6b20f08a0fe4ce4cf9195702a03656a54e1))

* chore: add a `lazy` boolean attribute to `RESTObject`

This can be used to tell if a `RESTObject` was created using
`lazy=True`.

Add a message to the `AttributeError` if attribute access fails for an
instance created with `lazy=True`. ([`a7e8cfb`](https://github.com/python-gitlab/python-gitlab/commit/a7e8cfbae8e53d2c4b1fb75d57d42f00db8abd81))

* chore: enable mypy check `strict_equality`

Enable the `mypy` `strict_equality` check. ([`a29cd6c`](https://github.com/python-gitlab/python-gitlab/commit/a29cd6ce1ff7fa7f31a386cea3e02aa9ba3fb6c2))

* chore: change name of API functional test to `api_func_v4`

The CLI test is `cli_func_v4` and using `api_func_v4` matches with
that naming convention. ([`8cf5cd9`](https://github.com/python-gitlab/python-gitlab/commit/8cf5cd935cdeaf36a6877661c8dfb0be6c69f587))

* chore(deps): update typing dependencies ([`e772248`](https://github.com/python-gitlab/python-gitlab/commit/e77224818e63e818c10a7fad69f90e16d618bdf7))

* chore(deps): update pre-commit hook pycqa/pylint to v2.14.5 ([`c75a1d8`](https://github.com/python-gitlab/python-gitlab/commit/c75a1d860709e17a7c3324c5d85c7027733ea1e1))

* chore(deps): update dependency pylint to v2.14.5 ([`e153636`](https://github.com/python-gitlab/python-gitlab/commit/e153636d74a0a622b0cc18308aee665b3eca58a4))

* chore(deps): update pre-commit hook commitizen-tools/commitizen to v2.28.0 ([`d238e1b`](https://github.com/python-gitlab/python-gitlab/commit/d238e1b464c98da86677934bf99b000843d36747))

* chore(deps): update dependency commitizen to v2.28.0 ([`8703dd3`](https://github.com/python-gitlab/python-gitlab/commit/8703dd3c97f382920075e544b1b9d92fab401cc8))

* chore(deps): update black to v22.6.0 ([`82bd596`](https://github.com/python-gitlab/python-gitlab/commit/82bd59673c5c66da0cfa3b24d58b627946fe2cc3))

* chore(deps): update pre-commit hook pycqa/pylint to v2.14.4 ([`5cd39be`](https://github.com/python-gitlab/python-gitlab/commit/5cd39be000953907cdc2ce877a6bf267d601b707))

* chore(ci_lint): add create attributes ([`6e1342f`](https://github.com/python-gitlab/python-gitlab/commit/6e1342fc0b7cf740b25a939942ea02cdd18a9625))

* chore: simplify multi-nested try blocks

Instead of have a multi-nested series of try blocks. Convert it to a
more readable series of `if` statements. ([`e734470`](https://github.com/python-gitlab/python-gitlab/commit/e7344709d931e2b254d225d77ca1474bc69971f8))

* chore(deps): update dependency requests to v2.28.1 ([`be33245`](https://github.com/python-gitlab/python-gitlab/commit/be3324597aa3f22b0692d3afa1df489f2709a73e))

* chore(deps): update dependency pylint to v2.14.4 ([`2cee2d4`](https://github.com/python-gitlab/python-gitlab/commit/2cee2d4a86e76d3f63f3608ed6a92e64813613d3))

* chore: fix misspelling ([`2d08fc8`](https://github.com/python-gitlab/python-gitlab/commit/2d08fc89fb67de25ad41f64c86a9b8e96e4c261a))

* chore(docs): convert tabs to spaces

Some tabs snuck into the documentation. Convert them to 4-spaces. ([`9ea5520`](https://github.com/python-gitlab/python-gitlab/commit/9ea5520cec8979000d7f5dbcc950f2250babea96))

### Documentation

* docs(cli): showcase use of token scopes ([`4a6f8d6`](https://github.com/python-gitlab/python-gitlab/commit/4a6f8d67a94a3d104a24081ad1dbad5b2e3d9c3e))

* docs(projects): document export with upload to URL ([`03f5484`](https://github.com/python-gitlab/python-gitlab/commit/03f548453d84d99354aae7b638f5267e5d751c59))

* docs: describe fetching existing export status ([`9c5b8d5`](https://github.com/python-gitlab/python-gitlab/commit/9c5b8d54745a58b9fe72ba535b7868d1510379c0))

* docs(authors): add John ([`e2afb84`](https://github.com/python-gitlab/python-gitlab/commit/e2afb84dc4a259e8f40b7cc83e56289983c7db47))

* docs: document CI Lint usage ([`d5de4b1`](https://github.com/python-gitlab/python-gitlab/commit/d5de4b1fe38bedc07862bd9446dfd48b92cb078d))

* docs(users): add docs about listing a user&#39;s projects

Add docs about listing a user&#39;s projects.

Update docs on the membership API to update the URL to the upstream
docs and also add a note that it requires Administrator access to use. ([`065a1a5`](https://github.com/python-gitlab/python-gitlab/commit/065a1a5a32d34286df44800084285b30b934f911))

* docs: update return type of pushrules

Update the return type of pushrules to surround None with back-ticks
to make it code-formatted. ([`53cbecc`](https://github.com/python-gitlab/python-gitlab/commit/53cbeccd581318ce4ff6bec0acf3caf935bda0cf))

* docs: describe ROPC flow in place of password authentication ([`91c17b7`](https://github.com/python-gitlab/python-gitlab/commit/91c17b704f51e9a06b241d549f9a07a19c286118))

* docs(readme): Remove redundant `-v` that breaks the command
Remove redundant `-v` that breaks the command ([`c523e18`](https://github.com/python-gitlab/python-gitlab/commit/c523e186cc48f6bcac5245e3109b50a3852d16ef))

### Feature

* feat: allow sort/ordering for project releases

See: https://docs.gitlab.com/ee/api/releases/#list-releases ([`b1dd284`](https://github.com/python-gitlab/python-gitlab/commit/b1dd284066b4b94482b9d41310ac48b75bcddfee))

* feat(cli): add a custom help formatter

Add a custom argparse help formatter that overrides the output
format to list items vertically.

The formatter is derived from argparse.HelpFormatter with minimal changes.

Co-authored-by: John Villalovos &lt;john@sodarock.com&gt;
Co-authored-by: Nejc Habjan &lt;nejc.habjan@siemens.com&gt; ([`005ba93`](https://github.com/python-gitlab/python-gitlab/commit/005ba93074d391f818c39e46390723a0d0d16098))

* feat: add support for iterations API ([`194ee01`](https://github.com/python-gitlab/python-gitlab/commit/194ee0100c2868c1a9afb161c15f3145efb01c7c))

* feat(groups): add support for shared projects API ([`66461ba`](https://github.com/python-gitlab/python-gitlab/commit/66461ba519a85bfbd3cba284a0c8de11a3ac7cde))

* feat(issues): add support for issue reorder API ([`8703324`](https://github.com/python-gitlab/python-gitlab/commit/8703324dc21a30757e15e504b7d20472f25d2ab9))

* feat(namespaces): add support for namespace existence API ([`4882cb2`](https://github.com/python-gitlab/python-gitlab/commit/4882cb22f55c41d8495840110be2d338b5545a04))

* feat: add support for group and project invitations API ([`7afd340`](https://github.com/python-gitlab/python-gitlab/commit/7afd34027a26b5238a979e3303d8e5d8a0320a07))

* feat(projects): add support for project restore API ([`4794ecc`](https://github.com/python-gitlab/python-gitlab/commit/4794ecc45d7aa08785c622918d08bb046e7359ae))

* feat: add support for filtering jobs by scope

See: &#39;scope&#39; here:
https://docs.gitlab.com/ee/api/jobs.html#list-project-jobs ([`0e1c0dd`](https://github.com/python-gitlab/python-gitlab/commit/0e1c0dd795886ae4741136e64c33850b164084a1))

* feat: add `asdict()` and `to_json()` methods to Gitlab Objects

Add an `asdict()` method that returns a dictionary representation copy
of the Gitlab Object. This is a copy and changes made to it will have
no impact on the Gitlab Object.

The `asdict()` method name was chosen as both the `dataclasses` and
`attrs` libraries have an `asdict()` function which has the similar
purpose of creating a dictionary represenation of an object.

Also add a `to_json()` method that returns a JSON string
representation of the object.

Closes: #1116 ([`08ac071`](https://github.com/python-gitlab/python-gitlab/commit/08ac071abcbc28af04c0fa655576e25edbdaa4e2))

* feat(api): add support for instance-level registry repositories ([`284d739`](https://github.com/python-gitlab/python-gitlab/commit/284d73950ad5cf5dfbdec2f91152ed13931bd0ee))

* feat(groups): add support for group-level registry repositories ([`70148c6`](https://github.com/python-gitlab/python-gitlab/commit/70148c62a3aba16dd8a9c29f15ed16e77c01a247))

* feat: Add &#39;merge_pipelines_enabled&#39; project attribute

Boolean. Enable or disable merge pipelines.

See:
https://docs.gitlab.com/ee/api/projects.html#edit-project
https://docs.gitlab.com/ee/ci/pipelines/merged_results_pipelines.html ([`fc33c93`](https://github.com/python-gitlab/python-gitlab/commit/fc33c934d54fb94451bd9b9ad65645c9c3d6fe2e))

* feat: support validating CI lint results ([`3b1ede4`](https://github.com/python-gitlab/python-gitlab/commit/3b1ede4a27cd730982d4c579437c5c689a8799e5))

* feat(cli): add support for global CI lint ([`3f67c4b`](https://github.com/python-gitlab/python-gitlab/commit/3f67c4b0fb0b9a39c8b93529a05b1541fcebcabe))

* feat(objects): add Project CI Lint support

Add support for validating a project&#39;s CI configuration [1]

[1] https://docs.gitlab.com/ee/api/lint.html ([`b213dd3`](https://github.com/python-gitlab/python-gitlab/commit/b213dd379a4108ab32181b9d3700d2526d950916))

* feat: add support for group push rules

Add the GroupPushRules and GroupPushRulesManager classes.

Closes: #1259 ([`b5cdc09`](https://github.com/python-gitlab/python-gitlab/commit/b5cdc097005c8a48a16e793a69c343198b14e035))

* feat(api): add support for `get` for a MR approval rule

In GitLab 14.10 they added support to get a single merge request
approval rule [1]

Add support for it to ProjectMergeRequestApprovalRuleManager

[1] https://docs.gitlab.com/ee/api/merge_request_approvals.html#get-a-single-merge-request-level-rule ([`89c18c6`](https://github.com/python-gitlab/python-gitlab/commit/89c18c6255ec912db319f73f141b47ace87a713b))

### Fix

* fix: support array types for most resources ([`d9126cd`](https://github.com/python-gitlab/python-gitlab/commit/d9126cd802dd3cfe529fa940300113c4ead3054b))

* fix: use the [] after key names for array variables in `params`

1. If a value is of type ArrayAttribute then append &#39;[]&#39; to the name
   of the value for query parameters (`params`).

This is step 3 in a series of steps of our goal to add full
support for the GitLab API data types[1]:
  * array
  * hash
  * array of hashes

Step one was: commit 5127b1594c00c7364e9af15e42d2e2f2d909449b
Step two was: commit a57334f1930752c70ea15847a39324fa94042460

Fixes: #1698

[1] https://docs.gitlab.com/ee/api/#encoding-api-parameters-of-array-and-hash-types ([`1af44ce`](https://github.com/python-gitlab/python-gitlab/commit/1af44ce8761e6ee8a9467a3e192f6c4d19e5cefe))

* fix(runners): fix listing for /runners/all ([`c6dd57c`](https://github.com/python-gitlab/python-gitlab/commit/c6dd57c56e92abb6184badf4708f5f5e65c6d582))

* fix(config): raise error when gitlab id provided but no config section found ([`1ef7018`](https://github.com/python-gitlab/python-gitlab/commit/1ef70188da1e29cd8ba95bf58c994ba7dd3010c5))

* fix(config): raise error when gitlab id provided but no config file found ([`ac46c1c`](https://github.com/python-gitlab/python-gitlab/commit/ac46c1cb291c03ad14bc76f5f16c9f98f2a5a82d))

* fix: add `get_all` param (and `--get-all`) to allow passing `all` to API ([`7c71d5d`](https://github.com/python-gitlab/python-gitlab/commit/7c71d5db1199164b3fa9958e3c3bc6ec96efc78d))

* fix: results returned by `attributes` property to show updates

Previously the `attributes` method would show the original values in a
Gitlab Object even if they had been updated. Correct this so that the
updated value will be returned.

Also use copy.deepcopy() to ensure that modifying the dictionary returned can
not also modify the object. ([`e5affc8`](https://github.com/python-gitlab/python-gitlab/commit/e5affc8749797293c1373c6af96334f194875038))

* fix: Enable epic notes

Add the notes attribute to GroupEpic ([`5fc3216`](https://github.com/python-gitlab/python-gitlab/commit/5fc3216788342a2325662644b42e8c249b655ded))

* fix(cli): remove irrelevant MR approval rule list filters ([`0daec5f`](https://github.com/python-gitlab/python-gitlab/commit/0daec5fa1428a56a6a927b133613e8b296248167))

* fix: ensure path elements are escaped

Ensure the path elements that are passed to the server are escaped.
For example a &#34;/&#34; will be changed to &#34;%2F&#34;

Closes: #2116 ([`5d9c198`](https://github.com/python-gitlab/python-gitlab/commit/5d9c198769b00c8e7661e62aaf5f930ed32ef829))

### Refactor

* refactor: migrate services to integrations ([`a428051`](https://github.com/python-gitlab/python-gitlab/commit/a4280514546cc6e39da91d1671921b74b56c3283))

* refactor(objects): move ci lint to separate file ([`6491f1b`](https://github.com/python-gitlab/python-gitlab/commit/6491f1bbb68ffe04c719eb9d326b7ca3e78eba84))

* refactor(test-projects): apply suggestions and use fixtures ([`a51f848`](https://github.com/python-gitlab/python-gitlab/commit/a51f848db4204b2f37ae96fd235ae33cb7c2fe98))

* refactor(test-projects): remove test_restore_project ([`9be0875`](https://github.com/python-gitlab/python-gitlab/commit/9be0875c3793324b4c4dde29519ee62b39a8cc18))

### Test

* test(cli): add tests for token scopes ([`263fe3d`](https://github.com/python-gitlab/python-gitlab/commit/263fe3d24836b34dccdcee0221bd417e0b74fb2e))

* test: add test to show issue fixed

https://github.com/python-gitlab/python-gitlab/issues/1698 has been
fixed. Add test to show that. ([`75bec7d`](https://github.com/python-gitlab/python-gitlab/commit/75bec7d543dd740c50452b21b0b4509377cd40ce))

* test: always ensure clean config environment ([`8d4f13b`](https://github.com/python-gitlab/python-gitlab/commit/8d4f13b192afd5d4610eeaf2bbea71c3b6a25964))

* test(ee): add an EE specific test ([`10987b3`](https://github.com/python-gitlab/python-gitlab/commit/10987b3089d4fe218dd2116dd871e0a070db3f7f))

* test(functional): simplify token creation ([`67ab24f`](https://github.com/python-gitlab/python-gitlab/commit/67ab24fe5ae10a9f8cc9122b1a08848e8927635d))

* test: fix broken test if user had config files

Use `monkeypatch` to ensure that no config files are reported for the
test.

Closes: #2172 ([`864fc12`](https://github.com/python-gitlab/python-gitlab/commit/864fc1218e6366b9c1d8b1b3832e06049c238d8c))

* test: allow `podman` users to run functional tests

Users of `podman` will likely have `DOCKER_HOST` set to something like
`unix:///run/user/1000/podman/podman.sock`

Pass this environment variable so that it will be used during the
functional tests. ([`ff215b7`](https://github.com/python-gitlab/python-gitlab/commit/ff215b7056ce2adf2b85ecc1a6c3227d2b1a5277))

* test(api_func_v4): catch deprecation warning for `gl.lint()`

Catch the deprecation warning for the call to `gl.lint()`, so it won&#39;t
show up in the log. ([`95fe924`](https://github.com/python-gitlab/python-gitlab/commit/95fe9247fcc9cba65c4afef934f816be06027ff5))

* test(functional): use both get_all and all in list() tests ([`201298d`](https://github.com/python-gitlab/python-gitlab/commit/201298d7b5795b7d7338793da8033dc6c71d6572))

* test: add more tests for container registries ([`f6b6e18`](https://github.com/python-gitlab/python-gitlab/commit/f6b6e18f96f4cdf67c8c53ae79e6a8259dcce9ee))

* test(functional): replace len() calls with list membership checks ([`97e0eb9`](https://github.com/python-gitlab/python-gitlab/commit/97e0eb9267202052ed14882258dceca0f6c4afd7))

* test(projects): add unit tests for projects ([`67942f0`](https://github.com/python-gitlab/python-gitlab/commit/67942f0d46b7d445f28f80d3f57aa91eeea97a24))

### Unknown

* Merge pull request #2198 from nickbroon/nickbroon-release-sort-order

feat: allow sort/ordering for project releases ([`c33cb20`](https://github.com/python-gitlab/python-gitlab/commit/c33cb20320e4b88bbf9ce994420d7daa69e7fc7f))

* Merge pull request #2195 from python-gitlab/jlvillal/array_test

test: add test to show issue fixed ([`1cf5932`](https://github.com/python-gitlab/python-gitlab/commit/1cf59323194b2352bd1c1313415cd09bbdddcc5f))

* Merge pull request #1699 from python-gitlab/jlvillal/arrays

fix: use the [] after key names for array variables in `params` ([`510ec30`](https://github.com/python-gitlab/python-gitlab/commit/510ec30f30e7ff8466b58d2661b67076de9d234b))

* Merge pull request #1778 from python-gitlab/jlvillal/gitlab-ee

chore: enable using GitLab EE in functional tests ([`b661003`](https://github.com/python-gitlab/python-gitlab/commit/b6610033d956d40e31575bf4aef69693d06f8b01))

* Merge pull request #2184 from python-gitlab/renovate/commitizen-tools-commitizen-2.x

chore(deps): update pre-commit hook commitizen-tools/commitizen to v2.29.0 ([`346cf76`](https://github.com/python-gitlab/python-gitlab/commit/346cf76b381ab1ea0c2c42885fedc41f8c5716b0))

* Merge pull request #2182 from python-gitlab/renovate/commitizen-2.x

chore(deps): update dependency commitizen to v2.29.0 ([`e2ca0b4`](https://github.com/python-gitlab/python-gitlab/commit/e2ca0b4956cacffb802a4594241dbd95f65e9906))

* Merge pull request #2173 from python-gitlab/jlvillal/config_test_fix

test: fix broken test if user had config files ([`1ecbc7c`](https://github.com/python-gitlab/python-gitlab/commit/1ecbc7c89b2d8104bd3dd3045ff551e808f06aac))

* Merge pull request #2166 from python-gitlab/jlvillal/podman

test: allow `podman` users to run functional tests ([`0b02b95`](https://github.com/python-gitlab/python-gitlab/commit/0b02b95c14ddea2f6b869b3150670f85af3839b6))

* Merge pull request #1785 from python-gitlab/jlvillal/reset_gitlab

chore: make reset_gitlab() better ([`789ef81`](https://github.com/python-gitlab/python-gitlab/commit/789ef81585942dd6b935ffe58630025a19436a46))

* Merge pull request #1784 from python-gitlab/jlvillal/sidekiq

chore: fixtures: after delete() wait to verify deleted ([`916b1db`](https://github.com/python-gitlab/python-gitlab/commit/916b1db28c6c18d6a8d419e7e88f2d8eb1531083))

* Merge pull request #2163 from python-gitlab/jlvillal/lint_warning

test(api_func_v4): catch deprecation warning for `gl.lint()` ([`1855279`](https://github.com/python-gitlab/python-gitlab/commit/1855279cf76b46aeebc908cfe6af81f7cb5b6e3f))

* Merge pull request #2161 from nickbroon/nickbroon-jobs_scope

feat: add support for filtering jobs by scope ([`0549afa`](https://github.com/python-gitlab/python-gitlab/commit/0549afa6631f21ab98e1f1457607daa03b398185))

* Merge pull request #2160 from python-gitlab/docs-author-add-john

docs(authors): add John ([`ead9f15`](https://github.com/python-gitlab/python-gitlab/commit/ead9f15819f7b04f9c6c85792558eff17c988ee3))

* Merge pull request #1872 from python-gitlab/jlvillal/as_dict

 feat: add `asdict()` and `to_json()` methods to Gitlab Objects ([`fcbced8`](https://github.com/python-gitlab/python-gitlab/commit/fcbced88025dcf2ff980104bec1d48df3258bc7c))

* Merge pull request #2082 from python-gitlab/jlvillal/mark_lazy_state

chore: add a `lazy` boolean attribute to `RESTObject` ([`2c90fd0`](https://github.com/python-gitlab/python-gitlab/commit/2c90fd0f317213a5a29bf6a2b63715a287e9fcfa))

* Merge pull request #2146 from python-gitlab/jlvillal/mypy_strict_step_by_step

chore: enable mypy check `strict_equality` ([`c84379d`](https://github.com/python-gitlab/python-gitlab/commit/c84379d1c9a681516585dc077ec1a237468b4991))

* Merge pull request #2147 from python-gitlab/jlvillal/api_func_v4

chore: change name of API functional test to `api_func_v4` ([`ed110bd`](https://github.com/python-gitlab/python-gitlab/commit/ed110bd131fd330e20ec55915b9452dbf8002e0b))

* Merge pull request #2141 from nickbroon/nickbroon-merge_pipelines_enabled

feat: Add &#39;merge_pipelines_enabled&#39; project attribute ([`e409811`](https://github.com/python-gitlab/python-gitlab/commit/e409811c8524bd7fa4bcee883c3b0e9b8096b184))

* Merge pull request #2125 from python-gitlab/jlvillal/user_docs

docs(users): add docs about listing a user&#39;s projects ([`1fbfb22`](https://github.com/python-gitlab/python-gitlab/commit/1fbfb224388c107ada9c741e88193179eab3f23c))

* Merge pull request #1896 from python-gitlab/jlvillal/ci_lint

feat: add Project CI Lint support ([`d15fea0`](https://github.com/python-gitlab/python-gitlab/commit/d15fea0ccf44732a2462fc7c63a97495efeb9f99))

* Merge pull request #2126 from python-gitlab/jlvillal/push_rules

docs: update return type of pushrules ([`88a1535`](https://github.com/python-gitlab/python-gitlab/commit/88a1535cbbd73a66493a6263c8e549158a6ee171))

* Merge pull request #1266 from gokeefe/gokeefe/group_push_rules

#1259 Add GroupPushRules and GroupPushRulesManager classes ([`768890a`](https://github.com/python-gitlab/python-gitlab/commit/768890a4c99928a0781c611c089e7cb5da5971a6))

* Merge pull request #2114 from python-gitlab/jlvillal/remove_trys

chore: simplify multi-nested try blocks ([`3df404c`](https://github.com/python-gitlab/python-gitlab/commit/3df404c8165c36486bbcdf03816bd0b3173d9de8))

* Merge pull request #2117 from python-gitlab/jlvillal/encodedid_path

fix: ensure path elements are escaped ([`04c6063`](https://github.com/python-gitlab/python-gitlab/commit/04c6063183d94fe8970bdad485cf8221db9c31a8))

* Merge pull request #2113 from tuxiqae/patch-1

Remove redundant `-v` that breaks the command ([`ca3b438`](https://github.com/python-gitlab/python-gitlab/commit/ca3b43892996890d9c976409393ee39f66c41b75))

* Merge pull request #2069 from antoineauger/test/unit-tests-projects

test(projects): add unit tests for projects ([`0e4db56`](https://github.com/python-gitlab/python-gitlab/commit/0e4db56ca694d210ad55dff8da7c7f0e62a509eb))

* Merge pull request #2110 from python-gitlab/jlvillal/mr_approval_rules

feat(api): add support for `get` for a MR approval rule ([`389e1e6`](https://github.com/python-gitlab/python-gitlab/commit/389e1e61266256983452c821cdff939bfe59925b))

* Merge pull request #2111 from python-gitlab/jlvillal/meta_fix

chore: fix misspelling ([`6486566`](https://github.com/python-gitlab/python-gitlab/commit/64865662c6e9024207b5bf197dc81782e22d2741))

* Merge pull request #2112 from python-gitlab/jlvillal/doc_remove_tabs

chore(docs): convert tabs to spaces ([`8771ad8`](https://github.com/python-gitlab/python-gitlab/commit/8771ad8ff3391ce42440fcb8df8da5dbe346e09e))

## v3.6.0 (2022-06-28)

### Chore

* chore(deps): ignore python-semantic-release updates ([`f185b17`](https://github.com/python-gitlab/python-gitlab/commit/f185b17ff5aabedd32d3facd2a46ebf9069c9692))

* chore(workflows): explicitly use python-version ([`eb14475`](https://github.com/python-gitlab/python-gitlab/commit/eb1447588dfbbdfe724fca9009ea5451061b5ff0))

* chore(deps): update actions/setup-python action to v4 ([`77c1f03`](https://github.com/python-gitlab/python-gitlab/commit/77c1f0352adc8488041318e5dfd2fa98a5b5af62))

* chore(deps): update typing dependencies ([`acc5c39`](https://github.com/python-gitlab/python-gitlab/commit/acc5c3971f13029288dff2909692a0171f4a66f7))

* chore(deps): update pre-commit hook pycqa/pylint to v2.14.3 ([`d1fe838`](https://github.com/python-gitlab/python-gitlab/commit/d1fe838b65ccd1a68fb6301bbfd06cd19425a75c))

* chore(ci): increase timeout for docker container to come online

Have been seeing timeout issues more and more. Increase timeout from
200 seconds to 300 seconds (5 minutes). ([`bda020b`](https://github.com/python-gitlab/python-gitlab/commit/bda020bf5f86d20253f39698c3bb32f8d156de60))

* chore(docs): ignore nitpicky warnings ([`1c3efb5`](https://github.com/python-gitlab/python-gitlab/commit/1c3efb50bb720a87b95307f4d6642e3b7f28f6f0))

* chore: patch sphinx for explicit re-exports ([`06871ee`](https://github.com/python-gitlab/python-gitlab/commit/06871ee05b79621f0a6fea47243783df105f64d6))

* chore: bump mypy pre-commit hook ([`0bbcad7`](https://github.com/python-gitlab/python-gitlab/commit/0bbcad7612f60f7c7b816c06a244ad8db9da68d9))

* chore(gitlab): fix implicit re-exports for mpypy ([`981b844`](https://github.com/python-gitlab/python-gitlab/commit/981b8448dbadc63d70867dc069e33d4c4d1cfe95))

* chore: add link to Commitizen in Github workflow

Add a link to the Commitizen website in the Github workflow. Hopefully
this will help people when their job fails. ([`d08d07d`](https://github.com/python-gitlab/python-gitlab/commit/d08d07deefae345397fc30280c4f790c7e61cbe2))

* chore(deps): update dependency pylint to v2.14.3 ([`9a16bb1`](https://github.com/python-gitlab/python-gitlab/commit/9a16bb158f3cb34a4c4cb7451127fbc7c96642e2))

* chore: fix issue found with pylint==2.14.3

A new error was reported when running pylint==2.14.3:
  gitlab/client.py:488:0: W1404: Implicit string concatenation found in call (implicit-str-concat)

Fixed this issue. ([`eeab035`](https://github.com/python-gitlab/python-gitlab/commit/eeab035ab715e088af73ada00e0a3b0c03527187))

* chore(deps): update pre-commit hook commitizen-tools/commitizen to v2.27.1 ([`22c5db4`](https://github.com/python-gitlab/python-gitlab/commit/22c5db4bcccf592f5cf7ea34c336208c21769896))

* chore(deps): update dependency requests to v2.28.0 ([`d361f4b`](https://github.com/python-gitlab/python-gitlab/commit/d361f4bd4ec066452a75cf04f64334234478bb02))

* chore(deps): update dependency mypy to v0.961 ([`f117b2f`](https://github.com/python-gitlab/python-gitlab/commit/f117b2f92226a507a8adbb42023143dac0cc07fc))

* chore(deps): update typing dependencies ([`aebf9c8`](https://github.com/python-gitlab/python-gitlab/commit/aebf9c83a4cbf7cf4243cb9b44375ca31f9cc878))

* chore(deps): update dependency mypy to v0.960 ([`8c016c7`](https://github.com/python-gitlab/python-gitlab/commit/8c016c7a53c543d07d16153039053bb370a6945b))

* chore(cli): rename &#34;object&#34; to &#34;GitLab resource&#34;

Make the parser name more user friendly by renaming from generic
&#34;object&#34; to &#34;GitLab resource&#34; ([`62e64a6`](https://github.com/python-gitlab/python-gitlab/commit/62e64a66dab4b3704d80d19a5dbc68b025b18e3c))

* chore: use multiple processors when running PyLint

Use multiple processors when running PyLint. On my system it took
about 10.3 seconds to run PyLint before this change. After this change
it takes about 5.8 seconds to run PyLint. ([`7f2240f`](https://github.com/python-gitlab/python-gitlab/commit/7f2240f1b9231e8b856706952ec84234177a495b))

* chore: enable pylint check: &#34;redefined-outer-name&#34;,

Enable the pylint check &#34;redefined-outer-name&#34; and fix the errors
detected. ([`1324ce1`](https://github.com/python-gitlab/python-gitlab/commit/1324ce1a439befb4620953a4df1f70b74bf70cbd))

* chore: enable pylint check: &#34;no-self-use&#34;

Enable the pylint check &#34;no-self-use&#34; and fix the errors detected. ([`80aadaf`](https://github.com/python-gitlab/python-gitlab/commit/80aadaf4262016a8181b5150ca7e17c8139c15fa))

* chore: enable pylint check: &#34;no-else-return&#34;

Enable the pylint check &#34;no-else-return&#34; and fix the errors detected. ([`d0b0811`](https://github.com/python-gitlab/python-gitlab/commit/d0b0811211f69f08436dcf7617c46617fe5c0b8b))

* chore: enable pylint check: &#34;attribute-defined-outside-init&#34;

Enable the pylint check: &#34;attribute-defined-outside-init&#34; and fix
errors detected. ([`d6870a9`](https://github.com/python-gitlab/python-gitlab/commit/d6870a981259ee44c64210a756b63dc19a6f3957))

* chore: enable pylint check &#34;raise-missing-from&#34;

Enable the pylint check &#34;raise-missing-from&#34; and fix errors detected. ([`1a2781e`](https://github.com/python-gitlab/python-gitlab/commit/1a2781e477471626e2b00129bef5169be9c7cc06))

* chore: enable pylint checks which require no changes

Enabled the pylint checks that don&#39;t require any code changes.
Previously these checks were disabled. ([`50fdbc4`](https://github.com/python-gitlab/python-gitlab/commit/50fdbc474c524188952e0ef7c02b0bd92df82357))

* chore: enable pylint checks

Enable the pylint checks:
  * unnecessary-pass
  * unspecified-encoding

Update code to resolve errors found ([`1e89164`](https://github.com/python-gitlab/python-gitlab/commit/1e8916438f7c4f67bd7745103b870d84f6ba2d01))

* chore: rename `whaction` and `action` to `resource_action` in CLI

Rename the variables `whaction` and `action` to `resource_action` to
improve code-readability. ([`fb3f28a`](https://github.com/python-gitlab/python-gitlab/commit/fb3f28a053f0dcf0a110bb8b6fd11696b4ba3dd9))

* chore: rename `what` to `gitlab_resource`

Naming a variable `what` makes it difficult to understand what it is
used for.

Rename it to `gitlab_resource` as that is what is being stored.

The Gitlab documentation talks about them being resources:
https://docs.gitlab.com/ee/api/api_resources.html

This will improve code readability. ([`c86e471`](https://github.com/python-gitlab/python-gitlab/commit/c86e471dead930468172f4b7439ea6fa207f12e8))

* chore: rename `__call__()` to `run()` in GitlabCLI

Less confusing to have it be a normal method. ([`6189437`](https://github.com/python-gitlab/python-gitlab/commit/6189437d2c8d18f6c7d72aa7743abd6d36fb4efa))

* chore: enable &#39;consider-using-sys-exit&#39; pylint check

Enable the &#39;consider-using-sys-exit&#39; pylint check and fix errors
raised. ([`0afcc3e`](https://github.com/python-gitlab/python-gitlab/commit/0afcc3eca4798801ff3635b05b871e025078ef31))

* chore: require f-strings

We previously converted all string formatting to use f-strings. Enable
pylint check to enforce this. ([`96e994d`](https://github.com/python-gitlab/python-gitlab/commit/96e994d9c5c1abd11b059fe9f0eec7dac53d2f3a))

* chore(ci): pin 3.11 to beta.1 ([`7119f2d`](https://github.com/python-gitlab/python-gitlab/commit/7119f2d228115fe83ab23612e189c9986bb9fd1b))

* chore(cli): ignore coverage on exceptions triggering cli.die ([`98ccc3c`](https://github.com/python-gitlab/python-gitlab/commit/98ccc3c2622a3cdb24797fd8790e921f5f2c1e6a))

* chore: move `utils._validate_attrs` inside `types.RequiredOptional`

Move the `validate_attrs` function to be inside the `RequiredOptional`
class. It makes sense for it to be part of the class as it is working
on data related to the class. ([`9d629bb`](https://github.com/python-gitlab/python-gitlab/commit/9d629bb97af1e14ce8eb4679092de2393e1e3a05))

* chore: remove use of &#39;%&#39; string formatter in `gitlab/utils.py`

Replace usage with f-string ([`0c5a121`](https://github.com/python-gitlab/python-gitlab/commit/0c5a1213ba3bb3ec4ed5874db4588d21969e9e80))

* chore: have `EncodedId` creation always return `EncodedId`

There is no reason to return an `int` as we can always return a `str`
version of the `int`

Change `EncodedId` to always return an `EncodedId`. This removes the
need to have `mypy` ignore the error raised. ([`a1a246f`](https://github.com/python-gitlab/python-gitlab/commit/a1a246fbfcf530732249a263ee42757a862181aa))

* chore: move `RequiredOptional` to the `gitlab.types` module

By having `RequiredOptional` in the `gitlab.base` module it makes it
difficult with circular imports. Move it to the `gitlab.types`
module which has no dependencies on any other gitlab module. ([`7d26530`](https://github.com/python-gitlab/python-gitlab/commit/7d26530640eb406479f1604cb64748d278081864))

* chore: update type-hints return signature for GetWithoutIdMixin methods

Commit f0152dc3cc9a42aa4dc3c0014b4c29381e9b39d6 removed situation
where `get()` in a `GetWithoutIdMixin` based class could return `None`

Update the type-hints to no longer return `Optional` AKA `None` ([`aa972d4`](https://github.com/python-gitlab/python-gitlab/commit/aa972d49c57f2ebc983d2de1cfb8d18924af6734))

* chore: correct ModuleNotFoundError() arguments

Previously in commit 233b79ed442aac66faf9eb4b0087ea126d6dffc5 I had
used the `name` argument for `ModuleNotFoundError()`. This basically
is the equivalent of not passing any message to
`ModuleNotFoundError()`. So when the exception was raised it wasn&#39;t
very helpful.

Correct that and add a unit-test that shows we get the message we
expect. ([`0b7933c`](https://github.com/python-gitlab/python-gitlab/commit/0b7933c5632c2f81c89f9a97e814badf65d1eb38))

* chore(deps): update typing dependencies ([`f3f79c1`](https://github.com/python-gitlab/python-gitlab/commit/f3f79c1d3afa923405b83dcea905fec213201452))

* chore(deps): update dependency commitizen to v2.27.1 ([`456f9f1`](https://github.com/python-gitlab/python-gitlab/commit/456f9f14453f2090fdaf88734fe51112bf4e7fde))

* chore(mixins): remove None check as http_get always returns value ([`f0152dc`](https://github.com/python-gitlab/python-gitlab/commit/f0152dc3cc9a42aa4dc3c0014b4c29381e9b39d6))

### Documentation

* docs(api): add separate section for advanced usage ([`22ae101`](https://github.com/python-gitlab/python-gitlab/commit/22ae1016f39256b8e2ca02daae8b3c7130aeb8e6))

* docs(api): document usage of head() methods ([`f555bfb`](https://github.com/python-gitlab/python-gitlab/commit/f555bfb363779cc6c8f8036f6d6cfa302e15d4fe))

* docs(projects): provide more detailed import examples ([`8f8611a`](https://github.com/python-gitlab/python-gitlab/commit/8f8611a1263b8c19fd19ce4a904a310b0173b6bf))

* docs(projects): document 404 gotcha with unactivated integrations ([`522ecff`](https://github.com/python-gitlab/python-gitlab/commit/522ecffdb6f07e6c017139df4eb5d3fc42a585b7))

* docs(variables): instruct users to follow GitLab rules for values ([`194b6be`](https://github.com/python-gitlab/python-gitlab/commit/194b6be7ccec019fefc04754f98b9ec920c29568))

* docs(api): stop linking to python-requests.org ([`49c7e83`](https://github.com/python-gitlab/python-gitlab/commit/49c7e83f768ee7a3fec19085a0fa0a67eadb12df))

* docs(api): fix incorrect docs for merge_request_approvals (#2094)

* docs(api): fix incorrect docs for merge_request_approvals

The `set_approvers()` method is on the `ProjectApprovalManager` class.
It is not part of the `ProjectApproval` class.

The docs were previously showing to call `set_approvers` using a
`ProjectApproval` instance, which would fail. Correct the
documentation.

This was pointed out by a question on the Gitter channel.

Co-authored-by: Nejc Habjan &lt;nejc.habjan@siemens.com&gt; ([`5583eaa`](https://github.com/python-gitlab/python-gitlab/commit/5583eaa108949386c66290fecef4d064f44b9e83))

* docs(api-usage): add import os in example ([`2194a44`](https://github.com/python-gitlab/python-gitlab/commit/2194a44be541e9d2c15d3118ba584a4a173927a2))

* docs: drop deprecated setuptools build_sphinx ([`048d66a`](https://github.com/python-gitlab/python-gitlab/commit/048d66af51cef385b22d223ed2a5cd30e2256417))

* docs(usage): refer to upsteam docs instead of custom attributes ([`ae7d3b0`](https://github.com/python-gitlab/python-gitlab/commit/ae7d3b09352b2a1bd287f95d4587b04136c7a4ed))

* docs(ext): fix rendering for RequiredOptional dataclass ([`4d431e5`](https://github.com/python-gitlab/python-gitlab/commit/4d431e5a6426d0fd60945c2d1ff00a00a0a95b6c))

* docs: documentation updates to reflect addition of mutually exclusive attributes ([`24b720e`](https://github.com/python-gitlab/python-gitlab/commit/24b720e49636044f4be7e4d6e6ce3da341f2aeb8))

* docs: use `as_list=False` or `all=True` in Getting started

In the &#34;Getting started with the API&#34; section of the documentation,
use either `as_list=False` or `all=True` in the example usages of the
`list()` method.

Also add a warning about the fact that `list()` by default does not
return all items. ([`de8c6e8`](https://github.com/python-gitlab/python-gitlab/commit/de8c6e80af218d93ca167f8b5ff30319a2781d91))

### Feature

* feat(downloads): allow streaming downloads access to response iterator (#1956)

* feat(downloads): allow streaming downloads access to response iterator

Allow access to the underlying response iterator when downloading in
streaming mode by specifying `iterator=True`.

Update type annotations to support this change.

* docs(api-docs): add iterator example to artifact download

Document the usage of the `iterator=True` option when downloading
artifacts

* test(packages): add tests for streaming downloads ([`b644721`](https://github.com/python-gitlab/python-gitlab/commit/b6447211754e126f64e12fc735ad74fe557b7fb4))

* feat(users): add approve and reject methods to User

As requested in #1604.

Co-authored-by: John Villalovos &lt;john@sodarock.com&gt; ([`f57139d`](https://github.com/python-gitlab/python-gitlab/commit/f57139d8f1dafa6eb19d0d954b3634c19de6413c))

* feat(api): support head() method for get and list endpoints ([`ce9216c`](https://github.com/python-gitlab/python-gitlab/commit/ce9216ccc542d834be7f29647c7ee98c2ca5bb01))

* feat(api): implement HEAD method ([`90635a7`](https://github.com/python-gitlab/python-gitlab/commit/90635a7db3c9748745471d2282260418e31c7797))

* feat(api): convert gitlab.const to Enums

This allows accessing the elements by value, i.e.:

import gitlab.const
gitlab.const.AccessLevel(20) ([`c3c6086`](https://github.com/python-gitlab/python-gitlab/commit/c3c6086c548c03090ccf3f59410ca3e6b7999791))

* feat: Add support for Protected Environments

- https://docs.gitlab.com/ee/api/protected_environments.html
- https://github.com/python-gitlab/python-gitlab/issues/1130

no write operation are implemented yet as I have no use case right now
and am not sure how it should be done ([`1dc9d0f`](https://github.com/python-gitlab/python-gitlab/commit/1dc9d0f91757eed9f28f0c7172654b9b2a730216))

* feat(users): add ban and unban methods ([`0d44b11`](https://github.com/python-gitlab/python-gitlab/commit/0d44b118f85f92e7beb1a05a12bdc6e070dce367))

* feat(docker): provide a Debian-based slim image ([`384031c`](https://github.com/python-gitlab/python-gitlab/commit/384031c530e813f55da52f2b2c5635ea935f9d91))

* feat: support mutually exclusive attributes and consolidate validation to fix board lists (#2037)

add exclusive tuple to RequiredOptional data class to support for
mutually exclusive attributes

consolidate _check_missing_create_attrs and _check_missing_update_attrs
from mixins.py into _validate_attrs in utils.py

change _create_attrs in board list manager classes from
required=(&#39;label_ld&#39;,) to
exclusive=(&#39;label_id&#39;,&#39;asignee_id&#39;,&#39;milestone_id&#39;)

closes https://github.com/python-gitlab/python-gitlab/issues/1897 ([`3fa330c`](https://github.com/python-gitlab/python-gitlab/commit/3fa330cc341bbedb163ba757c7f6578d735c6efb))

* feat(client): introduce `iterator=True` and deprecate `as_list=False` in `list()`

`as_list=False` is confusing as it doesn&#39;t explain what is being
returned. Replace it with `iterator=True` which more clearly explains
to the user that an iterator/generator will be returned.

This maintains backward compatibility with `as_list` but does issue a
DeprecationWarning if `as_list` is set. ([`cdc6605`](https://github.com/python-gitlab/python-gitlab/commit/cdc6605767316ea59e1e1b849683be7b3b99e0ae))

### Fix

* fix(base): do not fail repr() on lazy objects ([`1efb123`](https://github.com/python-gitlab/python-gitlab/commit/1efb123f63eab57600228b75a1744f8787c16671))

* fix(cli): project-merge-request-approval-rule

Using the CLI the command:
   gitlab project-merge-request-approval-rule list --mr-iid 1 --project-id foo/bar

Would raise an exception. This was due to the fact that `_id_attr` and
`_repr_attr` were set for keys which are not returned in the response.

Add a unit test which shows the `repr` function now works. Before it
did not.

This is an EE feature so we can&#39;t functional test it.

Closes: #2065 ([`15a242c`](https://github.com/python-gitlab/python-gitlab/commit/15a242c3303759b77b380c5b3ff9d1e0bf2d800c))

* fix(cli): fix project export download for CLI

Since ac1c619cae6481833f5df91862624bf0380fef67 we delete parent arg keys
from the args dict so this has been trying to access the wrong attribute. ([`5d14867`](https://github.com/python-gitlab/python-gitlab/commit/5d1486785793b02038ac6f527219801744ee888b))

### Refactor

* refactor: do not recommend plain gitlab.const constants ([`d652133`](https://github.com/python-gitlab/python-gitlab/commit/d65213385a6f497c2595d3af3a41756919b9c9a1))

* refactor: avoid possible breaking change in iterator (#2107)

Commit b6447211754e126f64e12fc735ad74fe557b7fb4 inadvertently
introduced a possible breaking change as it added a new argument
`iterator` and added it in between existing (potentially positional) arguments.

This moves the `iterator` argument to the end of the argument list and
requires it to be a keyword-only argument. ([`212ddfc`](https://github.com/python-gitlab/python-gitlab/commit/212ddfc9e9c5de50d2507cc637c01ceb31aaba41))

* refactor: remove no-op id argument in GetWithoutIdMixin ([`0f2a602`](https://github.com/python-gitlab/python-gitlab/commit/0f2a602d3a9d6579f5fdfdf945a236ae44e93a12))

* refactor(mixins): extract custom type transforms into utils ([`09b3b22`](https://github.com/python-gitlab/python-gitlab/commit/09b3b2225361722f2439952d2dbee6a48a9f9fd9))

### Test

* test: add tests and clean up usage for new enums ([`323ab3c`](https://github.com/python-gitlab/python-gitlab/commit/323ab3c5489b0d35f268bc6c22ade782cade6ba4))

* test(pylint): enable pylint &#34;unused-argument&#34; check

Enable the pylint &#34;unused-argument&#34; check and resolve issues it found.

  * Quite a few functions were accepting `**kwargs` but not then
    passing them on through to the next level. Now pass `**kwargs` to
    next level.
  * Other functions had no reason to accept `**kwargs`, so remove it
  * And a few other fixes. ([`23feae9`](https://github.com/python-gitlab/python-gitlab/commit/23feae9b0906d34043a784a01d31d1ff19ebc9a4))

* test(api): add tests for HEAD method ([`b0f02fa`](https://github.com/python-gitlab/python-gitlab/commit/b0f02facef2ea30f24dbfb3c52974f34823e9bba))

* test: add more tests for RequiredOptional ([`ce40fde`](https://github.com/python-gitlab/python-gitlab/commit/ce40fde9eeaabb4a30c5a87d9097b1d4eced1c1b))

* test: move back to using latest Python 3.11 version ([`8c34781`](https://github.com/python-gitlab/python-gitlab/commit/8c347813e7aaf26a33fe5ae4ae73448beebfbc6c))

* test: increase client coverage ([`00aec96`](https://github.com/python-gitlab/python-gitlab/commit/00aec96ed0b60720362c6642b416567ff39aef09))

* test(cli): improve coverage for custom actions ([`7327f78`](https://github.com/python-gitlab/python-gitlab/commit/7327f78073caa2fb8aaa6bf0e57b38dd7782fa57))

* test(gitlab): increase unit test coverage ([`df072e1`](https://github.com/python-gitlab/python-gitlab/commit/df072e130aa145a368bbdd10be98208a25100f89))

### Unknown

* Merge pull request #2105 from python-gitlab/renovate/actions-setup-python-4.x

chore(deps): update actions/setup-python action to v4 ([`ebd5795`](https://github.com/python-gitlab/python-gitlab/commit/ebd579588d05966ee66cce014b141e6ab39435cc))

* Merge pull request #2100 from python-gitlab/jlvillal/pylint_2022-06-26

test(pylint): enable pylint &#34;unused-argument&#34; check ([`3c3f865`](https://github.com/python-gitlab/python-gitlab/commit/3c3f8657a63276280ad971cc73ca8d8240704b2c))

* Merge pull request #2061 from bgamari/patch-1

feat(users): add approve and reject methods to User ([`f9b7c7b`](https://github.com/python-gitlab/python-gitlab/commit/f9b7c7b5c1c5782ffe1cec19420f3484681e1a67))

* Merge pull request #2089 from python-gitlab/jlvillal/more_time

chore(ci): increase timeout for docker container to come online ([`a825844`](https://github.com/python-gitlab/python-gitlab/commit/a825844e1f6a5aa7c35df90f1891d2ef91ffe4a8))

* Merge pull request #1688 from jspricke/enum

feat(api): Convert gitlab.const to Enums ([`f0ac3cd`](https://github.com/python-gitlab/python-gitlab/commit/f0ac3cda2912509d0a3132be8344e41ddcec71ab))

* Merge pull request #2084 from calve/protected-environments

feat: Add support for Protected Environments ([`1feabc0`](https://github.com/python-gitlab/python-gitlab/commit/1feabc08171afaa08cea3545eb70c169231ab5d1))

* Merge pull request #2083 from python-gitlab/jlvillal/cz

chore: add link to Commitizen in Github workflow ([`8342f53`](https://github.com/python-gitlab/python-gitlab/commit/8342f53854c0accf5bc8ce9a9be64a5f335eed07))

* Merge pull request #2066 from python-gitlab/jlvillal/approval_rule_id

fix(cli): project-merge-request-approval-rule ([`41ceaca`](https://github.com/python-gitlab/python-gitlab/commit/41ceaca1cdee6251beb453f22b7def3c95b279a5))

* Merge pull request #2076 from python-gitlab/renovate/pylint-2.x

chore(deps): update dependency pylint to v2.14.3 ([`e48ad91`](https://github.com/python-gitlab/python-gitlab/commit/e48ad91cbd7ee40f3d21e11700e22a754e14e31e))

* Merge pull request #2077 from python-gitlab/jlvillal/pylint

chore: fix issue found with pylint==2.14.3 ([`8e0cd8b`](https://github.com/python-gitlab/python-gitlab/commit/8e0cd8b398f5fd58554bf873b48428b4781eaa47))

* Merge pull request #2064 from antoineauger/feat/user-ban-unban

feat(users): add ban and unban methods ([`ca98d88`](https://github.com/python-gitlab/python-gitlab/commit/ca98d88fd3634eefc81b0b1e1eb723e0d99cf840))

* Merge pull request #2057 from walterrowe/main

docs: update docs to reflect addition of mutually exclusive attributes ([`0f607f6`](https://github.com/python-gitlab/python-gitlab/commit/0f607f685b1e766cee4322c239c9a44ae93072f2))

* Merge pull request #2055 from python-gitlab/jlvillal/resource

chore(cli): rename &#34;object&#34; to &#34;GitLab resource&#34; ([`0e3c461`](https://github.com/python-gitlab/python-gitlab/commit/0e3c461a2ad6ade9819db864261a82b357ce5808))

* Merge pull request #2045 from python-gitlab/jlvillal/test_validate_attrs

test: add more tests for RequiredOptional ([`40c9b4f`](https://github.com/python-gitlab/python-gitlab/commit/40c9b4f299d3c101bda7fabc89a42ff0f1f0ddc2))

* Merge pull request #2056 from python-gitlab/jlvillal/pylint_job

chore: use multiple processors when running PyLint ([`7b9bb3c`](https://github.com/python-gitlab/python-gitlab/commit/7b9bb3c920e99d1efaa495de47c2be929d62ee74))

* Merge pull request #2051 from python-gitlab/jlvillal/more_more_pylint

chore: enable more pylint checks ([`7a5923c`](https://github.com/python-gitlab/python-gitlab/commit/7a5923c8e77a41cb829a086a903aee4123ca4d14))

* Merge pull request #2054 from python-gitlab/jlvillal/resource

chore: rename `whaction` and `action` to `resource_action` in CLI ([`61b8beb`](https://github.com/python-gitlab/python-gitlab/commit/61b8beb8bed0a9d7cd30450fefba0dd76c0d35d6))

* Merge pull request #2049 from python-gitlab/jlvillal/python_311

test: move back to using latest Python 3.11 version ([`6cdccd9`](https://github.com/python-gitlab/python-gitlab/commit/6cdccd90177a70835db176155cf6d0dde70989d3))

* Merge pull request #2053 from python-gitlab/jlvillal/resource

chore: rename `what` to `gitlab_resource` ([`8d30b15`](https://github.com/python-gitlab/python-gitlab/commit/8d30b15310eae79cf82ffbaef82a3f2fbf408ec5))

* Merge pull request #2052 from python-gitlab/jlvillal/cli_minor_clean

chore: rename `__call__()` to `run()` in GitlabCLI ([`4eb5bad`](https://github.com/python-gitlab/python-gitlab/commit/4eb5bad1a7e17a38182e0ec68c48faa4a0306ceb))

* Merge pull request #2050 from python-gitlab/jlvillal/more_pylint

chore: enable &#39;consider-using-sys-exit&#39; pylint check ([`9ab3c10`](https://github.com/python-gitlab/python-gitlab/commit/9ab3c107567f38967d918b7d69f29fd3cc83218e))

* Merge pull request #2043 from python-gitlab/jlvillal/f-string

chore: require f-strings ([`3d000d3`](https://github.com/python-gitlab/python-gitlab/commit/3d000d3de86306faee063f4edf9f09aff7590791))

* Merge pull request #2042 from python-gitlab/jlvillal/exclusive

Clean-up the `validate_attrs` method/function ([`28cf3c3`](https://github.com/python-gitlab/python-gitlab/commit/28cf3c3d392f2f7f55dc142681181e15c702018a))

* Merge pull request #2040 from python-gitlab/jlvillal/type_alias

chore: have `EncodedId` creation always return `EncodedId` ([`dea9435`](https://github.com/python-gitlab/python-gitlab/commit/dea9435f21ededac998ba878a4fd2def698a3066))

* Merge pull request #2039 from python-gitlab/jlvillal/required_optional

chore: move `RequiredOptional` to the `gitlab.types` module ([`37eb8e0`](https://github.com/python-gitlab/python-gitlab/commit/37eb8e0a4f0fd5fc7e221163b84df3461e64475b))

* Merge pull request #2036 from python-gitlab/jlvillal/get_not_none

chore: update type-hints return signature for GetWithoutIdMixin methods ([`1f17349`](https://github.com/python-gitlab/python-gitlab/commit/1f17349826a0516c648db20ae80ac713bab8a160))

* Merge pull request #2033 from python-gitlab/jlvillal/module_not_found_error

chore: correct ModuleNotFoundError() arguments ([`b2e6f3b`](https://github.com/python-gitlab/python-gitlab/commit/b2e6f3bc0dd6d8a7da39939850689a3677eb2444))

* Merge pull request #2034 from python-gitlab/renovate/typing-dependencies

chore(deps): update typing dependencies ([`38218e5`](https://github.com/python-gitlab/python-gitlab/commit/38218e5d099f112ed0e1784282e5edc4956fee15))

* Merge pull request #2035 from python-gitlab/renovate/commitizen-2.x

chore(deps): update dependency commitizen to v2.27.1 ([`91e60ba`](https://github.com/python-gitlab/python-gitlab/commit/91e60bac86d62e61ca5526af29d3b7293d210fdc))

* Merge pull request #2032 from python-gitlab/jlvillal/i_hate_as_list

feat(client): introduce `iterator=True` and deprecate `as_list=False` in `list()` ([`c51b538`](https://github.com/python-gitlab/python-gitlab/commit/c51b538caae0a94d936d94d6da60c362492f9403))

* Merge pull request #1884 from python-gitlab/jlvillal/list_docs

docs: use `as_list=False` or `all=True` in Getting started ([`5ae18d0`](https://github.com/python-gitlab/python-gitlab/commit/5ae18d08aa11a01347514b43db8470bfd65fd534))

## v3.5.0 (2022-05-28)

### Chore

* chore(ci): fix prefix for action version ([`1c02189`](https://github.com/python-gitlab/python-gitlab/commit/1c021892e94498dbb6b3fa824d6d8c697fb4db7f))

* chore(ci): pin semantic-release version ([`0ea61cc`](https://github.com/python-gitlab/python-gitlab/commit/0ea61ccecae334c88798f80b6451c58f2fbb77c6))

* chore(deps): update pre-commit hook pycqa/pylint to v2.13.9 ([`1e22790`](https://github.com/python-gitlab/python-gitlab/commit/1e2279028533c3dc15995443362e290a4d2c6ae0))

* chore(deps): update dependency pylint to v2.13.9 ([`4224950`](https://github.com/python-gitlab/python-gitlab/commit/422495073492fd52f4f3b854955c620ada4c1daa))

* chore: run the `pylint` check by default in tox

Since we require `pylint` to pass in the CI. Let&#39;s run it by default
in tox. ([`55ace1d`](https://github.com/python-gitlab/python-gitlab/commit/55ace1d67e75fae9d74b4a67129ff842de7e1377))

* chore: rename the test which runs `flake8` to be `flake8`

Previously the test was called `pep8`. The test only runs `flake8` so
call it `flake8` to be more precise. ([`78b4f99`](https://github.com/python-gitlab/python-gitlab/commit/78b4f995afe99c530858b7b62d3eee620f3488f2))

* chore(deps): update pre-commit hook pycqa/pylint to v2.13.8 ([`1835593`](https://github.com/python-gitlab/python-gitlab/commit/18355938d1b410ad5e17e0af4ef0667ddb709832))

* chore(deps): update dependency pylint to v2.13.8 ([`b235bb0`](https://github.com/python-gitlab/python-gitlab/commit/b235bb00f3c09be5bb092a5bb7298e7ca55f2366))

* chore: exclude `build/` directory from mypy check

The `build/` directory is created by the tox environment
`twine-check`. When the `build/` directory exists `mypy` will have an
error. ([`989a12b`](https://github.com/python-gitlab/python-gitlab/commit/989a12b79ac7dff8bf0d689f36ccac9e3494af01))

* chore: add `cz` to default tox environment list and skip_missing_interpreters

Add the `cz` (`comittizen`) check by default.

Set skip_missing_interpreters = True so that when a user runs tox and
doesn&#39;t have a specific version of Python it doesn&#39;t mark it as an
error. ([`ba8c052`](https://github.com/python-gitlab/python-gitlab/commit/ba8c0522dc8a116e7a22c42e21190aa205d48253))

* chore(deps): update dependency types-requests to v2.27.25 ([`d6ea47a`](https://github.com/python-gitlab/python-gitlab/commit/d6ea47a175c17108e5388213abd59c3e7e847b02))

* chore(ci): replace commitlint with commitizen ([`b8d15fe`](https://github.com/python-gitlab/python-gitlab/commit/b8d15fed0740301617445e5628ab76b6f5b8baeb))

* chore(renovate): set schedule to reduce noise ([`882fe7a`](https://github.com/python-gitlab/python-gitlab/commit/882fe7a681ae1c5120db5be5e71b196ae555eb3e))

* chore(deps): update dependency types-requests to v2.27.24 ([`f88e3a6`](https://github.com/python-gitlab/python-gitlab/commit/f88e3a641ebb83818e11713eb575ebaa597440f0))

* chore(deps): update dependency types-requests to v2.27.23 ([`a6fed8b`](https://github.com/python-gitlab/python-gitlab/commit/a6fed8b4a0edbe66bf29cd7a43d51d2f5b8b3e3a))

### Documentation

* docs: update issue example and extend API usage docs ([`aad71d2`](https://github.com/python-gitlab/python-gitlab/commit/aad71d282d60dc328b364bcc951d0c9b44ab13fa))

* docs(CONTRIBUTING.rst): fix link to conventional-changelog commit format documentation ([`2373a4f`](https://github.com/python-gitlab/python-gitlab/commit/2373a4f13ee4e5279a424416cdf46782a5627067))

* docs: add missing Admin access const value

As shown here, Admin access is set to 60:
https://docs.gitlab.com/ee/api/protected_branches.html#protected-branches-api ([`3e0d4d9`](https://github.com/python-gitlab/python-gitlab/commit/3e0d4d9006e2ca6effae2b01cef3926dd0850e52))

* docs(merge_requests): add new possible merge request state and link to the upstream docs

The actual documentation do not mention the locked state for a merge request ([`e660fa8`](https://github.com/python-gitlab/python-gitlab/commit/e660fa8386ed7783da5c076bc0fef83e6a66f9a8))

### Feature

* feat(objects): support get project storage endpoint ([`8867ee5`](https://github.com/python-gitlab/python-gitlab/commit/8867ee59884ae81d6457ad6e561a0573017cf6b2))

* feat: display human-readable attribute in `repr()` if present ([`6b47c26`](https://github.com/python-gitlab/python-gitlab/commit/6b47c26d053fe352d68eb22a1eaf4b9a3c1c93e7))

* feat(ux): display project.name_with_namespace on project repr

This change the repr from:

$ gitlab.projects.get(id=some_id)
&lt;Project id:some_id&gt;

To:

$ gitlab.projects.get(id=some_id)
&lt;Project id:some_id name_with_namespace:&#34;group_name / project_name&#34;&gt;

This is especially useful when working on random projects or listing of
projects since users generally don&#39;t remember projects ids. ([`e598762`](https://github.com/python-gitlab/python-gitlab/commit/e5987626ca1643521b16658555f088412be2a339))

### Fix

* fix(cli): changed default `allow_abbrev` value to fix arguments collision problem (#2013)

fix(cli): change default `allow_abbrev` value to fix argument collision ([`d68cacf`](https://github.com/python-gitlab/python-gitlab/commit/d68cacfeda5599c62a593ecb9da2505c22326644))

* fix: duplicate subparsers being added to argparse

Python 3.11 added an additional check in the argparse libary which
detected duplicate subparsers being added. We had duplicate subparsers
being added.

Make sure we don&#39;t add duplicate subparsers.

Closes: #2015 ([`f553fd3`](https://github.com/python-gitlab/python-gitlab/commit/f553fd3c79579ab596230edea5899dc5189b0ac6))

### Test

* test(projects): add tests for list project methods ([`fa47829`](https://github.com/python-gitlab/python-gitlab/commit/fa47829056a71e6b9b7f2ce913f2aebc36dc69e9))

### Unknown

* Merge pull request #2022 from MichaelSweikata/feat/documentation-update

docs: update issue example and extend API usage docs ([`792cee9`](https://github.com/python-gitlab/python-gitlab/commit/792cee939843d8df4c87bb8068be147ec97fabac))

* Merge pull request #2012 from rnoberger/rnoberger/test-projects

test: increase projects coverage ([`fd9154e`](https://github.com/python-gitlab/python-gitlab/commit/fd9154e15f0094f2ceb5f98b2d8f3645b26c7fda))

* Merge pull request #2019 from python-gitlab/jlvillal/tox

Some improvements to our tox environment defaults ([`d121d2d`](https://github.com/python-gitlab/python-gitlab/commit/d121d2dfcf32d6c937e537d1dd4844b6efa38dcb))

* Merge pull request #2018 from python-gitlab/renovate/pycqa-pylint-2.x

chore(deps): update pre-commit hook pycqa/pylint to v2.13.8 ([`9e64645`](https://github.com/python-gitlab/python-gitlab/commit/9e646451dcca837807691a69545df93a5c93fd18))

* Merge pull request #2017 from python-gitlab/renovate/pylint-2.x

chore(deps): update dependency pylint to v2.13.8 ([`0049f83`](https://github.com/python-gitlab/python-gitlab/commit/0049f83ba7522d5721d0f6173934e294dfcc5d06))

* Merge pull request #2014 from python-gitlab/jlvillal/python3.11beta1

fix: duplicate subparsers being added to argparse ([`7d5a0c9`](https://github.com/python-gitlab/python-gitlab/commit/7d5a0c9c2a3fb4667151660bcf52d33a3f6d27a6))

* Merge pull request #1996 from Psycojoker/project-name-in-repr

feat(ux): display project.name_with_namespace on project repr ([`82c9a07`](https://github.com/python-gitlab/python-gitlab/commit/82c9a07a6ac703ec10431ebcdd1fc8c7dadac58d))

* Merge pull request #2008 from python-gitlab/jlvillal/mypy-tox

chore: exclude `build/` directory from mypy check ([`d169983`](https://github.com/python-gitlab/python-gitlab/commit/d169983abbc6094bcddac14a377b4196bc1fac4e))

* Merge pull request #2009 from python-gitlab/jlvillal/tox-env

chore: add `cz` to default tox environment list and skip_missing_interpreters ([`5cb2859`](https://github.com/python-gitlab/python-gitlab/commit/5cb2859e7c4f8390546f794417ca800ee46d3293))

* Merge pull request #2005 from carlosduelo/patch-1

merge request can have state locked ([`ef207da`](https://github.com/python-gitlab/python-gitlab/commit/ef207da0fc37c7cc4464913909ccb05eae6a24de))

* Merge pull request #2001 from python-gitlab/renovate/typing-dependencies

chore(deps): update dependency types-requests to v2.27.25 ([`04e0d24`](https://github.com/python-gitlab/python-gitlab/commit/04e0d24ecc41785b837e0e98cdcb43908e2505a3))

* Merge pull request #1994 from python-gitlab/renovate/typing-dependencies

chore(deps): update dependency types-requests to v2.27.24 ([`79b903d`](https://github.com/python-gitlab/python-gitlab/commit/79b903d24bf518b67c7da9ead2cdaec3c3f67f88))

## v3.4.0 (2022-04-28)

### Chore

* chore(deps): update dependency mypy to v0.950 ([`241e626`](https://github.com/python-gitlab/python-gitlab/commit/241e626c8e88bc1b6b3b2fc37e38ed29b6912b4e))

* chore(deps): update dependency types-requests to v2.27.22 ([`22263e2`](https://github.com/python-gitlab/python-gitlab/commit/22263e24f964e56ec76d8cb5243f1cad1d139574))

* chore(deps): update dependency types-requests to v2.27.21 ([`0fb0955`](https://github.com/python-gitlab/python-gitlab/commit/0fb0955b93ee1c464b3a5021bc22248103742f1d))

* chore(deps): update dependency pytest to v7.1.2 ([`fd3fa23`](https://github.com/python-gitlab/python-gitlab/commit/fd3fa23bd4f7e0d66b541780f94e15635851e0db))

* chore(deps): update typing dependencies ([`c12466a`](https://github.com/python-gitlab/python-gitlab/commit/c12466a0e7ceebd3fb9f161a472bbbb38e9bd808))

* chore(deps): update pre-commit hook pycqa/pylint to v2.13.7 ([`1396221`](https://github.com/python-gitlab/python-gitlab/commit/1396221a96ea2f447b0697f589a50a9c22504c00))

* chore(deps): update dependency pylint to v2.13.7 ([`5fb2234`](https://github.com/python-gitlab/python-gitlab/commit/5fb2234dddf73851b5de7af5d61b92de022a892a))

* chore(deps): update typing dependencies ([`d27cc6a`](https://github.com/python-gitlab/python-gitlab/commit/d27cc6a1219143f78aad7e063672c7442e15672e))

* chore(deps): update pre-commit hook pycqa/pylint to v2.13.5 ([`17d5c6c`](https://github.com/python-gitlab/python-gitlab/commit/17d5c6c3ba26f8b791ec4571726c533f5bbbde7d))

* chore(deps): update dependency pylint to v2.13.5 ([`5709675`](https://github.com/python-gitlab/python-gitlab/commit/570967541ecd46bfb83461b9d2c95bb0830a84fa))

* chore(deps): update codecov/codecov-action action to v3 ([`292e91b`](https://github.com/python-gitlab/python-gitlab/commit/292e91b3cbc468c4a40ed7865c3c98180c1fe864))

* chore(deps): update dependency types-setuptools to v57.4.12 ([`6551353`](https://github.com/python-gitlab/python-gitlab/commit/65513538ce60efdde80e5e0667b15739e6d90ac1))

* chore(client): remove duplicate code ([`5cbbf26`](https://github.com/python-gitlab/python-gitlab/commit/5cbbf26e6f6f3ce4e59cba735050e3b7f9328388))

* chore(deps): update dependency types-requests to v2.27.16 ([`ad799fc`](https://github.com/python-gitlab/python-gitlab/commit/ad799fca51a6b2679e2bcca8243a139e0bd0acf5))

* chore(deps): upgrade gitlab-ce to 14.9.2-ce.0 ([`d508b18`](https://github.com/python-gitlab/python-gitlab/commit/d508b1809ff3962993a2279b41b7d20e42d6e329))

* chore(deps): update pre-commit hook pycqa/pylint to v2.13.4 ([`9d0b252`](https://github.com/python-gitlab/python-gitlab/commit/9d0b25239773f98becea3b5b512d50f89631afb5))

* chore(deps): update dependency pylint to v2.13.4 ([`a9a9392`](https://github.com/python-gitlab/python-gitlab/commit/a9a93921b795eee0db16e453733f7c582fa13bc9))

* chore(deps): update pre-commit hook pycqa/pylint to v2.13.3 ([`8f0a3af`](https://github.com/python-gitlab/python-gitlab/commit/8f0a3af46a1f49e6ddba31ee964bbe08c54865e0))

* chore(deps): update dependency pylint to v2.13.3 ([`0ae3d20`](https://github.com/python-gitlab/python-gitlab/commit/0ae3d200563819439be67217a7fc0e1552f07c90))

* chore(deps): update black to v22.3.0 ([`8d48224`](https://github.com/python-gitlab/python-gitlab/commit/8d48224c89cf280e510fb5f691e8df3292577f64))

### Documentation

* docs(api-docs): docs fix for application scopes ([`e1ad93d`](https://github.com/python-gitlab/python-gitlab/commit/e1ad93df90e80643866611fe52bd5c59428e7a88))

### Feature

* feat(objects): support getting project/group deploy tokens by id ([`fcd37fe`](https://github.com/python-gitlab/python-gitlab/commit/fcd37feff132bd5b225cde9d5f9c88e62b3f1fd6))

* feat(user): support getting user SSH key by id ([`6f93c05`](https://github.com/python-gitlab/python-gitlab/commit/6f93c0520f738950a7c67dbeca8d1ac8257e2661))

* feat: emit a warning when using a `list()` method returns max

A common cause of issues filed and questions raised is that a user
will call a `list()` method and only get 20 items. As this is the
default maximum of items that will be returned from a `list()` method.

To help with this we now emit a warning when the result from a
`list()` method is greater-than or equal to 20 (or the specified
`per_page` value) and the user is not using either `all=True`,
`all=False`, `as_list=False`, or `page=X`. ([`1339d64`](https://github.com/python-gitlab/python-gitlab/commit/1339d645ce58a2e1198b898b9549ba5917b1ff12))

* feat(api): re-add topic delete endpoint

This reverts commit e3035a799a484f8d6c460f57e57d4b59217cd6de. ([`d1d96bd`](https://github.com/python-gitlab/python-gitlab/commit/d1d96bda5f1c6991c8ea61dca8f261e5b74b5ab6))

### Fix

* fix: avoid passing redundant arguments to API ([`3431887`](https://github.com/python-gitlab/python-gitlab/commit/34318871347b9c563d01a13796431c83b3b1d58c))

* fix: add ChunkedEncodingError to list of retryable exceptions ([`7beb20f`](https://github.com/python-gitlab/python-gitlab/commit/7beb20ff7b7b85fb92fc6b647d9c1bdb7568f27c))

* fix(cli): add missing filters for project commit list ([`149d244`](https://github.com/python-gitlab/python-gitlab/commit/149d2446fcc79b31d3acde6e6d51adaf37cbb5d3))

* fix: add 52x range to retry transient failures and tests ([`c3ef1b5`](https://github.com/python-gitlab/python-gitlab/commit/c3ef1b5c1eaf1348a18d753dbf7bda3c129e3262))

* fix: also retry HTTP-based transient errors ([`3b49e4d`](https://github.com/python-gitlab/python-gitlab/commit/3b49e4d61e6f360f1c787aa048edf584aec55278))

### Unknown

* Merge pull request #1988 from python-gitlab/renovate/mypy-0.x

chore(deps): update dependency mypy to v0.950 ([`0c0035e`](https://github.com/python-gitlab/python-gitlab/commit/0c0035e10dc472a572856e7a73a30e2d7b829d79))

* Merge pull request #1986 from python-gitlab/renovate/typing-dependencies

chore(deps): update dependency types-requests to v2.27.21 ([`ab8352e`](https://github.com/python-gitlab/python-gitlab/commit/ab8352ea224d2929826c70fed37d87c0e903ce93))

* Merge pull request #1983 from python-gitlab/renovate/pytest-7.x

chore(deps): update dependency pytest to v7.1.2 ([`4a6bd90`](https://github.com/python-gitlab/python-gitlab/commit/4a6bd90dcaf22eb03735a7198780aac7f243020f))

* Merge pull request #1981 from python-gitlab/renovate/typing-dependencies

chore(deps): update typing dependencies ([`cf2953e`](https://github.com/python-gitlab/python-gitlab/commit/cf2953e0e542baa0c36a9f521ad462365821ff96))

* Merge pull request #1980 from python-gitlab/renovate/pycqa-pylint-2.x

chore(deps): update pre-commit hook pycqa/pylint to v2.13.7 ([`0305979`](https://github.com/python-gitlab/python-gitlab/commit/0305979de2d06e753b73a4f378d772b3c720771d))

* Merge pull request #1979 from python-gitlab/renovate/pylint-2.x

chore(deps): update dependency pylint to v2.13.7 ([`396e30c`](https://github.com/python-gitlab/python-gitlab/commit/396e30c3be6df382ce2be3848c5683ddb79bfdd8))

* Merge pull request #1965 from python-gitlab/fix/redundant-args-api

fix: avoid passing redundant arguments to API ([`ba7692a`](https://github.com/python-gitlab/python-gitlab/commit/ba7692aee2f11b502565dd2c4b46aa99772c2ca7))

* Merge pull request #1974 from Sineaggi/add-chunked-to-list-of-retryable-exceptions

Add ChunkedEncodingError to list of retryable exceptions ([`07a16af`](https://github.com/python-gitlab/python-gitlab/commit/07a16af33c6d1965dae860d1e604ce36e42d8d87))

* Merge pull request #1963 from python-gitlab/feat/deploy-token-get

feat(objects): support getting project/group deploy tokens by id ([`69ace2d`](https://github.com/python-gitlab/python-gitlab/commit/69ace2dcf41a763b624079e57805c1ba09865312))

* Merge pull request #1962 from python-gitlab/feat/user-ssh-key

feat(user): support getting user SSH key by id ([`68bf5d8`](https://github.com/python-gitlab/python-gitlab/commit/68bf5d82b4480c541281d7f5eaf46850b13916d4))

* Merge pull request #1875 from python-gitlab/jlvillal/list_warning

feat: emit a warning when using a `list()` method returns max ([`4d6f125`](https://github.com/python-gitlab/python-gitlab/commit/4d6f1259a1806314830853f8917d1f5128479bc3))

* Merge pull request #1971 from python-gitlab/renovate/pycqa-pylint-2.x

chore(deps): update pre-commit hook pycqa/pylint to v2.13.5 ([`5370979`](https://github.com/python-gitlab/python-gitlab/commit/5370979a3f6e29cd17f77849c445561a892d912c))

* Merge pull request #1964 from python-gitlab/fix/missing-commit-list-filters

fix(cli): add missing filters for project commit list ([`3b0806e`](https://github.com/python-gitlab/python-gitlab/commit/3b0806ed5ce135935d0362068400d41874e3f4a9))

* Merge pull request #1968 from python-gitlab/renovate/codecov-codecov-action-3.x

chore(deps): update codecov/codecov-action action to v3 ([`de8cfd9`](https://github.com/python-gitlab/python-gitlab/commit/de8cfd9a0d394542750304c530888d1b869b3dfb))

* Merge pull request #1967 from python-gitlab/renovate/typing-dependencies

chore(deps): update dependency types-setuptools to v57.4.12 ([`3be5ac2`](https://github.com/python-gitlab/python-gitlab/commit/3be5ac26c615b7cdd59441273096b2f1b61b11bb))

* Merge pull request #1904 from Sineaggi/retry-additional-http-transient-errors

Retry additional http transient errors ([`0353bd4`](https://github.com/python-gitlab/python-gitlab/commit/0353bd4cceb3264a6d0dddbd6e338ca6213b9bac))

* Merge pull request #1961 from python-gitlab/renovate/typing-dependencies

chore(deps): update dependency types-requests to v2.27.16 ([`19ab07d`](https://github.com/python-gitlab/python-gitlab/commit/19ab07d425cbe9fd23e1e94e107b52f9d14eecf1))

* Merge pull request #1959 from python-gitlab/renovate/pycqa-pylint-2.x

chore(deps): update pre-commit hook pycqa/pylint to v2.13.4 ([`8db6841`](https://github.com/python-gitlab/python-gitlab/commit/8db68411d6444787ca339cf50dd96b2ab41de60c))

* Merge pull request #1958 from python-gitlab/renovate/pylint-2.x

chore(deps): update dependency pylint to v2.13.4 ([`400d8e5`](https://github.com/python-gitlab/python-gitlab/commit/400d8e58c390f967b5539517675d54e55c9453bc))

* Merge pull request #1951 from wacuuu/main

docs: small docs fix-up for application scopes ([`8e241e4`](https://github.com/python-gitlab/python-gitlab/commit/8e241e483bb8b316a831f5831e6db733dd04a08f))

* Merge pull request #1954 from python-gitlab/renovate/pycqa-pylint-2.x

chore(deps): update pre-commit hook pycqa/pylint to v2.13.3 ([`eee173e`](https://github.com/python-gitlab/python-gitlab/commit/eee173e6f3d464cee5ce3e705b727f266444d04f))

* Merge pull request #1953 from python-gitlab/renovate/pylint-2.x

chore(deps): update dependency pylint to v2.13.3 ([`5498f9e`](https://github.com/python-gitlab/python-gitlab/commit/5498f9e3e11187b63e7ef5f61c570a70bbfb1348))

* Merge pull request #1952 from python-gitlab/renovate/black

chore(deps): update black to v22.3.0 ([`f942e65`](https://github.com/python-gitlab/python-gitlab/commit/f942e65ad6e0ab911de1ee32b4f720cf061e3dec))

## v3.3.0 (2022-03-28)

### Chore

* chore(deps): update dependency sphinx to v4.5.0 ([`36ab769`](https://github.com/python-gitlab/python-gitlab/commit/36ab7695f584783a4b3272edd928de3b16843a36))

* chore(deps): update pre-commit hook pycqa/pylint to v2.13.2 ([`14d367d`](https://github.com/python-gitlab/python-gitlab/commit/14d367d60ab8f1e724c69cad0f39c71338346948))

* chore(deps): update dependency pylint to v2.13.2 ([`10f15a6`](https://github.com/python-gitlab/python-gitlab/commit/10f15a625187f2833be72d9bf527e75be001d171))

* chore(deps): update dependency types-requests to v2.27.15 ([`2e8ecf5`](https://github.com/python-gitlab/python-gitlab/commit/2e8ecf569670afc943e8a204f3b2aefe8aa10d8b))

* chore(deps): update pre-commit hook pycqa/pylint to v2.13.1 ([`1d0c6d4`](https://github.com/python-gitlab/python-gitlab/commit/1d0c6d423ce9f6c98511578acbb0f08dc4b93562))

* chore(deps): update dependency types-requests to v2.27.14 ([`be6b54c`](https://github.com/python-gitlab/python-gitlab/commit/be6b54c6028036078ef09013f6c51c258173f3ca))

* chore(deps): update dependency pylint to v2.13.1 ([`eefd724`](https://github.com/python-gitlab/python-gitlab/commit/eefd724545de7c96df2f913086a7f18020a5470f))

* chore(deps): update pre-commit hook pycqa/pylint to v2.13.0 ([`9fe60f7`](https://github.com/python-gitlab/python-gitlab/commit/9fe60f7b8fa661a8bba61c04fcb5b54359ac6778))

* chore(deps): update dependency pylint to v2.13.0 ([`5fa403b`](https://github.com/python-gitlab/python-gitlab/commit/5fa403bc461ed8a4d183dcd8f696c2a00b64a33d))

* chore(deps): update dependency mypy to v0.942 ([`8ba0f8c`](https://github.com/python-gitlab/python-gitlab/commit/8ba0f8c6b42fa90bd1d7dd7015a546e8488c3f73))

* chore(deps): update dependency pytest-console-scripts to v1.3.1 ([`da392e3`](https://github.com/python-gitlab/python-gitlab/commit/da392e33e58d157169e5aa3f1fe725457e32151c))

* chore(deps): update dependency pytest to v7.1.1 ([`e31f2ef`](https://github.com/python-gitlab/python-gitlab/commit/e31f2efe97995f48c848f32e14068430a5034261))

* chore(deps): update typing dependencies ([`21e7c37`](https://github.com/python-gitlab/python-gitlab/commit/21e7c3767aa90de86046a430c7402f0934950e62))

* chore(deps): update dependency mypy to v0.941 ([`3a9d4f1`](https://github.com/python-gitlab/python-gitlab/commit/3a9d4f1dc2069e29d559967e1f5498ccadf62591))

* chore(deps): update dependency pytest to v7.1.0 ([`27c7e33`](https://github.com/python-gitlab/python-gitlab/commit/27c7e3350839aaf5c06a15c1482fc2077f1d477a))

* chore(deps): update dependency types-requests to v2.27.12 ([`8cd668e`](https://github.com/python-gitlab/python-gitlab/commit/8cd668efed7bbbca370634e8c8cb10e3c7a13141))

* chore(deps): update dependency mypy to v0.940 ([`dd11084`](https://github.com/python-gitlab/python-gitlab/commit/dd11084dd281e270a480b338aba88b27b991e58e))

* chore(deps): update black to v22 ([`3f84f1b`](https://github.com/python-gitlab/python-gitlab/commit/3f84f1bb805691b645fac2d1a41901abefccb17e))

* chore(deps): update pre-commit hook alessandrojcm/commitlint-pre-commit-hook to v8 ([`5440780`](https://github.com/python-gitlab/python-gitlab/commit/544078068bc9d7a837e75435e468e4749f7375ac))

* chore(deps): update dependency types-setuptools to v57.4.10 ([`b37fc41`](https://github.com/python-gitlab/python-gitlab/commit/b37fc4153a00265725ca655bc4482714d6b02809))

* chore(deps): update dependency pytest to v7 ([`ae8d70d`](https://github.com/python-gitlab/python-gitlab/commit/ae8d70de2ad3ceb450a33b33e189bb0a3f0ff563))

* chore(deps): update actions/upload-artifact action to v3 ([`18a0eae`](https://github.com/python-gitlab/python-gitlab/commit/18a0eae11c480d6bd5cf612a94e56cb9562e552a))

* chore(deps): update actions/stale action to v5 ([`d841185`](https://github.com/python-gitlab/python-gitlab/commit/d8411853e224a198d0ead94242acac3aadef5adc))

* chore(deps): update actions/setup-python action to v3 ([`7f845f7`](https://github.com/python-gitlab/python-gitlab/commit/7f845f7eade3c0cdceec6bfe7b3d087a8586edc5))

* chore(deps): update dependency sphinx to v4.4.0 ([`425d161`](https://github.com/python-gitlab/python-gitlab/commit/425d1610ca19be775d9fdd857e61d8b4a4ae4db3))

* chore(deps): update actions/checkout action to v3 ([`7333cbb`](https://github.com/python-gitlab/python-gitlab/commit/7333cbb65385145a14144119772a1854b41ea9d8))

* chore(deps): update dependency pytest-console-scripts to v1.3 ([`9c202dd`](https://github.com/python-gitlab/python-gitlab/commit/9c202dd5a2895289c1f39068f0ea09812f28251f))

* chore(deps): update dependency mypy to v0.931 ([`33646c1`](https://github.com/python-gitlab/python-gitlab/commit/33646c1c4540434bed759d903c9b83af4e7d1a82))

* chore(deps): update typing dependencies ([`37a7c40`](https://github.com/python-gitlab/python-gitlab/commit/37a7c405c975359e9c1f77417e67063326c82a42))

* chore(deps): update dependency requests to v2.27.1 ([`95dad55`](https://github.com/python-gitlab/python-gitlab/commit/95dad55b0cb02fd30172b5b5b9b05a25473d1f03))

### Documentation

* docs(chore): include docs .js files in sdist ([`3010b40`](https://github.com/python-gitlab/python-gitlab/commit/3010b407bc9baabc6cef071507e8fa47c0f1624d))

* docs: fix typo and incorrect style ([`2828b10`](https://github.com/python-gitlab/python-gitlab/commit/2828b10505611194bebda59a0e9eb41faf24b77b))

* docs: add pipeline test report summary support ([`d78afb3`](https://github.com/python-gitlab/python-gitlab/commit/d78afb36e26f41d727dee7b0952d53166e0df850))

### Feature

* feat(object): add pipeline test report summary support ([`a97e0cf`](https://github.com/python-gitlab/python-gitlab/commit/a97e0cf81b5394b3a2b73d927b4efe675bc85208))

### Fix

* fix: support RateLimit-Reset header

Some endpoints are not returning the `Retry-After` header when
rate-limiting occurrs. In those cases use the `RateLimit-Reset` [1]
header, if available.

Closes: #1889

[1] https://docs.gitlab.com/ee/user/admin_area/settings/user_and_ip_rate_limits.html#response-headers ([`4060146`](https://github.com/python-gitlab/python-gitlab/commit/40601463c78a6f5d45081700164899b2559b7e55))

### Style

* style: reformat for black v22 ([`93d4403`](https://github.com/python-gitlab/python-gitlab/commit/93d4403f0e46ed354cbcb133821d00642429532f))

### Unknown

* Merge pull request #1947 from python-gitlab/renovate/typing-dependencies

chore(deps): update dependency types-requests to v2.27.15 ([`59ae16c`](https://github.com/python-gitlab/python-gitlab/commit/59ae16c98675b13325d82dab71abb262bba2cf85))

* Merge pull request #1895 from python-gitlab/jlvillal/rate-limit

fix: support RateLimit-Reset header ([`114958e`](https://github.com/python-gitlab/python-gitlab/commit/114958eb9f487859e8ae0916748e7a275e291d6e))

* Merge pull request #1905 from derekschrock/docs-static

docs(chore): Include docs .js files in sdist ([`363bc87`](https://github.com/python-gitlab/python-gitlab/commit/363bc873f8c804e485740396194c14361c560943))

* Merge pull request #1917 from python-gitlab/renovate/major-black

chore(deps): update black to v22 (major) ([`a4e76eb`](https://github.com/python-gitlab/python-gitlab/commit/a4e76eba3513c9d588ac46c4dbe8d235c9664510))

* Merge pull request #1919 from python-gitlab/renovate/alessandrojcm-commitlint-pre-commit-hook-8.x

chore(deps): update pre-commit hook alessandrojcm/commitlint-pre-commit-hook to v8 ([`71ebee4`](https://github.com/python-gitlab/python-gitlab/commit/71ebee492be5b5b1cd7c024a68c3be692d4bf91f))

* Merge pull request #1915 from kinbald/test-report-summary

feat: add support for test report summary ([`7966584`](https://github.com/python-gitlab/python-gitlab/commit/79665841e5d998872876987e1c3f480e455951a4))

## v3.2.0 (2022-02-28)

### Chore

* chore: create a custom `warnings.warn` wrapper

Create a custom `warnings.warn` wrapper that will walk the stack trace
to find the first frame outside of the `gitlab/` path to print the
warning against. This will make it easier for users to find where in
their code the error is generated from ([`6ca9aa2`](https://github.com/python-gitlab/python-gitlab/commit/6ca9aa2960623489aaf60324b4709848598aec91))

* chore: correct type-hints for per_page attrbute

There are occasions where a GitLab `list()` call does not return the
`x-per-page` header. For example the listing of custom attributes.

Update the type-hints to reflect that. ([`e825653`](https://github.com/python-gitlab/python-gitlab/commit/e82565315330883823bd5191069253a941cb2683))

* chore: require kwargs for `utils.copy_dict()`

The non-keyword arguments were a tiny bit confusing as the destination was
first and the source was second.

Change the order and require key-word only arguments to ensure we
don&#39;t silently break anyone. ([`7cf35b2`](https://github.com/python-gitlab/python-gitlab/commit/7cf35b2c0e44732ca02b74b45525cc7c789457fb))

* chore: create new ArrayAttribute class

Create a new ArrayAttribute class. This is to indicate types which are
sent to the GitLab server as arrays
https://docs.gitlab.com/ee/api/#array

At this stage it is identical to the CommaSeparatedListAttribute class
but will be used later to support the array types sent to GitLab.

This is the second step in a series of steps of our goal to add full
support for the GitLab API data types[1]:
  * array
  * hash
  * array of hashes

Step one was: commit 5127b1594c00c7364e9af15e42d2e2f2d909449b

[1] https://docs.gitlab.com/ee/api/#encoding-api-parameters-of-array-and-hash-types

Related: #1698 ([`a57334f`](https://github.com/python-gitlab/python-gitlab/commit/a57334f1930752c70ea15847a39324fa94042460))

* chore(ci): do not run release workflow in forks ([`2b6edb9`](https://github.com/python-gitlab/python-gitlab/commit/2b6edb9a0c62976ff88a95a953e9d3f2c7f6f144))

### Documentation

* docs: enable gitter chat directly in docs ([`bd1ecdd`](https://github.com/python-gitlab/python-gitlab/commit/bd1ecdd5ad654b01b34e7a7a96821cc280b3ca67))

* docs: add delete methods for runners and project artifacts ([`5e711fd`](https://github.com/python-gitlab/python-gitlab/commit/5e711fdb747fb3dcde1f5879c64dfd37bf25f3c0))

* docs: add retry_transient infos

Co-authored-by: Nejc Habjan &lt;hab.nejc@gmail.com&gt; ([`bb1f054`](https://github.com/python-gitlab/python-gitlab/commit/bb1f05402887c78f9898fbd5bd66e149eff134d9))

* docs: add transient errors retry info ([`b7a1266`](https://github.com/python-gitlab/python-gitlab/commit/b7a126661175a3b9b73dbb4cb88709868d6d871c))

* docs(artifacts): deprecate artifacts() and artifact() methods ([`64d01ef`](https://github.com/python-gitlab/python-gitlab/commit/64d01ef23b1269b705350106d8ddc2962a780dce))

* docs: revert &#34;chore: add temporary banner for v3&#34; (#1864)

This reverts commit a349793307e3a975bb51f864b48e5e9825f70182.

Co-authored-by: Wadim Klincov &lt;wadim.klincov@siemens.com&gt; ([`7a13b9b`](https://github.com/python-gitlab/python-gitlab/commit/7a13b9bfa4aead6c731f9a92e0946dba7577c61b))

### Feature

* feat(merge_request_approvals): add support for deleting MR approval rules ([`85a734f`](https://github.com/python-gitlab/python-gitlab/commit/85a734fec3111a4a5c4f0ddd7cb36eead96215e9))

* feat(artifacts): add support for project artifacts delete API ([`c01c034`](https://github.com/python-gitlab/python-gitlab/commit/c01c034169789e1d20fd27a0f39f4c3c3628a2bb))

* feat(mixins): allow deleting resources without IDs ([`0717517`](https://github.com/python-gitlab/python-gitlab/commit/0717517212b616cfd52cfd38dd5c587ff8f9c47c))

* feat(objects): add a complete artifacts manager ([`c8c2fa7`](https://github.com/python-gitlab/python-gitlab/commit/c8c2fa763558c4d9906e68031a6602e007fec930))

### Fix

* fix(services): use slug for id_attr instead of custom methods ([`e30f39d`](https://github.com/python-gitlab/python-gitlab/commit/e30f39dff5726266222b0f56c94f4ccfe38ba527))

* fix: remove custom `delete` method for labels

The usage of deleting was incorrect according to the current API.
Remove custom `delete()` method as not needed.

Add tests to show it works with labels needing to be encoded.

Also enable the test_group_labels() test function. Previously it was
disabled.

Add ability to do a `get()` for group labels.

Closes: #1867 ([`0841a2a`](https://github.com/python-gitlab/python-gitlab/commit/0841a2a686c6808e2f3f90960e529b26c26b268f))

### Style

* style(objects): add spacing to docstrings ([`700d25d`](https://github.com/python-gitlab/python-gitlab/commit/700d25d9bd812a64f5f1287bf50e8ddc237ec553))

### Test

* test(unit): clean up MR approvals fixtures ([`0eb4f7f`](https://github.com/python-gitlab/python-gitlab/commit/0eb4f7f06c7cfe79c5d6695be82ac9ca41c8057e))

* test(runners): add test for deleting runners by auth token ([`14b88a1`](https://github.com/python-gitlab/python-gitlab/commit/14b88a13914de6ee54dd2a3bd0d5960a50578064))

* test(functional): fix GitLab configuration to support pagination

When pagination occurs python-gitlab uses the URL provided by the
GitLab server to use for the next request.

We had previously set the GitLab server configuraiton to say its URL
was `http://gitlab.test` which is not in DNS. Set the hostname
in the URL to `http://127.0.0.1:8080` which is the correct URL for the
GitLab server to be accessed while doing functional tests.

Closes: #1877 ([`5b7d00d`](https://github.com/python-gitlab/python-gitlab/commit/5b7d00df466c0fe894bafeb720bf94ffc8cd38fd))

* test(services): add functional tests for services ([`2fea2e6`](https://github.com/python-gitlab/python-gitlab/commit/2fea2e64c554fd92d14db77cc5b1e2976b27b609))

* test(objects): add tests for project artifacts ([`8ce0336`](https://github.com/python-gitlab/python-gitlab/commit/8ce0336325b339fa82fe4674a528f4bb59963df7))

### Unknown

* Merge pull request #1882 from python-gitlab/jlvillal/custom_warn

chore: create a custom `warnings.warn` wrapper ([`5beda3b`](https://github.com/python-gitlab/python-gitlab/commit/5beda3baae97474f2625131c3d6e5799e75d546a))

* Merge pull request #1881 from python-gitlab/jlvillal/easy2

test(functional): fix GitLab configuration to support pagination ([`4cb7d92`](https://github.com/python-gitlab/python-gitlab/commit/4cb7d9224fb24e4a13fdff8271de5ce083ad7757))

* Merge pull request #1880 from python-gitlab/jlvillal/easy

chore: correct type-hints for per_page attrbute ([`5e19694`](https://github.com/python-gitlab/python-gitlab/commit/5e1969431294bdb11b37b12c2b2ca3f20466389e))

* Merge pull request #1876 from emirot/patch-1

docs: add transient errors retry info ([`9897c98`](https://github.com/python-gitlab/python-gitlab/commit/9897c982f0d10da94692b94d8585216c4553437e))

* Merge pull request #1871 from python-gitlab/jlvillal/copy_dict

chore: require kwargs for `utils.copy_dict()` ([`2adf31d`](https://github.com/python-gitlab/python-gitlab/commit/2adf31dff04cd9b037d8727ab1b48385248bbabd))

* Merge pull request #1868 from python-gitlab/jlvillal/delete_label

fix: remove custom `delete` method for labels ([`0ab0fc1`](https://github.com/python-gitlab/python-gitlab/commit/0ab0fc13acaa495459e41546dc23bbc7cfdb3c4b))

* Merge pull request #1866 from python-gitlab/jlvillal/arrays_2

chore: create new ArrayAttribute class ([`7646360`](https://github.com/python-gitlab/python-gitlab/commit/7646360d6b622b1008917116dc4f64ced32f4057))

## v3.1.1 (2022-01-28)

### Chore

* chore: use dataclass for RequiredOptional ([`30117a3`](https://github.com/python-gitlab/python-gitlab/commit/30117a3b6a8ee24362de798b2fa596a343b8774f))

* chore: remove redundant list comprehension ([`271cfd3`](https://github.com/python-gitlab/python-gitlab/commit/271cfd3651e4e9cda974d5c3f411cecb6dca6c3c))

* chore: consistently use open() encoding and file descriptor ([`dc32d54`](https://github.com/python-gitlab/python-gitlab/commit/dc32d54c49ccc58c01cd436346a3fbfd4a538778))

* chore: don&#39;t explicitly pass args to super() ([`618267c`](https://github.com/python-gitlab/python-gitlab/commit/618267ced7aaff46d8e03057fa0cab48727e5dc0))

* chore: always use context manager for file IO ([`e8031f4`](https://github.com/python-gitlab/python-gitlab/commit/e8031f42b6804415c4afee4302ab55462d5848ac))

* chore: remove old-style classes ([`ae2a015`](https://github.com/python-gitlab/python-gitlab/commit/ae2a015db1017d3bf9b5f1c5893727da9b0c937f))

* chore: rename `types.ListAttribute` to `types.CommaSeparatedListAttribute`

This name more accurately describes what the type is. Also this is the
first step in a series of steps of our goal to add full support for
the GitLab API data types[1]:
  * array
  * hash
  * array of hashes

[1] https://docs.gitlab.com/ee/api/#encoding-api-parameters-of-array-and-hash-types ([`5127b15`](https://github.com/python-gitlab/python-gitlab/commit/5127b1594c00c7364e9af15e42d2e2f2d909449b))

* chore: rename `gitlab/__version__.py` -&gt; `gitlab/_version.py`

It is confusing to have a `gitlab/__version__.py` because we also
create a variable `gitlab.__version__` which can conflict with
`gitlab/__version__.py`.

For example in `gitlab/const.py` we have to know that
`gitlab.__version__` is a module and not the variable due to the
ordering of imports. But in most other usage `gitlab.__version__` is a
version string.

To reduce confusion make the name of the version file
`gitlab/_version.py`. ([`b981ce7`](https://github.com/python-gitlab/python-gitlab/commit/b981ce7fed88c5d86a3fffc4ee3f99be0b958c1d))

* chore: create return type-hints for `get_id()` &amp; `encoded_id`

Create return type-hints for `RESTObject.get_id()` and
`RESTObject.encoded_id`. Previously was saying they return Any. Be
more precise in saying they can return either: None, str, or int. ([`0c3a1d1`](https://github.com/python-gitlab/python-gitlab/commit/0c3a1d163895f660340a6c2b2f196ad996542518))

* chore(tests): use method `projects.transfer()`

When doing the functional tests use the new function
`projects.transfer` instead of the deprecated function
`projects.transfer_project()` ([`e5af2a7`](https://github.com/python-gitlab/python-gitlab/commit/e5af2a720cb5f97e5a7a5f639095fad76a48f218))

### Documentation

* docs: enhance release docs for CI_JOB_TOKEN usage ([`5d973de`](https://github.com/python-gitlab/python-gitlab/commit/5d973de8a5edd08f38031cf9be2636b0e12f008d))

* docs(changelog): add missing changelog items ([`01755fb`](https://github.com/python-gitlab/python-gitlab/commit/01755fb56a5330aa6fa4525086e49990e57ce50b))

### Fix

* fix(cli): make &#39;per_page&#39; and &#39;page&#39; type explicit ([`d493a5e`](https://github.com/python-gitlab/python-gitlab/commit/d493a5e8685018daa69c92e5942cbe763e5dac62))

* fix(cli): make &#39;timeout&#39; type explicit ([`bbb7df5`](https://github.com/python-gitlab/python-gitlab/commit/bbb7df526f4375c438be97d8cfa0d9ea9d604e7d))

* fix(cli): allow custom methods in managers ([`8dfed0c`](https://github.com/python-gitlab/python-gitlab/commit/8dfed0c362af2c5e936011fd0b488b8b05e8a8a0))

* fix(objects): make resource access tokens and repos available in CLI ([`e0a3a41`](https://github.com/python-gitlab/python-gitlab/commit/e0a3a41ce60503a25fa5c26cf125364db481b207))

### Style

* style: use f-strings where applicable ([`cfed622`](https://github.com/python-gitlab/python-gitlab/commit/cfed62242e93490b8548c79f4ad16bd87de18e3e))

* style: use literals to declare data structures ([`019a40f`](https://github.com/python-gitlab/python-gitlab/commit/019a40f840da30c74c1e74522a7707915061c756))

### Test

* test: add a meta test to make sure that v4/objects/ files are imported

Add a test to make sure that all of the `gitlab/v4/objects/` files are
imported in `gitlab/v4/objects/__init__.py` ([`9c8c804`](https://github.com/python-gitlab/python-gitlab/commit/9c8c8043e6d1d9fadb9f10d47d7f4799ab904e9c))

* test: convert usage of `match_querystring` to `match`

In the `responses` library the usage of `match_querystring` is
deprecated. Convert to using `match` ([`d16e41b`](https://github.com/python-gitlab/python-gitlab/commit/d16e41bda2c355077cbdc419fe2e1d994fdea403))

* test: remove usage of httpmock library

Convert all usage of the `httpmock` library to using the `responses`
library. ([`5254f19`](https://github.com/python-gitlab/python-gitlab/commit/5254f193dc29d8854952aada19a72e5b4fc7ced0))

* test: use &#39;responses&#39; in test_mixins_methods.py

Convert from httmock to responses in test_mixins_methods.py

This leaves only one file left to convert ([`208da04`](https://github.com/python-gitlab/python-gitlab/commit/208da04a01a4b5de8dc34e62c87db4cfa4c0d9b6))

### Unknown

* Merge pull request #1862 from thomasgl-orange/cli-fix-timeout

fix(cli): make &#39;timeout&#39;, &#39;per_page&#39; and &#39;page&#39; type explicit ([`3fb4486`](https://github.com/python-gitlab/python-gitlab/commit/3fb4486045dc988f2e52bd8a843820e3f7e233e2))

* Merge pull request #1858 from python-gitlab/jlvillal/attribute_rename

chore: rename `types.ListAttribute` to `types.CommaSeparatedListAttribute` ([`39e7435`](https://github.com/python-gitlab/python-gitlab/commit/39e74355816700f101cd9bedd10a2873c2cdce1a))

* Merge pull request #1848 from python-gitlab/jlvillal/objects_imported

test: add a meta test to make sure that v4/objects/ files are imported ([`07539c9`](https://github.com/python-gitlab/python-gitlab/commit/07539c9da5e3728fd2c8c495ffc62b375b665f21))

* Merge pull request #1854 from MRigal/docs/small-releases-additions

Enhance releases API docs for CI_JOB_TOKEN usage ([`ff04900`](https://github.com/python-gitlab/python-gitlab/commit/ff049005cc9e5161eddda786e58ed4364639cf02))

* Merge pull request #1845 from python-gitlab/jlvillal/rm_httmock

Remove usage of httmock and clean up deprecations ([`ff4b1cc`](https://github.com/python-gitlab/python-gitlab/commit/ff4b1cc70910b5c45df96547815390736a550b54))

* Merge pull request #1838 from python-gitlab/jlvillal/version_mv

chore: rename `gitlab/__version__.py` to `gitlab/_version.py` ([`8af403c`](https://github.com/python-gitlab/python-gitlab/commit/8af403cb2b1c48acd6e9ebd392554926835c3893))

* Merge pull request #1843 from python-gitlab/jlvillal/rm_httmock

test: use &#39;responses&#39; in test_mixins_methods.py ([`fe14dd5`](https://github.com/python-gitlab/python-gitlab/commit/fe14dd512e59dbb782b2b1c1ab4d94a701a8758f))

* Merge pull request #1841 from python-gitlab/jlvillal/get_id

chore: create return type-hints for `get_id()` &amp; `encoded_id` ([`1ac982a`](https://github.com/python-gitlab/python-gitlab/commit/1ac982ae30781830c2a19a83a014e04a4b6bae41))

* Merge pull request #1840 from python-gitlab/docs/missing-changelog-items

docs(changelog): add missing changelog items ([`a1dbe86`](https://github.com/python-gitlab/python-gitlab/commit/a1dbe86c20b205ce135a7592d5c551e67adfb929))

* Merge pull request #1839 from python-gitlab/jlvillal/catch_warnings

chore(tests): use method `projects.transfer()` ([`48b06a9`](https://github.com/python-gitlab/python-gitlab/commit/48b06a95ad08c5d937d602357895b09d5dcecd9e))

## v3.1.0 (2022-01-14)

### Chore

* chore(groups): use encoded_id for group path ([`868f243`](https://github.com/python-gitlab/python-gitlab/commit/868f2432cae80578d99db91b941332302dd31c89))

* chore(objects): use `self.encoded_id` where applicable

Updated a few remaining usages of `self.id` to use `self.encoded_id`
as for the most part we shouldn&#39;t be using `self.id`

There are now only a few (4 lines of code) remaining uses of
`self.id`, most of which seem that they should stay that way. ([`75758bf`](https://github.com/python-gitlab/python-gitlab/commit/75758bf26bca286ec57d5cef2808560c395ff7ec))

* chore(objects): use `self.encoded_id` where could be a string

Updated a few remaining usages of `self.id` to use `self.encoded_id`
where it could be a string value. ([`c3c3a91`](https://github.com/python-gitlab/python-gitlab/commit/c3c3a914fa2787ae6a1368fe6550585ee252c901))

* chore(projects): fix typing for transfer method

Co-authored-by: John Villalovos &lt;john@sodarock.com&gt; ([`0788fe6`](https://github.com/python-gitlab/python-gitlab/commit/0788fe677128d8c25db1cc107fef860a5a3c2a42))

* chore: ignore intermediate coverage artifacts ([`110ae91`](https://github.com/python-gitlab/python-gitlab/commit/110ae9100b407356925ac2d2ffc65e0f0d50bd70))

* chore: replace usage of utils._url_encode() with utils.EncodedId()

utils.EncodedId() has basically the same functionalityy of using
utils._url_encode(). So remove utils._url_encode() as we don&#39;t need
it. ([`b07eece`](https://github.com/python-gitlab/python-gitlab/commit/b07eece0a35dbc48076c9ec79f65f1e3fa17a872))

* chore: add EncodedId string class to use to hold URL-encoded paths

Add EncodedId string class. This class returns a URL-encoded string
but ensures it will only URL-encode it once even if recursively
called.

Also added some functional tests of &#39;lazy&#39; objects to make sure they
work. ([`a2e7c38`](https://github.com/python-gitlab/python-gitlab/commit/a2e7c383e10509b6eb0fa8760727036feb0807c8))

* chore: add `pprint()` and `pformat()` methods to RESTObject

This is useful in debugging and testing. As can easily print out the
values from an instance in a more human-readable form. ([`d69ba04`](https://github.com/python-gitlab/python-gitlab/commit/d69ba0479a4537bbc7a53f342661c1984382f939))

* chore: add logging to `tests/functional/conftest.py`

I have found trying to debug issues in the functional tests can be
difficult. Especially when trying to figure out failures in the CI
running on Github.

Add logging to `tests/functional/conftest.py` to have a better
understanding of what is happening during a test run which is useful
when trying to troubleshoot issues in the CI. ([`a1ac9ae`](https://github.com/python-gitlab/python-gitlab/commit/a1ac9ae63828ca2012289817410d420da066d8df))

* chore: fix functional test failure if config present

Previously c8256a5933d745f70c7eea0a7d6230b51bac0fbc was done to fix
this but it missed two other failures. ([`c9ed3dd`](https://github.com/python-gitlab/python-gitlab/commit/c9ed3ddc1253c828dc877dcd55000d818c297ee7))

* chore(docs): use admonitions consistently ([`55c67d1`](https://github.com/python-gitlab/python-gitlab/commit/55c67d1fdb81dcfdf8f398b3184fc59256af513d))

* chore(dist): add docs *.md files to sdist

build_sphinx to fail due to setup.cfg warning-is-error ([`d9457d8`](https://github.com/python-gitlab/python-gitlab/commit/d9457d860ae7293ca218ab25e9501b0f796caa57))

* chore: fix missing comma

There was a missing comma which meant the strings were concatenated
instead of being two separate strings. ([`7c59fac`](https://github.com/python-gitlab/python-gitlab/commit/7c59fac12fe69a1080cc227512e620ac5ae40b13))

* chore: add a stale workflow

Use the stale action to close issues and pull-requests with no
activity.

Issues: It will mark them as stale after 60 days and then close
them once they have been stale for 15 days.

Pull-Requests: It will mark pull-requests as stale after 90 days and then close
them once they have been stale for 15 days.

https://github.com/actions/stale

Closes: #1649 ([`2c036a9`](https://github.com/python-gitlab/python-gitlab/commit/2c036a992c9d7fdf6ccf0d3132d9b215c6d197f5))

* chore: add functional test of mergerequest.get()

Add a functional test of test mergerequest.get() and
mergerequest.get(..., lazy=True)

Closes: #1425 ([`a92b55b`](https://github.com/python-gitlab/python-gitlab/commit/a92b55b81eb3586e4144f9332796c94747bf9cfe))

* chore: add temporary banner for v3 ([`a349793`](https://github.com/python-gitlab/python-gitlab/commit/a349793307e3a975bb51f864b48e5e9825f70182))

### Ci

* ci: don&#39;t fail CI if unable to upload the code coverage data

If a CI job can&#39;t upload coverage results to codecov.com it causes the
CI to fail and code can&#39;t be merged. ([`d5b3744`](https://github.com/python-gitlab/python-gitlab/commit/d5b3744c26c8c78f49e69da251cd53da70b180b3))

### Documentation

* docs: update project access token API reference link ([`73ae955`](https://github.com/python-gitlab/python-gitlab/commit/73ae9559dc7f4fba5c80862f0f253959e60f7a0c))

* docs(cli): make examples more easily navigable by generating TOC ([`f33c523`](https://github.com/python-gitlab/python-gitlab/commit/f33c5230cb25c9a41e9f63c0846c1ecba7097ee7))

### Feature

* feat: add support for Groups API method `transfer()` ([`0007006`](https://github.com/python-gitlab/python-gitlab/commit/0007006c184c64128caa96b82dafa3db0ea1101f))

* feat(api): add `project.transfer()` and deprecate `transfer_project()` ([`259668a`](https://github.com/python-gitlab/python-gitlab/commit/259668ad8cb54348e4a41143a45f899a222d2d35))

* feat(api): return result from `SaveMixin.save()`

Return the new object data when calling `SaveMixin.save()`.

Also remove check for `None` value when calling
`self.manager.update()` as that method only returns a dictionary.

Closes: #1081 ([`e6258a4`](https://github.com/python-gitlab/python-gitlab/commit/e6258a4193a0e8d0c3cf48de15b926bebfa289f3))

* feat: add support for Group Access Token API

See https://docs.gitlab.com/ee/api/group_access_tokens.html ([`c01b7c4`](https://github.com/python-gitlab/python-gitlab/commit/c01b7c494192c5462ec673848287ef2a5c9bd737))

### Fix

* fix: use url-encoded ID in all paths

Make sure all usage of the ID in the URL path is encoded. Normally it
isn&#39;t an issue as most IDs are integers or strings which don&#39;t contain
a slash (&#39;/&#39;). But when the ID is a string with a slash character it
will break things.

Add a test case that shows this fixes wikis issue with subpages which
use the slash character.

Closes: #1079 ([`12435d7`](https://github.com/python-gitlab/python-gitlab/commit/12435d74364ca881373d690eab89d2e2baa62a49))

* fix(members): use new *All objects for *AllManager managers

Change it so that:

  GroupMemberAllManager uses GroupMemberAll object
  ProjectMemberAllManager uses ProjectMemberAll object

Create GroupMemberAll and ProjectMemberAll objects that do not support
any Mixin type methods. Previously we were using GroupMember and
ProjectMember which support the `save()` and `delete()` methods but
those methods will not work with objects retrieved using the
`/members/all/` API calls.

`list()` API calls: [1]
  GET /groups/:id/members/all
  GET /projects/:id/members/all

`get()` API calls: [2]
  GET /groups/:id/members/all/:user_id
  GET /projects/:id/members/all/:user_id

Closes: #1825
Closes: #848

[1] https://docs.gitlab.com/ee/api/members.html#list-all-members-of-a-group-or-project-including-inherited-and-invited-members
[2] https://docs.gitlab.com/ee/api/members.html#get-a-member-of-a-group-or-project-including-inherited-and-invited-members ([`755e0a3`](https://github.com/python-gitlab/python-gitlab/commit/755e0a32e8ca96a3a3980eb7d7346a1a899ad58b))

* fix(cli): add missing list filters for environments ([`6f64d40`](https://github.com/python-gitlab/python-gitlab/commit/6f64d4098ed4a890838c6cf43d7a679e6be4ac6c))

* fix(api): services: add missing `lazy` parameter

Commit 8da0b758c589f608a6ae4eeb74b3f306609ba36d added the `lazy`
parameter to the services `get()` method but missed then using the
`lazy` parameter when it called `super(...).get(...)`

Closes: #1828 ([`888f332`](https://github.com/python-gitlab/python-gitlab/commit/888f3328d3b1c82a291efbdd9eb01f11dff0c764))

* fix: broken URL for FAQ about attribute-error-list

The URL was missing a &#39;v&#39; before the version number and thus the page
did not exist.

Previously the URL for python-gitlab 3.0.0 was:
https://python-gitlab.readthedocs.io/en/3.0.0/faq.html#attribute-error-list

Which does not exist.

Change it to:
https://python-gitlab.readthedocs.io/en/v3.0.0/faq.html#attribute-error-list
  add the &#39;v&#39; --------------------------^ ([`1863f30`](https://github.com/python-gitlab/python-gitlab/commit/1863f30ea1f6fb7644b3128debdbb6b7bb218836))

* fix: remove custom URL encoding

We were using `str.replace()` calls to take care of URL encoding
issues.

Switch them to use our `utils._url_encode()` function which itself uses
`urllib.parse.quote()`

Closes: #1356 ([`3d49e5e`](https://github.com/python-gitlab/python-gitlab/commit/3d49e5e6a2bf1c9a883497acb73d7ce7115b804d))

* fix: remove default arguments for mergerequests.merge()

The arguments `should_remove_source_branch` and
`merge_when_pipeline_succeeds` are optional arguments. We should not
be setting any default value for them.

https://docs.gitlab.com/ee/api/merge_requests.html#accept-mr

Closes: #1750 ([`8e589c4`](https://github.com/python-gitlab/python-gitlab/commit/8e589c43fa2298dc24b97423ffcc0ce18d911e3b))

* fix(cli): url-encode path components of the URL

In the CLI we need to make sure the components put into the path
portion of the URL are url-encoded. Otherwise they will be interpreted
as part of the path. For example can specify the project ID as a path,
but in the URL it must be url-encoded or it doesn&#39;t work.

Also stop adding the components of the path as query parameters in the
URL.

Closes: #783
Closes: #1498 ([`ac1c619`](https://github.com/python-gitlab/python-gitlab/commit/ac1c619cae6481833f5df91862624bf0380fef67))

* fix: change to `http_list` for some ProjectCommit methods

Fix the type-hints and use `http_list()` for the ProjectCommits methods:
   - diff()
   - merge_requests()
   - refs()

This will enable using the pagination support we have for lists.

Closes: #1805
Closes: #1231 ([`497e860`](https://github.com/python-gitlab/python-gitlab/commit/497e860d834d0757d1c6532e107416c6863f52f2))

### Test

* test(groups): enable group transfer tests ([`57bb67a`](https://github.com/python-gitlab/python-gitlab/commit/57bb67ae280cff8ac6e946cd3f3797574a574f4a))

### Unknown

* Merge pull request #1836 from python-gitlab/jlvillal/id_to_encodedid

chore(objects): use `self.encoded_id` where applicable ([`2c62d91`](https://github.com/python-gitlab/python-gitlab/commit/2c62d91a67442b21ce3011a2ba5aec7360ca766f))

* Merge pull request #1835 from python-gitlab/jlvillal/id_to_encodedid

chore(objects): use `self.encoded_id` where could be a string ([`34110dd`](https://github.com/python-gitlab/python-gitlab/commit/34110ddf4022340b238ecd964903bf7a6d729e38))

* Merge pull request #1832 from python-gitlab/jlvillal/return_save

feat(api): return result from `SaveMixin.save()` ([`27e0742`](https://github.com/python-gitlab/python-gitlab/commit/27e07422ba98b875f999192318f44f83eb16c501))

* Merge pull request #1834 from python-gitlab/jlvillal/cover_no_fail

ci: don&#39;t fail CI if unable to upload the code coverage data ([`da30753`](https://github.com/python-gitlab/python-gitlab/commit/da30753d4e9d328342ba18df19ccb457e04cab48))

* Merge pull request #1831 from python-gitlab/chore/ignore-coverage

chore: ignore intermediate coverage artifacts ([`8b14ff0`](https://github.com/python-gitlab/python-gitlab/commit/8b14ff0756569dd0afdc364ed95f0bb7393d5407))

* Merge pull request #1819 from python-gitlab/jlvillal/encoded_id

fix: use url-encoded ID in all paths ([`bc48840`](https://github.com/python-gitlab/python-gitlab/commit/bc488401143d486b6d7604b64689a61721b98ac3))

* Merge pull request #1827 from python-gitlab/jlvillal/all_objects

fix: members: use new *All objects for *AllManager managers ([`58e5b25`](https://github.com/python-gitlab/python-gitlab/commit/58e5b2528003d2ee6a55084cc32c6a4bf9aa5bd0))

* Merge pull request #1829 from python-gitlab/jlvillal/lazy_service

fix(api): services: add missing `lazy` parameter ([`824151c`](https://github.com/python-gitlab/python-gitlab/commit/824151ce9238f97118ec21aa8b3267cc7a2cd649))

* Merge pull request #1823 from python-gitlab/jlvillal/fix_url

fix: broken URL for FAQ about attribute-error-list ([`4a000b6`](https://github.com/python-gitlab/python-gitlab/commit/4a000b6c41f0a7ef6121c62a4c598edc20973799))

* Merge pull request #1812 from python-gitlab/jlvillal/pprint

chore: add `pprint()` and `pformat()` methods to RESTObject ([`bdc19b1`](https://github.com/python-gitlab/python-gitlab/commit/bdc19b162ca75c4a2eac70f3f9814ab31de97f7c))

* Merge pull request #1786 from python-gitlab/jlvillal/logging

test: add logging to `tests/functional/conftest.py` ([`ac81272`](https://github.com/python-gitlab/python-gitlab/commit/ac812727c26c9bde4ee5c1115029f2ff4ab1964b))

* Merge pull request #1816 from python-gitlab/jlvillal/remove_replace

fix: remove custom URL encoding ([`24d2766`](https://github.com/python-gitlab/python-gitlab/commit/24d27662caec641a9834b10a3e7269ba63c2b389))

* Merge pull request #1818 from python-gitlab/jlvillal/merge_request_merge_defaults

fix: remove default arguments for mergerequests.merge() ([`0dba899`](https://github.com/python-gitlab/python-gitlab/commit/0dba899c20dda3a9789992a1186cfd718e5b588f))

* Merge pull request #1790 from python-gitlab/jlvillal/parent_attrs

fix(cli): url-encode path components of the URL ([`22a1516`](https://github.com/python-gitlab/python-gitlab/commit/22a151695373ead50ede5cc623130c39bfe1030e))

* Merge pull request #1809 from python-gitlab/jlvillal/list_api

fix: change to `http_list` for some ProjectCommit methods ([`d45b59e`](https://github.com/python-gitlab/python-gitlab/commit/d45b59e800a14460a1ecdad2d750e42aa99bb96e))

* Merge pull request #1813 from derekschrock/missing-dist

chore(dist): add docs *.md files to sdist ([`4861883`](https://github.com/python-gitlab/python-gitlab/commit/48618832f154a8ba56be6edc2662a1b4c697a2f2))

* Merge pull request #1814 from python-gitlab/jlvillal/missing_comma

chore: fix missing comma ([`fd523b3`](https://github.com/python-gitlab/python-gitlab/commit/fd523b311ec7400884001e0d9a4d9756fcc37bdb))

* Merge pull request #1789 from python-gitlab/jlvillal/stale

chore: add a stale workflow ([`9896340`](https://github.com/python-gitlab/python-gitlab/commit/989634055b0c5ab622ac7774b546928a564a31ef))

* Merge pull request #1803 from python-gitlab/jlvillal/test_1425

chore: add functional test of mergerequest.get() ([`bc6c6e6`](https://github.com/python-gitlab/python-gitlab/commit/bc6c6e69e81db5f52afd422d8c8ec0c57a385acd))

## v3.0.0 (2022-01-05)

### Breaking

* feat(cli): allow options from args and environment variables

BREAKING-CHANGE: The gitlab CLI will now accept CLI arguments
and environment variables for its global options in addition
to configuration file options. This may change behavior for
some workflows such as running inside GitLab CI and with
certain environment variables configured. ([`ca58008`](https://github.com/python-gitlab/python-gitlab/commit/ca58008607385338aaedd14a58adc347fa1a41a0))

* fix: stop encoding &#39;.&#39; to &#39;%2E&#39;

Forcing the encoding of &#39;.&#39; to &#39;%2E&#39; causes issues. It also goes
against the RFC:
https://datatracker.ietf.org/doc/html/rfc3986.html#section-2.3

From the RFC:
  For consistency, percent-encoded octets in the ranges of ALPHA
  (%41-%5A and %61-%7A), DIGIT (%30-%39), hyphen (%2D), period (%2E),
  underscore (%5F), or tilde (%7E) should not be created by URI
  producers...

Closes #1006
Related #1356
Related #1561

BREAKING CHANGE: stop encoding &#39;.&#39; to &#39;%2E&#39;. This could potentially be
a breaking change for users who have incorrectly configured GitLab
servers which don&#39;t handle period &#39;.&#39; characters correctly. ([`702e41d`](https://github.com/python-gitlab/python-gitlab/commit/702e41dd0674e76b292d9ea4f559c86f0a99edfe))

* feat(cli): do not require config file to run CLI

BREAKING CHANGE: A config file is no longer needed to run
the CLI. python-gitlab will default to https://gitlab.com
with no authentication if there is no config file provided.
python-gitlab will now also only look for configuration
in the provided PYTHON_GITLAB_CFG path, instead of merging
it with user- and system-wide config files. If the
environment variable is defined and the file cannot be
opened, python-gitlab will now explicitly fail. ([`92a893b`](https://github.com/python-gitlab/python-gitlab/commit/92a893b8e230718436582dcad96175685425b1df))

* feat: remove support for Python 3.6, require 3.7 or higher

Python 3.6 is End-of-Life (EOL) as of 2021-12 as stated in
https://www.python.org/dev/peps/pep-0494/

By dropping support for Python 3.6 and requiring Python 3.7 or higher
it allows python-gitlab to take advantage of new features in Python
3.7, which are documented at:
https://docs.python.org/3/whatsnew/3.7.html

Some of these new features that may be useful to python-gitlab are:
  * PEP 563, postponed evaluation of type annotations.
  * dataclasses: PEP 557 – Data Classes
  * importlib.resources
  * PEP 562, customization of access to module attributes.
  * PEP 560, core support for typing module and generic types.
  * PEP 565, improved DeprecationWarning handling

BREAKING CHANGE: As of python-gitlab 3.0.0, Python 3.6 is no longer
supported. Python 3.7 or higher is required. ([`414009d`](https://github.com/python-gitlab/python-gitlab/commit/414009daebe19a8ae6c36f050dffc690dff40e91))

* chore: rename `master` branch to `main`

BREAKING CHANGE: As of python-gitlab 3.0.0, the default branch for development
has changed from `master` to `main`. ([`545f8ed`](https://github.com/python-gitlab/python-gitlab/commit/545f8ed24124837bf4e55aa34e185270a4b7aeff))

* refactor(objects): remove deprecated branch protect methods

BREAKING CHANGE: remove deprecated branch protect methods in favor of
the more complete protected branches API. ([`9656a16`](https://github.com/python-gitlab/python-gitlab/commit/9656a16f9f34a1aeb8ea0015564bad68ffb39c26))

* fix(api): replace deprecated attribute in delete_in_bulk() (#1536)

BREAKING CHANGE: The deprecated `name_regex` attribute has been removed
in favor of `name_regex_delete`.
(see https://gitlab.com/gitlab-org/gitlab/-/commit/ce99813cf54) ([`c59fbdb`](https://github.com/python-gitlab/python-gitlab/commit/c59fbdb0e9311fa84190579769e3c5c6aeb07fe5))

* fix(objects): rename confusing `to_project_id` argument

BREAKING CHANGE: rename confusing `to_project_id` argument in transfer_project
to `project_id` (`--project-id` in CLI). This is used for the source project,
not for the target namespace. ([`ce4bc0d`](https://github.com/python-gitlab/python-gitlab/commit/ce4bc0daef355e2d877360c6e496c23856138872))

* refactor(objects): remove deprecated constants defined in objects

BREAKING CHANGE: remove deprecated constants defined in
gitlab.v4.objects, and use only gitlab.const module ([`3f320af`](https://github.com/python-gitlab/python-gitlab/commit/3f320af347df05bba9c4d0d3bdb714f7b0f7b9bf))

* refactor(objects): remove deprecated tag release API

BREAKING CHANGE: remove deprecated tag release API.
This was removed in GitLab 14.0 ([`2b8a94a`](https://github.com/python-gitlab/python-gitlab/commit/2b8a94a77ba903ae97228e7ffa3cc2bf6ceb19ba))

* refactor(objects): remove deprecated project.issuesstatistics

BREAKING CHANGE: remove deprecated project.issuesstatistics
in favor of project.issues_statistics ([`ca7777e`](https://github.com/python-gitlab/python-gitlab/commit/ca7777e0dbb82b5d0ff466835a94c99e381abb7c))

* refactor(objects): remove deprecated members.all() method

BREAKING CHANGE: remove deprecated members.all() method
in favor of members_all.list() ([`4d7b848`](https://github.com/python-gitlab/python-gitlab/commit/4d7b848e2a826c58e91970a1d65ed7d7c3e07166))

* refactor(objects): remove deprecated pipelines() method

BREAKING CHANGE: remove deprecated pipelines() methods in favor of pipelines.list() ([`c4f5ec6`](https://github.com/python-gitlab/python-gitlab/commit/c4f5ec6c615e9f83d533a7be0ec19314233e1ea0))

* feat: default to gitlab.com if no URL given

BREAKING CHANGE: python-gitlab will now default to gitlab.com
if no URL is given ([`8236281`](https://github.com/python-gitlab/python-gitlab/commit/823628153ec813c4490e749e502a47716425c0f1))

* fix!: raise error if there is a 301/302 redirection

Before we raised an error if there was a 301, 302 redirect but only
from an http URL to an https URL.  But we didn&#39;t raise an error for
any other redirects.

This caused two problems:

  1. PUT requests that are redirected get changed to GET requests
     which don&#39;t perform the desired action but raise no error. This
     is because the GET response succeeds but since it wasn&#39;t a PUT it
     doesn&#39;t update. See issue:
     https://github.com/python-gitlab/python-gitlab/issues/1432
  2. POST requests that are redirected also got changed to GET
     requests. They also caused hard to debug tracebacks for the user.
     See issue:
     https://github.com/python-gitlab/python-gitlab/issues/1477

Correct this by always raising a RedirectError exception and improve
the exception message to let them know what was redirected.

Closes: #1485
Closes: #1432
Closes: #1477 ([`d56a434`](https://github.com/python-gitlab/python-gitlab/commit/d56a4345c1ae05823b553e386bfa393541117467))

### Chore

* chore: fix typo in MR documentation ([`2254222`](https://github.com/python-gitlab/python-gitlab/commit/2254222094d218b31a6151049c7a43e19c593a97))

* chore(deps): update dependency argcomplete to v2 ([`c6d7e9a`](https://github.com/python-gitlab/python-gitlab/commit/c6d7e9aaddda2f39262b695bb98ea4d90575fcce))

* chore(deps): update dependency requests to v2.27.0 ([`f8c3d00`](https://github.com/python-gitlab/python-gitlab/commit/f8c3d009db3aca004bbd64894a795ee01378cd26))

* chore: add test case to show branch name with period works

Add a test case to show that a branch name with a period can be
fetched with a `get()`

Closes: #1715 ([`ea97d7a`](https://github.com/python-gitlab/python-gitlab/commit/ea97d7a68dd92c6f43dd1f307d63b304137315c4))

* chore(deps): update typing dependencies ([`1f95613`](https://github.com/python-gitlab/python-gitlab/commit/1f9561314a880048227b6f3ecb2ed59e60200d19))

* chore(deps): update dependency mypy to v0.930 ([`ccf8190`](https://github.com/python-gitlab/python-gitlab/commit/ccf819049bf2a9e3be0a0af2a727ab53fc016488))

* chore(deps): upgrade mypy pre-commit hook ([`e19e4d7`](https://github.com/python-gitlab/python-gitlab/commit/e19e4d7cdf9cd04359cd3e95036675c81f4e1dc5))

* chore: fix functional test failure if config present

Fix functional test failure if config present and configured with
token.

Closes: #1791 ([`c8256a5`](https://github.com/python-gitlab/python-gitlab/commit/c8256a5933d745f70c7eea0a7d6230b51bac0fbc))

* chore: ensure reset_gitlab() succeeds

Ensure reset_gitlab() succeeds by waiting to make sure everything has
been deleted as expected. If the timeout is exceeded fail the test.

Not using `wait_for_sidekiq` as it didn&#39;t work. During testing I
didn&#39;t see any sidekiq processes as being busy even though not
everything was deleted. ([`0aa0b27`](https://github.com/python-gitlab/python-gitlab/commit/0aa0b272a90b11951f900b290a8154408eace1de))

* chore: skip a functional test if not using &gt;= py3.9

One of the tests requires Python 3.9 or higher to run. Mark the test
to be skipped if running Python less than 3.9. ([`ac9b595`](https://github.com/python-gitlab/python-gitlab/commit/ac9b59591a954504d4e6e9b576b7a43fcb2ddaaa))

* chore: update version in docker-compose.yml

When running with docker-compose on Ubuntu 20.04 I got the error:

  $ docker-compose up
  ERROR: The Compose file &#39;./docker-compose.yml&#39; is invalid because:
  networks.gitlab-network value Additional properties are not allowed (&#39;name&#39; was unexpected)

Changing the version in the docker-compose.yml file fro &#39;3&#39; to &#39;3.5&#39;
resolved the issue. ([`79321aa`](https://github.com/python-gitlab/python-gitlab/commit/79321aa0e33f0f4bd2ebcdad47769a1a6e81cba8))

* chore: generate artifacts for the docs build in the CI

When building the docs store the created documentation as an artifact
so that it can be viewed.

This will create a html-docs.zip file which can be downloaded
containing the contents of the `build/sphinx/html/` directory. It can
be downloaded, extracted, and then viewed. This can be useful in
reviewing changes to the documentation.

See https://github.com/actions/upload-artifact for more information on
how this works. ([`85b43ae`](https://github.com/python-gitlab/python-gitlab/commit/85b43ae4a96b72e2f29e36a0aca5321ed78f28d2))

* chore: add and document optional parameters for get MR

Add and document (some of the) optional parameters that can be done
for a `project.merge_requests.get()`

Closes #1775 ([`bfa3dbe`](https://github.com/python-gitlab/python-gitlab/commit/bfa3dbe516cfa8824b720ba4c52dd05054a855d7))

* chore(deps): update pre-commit hook alessandrojcm/commitlint-pre-commit-hook to v6 ([`fb9110b`](https://github.com/python-gitlab/python-gitlab/commit/fb9110b1849cea8fa5eddf56f1dbfc1c75f10ad9))

* chore: remove &#39;# type: ignore&#39; for new mypy version

mypy 0.920 now understands the type of
&#39;http.client.HTTPConnection.debuglevel&#39; so we remove the
&#39;type: ignore&#39; comment to make mypy pass ([`34a5f22`](https://github.com/python-gitlab/python-gitlab/commit/34a5f22c81590349645ce7ba46d4153d6de07d8c))

* chore(deps): update dependency mypy to v0.920 ([`a519b2f`](https://github.com/python-gitlab/python-gitlab/commit/a519b2ffe9c8a4bb42d6add5117caecc4bf6ec66))

* chore(deps): update pre-commit hook pycqa/flake8 to v4 ([`98a5592`](https://github.com/python-gitlab/python-gitlab/commit/98a5592ae7246bf927beb3300211007c0fadba2f))

* chore(deps): update pre-commit hook psf/black to v21 ([`b86e819`](https://github.com/python-gitlab/python-gitlab/commit/b86e819e6395a84755aaf42334b17567a1bed5fd))

* chore(deps): update pre-commit hook pycqa/isort to v5.10.1 ([`8ac4f4a`](https://github.com/python-gitlab/python-gitlab/commit/8ac4f4a2ba901de1ad809e4fc2fe787e37703a50))

* chore(ci): enable renovate for pre-commit ([`1ac4329`](https://github.com/python-gitlab/python-gitlab/commit/1ac432900d0f87bb83c77aa62757f8f819296e3e))

* chore: fix unit test if config file exists locally

Closes #1764 ([`c80b3b7`](https://github.com/python-gitlab/python-gitlab/commit/c80b3b75aff53ae228ec05ddf1c1e61d91762846))

* chore: add .env as a file that search tools should not ignore

The `.env` file was not set as a file that should not be ignored by
search tools. We want to have the search tools search any `.env`
files. ([`c9318a9`](https://github.com/python-gitlab/python-gitlab/commit/c9318a9f73c532bee7ba81a41de1fb521ab25ced))

* chore(deps): update dependency sphinx to v4.3.2 ([`2210e56`](https://github.com/python-gitlab/python-gitlab/commit/2210e56da57a9e82e6fd2977453b2de4af14bb6f))

* chore(deps): update dependency types-requests to v2.26.2 ([`ac7e329`](https://github.com/python-gitlab/python-gitlab/commit/ac7e32989a1e7b217b448f57bf2943ff56531983))

* chore: add Python 3.11 testing

Add a unit test for Python 3.11. This will use the latest version of
Python 3.11 that is available from
https://github.com/actions/python-versions/

At this time it is 3.11.0-alpha.2 but will move forward over time
until the final 3.11 release and updates. So 3.11.0, 3.11.1, ... will
be matched. ([`b5ec192`](https://github.com/python-gitlab/python-gitlab/commit/b5ec192157461f7feb326846d4323c633658b861))

* chore(api): temporarily remove topic delete endpoint

It is not yet available upstream. ([`e3035a7`](https://github.com/python-gitlab/python-gitlab/commit/e3035a799a484f8d6c460f57e57d4b59217cd6de))

* chore: fix renovate setup for gitlab docker image ([`49af15b`](https://github.com/python-gitlab/python-gitlab/commit/49af15b3febda5af877da06c3d8c989fbeede00a))

* chore: add get() methods for GetWithoutIdMixin based classes

Add the get() methods for the GetWithoutIdMixin based classes.

Update the tests/meta/test_ensure_type_hints.py tests to check to
ensure that the get methods are defined with the correct return type. ([`d27c50a`](https://github.com/python-gitlab/python-gitlab/commit/d27c50ab9d55dd715a7bee5b0c61317f8565c8bf))

* chore: github workflow: cancel prior running jobs on new push

If new new push is done to a pull-request, then cancel any already
running github workflow jobs in order to conserve resources. ([`fd81569`](https://github.com/python-gitlab/python-gitlab/commit/fd8156991556706f776c508c373224b54ef4e14f))

* chore: add running unit tests on windows/macos

Add running the unit tests on windows-latest and macos-latest with
Python 3.10. ([`ad5d60c`](https://github.com/python-gitlab/python-gitlab/commit/ad5d60c305857a8e8c06ba4f6db788bf918bb63f))

* chore: fix pylint error &#34;expression-not-assigned&#34;

Fix pylint error &#34;expression-not-assigned&#34; and remove check from the
disabled list.

And I personally think it is much more readable now and is less lines
of code. ([`a90eb23`](https://github.com/python-gitlab/python-gitlab/commit/a90eb23cb4903ba25d382c37ce1c0839642ba8fd))

* chore: set pre-commit mypy args to empty list

https://github.com/pre-commit/mirrors-mypy/blob/master/.pre-commit-hooks.yaml

Sets some default args which seem to be interfering with things. Plus
we set all of our args in the `pyproject.toml` file. ([`b67a6ad`](https://github.com/python-gitlab/python-gitlab/commit/b67a6ad1f81dce4670f9820750b411facc01a048))

* chore: run pre-commit on changes to the config file

If .pre-commit-config.yaml or .github/workflows/pre_commit.yml are
updated then run pre-commit. ([`5f10b3b`](https://github.com/python-gitlab/python-gitlab/commit/5f10b3b96d83033805757d72269ad0a771d797d4))

* chore: add initial pylint check

Initial pylint check is added. A LONG list of disabled checks is also
added. In the future we should work through the list and resolve the
errors or disable them on a more granular level. ([`041091f`](https://github.com/python-gitlab/python-gitlab/commit/041091f37f9ab615e121d5aafa37bf23ef72ba13))

* chore: enable &#39;warn_redundant_casts&#39; for mypy

Enable &#39;warn_redundant_casts&#39;for mypy and resolve one issue. ([`f40e9b3`](https://github.com/python-gitlab/python-gitlab/commit/f40e9b3517607c95f2ce2735e3b08ffde8d61e5a))

* chore: enable subset of the &#39;mypy --strict&#39; options that work

Enable the subset of the &#39;mypy --strict&#39; options that work with no
changes to the code. ([`a86d049`](https://github.com/python-gitlab/python-gitlab/commit/a86d0490cadfc2f9fe5490879a1258cf264d5202))

* chore(deps): update dependency black to v21.12b0 ([`ab841b8`](https://github.com/python-gitlab/python-gitlab/commit/ab841b8c63183ca20b866818ab2f930a5643ba5f))

* chore(docs): link to main, not master ([`af0cb4d`](https://github.com/python-gitlab/python-gitlab/commit/af0cb4d18b8bfbc0624ea2771d73544dc1b24b54))

* chore(docs): use builtin autodoc hints ([`5e9c943`](https://github.com/python-gitlab/python-gitlab/commit/5e9c94313f6714a159993cefb488aca3326e3e66))

* chore(docs): load autodoc-typehints module ([`bd366ab`](https://github.com/python-gitlab/python-gitlab/commit/bd366ab9e4b552fb29f7a41564cc180a659bba2f))

* chore: attempt to be more informative for missing attributes

A commonly reported issue from users on Gitter is that they get an
AttributeError for an attribute that should be present. This is often
caused due to the fact that they used the `list()` method to retrieve
the object and objects retrieved this way often only have a subset of
the full data.

Add more details in the AttributeError message that explains the
situation to users. This will hopefully allow them to resolve the
issue.

Update the FAQ in the docs to add a section discussing the issue.

Closes #1138 ([`1839c9e`](https://github.com/python-gitlab/python-gitlab/commit/1839c9e7989163a5cc9a201241942b7faca6e214))

* chore: use constants from gitlab.const module

Have code use constants from the gitlab.const module instead of from
the top-level gitlab module. ([`6b8067e`](https://github.com/python-gitlab/python-gitlab/commit/6b8067e668b6a37a19e07d84e9a0d2d2a99b4d31))

* chore(tests): apply review suggestions ([`381c748`](https://github.com/python-gitlab/python-gitlab/commit/381c748415396e0fe54bb1f41a3303bab89aa065))

* chore(deps): update dependency sphinx to v4.3.1 ([`93a3893`](https://github.com/python-gitlab/python-gitlab/commit/93a3893977d4e3a3e1916a94293e66373b1458fb))

* chore: remove pytest-console-scripts specific config

Remove the pytest-console-scripts specific config from the global
&#39;[pytest]&#39; config section.

Use the command line option `--script-launch-mode=subprocess`

Closes #1713 ([`e80dcb1`](https://github.com/python-gitlab/python-gitlab/commit/e80dcb1dc09851230b00f8eb63e0c78fda060392))

* chore(deps): update typing dependencies ([`8d4c953`](https://github.com/python-gitlab/python-gitlab/commit/8d4c95358c9e61c1cfb89562252498093f56d269))

* chore: remove duplicate/no-op tests from meta/test_ensure_type_hints

Before we were generating 725 tests for the
meta/test_ensure_type_hints.py tests.  Which isn&#39;t a huge concern as
it was fairly fast. But when we had a failure we would usually get two
failures for each problem as the same test was being run multiple
times.

Changed it so that:
  1. Don&#39;t add tests that are not for *Manager classes
  2. Use a set so that we don&#39;t have duplicate tests.

After doing that our generated test count in
meta/test_ensure_type_hints.py went from 725 to 178 tests.

Additionally removed the parsing of `pyproject.toml` to generate files
to ignore as we have finished adding type-hints to all files in
gitlab/v4/objects/. This also means we no longer use the toml library
so remove installation of `types-toml`.

To determine the test count the following command was run:
  $ tox -e py39 -- -k test_ensure_type_hints ([`a2f59f4`](https://github.com/python-gitlab/python-gitlab/commit/a2f59f4e3146b8871a9a1d66ee84295b44321ecb))

* chore: add type-hints to gitlab/v4/objects/files.py ([`0c22bd9`](https://github.com/python-gitlab/python-gitlab/commit/0c22bd921bc74f48fddd0ff7d5e7525086264d54))

* chore: add type-hints to gitlab/v4/objects/labels.py ([`d04e557`](https://github.com/python-gitlab/python-gitlab/commit/d04e557fb09655a0433363843737e19d8e11c936))

* chore: add type-hints to gitlab/v4/objects/sidekiq.py ([`a91a303`](https://github.com/python-gitlab/python-gitlab/commit/a91a303e2217498293cf709b5e05930d41c95992))

* chore: add type-hints to gitlab/v4/objects/services.py ([`8da0b75`](https://github.com/python-gitlab/python-gitlab/commit/8da0b758c589f608a6ae4eeb74b3f306609ba36d))

* chore: add type-hints to gitlab/v4/objects/repositories.py ([`00d7b20`](https://github.com/python-gitlab/python-gitlab/commit/00d7b202efb3a2234cf6c5ce09a48397a40b8388))

* chore: add type-hints to gitlab/v4/objects/pipelines.py ([`cb3ad6c`](https://github.com/python-gitlab/python-gitlab/commit/cb3ad6ce4e2b4a8a3fd0e60031550484b83ed517))

* chore: add type-hints to gitlab/v4/objects/milestones.py ([`8b6078f`](https://github.com/python-gitlab/python-gitlab/commit/8b6078faf02fcf9d966e2b7d1d42722173534519))

* chore: add type-hints to gitlab/v4/objects/jobs.py ([`e8884f2`](https://github.com/python-gitlab/python-gitlab/commit/e8884f21cee29a0ce4428ea2c4b893d1ab922525))

* chore: add type-hints to gitlab/v4/objects/issues.py ([`93e39a2`](https://github.com/python-gitlab/python-gitlab/commit/93e39a2947c442fb91f5c80b34008ca1d27cdf71))

* chore: add type-hints to gitlab/v4/objects/geo_nodes.py ([`13243b7`](https://github.com/python-gitlab/python-gitlab/commit/13243b752fecc54ba8fc0967ba9a223b520f4f4b))

* chore: add type-hints to gitlab/v4/objects/epics.py ([`d4adf8d`](https://github.com/python-gitlab/python-gitlab/commit/d4adf8dfd2879b982ac1314e89df76cb61f2dbf9))

* chore: fix issue with adding type-hints to &#39;manager&#39; attribute

When attempting to add type-hints to the the &#39;manager&#39; attribute into
a RESTObject derived class it would break things.

This was because our auto-manager creation code would automatically
add the specified annotated manager to the &#39;manager&#39; attribute. This
breaks things.

Now check in our auto-manager creation if our attribute is called
&#39;manager&#39;. If so we ignore it. ([`9a451a8`](https://github.com/python-gitlab/python-gitlab/commit/9a451a892d37e0857af5c82c31a96d68ac161738))

* chore(deps): update dependency types-setuptools to v57.4.3 ([`ec2c68b`](https://github.com/python-gitlab/python-gitlab/commit/ec2c68b0b41ac42a2bca61262a917a969cbcbd09))

* chore(deps): update dependency black to v21 ([`5bca87c`](https://github.com/python-gitlab/python-gitlab/commit/5bca87c1e3499eab9b9a694c1f5d0d474ffaca39))

* chore: enable mypy for tests/meta/* ([`ba7707f`](https://github.com/python-gitlab/python-gitlab/commit/ba7707f6161463260710bd2b109b172fd63472a1))

* chore: have renovate upgrade black version (#1700)

renovate is not upgrading the `black` package. There is an open
issue[1] about this.

Also change .commitlintrc.json to allow 200 character footer lines in
the commit message. Otherwise would be forced to split the URL across
multiple lines making it un-clickable :(

Use suggested work-arounds from:
  https://github.com/renovatebot/renovate/issues/7167#issuecomment-904106838
  https://github.com/scop/bash-completion/blob/e7497f6ee8232065ec11450a52a1f244f345e2c6/renovate.json#L34-L38

[1] https://github.com/renovatebot/renovate/issues/7167 ([`21228cd`](https://github.com/python-gitlab/python-gitlab/commit/21228cd14fe18897485728a01c3d7103bff7f822))

* chore: correct test_groups.py test

The test was checking twice if the same group3 was not in the returned
list.  Should have been checking for group3 and group4.

Also added a test that only skipped one group and checked that the
group was not in the returned list and a non-skipped group was in the
list. ([`9c878a4`](https://github.com/python-gitlab/python-gitlab/commit/9c878a4090ddb9c0ef63d06b57eb0e4926276e2f))

* chore: add type-hints to gitlab/v4/objects/merge_request_approvals.py ([`cf3a99a`](https://github.com/python-gitlab/python-gitlab/commit/cf3a99a0c4cf3dc51e946bf29dc44c21b3be9dac))

* chore: check setup.py with mypy

Prior commit 06184daafd5010ba40bb39a0768540b7e98bd171 fixed the
type-hints for setup.py. But missed removing &#39;setup&#39; from the exclude
list in pyproject.toml for mypy checks.

Remove &#39;setup&#39; from the exclude list in pyproject.toml from mypy checks. ([`77cb7a8`](https://github.com/python-gitlab/python-gitlab/commit/77cb7a8f64f25191d84528cc61e1d246296645c9))

* chore: ensure get() methods have correct type-hints

Fix classes which don&#39;t have correct &#39;get()&#39; methods for classes
derived from GetMixin.

Add a unit test which verifies that classes have the correct return
type in their &#39;get()&#39; method. ([`46773a8`](https://github.com/python-gitlab/python-gitlab/commit/46773a82565cef231dc3391c12f296ac307cb95c))

* chore: create a &#39;tests/meta/&#39; directory and put test_mro.py in it

The &#39;test_mro.py&#39; file is not really a unit test but more of a &#39;meta&#39;
check on the validity of the code base. ([`94feb8a`](https://github.com/python-gitlab/python-gitlab/commit/94feb8a5534d43a464b717275846faa75783427e))

* chore: add type-hints to setup.py and check with mypy ([`06184da`](https://github.com/python-gitlab/python-gitlab/commit/06184daafd5010ba40bb39a0768540b7e98bd171))

* chore: add type-hints to gitlab/v4/objects/snippets.py ([`f256d4f`](https://github.com/python-gitlab/python-gitlab/commit/f256d4f6c675576189a72b4b00addce440559747))

* chore(deps): update dependency types-pyyaml to v6.0.1 ([`a544cd5`](https://github.com/python-gitlab/python-gitlab/commit/a544cd576c127ba1986536c9ea32daf2a42649d4))

* chore(deps): update dependency sphinx to v4.3.0 ([`57283fc`](https://github.com/python-gitlab/python-gitlab/commit/57283fca5890f567626235baaf91ca62ae44ff34))

* chore(deps): update dependency types-requests to v2.26.0 ([`7528d84`](https://github.com/python-gitlab/python-gitlab/commit/7528d84762f03b668e9d63a18a712d7224943c12))

* chore(deps): update dependency isort to v5.10.1 ([`2012975`](https://github.com/python-gitlab/python-gitlab/commit/2012975ea96a1d3924d6be24aaf92a025e6ab45b))

* chore(deps): update dependency types-requests to v2.25.12 ([`205ad5f`](https://github.com/python-gitlab/python-gitlab/commit/205ad5fe0934478eb28c014303caa178f5b8c7ec))

* chore: enforce type-hints on most files in gitlab/v4/objects/

  * Add type-hints to some of the files in gitlab/v4/objects/
  * Fix issues detected when adding type-hints
  * Changed mypy exclusion to explicitly list the 13 files that have
    not yet had type-hints added. ([`7828ba2`](https://github.com/python-gitlab/python-gitlab/commit/7828ba2fd13c833c118a673bac09b215587ba33b))

* chore: add type hints for gitlab/v4/objects/commits.py ([`dc096a2`](https://github.com/python-gitlab/python-gitlab/commit/dc096a26f72afcebdac380675749a6991aebcd7c))

* chore(ci): add workflow to lock old issues ([`a7d64fe`](https://github.com/python-gitlab/python-gitlab/commit/a7d64fe5696984aae0c9d6d6b1b51877cc4634cf))

* chore: add type-hints to multiple files in gitlab/v4/objects/

Add and/or check type-hints for the following files
    gitlab.v4.objects.access_requests
    gitlab.v4.objects.applications
    gitlab.v4.objects.broadcast_messages
    gitlab.v4.objects.deployments
    gitlab.v4.objects.keys
    gitlab.v4.objects.merge_trains
    gitlab.v4.objects.namespaces
    gitlab.v4.objects.pages
    gitlab.v4.objects.personal_access_tokens
    gitlab.v4.objects.project_access_tokens
    gitlab.v4.objects.tags
    gitlab.v4.objects.templates
    gitlab.v4.objects.triggers

Add a &#39;get&#39; method with the correct type for Managers derived from
GetMixin. ([`8b75a77`](https://github.com/python-gitlab/python-gitlab/commit/8b75a7712dd1665d4b3eabb0c4594e80ab5e5308))

* chore: add type-hints to gitlab/v4/objects/groups.py

 * Add type-hints to gitlab/v4/objects/groups.py
 * Have share() function update object attributes.
 * Add &#39;get()&#39; method so that type-checkers will understand that
   getting a group is of type Group. ([`94dcb06`](https://github.com/python-gitlab/python-gitlab/commit/94dcb066ef3ff531778ef4efb97824f010b4993f))

* chore: add type-hints to gitlab/v4/objects/merge_requests.py

 * Add type-hints to gitlab/v4/objects/merge_requests.py
 * Add return value to cancel_merge_when_pipeline_succeeds() function
   as GitLab docs show it returns a value.
 * Add return value to approve() function as GitLab docs show it
   returns a value.
 * Add &#39;get()&#39; method so that type-checkers will understand that
   getting a project merge request is of type ProjectMergeRequest. ([`f9c0ad9`](https://github.com/python-gitlab/python-gitlab/commit/f9c0ad939154375b9940bf41a7e47caab4b79a12))

* chore(deps): update dependency isort to v5.10.0 ([`ae62468`](https://github.com/python-gitlab/python-gitlab/commit/ae6246807004b84d3b2acd609a70ce220a0ecc21))

* chore(ci): wait for all coverage jobs before posting comment ([`c7fdad4`](https://github.com/python-gitlab/python-gitlab/commit/c7fdad42f68927d79e0d1963ade3324370b9d0e2))

* chore(deps): update dependency types-pyyaml to v6 ([`0b53c0a`](https://github.com/python-gitlab/python-gitlab/commit/0b53c0a260ab2ec2c5ddb12ca08bfd21a24f7a69))

* chore(deps): update typing dependencies ([`4170dbe`](https://github.com/python-gitlab/python-gitlab/commit/4170dbe00112378a523b0fdf3208e8fa4bc5ef00))

* chore(deps): update dependency flake8 to v4 ([`79785f0`](https://github.com/python-gitlab/python-gitlab/commit/79785f0bee2ef6cc9872f816a78c13583dfb77ab))

* chore(deps): update typing dependencies ([`4eb8ec8`](https://github.com/python-gitlab/python-gitlab/commit/4eb8ec874083adcf86a1781c7866f9dd014f6d27))

* chore(deps): upgrade gitlab-ce to 14.3.2-ce.0 ([`5a1678f`](https://github.com/python-gitlab/python-gitlab/commit/5a1678f43184bd459132102cc13cf8426fe0449d))

* chore(objects): remove non-existing trigger ownership method ([`8dc7f40`](https://github.com/python-gitlab/python-gitlab/commit/8dc7f40044ce8c478769f25a87c5ceb1aa76b595))

* chore: add type-hints to gitlab/v4/objects/users.py

Adding type-hints to gitlab/v4/objects/users.py ([`88988e3`](https://github.com/python-gitlab/python-gitlab/commit/88988e3059ebadd3d1752db60c2d15b7e60e7c46))

* chore(deps): update dependency types-requests to v2.25.9 ([`e3912ca`](https://github.com/python-gitlab/python-gitlab/commit/e3912ca69c2213c01cd72728fd669724926fd57a))

* chore: fix type-check issue shown by new requests-types

types-requests==2.25.9 changed a type-hint. Update code to handle this
change. ([`0ee9aa4`](https://github.com/python-gitlab/python-gitlab/commit/0ee9aa4117b1e0620ba3cade10ccb94944754071))

* chore(deps): update python docker tag to v3.10 ([`b3d6d91`](https://github.com/python-gitlab/python-gitlab/commit/b3d6d91fed4e5b8424e1af9cadb2af5b6cd8162f))

* chore(deps): update dependency sphinx to v4 ([`73745f7`](https://github.com/python-gitlab/python-gitlab/commit/73745f73e5180dd21f450ac4d8cbcca19930e549))

* chore: clean up install docs ([`a5d8b7f`](https://github.com/python-gitlab/python-gitlab/commit/a5d8b7f2a9cf019c82bef1a166d2dc24f93e1992))

* chore: attempt to fix flaky functional test

Add an additional check to attempt to solve the flakiness of the
test_merge_request_should_remove_source_branch() test. ([`487b9a8`](https://github.com/python-gitlab/python-gitlab/commit/487b9a875a18bb3b4e0d49237bb7129d2c6dba2f))

* chore: convert to using type-annotations for managers

Convert our manager usage to be done via type annotations.

Now to define a manager to be used in a RESTObject subclass can simply
do:
      class ExampleClass(CRUDMixin, RESTObject):
          my_manager: MyManager

Any type-annotation that annotates it to be of type *Manager (with the
exception of RESTManager) will cause the manager to be created on the
object. ([`d8de4dc`](https://github.com/python-gitlab/python-gitlab/commit/d8de4dc373dc608be6cf6ba14a2acc7efd3fa7a7))

* chore: improve type-hinting for managers

The &#39;managers&#39; are dynamically created. This unfortunately means that
we don&#39;t have any type-hints for them and so editors which understand
type-hints won&#39;t know that they are valid attributes.

 * Add the type-hints for the managers we define.
 * Add a unit test that makes sure that the type-hints and the
   &#39;_managers&#39; attribute are kept in sync with each other.
 * Add unit test that makes sure specified managers in &#39;_managers&#39;
   have a name ending in &#39;Managers&#39; to keep with current convention.
 * Make RESTObject._managers always present with a default value of
   None.
 * Fix a type-issue revealed now that mypy knows what the type is ([`c9b5d3b`](https://github.com/python-gitlab/python-gitlab/commit/c9b5d3bac8f7c1f779dd57653f718dd0fac4db4b))

* chore(deps): update dependency types-pyyaml to v5.4.10 ([`bdb6cb9`](https://github.com/python-gitlab/python-gitlab/commit/bdb6cb932774890752569ebbc86509e011728ae6))

### Documentation

* docs: switch to Furo and refresh introduction pages ([`ee6b024`](https://github.com/python-gitlab/python-gitlab/commit/ee6b024347bf8a178be1a0998216f2a24c940cee))

* docs: correct documentation for updating discussion note

Closes #1777 ([`ee66f4a`](https://github.com/python-gitlab/python-gitlab/commit/ee66f4a777490a47ad915a3014729a9720bf909b))

* docs: rename documentation files to match names of code files

Rename the merge request related documentation files to match the code
files. This will make it easier to find the documentation quickly.

Rename:
  `docs/gl_objects/mrs.rst -&gt; `docs/gl_objects/merge_requests.rst`
  `docs/gl_objects/mr_approvals.rst -&gt; `docs/gl_objects/merge_request_approvals.rst` ([`ee3f865`](https://github.com/python-gitlab/python-gitlab/commit/ee3f8659d48a727da5cd9fb633a060a9231392ff))

* docs(project): remove redundant encoding parameter ([`fed613f`](https://github.com/python-gitlab/python-gitlab/commit/fed613f41a298e79a975b7f99203e07e0f45e62c))

* docs: use annotations for return types ([`79e785e`](https://github.com/python-gitlab/python-gitlab/commit/79e785e765f4219fe6001ef7044235b82c5e7754))

* docs: only use type annotations for documentation ([`b7dde0d`](https://github.com/python-gitlab/python-gitlab/commit/b7dde0d7aac8dbaa4f47f9bfb03fdcf1f0b01c41))

* docs: update docs to use gitlab.const for constants

Update the docs to use gitlab.const to access constants. ([`b3b0b5f`](https://github.com/python-gitlab/python-gitlab/commit/b3b0b5f1da5b9da9bf44eac33856ed6eadf37dd6))

* docs: add links to the GitLab API docs

Add links to the GitLab API docs for merge_requests.py as it contains
code which spans two different API documentation pages. ([`e3b5d27`](https://github.com/python-gitlab/python-gitlab/commit/e3b5d27bde3e104e520d976795cbcb1ae792fb05))

* docs: fix API delete key example ([`b31bb05`](https://github.com/python-gitlab/python-gitlab/commit/b31bb05c868793e4f0cb4573dad6bf9ca01ed5d9))

* docs(pipelines): document take_ownership method ([`69461f6`](https://github.com/python-gitlab/python-gitlab/commit/69461f6982e2a85dcbf95a0b884abd3f4050c1c7))

* docs(api): document the update method for project variables ([`7992911`](https://github.com/python-gitlab/python-gitlab/commit/7992911896c62f23f25742d171001f30af514a9a))

* docs(api): clarify job token usage with auth()

See issue #1620 ([`3f423ef`](https://github.com/python-gitlab/python-gitlab/commit/3f423efab385b3eb1afe59ad12c2da7eaaa11d76))

* docs: fix a few typos

There are small typos in:
- docs/gl_objects/deploy_tokens.rst
- gitlab/base.py
- gitlab/mixins.py
- gitlab/v4/objects/features.py
- gitlab/v4/objects/groups.py
- gitlab/v4/objects/packages.py
- gitlab/v4/objects/projects.py
- gitlab/v4/objects/sidekiq.py
- gitlab/v4/objects/todos.py

Fixes:
- Should read `treatment` rather than `reatment`.
- Should read `transferred` rather than `transfered`.
- Should read `registered` rather than `registred`.
- Should read `occurred` rather than `occured`.
- Should read `overridden` rather than `overriden`.
- Should read `marked` rather than `maked`.
- Should read `instantiate` rather than `instanciate`.
- Should read `function` rather than `fonction`. ([`7ea4ddc`](https://github.com/python-gitlab/python-gitlab/commit/7ea4ddc4248e314998fd27eea17c6667f5214d1d))

* docs: consolidate changelogs and remove v3 API docs ([`90da8ba`](https://github.com/python-gitlab/python-gitlab/commit/90da8ba0342ebd42b8ec3d5b0d4c5fbb5e701117))

* docs: correct documented return type

repository_archive() returns &#39;bytes&#39; not &#39;str&#39;

https://docs.gitlab.com/ee/api/repositories.html#get-file-archive

Fixes: #1584 ([`acabf63`](https://github.com/python-gitlab/python-gitlab/commit/acabf63c821745bd7e43b7cd3d799547b65e9ed0))

### Feature

* feat(docker): remove custom entrypoint from image

This is no longer needed as all of the configuration
is handled by the CLI and can be passed as arguments. ([`80754a1`](https://github.com/python-gitlab/python-gitlab/commit/80754a17f66ef4cd8469ff0857e0fc592c89796d))

* feat(api): support file format for repository archive ([`83dcabf`](https://github.com/python-gitlab/python-gitlab/commit/83dcabf3b04af63318c981317778f74857279909))

* feat: add support for `squash_option` in Projects

There is an optional `squash_option` parameter which can be used when
creating Projects and UserProjects.

Closes #1744 ([`a246ce8`](https://github.com/python-gitlab/python-gitlab/commit/a246ce8a942b33c5b23ac075b94237da09013fa2))

* feat(api): add support for Topics API ([`e7559bf`](https://github.com/python-gitlab/python-gitlab/commit/e7559bfa2ee265d7d664d7a18770b0a3e80cf999))

* feat: add delete on package_file object ([`124667b`](https://github.com/python-gitlab/python-gitlab/commit/124667bf16b1843ae52e65a3cc9b8d9235ff467e))

* feat(api): add support for epic notes

Added support for notes on group epics

Signed-off-by: Raimund Hook &lt;raimund.hook@exfo.com&gt; ([`7f4edb5`](https://github.com/python-gitlab/python-gitlab/commit/7f4edb53e9413f401c859701d8c3bac4a40706af))

* feat: add support for `projects.groups.list()`

Add support for `projects.groups.list()` endpoint.

Closes #1717 ([`68ff595`](https://github.com/python-gitlab/python-gitlab/commit/68ff595967a5745b369a93d9d18fef48b65ebedb))

* feat(api): add merge trains

Add support for merge trains ([`fd73a73`](https://github.com/python-gitlab/python-gitlab/commit/fd73a738b429be0a2642d5b777d5e56a4c928787))

* feat(api): add project milestone promotion

Adds promotion to Project Milestones

Signed-off-by: Raimund Hook &lt;raimund.hook@exfo.com&gt; ([`f068520`](https://github.com/python-gitlab/python-gitlab/commit/f0685209f88d1199873c1f27d27f478706908fd3))

* feat(api): add merge request approval state

Add support for merge request approval state ([`f41b093`](https://github.com/python-gitlab/python-gitlab/commit/f41b0937aec5f4a5efba44155cc2db77c7124e5e))

* feat(api): add project label promotion

Adds a mixin that allows the /promote endpoint to be called.

Signed-off-by: Raimund Hook &lt;raimund.hook@exfo.com&gt; ([`6d7c88a`](https://github.com/python-gitlab/python-gitlab/commit/6d7c88a1fe401d271a34df80943634652195b140))

* feat(objects): support delete package files API ([`4518046`](https://github.com/python-gitlab/python-gitlab/commit/45180466a408cd51c3ea4fead577eb0e1f3fe7f8))

* feat(objects): list starred projects of a user ([`47a5606`](https://github.com/python-gitlab/python-gitlab/commit/47a56061421fc8048ee5cceaf47ac031c92aa1da))

* feat(build): officially support and test python 3.10 ([`c042ddc`](https://github.com/python-gitlab/python-gitlab/commit/c042ddc79ea872fc8eb8fe4e32f4107a14ffed2d))

* feat(objects): support Create and Revoke personal access token API ([`e19314d`](https://github.com/python-gitlab/python-gitlab/commit/e19314dcc481b045ba7a12dd76abedc08dbdf032))

* feat: allow global retry_transient_errors setup

`retry_transient_errors` can now be set through the Gitlab instance and global configuration

Documentation for API usage has been updated and missing tests have been added. ([`3b1d3a4`](https://github.com/python-gitlab/python-gitlab/commit/3b1d3a41da7e7228f3a465d06902db8af564153e))

### Fix

* fix: handle situation where GitLab does not return values

If a query returns more than 10,000 records than the following values
are NOT returned:
  x.total_pages
  x.total

Modify the code to allow no value to be set for these values. If there
is not a value returned the functions will now return None.

Update unit test so no longer `xfail`

https://docs.gitlab.com/ee/user/gitlab_com/index.html#pagination-response-headers

Closes #1686 ([`cb824a4`](https://github.com/python-gitlab/python-gitlab/commit/cb824a49af9b0d155b89fe66a4cfebefe52beb7a))

* fix(build): do not include docs in wheel package ([`68a97ce`](https://github.com/python-gitlab/python-gitlab/commit/68a97ced521051afb093cf4fb6e8565d9f61f708))

* fix(api): delete invalid &#39;project-runner get&#39; command (#1628)

* fix(api): delete &#39;group-runner get&#39; and &#39;group-runner delete&#39; commands

Co-authored-by: Léo GATELLIER &lt;git@leogatellier.fr&gt; ([`905781b`](https://github.com/python-gitlab/python-gitlab/commit/905781bed2afa33634b27842a42a077a160cffb8))

* fix(build): do not package tests in wheel ([`969dccc`](https://github.com/python-gitlab/python-gitlab/commit/969dccc084e833331fcd26c2a12ddaf448575ab4))

### Refactor

* refactor: deprecate accessing constants from top-level namespace

We are planning on adding enumerated constants into gitlab/const.py,
but if we do that than they will end up being added to the top-level
gitlab namespace. We really want to get users to start using
`gitlab.const.` to access the constant values in the future.

Add the currently defined constants to a list that should not change.
Use a module level __getattr__ function so that we can deprecate
access to the top-level constants.

Add a unit test which verifies we generate a warning when accessing
the top-level constants. ([`c0aa0e1`](https://github.com/python-gitlab/python-gitlab/commit/c0aa0e1c9f7d7914e3062fe6503da870508b27cf))

* refactor: use new-style formatting for named placeholders ([`c0d8810`](https://github.com/python-gitlab/python-gitlab/commit/c0d881064f7c90f6a510db483990776ceb17b9bd))

* refactor: use f-strings for string formatting ([`7925c90`](https://github.com/python-gitlab/python-gitlab/commit/7925c902d15f20abaecdb07af213f79dad91355b))

### Test

* test: reproduce missing pagination headers in tests ([`501f9a1`](https://github.com/python-gitlab/python-gitlab/commit/501f9a1588db90e6d2c235723ba62c09a669b5d2))

* test: drop httmock dependency in test_gitlab.py ([`c764bee`](https://github.com/python-gitlab/python-gitlab/commit/c764bee191438fc4aa2e52d14717c136760d2f3f))

* test(api): fix current user mail count in newer gitlab ([`af33aff`](https://github.com/python-gitlab/python-gitlab/commit/af33affa4888fa83c31557ae99d7bbd877e9a605))

* test(cli): improve basic CLI coverage ([`6b892e3`](https://github.com/python-gitlab/python-gitlab/commit/6b892e3dcb18d0f43da6020b08fd4ba891da3670))

* test(build): add smoke tests for sdist &amp; wheel package ([`b8a47ba`](https://github.com/python-gitlab/python-gitlab/commit/b8a47bae3342400a411fb9bf4bef3c15ba91c98e))

### Unknown

* Merge pull request #1804 from mlegner/patch-1

chore: fix typo in MR documentation ([`1582387`](https://github.com/python-gitlab/python-gitlab/commit/158238779e4608e76138ae437acf80f3175d5580))

* Merge pull request #1800 from python-gitlab/jlvillal/dot_branch

chore: add test case to show branch name with period works ([`896a8c7`](https://github.com/python-gitlab/python-gitlab/commit/896a8c72ed32d6c22a202d86283cab2b7af44522))

* Merge pull request #1799 from python-gitlab/renovate/mypy-0.x

chore(deps): update dependency mypy to v0.930 ([`2323a7c`](https://github.com/python-gitlab/python-gitlab/commit/2323a7c46d88f7161e6a8793271b071ca8328801))

* Merge pull request #1792 from python-gitlab/jlvillal/cli_test

chore: fix functional test failure if config present ([`2ac2a68`](https://github.com/python-gitlab/python-gitlab/commit/2ac2a689defb2f959c4b53b9a179aa80a7178777))

* Merge pull request #1773 from python-gitlab/jlvillal/pagination

fix: handle situation where gitlab.com does not return values ([`a3eafab`](https://github.com/python-gitlab/python-gitlab/commit/a3eafab725ed0a30d1d35207f4941937f0aab886))

* Merge pull request #1783 from python-gitlab/jlvillal/sidekiq

chore: ensure reset_gitlab() succeeds ([`f26bf7d`](https://github.com/python-gitlab/python-gitlab/commit/f26bf7d3a86e4d5d1a43423476a46a381e62e8f9))

* Merge pull request #1782 from python-gitlab/jlvillal/repository_func_tests

chore: skip a functional test if not using &gt;= py3.9 ([`d65ce36`](https://github.com/python-gitlab/python-gitlab/commit/d65ce365ff69a6bec2aa8d306800f6f76cbef842))

* Merge pull request #1781 from python-gitlab/jlvillal/docker_compose

chore: update version in docker-compose.yml ([`171df89`](https://github.com/python-gitlab/python-gitlab/commit/171df891bc3153ae4dd79eac82c57675a0758e4b))

* Merge pull request #1774 from python-gitlab/jlvillal/doc_artifacts

chore: generate artifacts for the docs build in the CI ([`3cb2352`](https://github.com/python-gitlab/python-gitlab/commit/3cb235277716d8b20c91e2518675b7eed2d0e777))

* Merge pull request #1776 from python-gitlab/jlvillal/rebase_in_progress

Add some docs for getting the status of a merge_request rebase ([`e7d4d91`](https://github.com/python-gitlab/python-gitlab/commit/e7d4d9148a1bb8302c63fcd780d8dda416015248))

* Merge pull request #1766 from python-gitlab/jlvillal/leave_dot

fix: stop encoding &#39;.&#39; to &#39;%2E&#39; ([`eef8059`](https://github.com/python-gitlab/python-gitlab/commit/eef8059d63f4c882fca6390ae18e3002e86c90d9))

* Merge pull request #1770 from python-gitlab/renovate/alessandrojcm-commitlint-pre-commit-hook-6.x

chore(deps): update pre-commit hook alessandrojcm/commitlint-pre-commit-hook to v6 ([`182ab92`](https://github.com/python-gitlab/python-gitlab/commit/182ab9243f6777ac3319a68905c7ad6e6bdcd77b))

* Merge pull request #1753 from python-gitlab/renovate/mypy-0.x

chore(deps): update dependency mypy to v0.920 ([`5ea5392`](https://github.com/python-gitlab/python-gitlab/commit/5ea539298df2a8aabeb99bce634ec0eb3a1a903d))

* Merge pull request #1765 from python-gitlab/jlvillal/unit_test_config

chore: fix unit test if config file exists locally ([`ccefe80`](https://github.com/python-gitlab/python-gitlab/commit/ccefe80f150eb50176e52b8c9f5b4d0bdb4f5b43))

* Merge pull request #1757 from python-gitlab/jlvillal/gitignore

chore: add .env as a file that search tools should not ignore ([`3ee061c`](https://github.com/python-gitlab/python-gitlab/commit/3ee061c270de3e3becbcaccaed20ffeba833808e))

* Merge pull request #1746 from python-gitlab/jlvillal/squash_option

feat: add support for `squash_option` in Projects ([`7799cb9`](https://github.com/python-gitlab/python-gitlab/commit/7799cb91efb208e26745672610431f66f1fef4f9))

* Merge pull request #1743 from python-gitlab/feat/cli-without-config-file

feat(cli): do not require config file to run CLI ([`170a4d9`](https://github.com/python-gitlab/python-gitlab/commit/170a4d94acb661cba88e7c55c8ce0b33fa89e845))

* Merge pull request #1742 from python-gitlab/jlvillal/py311_alpha

chore: add Python 3.11 testing ([`74d4e4b`](https://github.com/python-gitlab/python-gitlab/commit/74d4e4b9113b375c5a18bcdf47e03d3fc2ee23d3))

* Merge pull request #1710 from python-gitlab/jlvillal/get_without_id

chore: add get() methods for GetWithoutIdMixin based classes ([`ac5defa`](https://github.com/python-gitlab/python-gitlab/commit/ac5defa0c09822cf2208e66218a37d3ce00ff35b))

* Merge pull request #1733 from simonisateur/fix-package-file-delete

feat: package file delete on package file object ([`2f37ccb`](https://github.com/python-gitlab/python-gitlab/commit/2f37ccb5cd8c487662e86aa077f1deabb27fbc9e))

* Merge pull request #1736 from python-gitlab/jlvillal/workflow

chore: github workflow: cancel prior running jobs on new push ([`4945353`](https://github.com/python-gitlab/python-gitlab/commit/494535337b71592effeca57bb1ff2e735ebeb58a))

* Merge pull request #1726 from python-gitlab/jlvillal/windows

chore: add running unit tests on windows/macos ([`83f36d6`](https://github.com/python-gitlab/python-gitlab/commit/83f36d6de5bf6b6bcb9e56243b414bff0093db72))

* Merge pull request #1738 from python-gitlab/jlvillal/pylint_fixes

chore: fix pylint error &#34;expression-not-assigned&#34; ([`3679591`](https://github.com/python-gitlab/python-gitlab/commit/3679591adabae780a74cb29f10f773666a1f8648))

* Merge pull request #1729 from python-gitlab/jlvillal/pylint

chore: add initial pylint check ([`3a7d6f6`](https://github.com/python-gitlab/python-gitlab/commit/3a7d6f6b7d168f00513266f5770624158f49ca2c))

* Merge pull request #1727 from python-gitlab/jlvillal/mypy_strict_two_steps

Enable more strict mypy checking ([`1c33080`](https://github.com/python-gitlab/python-gitlab/commit/1c33080cf161481baada2afa2710b31675711285))

* Merge pull request #1709 from python-gitlab/docs/sphinx-annotations

docs: only use type annotations for documentation ([`2708f91`](https://github.com/python-gitlab/python-gitlab/commit/2708f91d6f763ab02bdd24262892be66fa33390d))

* Merge pull request #1702 from python-gitlab/jlvillal/attribute_help

chore: attempt to be more informative for missing attributes ([`387e59f`](https://github.com/python-gitlab/python-gitlab/commit/387e59fda12c5b6608b1e59b8d79239891c32252))

* Merge pull request #1694 from python-gitlab/jlvillal/const_explicit

refactor: explicitly import gitlab.const values into top-level namespace ([`e6582a3`](https://github.com/python-gitlab/python-gitlab/commit/e6582a37a691880a69a75a347389eb4e4e95b20e))

* Merge pull request #1721 from python-gitlab/test/cli-coverage

test(cli): improve basic CLI coverage ([`09a973e`](https://github.com/python-gitlab/python-gitlab/commit/09a973ee379d82af05a5080decfaec16d2f4eab3))

* Merge pull request #1714 from python-gitlab/jlvillal/pytest_script_launch_mode

chore: remove pytest-console-scripts specific config ([`1badfeb`](https://github.com/python-gitlab/python-gitlab/commit/1badfeb97d7b5fdf61a3121c49f1e13ced7e2cc0))

* Merge pull request #1712 from StingRayZA/Epicnotes

feat(api): add support for epic notes ([`70b9870`](https://github.com/python-gitlab/python-gitlab/commit/70b9870f929c4db32fd2e1406db2122de9958bfd))

* Merge pull request #1718 from python-gitlab/jlvillal/project_groups

feat: add support for `projects.groups.list()` ([`64f2360`](https://github.com/python-gitlab/python-gitlab/commit/64f2360aecb082baac09cac716f88bd8cc6b443b))

* Merge pull request #1707 from python-gitlab/jlvillal/reduce_meta_tests

chore: remove duplicate/no-op tests from meta/test_ensure_type_hints ([`3225f2c`](https://github.com/python-gitlab/python-gitlab/commit/3225f2cfee740374ef36e5cd6796d2370d0e2344))

* Merge pull request #1695 from python-gitlab/jlvillal/mypy_epics

chore: add type-hints to remaining gitlab/v4/objects/*.py files ([`7ba5995`](https://github.com/python-gitlab/python-gitlab/commit/7ba5995ed472997e6bf98e8ae58107af307a5615))

* Merge pull request #1705 from python-gitlab/jlvillal/drop_py_36

feat: remove support for Python 3.6, require 3.7 or higher ([`a390ec3`](https://github.com/python-gitlab/python-gitlab/commit/a390ec3cdf8d73cc6714b52cd2721a0b9bf570ad))

* Merge pull request #1693 from python-gitlab/jlvillay/mypy_test_meta

chore: enable mypy for tests/meta/* ([`9b78c10`](https://github.com/python-gitlab/python-gitlab/commit/9b78c101309d201a4ff2d1ca7974a7c57cb1ad62))

* Merge pull request #1701 from python-gitlab/jlvillal/func_test

chore: correct test_groups.py test ([`178ec1a`](https://github.com/python-gitlab/python-gitlab/commit/178ec1aa5183b3d042fbde29f53f64c410d6caed))

* Merge pull request #1696 from python-gitlab/jlvillal/mypy_merge_request_approvals

chore: add type-hints to gitlab/v4/objects/merge_request_approvals.py ([`2cd15ac`](https://github.com/python-gitlab/python-gitlab/commit/2cd15ac44d8a45fa2d0dcab80cc933e3871db7f8))

* Merge pull request #1692 from python-gitlab/jlvillal/mypy_setup

chore: check setup.py with mypy ([`500895a`](https://github.com/python-gitlab/python-gitlab/commit/500895a518ecadbe89da61d9195350d7e3562566))

* Merge pull request #1681 from python-gitlab/jlvillal/mypy_ensure_type_hints

Ensure get() methods have correct type-hints ([`0951989`](https://github.com/python-gitlab/python-gitlab/commit/0951989cc4eaabc2e2bd82adeb38936d145ddec2))

* Merge pull request #1683 from python-gitlab/jlvillal/mypy_setup

chore: add type-hints to setup.py and check with mypy ([`a553ee7`](https://github.com/python-gitlab/python-gitlab/commit/a553ee76affc6e1030ab0464a8bb998168239f4a))

* Merge pull request #1691 from python-gitlab/jlvillal/mypy_snippets

chore: add type-hints to gitlab/v4/objects/snippets.py ([`f775668`](https://github.com/python-gitlab/python-gitlab/commit/f7756680d4b1d23ea3216458fb5c6bd73f709d5e))

* Merge pull request #1680 from python-gitlab/jlvillal/mypy_small_files_1

chore: enforce type-hints on most files in gitlab/v4/objects/ ([`472b300`](https://github.com/python-gitlab/python-gitlab/commit/472b300154c5e59289d83f0b34d24bc52eb9b6da))

* Merge pull request #1678 from python-gitlab/jlvillal/mypy_commits

chore: add type hints for gitlab/v4/objects/commits.py ([`9a2f54c`](https://github.com/python-gitlab/python-gitlab/commit/9a2f54cf044929dfc3fd89714ce657fa839e35d0))

* Merge pull request #1677 from python-gitlab/chore/ci-lock-threads

chore(ci): add workflow to lock old issues ([`0e6fb5e`](https://github.com/python-gitlab/python-gitlab/commit/0e6fb5e1ead843e466ba1bb1ef6a1461bb7cfd8d))

* Merge pull request #1674 from python-gitlab/jlvillal/mypy_small_files_1

chore: add type-hints to multiple files in gitlab/v4/objects/ ([`cf801d8`](https://github.com/python-gitlab/python-gitlab/commit/cf801d8e643cb6717ea8495b9463908ce12eef34))

* Merge pull request #1668 from python-gitlab/jlvillal/mypy_groups

chore: add type-hints to gitlab/v4/objects/groups.py ([`f3688dc`](https://github.com/python-gitlab/python-gitlab/commit/f3688dcf2dea33f5e17e456f86f8f50ff9312deb))

* Merge pull request #1673 from python-gitlab/jlvillal/mypy_merge_requests

chore: add type-hints to gitlab/v4/objects/merge_requests.py ([`32ea954`](https://github.com/python-gitlab/python-gitlab/commit/32ea954169c6d57948394c5752b06e742da37091))

* Merge pull request #1670 from python-gitlab/jlvillal/merge_requests_api

docs: add links to the GitLab API docs ([`4ab9e92`](https://github.com/python-gitlab/python-gitlab/commit/4ab9e9231bdd7d127b387c7d899e4e6f45767b22))

* Merge pull request #1665 from python-gitlab/renovate/isort-5.x

chore(deps): update dependency isort to v5.10.0 ([`f51d9be`](https://github.com/python-gitlab/python-gitlab/commit/f51d9be224ab509a62efe05e9f8ffb561af62df5))

* Merge pull request #1646 from JacobHenner/add-merge-trains

feat(api): add merge trains ([`ed88bce`](https://github.com/python-gitlab/python-gitlab/commit/ed88bcea09c337fe9ede822ea88e7770a9c6ade0))

* Merge pull request #1655 from StingRayZA/add-milestone-promote

feat(api): add project milestone promotion ([`5ce3b17`](https://github.com/python-gitlab/python-gitlab/commit/5ce3b17f52d9501fea68dee8818e726addb327ac))

* Merge pull request #1641 from JacobHenner/add-merge-request-approval-state

feat(api): add merge request approval state ([`422309f`](https://github.com/python-gitlab/python-gitlab/commit/422309fd11a1e0e9e88862992aed1f826e881f4e))

* Merge pull request #1610 from StingRayZA/add-label-promote

feat(api): add project label promotion ([`853d850`](https://github.com/python-gitlab/python-gitlab/commit/853d8505997b8b052d4421bb64c91dc499cecc90))

* Merge pull request #1629 from python-gitlab/chore/master-to-main

chore: rename `master` branch to `main` ([`63b2070`](https://github.com/python-gitlab/python-gitlab/commit/63b2070a833fad1959567b0e77f5f6533ca8b459))

* Merge pull request #1616 from lmmx/patch-1

Document the `update` method for project variables ([`e851eed`](https://github.com/python-gitlab/python-gitlab/commit/e851eed42d56718699261495698c0ac6ad6c6b22))

* Merge pull request #1624 from axl89/docs-clarification

Clarified CI Job Token auth() caveats ([`49fae96`](https://github.com/python-gitlab/python-gitlab/commit/49fae96ad6456ecca7b34dc61647b370311b4dc3))

* Merge pull request #1515 from JohnVillalovos/jlvillal/mypy_v4_obj_users

chore: add type-hints to gitlab/v4/objects/users.py ([`7753fa2`](https://github.com/python-gitlab/python-gitlab/commit/7753fa2dd009a12ceac47f4444c9a43a83bb53a9))

* Merge pull request #1621 from JohnVillalovos/jlvillal/mypy_dep

chore: fix type-check issue shown by new requests-types ([`e93f84b`](https://github.com/python-gitlab/python-gitlab/commit/e93f84bf89c0fa367c25be341092ec82228f3e08))

* Merge pull request #1619 from python-gitlab/renovate/python-3.x

chore(deps): update python docker tag to v3.10 ([`d97f79d`](https://github.com/python-gitlab/python-gitlab/commit/d97f79d0ec185014747a1e1b9c1f9e78db68dd51))

* Merge pull request #1617 from python-gitlab/feat/support-3.10

feat(build): officially support and test python 3.10 ([`5c17c36`](https://github.com/python-gitlab/python-gitlab/commit/5c17c3664b05ee77b04a464639b39d816d68a6d1))

* Merge pull request #1450 from python-gitlab/renovate/sphinx-4.x

chore(deps): update dependency sphinx to v4 ([`6ce56c2`](https://github.com/python-gitlab/python-gitlab/commit/6ce56c2ad2e99ff7fdb3ee09a132a3eafeab5313))

* Merge pull request #1603 from timgates42/bugfix_typos

docs: fix a few typos ([`227607c`](https://github.com/python-gitlab/python-gitlab/commit/227607ca47c78e3958c6649edb644c7e26d55281))

* Merge pull request #1486 from JohnVillalovos/jlvillal/prohibit_redirection

fix!: raise error if there is a 301/302 redirection ([`3742405`](https://github.com/python-gitlab/python-gitlab/commit/37424050a00d9b4f46aea9e35d9897478452506d))

* Merge pull request #1512 from JohnVillalovos/jlvillal/type_managers

chore: improve type-hinting for managers ([`5247e8b`](https://github.com/python-gitlab/python-gitlab/commit/5247e8bc5298bc017e117e1bfa6717183d07827f))

* Merge pull request #1585 from JohnVillalovos/jlvillal/archive_type

docs: correct documented return type ([`557c7d2`](https://github.com/python-gitlab/python-gitlab/commit/557c7d2d2057e90a8c3f9f25d3f2ca2ec2bece93))

* Merge pull request #1565 from javatarz/master

feat: allow global retry_transient_errors ([`d98d948`](https://github.com/python-gitlab/python-gitlab/commit/d98d948f997e973a42a8a21dfdbba0b435a602df))

## v2.10.1 (2021-08-28)

### Chore

* chore(deps): update dependency types-pyyaml to v5.4.8 ([`2ae1dd7`](https://github.com/python-gitlab/python-gitlab/commit/2ae1dd7d91f4f90123d9dd8ea92c61b38383e31c))

* chore(deps): update dependency types-pyyaml to v5.4.7 ([`ec8be67`](https://github.com/python-gitlab/python-gitlab/commit/ec8be67ddd37302f31b07185cb4778093e549588))

* chore(deps): update codecov/codecov-action action to v2 ([`44f4fb7`](https://github.com/python-gitlab/python-gitlab/commit/44f4fb78bb0b5a18a4703b68a9657796bf852711))

* chore(deps): update typing dependencies ([`34fc210`](https://github.com/python-gitlab/python-gitlab/commit/34fc21058240da564875f746692b3fb4c3f7c4c8))

* chore: define root dir in mypy, not tox ([`7a64e67`](https://github.com/python-gitlab/python-gitlab/commit/7a64e67c8ea09c5e4e041cc9d0807f340d0e1310))

* chore(deps): group typing requirements with mypy additional_dependencies ([`38597e7`](https://github.com/python-gitlab/python-gitlab/commit/38597e71a7dd12751b028f9451587f781f95c18f))

* chore: fix mypy pre-commit hook ([`bd50df6`](https://github.com/python-gitlab/python-gitlab/commit/bd50df6b963af39b70ea2db50fb2f30b55ddc196))

* chore(deps): update dependency types-requests to v2.25.2 ([`4782678`](https://github.com/python-gitlab/python-gitlab/commit/47826789a5f885a87ae139b8c4d8da9d2dacf713))

* chore(deps): update wagoid/commitlint-github-action action to v4 ([`ae97196`](https://github.com/python-gitlab/python-gitlab/commit/ae97196ce8f277082ac28fcd39a9d11e464e6da9))

* chore(deps): update dependency types-requests to v2.25.1 ([`a2d133a`](https://github.com/python-gitlab/python-gitlab/commit/a2d133a995d3349c9b0919dd03abaf08b025289e))

* chore(deps): update precommit hook pycqa/isort to v5.9.3 ([`e1954f3`](https://github.com/python-gitlab/python-gitlab/commit/e1954f355b989007d13a528f1e49e9410256b5ce))

* chore(deps): update dependency isort to v5.9.3 ([`ab46e31`](https://github.com/python-gitlab/python-gitlab/commit/ab46e31f66c36d882cdae0b02e702b37e5a6ff4e))

### Documentation

* docs(mergequests): gl.mergequests.list documentation was missleading ([`5b5a7bc`](https://github.com/python-gitlab/python-gitlab/commit/5b5a7bcc70a4ddd621cbd59e134e7004ad2d9ab9))

### Fix

* fix(mixins): improve deprecation warning

Also note what should be changed ([`57e0187`](https://github.com/python-gitlab/python-gitlab/commit/57e018772492a8522b37d438d722c643594cf580))

* fix(deps): upgrade requests to 2.25.0 (see CVE-2021-33503) ([`ce995b2`](https://github.com/python-gitlab/python-gitlab/commit/ce995b256423a0c5619e2a6c0d88e917aad315ba))

### Unknown

* Merge pull request #1550 from python-gitlab/renovate/codecov-codecov-action-2.x

chore(deps): update codecov/codecov-action action to v2 ([`e54832a`](https://github.com/python-gitlab/python-gitlab/commit/e54832af04119bd46a77b28203e7b68cdcfc601c))

* Merge pull request #1566 from Psycojoker/doc/mergequest_list_missleading_doc

docs(mergerequests): gl.mergerequests.list documentation was misleading ([`8e27721`](https://github.com/python-gitlab/python-gitlab/commit/8e27721554af417623bfe13a2b76710a61fca44d))

* Merge pull request #1571 from python-gitlab/fix-mixings-improve-deprecation-warning

fix(mixins): improve deprecation warning ([`e2fdfbb`](https://github.com/python-gitlab/python-gitlab/commit/e2fdfbb02516360d56d3b7a88a3ef245faf37941))

## v2.10.0 (2021-07-28)

### Chore

* chore(deps): update dependency requests to v2.26.0 ([`d3ea203`](https://github.com/python-gitlab/python-gitlab/commit/d3ea203dc0e4677b7f36c0f80e6a7a0438ea6385))

* chore(deps): update precommit hook pycqa/isort to v5.9.2 ([`521cddd`](https://github.com/python-gitlab/python-gitlab/commit/521cdddc5260ef2ba6330822ec96efc90e1c03e3))

* chore(deps): update dependency isort to v5.9.2 ([`d5dcf1c`](https://github.com/python-gitlab/python-gitlab/commit/d5dcf1cb7e703ec732e12e41d2971726f27a4bdc))

### Documentation

* docs(readme): move contributing docs to CONTRIBUTING.rst

Move the Contributing section of README.rst to CONTRIBUTING.rst, so it
is recognized by GitHub and shown when new contributors make pull
requests. ([`edf49a3`](https://github.com/python-gitlab/python-gitlab/commit/edf49a3d855b1ce4e2bd8a7038b7444ff0ab5fdc))

* docs: add example for mr.merge_ref

Signed-off-by: Matej Focko &lt;mfocko@redhat.com&gt; ([`b30b8ac`](https://github.com/python-gitlab/python-gitlab/commit/b30b8ac27d98ed0a45a13775645d77b76e828f95))

* docs(project): add example on getting a single project using name with namespace ([`ef16a97`](https://github.com/python-gitlab/python-gitlab/commit/ef16a979031a77155907f4160e4f5e159d839737))

### Feature

* feat(api): add merge_ref for merge requests

Support merge_ref on merge requests that returns commit of attempted
merge of the MR.

Signed-off-by: Matej Focko &lt;mfocko@redhat.com&gt; ([`1e24ab2`](https://github.com/python-gitlab/python-gitlab/commit/1e24ab247cc783ae240e94f6cb379fef1e743a52))

* feat(api): add `name_regex_keep` attribute in `delete_in_bulk()` ([`e49ff3f`](https://github.com/python-gitlab/python-gitlab/commit/e49ff3f868cbab7ff81115f458840b5f6d27d96c))

### Fix

* fix(api): do not require Release name for creation

Stop requiring a `name` attribute for creating a Release, since a
release name has not been required since GitLab 12.5. ([`98cd03b`](https://github.com/python-gitlab/python-gitlab/commit/98cd03b7a3085356b5f0f4fcdb7dc729b682f481))

### Test

* test(functional): add mr.merge_ref tests

- Add test for using merge_ref on non-merged MR
- Add test for using merge_ref on MR with conflicts

Signed-off-by: Matej Focko &lt;mfocko@redhat.com&gt; ([`a9924f4`](https://github.com/python-gitlab/python-gitlab/commit/a9924f48800f57fa8036e3ebdf89d1e04b9bf1a1))

### Unknown

* Merge pull request #1537 from antti-mikael/feat/registry-deleteinbulk-keepregex

feat(api): add `name_regex_keep` attribute in `delete_in_bulk()` ([`85713bb`](https://github.com/python-gitlab/python-gitlab/commit/85713bbbecdcec577a72749d2e495f823791b00f))

## v2.9.0 (2021-06-28)

### Chore

* chore: skip EE test case in functional tests ([`953f207`](https://github.com/python-gitlab/python-gitlab/commit/953f207466c53c28a877f2a88da9160acef40643))

* chore(deps): update dependency types-requests to v2 ([`a81a926`](https://github.com/python-gitlab/python-gitlab/commit/a81a926a0979e3272abfb2dc40d2f130d3a0ba5a))

* chore(deps): update dependency mypy to v0.910 ([`02a56f3`](https://github.com/python-gitlab/python-gitlab/commit/02a56f397880b3939b8e737483ac6f95f809ac9c))

* chore(deps): update precommit hook pycqa/isort to v5.9.1 ([`c57ffe3`](https://github.com/python-gitlab/python-gitlab/commit/c57ffe3958c1475c8c79bb86fc4b101d82350d75))

* chore(deps): update dependency isort to v5.9.1 ([`0479dba`](https://github.com/python-gitlab/python-gitlab/commit/0479dba8a26d2588d9616dbeed351b0256f4bf87))

* chore(deps): update dependency types-requests to v0.1.13 ([`c3ddae2`](https://github.com/python-gitlab/python-gitlab/commit/c3ddae239aee6694a09c864158e355675567f3d2))

* chore(deps): update dependency types-requests to v0.1.12 ([`f84c2a8`](https://github.com/python-gitlab/python-gitlab/commit/f84c2a885069813ce80c18542fcfa30cc0d9b644))

* chore(deps): update dependency types-pyyaml to v5 ([`5c22634`](https://github.com/python-gitlab/python-gitlab/commit/5c226343097427b3f45a404db5b78d61143074fb))

* chore(deps): update dependency types-pyyaml to v0.1.9 ([`1f5b3c0`](https://github.com/python-gitlab/python-gitlab/commit/1f5b3c03b2ae451dfe518ed65ec2bec4e80c09d1))

* chore(deps): update dependency types-pyyaml to v0.1.8 ([`e566767`](https://github.com/python-gitlab/python-gitlab/commit/e56676730d3407efdf4255b3ca7ee13b7c36eb53))

* chore(deps): update dependency types-requests to v0.1.11 ([`6ba629c`](https://github.com/python-gitlab/python-gitlab/commit/6ba629c71a4cf8ced7060580a6e6643738bc4186))

* chore(deps): update dependency mypy to v0.902 ([`19c9736`](https://github.com/python-gitlab/python-gitlab/commit/19c9736de06d032569020697f15ea9d3e2b66120))

* chore: add new required type packages for mypy

New version of mypy flagged errors for missing types. Install the
recommended type-* packages that resolve the issues. ([`a7371e1`](https://github.com/python-gitlab/python-gitlab/commit/a7371e19520325a725813e328004daecf9259dd2))

* chore: add type-hints to gitlab/v4/objects/projects.py

Adding type-hints to gitlab/v4/objects/projects.py ([`872dd6d`](https://github.com/python-gitlab/python-gitlab/commit/872dd6defd8c299e997f0f269f55926ce51bd13e))

### Documentation

* docs(tags): remove deprecated functions ([`1b1a827`](https://github.com/python-gitlab/python-gitlab/commit/1b1a827dd40b489fdacdf0a15b0e17a1a117df40))

* docs(release): add update example ([`6254a5f`](https://github.com/python-gitlab/python-gitlab/commit/6254a5ff6f43bd7d0a26dead304465adf1bd0886))

* docs: make Gitlab class usable for intersphinx ([`8753add`](https://github.com/python-gitlab/python-gitlab/commit/8753add72061ea01c508a42d16a27388b1d92677))

### Feature

* feat(api): add group hooks ([`4a7e9b8`](https://github.com/python-gitlab/python-gitlab/commit/4a7e9b86aa348b72925bce3af1e5d988b8ce3439))

* feat(release): allow to update release

Release API now supports PUT. ([`b4c4787`](https://github.com/python-gitlab/python-gitlab/commit/b4c4787af54d9db6c1f9e61154be5db9d46de3dd))

* feat(api): remove responsibility for API inconsistencies for MR reviewers ([`3d985ee`](https://github.com/python-gitlab/python-gitlab/commit/3d985ee8cdd5d27585678f8fbb3eb549818a78eb))

* feat(api): add support for creating/editing reviewers in project merge requests ([`676d1f6`](https://github.com/python-gitlab/python-gitlab/commit/676d1f6565617a28ee84eae20e945f23aaf3d86f))

* feat(api): add MR pipeline manager in favor of pipelines() method ([`954357c`](https://github.com/python-gitlab/python-gitlab/commit/954357c49963ef51945c81c41fd4345002f9fb98))

### Test

* test(releases): integration for release PUT ([`13bf61d`](https://github.com/python-gitlab/python-gitlab/commit/13bf61d07e84cd719931234c3ccbb9977c8f6416))

* test(releases): add unit-tests for release update ([`5b68a5a`](https://github.com/python-gitlab/python-gitlab/commit/5b68a5a73eb90316504d74d7e8065816f6510996))

### Unknown

* Merge pull request #1533 from sugonyak/add-group-hooks

feat(api): add group hooks ([`6abf13a`](https://github.com/python-gitlab/python-gitlab/commit/6abf13a7e25e368da342e7d1da6cfc19915c2dfd))

* Merge pull request #1522 from PPaques/1521-releases-edit

Support Release Update API ([`33d3428`](https://github.com/python-gitlab/python-gitlab/commit/33d342818599f403434e7024097449b6f21babc0))

* Merge pull request #1396 from spyoungtech/merge_request_reviewers

feat(api): add support for creating/editing reviewers in project MRs ([`2c86003`](https://github.com/python-gitlab/python-gitlab/commit/2c86003b36b443203c881dbcefb0ae3908ea1e34))

* Merge pull request #1528 from python-gitlab/renovate/types-requests-2.x

chore(deps): update dependency types-requests to v2 ([`af7aae7`](https://github.com/python-gitlab/python-gitlab/commit/af7aae73e90b54cab7bbf38a8575157416693423))

* Merge pull request #1323 from python-gitlab/feat/mr-pipeline-manager

feat(api): add merge request pipeline manager and deprecate mr.pipelines() method ([`e77554c`](https://github.com/python-gitlab/python-gitlab/commit/e77554c18f87a24ea1367cf9e2e53c48ad6ce3e4))

* Merge pull request #1513 from python-gitlab/renovate/types-pyyaml-0.x

chore(deps): update dependency types-pyyaml to v0.1.8 ([`e3aa023`](https://github.com/python-gitlab/python-gitlab/commit/e3aa0238da48589d41c84e3102611eb21d032ea5))

* Merge pull request #1514 from python-gitlab/renovate/types-requests-0.x

chore(deps): update dependency types-requests to v0.1.11 ([`82973ce`](https://github.com/python-gitlab/python-gitlab/commit/82973ce2bc66d76c5b7d579b71e59bea24e7146f))

* Merge pull request #1504 from python-gitlab/renovate/mypy-0.x

chore(deps): update dependency mypy to v0.902 ([`387e147`](https://github.com/python-gitlab/python-gitlab/commit/387e147adc1c029948f424045c52f9298cb01260))

* Merge pull request #1505 from JohnVillalovos/jlvillal/mypy-deps

chore: add new required type packages for mypy ([`5446423`](https://github.com/python-gitlab/python-gitlab/commit/5446423b7deeb1b634790f941ab399f5f3c6922d))

* Merge pull request #1511 from JohnVillalovos/jlvillal/testing-type-hints

 chore: add type-hints to gitlab/v4/objects/projects.py ([`8e6aaf5`](https://github.com/python-gitlab/python-gitlab/commit/8e6aaf552ac44c21c70f902e5bdf1a2f631e347c))

## v2.8.0 (2021-06-10)

### Chore

* chore(ci): use admin PAT for release workflow ([`d175d41`](https://github.com/python-gitlab/python-gitlab/commit/d175d416d5d94f4806f4262e1f11cfee99fb0135))

* chore: sync create and update attributes for Projects

Sync the create attributes with:
https://docs.gitlab.com/ee/api/projects.html#create-project

Sync the update attributes with documentation at:
https://docs.gitlab.com/ee/api/projects.html#edit-project

As a note the ordering of the attributes was done to match the
ordering of the attributes in the documentation.

Closes: #1497 ([`0044bd2`](https://github.com/python-gitlab/python-gitlab/commit/0044bd253d86800a7ea8ef0a9a07e965a65cc6a5))

* chore: add missing linters to pre-commit and pin versions ([`85bbd1a`](https://github.com/python-gitlab/python-gitlab/commit/85bbd1a5db5eff8a8cea63b2b192aae66030423d))

* chore: add type-hints to gitlab/v4/cli.py

  * Add type-hints to gitlab/v4/cli.py
  * Add required type-hints to other files based on adding type-hints
    to gitlab/v4/cli.py ([`2673af0`](https://github.com/python-gitlab/python-gitlab/commit/2673af0c09a7c5669d8f62c3cc42f684a9693a0f))

* chore: add missing optional create parameter for approval_rules

Add missing optional create parameter (&#39;protected_branch_ids&#39;) to the
project approvalrules.

https://docs.gitlab.com/ee/api/merge_request_approvals.html#create-project-level-rule ([`06a6001`](https://github.com/python-gitlab/python-gitlab/commit/06a600136bdb33bdbd84233303652afb36fb8a1b))

* chore: apply typing suggestions

Co-authored-by: John Villalovos &lt;john@sodarock.com&gt; ([`a11623b`](https://github.com/python-gitlab/python-gitlab/commit/a11623b1aa6998e6520f3975f0f3f2613ceee5fb))

* chore(ci): ignore .python-version from pyenv ([`149953d`](https://github.com/python-gitlab/python-gitlab/commit/149953dc32c28fe413c9f3a0066575caeab12bc8))

* chore: apply suggestions ([`fe7d19d`](https://github.com/python-gitlab/python-gitlab/commit/fe7d19de5aeba675dcb06621cf36ab4169391158))

* chore: clean up tox, pre-commit and requirements ([`237b97c`](https://github.com/python-gitlab/python-gitlab/commit/237b97ceb0614821e59ea041f43a9806b65cdf8c))

* chore: make certain dotfiles searchable by ripgrep

By explicitly NOT excluding the dotfiles we care about to the
.gitignore file we make those files searchable by tools like ripgrep.

By default dotfiles are ignored by ripgrep and other search tools (not
grep) ([`e4ce078`](https://github.com/python-gitlab/python-gitlab/commit/e4ce078580f7eac8cf1c56122e99be28e3830247))

* chore: use built-in function issubclass() instead of getmro()

Code was using inspect.getmro() to replicate the functionality of the
built-in function issubclass()

Switch to using issubclass() ([`81f6386`](https://github.com/python-gitlab/python-gitlab/commit/81f63866593a0486b03a4383d87ef7bc01f4e45f))

* chore: move &#39;gitlab/tests/&#39; dir to &#39;tests/unit/&#39;

Move the &#39;gitlab/tests/&#39; directory to &#39;tests/unit/&#39; so we have all the
tests located under the &#39;tests/&#39; directory. ([`1ac0722`](https://github.com/python-gitlab/python-gitlab/commit/1ac0722bc086b18c070132a0eb53747bbdf2ce0a))

* chore: correct a type-hint ([`046607c`](https://github.com/python-gitlab/python-gitlab/commit/046607cf7fd95c3d25f5af9383fdf10a5bba42c1))

* chore: rename &#39;tools/functional/&#39; to &#39;tests/functional/&#39;

Rename the &#39;tools/functional/&#39; directory to &#39;tests/functional/&#39;

This makes more sense as these are functional tests and not tools.

This was dicussed in:
https://github.com/python-gitlab/python-gitlab/discussions/1468 ([`502715d`](https://github.com/python-gitlab/python-gitlab/commit/502715d99e02105c39b2c5cf0e7457b3256eba0d))

* chore: add a merge_request() pytest fixture and use it

Added a pytest.fixture for merge_request(). Use this fixture in
tools/functional/api/test_merge_requests.py ([`8be2838`](https://github.com/python-gitlab/python-gitlab/commit/8be2838a9ee3e2440d066e2c4b77cb9b55fc3da2))

* chore: simplify functional tests

Add a helper function to have less code duplication in the functional
testing. ([`df9b5f9`](https://github.com/python-gitlab/python-gitlab/commit/df9b5f9226f704a603a7e49c78bc4543b412f898))

* chore: add functional test mr.merge() with long commit message

Functional test to show that
https://github.com/python-gitlab/python-gitlab/issues/1452 is fixed.

Added a functional test to ensure that we can use large commit message
(10_000+ bytes) in mr.merge()

Related to: #1452 ([`cd5993c`](https://github.com/python-gitlab/python-gitlab/commit/cd5993c9d638c2a10879d7e3ac36db06df867e54))

* chore: add a functional test for issue #1120

Going to switch to putting parameters from in the query string to
having them in the &#39;data&#39; body section. Add a functional test to make
sure that we don&#39;t break anything.

https://github.com/python-gitlab/python-gitlab/issues/1120 ([`7d66115`](https://github.com/python-gitlab/python-gitlab/commit/7d66115573c6c029ce6aa00e244f8bdfbb907e33))

* chore: fix import ordering using isort

Fix the import ordering using isort.

https://pycqa.github.io/isort/ ([`f3afd34`](https://github.com/python-gitlab/python-gitlab/commit/f3afd34260d681bbeec974b67012b90d407b7014))

* chore: add an isort tox environment and run isort in CI

  * Add an isort tox environment
  * Run the isort tox environment using --check in the Github CI

https://pycqa.github.io/isort/ ([`dda646e`](https://github.com/python-gitlab/python-gitlab/commit/dda646e8f2ecb733e37e6cffec331b783b64714e))

* chore(deps): update precommit hook alessandrojcm/commitlint-pre-commit-hook to v5 ([`9ff349d`](https://github.com/python-gitlab/python-gitlab/commit/9ff349d21ed40283d60692af5d19d86ed7e72958))

* chore(deps): update gitlab/gitlab-ce docker tag to v13.11.4-ce.0 ([`4223269`](https://github.com/python-gitlab/python-gitlab/commit/4223269608c2e58b837684d20973e02eb70e04c9))

* chore(deps): update dependency docker-compose to v1.29.2 ([`fc241e1`](https://github.com/python-gitlab/python-gitlab/commit/fc241e1ffa995417a969354e37d8fefc21bb4621))

* chore(ci): automate releases ([`0ef497e`](https://github.com/python-gitlab/python-gitlab/commit/0ef497e458f98acee36529e8bda2b28b3310de69))

* chore(ci): ignore debug and type_checking in coverage ([`885b608`](https://github.com/python-gitlab/python-gitlab/commit/885b608194a55bd60ef2a2ad180c5caa8f15f8d2))

* chore: mypy: Disallow untyped definitions

Be more strict and don&#39;t allow untyped definitions on the files we
check.

Also this adds type-hints for two of the decorators so that now
functions/methods decorated by them will have their types be revealed
correctly. ([`6aef2da`](https://github.com/python-gitlab/python-gitlab/commit/6aef2dadf715e601ae9c302be0ad9958345a97f2))

* chore(docs): fix import order for readthedocs build ([`c3de1fb`](https://github.com/python-gitlab/python-gitlab/commit/c3de1fb8ec17f5f704a19df4a56a668570e6fe0a))

* chore(deps): update gitlab/gitlab-ce docker tag to v13.11.3-ce.0 ([`f0b52d8`](https://github.com/python-gitlab/python-gitlab/commit/f0b52d829db900e98ab93883b20e6bd8062089c6))

* chore: have black run at the top-level

This will ensure everything is formatted with black, including
setup.py. ([`429d6c5`](https://github.com/python-gitlab/python-gitlab/commit/429d6c55602f17431201de17e63cdb2c68ac5d73))

* chore: have flake8 check the entire project

Have flake8 run at the top-level of the projects instead of just the
gitlab directory. ([`ab343ef`](https://github.com/python-gitlab/python-gitlab/commit/ab343ef6da708746aa08a972b461a5e51d898f8b))

* chore(deps): update gitlab/gitlab-ce docker tag to v13.11.2-ce.0 ([`434d15d`](https://github.com/python-gitlab/python-gitlab/commit/434d15d1295187d1970ebef01f4c8a44a33afa31))

* chore: remove commented-out print ([`0357c37`](https://github.com/python-gitlab/python-gitlab/commit/0357c37fb40fb6aef175177fab98d0eadc26b667))

* chore: make Get.*Mixin._optional_get_attrs always present

Always create GetMixin/GetWithoutIdMixin._optional_get_attrs attribute
with a default value of tuple()

This way we don&#39;t need to use hasattr() and we will know the type of
the attribute. ([`3c1a0b3`](https://github.com/python-gitlab/python-gitlab/commit/3c1a0b3ba1f529fab38829c9d355561fd36f4f5d))

### Documentation

* docs: fix typo in http_delete docstring ([`5226f09`](https://github.com/python-gitlab/python-gitlab/commit/5226f095c39985d04c34e7703d60814e74be96f8))

* docs(api): add behavior in local attributes when updating objects ([`38f65e8`](https://github.com/python-gitlab/python-gitlab/commit/38f65e8e9994f58bdc74fe2e0e9b971fc3edf723))

* docs: fail on  warnings during sphinx build

This is useful when docs aren&#39;t included in the toctree and don&#39;t show up on RTD. ([`cbd4d52`](https://github.com/python-gitlab/python-gitlab/commit/cbd4d52b11150594ec29b1ce52348c1086a778c8))

### Feature

* feat: add keys endpoint ([`a81525a`](https://github.com/python-gitlab/python-gitlab/commit/a81525a2377aaed797af0706b00be7f5d8616d22))

* feat(objects): add support for Group wikis (#1484)

feat(objects): add support for Group wikis ([`74f5e62`](https://github.com/python-gitlab/python-gitlab/commit/74f5e62ef5bfffc7ba21494d05dbead60b59ecf0))

* feat(objects): add support for generic packages API ([`79d88bd`](https://github.com/python-gitlab/python-gitlab/commit/79d88bde9e5e6c33029e4a9f26c97404e6a7a874))

* feat(api): add deployment mergerequests interface ([`fbbc0d4`](https://github.com/python-gitlab/python-gitlab/commit/fbbc0d400015d7366952a66e4401215adff709f0))

* feat(objects): support all issues statistics endpoints ([`f731707`](https://github.com/python-gitlab/python-gitlab/commit/f731707f076264ebea65afc814e4aca798970953))

* feat(objects): add support for descendant groups API ([`1b70580`](https://github.com/python-gitlab/python-gitlab/commit/1b70580020825adf2d1f8c37803bc4655a97be41))

* feat(objects): add pipeline test report support ([`ee9f96e`](https://github.com/python-gitlab/python-gitlab/commit/ee9f96e61ab5da0ecf469c21cccaafc89130a896))

* feat(objects): add support for billable members ([`fb0b083`](https://github.com/python-gitlab/python-gitlab/commit/fb0b083a0e536a6abab25c9ad377770cc4290fe9))

* feat: add feature to get inherited member for project/group ([`e444b39`](https://github.com/python-gitlab/python-gitlab/commit/e444b39f9423b4a4c85cdb199afbad987df026f1))

* feat: add code owner approval as attribute

The python API was missing the field code_owner_approval_required
as implemented in the GitLab REST API. ([`fdc46ba`](https://github.com/python-gitlab/python-gitlab/commit/fdc46baca447e042d3b0a4542970f9758c62e7b7))

* feat: indicate that we are a typed package

By adding the file: py.typed
it indicates that python-gitlab is a typed package and contains
type-hints.

https://www.python.org/dev/peps/pep-0561/ ([`e4421ca`](https://github.com/python-gitlab/python-gitlab/commit/e4421caafeeb0236df19fe7b9233300727e1933b))

* feat: add support for lists of integers to ListAttribute

Previously ListAttribute only support lists of integers. Now be more
flexible and support lists of items which can be coerced into strings,
for example integers.

This will help us fix issue #1407 by using ListAttribute for the
&#39;iids&#39; field. ([`115938b`](https://github.com/python-gitlab/python-gitlab/commit/115938b3e5adf9a2fb5ecbfb34d9c92bf788035e))

### Fix

* fix: catch invalid type used to initialize RESTObject

Sometimes we have errors where we don&#39;t get a dictionary passed to
RESTObject.__init__() method. This breaks things but in confusing
ways.

Check in the __init__() method and raise an exception if it occurs. ([`c7bcc25`](https://github.com/python-gitlab/python-gitlab/commit/c7bcc25a361f9df440f9c972672e5eec3b057625))

* fix: functional project service test (#1500)

chore: fix functional project service test ([`093db9d`](https://github.com/python-gitlab/python-gitlab/commit/093db9d129e0a113995501755ab57a04e461c745))

* fix: ensure kwargs are passed appropriately for ObjectDeleteMixin ([`4e690c2`](https://github.com/python-gitlab/python-gitlab/commit/4e690c256fc091ddf1649e48dbbf0b40cc5e6b95))

* fix(cli): add missing list filter for jobs ([`b3d1c26`](https://github.com/python-gitlab/python-gitlab/commit/b3d1c267cbe6885ee41b3c688d82890bb2e27316))

* fix: change mr.merge() to use &#39;post_data&#39;

MR https://github.com/python-gitlab/python-gitlab/pull/1121 changed
mr.merge() to use &#39;query_data&#39;. This appears to have been wrong.

From the Gitlab docs they state it should be sent in a payload body
https://docs.gitlab.com/ee/api/README.html#request-payload since
mr.merge() is a PUT request.

  &gt; Request Payload

  &gt; API Requests can use parameters sent as query strings or as a
  &gt; payload body. GET requests usually send a query string, while PUT
  &gt; or POST requests usually send the payload body

Fixes: #1452
Related to: #1120 ([`cb6a3c6`](https://github.com/python-gitlab/python-gitlab/commit/cb6a3c672b9b162f7320c532410713576fbd1cdc))

* fix(cli): fix parsing CLI objects to classnames ([`4252070`](https://github.com/python-gitlab/python-gitlab/commit/42520705a97289ac895a6b110d34d6c115e45500))

* fix(objects): allow lists for filters for in all objects ([`603a351`](https://github.com/python-gitlab/python-gitlab/commit/603a351c71196a7f516367fbf90519f9452f3c55))

* fix(objects): return server data in cancel/retry methods ([`9fed061`](https://github.com/python-gitlab/python-gitlab/commit/9fed06116bfe5df79e6ac5be86ae61017f9a2f57))

* fix(objects): add missing group attributes ([`d20ff4f`](https://github.com/python-gitlab/python-gitlab/commit/d20ff4ff7427519c8abccf53e3213e8929905441))

* fix: iids not working as a list in projects.issues.list()

Set the &#39;iids&#39; values as type ListAttribute so it will pass the list
as a comma-separated string, instead of a list.

Add a functional test.

Closes: #1407 ([`45f806c`](https://github.com/python-gitlab/python-gitlab/commit/45f806c7a7354592befe58a76b7e33a6d5d0fe6e))

* fix: add a check to ensure the MRO is correct

Add a check to ensure the MRO (Method Resolution Order) is correct for classes in
gitlab.v4.objects when doing type-checking.

An example of an incorrect definition:
    class ProjectPipeline(RESTObject, RefreshMixin, ObjectDeleteMixin):
                          ^^^^^^^^^^ This should be at the end.

Correct way would be:
    class ProjectPipeline(RefreshMixin, ObjectDeleteMixin, RESTObject):
                                      Correctly at the end ^^^^^^^^^^

Also fix classes which have the issue. ([`565d548`](https://github.com/python-gitlab/python-gitlab/commit/565d5488b779de19a720d7a904c6fc14c394a4b9))

### Style

* style: clean up test run config ([`dfa40c1`](https://github.com/python-gitlab/python-gitlab/commit/dfa40c1ef85992e85c1160587037e56778ab49c0))

### Test

* test(functional): force delete users on reset

Timing issues between requesting group deletion and GitLab enacting that
deletion resulted in errors while attempting to delete a user which was
the sole owner of said group (see: test_groups). Pass the &#39;hard_delete&#39;
parameter to ensure user deletion. ([`8f81456`](https://github.com/python-gitlab/python-gitlab/commit/8f814563beb601715930ed3b0f89c3871e6e2f33))

* test(api): fix issues test

Was incorrectly using the issue &#39;id&#39; vs &#39;iid&#39;. ([`8e5b0de`](https://github.com/python-gitlab/python-gitlab/commit/8e5b0de7d9b1631aac4e9ac03a286dfe80675040))

* test(functional): explicitly remove deploy tokens on reset

Deploy tokens would remain in the instance if the respective project or
group was deleted without explicitly revoking the deploy tokens first. ([`19a55d8`](https://github.com/python-gitlab/python-gitlab/commit/19a55d80762417311dcebde3f998f5ebc7e78264))

* test(cli): replace assignment expression

This is a feature added in 3.8, removing it allows for the test to run
with lower python versions. ([`11ae11b`](https://github.com/python-gitlab/python-gitlab/commit/11ae11bfa5f9fcb903689805f8d35b4d62ab0c90))

* test(functional): optionally keep containers running post-tests

Additionally updates token creation to make use of `first_or_create()`,
to avoid errors from the script caused by GitLab constraints preventing
duplicate tokens with the same value. ([`4c475ab`](https://github.com/python-gitlab/python-gitlab/commit/4c475abe30c36217da920477f3748e26f3395365))

* test(cli): add more real class scenarios ([`8cf5031`](https://github.com/python-gitlab/python-gitlab/commit/8cf5031a2caf2f39ce920c5f80316cc774ba7a36))

* test(functional): start tracking functional test coverage ([`f875786`](https://github.com/python-gitlab/python-gitlab/commit/f875786ce338b329421f772b181e7183f0fcb333))

* test(functional): add test for skip_groups list filter ([`a014774`](https://github.com/python-gitlab/python-gitlab/commit/a014774a6a2523b73601a1930c44ac259d03a50e))

### Unknown

* Merge pull request #1487 from JohnVillalovos/jlvillal/check_attrs

fix: catch invalid type used to initialize RESTObject ([`600a2c1`](https://github.com/python-gitlab/python-gitlab/commit/600a2c174f5fe274728b98b38d49f009946bcc4f))

* Merge pull request #1489 from python-gitlab/chore/release-action-gh-token

chore(ci): use PAT for release workflow ([`161bb0b`](https://github.com/python-gitlab/python-gitlab/commit/161bb0bf1684374ed01c4e3bc8ebc2f5afe7546b))

* Merge pull request #1499 from JohnVillalovos/jlvillal/projects_attrs

chore: sync create and update attributes for Projects ([`f91b72a`](https://github.com/python-gitlab/python-gitlab/commit/f91b72acdf3b27b6ad398e94f6934b25aca282c7))

* Merge pull request #1490 from benjamb/benbrown/keys

feat: add keys endpoint ([`d3fac50`](https://github.com/python-gitlab/python-gitlab/commit/d3fac50c70078d27d16a3edd69afeb28f5bbcd18))

* Merge pull request #1478 from benjamb/benbrown/keep-containers

Optionally keep containers after running integration tests ([`d981956`](https://github.com/python-gitlab/python-gitlab/commit/d981956a8782d3dc8210498e6b67af7a71abefa2))

* Merge pull request #1483 from JohnVillalovos/jlvillal/mypy_cli

chore: add type-hints to gitlab/v4/cli.py ([`55ae61a`](https://github.com/python-gitlab/python-gitlab/commit/55ae61a563ed6063aa3c8bcb9339c607bee35227))

* Merge pull request #1488 from JohnVillalovos/jlvillal/add_missing_option

chore: add missing optional create parameter for approval_rules ([`ac92205`](https://github.com/python-gitlab/python-gitlab/commit/ac922054eb22fcebf05526e8811d52770d34da53))

* Merge pull request #1249 from rmonat/master

feat: add pipeline test report support ([`fb7174e`](https://github.com/python-gitlab/python-gitlab/commit/fb7174e4aea0257eefb18c671285a1ad98222402))

* Merge pull request #1475 from JohnVillalovos/jlvillal/gitignore

chore: make certain dotfiles searchable by ripgrep ([`861d3d2`](https://github.com/python-gitlab/python-gitlab/commit/861d3d28ebca719d06bb004556daa12c24ffec72))

* Merge pull request #1481 from JohnVillalovos/jlvillal/no_getmro

chore: use built-in function issubclass() instead of getmro() ([`489b0d3`](https://github.com/python-gitlab/python-gitlab/commit/489b0d3068b30696f2ddc1dd5d8ad77b613ee914))

* Merge pull request #1474 from JohnVillalovos/jlvillal/mv_unit_tests

chore: move &#39;gitlab/tests/&#39; dir to &#39;tests/unit/&#39; ([`56770ce`](https://github.com/python-gitlab/python-gitlab/commit/56770ce3031809faa3ddba6724626518c2664191))

* Merge pull request #1480 from JohnVillalovos/jlvillal/fix_hint

chore: correct a type-hint ([`8eb911d`](https://github.com/python-gitlab/python-gitlab/commit/8eb911d6fd7bf95ed50bd893350ce997cbc31558))

* Merge pull request #1469 from JohnVillalovos/jlvillal/test_directory

chore: rename &#39;tools/functional/&#39; to &#39;tests/functional/&#39; ([`90ecf2f`](https://github.com/python-gitlab/python-gitlab/commit/90ecf2f91129ffa0cfb5db58300fbd11638d4ecc))

* Merge pull request #1465 from JohnVillalovos/jlvillal/fix_1452_query_parameters

Switch mr.merge() to use post_data (was using query_data) ([`9beff0d`](https://github.com/python-gitlab/python-gitlab/commit/9beff0d484b5fe86e2cd31f20cf00a309e09cf75))

* Merge pull request #1456 from python-gitlab/feat/billable-members

feat(objects): add support for billable members ([`184b94b`](https://github.com/python-gitlab/python-gitlab/commit/184b94bbe8da5595b06d187e30041e3331b6db8b))

* Merge pull request #1463 from JohnVillalovos/jlvillal/isort

chore: add isort as a checker ([`7824811`](https://github.com/python-gitlab/python-gitlab/commit/7824811e1cb99a0397149b74b0950441cdc21eda))

* Merge pull request #1290 from python-gitlab/fix/parse-cli-objects-camelcase

fix(cli): fix parsing CLI objects to classnames ([`1508eb7`](https://github.com/python-gitlab/python-gitlab/commit/1508eb78a03b8d9429e474b7a6814ffe74517abb))

* Merge pull request #1459 from python-gitlab/renovate/alessandrojcm-commitlint-pre-commit-hook-5.x

chore(deps): update precommit hook alessandrojcm/commitlint-pre-commit-hook to v5 ([`ce0e642`](https://github.com/python-gitlab/python-gitlab/commit/ce0e6427d448dfc18085a5403c793d9208ac3cf2))

* Merge pull request #1376 from Shkurupii/feat-get-inherited-members

feat: get inherited member for project/group ([`f35c73e`](https://github.com/python-gitlab/python-gitlab/commit/f35c73e50918e4d55b70323669f394e52e75cde9))

* Merge pull request #1455 from python-gitlab/renovate/gitlab-gitlab-ce-13.x

chore(deps): update gitlab/gitlab-ce docker tag to v13.11.4-ce.0 ([`c4979a8`](https://github.com/python-gitlab/python-gitlab/commit/c4979a889c8aa6f0c0a5d71b45b3cde7e642b2e7))

* Merge pull request #1451 from python-gitlab/renovate/docker-compose-1.x

chore(deps): update dependency docker-compose to v1.29.2 ([`3628949`](https://github.com/python-gitlab/python-gitlab/commit/3628949b940031bc6f422121f34062faed903e77))

* Merge pull request #1427 from python-gitlab/chore/automate-releases

chore(ci): automate releases ([`25695d9`](https://github.com/python-gitlab/python-gitlab/commit/25695d9fbf5bc51bb56694dd5ecedeef3c172105))

* Merge pull request #1448 from python-gitlab/docs/local-object-attributes

docs(api): add behavior in local attributes when updating objects ([`b0b2113`](https://github.com/python-gitlab/python-gitlab/commit/b0b2113d46a0db0664bb9ac5fda4730a217f8a2e))

* Merge pull request #1449 from python-gitlab/chore/ignore-typing-coverage

chore(ci): ignore debug and type_checking in coverage ([`62b544d`](https://github.com/python-gitlab/python-gitlab/commit/62b544dca37c390fb0d0f8004efbdd8aa5f43b77))

* Merge pull request #1440 from python-gitlab/test/functional-test-coverage

test(functional): start tracking functional test coverage ([`0d3b8ae`](https://github.com/python-gitlab/python-gitlab/commit/0d3b8aea752f487db22f22be87de3cde247f9ffb))

* Merge pull request #1420 from python-gitlab/fix/missing-list-attributes

fix(objects): make lists work for filters in all objects ([`45edae9`](https://github.com/python-gitlab/python-gitlab/commit/45edae9d65aced6fbd41fe68463418c6e4ca39ee))

* Merge pull request #1444 from python-gitlab/fix/return-retry-cancel-output

fix(objects): return server data in cancel/retry methods ([`1ddb54a`](https://github.com/python-gitlab/python-gitlab/commit/1ddb54a0b4605964477a0d5c5b8a895afe9c3989))

* Merge pull request #1409 from JohnVillalovos/jlvillal/untyped_defs

chore: mypy: Disallow untyped definitions ([`562fbbd`](https://github.com/python-gitlab/python-gitlab/commit/562fbbd83c0fabdf9f45d199a2bdd8f61595c4b0))

* Merge pull request #1442 from python-gitlab/chore/fix-readthedocs

chore(docs): fix import order for readthedocs build ([`b563cdc`](https://github.com/python-gitlab/python-gitlab/commit/b563cdc1a6cd585647fc53722081dceb6f7b4466))

* Merge pull request #1441 from python-gitlab/docs/no-manpages-warnings

docs: fail on warnings during sphinx build ([`e46cacf`](https://github.com/python-gitlab/python-gitlab/commit/e46cacf83ca11e9af5636ce9331c2acb61a9446c))

* Merge pull request #1438 from python-gitlab/fix/missing-group-attributes

fix(objects): add missing group attributes ([`5061972`](https://github.com/python-gitlab/python-gitlab/commit/5061972f7852002927805d82f133239d48141eb9))

* Merge pull request #1434 from python-gitlab/renovate/docker-gitlab-gitlab-ce-13.x

chore(deps): update gitlab/gitlab-ce docker tag to v13.11.3-ce.0 ([`1e6305e`](https://github.com/python-gitlab/python-gitlab/commit/1e6305e865d4e586f2fa3a5f638095d0c885e224))

* Merge pull request #1437 from daniellanner/feat/api-code-owner-approval

feat: add code owner approval as attribute ([`d61e669`](https://github.com/python-gitlab/python-gitlab/commit/d61e669e0e1f8530e996578f74336e73e1061e45))

* Merge pull request #1433 from JohnVillalovos/jlvillal/black

chore: have black run at the top-level ([`09ef8d4`](https://github.com/python-gitlab/python-gitlab/commit/09ef8d405c8c0bd4ac2af076304113f0c7e544e2))

* Merge pull request #1429 from JohnVillalovos/jlvillal/flake8

chore: have flake8 check the entire project ([`b498ebd`](https://github.com/python-gitlab/python-gitlab/commit/b498ebd804461031e2d2d391f77dfbbcf0d2e281))

* Merge pull request #1421 from JohnVillalovos/jlvillal/typed_gitlab

feat: indicate that we are a typed package ([`98891eb`](https://github.com/python-gitlab/python-gitlab/commit/98891eb2c52051134fd3046a4ef5d7b0a6af8fec))

* Merge pull request #1413 from JohnVillalovos/jlvillal/1407

fix: iids not working as a list in projects.issues.list() ([`a6b6cd4`](https://github.com/python-gitlab/python-gitlab/commit/a6b6cd4b598ab6eddcf3986486d43e5cdc990e09))

* Merge pull request #1352 from JohnVillalovos/jlvillal/fix_mro

fix: add a check to ensure the MRO is correct ([`909aa9a`](https://github.com/python-gitlab/python-gitlab/commit/909aa9a02b8a0eb2faed747bfbf5839c53266129))

* Merge pull request #1415 from JohnVillalovos/jlvillal/list_attribute_int

feat: add support for lists of integers to ListAttribute ([`dde01c7`](https://github.com/python-gitlab/python-gitlab/commit/dde01c70c2bbac4d1b35211b81347f4363219777))

* Merge pull request #1412 from JohnVillalovos/jlvillal/optional_get_attrs

chore: make Get.*Mixin._optional_get_attrs always present ([`5b81d7d`](https://github.com/python-gitlab/python-gitlab/commit/5b81d7d25e5deefa4333098ebb5bc646fcee2c8d))

## v2.7.1 (2021-04-26)

### Fix

* fix(files): do not url-encode file paths twice ([`8e25cec`](https://github.com/python-gitlab/python-gitlab/commit/8e25cecce3c0a19884a8d231ee1a672b80e94398))

### Unknown

* Merge pull request #1418 from python-gitlab/fix/urlencode-file-paths

fix(files): do not url-encode filepaths twice ([`37af229`](https://github.com/python-gitlab/python-gitlab/commit/37af2296703a481721489a66c5fc554257e34527))

## v2.7.0 (2021-04-25)

### Chore

* chore: bump version to 2.7.0 ([`34c4052`](https://github.com/python-gitlab/python-gitlab/commit/34c4052327018279c9a75d6b849da74eccc8819b))

* chore: make ListMixin._list_filters always present

Always create ListMixin._list_filters attribute with a default value
of tuple().

This way we don&#39;t need to use hasattr() and we will know the type of
the attribute. ([`8933113`](https://github.com/python-gitlab/python-gitlab/commit/89331131b3337308bacb0c4013e80a4809f3952c))

* chore: make RESTObject._short_print_attrs always present

Always create RESTObject._short_print_attrs with a default value of
None.

This way we don&#39;t need to use hasattr() and we will know the type of
the attribute. ([`6d55120`](https://github.com/python-gitlab/python-gitlab/commit/6d551208f4bc68d091a16323ae0d267fbb6003b6))

* chore(objects): remove noisy deprecation warning for audit events

It&#39;s mostly an internal thing anyway and can be removed in 3.0.0 ([`2953642`](https://github.com/python-gitlab/python-gitlab/commit/29536423e3e8866eda7118527a49b120fefb4065))

* chore(deps): update gitlab/gitlab-ce docker tag to v13.11.1-ce.0 ([`3088714`](https://github.com/python-gitlab/python-gitlab/commit/308871496041232f555cf4cb055bf7f4aaa22b23))

* chore: fix F841 errors reported by flake8

Local variable name is assigned to but never used

https://www.flake8rules.com/rules/F841.html ([`40f4ab2`](https://github.com/python-gitlab/python-gitlab/commit/40f4ab20ba0903abd3d5c6844fc626eb264b9a6a))

* chore: fix F401 errors reported by flake8

F401: Module imported but unused

https://www.flake8rules.com/rules/F401.html ([`ff21eb6`](https://github.com/python-gitlab/python-gitlab/commit/ff21eb664871904137e6df18308b6e90290ad490))

* chore: fix E711 error reported by flake8

E711: Comparison to none should be &#39;if cond is none:&#39;

https://www.flake8rules.com/rules/E711.html ([`630901b`](https://github.com/python-gitlab/python-gitlab/commit/630901b30911af01da5543ca609bd27bc5a1a44c))

* chore: fix E712 errors reported by flake8

E712: Comparison to true should be &#39;if cond is true:&#39; or &#39;if cond:&#39;

https://www.flake8rules.com/rules/E712.html ([`83670a4`](https://github.com/python-gitlab/python-gitlab/commit/83670a49a3affd2465f8fcbcc3c26141592c1ccd))

* chore: fix E741/E742 errors reported by flake8

Fixes to resolve errors for:
    https://www.flake8rules.com/rules/E741.html
      Do not use variables named &#39;I&#39;, &#39;O&#39;, or &#39;l&#39; (E741)

    https://www.flake8rules.com/rules/E742.html
      Do not define classes named &#39;I&#39;, &#39;O&#39;, or &#39;l&#39; (E742) ([`380f227`](https://github.com/python-gitlab/python-gitlab/commit/380f227a1ecffd5e22ae7aefed95af3b5d830994))

* chore(deps): update gitlab/gitlab-ce docker tag to v13.11.0-ce.0 ([`711896f`](https://github.com/python-gitlab/python-gitlab/commit/711896f20ff81826c58f1f86dfb29ad860e1d52a))

* chore: remove unused function sanitize_parameters()

The function sanitize_parameters() was used when the v3 API was in
use. Since v3 API support has been removed there are no more users of
this function. ([`443b934`](https://github.com/python-gitlab/python-gitlab/commit/443b93482e29fecc12fdbd2329427b37b05ba425))

* chore: fix typo in mr events ([`c5e6fb3`](https://github.com/python-gitlab/python-gitlab/commit/c5e6fb3bc74c509f35f973e291a7551b2b64dba5))

* chore(config): allow simple commands without external script ([`91ffb8e`](https://github.com/python-gitlab/python-gitlab/commit/91ffb8e97e213d2f14340b952630875995ecedb2))

* chore: make lint happy ([`7a7c9fd`](https://github.com/python-gitlab/python-gitlab/commit/7a7c9fd932def75a2f2c517482784e445d83881a))

* chore: make lint happy ([`b5f43c8`](https://github.com/python-gitlab/python-gitlab/commit/b5f43c83b25271f7aff917a9ce8826d39ff94034))

* chore: make lint happy ([`732e49c`](https://github.com/python-gitlab/python-gitlab/commit/732e49c6547c181de8cc56e93b30dc399e87091d))

* chore: add test ([`f8cf1e1`](https://github.com/python-gitlab/python-gitlab/commit/f8cf1e110401dcc6b9b176beb8675513fc1c7d17))

* chore: remove usage of getattr()

Remove usage of getattr(self, &#34;_update_uses_post&#34;, False)

Instead add it to class and set default value to False.

Add a tests that shows it is set to True for the
ProjectMergeRequestApprovalManager and ProjectApprovalManager classes. ([`2afd18a`](https://github.com/python-gitlab/python-gitlab/commit/2afd18aa28742a3267742859a88be6912a803874))

* chore: have _create_attrs &amp; _update_attrs be a namedtuple

Convert _create_attrs and _update_attrs to use a NamedTuple
(RequiredOptional) to help with code readability. Update all code to
use the NamedTuple. ([`aee1f49`](https://github.com/python-gitlab/python-gitlab/commit/aee1f496c1f414c1e30909767d53ae624fe875e7))

* chore(deps): update dependency docker-compose to v1.29.1 ([`a89ec43`](https://github.com/python-gitlab/python-gitlab/commit/a89ec43ee7a60aacd1ac16f0f1f51c4abeaaefef))

* chore(deps): update dependency sphinx to v3.5.4 ([`a886d28`](https://github.com/python-gitlab/python-gitlab/commit/a886d28a893ac592b930ce54111d9ae4e90f458e))

* chore(deps): update gitlab/gitlab-ce docker tag to v13.10.3-ce.0 ([`eabe091`](https://github.com/python-gitlab/python-gitlab/commit/eabe091945d3fe50472059431e599117165a815a))

* chore(deps): update gitlab/gitlab-ce docker tag to v13.10.1-ce.0 ([`1995361`](https://github.com/python-gitlab/python-gitlab/commit/1995361d9a767ad5af5338f4555fa5a3914c7374))

* chore: import audit events in objects ([`35a190c`](https://github.com/python-gitlab/python-gitlab/commit/35a190cfa0902d6a298aba0a3135c5a99edfe0fa))

* chore(deps): update dependency docker-compose to v1.28.6 ([`46b05d5`](https://github.com/python-gitlab/python-gitlab/commit/46b05d525d0ade6f2aadb6db23fadc85ad48cd3d))

* chore(deps): update gitlab/gitlab-ce docker tag to v13.10.0-ce.0 ([`5221e33`](https://github.com/python-gitlab/python-gitlab/commit/5221e33768fe1e49456d5df09e3f50b46933c8a4))

* chore(deps): update gitlab/gitlab-ce docker tag to v13.9.4-ce.0 ([`939f769`](https://github.com/python-gitlab/python-gitlab/commit/939f769e7410738da2e1c5d502caa765f362efdd))

* chore: fix package file test naming ([`8c80268`](https://github.com/python-gitlab/python-gitlab/commit/8c802680ae7d3bff13220a55efeed9ca79104b10))

* chore: add _create_attrs &amp; _update_attrs to RESTManager

Add the attributes: _create_attrs and _update_attrs to the RESTManager
class. This is so that we stop using getattr() if we don&#39;t need to.

This also helps with type-hints being available for these attributes. ([`147f05d`](https://github.com/python-gitlab/python-gitlab/commit/147f05d43d302d9a04bc87d957c79ce9e54cdaed))

* chore(deps): update gitlab/gitlab-ce docker tag to v13.9.3-ce.0 ([`2ddf45f`](https://github.com/python-gitlab/python-gitlab/commit/2ddf45fed0b28e52d31153d9b1e95d0cae05e9f5))

* chore: make _types always present in RESTManager

We now create _types = {} in RESTManager class.

By making _types always present in RESTManager it makes the code
simpler. We no longer have to do:
   types = getattr(self, &#34;_types&#34;, {})

And the type checker now understands the type. ([`924f83e`](https://github.com/python-gitlab/python-gitlab/commit/924f83eb4b5e160bd231efc38e2eea0231fa311f))

* chore: add type-hints for gitlab/mixins.py

  * Added type-hints for gitlab/mixins.py
  * Changed use of filter with a lambda expression to
    list-comprehension. mypy was not able to understand the previous
    code. Also list-comprehension is better :) ([`baea721`](https://github.com/python-gitlab/python-gitlab/commit/baea7215bbbe07c06b2ca0f97a1d3d482668d887))

* chore: add type hints to gitlab/base.py:RESTManager

Add some additional type hints to gitlab/base.py ([`9c55593`](https://github.com/python-gitlab/python-gitlab/commit/9c55593ae6a7308176710665f8bec094d4cadc2e))

* chore: put assert statements inside &#39;if TYPE_CHECKING:&#39;

To be safe that we don&#39;t assert while running, put the assert
statements, which are used by mypy to check that types are correct,
inside an &#39;if TYPE_CHECKING:&#39; block.

Also, instead of asserting that the item is a dict, instead assert
that it is not a requests.Response object. Theoretically the JSON
could return as a list or dict, though at this time we are assuming a
dict. ([`b562458`](https://github.com/python-gitlab/python-gitlab/commit/b562458f063c6be970f58c733fe01ec786798549))

* chore(deps): update dependency sphinx to v3.5.2 ([`9dee5c4`](https://github.com/python-gitlab/python-gitlab/commit/9dee5c420633bc27e1027344279c47862f7b16da))

* chore(deps): update gitlab/gitlab-ce docker tag to v13.9.2-ce.0 ([`933ba52`](https://github.com/python-gitlab/python-gitlab/commit/933ba52475e5dae4cf7c569d8283e60eebd5b7b6))

* chore: del &#39;import *&#39; in gitlab/v4/objects/project_access_tokens.py

Remove usage of &#39;import *&#39; in
gitlab/v4/objects/project_access_tokens.py. ([`9efbe12`](https://github.com/python-gitlab/python-gitlab/commit/9efbe1297d8d32419b8f04c3758ca7c83a95f199))

* chore: disallow incomplete type defs

Don&#39;t allow a partially annotated function definition. Either none of
the function is annotated or all of it must be.

Update code to ensure no-more partially annotated functions.

Update gitlab/cli.py with better type-hints. Changed Tuple[Any, ...]
to Tuple[str, ...] ([`907634f`](https://github.com/python-gitlab/python-gitlab/commit/907634fe4d0d30706656b8bc56260b5532613e62))

* chore(api): move repository endpoints into separate module ([`1ed154c`](https://github.com/python-gitlab/python-gitlab/commit/1ed154c276fb2429d3b45058b9314d6391dbff02))

* chore: add and fix some type-hints in gitlab/client.py

Was able to figure out better type-hints for gitlab/client.py ([`8837207`](https://github.com/python-gitlab/python-gitlab/commit/88372074a703910ba533237e6901e5af4c26c2bd))

* chore: add additional type-hints for gitlab/base.py

Add type-hints for the variables which are set via self.__dict__

mypy doesn&#39;t see them when they are assigned via self.__dict__. So
declare them in the class definition. ([`ad72ef3`](https://github.com/python-gitlab/python-gitlab/commit/ad72ef35707529058c7c680f334c285746b2f690))

* chore: add type-hints to gitlab/client.py

Adding some initial type-hints to gitlab/client.py ([`c9e5b4f`](https://github.com/python-gitlab/python-gitlab/commit/c9e5b4f6285ec94d467c7c10c45f4e2d5f656430))

* chore: remove import of gitlab.utils from __init__.py

Initially when extracting out the gitlab/client.py code we tried to
remove this but functional tests failed.

Later we fixed the functional test that was failing, so now remove the
unneeded import. ([`39b9183`](https://github.com/python-gitlab/python-gitlab/commit/39b918374b771f1d417196ca74fa04fe3968c412))

* chore: improve type-hints for gitlab/base.py

Determined the base class for obj_cls and adding type-hints for it. ([`cbd43d0`](https://github.com/python-gitlab/python-gitlab/commit/cbd43d0b4c95e46fc3f1cffddc6281eced45db4a))

* chore: add type-hints to gitlab/cli.py ([`10b7b83`](https://github.com/python-gitlab/python-gitlab/commit/10b7b836d31fbe36a7096454287004b46a7799dd))

* chore(deps): update dependency docker-compose to v1.28.5 ([`f4ab558`](https://github.com/python-gitlab/python-gitlab/commit/f4ab558f2cd85fe716e24f3aa4ede5db5b06e7c4))

* chore(deps): update wagoid/commitlint-github-action action to v3 ([`b3274cf`](https://github.com/python-gitlab/python-gitlab/commit/b3274cf93dfb8ae85e4a636a1ffbfa7c48f1c8f6))

* chore: add type-hints to gitlab/const.py ([`a10a777`](https://github.com/python-gitlab/python-gitlab/commit/a10a7777caabd6502d04f3947a317b5b0ac869f2))

* chore: add type hints to gitlab/utils.py ([`acd9294`](https://github.com/python-gitlab/python-gitlab/commit/acd9294fac52a636a016a7a3c14416b10573da28))

* chore: add type-hints to gitlab/config.py ([`213e563`](https://github.com/python-gitlab/python-gitlab/commit/213e5631b1efce11f8a1419cd77df5d9da7ec0ac))

* chore: remove usage of &#39;from ... import *&#39;

In gitlab/v4/objects/*.py remove usage of:
  * from gitlab.base import *
  * from gitlab.mixins import *

Change them to:
  * from gitlab.base import CLASS_NAME
  * from gitlab.mixins import CLASS_NAME

Programmatically update code to explicitly import needed classes only.

After the change the output of:
  $ flake8 gitlab/v4/objects/*py | grep &#39;REST\|Mixin&#39;

Is empty. Before many messages about unable to determine if it was a
valid name. ([`c83eaf4`](https://github.com/python-gitlab/python-gitlab/commit/c83eaf4f395300471311a67be34d8d306c2b3861))

* chore(deps): update gitlab/gitlab-ce docker tag to v13.9.1-ce.0 ([`f6fd995`](https://github.com/python-gitlab/python-gitlab/commit/f6fd99530d70f2a7626602fd9132b628bb968eab))

* chore: remove unused function _construct_url()

The function _construct_url() was used by the v3 API. All usage of the
function was removed in commit
fe89b949922c028830dd49095432ba627d330186 ([`009d369`](https://github.com/python-gitlab/python-gitlab/commit/009d369f08e46d1e059b98634ff8fe901357002d))

* chore: add type hints to gitlab/base.py ([`3727cbd`](https://github.com/python-gitlab/python-gitlab/commit/3727cbd21fc40b312573ca8da56e0f6cf9577d08))

* chore: remove usage of &#39;from ... import *&#39; in client.py

In gitlab/client.py remove usage of:
  * from gitlab.const import *
  * from gitlab.exceptions import *

Change them to:
  * import gitlab.const
  * import gitlab.exceptions

Update code to explicitly reference things in gitlab.const and
gitlab.exceptions

A flake8 run no longer lists any undefined variables. Before it listed
possible undefined variables. ([`bf0c8c5`](https://github.com/python-gitlab/python-gitlab/commit/bf0c8c5d123a7ad0587cb97c3aafd97ab2a9dabf))

* chore: explicitly import gitlab.v4.objects/cli

As we only support the v4 Gitlab API, explicitly import
gitlab.v4.objects and gitlab.v4.clie instead of dynamically importing
it depending on the API version.

This has the added benefit of mypy being able to type check the Gitlab
__init__() function as currently it will fail if we enable type
checking of __init__() it will fail.

Also, this also helps by not confusing tools like pyinstaller/cx_freeze with
dynamic imports so you don&#39;t need hooks for standalone executables. And
according to https://docs.gitlab.com/ee/api/,

    &#34;GraphQL co-exists with the current v4 REST API. If we have a v5 API, this
    should be a compatibility layer on top of GraphQL.&#34; ([`233b79e`](https://github.com/python-gitlab/python-gitlab/commit/233b79ed442aac66faf9eb4b0087ea126d6dffc5))

* chore(deps): update gitlab/gitlab-ce docker tag to v13.9.0-ce.0 ([`3aef19c`](https://github.com/python-gitlab/python-gitlab/commit/3aef19c51713bdc7ca0a84752da3ca22329fd4c4))

* chore(objects): make Project refreshable

Helps getting the real state of the project from the server. ([`958a6aa`](https://github.com/python-gitlab/python-gitlab/commit/958a6aa83ead3fb6be6ec61bdd894ad78346e7bd))

* chore(deps): update dependency docker-compose to v1.28.4 ([`8938484`](https://github.com/python-gitlab/python-gitlab/commit/89384846445be668ca6c861f295297d048cae914))

* chore(tests): remove unused URL segment ([`66f0b6c`](https://github.com/python-gitlab/python-gitlab/commit/66f0b6c23396b849f8653850b099e664daa05eb4))

* chore(deps): update dependency docker-compose to v1.28.3 ([`2358d48`](https://github.com/python-gitlab/python-gitlab/commit/2358d48acbe1c378377fb852b41ec497217d2555))

* chore: remove unused ALLOWED_KEYSET_ENDPOINTS variable

The variable ALLOWED_KEYSET_ENDPOINTS was added in commit
f86ef3bbdb5bffa1348a802e62b281d3f31d33ad.

Then most of that commit was removed in commit
e71fe16b47835aa4db2834e98c7ffc6bdec36723, but ALLOWED_KEYSET_ENDPOINTS
was missed. ([`3d5d5d8`](https://github.com/python-gitlab/python-gitlab/commit/3d5d5d8b13fc8405e9ef3e14be1fd8bd32235221))

* chore(deps): update dependency sphinx to v3.5.1 ([`f916f09`](https://github.com/python-gitlab/python-gitlab/commit/f916f09d3a9cac07246035066d4c184103037026))

* chore: remove Python 2 code

httplib is a Python 2 library. It was renamed to http.client in Python
3.

https://docs.python.org/2.7/library/httplib.html ([`b5d4e40`](https://github.com/python-gitlab/python-gitlab/commit/b5d4e408830caeef86d4c241ac03a6e8781ef189))

* chore(deps): update dependency sphinx to v3.5.0 ([`188c5b6`](https://github.com/python-gitlab/python-gitlab/commit/188c5b692fc195361c70f768cc96c57b3686d4b7))

* chore(deps): update gitlab/gitlab-ce docker tag to v13.8.4-ce.0 ([`832cb88`](https://github.com/python-gitlab/python-gitlab/commit/832cb88992cd7af4903f8b780e9475c03c0e6e56))

* chore(ci): deduplicate PR jobs ([`63918c3`](https://github.com/python-gitlab/python-gitlab/commit/63918c364e281f9716885a0f9e5401efcd537406))

* chore(deps): update gitlab/gitlab-ce docker tag to v13.8.3-ce.0 ([`e6c20f1`](https://github.com/python-gitlab/python-gitlab/commit/e6c20f18f3bd1dabdf181a070b9fdbfe4a442622))

* chore(deps): update precommit hook alessandrojcm/commitlint-pre-commit-hook to v4 ([`505a8b8`](https://github.com/python-gitlab/python-gitlab/commit/505a8b8d7f16e609f0cde70be88a419235130f2f))

* chore(deps): update gitlab/gitlab-ce docker tag to v13.8.2-ce.0 ([`7c12038`](https://github.com/python-gitlab/python-gitlab/commit/7c120384762e23562a958ae5b09aac324151983a))

* chore(deps): update dependency sphinx to v3.4.3 ([`37c992c`](https://github.com/python-gitlab/python-gitlab/commit/37c992c09bfd25f3ddcb026f830f3a79c39cb70d))

### Documentation

* docs(api): add examples for resource state events ([`4d00c12`](https://github.com/python-gitlab/python-gitlab/commit/4d00c12723d565dc0a83670f62e3f5102650d822))

* docs: add information about the gitter community

Add a section in the README.rst about the gitter community. The badge
already exists and is useful but very easy to miss. ([`6ff67e7`](https://github.com/python-gitlab/python-gitlab/commit/6ff67e7327b851fa67be6ad3d82f88ff7cce0dc9))

* docs(api): add release links API docs ([`36d65f0`](https://github.com/python-gitlab/python-gitlab/commit/36d65f03db253d710938c2d827c1124c94a40506))

* docs: add docs and examples for custom user agent ([`a69a214`](https://github.com/python-gitlab/python-gitlab/commit/a69a214ef7f460cef7a7f44351c4861503f9902e))

* docs: change travis-ci badge to githubactions ([`2ba5ba2`](https://github.com/python-gitlab/python-gitlab/commit/2ba5ba244808049aad1ee3b42d1da258a9db9f61))

### Feature

* feat(objects): add support for resource state events API ([`d4799c4`](https://github.com/python-gitlab/python-gitlab/commit/d4799c40bd12ed85d4bb834464fdb36c4dadcab6))

* feat: option to add a helper to lookup token ([`8ecf559`](https://github.com/python-gitlab/python-gitlab/commit/8ecf55926f8e345960560e5c5dd6716199cfb0ec))

* feat(objects): add support for group audit events API ([`2a0fbdf`](https://github.com/python-gitlab/python-gitlab/commit/2a0fbdf9fe98da6c436230be47b0ddb198c7eca9))

* feat: add ProjectPackageFile

Add ProjectPackageFile and the ability to list project package
package_files.

Fixes #1372 ([`b9d469b`](https://github.com/python-gitlab/python-gitlab/commit/b9d469bc4e847ae0301be28a0c70019a7f6ab8b6))

* feat(users): add follow/unfollow API ([`e456869`](https://github.com/python-gitlab/python-gitlab/commit/e456869d98a1b7d07e6f878a0d6a9719c1b10fd4))

* feat(projects): add project access token api ([`1becef0`](https://github.com/python-gitlab/python-gitlab/commit/1becef0253804f119c8a4d0b8b1c53deb2f4d889))

* feat: add an initial mypy test to tox.ini

Add an initial mypy test to test gitlab/base.py and gitlab/__init__.py ([`fdec039`](https://github.com/python-gitlab/python-gitlab/commit/fdec03976a17e0708459ba2fab22f54173295f71))

* feat(objects): add Release Links API support ([`28d7518`](https://github.com/python-gitlab/python-gitlab/commit/28d751811ffda45ff0b1c35e0599b655f3a5a68b))

* feat: add project audit endpoint ([`6660dbe`](https://github.com/python-gitlab/python-gitlab/commit/6660dbefeeffc2b39ddfed4928a59ed6da32ddf4))

* feat: add personal access token API

See: https://docs.gitlab.com/ee/api/personal_access_tokens.html ([`2bb16fa`](https://github.com/python-gitlab/python-gitlab/commit/2bb16fac18a6a91847201c174f3bf1208338f6aa))

* feat(issues): add missing get verb to IssueManager ([`f78ebe0`](https://github.com/python-gitlab/python-gitlab/commit/f78ebe065f73b29555c2dcf17b462bb1037a153e))

* feat: import from bitbucket server

I&#39;d like to use this libary to automate importing Bitbucket Server
repositories into GitLab.  There is a [GitLab API
endpoint](https://docs.gitlab.com/ee/api/import.html#import-repository-from-bitbucket-server)
to do this, but it is not exposed through this library.

* Add an `import_bitbucket_server` method to the `ProjectManager`.  This
  method calls this GitLab API endpoint:
  https://docs.gitlab.com/ee/api/import.html#import-repository-from-bitbucket-server
* Modify `import_gitlab` method docstring for python3 compatibility
* Add a skipped stub test for the existing `import_github` method ([`ff3013a`](https://github.com/python-gitlab/python-gitlab/commit/ff3013a2afeba12811cb3d860de4d0ea06f90545))

* feat(api,cli): make user agent configurable ([`4bb201b`](https://github.com/python-gitlab/python-gitlab/commit/4bb201b92ef0dcc14a7a9c83e5600ba5b118fc33))

### Fix

* fix: only append kwargs as query parameters

Some arguments to `http_request` were being read
from kwargs, but kwargs is where this function
creates query parameters from, by default. In
the absence of a `query_parameters` param, the
function would construct URLs with query
parameters such as `retry_transient_errors=True`
despite those parameters having no meaning to
the API to which the request was sent.

This change names those arguments that are
specific to `http_request` so that they do not
end up as query parameters read from kwargs. ([`b9ecc9a`](https://github.com/python-gitlab/python-gitlab/commit/b9ecc9a8c5d958bd7247946c4e8d29c18163c578))

* fix: only add query_parameters to GitlabList once

Fixes #1386 ([`ca2c3c9`](https://github.com/python-gitlab/python-gitlab/commit/ca2c3c9dee5dc61ea12af5b39d51b1606da32f9c))

* fix: correct ProjectFile.decode() documentation

ProjectFile.decode() returns &#39;bytes&#39; and not &#39;str&#39;.

Update the method&#39;s doc-string and add a type-hint.

ProjectFile.decode() returns the result of a call to
base64.b64decode()

The docs for that function state it returns &#39;bytes&#39;:
https://docs.python.org/3/library/base64.html#base64.b64decode

Fixes: #1403 ([`b180baf`](https://github.com/python-gitlab/python-gitlab/commit/b180bafdf282cd97e8f7b6767599bc42d5470bfa))

* fix: update user&#39;s bool data and avatar

If we want to update email, avatar and do not send email
confirmation change (`skip_reconfirmation` = True), `MultipartEncoder`
will try to encode everything except None and bytes. So it tries to encode bools.
Casting bool&#39;s values to their stringified int representation fix it. ([`3ba27ff`](https://github.com/python-gitlab/python-gitlab/commit/3ba27ffb6ae995c27608f84eef0abe636e2e63da))

* fix(types): prevent __dir__ from producing duplicates ([`5bf7525`](https://github.com/python-gitlab/python-gitlab/commit/5bf7525d2d37968235514d1b93a403d037800652))

* fix: correct some type-hints in gitlab/mixins.py

Commit baea7215bbbe07c06b2ca0f97a1d3d482668d887 introduced type-hints
for gitlab/mixins.py.

After starting to add type-hints to gitlab/v4/objects/users.py
discovered a few errors.

Main error was using &#39;=&#39; instead of &#39;:&#39;. For example:
  _parent = Optional[...] should be _parent: Optional[...]

Resolved those issues. ([`8bd3124`](https://github.com/python-gitlab/python-gitlab/commit/8bd312404cf647674baea792547705ef1948043d))

* fix: argument type was not a tuple as expected

While adding type-hints mypy flagged this as an issue. The third
argument to register_custom_action is supposed to be a tuple. It was
being passed as a string rather than a tuple of strings. ([`062f8f6`](https://github.com/python-gitlab/python-gitlab/commit/062f8f6a917abc037714129691a845c16b070ff6))

* fix: handling config value in _get_values_from_helper ([`9dfb4cd`](https://github.com/python-gitlab/python-gitlab/commit/9dfb4cd97e6eb5bbfc29935cbb190b70b739cf9f))

* fix: update doc for token helper ([`3ac6fa1`](https://github.com/python-gitlab/python-gitlab/commit/3ac6fa12b37dd33610ef2206ef4ddc3b20d9fd3f))

* fix: let the homedir be expanded in path of helper ([`fc7387a`](https://github.com/python-gitlab/python-gitlab/commit/fc7387a0a6039bc58b2a741ac9b73d7068375be7))

* fix: make secret helper more user friendly ([`fc2798f`](https://github.com/python-gitlab/python-gitlab/commit/fc2798fc31a08997c049f609c19dd4ab8d75964e))

* fix: linting issues and test ([`b04dd2c`](https://github.com/python-gitlab/python-gitlab/commit/b04dd2c08b69619bb58832f40a4c4391e350a735))

* fix: better real life token lookup example ([`9ef8311`](https://github.com/python-gitlab/python-gitlab/commit/9ef83118efde3d0f35d73812ce8398be2c18ebff))

* fix(objects): add single get endpoint for instance audit events ([`c3f0a6f`](https://github.com/python-gitlab/python-gitlab/commit/c3f0a6f158fbc7d90544274b9bf09d5ac9ac0060))

* fix: checking if RESTManager._from_parent_attrs is set

Prior to commit 3727cbd21fc40b312573ca8da56e0f6cf9577d08
RESTManager._from_parent_attrs did not exist unless it was explicitly
set. But commit 3727cbd21fc40b312573ca8da56e0f6cf9577d08 set it to a
default value of {}.

So the checks using hasattr() were no longer valid.

Update the checks to check if RESTManager._from_parent_attrs has a
value. ([`8224b40`](https://github.com/python-gitlab/python-gitlab/commit/8224b4066e84720d7efed3b7891c47af73cc57ca))

* fix: handle tags like debian/2%2.6-21 as identifiers

Git refnames are relatively free-form and can contain all sort for
special characters, not just `/` and `#`, see
http://git-scm.com/docs/git-check-ref-format

In particular, Debian&#39;s DEP-14 standard for storing packaging in git
repositories mandates the use of the `%` character in tags in some
cases like `debian/2%2.6-21`.

Unfortunately python-gitlab currently only escapes `/` to `%2F` and in
some cases `#` to `%23`. This means that when using the commit API to
retrieve information about the `debian/2%2.6-21` tag only the slash is
escaped before being inserted in the URL path and the `%` is left
untouched, resulting in something like
`/api/v4/projects/123/repository/commits/debian%2F2%2.6-21`. When
urllib3 seees that it detects the invalid `%` escape and then urlencodes
the whole string, resulting in
`/api/v4/projects/123/repository/commits/debian%252F2%252.6-21`, where
the original `/` got escaped twice and produced `%252F`.

To avoid the issue, fully urlencode identifiers and parameters to avoid
the urllib3 auto-escaping in all cases.

Signed-off-by: Emanuele Aina &lt;emanuele.aina@collabora.com&gt; ([`b4dac5c`](https://github.com/python-gitlab/python-gitlab/commit/b4dac5ce33843cf52badeb9faf0f7f52f20a9a6a))

* fix: remove duplicate class definitions in v4/objects/users.py

The classes UserStatus and UserStatusManager were each declared twice.
Remove the duplicate declarations. ([`7c4e625`](https://github.com/python-gitlab/python-gitlab/commit/7c4e62597365e8227b8b63ab8ba0c94cafc7abc8))

* fix: wrong variable name

Discovered this when I ran flake8 on the file. Unfortunately I was the
one who introduced this wrong variable name :( ([`15ec41c`](https://github.com/python-gitlab/python-gitlab/commit/15ec41caf74e264d757d2c64b92427f027194b82))

* fix: tox pep8 target, so that it can run

Previously running the pep8 target would fail as flake8 was not
installed.

Now install flake8 for the pep8 target.

NOTE: Running the pep8 target fails as there are many warnings/errors.
But it does allow us to run it and possibly work on reducing these
warnings/errors in the future.

In addition, add two checks to the ignore list as black takes care of
formatting. The two checks added to the ignore list are:
  * E501: line too long
  * W503: line break before binary operator ([`f518e87`](https://github.com/python-gitlab/python-gitlab/commit/f518e87b5492f2f3c201d4d723c07c746a385b6e))

* fix: undefined name errors

Discovered that there were some undefined names. ([`48ec9e0`](https://github.com/python-gitlab/python-gitlab/commit/48ec9e0f6a2d2da0a24ef8292c70dc441836a913))

* fix: extend wait timeout for test_delete_user()

Have been seeing intermittent failures of the test_delete_user()
functional test. Have made the following changes to hopefully resolve
the issue and if it still fails to know better why the failure
occurred.

*  Extend the wait timeout for test_delete_user() from 30 to 60
   tries of 0.5 seconds each.

*  Modify wait_for_sidekiq() to return True if sidekiq process
   terminated. Return False if the timeout expired.

*  Modify wait_for_sidekiq() to loop through all processes instead of
   assuming there is only one process. If all processes are not busy
   then return.

*  Modify wait_for_sidekiq() to sleep at least once before checking
   for processes being busy.

*  Check for True being returned in test_delete_user() call to
   wait_for_sidekiq() ([`19fde8e`](https://github.com/python-gitlab/python-gitlab/commit/19fde8ed0e794d33471056e2c07539cde70a8699))

* fix: test_update_group() dependency on ordering

Since there are two groups we can&#39;t depend on the one we changed to
always be the first one returned.

Instead fetch the group we want and then test our assertion against
that group. ([`e78a8d6`](https://github.com/python-gitlab/python-gitlab/commit/e78a8d6353427bad0055f116e94f471997ee4979))

* fix: honor parameter value passed

Gitlab allows setting the defaults for MR to delete the source. Also
the inline help of the CLI suggest that a boolean is expected, but no
matter what value you set, it will always delete. ([`c2f8f0e`](https://github.com/python-gitlab/python-gitlab/commit/c2f8f0e7db9529e1f1f32d790a67d1e20d2fe052))

### Refactor

* refactor(objects): move instance audit events where they belong ([`48ba88f`](https://github.com/python-gitlab/python-gitlab/commit/48ba88ffb983207da398ea2170c867f87a8898e9))

* refactor: move Gitlab and GitlabList to gitlab/client.py

Move the classes Gitlab and GitlabList from gitlab/__init__.py to the
newly created gitlab/client.py file.

Update one test case that was depending on requests being defined in
gitlab/__init__.py ([`53a7645`](https://github.com/python-gitlab/python-gitlab/commit/53a764530cc3c6411034a3798f794545881d341e))

* refactor(api): explicitly export classes for star imports ([`f05c287`](https://github.com/python-gitlab/python-gitlab/commit/f05c287512a9253c7f7d308d3437240ac8257452))

* refactor(v4): split objects and managers per API resource ([`a5a48ad`](https://github.com/python-gitlab/python-gitlab/commit/a5a48ad08577be70c6ca511d3b4803624e5c2043))

### Test

* test(object): add test for __dir__ duplicates ([`a8e591f`](https://github.com/python-gitlab/python-gitlab/commit/a8e591f742f777f8747213b783271004e5acc74d))

* test(objects): add tests for resource state events ([`10225cf`](https://github.com/python-gitlab/python-gitlab/commit/10225cf26095efe82713136ddde3330e7afc6d10))

* test(objects): add unit test for instance audit events ([`84e3247`](https://github.com/python-gitlab/python-gitlab/commit/84e3247d0cd3ddb1f3aa0ac91fb977c3e1e197b5))

* test: don&#39;t add duplicate fixture

Co-authored-by: Nejc Habjan &lt;hab.nejc@gmail.com&gt; ([`5d94846`](https://github.com/python-gitlab/python-gitlab/commit/5d9484617e56b89ac5e17f8fc94c0b1eb46d4b89))

* test(api): add functional test for release links API ([`ab2a1c8`](https://github.com/python-gitlab/python-gitlab/commit/ab2a1c816d83e9e308c0c9c7abf1503438b0b3be))

* test(api,cli): add tests for custom user agent ([`c5a37e7`](https://github.com/python-gitlab/python-gitlab/commit/c5a37e7e37a62372c250dfc8c0799e847eecbc30))

### Unknown

* Merge pull request #1408 from python-gitlab/chore/bump-to-2-7-0

chore: bump version to 2.7.0 ([`e37de18`](https://github.com/python-gitlab/python-gitlab/commit/e37de189d5799e9bdbbd7556289d4b617aff9c4d))

* Merge pull request #1411 from JohnVillalovos/jlvillal/list_filters

chore: make ListMixin._list_filters always present ([`62c75b5`](https://github.com/python-gitlab/python-gitlab/commit/62c75b5e637858f0e9ef7bed21a347bbd5e0b972))

* Merge pull request #1410 from JohnVillalovos/jlvillal/short_print_attr

chore: make RESTObject._short_print_attrs always present ([`09522b3`](https://github.com/python-gitlab/python-gitlab/commit/09522b356386f4e2ceef7e8c2604269e0682ed20))

* Merge pull request #1414 from python-gitlab/chore/remove-noisy-deprecation-warning

chore(objects): remove noisy deprecation warning for audit events ([`0a0fcaf`](https://github.com/python-gitlab/python-gitlab/commit/0a0fcaf27fe18867d2b4860badb52cafdac555cb))

* Merge pull request #1392 from bbatliner/patch-1

Improvements to HTTP requests ([`cfc42d2`](https://github.com/python-gitlab/python-gitlab/commit/cfc42d246a4fc9a9afa9a676efcac0774e909aab))

* Merge pull request #1406 from python-gitlab/renovate/docker-gitlab-gitlab-ce-13.x

chore(deps): update gitlab/gitlab-ce docker tag to v13.11.1-ce.0 ([`4f79dff`](https://github.com/python-gitlab/python-gitlab/commit/4f79dffbd5e1e296dee2e1276e3d2c441742d28a))

* Merge pull request #1405 from JohnVillalovos/jlvillal/returns_bytes

fix: correct ProjectFile.decode() documentation ([`c055de0`](https://github.com/python-gitlab/python-gitlab/commit/c055de05357e07fad57ebcefb5377997eae83e68))

* Merge pull request #1397 from JohnVillalovos/jlvillal/flake8

Fix all issues reported by running: tox -e pep8 and enable pep8 as a linter check ([`976e14d`](https://github.com/python-gitlab/python-gitlab/commit/976e14d95fc5716ad161cbf39d50e5863cd9b335))

* Merge pull request #1404 from DylannCordel/fix-upd-user-bool-data-and-avatar

fix: update user&#39;s bool data and avatar ([`5fac07a`](https://github.com/python-gitlab/python-gitlab/commit/5fac07ab883120375532bfaf1dcae0f1d8940fb6))

* Merge pull request #1383 from spyoungtech/dirfix

fix(types): prevent __dir__ in RestObject from producing duplicates ([`60c5fd8`](https://github.com/python-gitlab/python-gitlab/commit/60c5fd8878ff54f6e3fcd168545ab3af139f1dcc))

* Merge pull request #1400 from JohnVillalovos/jlvillal/sanitize

chore: remove unused function sanitize_parameters() ([`dd236a0`](https://github.com/python-gitlab/python-gitlab/commit/dd236a09c6a3e01a11410791210a95dd6cee9b5a))

* Merge pull request #1398 from JohnVillalovos/jlvillal/mypy_mixins

fix: correct some type-hints in gitlab/mixins.py ([`5b18d20`](https://github.com/python-gitlab/python-gitlab/commit/5b18d20f2f2bb71606892616f6c98ddc9d2ab836))

* Merge pull request #1399 from JohnVillalovos/jlvillal/fix_custom_action

fix: argument type was not a tuple as expected ([`fc4f7fd`](https://github.com/python-gitlab/python-gitlab/commit/fc4f7fd620ffc83acbc8ce531d0acb7ce4273763))

* Merge pull request #1364 from python-gitlab/feat/resource-state-events

feat: add support for resource state events API ([`916a7fe`](https://github.com/python-gitlab/python-gitlab/commit/916a7fe4661b3822a0a93fc75fb72d80f550582d))

* Merge pull request #1359 from klorenz/feat_token_lookup

feat(config): allow using a credential helper to lookup tokens ([`af781c1`](https://github.com/python-gitlab/python-gitlab/commit/af781c10db3829163f977e494e4008acf2096d64))

* Merge pull request #1375 from JohnVillalovos/jlvillal/update_uses_post

chore: remove usage of getattr() ([`d236267`](https://github.com/python-gitlab/python-gitlab/commit/d2362676d97633893aea27f878773e5fa009976f))

* Merge pull request #1366 from JohnVillalovos/jlvillal/create_attrs

chore: have _create_attrs &amp; _update_attrs be a namedtuple ([`d1697d4`](https://github.com/python-gitlab/python-gitlab/commit/d1697d4458d40a726fdf2629735deda211be8f38))

* Merge pull request #1391 from python-gitlab/renovate/docker-compose-1.x

chore(deps): update dependency docker-compose to v1.29.1 ([`a6d3556`](https://github.com/python-gitlab/python-gitlab/commit/a6d35568fbeb44855469279ea14b6b7d53aac37f))

* Merge pull request #1380 from python-gitlab/renovate/sphinx-3.x

chore(deps): update dependency sphinx to v3.5.4 ([`6b86878`](https://github.com/python-gitlab/python-gitlab/commit/6b86878d73dd573d6a86c5318a9f3a7927c98c73))

* Merge pull request #1363 from python-gitlab/feat/all-audit-events

Feat: cover all audit events ([`02ce49e`](https://github.com/python-gitlab/python-gitlab/commit/02ce49ede50e698840a0324b4b90ca1d3084d961))

* Merge pull request #1382 from python-gitlab/renovate/docker-compose-1.x

chore(deps): update dependency docker-compose to v1.28.6 ([`e798c9b`](https://github.com/python-gitlab/python-gitlab/commit/e798c9b685f1a3da8875f2cef9e6749f86d9ecbd))

* Merge pull request #1373 from JacobHenner/jacobhenner/add-package_files

feat: add support for Project Package Files ([`8ace76a`](https://github.com/python-gitlab/python-gitlab/commit/8ace76a8a5596171c782570fdde7a82119aeb9ff))

* Merge pull request #1371 from JohnVillalovos/jlvillal/create_attrs_1

chore: add _create_attrs &amp; _update_attrs to RESTManager ([`8603248`](https://github.com/python-gitlab/python-gitlab/commit/8603248f73d8c751023fbfd2a394c5b7d939af7f))

* Merge pull request #1369 from python-gitlab/renovate/docker-gitlab-gitlab-ce-13.x

chore(deps): update gitlab/gitlab-ce docker tag to v13.9.3-ce.0 ([`6fde243`](https://github.com/python-gitlab/python-gitlab/commit/6fde2437e82aeb8af903f81e351790b4695074a1))

* Merge pull request #1367 from JohnVillalovos/jlvillal/from_parent_attrs

fix: checking if RESTManager._from_parent_attrs is set ([`f93b9b5`](https://github.com/python-gitlab/python-gitlab/commit/f93b9b5af928e127635cc0f2976da5be22d6c735))

* Merge pull request #1365 from JohnVillalovos/jlvillal/getattr

chore: make _types always present in RESTManager ([`de73ea7`](https://github.com/python-gitlab/python-gitlab/commit/de73ea7933d3f3c94aa27a7d9b9ea7bfd64ad1f1))

* Merge pull request #1336 from em-/fix/quote-everything

fix: handle tags like debian/2%2.6-21 as identifiers ([`48fc907`](https://github.com/python-gitlab/python-gitlab/commit/48fc907403b630f069dfd63fada73f96a8c6e983))

* Merge pull request #1344 from JohnVillalovos/jlvillal/mixins

chore: add type-hints for gitlab/mixins.py ([`63ecd2e`](https://github.com/python-gitlab/python-gitlab/commit/63ecd2eba82408b034a90026050748c855a3ac96))

* Merge pull request #1353 from JohnVillalovos/jlvillal/mypy_base

chore: add type hints to gitlab/base.py:RESTManager ([`ebdfec7`](https://github.com/python-gitlab/python-gitlab/commit/ebdfec7ee66c1cc64024fe52b2b0821d51779c2a))

* Merge pull request #1350 from JohnVillalovos/jlvillal/isinstance

chore: Put assert statements inside &#39;if TYPE_CHECKING:&#39; ([`c530f75`](https://github.com/python-gitlab/python-gitlab/commit/c530f75a3f356e2fc9732c6a3688881e453115e7))

* Merge pull request #1361 from python-gitlab/renovate/sphinx-3.x

chore(deps): update dependency sphinx to v3.5.2 ([`c7a0669`](https://github.com/python-gitlab/python-gitlab/commit/c7a06691a9fa15d0238e2b041ceee6121c5cf19e))

* Merge pull request #1358 from python-gitlab/renovate/docker-gitlab-gitlab-ce-13.x

chore(deps): update gitlab/gitlab-ce docker tag to v13.9.2-ce.0 ([`aa13214`](https://github.com/python-gitlab/python-gitlab/commit/aa132149558e797332897ec8543a9ac9fb0da09b))

* Merge pull request #1351 from JohnVillalovos/jlvillal/import_start

chore: del &#39;import *&#39; in gitlab/v4/objects/project_access_tokens.py ([`96d2805`](https://github.com/python-gitlab/python-gitlab/commit/96d2805b5bf372cb79c2b7db5c1e499c41e477c1))

* Merge pull request #1342 from JohnVillalovos/jlvillal/mypy_incomplete

chore: disallow incomplete type defs ([`5f23ed9`](https://github.com/python-gitlab/python-gitlab/commit/5f23ed916aedbd266b9aaa5857461d80c9175031))

* Merge pull request #1347 from python-gitlab/chore/split-repository-methods

chore(api): move repository endpoints into separate module ([`d8b8a0a`](https://github.com/python-gitlab/python-gitlab/commit/d8b8a0a010b41465586dccf198582ae127a31530))

* Merge pull request #1343 from JohnVillalovos/jlvillal/mypy_testing_things

chore: add and fix some type-hints in gitlab/client.py ([`f5a65f0`](https://github.com/python-gitlab/python-gitlab/commit/f5a65f0580dedf127243fc3dd42f39c4d704eae1))

* Merge pull request #1345 from JohnVillalovos/jlvillal/mypy_base_fixes

chore: add additional type-hints for gitlab/base.py ([`7441455`](https://github.com/python-gitlab/python-gitlab/commit/74414552bd054b32016a7a9e010b13cd8a4f33d9))

* Merge pull request #1333 from python-gitlab/feat/user-follow-api

feat(users): add follow/unfollow API ([`5bc158d`](https://github.com/python-gitlab/python-gitlab/commit/5bc158d3d4a8ac0d0116fea7cfd33ad897918741))

* Merge pull request #1339 from JohnVillalovos/jlvillal/mypy_client_py

chore: add type-hints to gitlab/client.py ([`b0d75d9`](https://github.com/python-gitlab/python-gitlab/commit/b0d75d9e6fd4876446498f0aac97ae3f6ec601d5))

* Merge pull request #1341 from JohnVillalovos/jlvillal/gitter

doc: add information about the gitter community ([`adab83a`](https://github.com/python-gitlab/python-gitlab/commit/adab83a1330dc34e8e52d74dfef36ac97060d42c))

* Merge pull request #1340 from JohnVillalovos/jlvillal/gitlab_init

chore: remove import of gitlab.utils from __init__.py ([`d0eb1b5`](https://github.com/python-gitlab/python-gitlab/commit/d0eb1b53619e1d1dd0353715cdf500f82ead7ecf))

* Merge pull request #1338 from JohnVillalovos/jlvillal/mypy_base

Improve type-hints for gitlab/base.py ([`cbd4f1e`](https://github.com/python-gitlab/python-gitlab/commit/cbd4f1e73afc8eea0b75c0b5a8734886cb081c1b))

* Merge pull request #1334 from JohnVillalovos/jlvillal/mypy_cli

chore: add type-hints to gitlab/cli.py ([`f909cae`](https://github.com/python-gitlab/python-gitlab/commit/f909caea0d1edc779cf6139af769346013bbe358))

* Merge pull request #1337 from python-gitlab/renovate/docker-compose-1.x

chore(deps): update dependency docker-compose to v1.28.5 ([`bd62fed`](https://github.com/python-gitlab/python-gitlab/commit/bd62fed00a201dbd7a68083847634c03861826a2))

* Merge pull request #1335 from JohnVillalovos/jlvillal/remove_dup_classes

fix: remove duplicate class definitions in v4/objects/users.py ([`ecb686d`](https://github.com/python-gitlab/python-gitlab/commit/ecb686d8f263fadfd113d43178d2200be17d766e))

* Merge pull request #1328 from python-gitlab/renovate/wagoid-commitlint-github-action-3.x

chore(deps): update wagoid/commitlint-github-action action to v3 ([`6662252`](https://github.com/python-gitlab/python-gitlab/commit/666225221deec06014d5ccff46d1c21d5828c977))

* Merge pull request #1329 from JohnVillalovos/jlvillal/mypy_const

Add type-hints to gitlab/const.py ([`ca4c1d9`](https://github.com/python-gitlab/python-gitlab/commit/ca4c1d9ee96e2eaa8d69d61892351e239930640c))

* Merge pull request #1330 from JohnVillalovos/jlvillal/mypy_utils

chore: add type hints to gitlab/utils.py ([`a1a8bfe`](https://github.com/python-gitlab/python-gitlab/commit/a1a8bfe0e27c3fcaf145398742c3f5c145008cce))

* Merge pull request #1331 from JohnVillalovos/jlvillal/mypy_config

chore: add type-hints to gitlab/config.py ([`d207074`](https://github.com/python-gitlab/python-gitlab/commit/d207074deff7fd053977c0778f94e34416d5aa50))

* Merge pull request #1332 from JohnVillalovos/jlvillal/fix_variable

chore: fix wrong variable name in cli.py ([`665c0c3`](https://github.com/python-gitlab/python-gitlab/commit/665c0c3f1bd2c3bc0c65d4a2f51d25900cf6fed2))

* Merge pull request #1319 from JohnVillalovos/jlvillal/import_star

chore: remove usage of &#39;from ... import *&#39; ([`0b67ca2`](https://github.com/python-gitlab/python-gitlab/commit/0b67ca29d2cc6177e330b91519fdf54b05621769))

* Merge pull request #1327 from python-gitlab/feat/project-access-token-api

feat(projects): add project access token api ([`e06c51b`](https://github.com/python-gitlab/python-gitlab/commit/e06c51bcf29492dbc7ef838c35f6ef86a79af261))

* Merge pull request #1325 from JohnVillalovos/jlvillal/pep8

fix: tox pep8 target, so that it can run ([`bb227d3`](https://github.com/python-gitlab/python-gitlab/commit/bb227d3ba58745d62f03a919c671b6bba15464c1))

* Merge pull request #1322 from JohnVillalovos/jlvillal/missing_vars

fix: undefined name errors in v4 objects ([`a7ec67f`](https://github.com/python-gitlab/python-gitlab/commit/a7ec67f69a3177a9d6610ca7af80bcf09035cbbd))

* Merge pull request #1321 from JohnVillalovos/jlvillal/remove_cruft

chore: remove unused function _construct_url() ([`d90be1e`](https://github.com/python-gitlab/python-gitlab/commit/d90be1e6ed5b27e02e00cffec25317bef413fec4))

* Merge pull request #1299 from JohnVillalovos/mypy

Enable mypy type checking and add type hints to gitlab/base.py ([`a18bc5c`](https://github.com/python-gitlab/python-gitlab/commit/a18bc5c525b686af5f28216d2f1da95942b63f61))

* Merge pull request #1318 from JohnVillalovos/jlvillal/testing

chore: remove usage of &#39;from ... import *&#39; in client.py ([`d9fdf1d`](https://github.com/python-gitlab/python-gitlab/commit/d9fdf1db9b928ac154ad385cf6e7f8220ea42aa1))

* Merge pull request #1310 from JohnVillalovos/jlvillal/v4_only

chore: explicitly import gitlab.v4.objects/cli ([`8c58b07`](https://github.com/python-gitlab/python-gitlab/commit/8c58b071329ec5d37c45647963160ee54cc4048e))

* Merge pull request #1316 from JohnVillalovos/jlvillal/test_wait

test: extend wait timeout for test_delete_user() ([`5cc60d5`](https://github.com/python-gitlab/python-gitlab/commit/5cc60d5a8ac129652611d3dc12b350b5ca7262b9))

* Merge pull request #1314 from python-gitlab/feat/release-links

feat: add release links API support ([`2b29776`](https://github.com/python-gitlab/python-gitlab/commit/2b29776a033b9903d055df7c0716805e86d13fa2))

* Merge pull request #1311 from JohnVillalovos/jlvillal/fix_functional

fix: test_update_group() dependency on ordering ([`3381700`](https://github.com/python-gitlab/python-gitlab/commit/338170029c9c8855a6c44de8f3576e8389338652))

* Merge pull request #1307 from python-gitlab/renovate/docker-compose-1.x

chore(deps): update dependency docker-compose to v1.28.4 ([`649385c`](https://github.com/python-gitlab/python-gitlab/commit/649385cc03065d023d74399237331d1ea64f766f))

* Merge pull request #1308 from Sineaggi/add-project-audit-endpoint

feat: add project audit endpoint ([`0c5a23e`](https://github.com/python-gitlab/python-gitlab/commit/0c5a23ee03c69150d2d7f9092ca8fbb718117e08))

* Merge pull request #1301 from JohnVillalovos/refactor_jlvillal

refactor: move Gitlab and GitlabList to gitlab/client.py ([`2c4fcf8`](https://github.com/python-gitlab/python-gitlab/commit/2c4fcf83296cc65c08b76b2d9312004ecf670fb6))

* Merge pull request #1305 from python-gitlab/renovate/docker-compose-1.x

chore(deps): update dependency docker-compose to v1.28.3 ([`d4e7a03`](https://github.com/python-gitlab/python-gitlab/commit/d4e7a031eb64ecba09f2547bd7803f2cceb7558b))

* Merge pull request #1304 from python-gitlab/feat/personal-access-token-api

feat: add personal access token API ([`ef8fcf7`](https://github.com/python-gitlab/python-gitlab/commit/ef8fcf79a475e606918a65ed1eecf63175df0593))

* Merge pull request #1300 from JohnVillalovos/remove_cruft

chore: remove unused ALLOWED_KEYSET_ENDPOINTS variable ([`bec2094`](https://github.com/python-gitlab/python-gitlab/commit/bec2094180268effabd24e71ca74708c0e7832a9))

* Merge pull request #1303 from python-gitlab/renovate/sphinx-3.x

chore(deps): update dependency sphinx to v3.5.1 ([`9f6691d`](https://github.com/python-gitlab/python-gitlab/commit/9f6691d9deeb2d7a73e2dd187b6cc7ee69a5c578))

* Merge pull request #1271 from allcloud-jonathan/feature/honor-bool-for-delete-source

fix: honor parameter value passed ([`1552eb5`](https://github.com/python-gitlab/python-gitlab/commit/1552eb5bb0eec9a68c4ececfbf80387ca64fcebe))

* Merge pull request #1298 from JohnVillalovos/master

Remove Python 2 code ([`07edafe`](https://github.com/python-gitlab/python-gitlab/commit/07edafe8b7ffa25e530cd24db35ab64a9b5a285f))

* Merge pull request #1288 from python-gitlab/refactor/split-objects

refactor(v4): split objects and managers per API resource ([`9fcd962`](https://github.com/python-gitlab/python-gitlab/commit/9fcd9623fd8c89347202cd5a2e90e68ee2780f41))

* Merge pull request #1295 from python-gitlab/renovate/sphinx-3.x

chore(deps): update dependency sphinx to v3.5.0 ([`76e6f87`](https://github.com/python-gitlab/python-gitlab/commit/76e6f8782ff3c24863e20a8e938bd38cce3cf4f6))

* Merge pull request #1292 from python-gitlab/renovate/docker-gitlab-gitlab-ce-13.x

chore(deps): update gitlab/gitlab-ce docker tag to v13.8.4-ce.0 ([`45fc49e`](https://github.com/python-gitlab/python-gitlab/commit/45fc49ee07b367bd0abaaa16023b99dab5c46491))

* Merge pull request #1223 from python-gitlab/feat/single-issue-api

feat(issues): add missing get verb to IssueManager ([`9d6c188`](https://github.com/python-gitlab/python-gitlab/commit/9d6c1882d567116e16484f3e0a1036da4967c537))

* Merge pull request #1287 from python-gitlab/chore/deduplicate-pr-jobs

chore(ci): deduplicate PR jobs ([`9fe506f`](https://github.com/python-gitlab/python-gitlab/commit/9fe506fd13a91d806dff9542dbb3a99edb8e9c12))

* Merge pull request #1283 from fajpunk/import_bitbucket

feat: import from bitbucket server ([`b48563f`](https://github.com/python-gitlab/python-gitlab/commit/b48563f1ad96e3c70b36f6e55b2fe7ed8d324919))

* Merge pull request #1244 from python-gitlab/renovate/alessandrojcm-commitlint-pre-commit-hook-4.x

chore(deps): update precommit hook alessandrojcm/commitlint-pre-commit-hook to v4 ([`3935baf`](https://github.com/python-gitlab/python-gitlab/commit/3935baf1fc5120728949e65397ffb5776bdf1bc7))

* Merge pull request #1281 from python-gitlab/renovate/docker-gitlab-gitlab-ce-13.x

chore(deps): update gitlab/gitlab-ce docker tag to v13.8.2-ce.0 ([`1d9155c`](https://github.com/python-gitlab/python-gitlab/commit/1d9155ca6814847e93c1ec93c734ca004d353636))

* Merge pull request #1225 from python-gitlab/renovate/sphinx-3.x

chore(deps): update dependency sphinx to v3.4.3 ([`a985c34`](https://github.com/python-gitlab/python-gitlab/commit/a985c34c2e501fcfc9aadd500a191a8a20f0933c))

* Merge pull request #1277 from python-gitlab/feat/override-user-agent

feat(api,cli): make user agent configurable ([`643454c`](https://github.com/python-gitlab/python-gitlab/commit/643454c5c5bbfb66d5890232a4f07fb04a753486))

* Merge pull request #1276 from python-gitlab/bufferoverflow-patch-1

docs: switch from travis-ci.org to GitHub Actions ([`071d699`](https://github.com/python-gitlab/python-gitlab/commit/071d699f7e4bf7eb3aa49b78f9cc9e56a473e281))

## v2.6.0 (2021-01-29)

### Chore

* chore: offically support and test 3.9 ([`62dd07d`](https://github.com/python-gitlab/python-gitlab/commit/62dd07df98341f35c8629e8f0a987b35b70f7fe6))

* chore(deps): pin dependency requests-toolbelt to ==0.9.1 ([`4d25f20`](https://github.com/python-gitlab/python-gitlab/commit/4d25f20e8f946ab58d1f0c2ef3a005cb58dc8b6c))

* chore(deps): update dependency requests to v2.25.1 ([`9c2789e`](https://github.com/python-gitlab/python-gitlab/commit/9c2789e4a55822d7c50284adc89b9b6bfd936a72))

* chore(deps): update gitlab/gitlab-ce docker tag to v13.8.1-ce.0 ([`9854d6d`](https://github.com/python-gitlab/python-gitlab/commit/9854d6da84c192f765e0bc80d13bc4dae16caad6))

* chore(ci): add coverage and docs jobs ([`2de64cf`](https://github.com/python-gitlab/python-gitlab/commit/2de64cfa469c9d644a2950d3a4884f622ed9faf4))

* chore(ci): force colors in pytest runs ([`1502079`](https://github.com/python-gitlab/python-gitlab/commit/150207908a72869869d161ecb618db141e3a9348))

* chore(ci): pin docker-compose install for tests

This ensures python-dotenv with expected behavior for .env processing ([`1f7a2ab`](https://github.com/python-gitlab/python-gitlab/commit/1f7a2ab5bd620b06eb29146e502e46bd47432821))

* chore(ci): pin os version ([`cfa27ac`](https://github.com/python-gitlab/python-gitlab/commit/cfa27ac6453f20e1d1f33973aa8cbfccff1d6635))

* chore(ci): fix typo in matrix ([`5e1547a`](https://github.com/python-gitlab/python-gitlab/commit/5e1547a06709659c75d40a05ac924c51caffcccf))

* chore(ci): fix copy/paste oopsie ([`c6241e7`](https://github.com/python-gitlab/python-gitlab/commit/c6241e791357d3f90e478c456cc6d572b388e6d1))

* chore(ci): add pytest PR annotations ([`8f92230`](https://github.com/python-gitlab/python-gitlab/commit/8f9223041481976522af4c4f824ad45e66745f29))

* chore(ci): replace travis with Actions ([`8bb73a3`](https://github.com/python-gitlab/python-gitlab/commit/8bb73a3440b79df93c43214c31332ad47ab286d8))

* chore: move .env into docker-compose dir ([`55cbd1c`](https://github.com/python-gitlab/python-gitlab/commit/55cbd1cbc28b93673f73818639614c61c18f07d1))

* chore(deps): update gitlab/gitlab-ce docker tag to v13.5.4-ce.0 ([`265dbbd`](https://github.com/python-gitlab/python-gitlab/commit/265dbbdd37af88395574564aeb3fd0350288a18c))

* chore(deps): update gitlab/gitlab-ce docker tag to v13.5.3-ce.0 ([`d1b0b08`](https://github.com/python-gitlab/python-gitlab/commit/d1b0b08e4efdd7be2435833a28d12866fe098d44))

* chore(deps): update gitlab/gitlab-ce docker tag to v13.5.2-ce.0 ([`4a6831c`](https://github.com/python-gitlab/python-gitlab/commit/4a6831c6aa6eca8e976be70df58187515e43f6ce))

* chore(deps): update gitlab/gitlab-ce docker tag to v13.5.1-ce.0 ([`348e860`](https://github.com/python-gitlab/python-gitlab/commit/348e860a9128a654eff7624039da2c792a1c9124))

* chore(deps): update gitlab/gitlab-ce docker tag to v13.5.0-ce.0 ([`fc205cc`](https://github.com/python-gitlab/python-gitlab/commit/fc205cc593a13ec2ce5615293a9c04c262bd2085))

* chore(docs): always edit the file directly on master

There is no way to edit the raw commit ([`35e43c5`](https://github.com/python-gitlab/python-gitlab/commit/35e43c54cd282f06dde0d24326641646fc3fa29e))

* chore(cli): remove python2 code ([`1030e0a`](https://github.com/python-gitlab/python-gitlab/commit/1030e0a7e13c4ec3fdc48b9010e9892833850db9))

* chore(deps): update gitlab/gitlab-ce docker tag to v13.4.3-ce.0 ([`bc17889`](https://github.com/python-gitlab/python-gitlab/commit/bc178898776d2d61477ff773248217adfac81f56))

* chore: simplified search scope constants ([`16fc048`](https://github.com/python-gitlab/python-gitlab/commit/16fc0489b2fe24e0356e9092c9878210b7330a72))

* chore: added docs for search scopes constants ([`7565bf0`](https://github.com/python-gitlab/python-gitlab/commit/7565bf059b240c9fffaf6959ee168a12d0fedd77))

* chore: added constants for search API ([`8ef53d6`](https://github.com/python-gitlab/python-gitlab/commit/8ef53d6f6180440582d1cca305fd084c9eb70443))

* chore: apply suggestions ([`65ce026`](https://github.com/python-gitlab/python-gitlab/commit/65ce02675d9c9580860df91b41c3cf5e6bb8d318))

* chore(deps): update python docker tag to v3.9 ([`1fc65e0`](https://github.com/python-gitlab/python-gitlab/commit/1fc65e072003a2d1ebc29d741e9cef1860b5ff78))

* chore: use helper fixtures for test directories ([`40ec2f5`](https://github.com/python-gitlab/python-gitlab/commit/40ec2f528b885290fbb3e2d7ef0f5f8615219326))

* chore: allow overriding docker-compose env vars for tag ([`27109ca`](https://github.com/python-gitlab/python-gitlab/commit/27109cad0d97114b187ce98ce77e4d7b0c7c3270))

* chore: remove unnecessary random function ([`d4ee0a6`](https://github.com/python-gitlab/python-gitlab/commit/d4ee0a6085d391ed54d715a5ed4b0082783ca8f3))

* chore(deps): pin dependencies ([`14d8f77`](https://github.com/python-gitlab/python-gitlab/commit/14d8f77601a1ee4b36888d68f0102dd1838551f2))

* chore(deps): update gitlab/gitlab-ce docker tag to v13.3.6-ce.0 ([`57b5782`](https://github.com/python-gitlab/python-gitlab/commit/57b5782219a86153cc3425632e232db3f3c237d7))

* chore(test): remove hacking dependencies ([`9384493`](https://github.com/python-gitlab/python-gitlab/commit/9384493942a4a421aced4bccc7c7291ff30af886))

* chore(ci): add .readthedocs.yml ([`0ad441e`](https://github.com/python-gitlab/python-gitlab/commit/0ad441eee5f2ac1b7c05455165e0085045c24b1d))

* chore(ci): reduce renovate PR noise ([`f4d7a55`](https://github.com/python-gitlab/python-gitlab/commit/f4d7a5503f3a77f6aa4d4e772c8feb3145044fec))

* chore(deps): update gitlab/gitlab-ce docker tag to v13.3.5-ce.0 ([`c88d870`](https://github.com/python-gitlab/python-gitlab/commit/c88d87092f39d11ecb4f52ab7cf49634a0f27e80))

* chore(deps): update gitlab/gitlab-ce docker tag to v13.3.4-ce.0 ([`e94c4c6`](https://github.com/python-gitlab/python-gitlab/commit/e94c4c67f21ecaa2862f861953c2d006923d3280))

* chore(deps): update gitlab/gitlab-ce docker tag to v13.3.3-ce.0 ([`667bf01`](https://github.com/python-gitlab/python-gitlab/commit/667bf01b6d3da218df6c4fbdd9c7b9282a2aaff9))

### Documentation

* docs(cli-usage): fixed term ([`d282a99`](https://github.com/python-gitlab/python-gitlab/commit/d282a99e29abf390c926dcc50984ac5523d39127))

* docs(readme): update supported Python versions ([`20b1e79`](https://github.com/python-gitlab/python-gitlab/commit/20b1e791c7a78633682b2d9f7ace8eb0636f2424))

* docs(cli): use inline anonymous references for external links

There doesn&#39;t seem to be an obvious way to use an alias for identical
text labels that link to different targets. With inline links we can
work around this shortcoming. Until we know better. ([`f2cf467`](https://github.com/python-gitlab/python-gitlab/commit/f2cf467443d1c8a1a24a8ebf0ec1ae0638871336))

* docs(groups): add example for creating subgroups ([`92eb4e3`](https://github.com/python-gitlab/python-gitlab/commit/92eb4e3ca0ccd83dba2067ccc4ce206fd17be020))

* docs: clean up grammar and formatting in documentation ([`aff9bc7`](https://github.com/python-gitlab/python-gitlab/commit/aff9bc737d90e1a6e91ab8efa40a6756c7ce5cba))

* docs: add Project Merge Request approval rule documentation ([`449fc26`](https://github.com/python-gitlab/python-gitlab/commit/449fc26ffa98ef5703d019154f37a4959816f607))

* docs(issues): add admin, project owner hint

Closes #1101 ([`609c03b`](https://github.com/python-gitlab/python-gitlab/commit/609c03b7139db8af5524ebeb741fd5b003e17038))

* docs(readme): also add hint to delete gitlab-runner-test

Otherwise the whole testsuite will refuse to run ([`8894f2d`](https://github.com/python-gitlab/python-gitlab/commit/8894f2da81d885c1e788a3b21686212ad91d5bf2))

* docs(projects): correct fork docs

Closes #1126 ([`54921db`](https://github.com/python-gitlab/python-gitlab/commit/54921dbcf117f6b939e0c467738399be0d661a00))

* docs(cli): add example for job artifacts download ([`375b29d`](https://github.com/python-gitlab/python-gitlab/commit/375b29d3ab393f7b3fa734c5320736cdcba5df8a))

* docs(cli): add auto-generated CLI reference ([`6c21fc8`](https://github.com/python-gitlab/python-gitlab/commit/6c21fc83d3d6173bffb60e686ec579f875f8bebe))

### Feature

* feat: support multipart uploads ([`2fa3004`](https://github.com/python-gitlab/python-gitlab/commit/2fa3004d9e34cc4b77fbd6bd89a15957898e1363))

* feat: add MINIMAL_ACCESS constant

A &#34;minimal access&#34; access level was
[introduced](https://gitlab.com/gitlab-org/gitlab/-/issues/220203) in
GitLab 13.5. ([`49eb3ca`](https://github.com/python-gitlab/python-gitlab/commit/49eb3ca79172905bf49bab1486ecb91c593ea1d7))

* feat(tests): test label getter ([`a41af90`](https://github.com/python-gitlab/python-gitlab/commit/a41af902675a07cd4772bb122c152547d6d570f7))

* feat: adds support for project merge request approval rules (#1199) ([`c6fbf39`](https://github.com/python-gitlab/python-gitlab/commit/c6fbf399ec5cbc92f995a5d61342f295be68bd79))

* feat: unit tests added ([`f37ebf5`](https://github.com/python-gitlab/python-gitlab/commit/f37ebf5fd792c8e8a973443a1df386fa77d1248f))

* feat: added support for pipeline bridges ([`05cbdc2`](https://github.com/python-gitlab/python-gitlab/commit/05cbdc224007e9dda10fc2f6f7d63c82cf36dec0))

* feat(api): added wip filter param for merge requests ([`d6078f8`](https://github.com/python-gitlab/python-gitlab/commit/d6078f808bf19ef16cfebfaeabb09fbf70bfb4c7))

* feat(api): added wip filter param for merge requests ([`aa6e80d`](https://github.com/python-gitlab/python-gitlab/commit/aa6e80d58d765102892fadb89951ce29d08e1dab))

* feat(api): add support for user identity provider deletion ([`e78e121`](https://github.com/python-gitlab/python-gitlab/commit/e78e121575deb7b5ce490b2293caa290860fc3e9))

### Fix

* fix(api): use RetrieveMixin for ProjectLabelManager

Allows to get a single label from a project, which was missing before
even though the GitLab API has the ability to. ([`1a14395`](https://github.com/python-gitlab/python-gitlab/commit/1a143952119ce8e964cc7fcbfd73b8678ee2da74))

* fix(base): really refresh object

This fixes and error, where deleted attributes would not show up

Fixes #1155 ([`e1e0d8c`](https://github.com/python-gitlab/python-gitlab/commit/e1e0d8cbea1fed8aeb52b4d7cccd2e978faf2d3f))

* fix(cli): write binary data to stdout buffer ([`0733ec6`](https://github.com/python-gitlab/python-gitlab/commit/0733ec6cad5c11b470ce6bad5dc559018ff73b3c))

* fix: docs changed using the consts ([`650b65c`](https://github.com/python-gitlab/python-gitlab/commit/650b65c389c686bcc9a9cef81b6ca2a509d8cad2))

* fix: typo ([`9baa905`](https://github.com/python-gitlab/python-gitlab/commit/9baa90535b5a8096600f9aec96e528f4d2ac7d74))

* fix(cli): add missing args for project lists ([`c73e237`](https://github.com/python-gitlab/python-gitlab/commit/c73e23747d24ffef3c1a2a4e5f4ae24252762a71))

* fix(api): add missing runner access_level param ([`92669f2`](https://github.com/python-gitlab/python-gitlab/commit/92669f2ef2af3cac1c5f06f9299975060cc5e64a))

### Refactor

* refactor(tests): split functional tests ([`61e43eb`](https://github.com/python-gitlab/python-gitlab/commit/61e43eb186925feede073c7065e5ae868ffbb4ec))

### Test

* test: ignore failing test for now ([`4b4e253`](https://github.com/python-gitlab/python-gitlab/commit/4b4e25399f35e204320ac9f4e333b8cf7b262595))

* test: add test_project_merge_request_approvals.py ([`9f6335f`](https://github.com/python-gitlab/python-gitlab/commit/9f6335f7b79f52927d5c5734e47f4b8d35cd6c4a))

* test(cli): add test for job artifacts download ([`f4e7950`](https://github.com/python-gitlab/python-gitlab/commit/f4e79501f1be1394873042dd65beda49e869afb8))

* test(env): replace custom scripts with pytest and docker-compose ([`79489c7`](https://github.com/python-gitlab/python-gitlab/commit/79489c775141c4ddd1f7aecae90dae8061d541fe))

* test: add unit tests for badges API ([`2720b73`](https://github.com/python-gitlab/python-gitlab/commit/2720b7385a3686d3adaa09a3584d165bd7679367))

* test: add unit tests for resource label events API ([`e9a211c`](https://github.com/python-gitlab/python-gitlab/commit/e9a211ca8080e07727d0217e1cdc2851b13a85b7))

### Unknown

* Merge pull request #1273 from python-gitlab/chore/python3-9

chore: offically support and test 3.9 ([`48cb89b`](https://github.com/python-gitlab/python-gitlab/commit/48cb89bad043f7e406e2358a20512653fc40556d))

* Merge pull request #1230 from manuel-91/patch-1

cli-usage readme: fixed term ([`55c8c96`](https://github.com/python-gitlab/python-gitlab/commit/55c8c96e476f72cd8225c6033b4fb2ea800b55e6))

* Merge pull request #1238 from atombrella/install_version_doc

Updated supported Python versions in install doc ([`d037a71`](https://github.com/python-gitlab/python-gitlab/commit/d037a717fcb64ccb8e9958771f903ec95eea6d48))

* Merge pull request #1255 from bittner/docs/fix-external-links-tokens

Use inline anonymous references for external links ([`762f959`](https://github.com/python-gitlab/python-gitlab/commit/762f9592db69c872f6d64f9a2bba42f1dbc03bb1))

* Merge pull request #1251 from hchouraria/patch-1

docs(groups): add example for creating subgroups ([`5ac309a`](https://github.com/python-gitlab/python-gitlab/commit/5ac309a5eb420fdfdc023c8de9299c27eaeac186))

* Merge pull request #1272 from python-gitlab/renovate/pin-dependencies

chore(deps): pin dependency requests-toolbelt to ==0.9.1 ([`b567522`](https://github.com/python-gitlab/python-gitlab/commit/b567522443e78b12571f709dd3b3559dbd4ba741))

* Merge pull request #1233 from python-gitlab/renovate/requests-2.x

chore(deps): update dependency requests to v2.25.1 ([`78a02ce`](https://github.com/python-gitlab/python-gitlab/commit/78a02ced58566b9c05c9be37698f6ee1cfad088c))

* Merge pull request #1243 from python-gitlab/renovate/docker-gitlab-gitlab-ce-13.x

chore(deps): update gitlab/gitlab-ce docker tag to v13.8.1-ce.0 ([`cc2dd0c`](https://github.com/python-gitlab/python-gitlab/commit/cc2dd0c92e9844ae916c647a03e71b53df80bb15))

* Merge pull request #1252 from python-gitlab/feat/multipart-uploads

feat: support multipart uploads ([`4f8d901`](https://github.com/python-gitlab/python-gitlab/commit/4f8d9015869a2b8d3ee807319aa0423993083220))

* Merge pull request #1269 from nejch/fix/test-env

chore(ci): bring test environment back to life ([`fd179d4`](https://github.com/python-gitlab/python-gitlab/commit/fd179d4f88bf0707ef44fd5e3e007725a0331696))

* Merge pull request #1250 from JacobHenner/feature/add-minimal-access

feat: Add MINIMAL_ACCESS constant ([`fac0874`](https://github.com/python-gitlab/python-gitlab/commit/fac0874002cbb12fbacfb5fad28732c9c20d2e53))

* Merge pull request #1263 from ePirat/epirat-fix-get-label

fix(api): add missing GetMixin to ProjectLabelManager ([`e61a0f2`](https://github.com/python-gitlab/python-gitlab/commit/e61a0f2a1be030d28e8cb8fea9d703b7a34c12b8))

* Merge pull request #1200 from robinson96/feature/project_merge_request_approval_rules

Feature/project merge request approval rules ([`6035ca8`](https://github.com/python-gitlab/python-gitlab/commit/6035ca8ee91ab4c261253711d7a8a501d08fced0))

* Merge pull request #1213 from python-gitlab/fix/delete-attr

fix(base): really refresh object ([`af965d4`](https://github.com/python-gitlab/python-gitlab/commit/af965d484f2c7e7a5b4c5358b23f6a6629a9a6c6))

* Merge pull request #1212 from python-gitlab/chore/docs-edit-on-master

chore(docs): always edit the file directly on master ([`ce8460f`](https://github.com/python-gitlab/python-gitlab/commit/ce8460f976373311c423dcbc65fc981cdd252b73))

* Merge pull request #1211 from python-gitlab/docs/admin-project-owner

docs(issues): add admin, project owner hint ([`e5b047d`](https://github.com/python-gitlab/python-gitlab/commit/e5b047d3a326bd8c8deda83880c8bfd9c9b95fa1))

* Merge pull request #1214 from python-gitlab/docs/readme-gitlab-runner-test

docs(readme): also add hint to delete gitlab-runner-test ([`53b4c2f`](https://github.com/python-gitlab/python-gitlab/commit/53b4c2fea61a20e990a86caacddf8ff9112fa8db))

* Merge pull request #1210 from python-gitlab/docs/projects-correct-fork

docs(projects): correct fork docs ([`77ac8c3`](https://github.com/python-gitlab/python-gitlab/commit/77ac8c300fc647f18d4a71b84ae18a751bc1716f))

* Merge pull request #1202 from python-gitlab/fix/cli-binary-data

fix(cli): write binary data to stdout buffer ([`3a38c6d`](https://github.com/python-gitlab/python-gitlab/commit/3a38c6d78ceaed1116ebbdd8e5cded60c99c6f95))

* Merge pull request #1209 from python-gitlab/docs/cli-reference-page

docs(cli): add auto-generated CLI reference ([`9054a3b`](https://github.com/python-gitlab/python-gitlab/commit/9054a3be492091f3a323914ee24b682f993c9fcb))

* Merge pull request #1131 from valentingregoire/master

feat: added constants for search API ([`8cb8040`](https://github.com/python-gitlab/python-gitlab/commit/8cb8040198a6183c7c4bd3745af800fcf303fe43))

* Merge pull request #1205 from python-gitlab/refactor/split-functional-tests

refactor(tests): split functional tests ([`68a4162`](https://github.com/python-gitlab/python-gitlab/commit/68a41629ca0c27bd62d8e656071f612d443aaa1b))

* Merge pull request #1204 from python-gitlab/renovate/docker-python-3.x

chore(deps): update python docker tag to v3.9 ([`2002098`](https://github.com/python-gitlab/python-gitlab/commit/2002098a19f7a9302d373a867ab1a6f87848b6a0))

* Merge pull request #1203 from intostern/feat/bridge

Added support for pipeline bridges ([`c303dab`](https://github.com/python-gitlab/python-gitlab/commit/c303dabc720a2f840e7a45644647de59c7e0e7bf))

* Merge pull request #1206 from python-gitlab/fix/cli-project-list-args

fix(cli): add missing args for project lists ([`be0afdd`](https://github.com/python-gitlab/python-gitlab/commit/be0afdd3e0a7d94327fc075fcc0786b95731279d))

* Merge pull request #1178 from python-gitlab/test/cleanup-env

test(env): replace custom scripts with pytest and docker-compose ([`266030a`](https://github.com/python-gitlab/python-gitlab/commit/266030a67480aaf305069e8fea15b1528fa99d31))

* Merge pull request #1177 from python-gitlab/renovate/pin-dependencies

chore(deps): pin dependencies ([`0d89a6e`](https://github.com/python-gitlab/python-gitlab/commit/0d89a6e61bd4ae244c1545463272ef830d72dda9))

* Merge pull request #1189 from python-gitlab/chore/test-hacking-dependency

chore(test): remove hacking dependencies ([`d51042a`](https://github.com/python-gitlab/python-gitlab/commit/d51042a5f5f85256b2103bf83746b96e8622abeb))

* Merge pull request #1180 from Shkurupii/add-unittests-for-project-badges

test: add unit tests for badges API ([`6bdb7f8`](https://github.com/python-gitlab/python-gitlab/commit/6bdb7f8fd86543f683184e76e5c971ff669188ae))

* Merge pull request #1184 from python-gitlab/fix/runner-access-level

fix(api): add missing runner access_level param ([`a7c20ca`](https://github.com/python-gitlab/python-gitlab/commit/a7c20ca151fbbe379c40045415961b2035c93478))

* Merge pull request #1182 from jlpospisil/allow-mr-search-by-wip

Added MR wip filter param ([`74c1e4f`](https://github.com/python-gitlab/python-gitlab/commit/74c1e4fd4fc2815e897b90e3fc0f4b9d9eebe550))

* Merge pull request #1181 from python-gitlab/feat/delete-user-identities

feat(api): add support for user identity provider deletion ([`35f9cb8`](https://github.com/python-gitlab/python-gitlab/commit/35f9cb800c8b0d1473f3b6e113ff5c5a83874b7a))

* Merge pull request #1179 from python-gitlab/chore/readthedocs-yml

chore(ci): add .readthedocs.yml ([`49a0032`](https://github.com/python-gitlab/python-gitlab/commit/49a0032f44a76cdcf17dd45da4b23e24a6b9572c))

* Merge pull request #1175 from python-gitlab/chore/noisy-renovate

chore(ci): reduce renovate PR noise ([`8d662ab`](https://github.com/python-gitlab/python-gitlab/commit/8d662abf907fbdcec1f04629b911b159da77f4b0))

* Merge pull request #1174 from Shkurupii/add-unittests-for-resource-label-events

 Add unit tests for resource label events API ([`b1c2045`](https://github.com/python-gitlab/python-gitlab/commit/b1c204597f070a34495f35b25922ff6754537fb1))

* Merge pull request #1173 from python-gitlab/renovate/docker-gitlab-gitlab-ce-13.x

chore(deps): update gitlab/gitlab-ce docker tag to v13.3.5-ce.0 ([`24fdbef`](https://github.com/python-gitlab/python-gitlab/commit/24fdbef7dc38bebf41d8142f96f1a507207280ae))

* Merge pull request #1172 from python-gitlab/renovate/docker-gitlab-gitlab-ce-13.x

chore(deps): update gitlab/gitlab-ce docker tag to v13.3.4-ce.0 ([`2a6801e`](https://github.com/python-gitlab/python-gitlab/commit/2a6801e11b8af6ec9085e1131d5cac21a5e809f5))

* Merge pull request #1171 from python-gitlab/renovate/docker-gitlab-gitlab-ce-13.x

chore(deps): update gitlab/gitlab-ce docker tag to v13.3.3-ce.0 ([`769367c`](https://github.com/python-gitlab/python-gitlab/commit/769367c41d71610cc7d6a5eee67ebaaecb8b66bf))

## v2.5.0 (2020-09-01)

### Chore

* chore: bump python-gitlab to 2.5.0 ([`56fef01`](https://github.com/python-gitlab/python-gitlab/commit/56fef0180431f442ada5ce62352e4e813288257d))

* chore(deps): update python docker tag to v3.8 ([`a8070f2`](https://github.com/python-gitlab/python-gitlab/commit/a8070f2d9a996e57104f29539069273774cf5493))

* chore(test): use pathlib for paths ([`5a56b6b`](https://github.com/python-gitlab/python-gitlab/commit/5a56b6b55f761940f80491eddcdcf17d37215cfd))

* chore(deps): update gitlab/gitlab-ce docker tag to v13.3.2-ce.0 ([`9fd778b`](https://github.com/python-gitlab/python-gitlab/commit/9fd778b4a7e92a7405ac2f05c855bafbc51dc6a8))

* chore(ci): pin gitlab-ce version for renovate ([`cb79fb7`](https://github.com/python-gitlab/python-gitlab/commit/cb79fb72e899e65a1ad77ccd508f1a1baca30309))

* chore(env): add pre-commit and commit-msg hooks ([`82070b2`](https://github.com/python-gitlab/python-gitlab/commit/82070b2d2ed99189aebb1d595430ad5567306c4c))

* chore(ci): use fixed black version ([`9565684`](https://github.com/python-gitlab/python-gitlab/commit/9565684c86cb018fb22ee0b29345d2cd130f3fd7))

* chore: make latest black happy with existing code ([`6961479`](https://github.com/python-gitlab/python-gitlab/commit/696147922552a8e6ddda3a5b852ee2de6b983e37))

* chore: update tools dir for latest black version ([`c2806d8`](https://github.com/python-gitlab/python-gitlab/commit/c2806d8c0454a83dfdafd1bdbf7e10bb28d205e0))

* chore: remove unnecessary import ([`f337b7a`](https://github.com/python-gitlab/python-gitlab/commit/f337b7ac43e49f9d3610235749b1e2a21731352d))

* chore: make latest black happy with existing code ([`4039c8c`](https://github.com/python-gitlab/python-gitlab/commit/4039c8cfc6c7783270f0da1e235ef5d70b420ba9))

* chore: update tools dir for latest black version ([`f245ffb`](https://github.com/python-gitlab/python-gitlab/commit/f245ffbfad6f1d1f66d386a4b00b3a6ff3e74daa))

* chore: make latest black happy with existing code ([`d299753`](https://github.com/python-gitlab/python-gitlab/commit/d2997530bc3355048143bc29580ef32fc21dac3d))

* chore: run unittest2pytest on all unit tests ([`11383e7`](https://github.com/python-gitlab/python-gitlab/commit/11383e70f74c70e6fe8a56f18b5b170db982f402))

* chore: remove remnants of python2 imports ([`402566a`](https://github.com/python-gitlab/python-gitlab/commit/402566a665dfdf0862f15a7e59e4d804d1301c77))

### Documentation

* docs(variables): add docs for instance-level variables ([`ad4b87c`](https://github.com/python-gitlab/python-gitlab/commit/ad4b87cb3d6802deea971e6574ae9afe4f352e31))

* docs(api): add example for latest pipeline job artifacts ([`d20f022`](https://github.com/python-gitlab/python-gitlab/commit/d20f022a8fe29a6086d30aa7616aa1dac3e1bb17))

* docs(packages): add examples for Packages API and cli usage ([`a47dfcd`](https://github.com/python-gitlab/python-gitlab/commit/a47dfcd9ded3a0467e83396f21e6dcfa232dfdd7))

* docs(cli): add examples for group-project list ([`af86dcd`](https://github.com/python-gitlab/python-gitlab/commit/af86dcdd28ee1b16d590af31672c838597e3f3ec))

* docs: additional project file delete example

Showing how to delete without having to pull the file ([`9e94b75`](https://github.com/python-gitlab/python-gitlab/commit/9e94b7511de821619e8bcf66a3ae1f187f15d594))

### Feature

* feat(api): add support for instance variables ([`4492fc4`](https://github.com/python-gitlab/python-gitlab/commit/4492fc42c9f6e0031dd3f3c6c99e4c58d4f472ff))

* feat: add support to resource milestone events

Fixes #1154 ([`88f8cc7`](https://github.com/python-gitlab/python-gitlab/commit/88f8cc78f97156d5888a9600bdb8721720563120))

* feat(api): add endpoint for latest ref artifacts ([`b7a07fc`](https://github.com/python-gitlab/python-gitlab/commit/b7a07fca775b278b1de7d5cb36c8421b7d9bebb7))

* feat(api): add support for Packages API ([`71495d1`](https://github.com/python-gitlab/python-gitlab/commit/71495d127d30d2f4c00285485adae5454a590584))

* feat: add share/unshare group with group ([`7c6e541`](https://github.com/python-gitlab/python-gitlab/commit/7c6e541dc2642740a6ec2d7ed7921aca41446b37))

### Fix

* fix: wrong reconfirmation parameter when updating user&#39;s email

Since version 10.3 (and later), param to not send (re)confirmation when updating an user is
`skip_reconfirmation` (and not `skip_confirmation`).

See:

* https://gitlab.com/gitlab-org/gitlab-foss/-/merge_requests/15175?tab=
* https://docs.gitlab.com/11.11/ee/api/users.html#user-modification
* https://docs.gitlab.com/ee/api/users.html#user-modification ([`b5c267e`](https://github.com/python-gitlab/python-gitlab/commit/b5c267e110b2d7128da4f91c62689456d5ce275f))

* fix: tests fail when using REUSE_CONTAINER option

Fixes #1146 ([`0078f89`](https://github.com/python-gitlab/python-gitlab/commit/0078f8993c38df4f02da9aaa3f7616d1c8b97095))

* fix: implement Gitlab&#39;s behavior change for owned=True ([`9977799`](https://github.com/python-gitlab/python-gitlab/commit/99777991e0b9d5a39976d08554dea8bb7e514019))

### Refactor

* refactor: turn objects module into a package ([`da8af6f`](https://github.com/python-gitlab/python-gitlab/commit/da8af6f6be6886dca4f96390632cf3b91891954e))

* refactor: rewrite unit tests for objects with responses ([`204782a`](https://github.com/python-gitlab/python-gitlab/commit/204782a117f77f367dee87aa2c70822587829147))

* refactor: split unit tests by GitLab API resources ([`76b2cad`](https://github.com/python-gitlab/python-gitlab/commit/76b2cadf1418e4ea2ac420ebba5a4b4f16fbd4c7))

### Test

* test(api): add tests for variables API ([`66d108d`](https://github.com/python-gitlab/python-gitlab/commit/66d108de9665055921123476426fb6716c602496))

* test: add unit tests for resource milestone events API

Fixes #1154 ([`1317f4b`](https://github.com/python-gitlab/python-gitlab/commit/1317f4b62afefcb2504472d5b5d8e24f39b0d86f))

* test(packages): add tests for Packages API ([`7ea178b`](https://github.com/python-gitlab/python-gitlab/commit/7ea178bad398c8c2851a4584f4dca5b8adc89d29))

### Unknown

* Merge pull request #1170 from python-gitlab/chore/bump-to-2-5-0

chore: bump python-gitlab to 2.5.0 ([`784cba6`](https://github.com/python-gitlab/python-gitlab/commit/784cba659a9d15076711f5576549b4288df322cc))

* Merge pull request #1168 from python-gitlab/renovate/docker-python-3.x

chore(deps): update python docker tag to v3.8 ([`cf32499`](https://github.com/python-gitlab/python-gitlab/commit/cf324995e1477a43b8667b3a85c6a05aa4227199))

* Merge pull request #1163 from python-gitlab/feat/instance-variables-api

Feat: add support for instance variables API ([`723ca88`](https://github.com/python-gitlab/python-gitlab/commit/723ca886e3ef374d4238b0c41a3c678f148a6a07))

* Merge pull request #1167 from python-gitlab/renovate/docker-gitlab-gitlab-ce-13.x

chore(deps): update gitlab/gitlab-ce docker tag to v13.3.2-ce.0 ([`6e1ed68`](https://github.com/python-gitlab/python-gitlab/commit/6e1ed68842708e94fe1e4a07700d224fc93063a0))

* Merge pull request #1165 from DylannCordel/fix-user-email-reconfirmation

fix: wrong reconfirmation parameter when updating user&#39;s email ([`97e1dcc`](https://github.com/python-gitlab/python-gitlab/commit/97e1dcc889463305943612e3ffc87e111a9396cb))

* Merge pull request #1164 from nejch/master

chore(ci): pin gitlab-ce version for renovate ([`e6a9ba9`](https://github.com/python-gitlab/python-gitlab/commit/e6a9ba99692105405622ed196db36a05c2dcb1b8))

* Merge pull request #1162 from python-gitlab/chore/pre-commit-config

chore(env): add pre-commit and commit-msg hooks ([`97d8261`](https://github.com/python-gitlab/python-gitlab/commit/97d82610a091a85e6c118d0ad7914dcb898ec4dc))

* Merge pull request #1161 from python-gitlab/chore/ci-fixed-black-version

chore(ci): use fixed black version ([`28aa17e`](https://github.com/python-gitlab/python-gitlab/commit/28aa17e56df5de4f2c74c831910559387414c487))

* Merge pull request #1157 from Shkurupii/issue-1154

Add support to resource milestone events ([`750f4ee`](https://github.com/python-gitlab/python-gitlab/commit/750f4ee6554381830e6add55583903919db2ba29))

* Merge branch &#39;master&#39; into issue-1154 ([`fa899d7`](https://github.com/python-gitlab/python-gitlab/commit/fa899d7a6e76acbe392f3debb5fd61d71bd88ed2))

* Merge pull request #1159 from python-gitlab/feat/project-artifacts

Feat: Project job artifacts for latest successful pipeline ([`26f95f3`](https://github.com/python-gitlab/python-gitlab/commit/26f95f30a5219243f33d505747c65f798ac6a486))

* Merge pull request #1160 from python-gitlab/feat/packages-api

Feat: Add support for packages API ([`0f42e32`](https://github.com/python-gitlab/python-gitlab/commit/0f42e32cb756766735c7e277f099030f6b3d8fc7))

* Merge pull request #1156 from python-gitlab/docs/group-projects-list-cli

docs(cli): add examples for group-project list ([`a038e95`](https://github.com/python-gitlab/python-gitlab/commit/a038e9567fd16259e3ed360ab0defd779e9c3901))

* Merge pull request #1078 from python-gitlab/refactor/split-unit-tests

Refactor: split unit tests by API resources ([`a7e44a0`](https://github.com/python-gitlab/python-gitlab/commit/a7e44a0bb3629f776a52967d56ba67d9a61346eb))

* Merge pull request #1147 from ericfrederich/fix-1146

fix: tests fail when using REUSE_CONTAINER option ([`e2dc9ec`](https://github.com/python-gitlab/python-gitlab/commit/e2dc9ece1a0af37073c41bfa8161fcec5fa01234))

* Merge pull request #1139 from sathieu/share_group_with_group

feat: add share/unshare the group with a group ([`cfa8097`](https://github.com/python-gitlab/python-gitlab/commit/cfa80974a1e767928016e3935d2fd94d4ab705c1))

* Merge pull request #1152 from matthew-a-dunlap/doc-project-file-delete-example

docs: additional project file delete example ([`5b92de8`](https://github.com/python-gitlab/python-gitlab/commit/5b92de8eba9224210ecff1a1d4dae6a561c894be))

## v2.4.0 (2020-07-09)

### Chore

* chore: bump version to 2.4.0 ([`1606310`](https://github.com/python-gitlab/python-gitlab/commit/1606310a880f8a8a2a370db27511b57732caf178))

### Documentation

* docs(pipelines): simplify download

This uses a context instead of inventing your own stream handler which
makes the code simpler and should be fine for most use cases.

Signed-off-by: Paul Spooren &lt;mail@aparcar.org&gt; ([`9a068e0`](https://github.com/python-gitlab/python-gitlab/commit/9a068e00eba364eb121a2d7d4c839e2f4c7371c8))

### Feature

* feat: added NO_ACCESS const

This constant is useful for cases where no access is granted,
e.g. when creating a protected branch.

The `NO_ACCESS` const corresponds to the definition in
https://docs.gitlab.com/ee/api/protected_branches.html ([`dab4d0a`](https://github.com/python-gitlab/python-gitlab/commit/dab4d0a1deec6d7158c0e79b9eef20d53c0106f0))

### Fix

* fix: do not check if kwargs is none

Co-authored-by: Traian Nedelea &lt;tron1point0@pm.me&gt; ([`a349b90`](https://github.com/python-gitlab/python-gitlab/commit/a349b90ea6016ec8fbe91583f2bbd9832b41a368))

* fix: make query kwargs consistent between call in init and next ([`72ffa01`](https://github.com/python-gitlab/python-gitlab/commit/72ffa0164edc44a503364f9b7e25c5b399f648c3))

* fix: pass kwargs to subsequent queries in gitlab list ([`1d011ac`](https://github.com/python-gitlab/python-gitlab/commit/1d011ac72aeb18b5f31d10e42ffb49cf703c3e3a))

* fix: add masked parameter for variables command ([`b6339bf`](https://github.com/python-gitlab/python-gitlab/commit/b6339bf85f3ae11d31bf03c4132f6e7b7c343900))

* fix(merge): parse arguments as query_data ([`878098b`](https://github.com/python-gitlab/python-gitlab/commit/878098b74e216b4359e0ce012ff5cd6973043a0a))

### Unknown

* Merge pull request #1108 from stuartgunter/master

Added NO_ACCESS const ([`3a76d91`](https://github.com/python-gitlab/python-gitlab/commit/3a76d9194cea10e5a4714c18ac453343350b7d84))

* Merge pull request #1092 from aparcar/aparcar-patch-1

Update pipelines_and_jobs.rst ([`12a40cc`](https://github.com/python-gitlab/python-gitlab/commit/12a40cc3bdae6111ed750edb3c3a4ec8dbdaa8ef))

* Merge pull request #1124 from tyates-indeed/fix-1123

Pass kwargs to subsequent queries in GitlabList (fixes: #1123) ([`424a8cb`](https://github.com/python-gitlab/python-gitlab/commit/424a8cb3f3e0baa7d45748986395a7a921ba28b8))

* Merge pull request #1127 from gervasek/master

Add masked parameter for project-variable and group-variable ([`bfb5034`](https://github.com/python-gitlab/python-gitlab/commit/bfb50348b636d2b70a15edf3b065c0406ed6d511))

* Merge pull request #1121 from ferhat-aram/fix/bad-merge-request-arg-parsing

fix(merge): parse arguments as query_data ([`1d82310`](https://github.com/python-gitlab/python-gitlab/commit/1d82310da1a15f7172a3f87c2cf062bc0c17944d))

## v2.3.1 (2020-06-09)

### Chore

* chore: bump version to 2.3.1 ([`870e7ea`](https://github.com/python-gitlab/python-gitlab/commit/870e7ea12ee424eb2454dd7d4b7906f89fbfea64))

### Fix

* fix: disable default keyset pagination

Instead we set pagination to offset on the other paths ([`e71fe16`](https://github.com/python-gitlab/python-gitlab/commit/e71fe16b47835aa4db2834e98c7ffc6bdec36723))

### Unknown

* Merge pull request #1115 from python-gitlab/fix/keyset-pagination-revert

Fix/keyset pagination revert ([`3f585ad`](https://github.com/python-gitlab/python-gitlab/commit/3f585ad3f823aef4dd848942399e2bd0530a09b2))

## v2.3.0 (2020-06-08)

### Chore

* chore: correctly render rst ([`f674bf2`](https://github.com/python-gitlab/python-gitlab/commit/f674bf239e6ced4f420bee0a642053f63dace28b))

* chore: bump to 2.3.0 ([`01ff865`](https://github.com/python-gitlab/python-gitlab/commit/01ff8658532e7a7d3b53ba825c7ee311f7feb1ab))

* chore(ci): add codecov integration to Travis ([`e230568`](https://github.com/python-gitlab/python-gitlab/commit/e2305685dea2d99ca389f79dc40e40b8d3a1fee0))

* chore(test): remove outdated token test ([`e6c9fe9`](https://github.com/python-gitlab/python-gitlab/commit/e6c9fe920df43ae2ab13f26310213e8e4db6b415))

* chore: bring commit signatures up to date with 12.10 ([`dc382fe`](https://github.com/python-gitlab/python-gitlab/commit/dc382fe3443a797e016f8c5f6eac68b7b69305ab))

* chore: fix typo in docstring ([`c20f5f1`](https://github.com/python-gitlab/python-gitlab/commit/c20f5f15de84d1b1bbb12c18caf1927dcfd6f393))

* chore: remove old builds-email service ([`c60e2df`](https://github.com/python-gitlab/python-gitlab/commit/c60e2df50773535f5cfdbbb974713f28828fd827))

* chore(services): update available service attributes ([`7afc357`](https://github.com/python-gitlab/python-gitlab/commit/7afc3570c02c5421df76e097ce33d1021820a3d6))

* chore: use pytest for unit tests and coverage ([`9787a40`](https://github.com/python-gitlab/python-gitlab/commit/9787a407b700f18dadfb4153b3ba1375a615b73c))

### Ci

* ci: lint fixes ([`930122b`](https://github.com/python-gitlab/python-gitlab/commit/930122b1848b3d42af1cf8567a065829ec0eb44f))

* ci: add a test for creating and triggering pipeline schedule ([`9f04560`](https://github.com/python-gitlab/python-gitlab/commit/9f04560e59f372f80ac199aeee16378d8f80610c))

### Documentation

* docs(remote_mirrors): fix create command ([`bab91fe`](https://github.com/python-gitlab/python-gitlab/commit/bab91fe86fc8d23464027b1c3ab30619e520235e))

* docs(remote_mirrors): fix create command ([`1bb4e42`](https://github.com/python-gitlab/python-gitlab/commit/1bb4e42858696c9ac8cbfc0f89fa703921b969f3))

* docs: update authors ([`ac0c84d`](https://github.com/python-gitlab/python-gitlab/commit/ac0c84de02a237db350d3b21fe74d0c24d85a94e))

* docs(readme): add codecov badge for master ([`e21b2c5`](https://github.com/python-gitlab/python-gitlab/commit/e21b2c5c6a600c60437a41f231fea2adcfd89fbd))

* docs(readme): update test docs ([`6e2b1ec`](https://github.com/python-gitlab/python-gitlab/commit/6e2b1ec947a6e352b412fd4e1142006621dd76a4))

### Feature

* feat: add group runners api ([`4943991`](https://github.com/python-gitlab/python-gitlab/commit/49439916ab58b3481308df5800f9ffba8f5a8ffd))

* feat: add play command to project pipeline schedules

fix: remove version from setup

feat: add pipeline schedule play error exception

docs: add documentation for pipeline schedule play ([`07b9988`](https://github.com/python-gitlab/python-gitlab/commit/07b99881dfa6efa9665245647460e99846ccd341))

* feat(api): added support in the GroupManager to upload Group avatars ([`28eb7ea`](https://github.com/python-gitlab/python-gitlab/commit/28eb7eab8fbe3750fb56e85967e8179b7025f441))

* feat(services): add project service list API

Can be used to list available services
It was introduced in GitLab 12.7 ([`fc52221`](https://github.com/python-gitlab/python-gitlab/commit/fc5222188ad096932fa89bb53f03f7118926898a))

* feat: allow an environment variable to specify config location

It can be useful (especially in scripts) to specify a configuration
location via an environment variable. If the &#34;PYTHON_GITLAB_CFG&#34;
environment variable is defined, treat its value as the path to a
configuration file and include it in the set of default configuration
locations. ([`401e702`](https://github.com/python-gitlab/python-gitlab/commit/401e702a9ff14bf4cc33b3ed3acf16f3c60c6945))

* feat(types): add __dir__ to RESTObject to expose attributes ([`cad134c`](https://github.com/python-gitlab/python-gitlab/commit/cad134c078573c009af18160652182e39ab5b114))

### Fix

* fix: use keyset pagination by default for /projects &gt; 50000

Workaround for https://gitlab.com/gitlab-org/gitlab/-/issues/218504.
Remove this in 13.1 ([`f86ef3b`](https://github.com/python-gitlab/python-gitlab/commit/f86ef3bbdb5bffa1348a802e62b281d3f31d33ad))

* fix(config): fix duplicate code

Fixes #1094 ([`ee2df6f`](https://github.com/python-gitlab/python-gitlab/commit/ee2df6f1757658cae20cc1d9dd75be599cf19997))

* fix(project): add missing project parameters ([`ad8c67d`](https://github.com/python-gitlab/python-gitlab/commit/ad8c67d65572a9f9207433e177834cc66f8e48b3))

### Test

* test: disable test until Gitlab 13.1 ([`63ae77a`](https://github.com/python-gitlab/python-gitlab/commit/63ae77ac1d963e2c45bbed7948d18313caf2c016))

* test(runners): add all runners unit tests ([`127fa5a`](https://github.com/python-gitlab/python-gitlab/commit/127fa5a2134aee82958ce05357d60513569c3659))

* test(cli): convert shell tests to pytest test cases ([`c4ab4f5`](https://github.com/python-gitlab/python-gitlab/commit/c4ab4f57e23eed06faeac8d4fa9ffb9ce5d47e48))

### Unknown

* Merge pull request #1112 from python-gitlab/fix/rst-renderer

chore: correctly render rst ([`1f7dbc8`](https://github.com/python-gitlab/python-gitlab/commit/1f7dbc8dfb9c200d31ce8fad06feb235cade1481))

* Merge pull request #1111 from python-gitlab/chore/bump-version-2-3-0

chore: bump to 2.3.0 ([`a16ff3f`](https://github.com/python-gitlab/python-gitlab/commit/a16ff3f3dc29f79dacb07b120f3f9614325e03be))

* Merge pull request #1110 from python-gitlab/fix/keyset-pagination

Fix keyset pagination in 13.0 ([`f10dd38`](https://github.com/python-gitlab/python-gitlab/commit/f10dd3817a015eb5ee22b209ca9d12805a5dd714))

* Merge pull request #1102 from dotenorio/master

Update doc for remote_mirrors ([`ef6181b`](https://github.com/python-gitlab/python-gitlab/commit/ef6181bb5f5148739863da6838ac400fd76e4c0e))

* Merge branch &#39;master&#39; of github.com:dotenorio/python-gitlab ([`f5f4e12`](https://github.com/python-gitlab/python-gitlab/commit/f5f4e1236df67b79d90fde00b4a34a51b1e176ac))

* Merge pull request #1089 from python-gitlab/feat/group-runners

feat: add group runners api ([`38e9fde`](https://github.com/python-gitlab/python-gitlab/commit/38e9fde46a2e9e630154feb1cc533a75a55e4a2a))

* Merge pull request #1087 from python-gitlab/docs/update-authors

docs: update authors ([`89007c9`](https://github.com/python-gitlab/python-gitlab/commit/89007c9d1a642bda87ca086f00acf0f47d663611))

* Merge pull request #1099 from python-gitlab/fix/duplicate-code

fix(config): fix duplicate code ([`242cf65`](https://github.com/python-gitlab/python-gitlab/commit/242cf65fa4f6fa676a83c8a42061b003f0177ecc))

* Merge pull request #1086 from python-gitlab/test/pytest-cli-tests

test(cli): convert CLI shell tests to pytest test cases ([`74b3ddc`](https://github.com/python-gitlab/python-gitlab/commit/74b3ddcd5d44c4fe6c7c0189f87852d861e807f0))

* Merge pull request #1085 from python-gitlab/chore/codecov-travis

chore(ci): add codecov integration to Travis ([`91c1c27`](https://github.com/python-gitlab/python-gitlab/commit/91c1c27956a51e2e12e3104c30988696711230ff))

* Merge pull request #1082 from python-gitlab/chore/signature-gpg-x509

chore: bring commit signatures up to date with 12.10 ([`5a75310`](https://github.com/python-gitlab/python-gitlab/commit/5a753105d95859854e52adc2575a9a51d43c341c))

* Merge pull request #1069 from zillow/feat/add-custom-pipeline-schedule-play

feat: Add play command to project pipeline schedules ([`9d66cb3`](https://github.com/python-gitlab/python-gitlab/commit/9d66cb3ccc8d9edac68380b4b8ff285a9782e698))

* Merge pull request #1077 from Flor1an-dev/master

feat(api): added support in the GroupManager to upload Group avatars ([`7907e5a`](https://github.com/python-gitlab/python-gitlab/commit/7907e5a4b602d22d03d71ca51c6803f634bd8a78))

* Merge pull request #1075 from python-gitlab/feat/available-services

feat(services): add project service list API ([`dad505c`](https://github.com/python-gitlab/python-gitlab/commit/dad505c5e6aac3081ed796227e8f21d28b217ea0))

* Merge pull request #1074 from jeremycline/environment-variable

feat: Allow an environment variable to specify config location ([`0c3b717`](https://github.com/python-gitlab/python-gitlab/commit/0c3b717f9376668696ad13b6b481f28ab3c03abf))

* Merge pull request #1073 from python-gitlab/docs/readme-test-docs

docs(readme): update test docs ([`70cefe4`](https://github.com/python-gitlab/python-gitlab/commit/70cefe4d5b7f29db6c8c1deef524076510fd350a))

* Merge pull request #1072 from spyoungtech/feat/restobject-dir

feat(types): add __dir__ to RESTObject to expose attributes ([`c7c431a`](https://github.com/python-gitlab/python-gitlab/commit/c7c431af16f256f95a9553cf2e14925fa75f7d62))

* Merge pull request #1066 from nejch/chore/pytest-for-unit-tests

chore: use pytest to run unit tests and coverage ([`efc6182`](https://github.com/python-gitlab/python-gitlab/commit/efc6182378509f1e66c55b3443c6afcb2873dc77))

* Merge pull request #1067 from python-gitlab/fix/missing-project-attributes

fix(project): add missing project parameters ([`29fd95e`](https://github.com/python-gitlab/python-gitlab/commit/29fd95e7edbb0369b845afb7e9ee4dbed2e1d483))

## v2.2.0 (2020-04-07)

### Chore

* chore: bump to 2.2.0 ([`22d4b46`](https://github.com/python-gitlab/python-gitlab/commit/22d4b465c3217536cb444dafe5c25e9aaa3aa7be))

* chore: use raise..from for chained exceptions (#939) ([`79fef26`](https://github.com/python-gitlab/python-gitlab/commit/79fef262c3e05ff626981c891d9377abb1e18533))

* chore: rename ExportMixin to DownloadMixin ([`847da60`](https://github.com/python-gitlab/python-gitlab/commit/847da6063b4c63c8133e5e5b5b45e5b4f004bdc4))

* chore(mixins): factor out export download into ExportMixin ([`6ce5d1f`](https://github.com/python-gitlab/python-gitlab/commit/6ce5d1f14060a403f05993d77bf37720c25534ba))

* chore(group): update group_manager attributes (#1062)

* chore(group): update group_manager attributes

Co-Authored-By: Nejc Habjan &lt;hab.nejc@gmail.com&gt; ([`fa34f5e`](https://github.com/python-gitlab/python-gitlab/commit/fa34f5e20ecbd3f5d868df2fa9e399ac6559c5d5))

* chore: fix typo in allow_failures ([`265bbdd`](https://github.com/python-gitlab/python-gitlab/commit/265bbddacc25d709a8f13807ed04cae393d9802d))

* chore: pass environment variables in tox ([`e06d33c`](https://github.com/python-gitlab/python-gitlab/commit/e06d33c1bcfa71e0c7b3e478d16b3a0e28e05a23))

* chore: improve and document testing against different images ([`98d3f77`](https://github.com/python-gitlab/python-gitlab/commit/98d3f770c4cc7e15493380e1a2201c63f0a332a2))

* chore: remove references to python2 in test env ([`6e80723`](https://github.com/python-gitlab/python-gitlab/commit/6e80723e5fa00e8b870ec25d1cb2484d4b5816ca))

* chore: clean up for black and flake8 ([`4fede5d`](https://github.com/python-gitlab/python-gitlab/commit/4fede5d692fdd4477a37670b7b35268f5d1c4bf0))

* chore: flatten test_import_github ([`b8ea96c`](https://github.com/python-gitlab/python-gitlab/commit/b8ea96cc20519b751631b27941d60c486aa4188c))

* chore: move test_import_github into TestProjectImport ([`a881fb7`](https://github.com/python-gitlab/python-gitlab/commit/a881fb71eebf744bcbe232869f622ea8a3ac975f))

### Documentation

* docs: add docs for Group Import/Export API ([`8c3d744`](https://github.com/python-gitlab/python-gitlab/commit/8c3d744ec6393ad536b565c94f120b3e26b6f3e8))

* docs: fix comment of prev_page()

Co-Authored-By: Nejc Habjan &lt;hab.nejc@gmail.com&gt; ([`b066b41`](https://github.com/python-gitlab/python-gitlab/commit/b066b41314f55fbdc4ee6868d1e0aba1e5620a48))

* docs: fix comment of prev_page()

Co-Authored-By: Nejc Habjan &lt;hab.nejc@gmail.com&gt; ([`ac6b2da`](https://github.com/python-gitlab/python-gitlab/commit/ac6b2daf8048f4f6dea14bbf142b8f3a00726443))

* docs: fix comment of prev_page() ([`7993c93`](https://github.com/python-gitlab/python-gitlab/commit/7993c935f62e67905af558dd06394764e708cafe))

### Feature

* feat(api): add support for Gitlab Deploy Token API ([`01de524`](https://github.com/python-gitlab/python-gitlab/commit/01de524ce39a67b549b3157bf4de827dd0568d6b))

* feat(api): add support for remote mirrors API (#1056) ([`4cfaa2f`](https://github.com/python-gitlab/python-gitlab/commit/4cfaa2fd44b64459f6fc268a91d4469284c0e768))

* feat(api): add support for Group Import/Export API (#1037) ([`6cb9d92`](https://github.com/python-gitlab/python-gitlab/commit/6cb9d9238ea3cc73689d6b71e991f2ec233ee8e6))

* feat: add create from template args to ProjectManager

This commit adds the v4 Create project attributes necessary to create a
project from a project, instance, or group level template as documented
in https://docs.gitlab.com/ee/api/projects.html#create-project ([`f493b73`](https://github.com/python-gitlab/python-gitlab/commit/f493b73e1fbd3c3f1a187fed2de26030f00a89c9))

* feat: add support for commit GPG signature API ([`da7a809`](https://github.com/python-gitlab/python-gitlab/commit/da7a809772233be27fa8e563925dd2e44e1ce058))

### Fix

* fix(types): do not split single value string in ListAttribute ([`a26e585`](https://github.com/python-gitlab/python-gitlab/commit/a26e58585b3d82cf1a3e60a3b7b3bfd7f51d77e5))

* fix: add missing import_project param ([`9b16614`](https://github.com/python-gitlab/python-gitlab/commit/9b16614ba6444b212b3021a741b9c184ac206af1))

### Test

* test(api): add tests for group export/import API ([`e7b2d6c`](https://github.com/python-gitlab/python-gitlab/commit/e7b2d6c873f0bfd502d06c9bd239cedc465e51c5))

* test(types): reproduce get_for_api splitting strings (#1057) ([`babd298`](https://github.com/python-gitlab/python-gitlab/commit/babd298eca0586dce134d65586bf50410aacd035))

* test: create separate module for commit tests ([`8c03771`](https://github.com/python-gitlab/python-gitlab/commit/8c037712a53c1c54e46298fbb93441d9b7a7144a))

* test: move mocks to top of module ([`0bff713`](https://github.com/python-gitlab/python-gitlab/commit/0bff71353937a451b1092469330034062d24ff71))

* test: add unit tests for Project Import ([`f7aad5f`](https://github.com/python-gitlab/python-gitlab/commit/f7aad5f78c49ad1a4e05a393bcf236b7bbad2f2a))

* test: add unit tests for Project Export ([`600dc86`](https://github.com/python-gitlab/python-gitlab/commit/600dc86f34b6728b37a98b44e6aba73044bf3191))

* test: prepare base project test class for more tests ([`915587f`](https://github.com/python-gitlab/python-gitlab/commit/915587f72de85b45880a2f1d50bdae1a61eb2638))

### Unknown

* Merge pull request #1059 from python-gitlab/fix/raise-from

chore: use raise..from for chained exceptions (#939) ([`6749859`](https://github.com/python-gitlab/python-gitlab/commit/6749859505db73655f13a7950e70b67c1ee1d0fb))

* Merge pull request #1052 from machine424/deploy-tokens-support

feat(api): add support for Gitlab Deploy Token API ([`5979750`](https://github.com/python-gitlab/python-gitlab/commit/5979750fcc953148fcca910c04258f56c3027bce))

* Merge pull request #1064 from python-gitlab/feat/project-remote-mirrors

feat(api): add support for remote mirrors API (#1056) ([`3396aa5`](https://github.com/python-gitlab/python-gitlab/commit/3396aa51e055b7e7d3bceddc1b91deed17323f3a))

* Merge pull request #1063 from python-gitlab/feat/group-import-export

Feat: support for group import/export API ([`c161852`](https://github.com/python-gitlab/python-gitlab/commit/c161852b5a976d11f682c5af00ff3f4e8daa26ef))

* Merge pull request #1058 from python-gitlab/fix/listattribute-get-api-splits-string

Fix: ListAttribute get_for_api() splits strings ([`50fcd12`](https://github.com/python-gitlab/python-gitlab/commit/50fcd1237613645031410386e87b96b81ef5fb78))

* Merge pull request #1053 from lassimus/master

feat: add create from template args to ProjectManager ([`c5904c4`](https://github.com/python-gitlab/python-gitlab/commit/c5904c4c2e79ec302ff0de20bcb2792be4924bbe))

* Merge pull request #1054 from nejch/chore/cleanup-test-env

chore: improve test environment for upcoming features ([`8173021`](https://github.com/python-gitlab/python-gitlab/commit/8173021f996aca60756bfb248fdf8748d7a813df))

* Merge pull request #1055 from nejch/feat/commit-gpg-signature

feat: add support for commit GPG signature ([`1b8e748`](https://github.com/python-gitlab/python-gitlab/commit/1b8e74887945b363eb46908f2b5f9fa7eb6da40d))

* Merge pull request #1049 from donhui/typo-fix

* docs: fix comment of prev_page() ([`82deb7d`](https://github.com/python-gitlab/python-gitlab/commit/82deb7dbe261c4b42a9c45a5b85a2c767f3a8218))

* Merge pull request #1040 from nejch/test/project-export-import

test: update tests and params for project export/import ([`4ffaf1d`](https://github.com/python-gitlab/python-gitlab/commit/4ffaf1dc0365690df810c99573f5737f635240e0))

## v2.1.2 (2020-03-09)

### Chore

* chore: bump version to 2.1.2 ([`ad7e2bf`](https://github.com/python-gitlab/python-gitlab/commit/ad7e2bf7472668ffdcc85eec30db4139b92595a6))

### Unknown

* Merge pull request #1045 from python-gitlab/revert-1003-feat/all-keyset-pagination

Revert &#34;feat: use keyset pagination by default for `all=True`&#34; ([`6d941bd`](https://github.com/python-gitlab/python-gitlab/commit/6d941bdd90414d9ddce9f90166dbdc2adaf01d7d))

* Revert &#34;feat: use keyset pagination by default for `all=True`&#34; ([`6f843b6`](https://github.com/python-gitlab/python-gitlab/commit/6f843b63f7227ee3d338724d49b3ce111366a738))

## v2.1.1 (2020-03-09)

### Chore

* chore: bump version to 2.1.1 ([`6c5458a`](https://github.com/python-gitlab/python-gitlab/commit/6c5458a3bfc3208ad2d7cc40e1747f7715abe449))

* chore(user): update user attributes to 12.8 ([`666f880`](https://github.com/python-gitlab/python-gitlab/commit/666f8806eb6b3455ea5531b08cdfc022916616f0))

### Fix

* fix(docs): additional project statistics example ([`5ae5a06`](https://github.com/python-gitlab/python-gitlab/commit/5ae5a0627f85abba23cda586483630cefa7cf36c))

### Unknown

* Merge pull request #1043 from python-gitlab/chore/update-user-attributes

chore(user): update user attributes to 12.8 ([`8c44bb6`](https://github.com/python-gitlab/python-gitlab/commit/8c44bb6540f0e114525ec33f442a5fcf7eb381b6))

* Merge pull request #1042 from khuedoan98/patch-1

fix(docs): additional project statistics example ([`be5b15e`](https://github.com/python-gitlab/python-gitlab/commit/be5b15e27ad4a58d61f26e9f5ca3868f72959faa))

## v2.1.0 (2020-03-08)

### Chore

* chore: bump version to 2.1.0 ([`47cb58c`](https://github.com/python-gitlab/python-gitlab/commit/47cb58c24af48c77c372210f9e791edd2c2c98b0))

* chore: fix broken requests links

Another case of the double slash rewrite. ([`b392c21`](https://github.com/python-gitlab/python-gitlab/commit/b392c21c669ae545a6a7492044479a401c0bcfb3))

* chore: ensure developers use same gitlab image as Travis ([`fab17fc`](https://github.com/python-gitlab/python-gitlab/commit/fab17fcd6258b8c3aa3ccf6c00ab7b048b6beeab))

### Documentation

* docs: add reference for REQUESTS_CA_BUNDLE ([`37e8d5d`](https://github.com/python-gitlab/python-gitlab/commit/37e8d5d2f0c07c797e347a7bc1441882fe118ecd))

* docs(pagination): clear up pagination docs

Co-Authored-By: Mitar &lt;mitar.git@tnode.com&gt; ([`1609824`](https://github.com/python-gitlab/python-gitlab/commit/16098244ad7c19867495cf4f0fda0c83fe54cd2b))

### Feature

* feat(api): add support for GitLab OAuth Applications API ([`4e12356`](https://github.com/python-gitlab/python-gitlab/commit/4e12356d6da58c9ef3d8bf9ae67e8aef8fafac0a))

* feat: use keyset pagination by default for `all=True` ([`99b4484`](https://github.com/python-gitlab/python-gitlab/commit/99b4484da924f9378518a1a1194e1a3e75b48073))

* feat: add support for user memberships API (#1009) ([`c313c2b`](https://github.com/python-gitlab/python-gitlab/commit/c313c2b01d796418539e42d578fed635f750cdc1))

* feat: add support for commit revert API (#991) ([`5298964`](https://github.com/python-gitlab/python-gitlab/commit/5298964ee7db8a610f23de2d69aad8467727ca97))

* feat: add capability to control GitLab features per project or group ([`7f192b4`](https://github.com/python-gitlab/python-gitlab/commit/7f192b4f8734e29a63f1c79be322c25d45cfe23f))

### Fix

* fix(projects): correct copy-paste error ([`adc9101`](https://github.com/python-gitlab/python-gitlab/commit/adc91011e46dfce909b7798b1257819ec09d01bd))

* fix(objects): add default name data and use http post

Updating approvers new api needs a POST call. Also It needs a name of the new rule, defaulting this to &#39;name&#39;. ([`70c0cfb`](https://github.com/python-gitlab/python-gitlab/commit/70c0cfb686177bc17b796bf4d7eea8b784cf9651))

* fix: do not require empty data dict for create() ([`99d959f`](https://github.com/python-gitlab/python-gitlab/commit/99d959f74d06cca8df3f2d2b3a4709faba7799cb))

* fix(docs): fix typo in user memberships example ([`33889bc`](https://github.com/python-gitlab/python-gitlab/commit/33889bcbedb4aa421ea5bf83c13abe3168256c62))

* fix: remove trailing slashes from base URL (#913) ([`2e396e4`](https://github.com/python-gitlab/python-gitlab/commit/2e396e4a84690c2ea2ea7035148b1a6038c03301))

* fix: return response with commit data ([`b77b945`](https://github.com/python-gitlab/python-gitlab/commit/b77b945c7e0000fad4c422a5331c7e905e619a33))

* fix(docs): update to new set approvers call for # of approvers

to set the # of approvers for an MR you need to use the same function as for setting the approvers id. ([`8e0c526`](https://github.com/python-gitlab/python-gitlab/commit/8e0c52620af47a9e2247eeb7dcc7a2e677822ff4))

* fix(objects): update set_approvers function call

Added a miss paramter update to the set_approvers function ([`65ecadc`](https://github.com/python-gitlab/python-gitlab/commit/65ecadcfc724a7086e5f84dbf1ecc9f7a02e5ed8))

* fix(docs and tests): update docs and tests for set_approvers

Updated the docs with the new set_approvers arguments, and updated tests with the arg as well. ([`2cf12c7`](https://github.com/python-gitlab/python-gitlab/commit/2cf12c7973e139c4932da1f31c33bb7658b132f7))

* fix(objects): update to new gitlab api for path, and args

Updated the gitlab path for set_approvers to approvers_rules, added default arg for rule type, and added arg for # of approvals required. ([`e512cdd`](https://github.com/python-gitlab/python-gitlab/commit/e512cddd30f3047230e8eedb79d98dc06e93a77b))

* fix: remove null values from features POST data, because it fails
with HTTP 500 ([`1ec1816`](https://github.com/python-gitlab/python-gitlab/commit/1ec1816d7c76ae079ad3b3e3b7a1bae70e0dd95b))

### Performance

* perf: prepare environment when gitlab is reconfigured ([`3834d9c`](https://github.com/python-gitlab/python-gitlab/commit/3834d9cf800a0659433eb640cb3b63a947f0ebda))

### Style

* style: fix black violations ([`ad3e833`](https://github.com/python-gitlab/python-gitlab/commit/ad3e833671c49db194c86e23981215b13b96bb1d))

### Test

* test: add unit tests for base URLs with trailing slashes ([`32844c7`](https://github.com/python-gitlab/python-gitlab/commit/32844c7b27351b08bb86d8f9bd8fe9cf83917a5a))

* test: remove duplicate resp_get_project ([`cb43695`](https://github.com/python-gitlab/python-gitlab/commit/cb436951b1fde9c010e966819c75d0d7adacf17d))

* test: use lazy object in unit tests ([`31c6562`](https://github.com/python-gitlab/python-gitlab/commit/31c65621ff592dda0ad3bf854db906beb8a48e9a))

* test: add unit tests for revert commit API ([`d7a3066`](https://github.com/python-gitlab/python-gitlab/commit/d7a3066e03164af7f441397eac9e8cfef17c8e0c))

### Unknown

* Merge pull request #1039 from python-gitlab/fix/set-approvers

Fix/set approvers ([`481bd4f`](https://github.com/python-gitlab/python-gitlab/commit/481bd4f70e89b4fffb35a009e5532a2cec89607a))

* Merge pull request #1038 from nejch/fix/allow-empty-create-data

Fix: do not require empty data dict for create() ([`ca37d23`](https://github.com/python-gitlab/python-gitlab/commit/ca37d23fd3d5a9ab19f5aeb2000ac32c503caeb1))

* Merge pull request #1034 from filipowm/feat/api-oauth-applications

feat(api): add support for GitLab OAuth Applications using Applications API ([`e5afb55`](https://github.com/python-gitlab/python-gitlab/commit/e5afb554bf4bcc28555bde4030f50558f175a53b))

* Merge pull request #1032 from nejch/docs/requests-ca-bundle

docs: add reference to REQUESTS_CA_BUNDLE usage ([`fbcc820`](https://github.com/python-gitlab/python-gitlab/commit/fbcc8204a7f69405ec9a9a32b1e26256c7831e10))

* Merge pull request #1003 from python-gitlab/feat/all-keyset-pagination

feat: use keyset pagination by default for `all=True` ([`3aa9873`](https://github.com/python-gitlab/python-gitlab/commit/3aa9873c8e5f38c85f7ac4dd11a21728e553399b))

* Merge pull request #1022 from nejch/chore/ensure-latest-image

chore: ensure developers use same gitlab image as CI ([`745bdf7`](https://github.com/python-gitlab/python-gitlab/commit/745bdf7caeffa907bb0594b602194f41d3a75e3e))

* Merge pull request #1023 from nejch/perf/wait-gitlab-reconfigure

perf: wait for gitlab to reconfigure instead of using hardcoded sleep ([`2b3871d`](https://github.com/python-gitlab/python-gitlab/commit/2b3871d85e0f875edacc8eea5542df4d1f4c66f0))

* Merge pull request #1026 from nejch/feat/user-memberships

feat: add support for user memberships API (#1009) ([`f071390`](https://github.com/python-gitlab/python-gitlab/commit/f071390dadc4422c7d3cf77171334a617cfd9908))

* Merge pull request #1027 from nejch/fix/base-url-trailing-slash

Fix: remove trailing slash in base URL ([`292dfff`](https://github.com/python-gitlab/python-gitlab/commit/292dfff5050515d07b2e4f2231e2ec17dc2d5589))

* Merge pull request #1020 from nejch/feat/revert-commit-api

feat: add support for commit revert API (#991) ([`e8f0921`](https://github.com/python-gitlab/python-gitlab/commit/e8f0921d164c4b7db78e2f62e75eb32094b4456e))

* Merge pull request #1005 from charlesfayal/fix_set_approvers

change path for set_approvers to new api, with defaulted rule_type an… ([`19242c3`](https://github.com/python-gitlab/python-gitlab/commit/19242c398b9074e04e35cc687c31c543a10db280))

* Merge pull request #1008 from filipowm/feature/feature-flags-additional-config

Add capability to control GitLab features per project or group ([`066fc9b`](https://github.com/python-gitlab/python-gitlab/commit/066fc9bfdc1d8e6295cb924ea8471268ee869a90))

## v2.0.1 (2020-02-05)

### Chore

* chore: revert to 2.0.1

I&#39;ve misread the tag ([`272db26`](https://github.com/python-gitlab/python-gitlab/commit/272db2655d80fb81fbe1d8c56f241fe9f31b47e0))

* chore: bump to 2.1.0

There are a few more features in there ([`a6c0660`](https://github.com/python-gitlab/python-gitlab/commit/a6c06609123a9f4cba1a8605b9c849e4acd69809))

* chore: bump version to 2.0.1 ([`8287a0d`](https://github.com/python-gitlab/python-gitlab/commit/8287a0d993a63501fc859702fc8079a462daa1bb))

* chore(user): update user attributes

This also workarounds an GitLab issue, where private_profile, would reset to false if not supplied ([`27375f6`](https://github.com/python-gitlab/python-gitlab/commit/27375f6913547cc6e00084e5e77b0ad912b89910))

### Documentation

* docs(auth): remove email/password auth ([`c9329bb`](https://github.com/python-gitlab/python-gitlab/commit/c9329bbf028c5e5ce175e99859c9e842ab8234bc))

### Unknown

* Merge pull request #1007 from python-gitlab/chore/user-update

chore(user): update user attributes ([`f6d9858`](https://github.com/python-gitlab/python-gitlab/commit/f6d9858ab5c75a6c394db7e0978754fa48334353))

* Merge pull request #1000 from matusf/update-auth-docs

Update auth docs ([`7843ace`](https://github.com/python-gitlab/python-gitlab/commit/7843ace913589cf629f448a2541f290a4c7214cd))

## v2.0.0 (2020-01-26)

### Chore

* chore: build_sphinx needs sphinx &gt;= 1.7.6

Stepping thru Sphinx versions from 1.6.5 to 1.7.5 build_sphinx fails.  Once Sphinx == 1.7.6 build_sphinx finished. ([`528dfab`](https://github.com/python-gitlab/python-gitlab/commit/528dfab211936ee7794f9227311f04656a4d5252))

* chore: enforce python version requirements ([`70176db`](https://github.com/python-gitlab/python-gitlab/commit/70176dbbb96a56ee7891885553eb13110197494c))

* chore: bump to 2.0.0

Dropping support for legacy python requires a new major version ([`c817dcc`](https://github.com/python-gitlab/python-gitlab/commit/c817dccde8c104dcb294bbf1590c7e3ae9539466))

* chore: drop legacy python tests

Support dropped for: 2.7, 3.4, 3.5 ([`af8679a`](https://github.com/python-gitlab/python-gitlab/commit/af8679ac5c2c2b7774d624bdb1981d0e2374edc1))

* chore: add PyYaml as extra require ([`7ecd518`](https://github.com/python-gitlab/python-gitlab/commit/7ecd5184e62bf1b1f377db161b26fa4580af6b4c))

* chore: bump minimum required requests version

for security reasons ([`3f78aa3`](https://github.com/python-gitlab/python-gitlab/commit/3f78aa3c0d3fc502f295986d4951cfd0eee80786))

### Documentation

* docs: fix snippet get in project ([`3a4ff2f`](https://github.com/python-gitlab/python-gitlab/commit/3a4ff2fbf51d5f7851db02de6d8f0e84508b11a0))

* docs(projects): add raw file download docs

Fixes #969 ([`939e9d3`](https://github.com/python-gitlab/python-gitlab/commit/939e9d32e6e249e2a642d2bf3c1a34fde288c842))

### Feature

* feat: add global order_by option to ease pagination ([`d187925`](https://github.com/python-gitlab/python-gitlab/commit/d1879253dae93e182710fe22b0a6452296e2b532))

* feat: support keyset pagination globally ([`0b71ba4`](https://github.com/python-gitlab/python-gitlab/commit/0b71ba4d2965658389b705c1bb0d83d1ff2ee8f2))

* feat: add appearance API ([`4c4ac5c`](https://github.com/python-gitlab/python-gitlab/commit/4c4ac5ca1e5cabc4ea4b12734a7b091bc4c224b5))

* feat: add autocompletion support ([`973cb8b`](https://github.com/python-gitlab/python-gitlab/commit/973cb8b962e13280bcc8473905227cf351661bf0))

### Fix

* fix(projects): adjust snippets to match the API ([`e104e21`](https://github.com/python-gitlab/python-gitlab/commit/e104e213b16ca702f33962d770784f045f36cf10))

### Refactor

* refactor: support new list filters

This is most likely only useful for the CLI ([`bded2de`](https://github.com/python-gitlab/python-gitlab/commit/bded2de51951902444bc62aa016a3ad34aab799e))

* refactor: remove six dependency ([`9fb4645`](https://github.com/python-gitlab/python-gitlab/commit/9fb46454c6dab1a86ab4492df2368ed74badf7d6))

### Test

* test: adjust functional tests for project snippets ([`ac0ea91`](https://github.com/python-gitlab/python-gitlab/commit/ac0ea91f22b08590f85a2b0ffc17cd41ae6e0ff7))

* test: add project snippet tests ([`0952c55`](https://github.com/python-gitlab/python-gitlab/commit/0952c55a316fc8f68854badd68b4fc57658af9e7))

### Unknown

* Merge pull request #1001 from python-gitlab/feat/keyset-pagination

Feat/keyset pagination ([`df485a9`](https://github.com/python-gitlab/python-gitlab/commit/df485a92b713a0f2f983c72d9d41ea3a771abf88))

* Merge pull request #996 from python-gitlab/feat/appearance

feat: add appearance API ([`7fd3226`](https://github.com/python-gitlab/python-gitlab/commit/7fd3226fc6b629d503bc1b0a657bc21f69bc4696))

* Merge pull request #988 from jgroom33/patch-3

docs: fix snippet get in project ([`afdc43f`](https://github.com/python-gitlab/python-gitlab/commit/afdc43f401e20550ed181d4b87829739791d2ee3))

* Merge pull request #984 from derekschrock/patch-1

chore: build_sphinx needs sphinx &gt;= 1.7.6 ([`fc2ed13`](https://github.com/python-gitlab/python-gitlab/commit/fc2ed136c10920c5c0ef11247d0287b12e2a25ed))

* Merge pull request #982 from python-gitlab/chore/version-requirements

chore: enforce python version requirements ([`83fcd1b`](https://github.com/python-gitlab/python-gitlab/commit/83fcd1b189ea9acfec79a4b3b3290958007a58e7))

* Merge pull request #980 from python-gitlab/refactor/cleanup-upgrade

Refactor/cleanup upgrade ([`5fa0e16`](https://github.com/python-gitlab/python-gitlab/commit/5fa0e162f561451f7fa487dc4a4ff265c1d37f79))

* Merge pull request #979 from python-gitlab/fix/project-snippets

Fix/project snippets ([`5a10eb3`](https://github.com/python-gitlab/python-gitlab/commit/5a10eb3af52a8619d446616196dd3c0c3b91c395))

* Merge pull request #941 from mchlumsky/feat/autocompletion

feat: add autocompletion support ([`ec6e04c`](https://github.com/python-gitlab/python-gitlab/commit/ec6e04c16a8509519387b985a3ceef89d51a200b))

## v1.15.0 (2019-12-16)

### Chore

* chore: bump version to 1.15.0 ([`2a01326`](https://github.com/python-gitlab/python-gitlab/commit/2a01326e8e02bbf418b3f4c49ffa60c735b107dc))

* chore(ci): use correct crane ci ([`18913dd`](https://github.com/python-gitlab/python-gitlab/commit/18913ddce18f78e7432f4d041ab4bd071e57b256))

### Documentation

* docs(projects): fix file deletion docs

The function `file.delete()` requires `branch` argument in addition to `commit_message`. ([`1c4f1c4`](https://github.com/python-gitlab/python-gitlab/commit/1c4f1c40185265ae73c52c6d6c418e02ab33204e))

* docs: added docs for statistics ([`8c84cbf`](https://github.com/python-gitlab/python-gitlab/commit/8c84cbf6374e466f21d175206836672b3dadde20))

### Feature

* feat: allow cfg timeout to be overrided via kwargs

On startup, the `timeout` parameter is loaded from config and stored on
the base gitlab object instance. This instance parameter is used as the
timeout for all API requests (it&#39;s passed into the `session` object when
making HTTP calls).

This change allows any API method to specify a `timeout` argument to
`**kwargs` that will override the global timeout value. This was
somewhat needed / helpful for the `import_github` method.

I have also updated the docs accordingly. ([`e9a8289`](https://github.com/python-gitlab/python-gitlab/commit/e9a8289a381ebde7c57aa2364258d84b4771d276))

* feat: add support for /import/github

Addresses python-gitlab/python-gitlab#952

This adds a method to the `ProjectManager` called `import_github`, which
maps to the `/import/github` API endpoint. Calling `import_github` will
trigger an import operation from &lt;repo_id&gt; into &lt;target_namespace&gt;,
using &lt;personal_access_token&gt; to authenticate against github. In
practice a gitlab server may take many 10&#39;s of seconds to respond to
this API call, so we also take the liberty of increasing the default
timeout (only for this method invocation).

Unfortunately since `import` is a protected keyword in python, I was unable
to follow the endpoint structure with the manager namespace. I&#39;m open to
suggestions on a more sensible interface.

I&#39;m successfully using this addition to batch-import hundreds of github
repositories into gitlab. ([`aa4d41b`](https://github.com/python-gitlab/python-gitlab/commit/aa4d41b70b2a66c3de5a7dd19b0f7c151f906630))

* feat: nicer stacktrace ([`697cda2`](https://github.com/python-gitlab/python-gitlab/commit/697cda241509dd76adc1249b8029366cfc1d9d6e))

* feat: add variable_type/protected to projects ci variables

This adds the ci variables types and protected flag for create/update 
requests.

See 
https://docs.gitlab.com/ee/api/project_level_variables.html#create-variable ([`4724c50`](https://github.com/python-gitlab/python-gitlab/commit/4724c50e9ec0310432c70f07079b1e03ab3cc666))

* feat: add variable_type to groups ci variables

This adds the ci variables types for create/update requests.

See 
https://docs.gitlab.com/ee/api/group_level_variables.html#create-variable ([`0986c93`](https://github.com/python-gitlab/python-gitlab/commit/0986c93177cde1f3be77d4f73314c37b14bba011))

* feat: access project&#39;s issues statistics

Fixes #966 ([`482e57b`](https://github.com/python-gitlab/python-gitlab/commit/482e57ba716c21cd7b315e5803ecb3953c479b33))

* feat: adding project stats

Fixes #967 ([`db0b00a`](https://github.com/python-gitlab/python-gitlab/commit/db0b00a905c14d52eaca831fcc9243f33d2f092d))

* feat: retry transient HTTP errors

Fixes #970 ([`59fe271`](https://github.com/python-gitlab/python-gitlab/commit/59fe2714741133989a7beed613f1eeb67c18c54e))

### Fix

* fix: ignore all parameter, when as_list=True

Closes #962 ([`137d72b`](https://github.com/python-gitlab/python-gitlab/commit/137d72b3bc00588f68ca13118642ecb5cd69e6ac))

### Style

* style: format with the latest black version ([`06a8050`](https://github.com/python-gitlab/python-gitlab/commit/06a8050571918f0780da4c7d6ae514541118cf1a))

### Test

* test: added tests for statistics ([`8760efc`](https://github.com/python-gitlab/python-gitlab/commit/8760efc89bac394b01218b48dd3fcbef30c8b9a2))

* test: test that all is ignored, when as_list=False ([`b5e88f3`](https://github.com/python-gitlab/python-gitlab/commit/b5e88f3e99e2b07e0bafe7de33a8899e97c3bb40))

### Unknown

* Merge pull request #959 from andrew-littlebits/feat/import-github

feat: add support for /import/github ([`97e1fca`](https://github.com/python-gitlab/python-gitlab/commit/97e1fcab30a274cecf4332233cbf420d752143e0))

* Merge pull request #973 from mitar/patch-1

Nicer stacktrace ([`61eaad2`](https://github.com/python-gitlab/python-gitlab/commit/61eaad2ff32776c121eeb67202b0063a7b1cc2e1))

* Merge pull request #971 from jooola/ci_vars_type

feat: add more options for project/group ci variables manipulation ([`938fc0a`](https://github.com/python-gitlab/python-gitlab/commit/938fc0ae1eff7625d18cdf11fc019d83da02ba0c))

* Merge pull request #974 from python-gitlab/docs/file-deletion-docs

docs(projects): fix file deletion docs ([`59af4e4`](https://github.com/python-gitlab/python-gitlab/commit/59af4e434a669cd8c7dd8b8cb9aa0155aef45ca9))

* Merge pull request #968 from mitar/stats

Stats ([`62b0b62`](https://github.com/python-gitlab/python-gitlab/commit/62b0b624695593a65c9fb1fe18f8fc108ed7c4f7))

* Merge pull request #972 from mitar/http-retry

Retry transient HTTP errors ([`36bbd37`](https://github.com/python-gitlab/python-gitlab/commit/36bbd37e6a79c6fd5e9b4d64119eda7812364387))

* Merge pull request #963 from python-gitlab/fix/as_list

Fix/as list ([`3e2d694`](https://github.com/python-gitlab/python-gitlab/commit/3e2d69417aa8c6b043ee99fea5f8d7e31a2ba3e8))

## v1.14.0 (2019-12-07)

### Chore

* chore: bump version to 1.14.0 ([`164fa4f`](https://github.com/python-gitlab/python-gitlab/commit/164fa4f360a1bb0ecf5616c32a2bc31c78c2594f))

* chore(ci): switch to crane docker image (#944) ([`e0066b6`](https://github.com/python-gitlab/python-gitlab/commit/e0066b6b7c5ce037635f6a803ea26707d5684ef5))

### Documentation

* docs(readme): fix Docker image reference

v1.8.0 is not available.
```
Unable to find image &#39;registry.gitlab.com/python-gitlab/python-gitlab:v1.8.0&#39; locally
docker: Error response from daemon: manifest for registry.gitlab.com/python-gitlab/python-gitlab:v1.8.0 not found: manifest unknown: manifest unknown.
``` ([`b9a40d8`](https://github.com/python-gitlab/python-gitlab/commit/b9a40d822bcff630a4c92c395c134f8c002ed1cb))

* docs(snippets): fix snippet docs

Fixes #954 ([`bbaa754`](https://github.com/python-gitlab/python-gitlab/commit/bbaa754673c4a0bffece482fe33e4875ddadc2dc))

* docs: fix typo ([`d9871b1`](https://github.com/python-gitlab/python-gitlab/commit/d9871b148c7729c9e401f43ff6293a5e65ce1838))

* docs: add project and group cluster examples ([`d15801d`](https://github.com/python-gitlab/python-gitlab/commit/d15801d7e7742a43ad9517f0ac13b6dba24c6283))

* docs(changelog): add notice for release-notes on Github (#938) ([`de98e57`](https://github.com/python-gitlab/python-gitlab/commit/de98e572b003ee4cf2c1ef770a692f442c216247))

* docs(pipelines_and_jobs): add pipeline custom variables usage example ([`b275eb0`](https://github.com/python-gitlab/python-gitlab/commit/b275eb03c5954ca24f249efad8125d1eacadd3ac))

### Feature

* feat: add audit endpoint ([`2534020`](https://github.com/python-gitlab/python-gitlab/commit/2534020b1832f28339ef466d6dd3edc21a521260))

* feat: add project and group clusters ([`ebd053e`](https://github.com/python-gitlab/python-gitlab/commit/ebd053e7bb695124c8117a95eab0072db185ddf9))

* feat: add support for include_subgroups filter ([`adbcd83`](https://github.com/python-gitlab/python-gitlab/commit/adbcd83fa172af2f3929ba063a0e780395b102d8))

### Fix

* fix(project-fork): copy create fix from ProjectPipelineManager ([`516307f`](https://github.com/python-gitlab/python-gitlab/commit/516307f1cc9e140c7d85d0ed0c419679b314f80b))

* fix(project-fork): correct path computation for project-fork list ([`44a7c27`](https://github.com/python-gitlab/python-gitlab/commit/44a7c2788dd19c1fe73d7449bd7e1370816fd36d))

* fix(labels): ensure label.save() works

Otherwise, we get:
   File &#34;gitlabracadabra/mixins/labels.py&#34;, line 67, in _process_labels
     current_label.save()
   File &#34;gitlab/exceptions.py&#34;, line 267, in wrapped_f
     return f(*args, **kwargs)
   File &#34;gitlab/v4/objects.py&#34;, line 896, in save
     self._update_attrs(server_data)
   File &#34;gitlab/base.py&#34;, line 131, in _update_attrs
     self.__dict__[&#34;_attrs&#34;].update(new_attrs)
 TypeError: &#39;NoneType&#39; object is not iterable

Because server_data is None. ([`727f536`](https://github.com/python-gitlab/python-gitlab/commit/727f53619dba47f0ab770e4e06f1cb774e14f819))

* fix: added missing attributes for project approvals

Reference: https://docs.gitlab.com/ee/api/merge_request_approvals.html#change-configuration

Missing attributes:
* merge_requests_author_approval
* merge_requests_disable_committers_approval ([`460ed63`](https://github.com/python-gitlab/python-gitlab/commit/460ed63c3dc4f966d6aae1415fdad6de125c6327))

### Unknown

* Merge pull request #949 from idanbensha/add_audit_events

feat: add audit endpoint ([`98e1b0a`](https://github.com/python-gitlab/python-gitlab/commit/98e1b0ae77a627d21ce971ee4df813e1955f69a0))

* Merge pull request #958 from vvv/fix-docker-ref

README.rst: fix the upstream Docker image reference ([`f6f5178`](https://github.com/python-gitlab/python-gitlab/commit/f6f5178c1dc7aeb3fdbee19b1768e30b2be4f4f4))

* Merge pull request #955 from python-gitlab/fix/snippet-docs

docs(snippets): fix snippet docs ([`9961aaa`](https://github.com/python-gitlab/python-gitlab/commit/9961aaa1508e08a567c8c66cb194385788b8113e))

* Merge pull request #953 from bmwiedemann/master

Fix doc typo ([`267a9a1`](https://github.com/python-gitlab/python-gitlab/commit/267a9a151ba9f2338f50fbb118513807ebce9704))

* Merge pull request #947 from lundbird/master

docs: add project and group cluster examples ([`e4cad49`](https://github.com/python-gitlab/python-gitlab/commit/e4cad490b9cd16aa20ea84bb4bd24a6d25b19411))

* Merge pull request #946 from lundbird/master

feat: add project and group clusters ([`da557c9`](https://github.com/python-gitlab/python-gitlab/commit/da557c931fa6c6d50c373fc022d88acf1431c24a))

* Merge pull request #943 from choyrim/942-project-fork-list-404

#942: fix up path computation for project-fork list ([`ecad2c8`](https://github.com/python-gitlab/python-gitlab/commit/ecad2c83635c5e5f7003f61502391446ebc631c9))

* Merge pull request #937 from sathieu/fix_labels_save

fix(labels): ensure label.save() works ([`c937338`](https://github.com/python-gitlab/python-gitlab/commit/c937338b0119b08b358f97b4716c56777ee7bb80))

* Merge pull request #934 from tymonx/fix-missing-attribute-for-project-approvals

Added missing attributes for project approvals ([`9608886`](https://github.com/python-gitlab/python-gitlab/commit/960888628617beae75392dcdcb6ef5a66abd976d))

* Merge pull request #929 from SVLay/docs/pipeline-variables

docs(pipelines_and_jobs): add pipeline custom variables usage example ([`4efa6e6`](https://github.com/python-gitlab/python-gitlab/commit/4efa6e6e5b9b57a3c4eda9ef20a4194b384055dc))

* Merge pull request #932 from ConorNevin/master

Add support for include_subgroups filter ([`1f18230`](https://github.com/python-gitlab/python-gitlab/commit/1f182302c206502f5202d1707fef69adf527fea7))

## v1.13.0 (2019-11-02)

### Chore

* chore: bump version to 1.13.0 ([`d0750bc`](https://github.com/python-gitlab/python-gitlab/commit/d0750bc01ed12952a4d259a13b3917fa404fd435))

* chore(setup): we support 3.8 (#924)

* chore(setup): we support 3.8

* style: format with black ([`6048175`](https://github.com/python-gitlab/python-gitlab/commit/6048175ef2c21fda298754e9b07515b0a56d66bd))

* chore(ci): update latest docker image for every tag ([`01cbc7a`](https://github.com/python-gitlab/python-gitlab/commit/01cbc7ad04a875bea93a08c0ce563ab5b4fe896b))

* chore(dist): add test data

Closes #907 ([`3133ed7`](https://github.com/python-gitlab/python-gitlab/commit/3133ed7d1df6f49de380b35331bbcc67b585a61b))

### Documentation

* docs: projects get requires id

Also, add an example value for project_id to the other projects.get()
example. ([`5bd8947`](https://github.com/python-gitlab/python-gitlab/commit/5bd8947bd16398aed218f07458aef72e67f2d130))

* docs(project): fix group project example

GroupManager.search is removed since 9a66d78, use list(search=&#39;keyword&#39;) instead ([`e680943`](https://github.com/python-gitlab/python-gitlab/commit/e68094317ff6905049e464a59731fe4ab23521de))

### Feature

* feat: add users activate, deactivate functionality

These were introduced in GitLab 12.4 ([`32ad669`](https://github.com/python-gitlab/python-gitlab/commit/32ad66921e408f6553b9d60b6b4833ed3180f549))

* feat: send python-gitlab version as user-agent ([`c22d49d`](https://github.com/python-gitlab/python-gitlab/commit/c22d49d084d1e03426cfab0d394330f8ab4bd85a))

* feat: add deployment creation

Added in GitLab 12.4

Fixes #917 ([`ca256a0`](https://github.com/python-gitlab/python-gitlab/commit/ca256a07a2cdaf77a5c20e307d334b82fd0fe861))

* feat(test): unused unittest2, type -&gt; isinstance ([`33b1801`](https://github.com/python-gitlab/python-gitlab/commit/33b180120f30515d0f76fcf635cb8c76045b1b42))

* feat(auth): remove deprecated session auth ([`b751cdf`](https://github.com/python-gitlab/python-gitlab/commit/b751cdf424454d3859f3f038b58212e441faafaf))

* feat(doc): remove refs to api v3 in docs ([`6beeaa9`](https://github.com/python-gitlab/python-gitlab/commit/6beeaa993f8931d6b7fe682f1afed2bd4c8a4b73))

### Fix

* fix(projects): support `approval_rules` endpoint for projects

The `approvers` API endpoint is deprecated [1]. GitLab instead uses
the `approval_rules` API endpoint to modify approval settings for
merge requests. This adds the functionality for project-level
merge request approval settings.

Note that there does not exist an endpoint to &#39;get&#39; a single
approval rule at this moment - only &#39;list&#39;.

[1] https://docs.gitlab.com/ee/api/merge_request_approvals.html ([`2cef2bb`](https://github.com/python-gitlab/python-gitlab/commit/2cef2bb40b1f37b97bb2ee9894ab3b9970cef231))

### Test

* test(projects): support `approval_rules` endpoint for projects ([`94bac44`](https://github.com/python-gitlab/python-gitlab/commit/94bac4494353e4f597df0251f0547513c011e6de))

* test: remove warning about open files from test_todo()

When running unittests python warns that the json file from test_todo()
was still open. Use with to open, read, and create encoded json data
that is used by resp_get_todo(). ([`d6419aa`](https://github.com/python-gitlab/python-gitlab/commit/d6419aa86d6ad385e15d685bf47242bb6c67653e))

### Unknown

* Merge pull request #931 from python-gitlab/choree/1-13-0

chore: bump version to 1.13.0 ([`f39c68f`](https://github.com/python-gitlab/python-gitlab/commit/f39c68fd0b180ba72dd11e3cbad932d16d4bb484))

* Merge pull request #919 from appian/project-approval-rules

fix(projects): support `approval_rules` endpoint for projects ([`fddc25a`](https://github.com/python-gitlab/python-gitlab/commit/fddc25adac16a74f61d81871f9ae13c0227d92d6))

* Merge pull request #923 from python-gitlab/feat/users-activate-deactivate

feat: add users activate, deactivate functionality ([`912e16b`](https://github.com/python-gitlab/python-gitlab/commit/912e16b95611715b4df3fae019687f7616af51c1))

* Merge pull request #922 from python-gitlab/chore/latest-docker-image

chore(ci): update latest docker image for every tag ([`ac2266b`](https://github.com/python-gitlab/python-gitlab/commit/ac2266b66553cec11740bd5246e23d649606b5ef))

* Merge pull request #921 from python-gitlab/feat/python-gitlab-agent

feat: send python-gitlab version as user-agent ([`8cb5488`](https://github.com/python-gitlab/python-gitlab/commit/8cb5488142ca7fc7563fac65b434b672a14369fc))

* Merge pull request #920 from python-gitlab/feat/deployment-create

feat: add deployment creation ([`dad6805`](https://github.com/python-gitlab/python-gitlab/commit/dad68050c1269519f35dcdb29dc94a03f47532c5))

* Merge pull request #916 from python-gitlab/chore/add-test-to-dist

chore(dist): add test data ([`e790b1e`](https://github.com/python-gitlab/python-gitlab/commit/e790b1ec40ed690152776a87c15e7f7d5d3b9136))

* Merge pull request #914 from terminalmage/issue913

Remove inaccurate projects.get() example ([`d2c9cee`](https://github.com/python-gitlab/python-gitlab/commit/d2c9ceece5d6473f286e00963252abbcf1a2a17c))

* Merge pull request #911 from xdavidwu/fix-project-doc

docs(project): fix group project example ([`d853a76`](https://github.com/python-gitlab/python-gitlab/commit/d853a767ac8835615e0fded3087f55ca8594c1ed))

* Merge pull request #906 from jouve/test-cleanup

unused unittest2, type -&gt; isinstance ([`42a1ba6`](https://github.com/python-gitlab/python-gitlab/commit/42a1ba6be175a9838c589cb1e40636b3910db505))

* Merge pull request #904 from jouve/remove-cred-auth

remove deprecated session auth ([`67a9c1f`](https://github.com/python-gitlab/python-gitlab/commit/67a9c1f1c62393b02919d25bcc98c3683d92576a))

* Merge pull request #908 from derekschrock/todo-units-test

Remove warning about open files from test_todo() ([`ff808ee`](https://github.com/python-gitlab/python-gitlab/commit/ff808ee94a73d65802a21ff1350090885d4befd5))

* Merge pull request #905 from jouve/doc-v3

remove references to api v3 in docs ([`92ba028`](https://github.com/python-gitlab/python-gitlab/commit/92ba0283b63e562e181061252787e0e46da83a29))

## v1.12.1 (2019-10-07)

### Fix

* fix: fix not working without auth ([`03b7b5b`](https://github.com/python-gitlab/python-gitlab/commit/03b7b5b07e1fd2872e8968dd6c29bc3161c6c43a))

### Unknown

* Merge pull request #901 from python-gitlab/fix/non-auth

fix: fix not working without auth ([`f4b2927`](https://github.com/python-gitlab/python-gitlab/commit/f4b29278771e48320e2da4bacc4544d263d1754c))

## v1.12.0 (2019-10-06)

### Chore

* chore: bump to 1.12.0 ([`4648128`](https://github.com/python-gitlab/python-gitlab/commit/46481283a9985ae1b07fe686ec4a34e4a1219b66))

* chore(ci): build test images on tag ([`0256c67`](https://github.com/python-gitlab/python-gitlab/commit/0256c678ea9593c6371ffff60663f83c423ca872))

### Documentation

* docs(project): add submodule docs ([`b5969a2`](https://github.com/python-gitlab/python-gitlab/commit/b5969a2dcea77fa608cc29be7a5f39062edd3846))

* docs(projects): add note about project list

Fixes #795 ([`44407c0`](https://github.com/python-gitlab/python-gitlab/commit/44407c0f59b9602b17cfb93b5e1fa37a84064766))

* docs(repository-tags): fix typo

Closes #879 ([`3024c5d`](https://github.com/python-gitlab/python-gitlab/commit/3024c5dc8794382e281b83a8266be7061069e83e))

* docs(todo): correct todo docs ([`d64edcb`](https://github.com/python-gitlab/python-gitlab/commit/d64edcb4851ea62e72e3808daf7d9b4fdaaf548b))

### Feature

* feat(project): implement update_submodule ([`4d1e377`](https://github.com/python-gitlab/python-gitlab/commit/4d1e3774706f336e87ebe70e1b373ddb37f34b45))

* feat(ci): improve functionnal tests ([`eefceac`](https://github.com/python-gitlab/python-gitlab/commit/eefceace2c2094ef41d3da2bf3c46a58a450dcba))

* feat(project): add file blame api

https://docs.gitlab.com/ee/api/repository_files.html#get-file-blame-from-repository ([`f5b4a11`](https://github.com/python-gitlab/python-gitlab/commit/f5b4a113a298d33cb72f80c94d85bdfec3c4e149))

* feat: add support for job token

See https://docs.gitlab.com/ee/api/jobs.html#get-job-artifacts for usage ([`cef3aa5`](https://github.com/python-gitlab/python-gitlab/commit/cef3aa51a6928338c6755c3e6de78605fae8e59e))

* feat(user): add status api ([`62c9fe6`](https://github.com/python-gitlab/python-gitlab/commit/62c9fe63a47ddde2792a4a5e9cd1c7aa48661492))

### Fix

* fix(cli): fix cli command user-project list ([`c17d7ce`](https://github.com/python-gitlab/python-gitlab/commit/c17d7ce14f79c21037808894d8c7ba1117779130))

* fix(labels): don&#39;t mangle label name on update ([`1fb6f73`](https://github.com/python-gitlab/python-gitlab/commit/1fb6f73f4d501c2b6c86c863d40481e1d7a707fe))

* fix(todo): mark_all_as_done doesn&#39;t return anything ([`5066e68`](https://github.com/python-gitlab/python-gitlab/commit/5066e68b398039beb5e1966ba1ed7684d97a8f74))

### Refactor

* refactor: remove obsolete test image

Follow up of #896 ([`a14c02e`](https://github.com/python-gitlab/python-gitlab/commit/a14c02ef85bd4d273b8c7f0f6bd07680c91955fa))

* refactor: remove unused code, simplify string format ([`c7ff676`](https://github.com/python-gitlab/python-gitlab/commit/c7ff676c11303a00da3a570bf2893717d0391f20))

### Style

* style: format with black ([`fef085d`](https://github.com/python-gitlab/python-gitlab/commit/fef085dca35d6b60013d53a3723b4cbf121ab2ae))

### Test

* test(submodules): correct test method ([`e59356f`](https://github.com/python-gitlab/python-gitlab/commit/e59356f6f90d5b01abbe54153441b6093834aa11))

* test(func): disable commit test

GitLab seems to be randomly failing here ([`c9c76a2`](https://github.com/python-gitlab/python-gitlab/commit/c9c76a257d2ed3b394f499253d890c2dd9a01e24))

* test(todo): add unittests ([`7715567`](https://github.com/python-gitlab/python-gitlab/commit/77155678a5d8dbbf11d00f3586307694042d3227))

* test(status): add user status test ([`fec4f9c`](https://github.com/python-gitlab/python-gitlab/commit/fec4f9c23b8ba33bb49dca05d9c3e45cb727e0af))

* test: re-enabled py_func_v4 test ([`49d84ba`](https://github.com/python-gitlab/python-gitlab/commit/49d84ba7e95fa343e622505380b3080279b83f00))

### Unknown

* Merge pull request #899 from python-gitlab/chore/package-version

chore: bump to 1.12.0 ([`35cc8c7`](https://github.com/python-gitlab/python-gitlab/commit/35cc8c789fda4977add7f399bf426352b1aa246f))

* Merge pull request #898 from python-gitlab/feat/update_submodule

Feat/update submodule ([`6f4332d`](https://github.com/python-gitlab/python-gitlab/commit/6f4332db37b0a609ec4bd5e2c0b7ffc01717599c))

* Merge pull request #897 from python-gitlab/refactor/remove-obsolete-image

refactor: remove obsolete test image ([`fcea41c`](https://github.com/python-gitlab/python-gitlab/commit/fcea41c61f7776cf57ed5001facbc1e77d2834c4))

* Merge pull request #892 from godaji/remove-unused-code

Remove unused code and simplify string format. ([`214f7ef`](https://github.com/python-gitlab/python-gitlab/commit/214f7ef5f3b6e99b7756982c5b883e40d3b22657))

* Merge pull request #896 from jouve/fix-functionnal-test

improve functionnal tests ([`d7d2260`](https://github.com/python-gitlab/python-gitlab/commit/d7d2260945994a9e73fe3f7f9328f3ec9d9c54d4))

* Merge pull request #894 from minitux/master

feat (project): add file blame api ([`082a624`](https://github.com/python-gitlab/python-gitlab/commit/082a62456deaa68274ed1c44a744c79c5356a622))

* Merge pull request #891 from python-gitlab/docs/project-note-list

docs(projects): add note about project list ([`ba2b60e`](https://github.com/python-gitlab/python-gitlab/commit/ba2b60e32c12cacf18762a286d05e073529b9898))

* Merge pull request #886 from LuckySB/cli_user_project

fix cli command user-project list ([`88b1833`](https://github.com/python-gitlab/python-gitlab/commit/88b183376de5b8c986eac24955ef129ca4d781cc))

* Merge pull request #885 from sathieu/patch-1

Don&#39;t mangle label name on update ([`ff10726`](https://github.com/python-gitlab/python-gitlab/commit/ff10726d70a62d32ef39398a431def9656c93927))

* Merge pull request #880 from python-gitlab/docs/tags-fix-typo

docs(repository-tags): fix typo ([`c287bdd`](https://github.com/python-gitlab/python-gitlab/commit/c287bdd0889881d89f991d3929ae513d91b5894c))

* Merge pull request #878 from python-gitlab/test/todo-unit-test

Test/todo unit test ([`040894d`](https://github.com/python-gitlab/python-gitlab/commit/040894d245709c5c2524d59d2b228a21dd74d1a4))

* Merge pull request #876 from sathieu/job_token

Add support for job token ([`8474829`](https://github.com/python-gitlab/python-gitlab/commit/8474829a3fe40aca8f5d4c1c627908f0830a8f59))

* Merge pull request #875 from python-gitlab/feat/status-api

feat(user): add status api ([`b7f3342`](https://github.com/python-gitlab/python-gitlab/commit/b7f33429c75ed2f464ebd9b4d3c56d3479df3faa))

* Merge pull request #874 from python-gitlab/test/py-fun-test

test: re-enabled py_func_v4 test ([`1490b0e`](https://github.com/python-gitlab/python-gitlab/commit/1490b0e7f175d54cc6d35de7aac6d9e45c0e3d51))

## v1.11.0 (2019-08-31)

### Chore

* chore: bump package version ([`37542cd`](https://github.com/python-gitlab/python-gitlab/commit/37542cd28aa94ba01d5d289d950350ec856745af))

### Feature

* feat: add methods to retrieve an individual project environment ([`29de40e`](https://github.com/python-gitlab/python-gitlab/commit/29de40ee6a20382c293d8cdc8d831b52ad56a657))

* feat: group labels with subscriptable mixin ([`4a9ef9f`](https://github.com/python-gitlab/python-gitlab/commit/4a9ef9f0fa26e01fc6c97cf88b2a162e21f61cce))

### Fix

* fix(projects): avatar uploading for projects ([`558ace9`](https://github.com/python-gitlab/python-gitlab/commit/558ace9b007ff9917734619c05a7c66008a4c3f0))

* fix: remove empty list default arguments

Signed-off-by: Frantisek Lachman &lt;flachman@redhat.com&gt; ([`6e204ce`](https://github.com/python-gitlab/python-gitlab/commit/6e204ce819fc8bdd5359325ed7026a48d63f8103))

* fix: remove empty dict default arguments

Signed-off-by: Frantisek Lachman &lt;flachman@redhat.com&gt; ([`8fc8e35`](https://github.com/python-gitlab/python-gitlab/commit/8fc8e35c63d7ebd80408ae002693618ca16488a7))

* fix: add project and group label update without id to fix cli ([`a3d0d7c`](https://github.com/python-gitlab/python-gitlab/commit/a3d0d7c1e7b259a25d9dc84c0b1de5362c80abb8))

### Test

* test: add group label cli tests ([`f7f24bd`](https://github.com/python-gitlab/python-gitlab/commit/f7f24bd324eaf33aa3d1d5dd12719237e5bf9816))

### Unknown

* Merge pull request #865 from orf/retrieve-environment

feat: add methods to retrieve an individual project environment ([`0389e66`](https://github.com/python-gitlab/python-gitlab/commit/0389e664c0a04021b3df097bacad3940f158607f))

* Merge pull request #861 from ravanscafi/fix-project-avatar

Fix avatar uploading for projects ([`99a9415`](https://github.com/python-gitlab/python-gitlab/commit/99a941526a1845559d92b607fd9e2d86efb7e7b6))

* Merge pull request #860 from lachmanfrantisek/fix-mutable-default-arguments

Fix mutable default arguments ([`e8a3585`](https://github.com/python-gitlab/python-gitlab/commit/e8a3585ed0e7dfa2f64f6c3378a598120f5f8167))

* Merge pull request #847 from sidisel-albertolopez/feat/grouplabels

feat: Add grouplabel support with subscribable mixin ([`edb3359`](https://github.com/python-gitlab/python-gitlab/commit/edb3359fb3a77050d3e162da641445952397279b))

## v1.10.0 (2019-07-22)

### Chore

* chore: bump package version to 1.10.0 ([`c7c8470`](https://github.com/python-gitlab/python-gitlab/commit/c7c847056b6d24ba7a54b93837950b7fdff6c477))

* chore(setup): add 3.7 to supported python versions ([`b1525c9`](https://github.com/python-gitlab/python-gitlab/commit/b1525c9a4ca2d8c6c14d745638b3292a71763aeb))

* chore: move checks back to travis ([`b764525`](https://github.com/python-gitlab/python-gitlab/commit/b7645251a0d073ca413bba80e87884cc236e63f2))

* chore: disable failing travis test ([`515aa9a`](https://github.com/python-gitlab/python-gitlab/commit/515aa9ac2aba132d1dfde0418436ce163fca2313))

* chore(ci): rebuild test image, when something changed ([`2fff260`](https://github.com/python-gitlab/python-gitlab/commit/2fff260a8db69558f865dda56f413627bb70d861))

* chore(ci): update the GitLab version in the test image ([`c410699`](https://github.com/python-gitlab/python-gitlab/commit/c41069992de392747ccecf8c282ac0549932ccd1))

* chore(ci): add automatic GitLab image pushes ([`95c9b6d`](https://github.com/python-gitlab/python-gitlab/commit/95c9b6dd489fc15c7dfceffca909917f4f3d4312))

* chore(ci): fix gitlab PyPI publish ([`3e37df1`](https://github.com/python-gitlab/python-gitlab/commit/3e37df16e2b6a8f1beffc3a595abcb06fd48a17c))

* chore: add a tox job to run black

Allow lines to be 88 chars long for flake8. ([`c27fa48`](https://github.com/python-gitlab/python-gitlab/commit/c27fa486698e441ebc16448ee93e5539cb885ced))

* chore(ci): use reliable ci system ([`724a672`](https://github.com/python-gitlab/python-gitlab/commit/724a67211bc83d67deef856800af143f1dbd1e78))

* chore(ci): don&#39;t try to publish existing release ([`b4e818d`](https://github.com/python-gitlab/python-gitlab/commit/b4e818db7887ff1ec337aaf392b5719f3931bc61))

* chore: release tags to PyPI automatically

Fixes #609 ([`3133b48`](https://github.com/python-gitlab/python-gitlab/commit/3133b48a24ce3c9e2547bf2a679d73431dfbefab))

* chore(tests): add rate limit tests ([`e216f06`](https://github.com/python-gitlab/python-gitlab/commit/e216f06d4d25d37a67239e93a8e2e400552be396))

### Documentation

* docs(snippets): fix project-snippets layout

Fixes #828 ([`7feb97e`](https://github.com/python-gitlab/python-gitlab/commit/7feb97e9d89b4ef1401d141be3d00b9d0ff6b75c))

* docs(projects): add mention about project listings

Having exactly 20 internal and 5 private projects in the group
spent some time debugging this issue.

Hopefully that helped: https://github.com/python-gitlab/python-gitlab/issues/93

Imho should be definitely mention about `all=True` parameter. ([`f604b25`](https://github.com/python-gitlab/python-gitlab/commit/f604b2577b03a6a19641db3f2060f99d24cc7073))

* docs(readme): fix six url

six URL was pointing to 404 ([`0bc30f8`](https://github.com/python-gitlab/python-gitlab/commit/0bc30f840c9c30dd529ae85bdece6262d2702c94))

* docs: re-order api examples

`Pipelines and Jobs` and `Protected Branches` are out of order in contents and sometimes hard to find when looking for examples. ([`5d149a2`](https://github.com/python-gitlab/python-gitlab/commit/5d149a2262653b729f0105639ae5027ae5a109ea))

* docs: add pipeline deletion ([`2bb2571`](https://github.com/python-gitlab/python-gitlab/commit/2bb257182c237384d60b8d90cbbff5a0598f283b))

* docs(api-usage): fix project group example

Fixes #798 ([`40a1bf3`](https://github.com/python-gitlab/python-gitlab/commit/40a1bf36c2df89daa1634e81c0635c1a63831090))

* docs: remove v3 support ([`7927663`](https://github.com/python-gitlab/python-gitlab/commit/792766319f7c43004460fc9b975549be55430987))

* docs: Add an example of trigger token usage

Closes #752 ([`ea1eefe`](https://github.com/python-gitlab/python-gitlab/commit/ea1eefef2896420ae4e4d248155e4c5d33b4034e))

* docs(readme): add more info about commitlint, code-format ([`286f703`](https://github.com/python-gitlab/python-gitlab/commit/286f7031ed542c97fb8792f61012d7448bee2658))

* docs(readme): provide commit message guidelines

Fixes #660 ([`bed8e1b`](https://github.com/python-gitlab/python-gitlab/commit/bed8e1ba80c73b1d976ec865756b62e66342ce32))

* docs(setup): use proper readme on PyPI ([`6898097`](https://github.com/python-gitlab/python-gitlab/commit/6898097c45d53a3176882a3d9cb86c0015f8d491))

* docs(projects): fix typo in code sample

Fixes #630 ([`b93f2a9`](https://github.com/python-gitlab/python-gitlab/commit/b93f2a9ea9661521878ac45d70c7bd9a5a470548))

* docs(groups): fix typo

Fixes #635 ([`ac2d65a`](https://github.com/python-gitlab/python-gitlab/commit/ac2d65aacba5c19eca857290c5b47ead6bb4356d))

* docs(cli): add PyYAML requirement notice

Fixes #606 ([`d29a489`](https://github.com/python-gitlab/python-gitlab/commit/d29a48981b521bf31d6f0304b88f39a63185328a))

* docs(readme): add docs build information ([`6585c96`](https://github.com/python-gitlab/python-gitlab/commit/6585c967732fe2a53c6ad6d4d2ab39aaa68258b0))

* docs: add MR approvals in index ([`0b45afb`](https://github.com/python-gitlab/python-gitlab/commit/0b45afbeed13745a2f9d8a6ec7d09704a6ab44fb))

* docs(api-usage): add rate limit documentation ([`ad4de20`](https://github.com/python-gitlab/python-gitlab/commit/ad4de20fe3a2fba2d35d4204bf5b0b7f589d4188))

* docs(projects): fix typo ([`c6bcfe6`](https://github.com/python-gitlab/python-gitlab/commit/c6bcfe6d372af6557547a408a8b0a39b909f0cdf))

* docs: trigger_pipeline only accept branches and tags as ref

Fixes #430 ([`d63748a`](https://github.com/python-gitlab/python-gitlab/commit/d63748a41cc22bba93a9adf0812e7eb7b74a0161))

* docs: fix invalid Raise attribute in docstrings ([`95a3fe6`](https://github.com/python-gitlab/python-gitlab/commit/95a3fe6907676109e1cd2f52ca8f5ad17e0d01d0))

* docs: add missing = ([`391417c`](https://github.com/python-gitlab/python-gitlab/commit/391417cd47d722760dfdaab577e9f419c5dca0e0))

* docs: remove the build warning about _static ([`764d3ca`](https://github.com/python-gitlab/python-gitlab/commit/764d3ca0087f0536c48c9e1f60076af211138b9b))

* docs: fix &#34;required&#34; attribute ([`e64d0b9`](https://github.com/python-gitlab/python-gitlab/commit/e64d0b997776387f400eaec21c37ce6e58d49095))

* docs: add missing requiredCreateAttrs ([`b08d74a`](https://github.com/python-gitlab/python-gitlab/commit/b08d74ac3efb505961971edb998ce430e430d652))

* docs: add a note for python 3.5 for file content update

The data passed to the JSON serializer must be a string with python 3.
Document this in the exemples.

Fix #175 ([`ca014f8`](https://github.com/python-gitlab/python-gitlab/commit/ca014f8c3e4877a4cc1ae04e1302fb57d39f47c4))

* docs: improve the pagination section ([`29e2efe`](https://github.com/python-gitlab/python-gitlab/commit/29e2efeae22ce5fa82e3541360b234e0053a65c2))

* docs: notes API ([`3e026d2`](https://github.com/python-gitlab/python-gitlab/commit/3e026d2ee62eba3ad92ff2cdd53db19f5e0e9f6a))

* docs: snippets API ([`35b7f75`](https://github.com/python-gitlab/python-gitlab/commit/35b7f750c7e38a39cd4cb27195d9aa4807503b29))

* docs: tags API ([`dd79eda`](https://github.com/python-gitlab/python-gitlab/commit/dd79eda78f91fc7e1e9a08b1e70ef48e3b4bb06d))

* docs: system hooks API ([`5c51bf3`](https://github.com/python-gitlab/python-gitlab/commit/5c51bf3d49302afe4725575a83d81a8c9eeb8779))

* docs: add ApplicationSettings API ([`ab7d794`](https://github.com/python-gitlab/python-gitlab/commit/ab7d794251bcdbafce69b1bde0628cd3b710d784))

* docs: repository files API ([`f00340f`](https://github.com/python-gitlab/python-gitlab/commit/f00340f72935b6fd80df7b62b811644b63049b5a))

* docs: project repository API ([`71a2a4f`](https://github.com/python-gitlab/python-gitlab/commit/71a2a4fb84321e73418fda1ce4e4d47177af928c))

* docs: add milestones API ([`7411907`](https://github.com/python-gitlab/python-gitlab/commit/74119073dae18214df1dd67ded6cd57abda335d4))

* docs: add MR API ([`5614a7c`](https://github.com/python-gitlab/python-gitlab/commit/5614a7c9bf62aede3804469b6781f45d927508ea))

* docs: add licenses API ([`4540614`](https://github.com/python-gitlab/python-gitlab/commit/4540614a38067944c628505225bb15928d8e3c93))

* docs: add labales API ([`31882b8`](https://github.com/python-gitlab/python-gitlab/commit/31882b8a57f3f4c7e4c4c4b319af436795ebafd3))

* docs: add deploy keys API ([`ea089e0`](https://github.com/python-gitlab/python-gitlab/commit/ea089e092439a8fe95b50c3d0592358550389b51))

* docs: issues API ([`41cbc32`](https://github.com/python-gitlab/python-gitlab/commit/41cbc32621004aab2cae5f7c14fc60005ef7b966))

* docs: commits API ([`07c5594`](https://github.com/python-gitlab/python-gitlab/commit/07c55943eebb302bc1b8feaf482d929c83e9ebe1))

* docs: groups API documentation ([`4d871aa`](https://github.com/python-gitlab/python-gitlab/commit/4d871aadfaa9f57f5ae9f8b49f8367a5ef58545d))

* docs: Add builds-related API docs ([`8e6a944`](https://github.com/python-gitlab/python-gitlab/commit/8e6a9442324926ed1dec0a8bfaf77792e4bdb10f))

* docs: fork relationship API ([`21f48b3`](https://github.com/python-gitlab/python-gitlab/commit/21f48b357130720551d5cccbc62f5275fe970378))

* docs: project search API ([`e4cd04c`](https://github.com/python-gitlab/python-gitlab/commit/e4cd04c225e2160f02a8f292dbd4c0f6350769e4))

* docs: document hooks API ([`b21dca0`](https://github.com/python-gitlab/python-gitlab/commit/b21dca0acb2c12add229a1742e0c552aa50618c1))

* docs: add project members doc ([`dcf31a4`](https://github.com/python-gitlab/python-gitlab/commit/dcf31a425217efebe56d4cbc8250dceb3844b2fa))

* docs: document projects API ([`967595f`](https://github.com/python-gitlab/python-gitlab/commit/967595f504b8de076ae9218a96c3b8dd6273b9d6))

* docs: crossref improvements ([`6f9f42b`](https://github.com/python-gitlab/python-gitlab/commit/6f9f42b64cb82929af60e299c70773af6d406a6e))

* docs: start a FAQ ([`c305459`](https://github.com/python-gitlab/python-gitlab/commit/c3054592f79caa782ec79816501335e9a5c4e9ed))

* docs: do not use the :option: markup ([`368017c`](https://github.com/python-gitlab/python-gitlab/commit/368017c01f15013ab4cc9405c246a86e67f3b067))

### Feature

* feat: add mr rebase method ([`bc4280c`](https://github.com/python-gitlab/python-gitlab/commit/bc4280c2fbff115bd5e29a6f5012ae518610f626))

* feat: get artifact by ref and job ([`cda1174`](https://github.com/python-gitlab/python-gitlab/commit/cda117456791977ad300a1dd26dec56009dac55e))

* feat: add support for issue.related_merge_requests

Closes #794 ([`90a3631`](https://github.com/python-gitlab/python-gitlab/commit/90a363154067bcf763043124d172eaf705c8fe90))

* feat: add support for board update

Closes #801 ([`908d79f`](https://github.com/python-gitlab/python-gitlab/commit/908d79fa56965e7b3afcfa23236beef457cfa4b4))

* feat: bump version to 1.9.0 ([`aaed448`](https://github.com/python-gitlab/python-gitlab/commit/aaed44837869bd2ce22b6f0d2e1196b1d0e626a6))

* feat: implement artifacts deletion

Closes #744 ([`76b6e1f`](https://github.com/python-gitlab/python-gitlab/commit/76b6e1fc0f42ad00f21d284b4ca2c45d6020fd19))

* feat: add endpoint to get the variables of a pipeline

It adds a new endpoint which was released in the Gitlab CE 11.11.

Signed-off-by: Agustin Henze &lt;tin@redhat.com&gt; ([`564de48`](https://github.com/python-gitlab/python-gitlab/commit/564de484f5ef4c76261057d3d2207dc747da020b))

* feat(GitLab Update): delete ProjectPipeline (#736)

* feat(GitLab Update): delete ProjectPipeline

As of Gitlab 11.6 it is now possible to delete a pipeline - https://docs.gitlab.com/ee/api/pipelines.html#delete-a-pipeline ([`768ce19`](https://github.com/python-gitlab/python-gitlab/commit/768ce19c5e5bb197cddd4e3871c175e935c68312))

* feat: Added approve &amp; unapprove method for Mergerequests

Offical GitLab API supports this for GitLab EE ([`53f7de7`](https://github.com/python-gitlab/python-gitlab/commit/53f7de7bfe0056950a8e7271632da3f89e3ba3b3))

* feat: obey the rate limit

done by using the retry-after header

Fixes #166 ([`2abf9ab`](https://github.com/python-gitlab/python-gitlab/commit/2abf9abacf834da797f2edf6866e12886d642b9d))

### Fix

* fix: improve pickle support ([`b4b5dec`](https://github.com/python-gitlab/python-gitlab/commit/b4b5decb7e49ac16d98d56547a874fb8f9d5492b))

* fix(cli): allow --recursive parameter in repository tree

Fixes #718
Fixes #731 ([`7969a78`](https://github.com/python-gitlab/python-gitlab/commit/7969a78ce8605c2b0195734e54c7d12086447304))

* fix(cli): don&#39;t fail when the short print attr value is None

Fixes #717
Fixes #727 ([`8d1552a`](https://github.com/python-gitlab/python-gitlab/commit/8d1552a0ad137ca5e14fabfc75f7ca034c2a78ca))

* fix(cli): fix update value for key not working ([`b766203`](https://github.com/python-gitlab/python-gitlab/commit/b7662039d191ebb6a4061c276e78999e2da7cd3f))

* fix: convert # to %23 in URLs

Refactor a bit to handle this change, and add unit tests.

Closes #779 ([`14f5385`](https://github.com/python-gitlab/python-gitlab/commit/14f538501bfb47c92e02e615d0817675158db3cf))

* fix: pep8 errors

Errors have not been detected by broken travis runs. ([`334f9ef`](https://github.com/python-gitlab/python-gitlab/commit/334f9efb18c95bb5df3271d26fa0a55b7aec1c7a))

* fix(api): Make *MemberManager.all() return a list of objects

Fixes #699 ([`d74ff50`](https://github.com/python-gitlab/python-gitlab/commit/d74ff506ca0aadaba3221fc54cbebb678240564f))

* fix: use python2 compatible syntax for super ([`b08efcb`](https://github.com/python-gitlab/python-gitlab/commit/b08efcb9d155c20fa938534dd2d912f5191eede6))

* fix: re-add merge request pipelines ([`877ddc0`](https://github.com/python-gitlab/python-gitlab/commit/877ddc0dbb664cd86e870bb81d46ca614770b50e))

* fix(api): Don&#39;t try to parse raw downloads

http_get always tries to interpret the retrieved data if the
content-type is json. In some cases (artifact download for instance)
this is not the expected behavior.

This patch changes http_get and download methods to always get the raw
data without parsing.

Closes #683 ([`35a6d85`](https://github.com/python-gitlab/python-gitlab/commit/35a6d85acea4776e9c4ad23ff75259481a6bcf8d))

* fix(api): avoid parameter conflicts with python and gitlab

Provide another way to send data to gitlab with a new `query_parameters`
argument. This parameter can be used to explicitly define the dict of
items to send to the server, so that **kwargs are only used to specify
python-gitlab specific parameters.

Closes #566
Closes #629 ([`4bd027a`](https://github.com/python-gitlab/python-gitlab/commit/4bd027aac41c41f7e22af93c7be0058d2faf7fb4))

* fix: remove decode() on error_message string

The integration tests failed because a test called &#39;decode()&#39; on a
string-type variable - the GitLabException class handles byte-to-string
conversion already in its __init__. This commit removes the call to
&#39;decode()&#39; in the test.

```
Traceback (most recent call last):
  File &#34;./tools/python_test_v4.py&#34;, line 801, in &lt;module&gt;
    assert &#39;Retry later&#39; in error_message.decode()
AttributeError: &#39;str&#39; object has no attribute &#39;decode&#39;
``` ([`16bda20`](https://github.com/python-gitlab/python-gitlab/commit/16bda20514e036e51bef210b565671174cdeb637))

* fix: handle empty &#39;Retry-After&#39; header from GitLab

When requests are throttled (HTTP response code 429), python-gitlab
assumed that &#39;Retry-After&#39; existed in the response headers. This is
not always the case and so the request fails due to a KeyError. The
change in this commit adds a rudimentary exponential backoff to the
&#39;http_request&#39; method, which defaults to 10 retries but can be set
to -1 to retry without bound. ([`7a3724f`](https://github.com/python-gitlab/python-gitlab/commit/7a3724f3fca93b4f55aed5132cf46d3718c4f594))

* fix(api): make reset_time_estimate() work again

Closes #672 ([`cb388d6`](https://github.com/python-gitlab/python-gitlab/commit/cb388d6e6d5ec6ef1746edfffb3449c17e31df34))

* fix: enable use of YAML in the CLI

In order to use the YAML output, PyYaml needs to be installed on the docker image.
This commit adds the installation to the dockerfile as a separate layer. ([`ad0b476`](https://github.com/python-gitlab/python-gitlab/commit/ad0b47667f98760d6a802a9d08b2da8f40d13e87))

* fix: docker entry point argument passing

Fixes the problem of passing spaces in the arguments to the docker entrypoint.

Before this fix, there was virtually no way to pass spaces in arguments such as task description. ([`67ab637`](https://github.com/python-gitlab/python-gitlab/commit/67ab6371e69fbf137b95fd03105902206faabdac))

* fix(cli): exit on config parse error, instead of crashing

* Exit and hint user about possible errors
* test: adjust test cases to config missing error ([`6ad9da0`](https://github.com/python-gitlab/python-gitlab/commit/6ad9da04496f040ae7d95701422434bc935a5a80))

* fix(docker): use docker image with current sources ([`06e8ca8`](https://github.com/python-gitlab/python-gitlab/commit/06e8ca8747256632c8a159f760860b1ae8f2b7b5))

* fix(cli): print help and usage without config file

Fixes #560 ([`6bb4d17`](https://github.com/python-gitlab/python-gitlab/commit/6bb4d17a92832701b9f064a6577488cc42d20645))

### Refactor

* refactor: format everything black ([`318d277`](https://github.com/python-gitlab/python-gitlab/commit/318d2770cbc90ae4d33170274e214b9d828bca43))

* refactor: rename MASTER_ACCESS

to MAINTAINER_ACCESS to follow GitLab 11.0 docs

See:
https://docs.gitlab.com/ce/user/permissions.html#project-members-permissions ([`c38775a`](https://github.com/python-gitlab/python-gitlab/commit/c38775a5d52620a9c2d506d7b0952ea7ef0a11fc))

### Style

* style: format with black again ([`22b5082`](https://github.com/python-gitlab/python-gitlab/commit/22b50828d6936054531258f3dc17346275dd0aee))

### Test

* test: minor test fixes ([`3b523f4`](https://github.com/python-gitlab/python-gitlab/commit/3b523f4c39ba4b3eacc9e76fcb22de7b426d2f45))

* test: add project releases test

Fixes #762 ([`8ff8af0`](https://github.com/python-gitlab/python-gitlab/commit/8ff8af0d02327125fbfe1cfabe0a09f231e64788))

* test: increase speed by disabling the rate limit faster ([`497f56c`](https://github.com/python-gitlab/python-gitlab/commit/497f56c3e1b276fb9499833da0cebfb3b756d03b))

* test: always use latest version to test ([`82b0fc6`](https://github.com/python-gitlab/python-gitlab/commit/82b0fc6f3884f614912a6440f4676dfebee12d8e))

* test: update the tests for GitLab 11.11

Changes in GitLab make the functional tests fail:

* Some actions add new notes and discussions: do not use hardcoded
  values in related listing asserts
* The feature flag API is buggy (errors 500): disable the tests for now ([`622854f`](https://github.com/python-gitlab/python-gitlab/commit/622854fc22c31eee988f8b7f59dbc033ff9393d6))

### Unknown

* Merge pull request #842 from python-gitlab/chore/bump-package-version

chore: bump package version to 1.10.0 ([`2c1ea56`](https://github.com/python-gitlab/python-gitlab/commit/2c1ea56a217525bbb0a5321eb392c7fe7c100d44))

* Merge pull request #841 from python-gitlab/docs/project-snippets

docs(snippets): fix project-snippets layout ([`29d102f`](https://github.com/python-gitlab/python-gitlab/commit/29d102f893025188a6c300d8cc27d0d62147d6df))

* Merge pull request #840 from python-gitlab/docs/project-docs

docs(projects): add mention about project listings ([`de19296`](https://github.com/python-gitlab/python-gitlab/commit/de19296c57e40fede902270543800b499d90f82c))

* Merge pull request #838 from python-gitlab/pickle-fix

fix: improve pickle support ([`f0e3daa`](https://github.com/python-gitlab/python-gitlab/commit/f0e3daadb7f669b7d041a3024da238b54eaacda4))

* Merge pull request #839 from python-gitlab/dajsn-fix-readme-six-url

docs(readme): fix six url ([`8d54cf5`](https://github.com/python-gitlab/python-gitlab/commit/8d54cf57b03ff5509801c10d9dfe47e708173935))

* Merge pull request #837 from python-gitlab/PR-bugfix-718

fix(cli): allow --recursive parameter in repository tree ([`27b9706`](https://github.com/python-gitlab/python-gitlab/commit/27b9706b43f14f9e0cf954cdec368c63e83a2a0d))

* Merge pull request #836 from python-gitlab/test/project-releases

 test: add project releases test ([`262b222`](https://github.com/python-gitlab/python-gitlab/commit/262b222000dad30fc6dfc63ccf2fa200eba09662))

* Merge pull request #835 from python-gitlab/bugfix-717

fix(cli): don&#39;t fail when the short print attr value is None ([`0b0a60f`](https://github.com/python-gitlab/python-gitlab/commit/0b0a60fd72fc7b1073c4b5f32022b3a063ec9c96))

* Merge pull request #833 from python-gitlab/project-variable-update

fix(cli): fix update value for key not working ([`6c673c6`](https://github.com/python-gitlab/python-gitlab/commit/6c673c6b052cd5b18ba5b1f83137485431666730))

* Merge pull request #834 from python-gitlab/chore/setup-supported-versions

chore(setup): add 3.7 to supported python versions ([`8306ef2`](https://github.com/python-gitlab/python-gitlab/commit/8306ef21be731336c9706c9908133cfcb3b6a5f4))

* Merge pull request #832 from python-gitlab/test/always-latest

test: always use latest version to test ([`8f1ed93`](https://github.com/python-gitlab/python-gitlab/commit/8f1ed933f58f36b5383c3f862a59ce73e7954f02))

* Merge pull request #823 from jeroen92/rebase-mr

Resolve #822, add mr rebase ([`b9877b4`](https://github.com/python-gitlab/python-gitlab/commit/b9877b4e6479e66ca30a2908ee9c2703366eb9ce))

* Merge pull request #831 from python-gitlab/chore/move-back-to-travis

chore: move checks back to travis ([`c8a7e31`](https://github.com/python-gitlab/python-gitlab/commit/c8a7e31cb57e3be7287ba237dbda7c4efa195b29))

* Merge pull request #830 from python-gitlab/chore/ci-disable-py-func

Chore/ci disable py func ([`2e42e28`](https://github.com/python-gitlab/python-gitlab/commit/2e42e289efbf24fb6fd85df45b56a875875b6932))

* Merge pull request #827 from ahaynssen/master

docs: re-order api examples ([`5492b71`](https://github.com/python-gitlab/python-gitlab/commit/5492b71a189f6a85e8f1542e13295f528555df31))

* Merge pull request #824 from python-gitlab/feat/add-ref-artifacts

feat: get artifact by ref and job ([`4a8503d`](https://github.com/python-gitlab/python-gitlab/commit/4a8503db1c55f5a8d1cc66533325d2d832622f85))

* Merge pull request #803 from python-gitlab/feat/related_mr

feat: add support for issue.related_merge_requests ([`ad1c0dd`](https://github.com/python-gitlab/python-gitlab/commit/ad1c0dda37f573673beaf9f25187f51751a5a484))

* Merge pull request #804 from python-gitlab/feat/update_board

feat: add support for board update ([`f539c36`](https://github.com/python-gitlab/python-gitlab/commit/f539c36dddf8e0eb3b2156a3ed4e2ff2fa667cf1))

* Merge pull request #808 from minitux/patch-1 ([`2ea8eb8`](https://github.com/python-gitlab/python-gitlab/commit/2ea8eb8c66480fce2a3cd5294f0dc64ce826b12b))

* Merge pull request #805 from python-gitlab/chore/ci-rebuild-image

chore(ci): rebuild test image, when something changed ([`6625a06`](https://github.com/python-gitlab/python-gitlab/commit/6625a062e3e4cc42abdaec9ea08e3b6e7f6a9c58))

* Merge pull request #802 from python-gitlab/chore/gitlab-11.11.3

chore(ci): update the GitLab version in the test image ([`51751c5`](https://github.com/python-gitlab/python-gitlab/commit/51751c5f78ec14e416e595fd42f97d55197df347))

* Merge pull request #792 from python-gitlab/chore/enable-gitlab-ci-builds

chore(ci): add automatic GitLab image pushes ([`50c53c0`](https://github.com/python-gitlab/python-gitlab/commit/50c53c034b4b8c0b408da47d3347f103e7f32493))

* Merge pull request #800 from python-gitlab/chore/ci-publish

chore(ci): fix gitlab PyPI publish ([`722a6ef`](https://github.com/python-gitlab/python-gitlab/commit/722a6efb23c6e6b87a7354c1c6ae8e50ae14c709))

* Merge pull request #797 from python-gitlab/feat/version-bump

feat: bump version to 1.9.0 ([`4b04432`](https://github.com/python-gitlab/python-gitlab/commit/4b0443285e3207d89b4b46211f713614fb526758))

* Merge pull request #799 from python-gitlab/docs/fix-group-access

docs(api-usage): fix project group example ([`b5aaa3e`](https://github.com/python-gitlab/python-gitlab/commit/b5aaa3eda97589ab94f921c4bcbb6e86740dde51))

* Merge pull request #767 from python-gitlab/fix/744/delete_artifacts

feature: Implement artifacts deletion ([`4e1dd27`](https://github.com/python-gitlab/python-gitlab/commit/4e1dd27d6400acd152be19692f3193f948422769))

* Merge pull request #791 from python-gitlab/tests-for-gl-11.11

test: update the tests for GitLab 11.11 ([`e45a6e2`](https://github.com/python-gitlab/python-gitlab/commit/e45a6e2618db30834f732c5a7bc9f1c038c45c31))

* Merge pull request #789 from python-gitlab/no-more-v3

docs: remove v3 support ([`e2115b1`](https://github.com/python-gitlab/python-gitlab/commit/e2115b1e5bb0bb2861427dd136362f92ec00619d))

* Merge pull request #785 from agustinhenze/add-pipeline-get-variables-endpoint

Add new endpoint to get the variables of a pipeline ([`463cedc`](https://github.com/python-gitlab/python-gitlab/commit/463cedc952155ad56ce0762bc04e0ff303b093fe))

* Merge pull request #768 from python-gitlab/trigger_token_example

docs: Add an example of trigger token usage ([`5af0b52`](https://github.com/python-gitlab/python-gitlab/commit/5af0b527a44d10b648c2c1464cfbb25c2a642af0))

* Merge pull request #790 from python-gitlab/fix/779

fix: convert # to %23 in URLs ([`101ccd1`](https://github.com/python-gitlab/python-gitlab/commit/101ccd148ee011e3b8e01d93f176ed969411c634))

* Merge pull request #788 from python-gitlab/black-in-tox

Add a tox job to run black ([`d135e4e`](https://github.com/python-gitlab/python-gitlab/commit/d135e4ef93a191aeb50ce1296757f7e75926a23c))

* Merge pull request #778 from python-gitlab/docs/readme-code-format

docs(readme): add more info about commitlint, code-format ([`794d64c`](https://github.com/python-gitlab/python-gitlab/commit/794d64c8ef8ef0448205b51ff4a25c1589c2b2dd))

* Merge pull request #775 from python-gitlab/refactor/black

refactor: format everything black ([`290e5ed`](https://github.com/python-gitlab/python-gitlab/commit/290e5edaf162c986dbb5eae8c1da63e47e62555d))

* Merge pull request #776 from python-gitlab/revert-760-custom_cli_actions_fix

Revert &#34;Custom cli actions fix&#34; ([`ef32990`](https://github.com/python-gitlab/python-gitlab/commit/ef32990347d0ab9145b8919d25269766dc2ce445))

* Revert &#34;Custom cli actions fix&#34; ([`d3a20c5`](https://github.com/python-gitlab/python-gitlab/commit/d3a20c514651dfe542a295eb608af1de22a28736))

* Merge pull request #760 from kkoralsky/custom_cli_actions_fix

Custom cli actions fix ([`e8823e9`](https://github.com/python-gitlab/python-gitlab/commit/e8823e91b04fd6cf3838ad256c02373db7029191))

* fix -/_ replacament for *Manager custom actions ([`6158fd2`](https://github.com/python-gitlab/python-gitlab/commit/6158fd23022b2e2643b6da7a39708b28ce59270a))

* dont ask for id attr if this is *Manager originating custom action ([`adb6305`](https://github.com/python-gitlab/python-gitlab/commit/adb63054add31e06cefec09982a02b1cd21c2cbd))

* Merge pull request #759 from kkoralsky/registry_api

registry api implementation ([`84bcdc0`](https://github.com/python-gitlab/python-gitlab/commit/84bcdc0c452d2ada9a47aa9907d7551aeac23821))

* documentation fix ([`2d9078e`](https://github.com/python-gitlab/python-gitlab/commit/2d9078e8e785e3a17429623693f84bbf8526ee58))

* whitespaces ([`c91230e`](https://github.com/python-gitlab/python-gitlab/commit/c91230e4863932ef8b8781835a37077301fd7440))

* documentation ([`4d31b9c`](https://github.com/python-gitlab/python-gitlab/commit/4d31b9c7b9bddf6ae2da41d2f87c6e92f97122e0))

* fix docstring &amp; improve coding style ([`3cede7b`](https://github.com/python-gitlab/python-gitlab/commit/3cede7bed7caca026ec1bce8991eaac2e43c643a))

* register cli action for delete_in_bulk ([`0b79ce9`](https://github.com/python-gitlab/python-gitlab/commit/0b79ce9c32cbc0bf49d877e123e49e2eb199b8af))

* fix repository_id marshaling in cli ([`340cd37`](https://github.com/python-gitlab/python-gitlab/commit/340cd370000bbb48b81a5b7c1a7bf9f33997cef9))

* merged new release &amp; registry apis ([`910c286`](https://github.com/python-gitlab/python-gitlab/commit/910c2861a3c895cca5aff0a0df1672bb7388c526))

* Merge pull request #773 from python-gitlab/chore/ci-reliable-system

chore(ci): use reliable ci system ([`3dc6413`](https://github.com/python-gitlab/python-gitlab/commit/3dc64131eaec7d08b059039f446cc8d8c4b58c81))

* Merge pull request #769 from python-gitlab/pep-fixes

fix: pep8 errors ([`a730598`](https://github.com/python-gitlab/python-gitlab/commit/a7305980ef4065a6518951fb166b11eec9003b4d))

* Merge pull request #746 from therealgambo/master

add project releases api ([`16de1b0`](https://github.com/python-gitlab/python-gitlab/commit/16de1b03fde3dbbe8f851614dd1d8c09de102fe5))

* Use NoUpdateMixin for now ([`8e55a3c`](https://github.com/python-gitlab/python-gitlab/commit/8e55a3c85f3537e2be1032bf7d28080a4319ec89))

* add project releases api ([`3680545`](https://github.com/python-gitlab/python-gitlab/commit/3680545a01513ed044eb888151d2e2c635cea255))

* Merge pull request #714 from jaraco/feature/runpy-invoke

Add runpy hook, allowing invocation with &#39;python -m gitlab&#39;. ([`a3a7713`](https://github.com/python-gitlab/python-gitlab/commit/a3a771310de16be7bba041c962223f7bda9aa4d6))

* Add runpy hook. Fixes #713.

Allows for invocation with &#39;python -m gitlab&#39; ([`cd2a14e`](https://github.com/python-gitlab/python-gitlab/commit/cd2a14ea1bb4feca636de1d660378a3807101e63))

* Merge pull request #738 from jeroendecroos/Gitlab_from_config_inheritance

Make gitlab.Gitlab.from_config a classmethod ([`6bd1902`](https://github.com/python-gitlab/python-gitlab/commit/6bd19027f2cd1cc20d59182d8856f5955e0702e5))

* Make gitlab.Gitlab.from_config a classmethod ([`0b70da3`](https://github.com/python-gitlab/python-gitlab/commit/0b70da335690456a556afb9ff7a56dfca693b019))

* Merge pull request #732 from hakanf/master

Re-enable command specific help messages ([`a6e10f9`](https://github.com/python-gitlab/python-gitlab/commit/a6e10f957aeccd7a1fd4e769f7e3acf6e4683308))

* Use sys.exit as in rest of code ([`6fe2988`](https://github.com/python-gitlab/python-gitlab/commit/6fe2988dd050c05b17556cacac4e283fbf5242a8))

* Re-enable command specific help mesaages

This makes sure that the global help message wont be printed instead of the command spedific one unless we fail to read the configuration file ([`a8caddc`](https://github.com/python-gitlab/python-gitlab/commit/a8caddcb1e193c5472f5521dee0e18b1af32c89b))

* Merge pull request #729 from xarx00/PR-bugfix-716

Fix for #716: %d replaced by %s ([`bc973d4`](https://github.com/python-gitlab/python-gitlab/commit/bc973d450114fcdb2fb8222ab598b5d932585064))

* Fix for #716: %d replaced by %s ([`675f879`](https://github.com/python-gitlab/python-gitlab/commit/675f879c1ec6cf1c77cbf96d8b7b2cd51e1cbaad))

* Merge pull request #725 from python-gitlab/fix/699

fix(api): Make *MemberManager.all() return a list of objects ([`1792442`](https://github.com/python-gitlab/python-gitlab/commit/17924424e5112f5c4b3de16e46856794dea3509b))

* Merge pull request #721 from purificant/fix_typo

fix tiny typo ([`b21fa28`](https://github.com/python-gitlab/python-gitlab/commit/b21fa2854302ef4d9301242ef719eaa509adf077))

* fix tiny typo ([`2023875`](https://github.com/python-gitlab/python-gitlab/commit/20238759d33710ed2d7158bc8ce6123db6760ab9))

* Merge pull request #707 from python-gitlab/fix/python-tests

fix: use python2 compatible syntax for super ([`e58d2a8`](https://github.com/python-gitlab/python-gitlab/commit/e58d2a8567545ce14a6e1ee64423fe12f571b2ca))

* Merge pull request #706 from python-gitlab/chore/ci-existing-release

chore(ci): don&#39;t try to publish existing release ([`39cb97d`](https://github.com/python-gitlab/python-gitlab/commit/39cb97d0f15b675f308a052f0c4856d467971f14))

* Merge pull request #702 from jpiron/eq_hash

Implement __eq__ and __hash__ methods ([`a4ea0fe`](https://github.com/python-gitlab/python-gitlab/commit/a4ea0fe6b91d856b30d25c9f0f71ef9cae8f3f08))

* Implement __eq__ and __hash__ methods

To ease lists and sets manipulations. ([`3d60850`](https://github.com/python-gitlab/python-gitlab/commit/3d60850aa42351a0bb0066ef579ade95df5a81ee))

* Merge pull request #705 from python-gitlab/release-1.8.0

Release version 1.8.0 ([`57fa4e3`](https://github.com/python-gitlab/python-gitlab/commit/57fa4e37aaf6ccee0d75085520f96fd15752a3df))

* Release version 1.8.0 ([`4fce338`](https://github.com/python-gitlab/python-gitlab/commit/4fce3386cf54c9d66c44f5b9c267330928bd1efe))

* Merge pull request #701 from jpiron/fix_all_behaviour

Fix all kwarg behaviour ([`8ce4e9e`](https://github.com/python-gitlab/python-gitlab/commit/8ce4e9e07913d9b9bb916d079ff0a7c528830a2d))

* Fix all kwarg behaviour

`all` kwarg is used to manage GitlabList generator behaviour.
However, as it is not poped from kwargs, it is sent to Gitlab API.
Some endpoints such as [the project commits](https://docs.gitlab.com/ee/api/commits.html#list-repository-commits) one,
support a `all` attribute.
This means a call like `project.commits.list(all=True, ref_name=&#39;master&#39;)`
won&#39;t return all the master commits as one might expect but all the
repository&#39;s commits.
To prevent confusion, the same kwarg shouldn&#39;t be used for 2 distinct
purposes.
Moreover according to [the documentation](https://python-gitlab.readthedocs.io/en/stable/gl_objects/commits.html#examples),
the `all` project commits API endpoint attribute doesn&#39;t seem supported. ([`6b2bf5b`](https://github.com/python-gitlab/python-gitlab/commit/6b2bf5b29c235243c11bbc994e7f2540a6a3215e))

* Merge pull request #689 from python-gitlab/fix/wrong-rebase

fix: re-add merge request pipelines ([`31bca2f`](https://github.com/python-gitlab/python-gitlab/commit/31bca2f9ee55ffa69d34f4584e90da01d3f6325e))

* Merge pull request #685 from Joustie/master

feat: Added approve method for Mergerequests ([`641b80a`](https://github.com/python-gitlab/python-gitlab/commit/641b80a373746c9e6dc6d043216ebc4ba5613011))

* Merge branch &#39;master&#39; into master ([`b51d296`](https://github.com/python-gitlab/python-gitlab/commit/b51d2969ad34a9aad79e42a69f275caf2a4059cb))

* Merge pull request #687 from python-gitlab/fix/683/raw_download

fix(api): Don&#39;t try to parse raw downloads ([`52d7631`](https://github.com/python-gitlab/python-gitlab/commit/52d76312660109d3669d459b11b448a3a60b9603))

* Merge pull request #680 from python-gitlab/chore/automatic-deploy

chore: release tags to PyPI automatically ([`ca8c85c`](https://github.com/python-gitlab/python-gitlab/commit/ca8c85cf3ed4d4d62fc86a3b52ea8a5c4f2d0cd0))

* Merge pull request #681 from python-gitlab/no-param-conflicts

fix(api): avoid parameter conflicts with python and gitlab ([`572029c`](https://github.com/python-gitlab/python-gitlab/commit/572029cd49fe356e38ee8bddc3dda3067cf868b0))

* Merge pull request #678 from appian/backoff-requests

Fix missing &#34;Retry-After&#34; header and fix integration tests ([`89679ce`](https://github.com/python-gitlab/python-gitlab/commit/89679ce5ee502e57dbe7cec2b78f4f70b85fd3a5))

* Merge pull request #673 from python-gitlab/fix/672

fix(api): make reset_time_estimate() work again ([`ce2c835`](https://github.com/python-gitlab/python-gitlab/commit/ce2c8356cdd0e086ec67a1bf73adc2d0ea251971))

* Merge pull request #664 from python-gitlab/docs/commit-message

docs(readme): provide commit message guidelines ([`85ac102`](https://github.com/python-gitlab/python-gitlab/commit/85ac10200805de480a076760368336c8135e5acf))

* Merge pull request #659 from python-gitlab/docs/readme-pypi

docs(setup): use proper readme on PyPI ([`9be82e1`](https://github.com/python-gitlab/python-gitlab/commit/9be82e1dfc77010fa9b4c1b6313abae519a00ac4))

* Merge pull request #657 from python-gitlab/release-1.7.0

Prepare the 1.7.0 release ([`704ca51`](https://github.com/python-gitlab/python-gitlab/commit/704ca51d9e487b2a665f219a5f7ce8b05e8eeea7))

* Prepare the 1.7.0 release ([`456f3c4`](https://github.com/python-gitlab/python-gitlab/commit/456f3c48e48dcff59e063c2572b6028f1abfba82))

* Merge pull request #656 from esabouraud/feature-protectedbranchesoptions

Issue 653 Add access control options to protected branch creation ([`59e3e45`](https://github.com/python-gitlab/python-gitlab/commit/59e3e457f01810666d90381c25f52addecb606e2))

* Add access control options to protected branch creation ([`cebbbf6`](https://github.com/python-gitlab/python-gitlab/commit/cebbbf67f2529bd9380276ac28abe726d3a57a81))

* Merge pull request #652 from roozbehf/fix/docker-enable-use-of-yaml

fix: enable use of YAML in the CLI ([`728f2dd`](https://github.com/python-gitlab/python-gitlab/commit/728f2dd1677522a4fcca76769ed127146c034c29))

* Merge pull request #651 from roozbehf/fix/docker-entrypoint-arguments

fix: docker entry point argument passing ([`f945910`](https://github.com/python-gitlab/python-gitlab/commit/f945910d54bd8817560d45eb135d18e4b52b6717))

* Merge pull request #641 from python-gitlab/refactor/excpetion_msg

Improve error message handling in exceptions ([`7bd41cb`](https://github.com/python-gitlab/python-gitlab/commit/7bd41cbf88af87a31ad1943f58c5f7f8295d956b))

* Improve error message handling in exceptions

* Depending on the request Gitlab has a &#39;message&#39; or &#39;error&#39; attribute
in the json data, handle both
* Add some consistency by converting messages to unicode or str for
exceptions (depending on the python version)

Closes #616 ([`1fb1296`](https://github.com/python-gitlab/python-gitlab/commit/1fb1296c9191e57e109c4e5eb9504bce191a6ff1))

* Merge pull request #625 from python-gitlab/fix/611/resource_label_event

Add support to resource label events ([`20eb7d8`](https://github.com/python-gitlab/python-gitlab/commit/20eb7d8900cdc24c3ea1e7ef2262dca9965a2884))

* Add support to resource label events

Closes #611 ([`95d0d74`](https://github.com/python-gitlab/python-gitlab/commit/95d0d745d4bafe702c89c972f644b049d6c810ab))

* Merge pull request #642 from python-gitlab/feature/589/member_all

[feature] Add support for members all() method ([`22536f3`](https://github.com/python-gitlab/python-gitlab/commit/22536f34d87e5df1a3400d3f474a988c93b9bfb1))

* [feature] Add support for members all() method

Closes #589 ([`ef1523a`](https://github.com/python-gitlab/python-gitlab/commit/ef1523a23737db45d0f439badcd8be564bcb67fb))

* Merge pull request #639 from python-gitlab/fix/628/doc_typo

[docs] Fix typo in custom attributes example ([`011274e`](https://github.com/python-gitlab/python-gitlab/commit/011274e7f94519d30dee59f5448215838d058e37))

* [docs] Fix typo in custom attributes example

Closes #628 ([`bb251b8`](https://github.com/python-gitlab/python-gitlab/commit/bb251b8ef780216de03dde67912ad5fffbb30390))

* Merge pull request #638 from python-gitlab/fix/633/milestone_filter

[docs] Fix the milestone filetring doc (iid -&gt; iids) ([`e6df9a8`](https://github.com/python-gitlab/python-gitlab/commit/e6df9a8b2f9c2397ea3ae67dfe19a2fa91f41c19))

* [docs] Fix the milestone filetring doc (iid -&gt; iids)

Fixes #633 ([`0c9a00b`](https://github.com/python-gitlab/python-gitlab/commit/0c9a00bb154007a0a9f665ca38e6fec50d378eaf))

* Merge pull request #634 from python-gitlab/docs/project-typo

docs(projects): fix typo in code sample

Closes #630 ([`c8eaeb2`](https://github.com/python-gitlab/python-gitlab/commit/c8eaeb2d258055b8fc77cbeef373aee5551c181a))

* Merge pull request #636 from python-gitlab/docs/groups-fix-typo

docs(groups): fix typo ([`c72a87a`](https://github.com/python-gitlab/python-gitlab/commit/c72a87aa36c497017df06986bf32200dee3688e4))

* Merge pull request #627 from nicgrayson/fix-docs-typo

Fix 3 typos in docs ([`7f09666`](https://github.com/python-gitlab/python-gitlab/commit/7f09666eb200526d7293cb42e6c9fda5c41beb87))

* Fix 3 typos ([`a5ab2bb`](https://github.com/python-gitlab/python-gitlab/commit/a5ab2bb6272acd0285ce84ba6f01fe417c1c5124))

* Merge pull request #624 from python-gitlab/update/docker-image

Use the pythongitlab/test-python-gitlab docker image for tests ([`742243f`](https://github.com/python-gitlab/python-gitlab/commit/742243f4f43042d4b561e3875dc38e560bb71624))

* Use the pythongitlab/test-python-gitlab docker image for tests

This images is updated to the latest GitLab CE.

Fix the diff() test to match the change in the API output. ([`2c6c929`](https://github.com/python-gitlab/python-gitlab/commit/2c6c929f78dfda92d5ae93235bb9065d289a68cc))

* Merge pull request #619 from python-gitlab/issue/595

[docs] Add an example of pipeline schedule vars listing ([`fcce7a3`](https://github.com/python-gitlab/python-gitlab/commit/fcce7a316968a9aea7aa504730cea1734c2f897a))

* [docs] Add an example of pipeline schedule vars listing

Closes #595 ([`f7fbfca`](https://github.com/python-gitlab/python-gitlab/commit/f7fbfca7e6a32a31dbf7ca8e1d4f83b34b7ac9db))

* Merge pull request #626 from python-gitlab/fix/596/maintainer_wanted

[README] Remove the &#34;maintainer(s) wanted&#34; notice ([`bc6ce04`](https://github.com/python-gitlab/python-gitlab/commit/bc6ce047959a57e58e8260b41556f29b3da27da4))

* [README] Remove the &#34;maintainer(s) wanted&#34; notice

Closes #596 ([`f51fa19`](https://github.com/python-gitlab/python-gitlab/commit/f51fa19dc4f78d036f18217436add00b7d94c39d))

* Merge pull request #620 from bittner/patch-1

Add Gitter badge to README ([`74623cf`](https://github.com/python-gitlab/python-gitlab/commit/74623cf38d20fe93183cd3721b751796019ab98c))

* Add Gitter badge to README ([`31d1c5d`](https://github.com/python-gitlab/python-gitlab/commit/31d1c5dadb5f816d23e7882aa112042db019b681))

* Merge pull request #613 from mkosiarc/fixDoc

[docs] fix discussions typo ([`368a34d`](https://github.com/python-gitlab/python-gitlab/commit/368a34d6d7a6a8bddc81a4365391d09485005f97))

* [docs] fix discussions typo ([`54b6a54`](https://github.com/python-gitlab/python-gitlab/commit/54b6a545399b51a34fb11819cc24f288bc191651))

* Merge pull request #605 from python-gitlab/fix/docker

fix(docker): use docker image with current sources ([`c9f7986`](https://github.com/python-gitlab/python-gitlab/commit/c9f7986a83bc4aa1743f446b7a10fc79bc909eda))

* Merge pull request #608 from python-gitlab/ci-output-option

 docs(cli): add PyYAML requirement notice ([`156a21e`](https://github.com/python-gitlab/python-gitlab/commit/156a21e1a2c9dcb6a14d95655ef24d5520e1dcc1))

* Merge pull request #607 from python-gitlab/refactor/rename-variable

refactor: rename MASTER_ACCESS ([`5ff2608`](https://github.com/python-gitlab/python-gitlab/commit/5ff2608f3eef773f06d3b1c70c2317a96f53a4b4))

* Merge pull request #601 from max-wittig/fix/help-usage

fix(cli): print help and usage without config file ([`32b5122`](https://github.com/python-gitlab/python-gitlab/commit/32b5122d14d32c06c7db3a2923fe56a6331562e5))

* Merge pull request #600 from hans-d/docker

more flexible docker ([`3a8b1a0`](https://github.com/python-gitlab/python-gitlab/commit/3a8b1a0b11b9e6a60037f90c99dd288cecd09d3d))

* Merge branch &#39;master&#39; into docker ([`756c73c`](https://github.com/python-gitlab/python-gitlab/commit/756c73c011b64f94747638f9e5d9afa128aeafe0))

* Add project protected tags management (#581) ([`ea71f1d`](https://github.com/python-gitlab/python-gitlab/commit/ea71f1d121b723140671e2090182174234f0e2a1))

* more flexible docker ([`21d2577`](https://github.com/python-gitlab/python-gitlab/commit/21d257782bb1aea9d154e797986ed0f6cdd36fad))

* README: add a note about maintainers ([`77f4d3a`](https://github.com/python-gitlab/python-gitlab/commit/77f4d3af9c1e5f08b8f4e3aa32c7944c9814dab0))

* Merge pull request #586 from Halliburton-Landmark/project-issue-create-args

add missing comma in ProjectIssueManager _create_attrs ([`58d5c0a`](https://github.com/python-gitlab/python-gitlab/commit/58d5c0a40b08870ffff4ec206a312e2630145a71))

* add missing comma in ProjectIssueManager _create_attrs

This fixes the argument handling for assignee/milestone ID when for `project-issue create` ([`83fb4f9`](https://github.com/python-gitlab/python-gitlab/commit/83fb4f9ec5f60a122fe9db26c426be74c335e5d5))

* [docs] Add a note about GroupProject limited API ([`9e60364`](https://github.com/python-gitlab/python-gitlab/commit/9e60364306a894855c8e0744ed4b93cec8ea9ad0))

* Fix the https redirection test ([`6f80380`](https://github.com/python-gitlab/python-gitlab/commit/6f80380ed1de49dcc035d06408263d4961e7d18b))

* [docs] add a warning about https://

http to https redirection cause problems. Make notes of this in the
docs. ([`042b706`](https://github.com/python-gitlab/python-gitlab/commit/042b706238810fa3b4fde92d298a709ebdb3a925))

* [docs] fix cut and paste leftover ([`b02c30f`](https://github.com/python-gitlab/python-gitlab/commit/b02c30f8b1829e87e2cc28ae7fdf8bb458a4b1c7))

* Use https:// for gitlab URL ([`256518c`](https://github.com/python-gitlab/python-gitlab/commit/256518cc1fab21c3dbfa7b67d5edcc81119090c5))

* [docs] Fix the owned/starred usage documentation

Closes #579 ([`ccf0c2a`](https://github.com/python-gitlab/python-gitlab/commit/ccf0c2ad35d4dd1af4f36e411027286a0be0f49f))

* 1.6.0 release ([`d8c2488`](https://github.com/python-gitlab/python-gitlab/commit/d8c2488a7b32e8f4a36109c4a4d6d4aad7ab8942))

* [cli] Fix the project-export download

Closes #559 ([`facbc8c`](https://github.com/python-gitlab/python-gitlab/commit/facbc8cb858ac400e912a905be3668ee2d33e2cd))

* Minor doc updates ([`e9506d1`](https://github.com/python-gitlab/python-gitlab/commit/e9506d15a971888a9af72b37d3e7dbce55e49126))

* Add a FAQ ([`4d4c8ad`](https://github.com/python-gitlab/python-gitlab/commit/4d4c8ad1f75142fa1ca6ccd037e9d501ca873b60))

* Raise an exception on https redirects for PUT/POST

POST and PUT requests are modified by clients when redirections happen.
A common problem with python-gitlab is a misconfiguration of the server
URL: the http to https redirection breaks some requests.

With this change python-gitlab should detect problematic redirections,
and raise a proper exception instead of failing with a cryptic error.

Closes #565 ([`a221d7b`](https://github.com/python-gitlab/python-gitlab/commit/a221d7b35bc20da758e7467fe789e16613c54275))

* [docs] Add/updates notes about read-only objects

MR and issues attached to the root API or groups are not editable.
Provide notes describing how to manage this. ([`80a68f9`](https://github.com/python-gitlab/python-gitlab/commit/80a68f9258422d5d74f05a20234070ce3d6f5559))

* Merge pull request #572 from btmanm/master

Update projects.rst ([`ff6ca5d`](https://github.com/python-gitlab/python-gitlab/commit/ff6ca5db6f7773328bac7d11830c89f76b3fe065))

* Update projects.rst ([`6ada4b0`](https://github.com/python-gitlab/python-gitlab/commit/6ada4b004ab3a1b25b07809a0c87fec6f9c1fcb4))

* Merge pull request #569 from mattthias/patch-1

Minor typo &#34;ou&#34; vs. &#34;or&#34; ([`0a687d3`](https://github.com/python-gitlab/python-gitlab/commit/0a687d38c777171befd6fa1d6292cf914dfc47ec))

* Minor typo &#34;ou&#34; vs. &#34;or&#34;

This change fixes a minor type in the table of possible values for options in the global section. ([`a68f459`](https://github.com/python-gitlab/python-gitlab/commit/a68f459da690b4231dddcc6609de7e1e709ba7cf))

* Add support for project transfers from the projects interface. (#561)

See https://docs.gitlab.com/ee/api/projects.html#transfer-a-project-to-a-new-namespace ([`a1c79d2`](https://github.com/python-gitlab/python-gitlab/commit/a1c79d2b7d719204c829235a9b0ebb08b45b4efb))

* Added support for listing forks of a project  (#562) ([`b325bd7`](https://github.com/python-gitlab/python-gitlab/commit/b325bd73400e3806e6ede59cc10011fbf138b877))

* MR: add the squash attribute for create/update

Closes #557 ([`35c8c82`](https://github.com/python-gitlab/python-gitlab/commit/35c8c8298392188c51e5956dd2eb90bb3d81a301))

* Implement MR.pipelines()

Closes #555 ([`32ae924`](https://github.com/python-gitlab/python-gitlab/commit/32ae92469f13fe2cbeb87361a4608dd5d95b3a70))

* Support group and global MR listing

Closes #553 ([`0379efa`](https://github.com/python-gitlab/python-gitlab/commit/0379efaa641d22ccdb530214c56ec72891f73c4a))

* Project import: fix the override_params parameter

Closes #552 ([`3461904`](https://github.com/python-gitlab/python-gitlab/commit/34619042e4839cf1f3031b1c3e6f791104f02dfe))

* [cli] Fix the case where we have nothing to print ([`a139179`](https://github.com/python-gitlab/python-gitlab/commit/a139179ea8246b2f000327bd1e106d5708077b31))

* [cli] Output: handle bytes in API responses

Closes #548 ([`bbef1f9`](https://github.com/python-gitlab/python-gitlab/commit/bbef1f916c8ab65ed7f9717859caf516ebedb335))

* Improve the snippets examples

closes #543 ([`bdbec67`](https://github.com/python-gitlab/python-gitlab/commit/bdbec678b1df23fd57b2e3c538e3eeac8d236690))

* Merge pull request #542 from tpdownes/patch-1

Fix simple typo in identity modification example ([`9751ab6`](https://github.com/python-gitlab/python-gitlab/commit/9751ab69ab4e492fadde015de922457e6a1c60ae))

* Fix simple typo in identity modification example ([`35fe227`](https://github.com/python-gitlab/python-gitlab/commit/35fe2275efe15861edd53ec5038497b475e47c7c))

* [docs] don&#39;t use hardcoded values for ids ([`fe43a28`](https://github.com/python-gitlab/python-gitlab/commit/fe43a287259633d1d8d4ea1ebc94320bc8020a9b))

* 1.5.1 release ([`5e6330f`](https://github.com/python-gitlab/python-gitlab/commit/5e6330f82b121a4d7772f4083dd94bdf9a6d915d))

* Improve the protect branch creation example

Closes #536 ([`590c41a`](https://github.com/python-gitlab/python-gitlab/commit/590c41ae5030140ea16904d22c15daa3a9ffd374))

* Fix the ProjectPipelineJob base class

Closes #537 ([`4cf8118`](https://github.com/python-gitlab/python-gitlab/commit/4cf8118ceb62ad661398036e26bc91b4665dc8ee))

* Prepare the 1.5.0 release ([`eaa4450`](https://github.com/python-gitlab/python-gitlab/commit/eaa44509316ad7e80f9e73ddde310987132d7508))

* [cli] Fix the non-verbose output of ProjectCommitComment

Closes #433 ([`d5289fe`](https://github.com/python-gitlab/python-gitlab/commit/d5289fe9369621aae9ac33bbd102b400dda97414))

* Use the same description for **kwargs everywhere ([`b1c6392`](https://github.com/python-gitlab/python-gitlab/commit/b1c63927aaa7c753fa622af5ac3637102ba9aea3))

* [docs] Add an example for external identities settings

Fixes #528 ([`21e382b`](https://github.com/python-gitlab/python-gitlab/commit/21e382b0c64350632a14222c43d9629cc89a9837))

* Revert &#34;make as_list work for all queries&#34;

This reverts commit 8e787612fa77dc945a4c1327e9faa6eee10c48f2.

This change broke the basic generator usage (Fixes #534) ([`1a04634`](https://github.com/python-gitlab/python-gitlab/commit/1a04634ae37888c3cd80c4676904664b0c8dbeab))

* Add support for epics API (EE)

Fixes #525 ([`ba90e30`](https://github.com/python-gitlab/python-gitlab/commit/ba90e305bc2d54eb42aa0f8251a9e45b0d1736e4))

* README update ([`b2cb700`](https://github.com/python-gitlab/python-gitlab/commit/b2cb70016e4fd2baa1f136a17946a474f1b18f24))

* ProjectPipelineJob objects can only be listed

And they are not directly related to ProjectJob objects.

Fixes #531 ([`e1af0a0`](https://github.com/python-gitlab/python-gitlab/commit/e1af0a08d9fb29e67a96d67cc2609eecdfc182f7))

* Add support for the LDAP gorups API ([`ebf822c`](https://github.com/python-gitlab/python-gitlab/commit/ebf822cef7e686d8a198dcf419c20b1bfb88dea3))

* Add support for the EE license API ([`5183069`](https://github.com/python-gitlab/python-gitlab/commit/5183069722224914bd6c2d25996163861183415b))

* Merge pull request #530 from stefancrain/master

Correct session example ([`3f88ad0`](https://github.com/python-gitlab/python-gitlab/commit/3f88ad0dd92b6d5e418e2a615b57dc62a5f7b870))

* Correct session example ([`01969c2`](https://github.com/python-gitlab/python-gitlab/commit/01969c21391c61c915f39ebda8dfb758400a45f2))

* Implement MR-level approvals

Fixes #323 ([`59a19ca`](https://github.com/python-gitlab/python-gitlab/commit/59a19ca36c6790e3c813cb2742efdf8c5fdb122e))

* Add push rules tests ([`8df6de9`](https://github.com/python-gitlab/python-gitlab/commit/8df6de9ea520e08f1e142ae962090a0a9499bfaf))

*  Add project push rules configuration  (#520) ([`2c22a34`](https://github.com/python-gitlab/python-gitlab/commit/2c22a34ef68da190520fac4b326144061898e0cc))

* [docs] projects.all() doesn&#39;t exist in v4

Fixes #526 ([`617aa64`](https://github.com/python-gitlab/python-gitlab/commit/617aa64c8066ace4be4bbc3f510f27d3a0519daf))

* Pull mirroring doesn&#39;t return data ([`b610d66`](https://github.com/python-gitlab/python-gitlab/commit/b610d6629f926623344e2393a184958a83af488a))

* Add support for Project.pull_mirror (EE) ([`ebd6217`](https://github.com/python-gitlab/python-gitlab/commit/ebd6217853de7e7b6a140bbdf7e8779b5a40b861))

* Add support for board creation/deletion (EE) ([`f4c4e52`](https://github.com/python-gitlab/python-gitlab/commit/f4c4e52fd8962638ab79429a49fd4a699048bafc))

* Add support for LDAP groups ([`d6a61af`](https://github.com/python-gitlab/python-gitlab/commit/d6a61afc0c599a85d74947617cb13ab39b4929fc))

* Merge pull request #514 from jouve/generator

make as_list=False work for all=True queries ([`a6512f9`](https://github.com/python-gitlab/python-gitlab/commit/a6512f9efcf50db1354bbd903526b78d8e766ae1))

* make as_list work for all queries ([`8e78761`](https://github.com/python-gitlab/python-gitlab/commit/8e787612fa77dc945a4c1327e9faa6eee10c48f2))

* Add support for issue links (EE)

Fixes #422 ([`8873eda`](https://github.com/python-gitlab/python-gitlab/commit/8873edaeebd18d6b2ed08a8609c011ad29249b48))

* Add geo nodes API support

Fixes #524 ([`39c8ad5`](https://github.com/python-gitlab/python-gitlab/commit/39c8ad5a9405469370e429548e08aa475797b92b))

* Merge branch &#39;master&#39; of github.com:python-gitlab/python-gitlab ([`5a855fd`](https://github.com/python-gitlab/python-gitlab/commit/5a855fdb7f9eadc00e8b917d43a601fdc45d514a))

* Merge pull request #522 from beyondliu/master

fix #521 change post_data default value to None ([`6dd8774`](https://github.com/python-gitlab/python-gitlab/commit/6dd8774e1fa62e6f29cd760509e0274f4205683f))

* fix #521 change post_data default value to None ([`d4c1a8c`](https://github.com/python-gitlab/python-gitlab/commit/d4c1a8ce8f0b0a9d60922e22cdc044343fe24cd3))

* Add basic testing forr EE endpoints

Today we don&#39;t have a solution for easily deploying an EE instance so
using the functional tools is not possible.

This patch provides a testing script that needs to be run against a
private EE instance. ([`c88333b`](https://github.com/python-gitlab/python-gitlab/commit/c88333bdd89df81d469018c76025d01fba2eaba9))

* Add support for project-level MR approval configuration ([`473dc6f`](https://github.com/python-gitlab/python-gitlab/commit/473dc6f50d27b2e5349bb2e7c8bc07b48e9834d1))

* Merge pull request #519 from jouve/silence

silence logs/warnings in unittests ([`bbefb99`](https://github.com/python-gitlab/python-gitlab/commit/bbefb9936a18909d28d0f81b6ce99d4981ab8148))

* silence logs/warnings in unittests ([`3fa24ea`](https://github.com/python-gitlab/python-gitlab/commit/3fa24ea8f5af361f39f1fb56ec911d381b680943))

* Merge pull request #517 from jouve/dedup

projectpipelinejob was defined twice ([`92ca5c4`](https://github.com/python-gitlab/python-gitlab/commit/92ca5c4f9e2c3a8651761c9b13a290df669d62a4))

* projectpipelinejob was defined twice ([`17d9354`](https://github.com/python-gitlab/python-gitlab/commit/17d935416033778c06ed89cbd9fb6990bd20d47c))

* Use python 2 on travis for now ([`33c2457`](https://github.com/python-gitlab/python-gitlab/commit/33c245771bba81b7ab778da8df6faf12d4259e08))

* tests: default to python 3

Fix the bytes/str issues ([`b3df26e`](https://github.com/python-gitlab/python-gitlab/commit/b3df26e4247fd4af04a753d17e81efed5aa77ec7))

* Make ProjectCommitStatus.create work with CLI

Fixes #511 ([`34c8a03`](https://github.com/python-gitlab/python-gitlab/commit/34c8a03462e4ac9e3a7cf7f591ec19d17ac6e0bc))

* time_stats(): use an existing attribute if available

A time_stats attribute is returned by GitLab when fetching issues and
merge requests (on reasonably recent GitLab versions). Use this info
instead of making a new API call if possible.

Fixes #510 ([`f2223e2`](https://github.com/python-gitlab/python-gitlab/commit/f2223e2397aebd1a805bae25b0d6a5fc58519d5d))

* Update time stats docs ([`f8e6b13`](https://github.com/python-gitlab/python-gitlab/commit/f8e6b13a2ed8d022ef206de809546dcc0318cd08))

* Fix the IssueManager path to avoid redirections ([`eae1805`](https://github.com/python-gitlab/python-gitlab/commit/eae18052c0abbee5b38fca793ec2f804ec2e6c61))

* Add support for group badges

Also consolidate project/group badges tests, and add some docs

Fixes #469 ([`9412a5d`](https://github.com/python-gitlab/python-gitlab/commit/9412a5ddb1217368e0ac19fc06a4ff32711b931f))

* Merge pull request #507 from Miouge1/badges

Add support for Project badges ([`01a41ef`](https://github.com/python-gitlab/python-gitlab/commit/01a41efd271dd08d4b5744473fb71a67d9f5dea5))

* Add support for Project badges ([`e00cad4`](https://github.com/python-gitlab/python-gitlab/commit/e00cad4f73c43d28799ec6e79e32fd03e58e79b4))

* Add support for the gitlab CI lint API ([`40b9f4d`](https://github.com/python-gitlab/python-gitlab/commit/40b9f4d62d5b9853bfd63317d8ad578b4525e665))

* Update the settings attributes ([`0cc9828`](https://github.com/python-gitlab/python-gitlab/commit/0cc9828fda25531a57010cb310f23d3c185e63a6))

* Implement runner token validation ([`71368e7`](https://github.com/python-gitlab/python-gitlab/commit/71368e7292b0e6d0f0dab9039983fa35689eeab0))

* Runners can be created (registered) ([`782875a`](https://github.com/python-gitlab/python-gitlab/commit/782875a4d04bf3ebd9a0ae43240aadcde02a24f5))

* Implement runner jobs listing ([`0be81cb`](https://github.com/python-gitlab/python-gitlab/commit/0be81cb8f48b7497a05ec7d1e7cf0a1b6eb045a1))

* Add missing project attributes ([`096d9ec`](https://github.com/python-gitlab/python-gitlab/commit/096d9ecde6390a4d2795d0347280ccb2c1517143))

* Add pipeline listing filters ([`51718ea`](https://github.com/python-gitlab/python-gitlab/commit/51718ea7fb566d8ebeb310520c8e6557e19152e0))

* Update MR attributes ([`2332904`](https://github.com/python-gitlab/python-gitlab/commit/23329049110d0514e497704021a5d20ebc56d31e))

* Implement the markdown rendering API

Testing will be enable when GitLab 11.0 is available. ([`9be50be`](https://github.com/python-gitlab/python-gitlab/commit/9be50be98468e78400861718202f48eddfa83839))

* Add support for group boards ([`fbd2010`](https://github.com/python-gitlab/python-gitlab/commit/fbd2010e09f0412ea52cd16bb26cf988836bc03f))

* Fix the participants() decorator ([`8374bcc`](https://github.com/python-gitlab/python-gitlab/commit/8374bcc341eadafb8c7fbb2920d7f001a5a43b63))

* Issues: add missing attributes and methods ([`e901f44`](https://github.com/python-gitlab/python-gitlab/commit/e901f440d787c1fd43fdba1838a1f37066329ccf))

* Update some group attributes ([`4ec8975`](https://github.com/python-gitlab/python-gitlab/commit/4ec8975982290f3950d629f0fd7c73f351ead84f))

* Add feature flags deletion support ([`f082568`](https://github.com/python-gitlab/python-gitlab/commit/f082568b9a09f117cd88dd18e7582a620540ff95))

* Add support for environment stop() ([`9c19e06`](https://github.com/python-gitlab/python-gitlab/commit/9c19e06dbb792308d2fcd4fff1239043981b5f61))

* deploy key: add missing attributes ([`6779616`](https://github.com/python-gitlab/python-gitlab/commit/677961624fbc5ab190e581ae89c9f0317ac3029e))

* Deployment: add list filters ([`ce7911a`](https://github.com/python-gitlab/python-gitlab/commit/ce7911a858c17c1cf1363daca2c650d66c66dd4b))

* Add commit.merge_requests() support ([`c19ad90`](https://github.com/python-gitlab/python-gitlab/commit/c19ad90b488edabc47e3a5a5d477a3007eecaa69))

* Enable mr.participant test ([`3c53f7f`](https://github.com/python-gitlab/python-gitlab/commit/3c53f7fb8d9c0f829fbbc87acc7c83590a11b467))

* Implement commit.refs() ([`32569ea`](https://github.com/python-gitlab/python-gitlab/commit/32569ea27d36c7341b031f11d14f79fd6abd373f))

* Add missing docs file ([`63a4c7c`](https://github.com/python-gitlab/python-gitlab/commit/63a4c7c95112f6c6aed6e9fa6cf4afd88f0b80e7))

* Implement user_agent_detail for snippets

Add a new UserAgentDetail mixin to avoid code duplication. ([`7025743`](https://github.com/python-gitlab/python-gitlab/commit/70257438044b793a42adce791037b9b86ae35d9b))

* Add support for merged branches deletion ([`590ea0d`](https://github.com/python-gitlab/python-gitlab/commit/590ea0da7e5617c42e705c62370d6e94ff46ea74))

* Add support for the discussions API

Fixes #501 ([`4461139`](https://github.com/python-gitlab/python-gitlab/commit/4461139b4ace84368ccd595a459d51f9fd81b7a1))

* Document the global per_page setting ([`660f0cf`](https://github.com/python-gitlab/python-gitlab/commit/660f0cf546d18b28883e97c1182984593bbae643))

* Merge pull request #505 from jouve/config_per_page

add per_page config option ([`d981904`](https://github.com/python-gitlab/python-gitlab/commit/d9819042acde6cb30cbac3ef8f4fefa15a282459))

* add per_page config option ([`589a9aa`](https://github.com/python-gitlab/python-gitlab/commit/589a9aad58383b98b5321db106e77afa0a9a761b))

* Add support for the search API

Fixes #470 ([`97c8619`](https://github.com/python-gitlab/python-gitlab/commit/97c8619c5b07abc714417d6e5be2f553270b54a6))

* Add support for project import/export

Fixes #471 ([`b5f9616`](https://github.com/python-gitlab/python-gitlab/commit/b5f9616f21b7dcdf166033d0dba09b3dd2289849))

* pep8 fix ([`42007ec`](https://github.com/python-gitlab/python-gitlab/commit/42007ec651e6203f608484e6de899907196a808f))

* Add support for user avatar upload

Fixes #308 ([`174185b`](https://github.com/python-gitlab/python-gitlab/commit/174185bd45abb7c99cf28432a227660023d53632))

* travis-ci: remove the v3 tests ([`175abe9`](https://github.com/python-gitlab/python-gitlab/commit/175abe950c9f08dc9f66de21b20e7f4df5454517))

* [docs] update the sphinx extension for v4 objects ([`194ed0b`](https://github.com/python-gitlab/python-gitlab/commit/194ed0b87c2a24a7f5bf8c092ab745b317031ad3))

* [docs] Rework the examples pages

* Get rid of the .py files and bring all the python examples in the RST
files
* Fix a few things ([`5292ffb`](https://github.com/python-gitlab/python-gitlab/commit/5292ffb366f97e4dc611dfd49a1dca7d1e934f4c))

* Add release notes for 1.5 ([`2c34237`](https://github.com/python-gitlab/python-gitlab/commit/2c342372814bbac2203d7b4c0f2cd32541bab979))

* Drop GetFromListMixin ([`09d1ec0`](https://github.com/python-gitlab/python-gitlab/commit/09d1ec04e52fc796cc25e1e29e73969c595e951d))

* Drop API v3 support

Drop the code, the tests, and update the documentation. ([`fe89b94`](https://github.com/python-gitlab/python-gitlab/commit/fe89b949922c028830dd49095432ba627d330186))

* ChangeLog: fix link ([`7011694`](https://github.com/python-gitlab/python-gitlab/commit/701169441194bf0441cee13f2ab5784ffad7a207))

* Prepare the 1.4.0 release ([`3ad706e`](https://github.com/python-gitlab/python-gitlab/commit/3ad706eefb60caf34b4db3e9c04bbd119040f0db))

* pep8 fix ([`e6ecf65`](https://github.com/python-gitlab/python-gitlab/commit/e6ecf65c5f0bd3f95a47af6bbe484af9bbd68ca6))

* Deprecate GetFromListMixin

This mixin provides a workaround for get() for GitLab objects that don&#39;t
implement a &#39;get a single object&#39; API. We are now getting conflicts
because GitLab adds GET methods, and this is against the &#34;Implement only
what exists in the API&#34; strategy.

Also use the proper GET API call for objects that support it. ([`a877514`](https://github.com/python-gitlab/python-gitlab/commit/a877514d565a1273fe21e81d1d00e1ed372ece4c))

* longer docker image startup timeout for tests ([`5335788`](https://github.com/python-gitlab/python-gitlab/commit/5335788480d840566d745d39deb85895a5fc93af))

* Add docs for the `files` arg in http_* ([`79c4682`](https://github.com/python-gitlab/python-gitlab/commit/79c4682549aa589644b933396f53c4fd60ec8dc7))

* Merge pull request #500 from ericfrederich/efficient_get

More efficient .get() for group members. ([`66d8f30`](https://github.com/python-gitlab/python-gitlab/commit/66d8f3075e0812b36bd36bbd99d0dbd88b0ff1d7))

* More efficient .get() for group members.

Fixes #499 ([`dabfeb3`](https://github.com/python-gitlab/python-gitlab/commit/dabfeb345289f85c884b08c50a10f4c909ad24d9))

* api-usage: bit more detail for listing with `all` ([`4cc9739`](https://github.com/python-gitlab/python-gitlab/commit/4cc9739f600321b3117953b083a86a4e4c306b2f))

* prepare release notes for 1.4 ([`68b798b`](https://github.com/python-gitlab/python-gitlab/commit/68b798b96330db70c94a7aba7bb96c6cdab8718c))

* [tests] fix functional tests for python3

Fixes #486 ([`3dc997f`](https://github.com/python-gitlab/python-gitlab/commit/3dc997ffba46a6e0666b9b3416ce50ce3ad71959))

* [docs] update service.available() example for API v4

Fixes #482 ([`6d4ef0f`](https://github.com/python-gitlab/python-gitlab/commit/6d4ef0fcf04a5295c9601b6f8268a27e3bfce198))

* [docs] add a code example for listing commits of a MR

Fixes #491 ([`037585c`](https://github.com/python-gitlab/python-gitlab/commit/037585cc84cf7b4780b3f20449aa1969e24f1ed9))

* [docs] move mr samples in rst file ([`a643763`](https://github.com/python-gitlab/python-gitlab/commit/a643763224f98295132665054eb5bdad62dbf54d))

* Merge pull request #484 from Matusf/docs-example-raises-attribute-error

Change method for getting content of snippet ([`85f2388`](https://github.com/python-gitlab/python-gitlab/commit/85f238846071724c9323df06fdc757de2b453608))

* Add API v3 example ([`5c16c8d`](https://github.com/python-gitlab/python-gitlab/commit/5c16c8d03c39d4b6d87490a36102cdd4d2ad2160))

* Change method for getting content of snippet ([`505c749`](https://github.com/python-gitlab/python-gitlab/commit/505c74907fca52d315b273033e3d62643623425b))

* Fix URL encoding on branch methods

Fixes #493 ([`736fece`](https://github.com/python-gitlab/python-gitlab/commit/736fece2219658ff446ea31ee3c03dfe18ecaacb))

* Merge pull request #488 from siemens/feat/rate-limit

feat: obey the rate limit ([`86a8251`](https://github.com/python-gitlab/python-gitlab/commit/86a825143fdae82d231c2c3589d81b26c8c3ab81))

* Revert &#34;Token scopes are a list&#34;

This reverts commit 32b399af0e506b38a10a2c625338848a03f0b35d. ([`25ed8e7`](https://github.com/python-gitlab/python-gitlab/commit/25ed8e73f352b7f542a418c4ca2c802e3d90d06f))

* Merge pull request #483 from ToonMeynen/patch-2

Update projects.py documentation ([`2b9ae5c`](https://github.com/python-gitlab/python-gitlab/commit/2b9ae5ce1664b97414152dfb1acb50fbcd05f95e))

* Update projects.py

Add missing attributes to file.create in order to make it work. ([`629b1e1`](https://github.com/python-gitlab/python-gitlab/commit/629b1e1c9488cea4bf853a42622dd7f182ee47ed))

* Merge pull request #481 from max-wittig/docs/fix-typo

docs(projects): fix typo ([`f3533cd`](https://github.com/python-gitlab/python-gitlab/commit/f3533cd7b4c84454a78644af6f2f2c1a16bbe109))

* Fix the impersonation token deletion example

Fixes #476 ([`c5b9676`](https://github.com/python-gitlab/python-gitlab/commit/c5b9676687964709282bf4c3390dfda40d2fb0f4))

* [docs] Move notes examples in their own file

Fixes #472 ([`f980707`](https://github.com/python-gitlab/python-gitlab/commit/f980707d5452d1f73f517bbaf91f1a0c045c2172))

* Expose additional properties for Gitlab objects

* url: the URL provided by the user (from config or constructor)
* api_url: the computed base endpoint (URL/api/v?)

Fixes #474 ([`f09089b`](https://github.com/python-gitlab/python-gitlab/commit/f09089b9bcf8be0b90de62e33dd9797004790204))

* Token scopes are a list ([`32b399a`](https://github.com/python-gitlab/python-gitlab/commit/32b399af0e506b38a10a2c625338848a03f0b35d))

* [docs] fix GitLab refernce for notes ([`33b2b1c`](https://github.com/python-gitlab/python-gitlab/commit/33b2b1c0d2c88213a84366d1051a5958ad4e2a20))

* Provide a basic issue template ([`3d8d413`](https://github.com/python-gitlab/python-gitlab/commit/3d8d4136a51ea58be5b4544acf9b01f02f34a120))

* Get rid of _sanitize_data

It was used in one class only, no need for added complexity. ([`79dc1f1`](https://github.com/python-gitlab/python-gitlab/commit/79dc1f17a65364d2d23c2d701118200b2f7cd187))

* Implement attribute types to handle special cases

Some attributes need to be parsed/modified to work with the API (for
instance lists). This patch provides two attribute types that will
simplify parts of the code, and fix some CLI bugs.

Fixes #443 ([`1940fee`](https://github.com/python-gitlab/python-gitlab/commit/1940feec3dbb099dc3d671cd14ba756e7d34b071))

* update docs copyright years ([`455a8fc`](https://github.com/python-gitlab/python-gitlab/commit/455a8fc8cab12bbcbf35f04053da84ec0ed1c5c6))

* [docs] Merge builds.rst and builds.py ([`78bb6b5`](https://github.com/python-gitlab/python-gitlab/commit/78bb6b5baf5a75482060261198c45dd3710fc98e))

* Support downloading a single artifact file

Fixes #432 ([`9080f69`](https://github.com/python-gitlab/python-gitlab/commit/9080f69d6c9242c1131ca7ff84489f2bb26bc867))

* pep8 fix ([`9cb6bbe`](https://github.com/python-gitlab/python-gitlab/commit/9cb6bbedd350a2241113fe1d731b4cfe56c19d4f))

* [cli] Fix listing of strings ([`cb8ca65`](https://github.com/python-gitlab/python-gitlab/commit/cb8ca6516befa4d3421cf734b4c72ec75ddeb654))

* Add basic unit tests for v4 CLI ([`88391bf`](https://github.com/python-gitlab/python-gitlab/commit/88391bf7cd7a8d710a62fdb835ef56f06da8a6a5))

* [cli] Restore the --help option behavior

Fixes #381 ([`7c6be94`](https://github.com/python-gitlab/python-gitlab/commit/7c6be94630d35793e58fafd38625c29779f7a09a))

* Add support for recursive tree listing

Fixes #452 ([`d35a31d`](https://github.com/python-gitlab/python-gitlab/commit/d35a31d1268c6c8edb9f8b8322c5c66cb70ea9ae))

* [cli] Allow to read args from files

With the @/file/path syntax (similar to curl) user can provide values
from attributes in files.

Fixes #448 ([`748d57e`](https://github.com/python-gitlab/python-gitlab/commit/748d57ee64036305a84301db7211b713c1995391))

* [docs] Commits: add an example of binary file creation

Binary files need to be encoded in base64.

Fixes #427 ([`c7b3f96`](https://github.com/python-gitlab/python-gitlab/commit/c7b3f969fc3fcf9d057a23638d121f51513bb13c))

* [docs] Fix the time tracking examples

Fixes #449 ([`4a2ae8a`](https://github.com/python-gitlab/python-gitlab/commit/4a2ae8ab9ca4f0e0de978f982e44371047988e5d))

* tests: increase waiting time and hope for the best ([`2e51332`](https://github.com/python-gitlab/python-gitlab/commit/2e51332f635cb0dbe7312e084a1ac7d49499cc8c))

* Merge pull request #426 from tardyp/readmixin

introduce RefreshMixin ([`ee4591d`](https://github.com/python-gitlab/python-gitlab/commit/ee4591d44fa3c998694eded7f57aada2f6ea90c2))

* introduce RefreshMixin

RefreshMixin allows to update a REST object so that you can poll on it.
This is mostly useful for pipelines and jobs, but could be set on most of other objects, with unknown usecases. ([`3424333`](https://github.com/python-gitlab/python-gitlab/commit/3424333bc98fcfc4733f2c5f1bf9a93b9a02135b))

* Merge pull request #446 from jwilk-forks/spelling

Fix typos in documentation ([`6bcc92a`](https://github.com/python-gitlab/python-gitlab/commit/6bcc92a39a9a9dd97fa7387f754474c1cc5d78dc))

* Fix typos in documentation ([`c976fec`](https://github.com/python-gitlab/python-gitlab/commit/c976fec6c1bbf8c37cc23b9c2d07efbdd39a1670))

* [cli] _id_attr is required on creation ([`e65dfa3`](https://github.com/python-gitlab/python-gitlab/commit/e65dfa30f9699292ffb911511ecd7c347a03775c))

* CLI: display_list need to support **kwargs ([`5e27bc4`](https://github.com/python-gitlab/python-gitlab/commit/5e27bc4612117abcc8d507f3201c28ea4a0c53a4))

* [cli] fix listing for json and yaml output

Fixes #438 ([`4bdce7a`](https://github.com/python-gitlab/python-gitlab/commit/4bdce7a6b6299c3d80ac602f3d917032b5eaabff))

* Merge pull request #445 from esabouraud/feature-unshare

Add support for unsharing projects with groups ([`6c08266`](https://github.com/python-gitlab/python-gitlab/commit/6c08266ee93f6a038e8f96253791b4e5793237b1))

* Add support for unsharing projects to v3 API (untested) ([`c8c4b42`](https://github.com/python-gitlab/python-gitlab/commit/c8c4b4262113860b61318706b913f45634279ec6))

* Add support for unsharing projects to v4 API ([`5fdd06e`](https://github.com/python-gitlab/python-gitlab/commit/5fdd06e1ee57e42a746aefcb96d819c0ed7835bf))

* ProjectKeys can be updated

Closes #444 ([`9a30266`](https://github.com/python-gitlab/python-gitlab/commit/9a30266d197c45b00bafd4cea2aa4ca30637046b))

* Require requests&gt;=2.4.2

Closes #441 ([`a7314ec`](https://github.com/python-gitlab/python-gitlab/commit/a7314ec1f80bbcbbb1f1a81c127570a446a408a4))

* Prepare the 1.3.0 release ([`10bd1f4`](https://github.com/python-gitlab/python-gitlab/commit/10bd1f43f59b2257e6195b290b0dc8a578b7562a))

* Add docs for pipeline schedules ([`ac123df`](https://github.com/python-gitlab/python-gitlab/commit/ac123dfe67240f25de52dc445bde93726d5862c1))

* Move the pipelines doc to builds.rst ([`d416238`](https://github.com/python-gitlab/python-gitlab/commit/d416238a73ea9f3b09fd04cbd46eeee2f231a499))

* Merge pull request #429 from Miouge1/doc-mr-labels

Add documentation about labels update ([`0cbd9c6`](https://github.com/python-gitlab/python-gitlab/commit/0cbd9c6104970660277aed7c9add33bc5289c367))

* Add documentation about labels update ([`eb5c149`](https://github.com/python-gitlab/python-gitlab/commit/eb5c149af74f064aa1512fc1c6964e9ade5bb0c0))

* pep8 fixes ([`e7546de`](https://github.com/python-gitlab/python-gitlab/commit/e7546dee1fff0265116ae96668e049100f76b66c))

* Remove pipeline schedules from v3 (not supported) ([`0a06779`](https://github.com/python-gitlab/python-gitlab/commit/0a06779f563be22d5a654eaf1423494e31c6a35d))

* Merge branch &#39;mlq-feature/pipeline-schedules&#39; ([`39a0429`](https://github.com/python-gitlab/python-gitlab/commit/39a04297d2661f82980f1b1921a3aba1ab1feb32))

* Update pipeline schedules code ([`6a87d38`](https://github.com/python-gitlab/python-gitlab/commit/6a87d38b0c5ffdfa9c78dcf5232ec78986010ce6))

* Project pipeline jobs ([`b861837`](https://github.com/python-gitlab/python-gitlab/commit/b861837b25bb45dbe40b035dff5f41898450e22b))

* Project pipeline schedules ([`34e32a0`](https://github.com/python-gitlab/python-gitlab/commit/34e32a0944b65583a57b97bf0124b8935ab49fa7))

* Project pipeline jobs ([`fd726cd`](https://github.com/python-gitlab/python-gitlab/commit/fd726cdb61a78aafb780cae56a7909e7b648e4dc))

* Project pipeline schedules ([`31eb913`](https://github.com/python-gitlab/python-gitlab/commit/31eb913be34f8dea0c4b1f8396b74bb74b32a6f0))

* Merge pull request #420 from tardyp/patch-2

make trigger_pipeline return the pipeline ([`70c779c`](https://github.com/python-gitlab/python-gitlab/commit/70c779c4243d1807323cc1afc8cbc97918c3b8fc))

* fix pep8 ([`8134f84`](https://github.com/python-gitlab/python-gitlab/commit/8134f84f96059dbde72359c414352e2dbe3535e0))

* make trigger_pipeline return the pipeline

Trigger_pipeline returns nothing, which makes it difficult to track the pipeline being trigger.

Next PR will be about updating a pipeline object to get latest status (not sure yet the best way to do it) ([`72ade19`](https://github.com/python-gitlab/python-gitlab/commit/72ade19046f47b35c1b5ad7333f11fee0dc1e56f))

* Merge pull request #419 from tardyp/patch-1

Simplify the example for streamed artifacts ([`6ea7ab7`](https://github.com/python-gitlab/python-gitlab/commit/6ea7ab73eb6be20c4e8c092044bf0efe421ce4f5))

* add a Simplified example for streamed artifacts

Going through an object adds a lot of complication.
Adding example for unzipping on the fly ([`faeb1c1`](https://github.com/python-gitlab/python-gitlab/commit/faeb1c140637ce25209e5553cab6a488c363a912))

* Default to API v4 ([`f276f13`](https://github.com/python-gitlab/python-gitlab/commit/f276f13df50132554984f989b1d3d6c5fa8cdc01))

* Gitlab can be used as context manager

Fixes #371 ([`b4f0317`](https://github.com/python-gitlab/python-gitlab/commit/b4f03173f33ed8d214ddc20b4791ec11677f6bb1))

* config: support api_version in the global section

Fixes #421 ([`29bd813`](https://github.com/python-gitlab/python-gitlab/commit/29bd81336828b72a47673c76862cb4b532401766))

* Add Gitlab and User events support

Closes #412 ([`1ca3080`](https://github.com/python-gitlab/python-gitlab/commit/1ca30807566ca3ac1bd295516a122cd75ba9031f))

* Add support for getting list of user projects

Fixes #403 ([`96a1a78`](https://github.com/python-gitlab/python-gitlab/commit/96a1a784bd0cc0d0ce9dc3a83ea3a46380adc905))

* Add support for MR participants API

Fixes #387 ([`08f19b3`](https://github.com/python-gitlab/python-gitlab/commit/08f19b3d79dd50bab5afe58fe1b3b3825ddf9c25))

* Update the groups documentation

Closes #410 ([`638da69`](https://github.com/python-gitlab/python-gitlab/commit/638da6946d0a731aee3392b9eafc610985691855))

* Fix wrong tag example

Fixes #416 ([`e957817`](https://github.com/python-gitlab/python-gitlab/commit/e95781720210b62753af4463dd6c2e5f106439c8))

* Add manager for jobs within a pipeline. (#413) ([`bdb6d63`](https://github.com/python-gitlab/python-gitlab/commit/bdb6d63d4f7423e80e51350546698764994f08c8))

* Merge pull request #408 from movermeyer/patch-1

Adding the supported version badge ([`5149651`](https://github.com/python-gitlab/python-gitlab/commit/5149651fb4d21dabfde012238abad470bb0aa9b5))

* Adding the supported version badge ([`9253661`](https://github.com/python-gitlab/python-gitlab/commit/9253661c381e9298643e689074c00b7fae831955))

* Merge pull request #409 from movermeyer/patch-2

Clarifying what compatible means ([`8a953c2`](https://github.com/python-gitlab/python-gitlab/commit/8a953c2d3ede2bdd672323621b4e72a5f660f6f5))

* Clarifying what supports means ([`b980c9f`](https://github.com/python-gitlab/python-gitlab/commit/b980c9f7db97f8d55ed50d116a1d9fcf817ebf0d))

* Prepare v1.2.0 ([`3a119cd`](https://github.com/python-gitlab/python-gitlab/commit/3a119cd6a4841fae5b2f116512830ed12b4b29f0))

* Respect content of REQUESTS_CA_BUNDLE and *_proxy envvars

Explicitly call the requests session.merge_environment_settings()
method, which will use some environment variables to setup the session
properly.

Closes #352 ([`6f50447`](https://github.com/python-gitlab/python-gitlab/commit/6f50447917f3af4ab6611d0fdf7eb9bb67ee32c5))

* Add doc for search by custom attribute ([`2e2a78d`](https://github.com/python-gitlab/python-gitlab/commit/2e2a78da9e3910bceb30bd9ac9e574b8b1425d05))

* Add support for user/group/project filter by custom attribute

Closes #367 ([`65c64eb`](https://github.com/python-gitlab/python-gitlab/commit/65c64ebc08d75092151e828fab0fa73f5fd22e45))

* Add support for project and group custom variables

implements parts of #367 ([`fa52024`](https://github.com/python-gitlab/python-gitlab/commit/fa520242b878d25e37aacfcb0d838c58d3a4b271))

* Add support for features flags

Fixes #360 ([`f5850d9`](https://github.com/python-gitlab/python-gitlab/commit/f5850d950a77b1d985fdc3d1639e2627468d3548))

* Add support for pagesdomains

Closes #362 ([`c281d95`](https://github.com/python-gitlab/python-gitlab/commit/c281d95c2f978d8d2eb1d77352babf5217d32062))

* Add supported python versions in setup.py ([`6923f11`](https://github.com/python-gitlab/python-gitlab/commit/6923f117bc20fffcb0256e7cda35534ee48b058f))

* Add support for subgroups listing

Closes #390 ([`928865e`](https://github.com/python-gitlab/python-gitlab/commit/928865ef3533401163192faa0889019bc6b0cd2a))

* Add groups listing attributes ([`81c9d1f`](https://github.com/python-gitlab/python-gitlab/commit/81c9d1f95ef710ccd2472bc9fe4267d8a8be4ae1))

* Merge pull request #406 from ericfrederich/pagination

Allow per_page to be used with generators. ([`79d2ca4`](https://github.com/python-gitlab/python-gitlab/commit/79d2ca4bcc29fa0e30a44940adb7491a84e8b573))

* Allow per_page to be used with generators.

Fixes #405 ([`3b1d1dd`](https://github.com/python-gitlab/python-gitlab/commit/3b1d1dd8b9fc80a10cf52641701f7e1e6a8277f1))

* Update groups tests

Group search in gitlab 10.3 requires a query string with more than 3
characters. Not sure if feature or bug, but let&#39;s handle it. ([`7efbc30`](https://github.com/python-gitlab/python-gitlab/commit/7efbc30b9d8cf8ea856b68ab85b9cd2340121358))

* Minor doc update (variables)

Fixes #400 ([`70e721f`](https://github.com/python-gitlab/python-gitlab/commit/70e721f1eebe5194e18abe49163181559be6897a))

* Update testing tools for /session removal ([`8ad4a76`](https://github.com/python-gitlab/python-gitlab/commit/8ad4a76a90817a38becc80d212264c91b961565b))

* Remove now-invalid test ([`5a5cd74`](https://github.com/python-gitlab/python-gitlab/commit/5a5cd74f34faa5a9f06a6608b139ed08af05dc9f))

* ProjectFile.create(): don&#39;t modify the input data

Fixes #394 ([`0a38143`](https://github.com/python-gitlab/python-gitlab/commit/0a38143da076bd682619396496fefecf0286e4a9))

* submanagers: allow having undefined parameters

This might happen in CLI context, where recursion to discover parent
attributes is not required (URL gets hardcoded)

Fix should fix the CLI CI. ([`6f36f70`](https://github.com/python-gitlab/python-gitlab/commit/6f36f707cfaafc6e565aad14346d01d637239f79))

* [docs] Add a note about password auth being removed from GitLab

Provide a code snippet demonstrating how to use cookie-based
authentication.

Fixes #380 ([`e08d3fd`](https://github.com/python-gitlab/python-gitlab/commit/e08d3fd84336c33cf7860e130d2e95f7127dc88d))

* Add missing doc file ([`93f1499`](https://github.com/python-gitlab/python-gitlab/commit/93f149919e569bdecab072b120ee6a6ea528452f))

* [docstrings] Explicitly documentation pagination arguments

Fixes #393 ([`b0ce3c8`](https://github.com/python-gitlab/python-gitlab/commit/b0ce3c80757f19a93733509360e5440c52920f48))

* mixins.py: Avoid sending empty update data to issue.save (#389) ([`0c3a6cb`](https://github.com/python-gitlab/python-gitlab/commit/0c3a6cb889473545efd0e8a17e175cb5ff652c34))

* Update project services docs for v4

Fixes #396 ([`4e048e1`](https://github.com/python-gitlab/python-gitlab/commit/4e048e179dfbe99d88672f4b5e0471b696e65ea6))

* Add support for award emojis

Fixes #361 ([`b33265c`](https://github.com/python-gitlab/python-gitlab/commit/b33265c7c235b4365c1a7b2b03ac519ba9e26fa4))

* Make todo() raise GitlabTodoError on error ([`2167409`](https://github.com/python-gitlab/python-gitlab/commit/2167409fd6388be6758ae71762af88a466ec648d))

* Add doc to get issue from iid (#321) ([`b775069`](https://github.com/python-gitlab/python-gitlab/commit/b775069bcea51c0813a57e220c387623f361c488))

* Merge pull request #382 from ptomato/subscribe-response-code

Expected HTTP response for subscribe is 201 ([`f624d2e`](https://github.com/python-gitlab/python-gitlab/commit/f624d2e642e4ebabb8d330595f3fe0fc9882add7))

* Expected HTTP response for subscribe is 201

It seems that the GitLab API gives HTTP response code 201 (&#34;created&#34;) when
successfully subscribing to an object, not 200. ([`0d5f275`](https://github.com/python-gitlab/python-gitlab/commit/0d5f275d9b23d20da45ac675da10bfd428327a2f))

* Merge pull request #374 from benjamb/typos

Fix typos in docs ([`8f3b656`](https://github.com/python-gitlab/python-gitlab/commit/8f3b656d007c95fa2fa99389aaf326a2eb998e16))

* Fix typos in docs ([`7c886de`](https://github.com/python-gitlab/python-gitlab/commit/7c886dea5e9c42c88be01ef077532202cbad65ea))

* Fix link to settings API ([`be386b8`](https://github.com/python-gitlab/python-gitlab/commit/be386b81049e84a4b9a0daeb6cbba15ddb4b041e))

* Update pagination docs for ProjectCommit

In v3 pagination starts at page 0 instead of page 1.

Fixes: #377 ([`c6c0686`](https://github.com/python-gitlab/python-gitlab/commit/c6c068629273393eaf4f7063e1e01c5f0528c4ec))

* Revert &#34;Add unit tests for mixin exceptions&#34;

This reverts commit 4ee139ad5c58006da1f9af93fdd4e70592e6daa0. ([`084b905`](https://github.com/python-gitlab/python-gitlab/commit/084b905f78046d894fc76d3ad545689312b94bb8))

* Add support for project housekeeping

Closes #368 ([`9ede652`](https://github.com/python-gitlab/python-gitlab/commit/9ede6529884e850532758ae218465c1b7584c2d4))

* Add unit tests for mixin exceptions ([`4ee139a`](https://github.com/python-gitlab/python-gitlab/commit/4ee139ad5c58006da1f9af93fdd4e70592e6daa0))

* Add a SetMixin

Use it for UserCustomAttribute, will be useful for
{Project,Group}CustomAttribute (#367) ([`a1b097c`](https://github.com/python-gitlab/python-gitlab/commit/a1b097ce1811d320322a225d22183c36125b4a3c))

* Add support for user_agent_detail (issues)

https://docs.gitlab.com/ce/api/issues.html#get-user-agent-details ([`397d677`](https://github.com/python-gitlab/python-gitlab/commit/397d67745f573f1d6bcf9399e3ee602640b019c8))

* Merge pull request #369 from Lujeni/fix_typo_projects_documentation

[docs] Bad arguments in projetcs file documentation ([`ad35482`](https://github.com/python-gitlab/python-gitlab/commit/ad35482bdeb587ec816cac4f2231b93fcdd0066a))

* [docs] Bad arguments in projetcs file documentation ([`5ee4e73`](https://github.com/python-gitlab/python-gitlab/commit/5ee4e73b81255c30d049c8649a8d5685fa4320aa))

* update user docs with gitlab URLs ([`29d8d72`](https://github.com/python-gitlab/python-gitlab/commit/29d8d72e4ef3aaf21a45954c53b9048e61736d28))

* Add support for user activities ([`44a7ef6`](https://github.com/python-gitlab/python-gitlab/commit/44a7ef6d390b534977fb14a360e551634135bc20))

* generate coverage reports with tox ([`7fadf46`](https://github.com/python-gitlab/python-gitlab/commit/7fadf4611709157343e1421e9af27ae1abb9d81c))

* typo ([`2d689f2`](https://github.com/python-gitlab/python-gitlab/commit/2d689f236b60684a98dc9c75be103c4dfc7e4aa5))

* Add support for impersonation tokens API

Closes #363 ([`8fec612`](https://github.com/python-gitlab/python-gitlab/commit/8fec612157e4c15f587c11efc98e7e339dfcff28))

* Add missing mocking on unit test ([`700e84f`](https://github.com/python-gitlab/python-gitlab/commit/700e84f3ea1a8e0f99775d02cd1a832d05d3ec8d))

* Add support for oauth and anonymous auth in config/CLI ([`0732826`](https://github.com/python-gitlab/python-gitlab/commit/07328263c317d7ee78723fee8b66f48abffcfb36))

* Rework authentication args handling

* Raise exceptions when conflicting arguments are used
* Build the auth headers when instanciating Gitlab, not on each request
* Enable anonymous Gitlab objects (#364)

Add docs and unit tests ([`e9b1583`](https://github.com/python-gitlab/python-gitlab/commit/e9b158363e5b0ea451638b1c3a660f138a24521d))

* Remove deprecated objects/methods ([`ba6e09e`](https://github.com/python-gitlab/python-gitlab/commit/ba6e09ec804bf5cea39282590bb4cb829a836873))

* Oauth token support (#357) ([`c30121b`](https://github.com/python-gitlab/python-gitlab/commit/c30121b07b1997cc11e2011fc26d45ec53372b5a))

* Merge branch &#39;master&#39; of github.com:python-gitlab/python-gitlab ([`3bc3e60`](https://github.com/python-gitlab/python-gitlab/commit/3bc3e607e3e52cc5e676f379eca31316ad9c330a))

* Merge pull request #365 from jeromerobert/master

[doc] Fix project.triggers.create example with v4 API ([`30b1c03`](https://github.com/python-gitlab/python-gitlab/commit/30b1c03efe5b1927500103f5f9e6fb5b5ad9d312))

* [doc] Fix project.triggers.create example with v4 API ([`6c5ee84`](https://github.com/python-gitlab/python-gitlab/commit/6c5ee8456d5436dcf73e0c4f0572263de7c718c5))

* Merge pull request #342 from matejzero/mattermost

Add mattermost service support ([`82897b7`](https://github.com/python-gitlab/python-gitlab/commit/82897b7c0461f069f5067de3ebf787466a6c4486))

* Add mattermost service support ([`b5e6a46`](https://github.com/python-gitlab/python-gitlab/commit/b5e6a469e7e299dfa09bac730daee48432454075))

* Add users custome attributes support ([`4fb2e43`](https://github.com/python-gitlab/python-gitlab/commit/4fb2e439803bd55868b91827a5fbaa448f1dff56))

* 1.1.0 release ([`32f7e17`](https://github.com/python-gitlab/python-gitlab/commit/32f7e17208987fa345670421c333e22ae6aced6a))

* improve comment in release notes ([`9eff543`](https://github.com/python-gitlab/python-gitlab/commit/9eff543a42014ba30cf8af099534d507f7acebd4))

* [doc] Add sample code for client-side certificates

Closes #23 ([`fa89746`](https://github.com/python-gitlab/python-gitlab/commit/fa897468cf565fb8546b47637cd9703981aedbc0))

* Module&#39;s base objects serialization (#359)

Make gitlab objects serializable

With current implementation of API v3 and v4 support, some instances
have properties of type module and are not serializable. Handle
these properties manually with setstate and getstate methods. ([`226e6ce`](https://github.com/python-gitlab/python-gitlab/commit/226e6ce9e5217367c896125a2b4b9d16afd2cf94))

* Pagination generators: expose more information

Expose the X-* pagination attributes returned by the Gitlab server when
requesting lists.

Closes #304 ([`38d4467`](https://github.com/python-gitlab/python-gitlab/commit/38d446737f45ea54136d1f03f75fbddf46c45e00))

* Add a contributed Dockerfile

Thanks oupala!

Closes #295 ([`fba7730`](https://github.com/python-gitlab/python-gitlab/commit/fba7730161c15be222a22b4618d79bb92a87ef1f))

* Fix the CLI for objects without ID (API v4)

Fixes #319 ([`9dd410f`](https://github.com/python-gitlab/python-gitlab/commit/9dd410feec4fe4e85eb735ad0007adcf06fe03cc))

* Update the repository_blob documentation

Fixes #312 ([`d415cc0`](https://github.com/python-gitlab/python-gitlab/commit/d415cc0929aed8bf95cbbb54f64d457e42d77696))

* Add support for wiki pages ([`5082879`](https://github.com/python-gitlab/python-gitlab/commit/5082879dcfbe322bb16e4c2387c25ec4f4407cb1))

* Move the ProjectManager class for readability ([`4744200`](https://github.com/python-gitlab/python-gitlab/commit/4744200d982f7fc556d1202330b218850bd232d6))

* Add support for GPG keys

Closes #355 ([`d0c4118`](https://github.com/python-gitlab/python-gitlab/commit/d0c4118020e11c3132a46fc50d3caecf9a41e7d2))

* Add support for group milestones

Closes #349 ([`aba713a`](https://github.com/python-gitlab/python-gitlab/commit/aba713a0bdbcdb5f898c5e7dcf276811bde6e99b))

* Move group related code for readability ([`cf6767c`](https://github.com/python-gitlab/python-gitlab/commit/cf6767ca90df9081b48d1b75a30d74b6afc799af))

* Update the ssl_verify docstring ([`4c3aa23`](https://github.com/python-gitlab/python-gitlab/commit/4c3aa23775f509aa1c69732ea0a66262f1f5269e))

* Project: add support for printing_merge_request_link_enabled attr

Closes #353 ([`3a8c480`](https://github.com/python-gitlab/python-gitlab/commit/3a8c4800b31981444fb8fa614e185e2b6a310954))

* ProjectFileManager: custom update() method

Closes #340 ([`fe5805f`](https://github.com/python-gitlab/python-gitlab/commit/fe5805f3b60fc97c107e1c9b0a4ff299459ca800))

* Document the Gitlab session parameter

Provide a proxy setup example.

Closes #341 ([`1b5d480`](https://github.com/python-gitlab/python-gitlab/commit/1b5d4809d8a6a5a6b130265d5ab8fb97fc725ee8))

* [docs] document `get_create_attrs` in the API tutorial ([`b23e344`](https://github.com/python-gitlab/python-gitlab/commit/b23e344c89c26dd782ec5098b65b226b3323d6eb))

* Change ProjectUser and GroupProject base class

python-gitlab shouldn&#39;t try to provide features that are not existing in
the Gitlab API: GroupProject and ProjectUser objects should not provide
unsupported API methods (no get, no create, no update).

This Closes #346 by making explicit that we don&#39;t support these
non-existant methods. ([`8c9ad29`](https://github.com/python-gitlab/python-gitlab/commit/8c9ad299a20dcd23f9da499ad5ed785814c7b32e))

* Remove support for &#34;constructor types&#34; in v4

In v3 we create objects from json dicts when it makes sense. Support for
this feature has not been kept in v4, and we didn&#39;t get requests for it
so let&#39;s drop the _constructor_types definitions. ([`32ea62a`](https://github.com/python-gitlab/python-gitlab/commit/32ea62af967e5ee0304d8e16d7000bb052a506e4))

* Snippet notes support all the CRUD methods

Fixes #343 ([`dc504ab`](https://github.com/python-gitlab/python-gitlab/commit/dc504ab815cc9ad74a6a6beaf6faa88a5d99c293))

* ProjectFileManager.create: handle / in file paths

Replace / with %2F as is done in other methods.

Fixes #339 ([`9d0a479`](https://github.com/python-gitlab/python-gitlab/commit/9d0a47987a316f9eb1bbb65c587d6fa75e4c6409))

* Add support for listing project users

https://docs.gitlab.com/ce/api/projects.html#get-project-users

Closes #328 ([`d6fa94e`](https://github.com/python-gitlab/python-gitlab/commit/d6fa94ef38c638206d1d18bbd6ddf3f56057b1ce))

* [docs] improve the labels usage documentation

Closes #329 ([`5945537`](https://github.com/python-gitlab/python-gitlab/commit/5945537c157818483a4a14138619fa6b9341e6b3))

* Drop leftover pdb call ([`316754d`](https://github.com/python-gitlab/python-gitlab/commit/316754dd8290ee80c8c197eb1eca559fce97792e))

* Tags release description: support / in tag names ([`f3f300c`](https://github.com/python-gitlab/python-gitlab/commit/f3f300c493c3a944e57b212088f5719474b98081))

* [docs] update the file upload samples

Closes #335 ([`72664c4`](https://github.com/python-gitlab/python-gitlab/commit/72664c45baa59507028aeb3986bba42c75c3cbb8))

* Make the delete() method handle / in ids

Replace the / with the HTTP %2F as is done with other methods.

Closes #337 ([`8764903`](https://github.com/python-gitlab/python-gitlab/commit/87649035230cc1161a3e8e8e648d4f65f8480ac0))

* Fix trigger variables in v4 API (#334)

Fix trigger variables in v4 API

Close #333 ([`ac430a3`](https://github.com/python-gitlab/python-gitlab/commit/ac430a3cac4be76efc02e4321f7ee88867d28712))

* Prepare the 1.0.2 release ([`9e09cf6`](https://github.com/python-gitlab/python-gitlab/commit/9e09cf618a01e2366f2ae7d66874f4697567cfc3))

* ProjectFile: handle / in path for delete() and save()

Fixes #326 ([`05656bb`](https://github.com/python-gitlab/python-gitlab/commit/05656bbe237707794e9dd1e75e453413c0cf25a5))

* Properly handle the labels attribute in ProjectMergeRequest

This should have made it into e09581fc but something went wrong
(probably a PEBCAK).

Closes #325 ([`69f1045`](https://github.com/python-gitlab/python-gitlab/commit/69f1045627d8b5a9bdc51f8b74bf4394c95c8d9f))

* [docs] remove example usage of submanagers

Closes #324 ([`9484106`](https://github.com/python-gitlab/python-gitlab/commit/94841060e3417d571226fd5e6da35d5080ac3ecb))

* 1.0.1 release ([`e5f59bd`](https://github.com/python-gitlab/python-gitlab/commit/e5f59bd065ecfc3b66d101d7093a94995a7110e2))

* Add missing doc file ([`a346f92`](https://github.com/python-gitlab/python-gitlab/commit/a346f921560e6eb52f52ed0c660ecae7fcd73b6a))

* Fix a couple listing calls to allow proper pagination

Project.repository_tree and Project.repository_contributors return
lists, so use http_list to allow users to use listing features such as
`all=True`.

Closes #314 ([`80351ca`](https://github.com/python-gitlab/python-gitlab/commit/80351caf6dec0f1f2ebaccacd88d7175676e340f))

* CommitStatus: `sha` is parent attribute

Fixes #316 ([`7d6f3d0`](https://github.com/python-gitlab/python-gitlab/commit/7d6f3d0cd5890c8a71704419e78178ca887357fe))

* Merge pull request #317 from mion00/patch-1

Fix http_get method in get artifacts and job trace ([`d321847`](https://github.com/python-gitlab/python-gitlab/commit/d321847b90ea88b66f1c01fc2798048a6a7766dc))

* Fix http_get method in get artifacts and job trace ([`bb5a1df`](https://github.com/python-gitlab/python-gitlab/commit/bb5a1df9a52c048bf2cb1ab54a4823a3bb57be9b))

* exception message: mimic v3 API ([`05da7ba`](https://github.com/python-gitlab/python-gitlab/commit/05da7ba89a4bc41b079a13a2963ce55275350c41))

* Exceptions: use a proper error message ([`e35563e`](https://github.com/python-gitlab/python-gitlab/commit/e35563ede40241a4acf3341edea7e76362a2eaec))

* Fix the labels attrs on MR and issues

Fixes #306 ([`e09581f`](https://github.com/python-gitlab/python-gitlab/commit/e09581fccba625e4a0cf9eb67de2a9471fce3b9d))

* Fix password authentication for v4

Fixes #311 ([`89bf53f`](https://github.com/python-gitlab/python-gitlab/commit/89bf53f577fa8952902179b176ae828eb5701633))

* Merge pull request #309 from mkobit/patch-1

Minor typo fix in &#34;Switching to v4&#34; documentation ([`9d6036c`](https://github.com/python-gitlab/python-gitlab/commit/9d6036cbc9b545596c83b3be0f5022cc71954aed))

* Minor typo fix in &#34;Switching to v4&#34; documentation ([`5841070`](https://github.com/python-gitlab/python-gitlab/commit/5841070dd2b4509b20124921bee8c186f1b80fc1))

* adds project upload feature (#239) ([`29879d6`](https://github.com/python-gitlab/python-gitlab/commit/29879d61d117ff7909302ed845a6a1eb13814365))

* Merge pull request #307 from RobberPhex/fix-tag-api

Fix tag api ([`fd40fce`](https://github.com/python-gitlab/python-gitlab/commit/fd40fce913fbb3cd0e3aa2fd042e20bf1d51e9d6))

* add list method ([`b537b30`](https://github.com/python-gitlab/python-gitlab/commit/b537b30ab1cff0e465d6e299c8e55740cca1ff85))

* GitlabError filled by response ([`4b36786`](https://github.com/python-gitlab/python-gitlab/commit/4b3678669efef823fdf2ecc5251d9003a806d3e1))

* Tag can get by id ([`cc249ce`](https://github.com/python-gitlab/python-gitlab/commit/cc249cede601139476a53a5da23741d7413f86a5))

* Update changelog, release notes and authors for v1.0 ([`3d8df3c`](https://github.com/python-gitlab/python-gitlab/commit/3d8df3ccb22142c4cff86ba879882b0269f1b3b6))

* Switch the version to 1.0.0

The v4 API breaks the compatibility with v3 (at the python-gitlab
level), but I believe it is for the greater good. The new code is way
easier to read and maintain, and provides more possibilities.

The v3 API will die eventually. ([`670217d`](https://github.com/python-gitlab/python-gitlab/commit/670217d4785f52aa502dce6c9c16a3d581a7719c))

* pep8 fix ([`d0e2a15`](https://github.com/python-gitlab/python-gitlab/commit/d0e2a1595c54a1481b8ca8a4de6e1c12686be364))

* Improve the docs to make v4 a first class citizen ([`60efc83`](https://github.com/python-gitlab/python-gitlab/commit/60efc83b5a00c733b5fc19fc458674709cd7f9ce))

* [v4] fix CLI for some mixin methods ([`0268fc9`](https://github.com/python-gitlab/python-gitlab/commit/0268fc91e9596b8b02c13648ae4ea94ae0540f03))

* FIX Group.tranfer_project ([`947feaf`](https://github.com/python-gitlab/python-gitlab/commit/947feaf344478fa1b81012124fedaa9de10e224a))

* tests: faster docker shutdown

Kill the test container violently, no need to wait for a proper
shutdown. ([`d8db707`](https://github.com/python-gitlab/python-gitlab/commit/d8db70768c276235007e5c794f822db7403b6d30))

* tests: default to v4 API ([`0099ff2`](https://github.com/python-gitlab/python-gitlab/commit/0099ff2cc63a5eeb523bb515a38bd9061e69d187))

* Add support for protected branches

This feature appeared in gitlab 9.5.

Fixes #299 ([`c99e399`](https://github.com/python-gitlab/python-gitlab/commit/c99e399443819024e2e44cbd437091a39641ae68))

* Merge branch &#39;group-variables&#39; ([`fcccfbd`](https://github.com/python-gitlab/python-gitlab/commit/fcccfbda6342659ae4e040901bfd0ddaeb4541d5))

* Add support for group variables ([`eb191df`](https://github.com/python-gitlab/python-gitlab/commit/eb191dfaa42eb39d9d1b5acc21fc0c4c0fb99427))

* [v4] More python functional tests ([`0e0d4ae`](https://github.com/python-gitlab/python-gitlab/commit/0e0d4aee3e73e2caf86c50bc9152764528f7725a))

* update tox/travis for CLI v3/4 tests ([`311464b`](https://github.com/python-gitlab/python-gitlab/commit/311464b71c508503d5275db5975bc10ed74674bd))

* [tests] Use -n to not use a venv ([`5210956`](https://github.com/python-gitlab/python-gitlab/commit/5210956278e8d0bd4e5676fc116851626ac89491))

* [v4] Make sudo the first argument in CLI help ([`022a0f6`](https://github.com/python-gitlab/python-gitlab/commit/022a0f68764c60fb6a2fd7493d511438037cbd53))

* Fix the v4 CLI tests (id/iid) ([`b0af946`](https://github.com/python-gitlab/python-gitlab/commit/b0af946767426ed378bbec52c02da142c9554e71))

* [v4] Fix the CLI for project files ([`cda2d59`](https://github.com/python-gitlab/python-gitlab/commit/cda2d59e13bfa48447f2a1b999a2538f6baf83f5))

* Make CLI tests work for v4 as well ([`f00562c`](https://github.com/python-gitlab/python-gitlab/commit/f00562c7682875930b505fac0b1fc7e19ab1358c))

* [v4] Use - instead of _ in CLI legacy output

This mimics the v3 behavior. ([`f762cf6`](https://github.com/python-gitlab/python-gitlab/commit/f762cf6d64823654e5b7c5beaacd232a1282ef38))

* make v3 CLI work again ([`59550f2`](https://github.com/python-gitlab/python-gitlab/commit/59550f27feaf20cfeb65511292906f99f64b6745))

* CLI: yaml and json outputs for v4

Verbose mode only works with the legacy output. Also add support for
filtering the output by defining the list of fields that need to be
displayed (yaml and json only). ([`abade40`](https://github.com/python-gitlab/python-gitlab/commit/abade405af9099a136b68d0eb19027d038dab60b))

* [v4] CLI support is back ([`9783207`](https://github.com/python-gitlab/python-gitlab/commit/9783207f4577bd572f09c25707981ed5aa83b116))

* [v4] drop unused CurrentUserManager.credentials_auth method ([`a4f0c52`](https://github.com/python-gitlab/python-gitlab/commit/a4f0c520f4250ceb228087f31f7b351f74989020))

* README: mention v4 support ([`b919555`](https://github.com/python-gitlab/python-gitlab/commit/b919555cb434005242e16161abba9ae022455b31))

* Update the objects doc/examples for v4 ([`4057644`](https://github.com/python-gitlab/python-gitlab/commit/4057644f03829e4439ec8ab1feacf90c65d976eb))

* Fix Args attribute in docstrings ([`80eab7b`](https://github.com/python-gitlab/python-gitlab/commit/80eab7b0c0682c5df99495acc4d6f71f36603cfc))

* [v4] Fix getting projects using full namespace ([`72e783d`](https://github.com/python-gitlab/python-gitlab/commit/72e783de6b6e93e24dd93f5ac28383c2893bd7a6))

* Fix URL for branch.unprotect ([`279704f`](https://github.com/python-gitlab/python-gitlab/commit/279704fb41f74bf797bf2db5be0ed5a8d7889366))

* on_http_error: properly wrap the function

This fixes the API docs. ([`4ed22b1`](https://github.com/python-gitlab/python-gitlab/commit/4ed22b1594fd16d93fcdcaab7db8c467afd41fea))

* [v4] fix the project attributes for jobs

builds_enabled and public_builds are now jobs_enabled and public_jobs. ([`d1e7cc7`](https://github.com/python-gitlab/python-gitlab/commit/d1e7cc797a379be3f434d0e275d14486f858f80e))

* Fix Gitlab.version()

The method was overwritten by the result of the call. ([`45c4aaf`](https://github.com/python-gitlab/python-gitlab/commit/45c4aaf1604b710d2b15238f305cd7ca51317895))

* Merge pull request #294 from wayfair/feature_internal_cert_configuration

Support SSL verification via internal CA bundle ([`0e70dd9`](https://github.com/python-gitlab/python-gitlab/commit/0e70dd9bfaa8025768e032820a3e0cba2da90611))

* Support SSL verification via internal CA bundle

- Also updates documentation
- See issues #204 and #270 ([`4af4748`](https://github.com/python-gitlab/python-gitlab/commit/4af47487a279f494fd3118a01d21b401cd770d2b))

* Merge pull request #278 from asfaltboy/link-docs-gitlab-token

Docs: Add link to gitlab docs on obtaining a token ([`657f011`](https://github.com/python-gitlab/python-gitlab/commit/657f0119a3e13ceb07e4d0b17fa126260a4dafc7))

* Docs: Add link to gitlab docs on obtaining a token

I find these sort of links very user friendly 😅 ([`9b8b806`](https://github.com/python-gitlab/python-gitlab/commit/9b8b8060a56465d8aade2368033172387e15527a))

* update tox/travis test envs ([`759f6ed`](https://github.com/python-gitlab/python-gitlab/commit/759f6edaf71b456cc36e9de00157385c28e2e3e7))

* Merge branch &#39;rework_api&#39; ([`3ccdec0`](https://github.com/python-gitlab/python-gitlab/commit/3ccdec04525456c906f26ee2e931607a5d0dcd20))

* Make the project services work in v4 ([`2816c1a`](https://github.com/python-gitlab/python-gitlab/commit/2816c1ae51b01214012679b74aa14de1a6696eb5))

* Fix v3 tests ([`eee39a3`](https://github.com/python-gitlab/python-gitlab/commit/eee39a3a5f1ef3bccc45b0f23009531a9bf76801))

* Update tests for list() changes ([`7592ec5`](https://github.com/python-gitlab/python-gitlab/commit/7592ec5f6948994b8f8d9e82e2ca52c05f17829d))

* remove py3.6 from travis tests ([`217dc3e`](https://github.com/python-gitlab/python-gitlab/commit/217dc3e84c8f4625686e27e1b5e498a49af1a11f))

* Restore the prvious listing behavior

Return lists by default : this makes the explicit use of pagination work
again.

Use generators only when `as_list` is explicitly set to `False`. ([`5a4aafb`](https://github.com/python-gitlab/python-gitlab/commit/5a4aafb6ec7a3927551f2ce79425c60c399addd5))

* functional tests for v4

Update the python tests for v4, and fix the problems raised when running
those tests. ([`d7c7911`](https://github.com/python-gitlab/python-gitlab/commit/d7c79113a4dd4f23789ac8adb17add590929ae53))

* Restore correct exceptions

Match the exceptions raised in v3 for v4.

Also update the doc strings with correct information. ([`c15ba3b`](https://github.com/python-gitlab/python-gitlab/commit/c15ba3b61065973da983ff792a34268a3ba75e12))

* Fix merge_when_build_succeeds attribute name

Fixes #285 ([`374a6c4`](https://github.com/python-gitlab/python-gitlab/commit/374a6c4544931a564221cccabb6abbda9e6bc558))

* Merge branch &#39;master&#39; into rework_api ([`274b3bf`](https://github.com/python-gitlab/python-gitlab/commit/274b3bffc3365eca2fd3fa10c1e7e9b49990533e))

* remove useless attributes ([`fe3a06c`](https://github.com/python-gitlab/python-gitlab/commit/fe3a06c2a6a9776c22ff9120c99b3654e02e5e50))

* Refactor the CLI

v3 and v4 CLI will be very different, so start moving things in their
own folders.

For now v4 isn&#39;t working at all. ([`e3d50b5`](https://github.com/python-gitlab/python-gitlab/commit/e3d50b5e768fd398eee4a099125b1f87618f7428))

* Add missing doc files ([`fd5ac4d`](https://github.com/python-gitlab/python-gitlab/commit/fd5ac4d5eaed1a174ba8c086d0db3ee2001ab3b9))

* typo ([`67be226`](https://github.com/python-gitlab/python-gitlab/commit/67be226cb3f5e00aef35aacfd08c63de0389a5d7))

* build submanagers for v3 only ([`ea79bdc`](https://github.com/python-gitlab/python-gitlab/commit/ea79bdc287429791e70f2e855d70cbbbe463dd3c))

* Fix GroupProject constructor ([`afe4b05`](https://github.com/python-gitlab/python-gitlab/commit/afe4b05de9833d450b9bb52f572be5663d8f4dd7))

* minor doc updates ([`6e5a6ec`](https://github.com/python-gitlab/python-gitlab/commit/6e5a6ec1f7c2993697c359b2bcab0e1324e219bc))

* Fix changelog and release notes inclusion in sdist ([`1922cd5`](https://github.com/python-gitlab/python-gitlab/commit/1922cd5d9b182902586170927acb758f8a6f614c))

* Rework documentation ([`1a7f672`](https://github.com/python-gitlab/python-gitlab/commit/1a7f67274c9175f46a76c5ae0d8bde7ca2731014))

* Remove unused future.division import

We don&#39;t do math. ([`2a0afc5`](https://github.com/python-gitlab/python-gitlab/commit/2a0afc50311c727ee3bef700553fb60924439ef4))

* add support for objects delete() ([`32c704c`](https://github.com/python-gitlab/python-gitlab/commit/32c704c7737f0699e1c6979c6b4a8798ae41e930))

* pep8 fixes ([`26c0441`](https://github.com/python-gitlab/python-gitlab/commit/26c0441a875c566685bb55a12825ae622a002e2a))

* Document switching to v4 ([`186e11a`](https://github.com/python-gitlab/python-gitlab/commit/186e11a2135ae7df759641982fd42b3bc1bb944d))

* 0.10 is old history: remove the upgrade doc ([`76e9b12`](https://github.com/python-gitlab/python-gitlab/commit/76e9b1211fd23a3565ab00be0b169d782a14dca7))

* Add laziness to get()

The goal is to create empty objects (no API called) but give access to
the managers. Using this users can reduce the number of API calls but
still use the same API to access children objects.

For example the following will only make one API call but will still get
the result right:

gl.projects.get(49, lazy=True).issues.get(2, lazy=True).notes.list()

This removes the need for more complex managers attributes (e.g.
gl.project_issue_notes) ([`61fba84`](https://github.com/python-gitlab/python-gitlab/commit/61fba8431d0471128772429b9a8921d8092fa71b))

* Drop invalid doc about raised exceptions ([`197ffd7`](https://github.com/python-gitlab/python-gitlab/commit/197ffd70814ddf577655b3fdb7865f4416201353))

* Add new event types to ProjectHook ([`a0f215c`](https://github.com/python-gitlab/python-gitlab/commit/a0f215c2deb16ce5d9e96de5b36e4f360ac1b168))

* Fix a few remaining methods ([`3488c5c`](https://github.com/python-gitlab/python-gitlab/commit/3488c5cf137b0dbe6e96a4412698bafaaa640143))

* tests for objects mixins ([`68f4114`](https://github.com/python-gitlab/python-gitlab/commit/68f411478f0d693f7d37436a9280847cb610a15b))

* Add tests for managers mixins ([`b776c5e`](https://github.com/python-gitlab/python-gitlab/commit/b776c5ee66a84f89acd4126ea729c77196e07f66))

* Basic test for GitlabList ([`f2c4a6e`](https://github.com/python-gitlab/python-gitlab/commit/f2c4a6e0e27eb5af795dd1a4281014502c1ff1e4))

* Fix GitlabList.__len__ ([`15511bf`](https://github.com/python-gitlab/python-gitlab/commit/15511bfba32685b7c67ca8886626076cdf3561ab))

* Unit tests for REST* classes ([`0d94ee2`](https://github.com/python-gitlab/python-gitlab/commit/0d94ee228b6ac1ffef4c4cac68a4e4757a6a824c))

* Merge branch &#39;rework_api&#39; of github.com:python-gitlab/python-gitlab into rework_api ([`a5b39a5`](https://github.com/python-gitlab/python-gitlab/commit/a5b39a526035c1868a39f0533f019e5e24eeb4db))

* Tests and fixes for the http_* methods ([`904c9fa`](https://github.com/python-gitlab/python-gitlab/commit/904c9fadaa892cb4a2dbd12e564841281aa86c51))

* make the tests pass ([`d0a9334`](https://github.com/python-gitlab/python-gitlab/commit/d0a933404f4acec28956e1f07e9dcc3261fae87e))

* Migrate all v4 objects to new API

Some things are probably broken. Next step is writting unit and
functional tests.

And fix. ([`6be990c`](https://github.com/python-gitlab/python-gitlab/commit/6be990cef8725eca6954e9098f83ff8f4ad202a8))

* Simplify SidekiqManager ([`230b567`](https://github.com/python-gitlab/python-gitlab/commit/230b5679ee083dc8a5f3a8deb0bef2dab0fe12d6))

* New API: handle gl.auth() and CurrentUser* classes ([`7193034`](https://github.com/python-gitlab/python-gitlab/commit/71930345be5b7a1a89f7f823a563cb6cd4bd790b))

* Add support for managers in objects for new API

Convert User* to the new REST* API. ([`5319d0d`](https://github.com/python-gitlab/python-gitlab/commit/5319d0de2fa13e6ed7c65b4d8e9dc26ccb6f18eb))

* pep8 ([`29cb0e4`](https://github.com/python-gitlab/python-gitlab/commit/29cb0e42116ad066e6aabb39362785fd61c65924))

* Move the mixins in their own module ([`0748c89`](https://github.com/python-gitlab/python-gitlab/commit/0748c8993f0afa6ca89836601a19c7aeeaaf8397))

* Rework the manager and object classes

Add new RESTObject and RESTManager base class, linked to a bunch of
Mixin class to implement the actual CRUD methods.

Object are generated by the managers, and special cases are handled in
the derivated classes.

Both ways (old and new) can be used together, migrate only a few v4
objects to the new method as a POC.

TODO: handle managers on generated objects (have to deal with attributes
in the URLs). ([`29e0bae`](https://github.com/python-gitlab/python-gitlab/commit/29e0baee39728472abd6b67822b04518c3985d97))

* pep8 again ([`b7298de`](https://github.com/python-gitlab/python-gitlab/commit/b7298dea19f37d3ae0dfb3e233f3bc7cf5bda10d))

* Add lower-level methods for Gitlab()

Multiple goals:
* Support making direct queries to the Gitlab server, without objects
  and managers.
* Progressively remove the need to know about managers and objects in
  the Gitlab class; the Gitlab should only be an HTTP proxy to the
  gitlab server.
* With this the objects gain control on how they should do requests.
  The complexities of dealing with object specifics will be moved in the
  object classes where they belong. ([`7ddbd5e`](https://github.com/python-gitlab/python-gitlab/commit/7ddbd5e5e124be1d93fbc77da7229fc80062b35f))

* Tests and fixes for the http_* methods ([`ff82c88`](https://github.com/python-gitlab/python-gitlab/commit/ff82c88df5794dbf0020989cfc52412cefc4c176))

* make the tests pass ([`f754f21`](https://github.com/python-gitlab/python-gitlab/commit/f754f21dd9138142b923cf3b919187a4638b674a))

* Migrate all v4 objects to new API

Some things are probably broken. Next step is writting unit and
functional tests.

And fix. ([`f418767`](https://github.com/python-gitlab/python-gitlab/commit/f418767ec94c430aabd132d189d1c5e9e2370e68))

* Simplify SidekiqManager ([`0467f77`](https://github.com/python-gitlab/python-gitlab/commit/0467f779eb1d2649f3626e3817531511d3397038))

* New API: handle gl.auth() and CurrentUser* classes ([`a1c9e2b`](https://github.com/python-gitlab/python-gitlab/commit/a1c9e2bce1d0df0eff0468fabad4919d0565f09f))

* Add support for managers in objects for new API

Convert User* to the new REST* API. ([`a506902`](https://github.com/python-gitlab/python-gitlab/commit/a50690288f9c03ec37ff374839d1f465c74ecf0a))

* pep8 ([`9fbdb94`](https://github.com/python-gitlab/python-gitlab/commit/9fbdb9461a660181a3a268cd398865cafd0b4a89))

* Move the mixins in their own module ([`fb5782e`](https://github.com/python-gitlab/python-gitlab/commit/fb5782e691a11aad35e57f55af139ec4b951a225))

* Rework the manager and object classes

Add new RESTObject and RESTManager base class, linked to a bunch of
Mixin class to implement the actual CRUD methods.

Object are generated by the managers, and special cases are handled in
the derivated classes.

Both ways (old and new) can be used together, migrate only a few v4
objects to the new method as a POC.

TODO: handle managers on generated objects (have to deal with attributes
in the URLs). ([`993d576`](https://github.com/python-gitlab/python-gitlab/commit/993d576ba794a29aacd56a7610e79a331789773d))

* pep8 again ([`d809fef`](https://github.com/python-gitlab/python-gitlab/commit/d809fefaf5b382f13f8f9da344320741e553ced1))

* Add lower-level methods for Gitlab()

Multiple goals:
* Support making direct queries to the Gitlab server, without objects
  and managers.
* Progressively remove the need to know about managers and objects in
  the Gitlab class; the Gitlab should only be an HTTP proxy to the
  gitlab server.
* With this the objects gain control on how they should do requests.
  The complexities of dealing with object specifics will be moved in the
  object classes where they belong. ([`c5ad540`](https://github.com/python-gitlab/python-gitlab/commit/c5ad54062ad767c0d2882f64381ad15c034e8872))

* Merge pull request #282 from velvetz7/docs_typo

Fixed repository_compare examples ([`e87835f`](https://github.com/python-gitlab/python-gitlab/commit/e87835fe02aeb174c1b0355a1733733d89b2e404))

* Changed attribution reference ([`73be8f9`](https://github.com/python-gitlab/python-gitlab/commit/73be8f9a64b8a8db39f1a9d39b7bd677e1c68b0a))

* fixed repository_compare examples ([`261db17`](https://github.com/python-gitlab/python-gitlab/commit/261db178f2e91b68f45a6535009367b56af75769))

* Fix merge_when_build_succeeds attribute name

Fixes #285 ([`67d9a89`](https://github.com/python-gitlab/python-gitlab/commit/67d9a8989b76af25fca1b5f0f82c4af5e81332eb))

* Merge pull request #286 from jonafato/python3.6

Declare support for Python 3.6 ([`cb8c1a1`](https://github.com/python-gitlab/python-gitlab/commit/cb8c1a198276cc6aa2a3ddbf52bcc3866418e9fd))

* Declare support for Python 3.6

Add Python 3.6 environments to `tox.ini` and `.travis.yml`. ([`4c916b8`](https://github.com/python-gitlab/python-gitlab/commit/4c916b893e84993369d06dee5523cd00ea6b626a))

* Merge pull request #287 from guyzmo/features/dependency_injection

Added dependency injection support for Session ([`46b7f48`](https://github.com/python-gitlab/python-gitlab/commit/46b7f488c3dcd6f2e975f69fe1a378b920721b87))

* Added dependency injection support for Session

fixes #280

Signed-off-by: Guyzmo &lt;guyzmo+github+pub@m0g.net&gt; ([`116e3d4`](https://github.com/python-gitlab/python-gitlab/commit/116e3d42c9e94c6d23128533da6c25920ff04d0f))

* Merge pull request #276 from elisarver/patch-1

Missing expires_at in GroupMembers update ([`f19681f`](https://github.com/python-gitlab/python-gitlab/commit/f19681fc0d1aeb36f56c9c7f07aac83915a59497))

* Missing expires_at in GroupMembers update

CreateAttrs was set twice in GroupMember due to possible copy-paste error. ([`d41e972`](https://github.com/python-gitlab/python-gitlab/commit/d41e9728c0f583e031313419bcf998bfdfb8688a))

* 0.21.2 release ([`19f1b1a`](https://github.com/python-gitlab/python-gitlab/commit/19f1b1a968aba7bd9604511c015e8930e5111324))

* Merge pull request #272 from astronouth7303/patch-1

Add new event types to ProjectHook ([`4ce2794`](https://github.com/python-gitlab/python-gitlab/commit/4ce2794b284647283c861d28f77a6d63ba809bc9))

* Add new event types to ProjectHook

These are being returned in the live API, but can&#39;t set them. ([`1a58f7e`](https://github.com/python-gitlab/python-gitlab/commit/1a58f7e522bb4784e2127582b2d46d6991a8f2a9))

* Fixed spelling mistake (#269) ([`2b1e0f0`](https://github.com/python-gitlab/python-gitlab/commit/2b1e0f0041ae04134d38a5db47cc301aa757d7ea))

* import urlencode() from six.moves.urllib.parse instead of from urllib (#268)

Fixes AttributeError on Python 3, as `urlencode` function has been moved to `urllib.parse` module.

`six.moves.urllib.parse.urlencode()` is an py2.py3 compatible alias of `urllib.parse.urlencode()` on Python 3, and of `urllib.urlencode()` on Python 2. ([`88900e0`](https://github.com/python-gitlab/python-gitlab/commit/88900e06761794442716c115229bd1f780cfbcef))

* Prepare for v4 API testing ([`38bff3e`](https://github.com/python-gitlab/python-gitlab/commit/38bff3eb43ee6526b3e3b35c8207fac9ef9bc9d9))

* [v4] Make project issues work properly

* Use iids instead of ids
* Add required duration argument for time_estimate() and
  add_spent_time() ([`ac3aef6`](https://github.com/python-gitlab/python-gitlab/commit/ac3aef64d8d1275a457fc4164cafda85c2a42b1a))

* Remove extra_attrs argument from _raw_list (unneeded) ([`f3b2855`](https://github.com/python-gitlab/python-gitlab/commit/f3b28553aaa5e4e71df7892ea6c34fcc8dc61f90))

* pep8 fix ([`0663184`](https://github.com/python-gitlab/python-gitlab/commit/06631847a7184cb22e28cd170c034a4d6d16fe8f))

* Fix python functional tests ([`f733ffb`](https://github.com/python-gitlab/python-gitlab/commit/f733ffb1c1ac2243c14c660bfac98443c1a7e67c))

* [v4] Make MR work properly

* Use iids instead of ids (Fixes #266)
* Add required duration argument for time_estimate() and
  add_spent_time() ([`1ab9ff0`](https://github.com/python-gitlab/python-gitlab/commit/1ab9ff06027a478ebedb7840db71cd308da65161))

* install doc: use sudo for system commands

Fixes #267 ([`a3b8858`](https://github.com/python-gitlab/python-gitlab/commit/a3b88583d05274b5e858ee0cd198f925ad22d4d0))

* Changelog update ([`4bf251c`](https://github.com/python-gitlab/python-gitlab/commit/4bf251cf94d902e919bfd5a75f5a9bdc4e8bf9dc))

* Update API docs for v4 ([`1ac66bc`](https://github.com/python-gitlab/python-gitlab/commit/1ac66bc8c36462c8584d80dc730f6d32f3ec708a))

* Fix broken docs examples ([`746846c`](https://github.com/python-gitlab/python-gitlab/commit/746846cda9bc18b561a6335bd4951947a74b5bf6))

* Prepare the 0.21.1 release ([`3ff7d9b`](https://github.com/python-gitlab/python-gitlab/commit/3ff7d9b70e8bf464706ab1440c87db5aba9c418f))

* move changelog and release notes at the end of index ([`d75e565`](https://github.com/python-gitlab/python-gitlab/commit/d75e565ca0d4bd44e0e0f4a108e3648e21f799b5))

* [v4] Fix the jobs manager attribute in Project ([`4f1b952`](https://github.com/python-gitlab/python-gitlab/commit/4f1b952158b9bbbd8dece1cafde16ed4e4f98741))

* Prepare the 0.21 release ([`cd9194b`](https://github.com/python-gitlab/python-gitlab/commit/cd9194baa78ec55800312661e97fc5a45ed1d659))

* update copyright years ([`ba41e5e`](https://github.com/python-gitlab/python-gitlab/commit/ba41e5e02ce638facdf7542ec8ae23fc1eb4f844))

* [v4] Add support for dockerfiles API ([`0aa38c1`](https://github.com/python-gitlab/python-gitlab/commit/0aa38c1517634b7fd3b4ba4c40c512390625e854))

* [v4] Builds have been renamed to Jobs ([`deac5a8`](https://github.com/python-gitlab/python-gitlab/commit/deac5a8808195aaf806a8a02448935b7725b5de6))

* [v4] Triggers: update object

* Add support for the description attribute
* Add ``take_ownership`` support
* Triggers now use ``id`` as identifier ([`29e735d`](https://github.com/python-gitlab/python-gitlab/commit/29e735d11af3464da56bb11da58fa6028a96546d))

* add a warning about the upcoming v4 as default ([`5ea7f84`](https://github.com/python-gitlab/python-gitlab/commit/5ea7f8431fc14e4d33c2fe0babd0401f2543f2c6))

* Add v4 support to docs ([`f2b94a7`](https://github.com/python-gitlab/python-gitlab/commit/f2b94a7f2cef6ca7d5e6d87494ed3e90426d8d2b))

* Update release notes for v4 ([`627a6aa`](https://github.com/python-gitlab/python-gitlab/commit/627a6aa0620ec53dcb24a97c0e584d01dcc4d07f))

* pep8 fix ([`03ac8da`](https://github.com/python-gitlab/python-gitlab/commit/03ac8dac90a2f4e21b59b2cdd61ef1add97c445b))

* Merge branch &#39;v4_support&#39; ([`766efe6`](https://github.com/python-gitlab/python-gitlab/commit/766efe6180041f9730d2966549637754bb85d868))

* [v4] User: drop the manager filters ([`dcbb501`](https://github.com/python-gitlab/python-gitlab/commit/dcbb5015626190528a160b4bf93ba18e72c48fff))

* [v4] Remove deprecated objects methods and classes ([`8e4b65f`](https://github.com/python-gitlab/python-gitlab/commit/8e4b65fc78f47a2be658b11ae30f84da66b13c2a))

* pop8 fixes ([`441244b`](https://github.com/python-gitlab/python-gitlab/commit/441244b8d91ac0674195dbb2151570712d234d15))

* [v4] Users confirm attribute renamed skip_confirmation ([`cd98903`](https://github.com/python-gitlab/python-gitlab/commit/cd98903d6c1a2cbf21d533d6d6d4ea58917930b1))

* [v4] repository tree: s/ref_name/ref/ ([`2dd84e8`](https://github.com/python-gitlab/python-gitlab/commit/2dd84e8170502ded3fb8f9b62e0571351ad6e0be))

* [v4] Try to make the files raw() method work ([`0d1ace1`](https://github.com/python-gitlab/python-gitlab/commit/0d1ace10f160f69ed7f20d5ddaa229361641e4d9))

* [v4] Update triggers endpoint and attrs ([`0c3fe39`](https://github.com/python-gitlab/python-gitlab/commit/0c3fe39c459d27303e7765c80438e7ade0dda583))

* [v4] Milestones: iid =&gt; iids ([`449f607`](https://github.com/python-gitlab/python-gitlab/commit/449f6071feb626df893f26653d89725dd6fb818b))

* 202 is expected on some delete operations ([`b9eb10a`](https://github.com/python-gitlab/python-gitlab/commit/b9eb10a5d090b8357fab72cbc077b45e5d5df115))

* [v4] Rename the ACCESS* variables ([`cd18aee`](https://github.com/python-gitlab/python-gitlab/commit/cd18aee5c33315a880d9427a8a201c676e7b3871))

* [v4] GroupManager.search is not needed ([`9a66d78`](https://github.com/python-gitlab/python-gitlab/commit/9a66d780198c5e0abb1abd982063723fe8a16716))

* [v4] Rename the visibility attribute

Also change the value of the VISIBILITY_* consts, and move them to the
`objects` module root.

TODO: deal the numerical value used by v3. ([`27c1e95`](https://github.com/python-gitlab/python-gitlab/commit/27c1e954d8fc07325c5e156e0b130e9a4757e7ff))

* [v4] Remove public attribute for projects ([`9b625f0`](https://github.com/python-gitlab/python-gitlab/commit/9b625f07ec36a073066fa15d2fbf294bf014e62e))

* [v4] MR s/build/pipeline/ in attributes ([`9de53bf`](https://github.com/python-gitlab/python-gitlab/commit/9de53bf8710b826ffcacfb15330469d537add14c))

* [v4] Rename branch_name to branch ([`8b75bc8`](https://github.com/python-gitlab/python-gitlab/commit/8b75bc8d96878e5d058ebd5ec5c82383a0d92573))

* [v4] Update (un)subscribtion endpoints ([`90c8958`](https://github.com/python-gitlab/python-gitlab/commit/90c895824aaf84a9a77f9a3fd18db6d16b73908d))

* [v4] Update user (un)block HTTP methods ([`5c8cb29`](https://github.com/python-gitlab/python-gitlab/commit/5c8cb293bca387309b9e40fc6b1a96cc8fbd8dfe))

* [v4] Drop ProjectKeyManager.enable() ([`41f141d`](https://github.com/python-gitlab/python-gitlab/commit/41f141d84c6b2790e5d28f476fbfe139be77881e))

* [v4] Add projects.list() attributes

All the ProjectManager filter methods can now be handled by
projects.list(). ([`e789cee`](https://github.com/python-gitlab/python-gitlab/commit/e789cee1cd619e9e1b2358915936bccc876879ad))

* [v4] Update project fork endpoint ([`6684c13`](https://github.com/python-gitlab/python-gitlab/commit/6684c13a4f98b4c4b7c8a6af1957711d7cc0ae2b))

* [v4] Update the licenses templates endpoint ([`206be8f`](https://github.com/python-gitlab/python-gitlab/commit/206be8f517d9b477ee217e8102647df7efa120da))

* [v4] Update project unstar endpoint ([`76ca234`](https://github.com/python-gitlab/python-gitlab/commit/76ca2345ec3019a440696b59861d40333e2a1353))

* [v4] Update project keys endpoint ([`d71800b`](https://github.com/python-gitlab/python-gitlab/commit/d71800bb2d7ea4427da75105e7830082d2d832f0))

* [v4] Update iid attr for issues and MRs ([`9259041`](https://github.com/python-gitlab/python-gitlab/commit/92590410a0ce28fbeb984eec066d53f03d8f6212))

* [v4] projects.search() has been removed ([`af70ec3`](https://github.com/python-gitlab/python-gitlab/commit/af70ec3e2ff17385c4b72fe4d317313e94f5cb0b))

* [v4] Drop teams support ([`17dffdf`](https://github.com/python-gitlab/python-gitlab/commit/17dffdffdc638111d0652526fcaf17f373ed1ee3))

* Add missing base.py file ([`3f7e5f3`](https://github.com/python-gitlab/python-gitlab/commit/3f7e5f3e16a982e13c0d4d6bc15ebc1a153c6a8f))

* Duplicate the v3/objects.py in v4/

Using imports from v3/objects.py in v4/objects.py will have side
effects. Duplication is not the most elegant choice but v4 is the future
and v3 will die eventually. ([`3aa6b48`](https://github.com/python-gitlab/python-gitlab/commit/3aa6b48f47d6ec2b6153d56b01b4b0151212c7e3))

* Reorganise the code to handle v3 and v4 objects

Having objects managing both versions will only make the code more
complicated, with lots of tests everywhere. This solution might generate
some code duplication, but it should be maintainable. ([`e853a30`](https://github.com/python-gitlab/python-gitlab/commit/e853a30b0c083fa835513a82816b315cf147092c))

* Update Gitlab __init__ docstring ([`f373885`](https://github.com/python-gitlab/python-gitlab/commit/f3738854f0d010bade44edc60404dbab984d2adb))

* [v4] Update project search API

* projects.search() is not implemented in v4
* add the &#39;search&#39; attribute to projects.list() ([`deecf17`](https://github.com/python-gitlab/python-gitlab/commit/deecf1769ed4d3e9e2674412559413eb058494cf))

* Initial, non-functional v4 support ([`c02dabd`](https://github.com/python-gitlab/python-gitlab/commit/c02dabd25507a14d666e85c7f1ea7831c64d0394))

* Deprecate parameter related methods in gitlab.Gitlab

These methods change the auth information and URL, and might have some
unwanted side effects.

Users should create a new Gitlab instance to change the URL and
authentication information. ([`7ac1e4c`](https://github.com/python-gitlab/python-gitlab/commit/7ac1e4c1fe4ccff8c8ee4a9ae212a227d5499bce))

* Add &#39;search&#39; attribute to projects.list()

projects.search() has been deprecated by Gitlab ([`ce3dd0d`](https://github.com/python-gitlab/python-gitlab/commit/ce3dd0d1ac3fbed3cf671720e273470fb1ccdbc6))

* Update URLs to reflect the github changes ([`7def297`](https://github.com/python-gitlab/python-gitlab/commit/7def297fdf1e0d6926669a4a51cdb8519da1dca1))

* Fixed repository_tree and repository_blob path encoding (#265) ([`f3dfa6a`](https://github.com/python-gitlab/python-gitlab/commit/f3dfa6abcc0c6fba305072d368b223b102eb379f))

* MR: add support for time tracking features

Fixes #248 ([`324f81b`](https://github.com/python-gitlab/python-gitlab/commit/324f81b0869ffb8f75a0c207d12138201d01b097))

* Available services: return a list

The method returned a JSON string, which made no sense...

Fixes #258 ([`5b90061`](https://github.com/python-gitlab/python-gitlab/commit/5b90061628e50da73ec4253631e5c636413b49df))

* Make GroupProjectManager a subclass of ProjectManager

Fixes #255 ([`468246c`](https://github.com/python-gitlab/python-gitlab/commit/468246c9ffa15712f6dd9a5add4914af912bdd9c))

* Add support for nested groups (#257) ([`5afeeb7`](https://github.com/python-gitlab/python-gitlab/commit/5afeeb7810b81020f7e9caacbc263dd1fd3e20f9))

* Add support for priority attribute in labels

Fixes #256 ([`5901a1c`](https://github.com/python-gitlab/python-gitlab/commit/5901a1c4b7b82670c4283f84c4fb107ff77e0e76))

* Support milestone start date (#251) ([`9561b81`](https://github.com/python-gitlab/python-gitlab/commit/9561b81a6a9e7af4da1eba6184fc0d3f99270fdd))

* Merge pull request #249 from guikcd/patch-1

docs: s/correspnding/corresponding/ ([`f03613d`](https://github.com/python-gitlab/python-gitlab/commit/f03613dd045daf3800fed3d79d8f3f3de0d33519))

* s/correspnding/corresponding/ ([`e5c7246`](https://github.com/python-gitlab/python-gitlab/commit/e5c7246d603b289fc9f5b56dfb4f7eda88bdf205))

* Feature/milestone merge requests (#247)

Added milestone.merge_requests() API ([`34c7a23`](https://github.com/python-gitlab/python-gitlab/commit/34c7a234b5c84b2f40217bea3aadc7f77129cc8d))

* Update User options for creation and update

Fixes #246 ([`9d80699`](https://github.com/python-gitlab/python-gitlab/commit/9d806995d51a9ff846b10ed95a738e5cafe9e7d2))

* Merge pull request #245 from TimNN/mr-time-stats

Add time_stats to ProjectMergeRequest ([`f05a24b`](https://github.com/python-gitlab/python-gitlab/commit/f05a24b724a414d599b27879e8fb9564491e39a7))

* add time_stats to ProjectMergeRequest ([`63a11f5`](https://github.com/python-gitlab/python-gitlab/commit/63a11f514e5f5d43450aa2d6ecd0d664eb0cfd17))

* Prepare 0.20 release ([`c545504`](https://github.com/python-gitlab/python-gitlab/commit/c545504da79bca1f26ccfc16c3bf34ef3cc0d22c))

* Merge pull request #244 from gpocentek/issue/209

Make GroupProject inherit from Project ([`20d6678`](https://github.com/python-gitlab/python-gitlab/commit/20d667840ab7097260d453e9a79b7377f216bc1c))

* Make GroupProject inherit from Project

Fixes #209 ([`380bcc4`](https://github.com/python-gitlab/python-gitlab/commit/380bcc4cce66d7b2c080f258a1acb0d14a5a1fc3))

* Stop listing if recursion limit is hit (#234) ([`989f3b7`](https://github.com/python-gitlab/python-gitlab/commit/989f3b706d97045f4ea6af69fd11233e2f54adbf))

* Provide API wrapper for cherry picking commits (#236) ([`22bf128`](https://github.com/python-gitlab/python-gitlab/commit/22bf12827387cb1719bacae6c0c745cd768eee6c))

* add &#39;delete source branch&#39; option when creating MR (#241) ([`8677f1c`](https://github.com/python-gitlab/python-gitlab/commit/8677f1c0250e9ab6b1e16da17d593101128cf057))

* Merge pull request #243 from DmytroLitvinov/fix/bug_242

Change to correct logic of functions ([`cc4fe78`](https://github.com/python-gitlab/python-gitlab/commit/cc4fe787a584501a1aa4218be4796ce88048cc1f))

* Change to correct logic of functions ([`889bbe5`](https://github.com/python-gitlab/python-gitlab/commit/889bbe57d07966f1f146245db1e62accd5b23d93))

* Implement pipeline creation API (#237) ([`8c27e70`](https://github.com/python-gitlab/python-gitlab/commit/8c27e70b821e02921dfec4f8e4c6b77b5b284009))

* Properly handle extra args when listing with all=True

Fixes #233 ([`3b38844`](https://github.com/python-gitlab/python-gitlab/commit/3b388447fecab4d86a3387178bfb2876776d7567))

* Add support for merge request notes deletion

Fixes #227 ([`e39d7ea`](https://github.com/python-gitlab/python-gitlab/commit/e39d7eaaba18a7aa5cbcb4240feb0db11516b312))

* Add DeployKey{,Manager} classes

They are the same as Key and KeyManager but the name makes more sense.

Fixes #212 ([`a3f2ab1`](https://github.com/python-gitlab/python-gitlab/commit/a3f2ab138502cf3217d1b97ae7f3cd3a4f8b324f))

* Include chanlog and release notes in docs ([`ea0759d`](https://github.com/python-gitlab/python-gitlab/commit/ea0759d71c6678b8ce65791535a9be1675d9cfab))

* Minor changelog formatting update ([`99e6f65`](https://github.com/python-gitlab/python-gitlab/commit/99e6f65fb965aefc09ecba67f7155baf2c4379a6))

* Make sure that manager objects are never overwritten

Group.projects (manager) can be replaced by a list of Project objects
when creating/updating objects. The GroupObject API is more consistent
and closer to the GitLab API, so make sure it is always used.

Fixes #209 ([`35339d6`](https://github.com/python-gitlab/python-gitlab/commit/35339d667097d8b937c1f9f2407e4c109834ad54))

* Changelog: improvements. Fixes #229 (#230)

+ change indentation so bullet points are not treated as quote
+ add links to releases
+ add dates to releases
+ use releases as headers ([`37ee7ea`](https://github.com/python-gitlab/python-gitlab/commit/37ee7ea6a9354c0ea5bd618d48b4a2a3ddbc950c))

* Time tracking (#222)

* Added gitlab time tracking features

- get/set/remove estimated time per issue
- get/set/remove time spent per issue

* Added documentation for time tracking functions ([`92151b2`](https://github.com/python-gitlab/python-gitlab/commit/92151b22b5b03b3d529caf1865a2e35738a2f3d2))

* 0.19 release ([`cd69624`](https://github.com/python-gitlab/python-gitlab/commit/cd696240ec9000ce12c4232db3436fbca58b8fdd))

* {Project,Group}Member: support expires_at attribute

Fixes #224 ([`a273a17`](https://github.com/python-gitlab/python-gitlab/commit/a273a174ea00b563d16138ed98cc723bad7b7e29))

* Handle settings.domain_whitelist, partly

The API doesn&#39;t like receiving lists, although documentation says it&#39;s
what&#39;s expected. To be investigated.

This fixes the tests. ([`41ca449`](https://github.com/python-gitlab/python-gitlab/commit/41ca4497c3e30100991db0e8c673b722e45a6f44))

* Merge pull request #216 from ExodusIntelligence/hotfix-issue_due_date-215

added due_date attribute to ProjectIssue ([`1e0ae59`](https://github.com/python-gitlab/python-gitlab/commit/1e0ae591616b297739bb5f35db6697eee88909a3))

* fixes gpocentek/python-gitlab#215 ([`58708b1`](https://github.com/python-gitlab/python-gitlab/commit/58708b186e71289427cbce8decfeab28fdf66ad6))

* Merge pull request #220 from alexwidener/master

Added pipeline_events to ProjectHook attrs ([`19c7784`](https://github.com/python-gitlab/python-gitlab/commit/19c77845a2d69bed180f175f3a98761655631d0f))

* Added pipeline_events to ProejctHook attrs

Ran tests, all passed. ([`3f98e03`](https://github.com/python-gitlab/python-gitlab/commit/3f98e0345c451a8ecb7d46d727acf7725ce73d80))

* document the dynamic aspect of objects ([`2f274bc`](https://github.com/python-gitlab/python-gitlab/commit/2f274bcd0bfb9fef2a2682445843b7804980ecf6))

* Deploy keys: rework enable/disable

The method have been moved to the keys manager class as they don&#39;t make
sens at all on the project keys themselves.

Update doc and add tests.

Fixes #196 ([`492a751`](https://github.com/python-gitlab/python-gitlab/commit/492a75121375059a66accbbbd6af433acf6d7106))

* Merge pull request #210 from comel/services-1

Add builds-email and pipelines-email services ([`dad1345`](https://github.com/python-gitlab/python-gitlab/commit/dad134556dd624243c85b5f61a40cc893357492d))

* Add builds-email and pipelines-email services ([`5cfa6fc`](https://github.com/python-gitlab/python-gitlab/commit/5cfa6fccf1a0c5c03871e1b3a4f910e25abfd854))

* deploy keys doc: fix inclusion ([`1d827bd`](https://github.com/python-gitlab/python-gitlab/commit/1d827bd50041eab2ce3871c9070a698f6762d019))

* Merge branch &#39;nutztherookie-patch-1&#39; ([`5352c36`](https://github.com/python-gitlab/python-gitlab/commit/5352c36a89566eb5efc673259de22e0ade3db54e))

* Fix install doc

it&#39;s just confusing that it would say &#34;pip&#34; again :) ([`4fba82e`](https://github.com/python-gitlab/python-gitlab/commit/4fba82eef461c5ef5829f6ce126aa393a8a56254))

* Add support for commit creation

Fixes #206 ([`ee666fd`](https://github.com/python-gitlab/python-gitlab/commit/ee666fd57e5cb100b6e195bb74228ac242d8932a))

* Add support for project runners

This API allows to enable/disable specific runners for a project, and to
list the project associated runners.

Fix #205 ([`04435e1`](https://github.com/python-gitlab/python-gitlab/commit/04435e1b13166fb45216c494f3af4d9bdb76bcaf))

* Support the scope attribute in runners.list() ([`de0536b`](https://github.com/python-gitlab/python-gitlab/commit/de0536b1cfff43c494c64930a37333529e589a94))

* Merge pull request #203 from vilhelmen/master

Update project.archive() docs ([`c538de7`](https://github.com/python-gitlab/python-gitlab/commit/c538de75f39ecc29741b961b981e3fdf0b18d317))

* Update project.archive() docs ([`e7560a9`](https://github.com/python-gitlab/python-gitlab/commit/e7560a9d07632cf4b7da8d44acbb63aa1248104a))

* Some objects need getRequires to be set to False ([`05b3abf`](https://github.com/python-gitlab/python-gitlab/commit/05b3abf99b7af987a66c549fbd66e11710d5e3e6))

* Forbid empty id for get()

Unless the class explicitly defines it&#39;s OK (getRequiresId set to True). ([`18415fe`](https://github.com/python-gitlab/python-gitlab/commit/18415fe34f44892da504ec578ea35e74f0d78565))

* prepare the 0.18 release ([`8028ec7`](https://github.com/python-gitlab/python-gitlab/commit/8028ec7807f18c928610ca1be36907bfc4c25f1f))

* sudo: always use strings

The behavior seems to have changed on recent gitlab releases and
providing an ID as int doesn&#39;t work anymore. Using a string seems to
make things work again.

Fixes #193 ([`d6c87d9`](https://github.com/python-gitlab/python-gitlab/commit/d6c87d956eaaeafe2bd4b0e65b42e1afdf0e10bb))

* Update known attributes for projects

Fixes #181 ([`3804661`](https://github.com/python-gitlab/python-gitlab/commit/3804661f2c1336eaac0648cf9d0fc47687244e02))

* Fix duplicated data in API docs

Fixes #190 ([`73990b4`](https://github.com/python-gitlab/python-gitlab/commit/73990b46d05fce5952ef9e6a6579ba1706aa72e8))

* Add functional tests for Snippet ([`d3d8baf`](https://github.com/python-gitlab/python-gitlab/commit/d3d8bafa22e271e75e92a3df205e533bfe2e7d11))

* Snippet: content() -&gt; raw()

Using the content() method causes conflicts with the API `content`
attribute. ([`064e2b4`](https://github.com/python-gitlab/python-gitlab/commit/064e2b4bb7cb4b1775a78f51ebb46a00c9733af9))

* SnippetManager: all() -&gt; public()

Rename the method to make what it does more explicit. ([`7453895`](https://github.com/python-gitlab/python-gitlab/commit/745389501281d9bcc069e86b1b41e1936132af27))

* [docs] Add doc for snippets ([`bd7d2f6`](https://github.com/python-gitlab/python-gitlab/commit/bd7d2f6d254f55fe422aa21c9e568b8d213995b8))

* Merge branch &#39;guyzmo-features/personal_snippets&#39; ([`0a4d40e`](https://github.com/python-gitlab/python-gitlab/commit/0a4d40eeb77ddaba39f320ed5ceaad65374b9bda))

* Merge branch &#39;features/personal_snippets&#39; of https://github.com/guyzmo/python-gitlab into guyzmo-features/personal_snippets ([`26c8a0f`](https://github.com/python-gitlab/python-gitlab/commit/26c8a0f25707dafdf772d1e7ed455ee065b7e277))

* Added support for Snippets (new API in Gitlab 8.15)

cf [Gitlab-CE MR !6373](https://gitlab.com/gitlab-org/gitlab-ce/merge_requests/6373)

Signed-off-by: Guyzmo &lt;guyzmo+github@m0g.net&gt; ([`6022dfe`](https://github.com/python-gitlab/python-gitlab/commit/6022dfec44c67f7f45b0c3274f5eef02e8ac93f0))

* [CLI] Fix wrong use of arguments

The previous change removed undefined arguments from the args dict,
don&#39;t try to use possibly missing arguments without a fallback value. ([`b05c0b6`](https://github.com/python-gitlab/python-gitlab/commit/b05c0b67f8a024a67cdd16e83e70ced879e5913a))

* [CLI] ignore empty arguments

Gitlab 8.15 doesn&#39;t appreciate arguments with None as value. This breaks
the python-gitlab CLI.

Fixes #199 ([`f4fcf45`](https://github.com/python-gitlab/python-gitlab/commit/f4fcf4550eddf5c897e432efbc3ef605d6a8a419))

* [docs] artifacts example: open file in wb mode

Fixes #194 ([`35c6bbb`](https://github.com/python-gitlab/python-gitlab/commit/35c6bbb9dfaa49d0f080991a41eafc9dccb2e9f8))

* [docs] update pagination section

First page is page 1.

Fixes #197 ([`d86ca59`](https://github.com/python-gitlab/python-gitlab/commit/d86ca59dbe1d7f852416ec227a7d241d236424cf))

* Merge pull request #192 from galet/gitlab-8.14-jira

Fix JIRA service editing for GitLab 8.14+ ([`15d3362`](https://github.com/python-gitlab/python-gitlab/commit/15d336256c0dca756e189fb9746ab60be2d3c886))

* Add jira_issue_transition_id to the JIRA service optional fields ([`f7e6482`](https://github.com/python-gitlab/python-gitlab/commit/f7e6482f6f8e5a5893f22739ec98005846c74eec))

* Fix JIRA service editing for GitLab 8.14+

GitLab simplified the configuration for JIRA service and renamed most of
the fields. To maintain backward compatibility all mandatory fields were
moved to optional section. ([`343c131`](https://github.com/python-gitlab/python-gitlab/commit/343c131069c76fe68900d95b2a3e996e25e5c9c7))

* prepare 0.17 release ([`932ccd2`](https://github.com/python-gitlab/python-gitlab/commit/932ccd2214fc41a8274626397c4a88a3d6eef585))

* Merge pull request #186 from localmed/fix-should-remove-source-branch

Fix `should_remove_source_branch` ([`39288c8`](https://github.com/python-gitlab/python-gitlab/commit/39288c8fca774112ef1445c1281001a6190dd080))

* Fix `should_remove_source_branch` ([`ac2bf24`](https://github.com/python-gitlab/python-gitlab/commit/ac2bf240510f26c477ea02eddb0425f2afb64fcc))

* Rework requests arguments

* Factorize the code
* Don&#39;t send empty auth information to requests (Fixes #188) ([`6e5734b`](https://github.com/python-gitlab/python-gitlab/commit/6e5734bd910ef2d04122c162bac44c8843793312))

* Add support for triggering a new build

Fixes #184 ([`de05dae`](https://github.com/python-gitlab/python-gitlab/commit/de05daea0aa30e73c3a6f073bd173f23489c8339))

* CLI: add support for project all --all

Rework the extra opts definition to allow setting typed arguments.

Fixes #153 ([`f5f734e`](https://github.com/python-gitlab/python-gitlab/commit/f5f734e3a714693c9596a9f57bcb94deb8c9813e))

* Merge pull request #183 from GregoryEAllen/master

Please add these missing attrs ([`840cb89`](https://github.com/python-gitlab/python-gitlab/commit/840cb895f67b4b810eda94e9985d219e74a12397))

* Merge pull request #2 from GregoryEAllen/GregoryEAllen-patch-2

Add attr &#39;updated_at&#39; to ProjectIssue ([`f290b2b`](https://github.com/python-gitlab/python-gitlab/commit/f290b2b6e413604bc1b966266ab87f301cd0e32b))

* Add attr &#39;updated_at&#39; to ProjectIssue ([`a25fef5`](https://github.com/python-gitlab/python-gitlab/commit/a25fef5076286543a522b907c51f2c9060262867))

* Merge pull request #1 from GregoryEAllen/GregoryEAllen-patch-1

Add attr &#39;created_at&#39; to ProjectIssueNote ([`14e7ccd`](https://github.com/python-gitlab/python-gitlab/commit/14e7ccd10f04b2aa5b986580bca52f9361af4858))

* Add attr &#39;created_at&#39; to ProjectIssueNote ([`5b24122`](https://github.com/python-gitlab/python-gitlab/commit/5b2412217481b6ddf654277e0748585135a4fe64))

* Add support for templates API

Add gitlab CI and gitignores APIs

Rework the templates/license API docs ([`570e75d`](https://github.com/python-gitlab/python-gitlab/commit/570e75d5548daa971ff570a634dec0767e3ba6c0))

* Restore the Gitlab.user_projects manager ([`463893f`](https://github.com/python-gitlab/python-gitlab/commit/463893fb085becad96c0353d411b93c41dba2ab2))

* Make the manager objects create mor dynamic

For the gitlab.Gitlab object make the detection of &#34;submanagers&#34; more
dynamic. This will avoid duplication of definitions.

Update the sphinx extension to add these managers in the list of
attributes. ([`81e1c13`](https://github.com/python-gitlab/python-gitlab/commit/81e1c13e05172d86b613f13ddacc896db5ffd250))

* Implement merge requests diff support ([`92180e4`](https://github.com/python-gitlab/python-gitlab/commit/92180e47f76eaf293728cb1d463f601925404123))

* Remove deprecated methods

Also deprecate {un,}archive_() in favor of {un,}archive().

Fix #115 ([`c970a22`](https://github.com/python-gitlab/python-gitlab/commit/c970a22e933523b02f3536113ed5afc7a7e9ffe5))

* Add a &#39;report a bug&#39; link on doc ([`258aab4`](https://github.com/python-gitlab/python-gitlab/commit/258aab45e5f9a2097de61f0927e9fa561b058185))

* Implement __repr__ for gitlab objects

Fix #114 ([`1833117`](https://github.com/python-gitlab/python-gitlab/commit/1833117f40e5cbdccde3e5f75dcabc1468e68b04))

* Sphinx ext: factorize the build methods ([`7cfbe87`](https://github.com/python-gitlab/python-gitlab/commit/7cfbe872faaae1aee67893ba8e8dc39b7ee56f84))

* Fix tuples definition ([`6c0a3d9`](https://github.com/python-gitlab/python-gitlab/commit/6c0a3d9a5473c82a69a80302622fe0e63d0fb799))

* pep8 fix ([`68c09b7`](https://github.com/python-gitlab/python-gitlab/commit/68c09b7f13ed11e728bd33a6a69d1b9c43a0d402))

* API docs: add managers doc in GitlabObject&#39;s ([`20143f5`](https://github.com/python-gitlab/python-gitlab/commit/20143f58723a2e1de1eb436a414d2afd31f8ed24))

* Build managers on demand on GitlabObject&#39;s ([`e57a86b`](https://github.com/python-gitlab/python-gitlab/commit/e57a86b7b67a4dd7f684475ddba03703d169c9c6))

* Fix docstring for http_{username,password} ([`11c1425`](https://github.com/python-gitlab/python-gitlab/commit/11c14257e4c7e5d2b31f7e68df8dec1f14878fea))

* Rework the API documentation

Update the sphinx extension to add method definition in the docs. This
makes the documentation a bit more usable.

Hide attributes that should not have been exposed. They still exist in
the code but their documentation doesn&#39;t make much sense. ([`be83ff9`](https://github.com/python-gitlab/python-gitlab/commit/be83ff9c73d7d8a5807ddce305595ada2b56ba8a))

* fix line too long ([`9f7f45f`](https://github.com/python-gitlab/python-gitlab/commit/9f7f45fe2616442d4d05f46fd6d90001ffb12ee6))

* Move deploy key enable/disable to the object

To keep things consistent with other objects, action methods are
available on the object itself, not the manager. ([`c17ecc0`](https://github.com/python-gitlab/python-gitlab/commit/c17ecc09df4bec4e913d6b971672bc48ad13de28))

* Merge branch &#39;master-project-deploy-keys&#39; of https://github.com/Asher256/python-gitlab into Asher256-master-project-deploy-keys ([`0c1817f`](https://github.com/python-gitlab/python-gitlab/commit/0c1817f8be113a949218332a61655a1a835248c5))

* Project deploy key response code = 201 ([`6bedfc3`](https://github.com/python-gitlab/python-gitlab/commit/6bedfc32e1f35e21ab3f1c6f0a2cf5c66b06a95e))

* Fixing the response and project_id argument ([`72d982b`](https://github.com/python-gitlab/python-gitlab/commit/72d982b70b00f4018de3c1cac3bbf1507283aa33))

* Documentation for enable/disable deploy key functions ([`f9cb718`](https://github.com/python-gitlab/python-gitlab/commit/f9cb7184f8907de7f99009b7cce92c5c4eec2107))

* New exception for ProjectKey.enable_deploy_key and disable_deploy_key ([`61d4cac`](https://github.com/python-gitlab/python-gitlab/commit/61d4cac5c711268ef80e52404c047da2a1f415ca))

* enable/disable deploy key methos moved to the class ProjectKey() ([`fc5c52c`](https://github.com/python-gitlab/python-gitlab/commit/fc5c52ce6595784a13e9c114a2ef9b7c9aeaf39a))

* Delete is used for &#39;/projects/%s/deploy_keys/%s/disable&#39; ([`67aa795`](https://github.com/python-gitlab/python-gitlab/commit/67aa79550ab9f39071652ced840f7963ec7a3992))

* Feature: enable / disable the deploy key in a project ([`6310d71`](https://github.com/python-gitlab/python-gitlab/commit/6310d71c53558a201600bd48a174147623c99462))

* add missing files in MANIFEST.in ([`12fca84`](https://github.com/python-gitlab/python-gitlab/commit/12fca8409156b910cab0240bf77726a0b0bca1e0))

* ProjectHook: support the token attribute

Fix #170 ([`cd5f849`](https://github.com/python-gitlab/python-gitlab/commit/cd5f84967444cc07cf9e7bdfd63324ad4890b370))

* Merge pull request #178 from cgumpert/master

fix bug when retrieving changes for merge request ([`4689e73`](https://github.com/python-gitlab/python-gitlab/commit/4689e73b051fa985168cb648f49ee2dd6b6df523))

* fix bug when retrieving changes for merge request

Erroneously a merge request would return its commit when being queried for its changes. ([`34d6050`](https://github.com/python-gitlab/python-gitlab/commit/34d6050fe411c52d6653ddff7d48cfa6a0420690))

* Merge pull request #172 from xiaopeng163/master

edit doc badge url in README.rst ([`ff32514`](https://github.com/python-gitlab/python-gitlab/commit/ff325142a4461bf4ed8117c998a4100c24b49f59))

* edit doc badge url

Signed-off-by: Peng Xiao &lt;xiaoquwl@gmail.com&gt; ([`376acda`](https://github.com/python-gitlab/python-gitlab/commit/376acda7ae0688cce6ab6803d8041ea8d37d06fd))

* Don&#39;t overwrite attributes returned by the server

Fixes #171 ([`2c7a999`](https://github.com/python-gitlab/python-gitlab/commit/2c7a999f23b168f85c2b1c06296f617c626fde9d))

* README typo ([`62058f6`](https://github.com/python-gitlab/python-gitlab/commit/62058f68dab820b04381c728f40d972eb60f6612))

* Add support for the notification settings API ([`b15f17b`](https://github.com/python-gitlab/python-gitlab/commit/b15f17b6d2008ee658cf9206aa37faaf966a521b))

* Add support for broadcast messages API ([`6d3450c`](https://github.com/python-gitlab/python-gitlab/commit/6d3450c4fe4a2e592b9000be309819278f519e11))

* Add support for Gitlab.version() ([`c185fe2`](https://github.com/python-gitlab/python-gitlab/commit/c185fe27eabb602b8e75528f168bd7724b0fa0e3))

* Add support for boards API

This is not fully usable because the gitlab API has some limitations:

- not possible to create boards programmatically
- not possible to get labels ID
  (https://gitlab.com/gitlab-org/gitlab-ce/issues/23448) ([`f332907`](https://github.com/python-gitlab/python-gitlab/commit/f332907457c897ad0483a0bffce3d01503445d0b))

* Merge pull request #169 from hakkeroid/allow-iid-parameter-to-request-distinct-objects

Convert response list to single data source for iid requests ([`20fdbe8`](https://github.com/python-gitlab/python-gitlab/commit/20fdbe870f161ad7c47c7d57ebb2b6952acba8be))

* Convert response list to single data source for iid requests ([`23b5b6e`](https://github.com/python-gitlab/python-gitlab/commit/23b5b6e583c257821bea077096378df2fc20fde6))

* Merge pull request #168 from hakkeroid/pass_kwargs_to_object_factory

Pass kwargs to object factory ([`9da5d69`](https://github.com/python-gitlab/python-gitlab/commit/9da5d69002c59317ef215bfaf70db2ab5b38b490))

* Add .tox to ignore to respect default tox settings ([`cc151f3`](https://github.com/python-gitlab/python-gitlab/commit/cc151f3c1f350b0e05b2daa4cf440a6a7df8c36b))

* Pass kwargs to the object factory ([`ef69808`](https://github.com/python-gitlab/python-gitlab/commit/ef698087313bebec0fef4af5b0032f96465d723b))

* Merge pull request #165 from hakkeroid/patch-1

Fix ProjectBuild.play raising error even on success ([`5f444e4`](https://github.com/python-gitlab/python-gitlab/commit/5f444e4ddf1087a8c4081f9b8d8b3d87d36a0985))

* Fix ProjectBuild.play raises error on success

Running play on ProjectBuild raises a GitlabBuildPlayError although the request was successful. It looks like gitlab returns a 200-OK instead of 201-CREATED response and as such always raises an exception. ([`0793271`](https://github.com/python-gitlab/python-gitlab/commit/079327141d3701699d98c03a71d9ad77215dd73c))

* README: add badges for pypi and RTD ([`945cc66`](https://github.com/python-gitlab/python-gitlab/commit/945cc66b387599e572fc4f2eaea9ba7095b64b8e))

* Set version to 0.16 ([`46ea44a`](https://github.com/python-gitlab/python-gitlab/commit/46ea44acea4cbac5037cc91141aa205326448801))

* prepare the 0.16 release ([`117f7f5`](https://github.com/python-gitlab/python-gitlab/commit/117f7f584ed58f0f36b3cf6cb3a8d2a256c4aae4))

* Implement ProjectBuild.play() ([`673dc36`](https://github.com/python-gitlab/python-gitlab/commit/673dc3636e5ab6846c88cb4dac71f0690b02494d))

* Merge pull request #159 from JonathonReinhart/158-erase-build

Add ProjectBuild.erase() ([`d4a24a5`](https://github.com/python-gitlab/python-gitlab/commit/d4a24a5c4dc54ac03b917723347047e3995afcc9))

* Update docs to use ProjectBuild.erase() ([`3b3930b`](https://github.com/python-gitlab/python-gitlab/commit/3b3930b5525e7ea46afc271949f52d02adc6b5ce))

* Add ProjectBuild.erase()

We can&#39;t use the existing delete() functionality, because GitLab uses
`POST /projects/:id/builds/:build_id/erase` to erase a build. Instead of
overriding delete(), we add a separate erase() method to keep the naming
consistent, and allow potentially more fine-grained operations in the
future.

- https://docs.gitlab.com/ce/api/builds.html#erase-a-build ([`c2f45e9`](https://github.com/python-gitlab/python-gitlab/commit/c2f45e90a52cb418665c65258628d382e0725401))

* Workaround gitlab setup failure in tests

While running the functional tests in a venv, the token download
somtimes fail. Try to get it multiple times before failing. ([`7d424ae`](https://github.com/python-gitlab/python-gitlab/commit/7d424ae5a4dad41533af7add24d728c315563022))

* rework travis and tox setup ([`3371e0e`](https://github.com/python-gitlab/python-gitlab/commit/3371e0e1281a8d6dfa22e921bee98214b60c1ff1))

* Use the plural merge_requests URL everywhere

This breaks compatibility with older gitlab versions but maintaining
support for changed APIs is just too complex and time consuming. See
issue #139 if you need a workaround.

Fixes #157 ([`cb30dd1`](https://github.com/python-gitlab/python-gitlab/commit/cb30dd1d4caaba03f464cdf5751ef0336f8a6c33))

* Fix examples for file modification

Fixes #156 ([`d09eaa0`](https://github.com/python-gitlab/python-gitlab/commit/d09eaa09a106c6fbdb32a48cec01557023874ef6))

* Merge branch &#39;master&#39; of github.com:gpocentek/python-gitlab ([`6f7e499`](https://github.com/python-gitlab/python-gitlab/commit/6f7e499a93b8e80181cb8c91a5b1d63ec76f1ba0))

* Merge pull request #155 from rafaeleyng/add-only_allow_merge_if_build_succeeds

add only_allow_merge_if_build_succeeds option to project objects ([`26d97a7`](https://github.com/python-gitlab/python-gitlab/commit/26d97a736022c7f6828529920d2dbc88ecada18c))

* break lines too long ([`608ebbd`](https://github.com/python-gitlab/python-gitlab/commit/608ebbd0f50e3f526f8110d2596e1c9cae5f252b))

* add only_allow_merge_if_build_succeeds option to project objects ([`94932a0`](https://github.com/python-gitlab/python-gitlab/commit/94932a038bc6a862ecaaa1da87141b832b10ceda))

* Add support for --all in CLI

Fixes #153 ([`5860421`](https://github.com/python-gitlab/python-gitlab/commit/58604213efbe4d275be8da6615ed77d6f3510cbe))

* Merge pull request #154 from derek-austin/patch-1

Create a project in a group ([`4390afb`](https://github.com/python-gitlab/python-gitlab/commit/4390afbff39deb5a33b857342dae6ee494684ce7))

* Create a project in a group

Just a sketch, feel free to toss it and do it in the right way. ([`b057a94`](https://github.com/python-gitlab/python-gitlab/commit/b057a94e70f485b0e9d2a22572d87b975ae44002))

* Merge pull request #150 from vilhelmen/master

Add branch protection notes ([`1e1d467`](https://github.com/python-gitlab/python-gitlab/commit/1e1d467c9570f75027e45ec461e808617df6c0fa))

* Brief branch protection notes

You can pass developers_can_push and developers_can_merge to the protect function. Handy! ([`8a560c6`](https://github.com/python-gitlab/python-gitlab/commit/8a560c6ada94ec715e36b47ba722d5a128a4e154))

* Merge pull request #147 from derek-austin/derek-austin-patch-1

Missing coma concatenates array values ([`ddba752`](https://github.com/python-gitlab/python-gitlab/commit/ddba752eb20af39fa54e13a7f565108a4ad011e9))

* Missing coma concatenates array values

&#39;enabled_git_access_protocolgravatar_enabled&#39; were two distinct values in ApplicationSettings.optionalUpdateAttrs. ([`02a8bf4`](https://github.com/python-gitlab/python-gitlab/commit/02a8bf4a6fd3daceac60a869a66a014824bcad43))

* Merge branch &#39;master&#39; of github.com:gpocentek/python-gitlab ([`53f9322`](https://github.com/python-gitlab/python-gitlab/commit/53f93225ebb571f1c283ec848959975e3815e4ad))

* Merge pull request #146 from galet/add-api-url-to-jira-params

JIRA service - add api_url to optional attributes ([`d83b838`](https://github.com/python-gitlab/python-gitlab/commit/d83b8380fe87a0de88cf2e0d6ff56f95e9b83bac))

* JIRA service - add api_url to optional attributes

The api_url attribute is mandatory at least since GitLab 8.11. Otherwise
server returns gitlab.exceptions.GitlabUpdateError: 400: 400 (Bad request) &#34;api_url&#34; not given.

Keep it as optional to maintain backward compatibility with older GitLab
versions. ([`c8c43ee`](https://github.com/python-gitlab/python-gitlab/commit/c8c43ee74fa58c1011a404c2a0f296a0042451e9))

* Merge branch &#39;master&#39; of github.com:gpocentek/python-gitlab ([`2ac42d6`](https://github.com/python-gitlab/python-gitlab/commit/2ac42d623d69b5f4d1262c869657ab5971f67eca))

* Merge pull request #144 from koyaan/master

Add the ability to fork to a specific namespace ([`449830f`](https://github.com/python-gitlab/python-gitlab/commit/449830f7ddad06d035995d7d004111a1be774532))

* fix doc ([`0c1c894`](https://github.com/python-gitlab/python-gitlab/commit/0c1c8944ea100220d35afbf9e5eea40d360ca454))

* add doc ([`648dc86`](https://github.com/python-gitlab/python-gitlab/commit/648dc86dcc0fdb81dcbfa8f02c6011895ced7fc5))

* fix pep8 ([`a692d59`](https://github.com/python-gitlab/python-gitlab/commit/a692d59a1bb2a3438c115ada768471fc7a3f9e4b))

* Add the ability to fork to a specific namespace ([`4852462`](https://github.com/python-gitlab/python-gitlab/commit/48524627ee8cb0c90c6bc17a9641bcbb5364313e))

* 0.15.1 release ([`90ad2de`](https://github.com/python-gitlab/python-gitlab/commit/90ad2dec7a0b158b2e77ae0cb403b01f2e1498d4))

* Properly fix _raw_list ([`dc3dcd1`](https://github.com/python-gitlab/python-gitlab/commit/dc3dcd11f3921929cc13260fbfb13aa3ae5117ce))

* &#39;path&#39; is an existing gitlab attr, don&#39;t use it

Use path_ instead of path as parameter name for methods using it.
Otherwise it might conflict with GitlabObject attributes. ([`b815f3a`](https://github.com/python-gitlab/python-gitlab/commit/b815f3a1f58cd697b4b95f6f0b24883282e09f77))

* Fix and test pagination

Fixes #140 ([`c08c913`](https://github.com/python-gitlab/python-gitlab/commit/c08c913b82bf7421600b248d055db497d627802a))

* minor RST fix ([`47cb278`](https://github.com/python-gitlab/python-gitlab/commit/47cb27824d2e1b3d056817c45cbb2d5dca1df904))

* bump version and update changelog ([`79f46c2`](https://github.com/python-gitlab/python-gitlab/commit/79f46c24682026e319e1c9bc36267d2290c3a33e))

* Add support for project deployments ([`8d7faf4`](https://github.com/python-gitlab/python-gitlab/commit/8d7faf42b3e928ead8eb6eb58b7abf94364b53e2))

* Add support for access requests ([`40db4cd`](https://github.com/python-gitlab/python-gitlab/commit/40db4cdd24cf31fd6a192b229c132fe28e682eb8))

* Add support for project pipelines ([`8257400`](https://github.com/python-gitlab/python-gitlab/commit/8257400fd78e0fdc26fdcb207dbc6e923332e209))

* Add support for project services API ([`ef2dbf7`](https://github.com/python-gitlab/python-gitlab/commit/ef2dbf7034aee21ecf225be5cfefee8ab4379bbe))

* Remove unused ProjectTagReleaseManager class ([`ded5258`](https://github.com/python-gitlab/python-gitlab/commit/ded52580346a59e788d7c53e09d9df8ae549f60c))

* Fix canGet attribute (typo) ([`0178f3d`](https://github.com/python-gitlab/python-gitlab/commit/0178f3d05911608493224c2e79cbeeba9c1f4784))

* Remove _get_list_or_object() and its tests ([`451c174`](https://github.com/python-gitlab/python-gitlab/commit/451c17492e1399e2359c761f1fb27982e6596696))

* Let _data_for_gitlab return python data ([`a8f6fdd`](https://github.com/python-gitlab/python-gitlab/commit/a8f6fdd43bba84270ec841eb019ea5c332d26e04))

* Refactor the Gitlab class

Make use of the _raw_* methods in the CRUD methods. ([`fe96edf`](https://github.com/python-gitlab/python-gitlab/commit/fe96edf06c4a520ae6b7e67d83e100c69233cbf6))

* fix pep8 test ([`e0d226b`](https://github.com/python-gitlab/python-gitlab/commit/e0d226bab60bebd3bda28d40d0d13fa282669b9e))

* Remove method marked as deprecated 7 months ago ([`438dc2f`](https://github.com/python-gitlab/python-gitlab/commit/438dc2fa5969bc4d66d6bcbe920fbcdb8a62d3ba))

* Add copyright header to utils.py ([`83cb8c0`](https://github.com/python-gitlab/python-gitlab/commit/83cb8c0eff5ccc89d53f70174760f88ac0db7506))

* Move the constants at the gitlab root level ([`2ced9d0`](https://github.com/python-gitlab/python-gitlab/commit/2ced9d0717ee84169f9b1f190fb6694e1134572d))

* Add sidekiq metrics support ([`23b2a30`](https://github.com/python-gitlab/python-gitlab/commit/23b2a3072238546da2a2f8e48ce09db85a59feef))

* implement the todo API ([`131739f`](https://github.com/python-gitlab/python-gitlab/commit/131739f492946ba1cd58852be1caf000af451384))

* Update the ApplicationSettings attributes ([`1c53ecb`](https://github.com/python-gitlab/python-gitlab/commit/1c53ecbf8b6fcdb9335874734855ca7cab1999f6))

* Fix fork creation documentation

Fixes #136 ([`baa09fe`](https://github.com/python-gitlab/python-gitlab/commit/baa09fecb277a206aa41b22d97c60d5b230656c1))

* Run more tests in travis

Travis has some limitations so this patch sets up some tricks to run the
functional tests. ([`f82f962`](https://github.com/python-gitlab/python-gitlab/commit/f82f9623819bf0df7066545722edcc09b7d8caf0))

* ignore pep8 error ([`fa75571`](https://github.com/python-gitlab/python-gitlab/commit/fa75571a334166632ad970c32a6b995785604803))

* add a basic HTTP debug method ([`c9915a4`](https://github.com/python-gitlab/python-gitlab/commit/c9915a4e43c4e7e0e086d815aec722a370e7e0b5))

* Update changelog/authors/version for 0.14 ([`e4624c9`](https://github.com/python-gitlab/python-gitlab/commit/e4624c9f17a8fbbe57da4316e6927f6d39bcc5a3))

* MR merge(): update the object ([`799b593`](https://github.com/python-gitlab/python-gitlab/commit/799b5934d00c8ae199c5b0a6bdd18f4b0e06d223))

* MR (un)subscribe: don&#39;t fail if state doesn&#39;t change ([`d7967c6`](https://github.com/python-gitlab/python-gitlab/commit/d7967c6d0d6621faf2ce294073f04b53172877d6))

* Handle empty messages from server in exceptions ([`178bfb7`](https://github.com/python-gitlab/python-gitlab/commit/178bfb77dd33ec9a434871c7b9b34ae320bd1ce4))

* MR: fix updates ([`4a73b85`](https://github.com/python-gitlab/python-gitlab/commit/4a73b85f89a4d568938bd2785506fa3708ad5c83))

* fix labels deletion example ([`71edeeb`](https://github.com/python-gitlab/python-gitlab/commit/71edeeb12139763944e8b205080dbbcc4a4a2a75))

* Fix the listing of some resources

The parent ID wasn&#39;t available in the generated objects, leading to
exceptions when trying to use specific methods for these objects.

Fixes #132 ([`922041d`](https://github.com/python-gitlab/python-gitlab/commit/922041d1215dc00ecd633e4fc330fd991ad578bd))

* MR: get list of changes and commits ([`92edb99`](https://github.com/python-gitlab/python-gitlab/commit/92edb9922b178783f9307c84147352ae31f32d0b))

* remove debug print statement ([`4fd00f8`](https://github.com/python-gitlab/python-gitlab/commit/4fd00f8a7a879eb113e3998b1c9ef82758560235))

* Add support for project environments ([`5b08d2a`](https://github.com/python-gitlab/python-gitlab/commit/5b08d2a364d0f355c8df9e4926e5a54fc5f15f36))

* add support for global deploy key listing ([`9bd2cb7`](https://github.com/python-gitlab/python-gitlab/commit/9bd2cb70b255b5ec8c2112d186a829f78c1bb6be))

* Merge branch &#39;master&#39; of github.com:gpocentek/python-gitlab ([`e3ac32f`](https://github.com/python-gitlab/python-gitlab/commit/e3ac32f76a54e06c9c465c5acd41398988154fe9))

* doc: replace incorrect archive call() ([`e1f5e15`](https://github.com/python-gitlab/python-gitlab/commit/e1f5e1560e53019d45b113a71916ad9a7695afeb))

* document namespaces API ([`1f52cd2`](https://github.com/python-gitlab/python-gitlab/commit/1f52cd2df35dab33dbf7429c8d514443278b549a))

* add a contributing section in README ([`e6ffd69`](https://github.com/python-gitlab/python-gitlab/commit/e6ffd69bc745ce1a5b857fc248a3bef793e30138))

* Merge pull request #131 from chrwen-omicron/enable_container_registry

Added a new project attribute to enable the container registry. ([`e0f2290`](https://github.com/python-gitlab/python-gitlab/commit/e0f2290fdbbb8d2ee4c9fcb9e531b04bb69232fa))

* Added a new project attribute to enable the container registry. ([`d61510e`](https://github.com/python-gitlab/python-gitlab/commit/d61510e55f73ed328dde66f8a6c1138d554ab000))

* Add support from listing group issues ([`580f21e`](https://github.com/python-gitlab/python-gitlab/commit/580f21ea9a80bfe7062296ac7684489d5375df69))

* Docs: drop the FAQ

The only question is now documented in the API examples. ([`261f947`](https://github.com/python-gitlab/python-gitlab/commit/261f9470f457673e8082e673fb09861a993fdabc))

* Improve commit statuses and comments

Fixes #92 ([`f0fbefe`](https://github.com/python-gitlab/python-gitlab/commit/f0fbefe9f8eef4dd04afd8e98d7eed454ce75590))

* tests: don&#39;t use deprecated Content method ([`741896d`](https://github.com/python-gitlab/python-gitlab/commit/741896d5af682de01101ed4e7713b1daecaf7843))

* CLI: refactor _die() ([`99d0177`](https://github.com/python-gitlab/python-gitlab/commit/99d0177b3f4d4d08e8c021809eb01d4744ea32fd))

* doc: fix doubled parameter ([`58ddf1d`](https://github.com/python-gitlab/python-gitlab/commit/58ddf1d52d184243a40a754b80275dc3882ccacd))

* Replace Snippet.Content() with a new content() method

This new method use the standard lowercase name and implements data
streaming. ([`832ed9f`](https://github.com/python-gitlab/python-gitlab/commit/832ed9f4c23ba3cb4fba68f1083dbabfa9fe32a7))

* fix unit tests ([`3198ead`](https://github.com/python-gitlab/python-gitlab/commit/3198eadb748593de5ac803bc49926300c2849a4f))

* Groups can be updated ([`048b1cf`](https://github.com/python-gitlab/python-gitlab/commit/048b1cfbe5cb058dda088d7d0020dcd2aa49cc49))

* Add missing args in docstrings ([`075345a`](https://github.com/python-gitlab/python-gitlab/commit/075345aa3c06e0c29a2edd1dec219c445fc1f220))

* Allow to stream the downloads when appropriate

Some API calls will download possibly large data, resulting in a high
memory usage and out-of-memory errors. For these API calls use the
requests streaming capabilities and download chunked data. The caller is
responsible of providing a callable to actually store the data.

The default callable just prints the data on stdout. ([`94aea52`](https://github.com/python-gitlab/python-gitlab/commit/94aea524a23ac428259bae327a1fccdd2f5b841d))

* Implement ProjectBuild.keep_artifacts ([`e0cf1c2`](https://github.com/python-gitlab/python-gitlab/commit/e0cf1c276d16ba9a0e26853e5ac94668a5b60818))

* Gitlab: add managers for build-related resources ([`b339ed9`](https://github.com/python-gitlab/python-gitlab/commit/b339ed98ee4981dd494096f73e5e8a8eb0b6116b))

* Implement runners global API ([`6eb11fd`](https://github.com/python-gitlab/python-gitlab/commit/6eb11fd73840889a7ab244c516c235a2dc7e6867))

* Add docstring for settings manager in Gitlab class ([`52c8825`](https://github.com/python-gitlab/python-gitlab/commit/52c8825f7db7ff9a0a24a2bda6451af747822589))

* Fix pep8 test ([`63f0c4d`](https://github.com/python-gitlab/python-gitlab/commit/63f0c4d21e14b06e8a70e9b752262399e2195b31))

* implement CLI for project archive/unarchive/share ([`fc68e9b`](https://github.com/python-gitlab/python-gitlab/commit/fc68e9bbf8cf24eca4faf57997f0c7273944eabe))

* Implement sharing project with a group ([`e7c4125`](https://github.com/python-gitlab/python-gitlab/commit/e7c412510ba014f6e1cf94b725b0e24665c7b4ed))

* Fix ProjectMember update ([`2df4c9e`](https://github.com/python-gitlab/python-gitlab/commit/2df4c9e52a89de7256dacef9cb567ea1b2e056f4))

* Update ProjectSnippet attributes

&#39;visibility_level&#39; has been added as an optional attribute to keep
compatibility with older releases of gitlab.

Fixes #129 ([`3ad612d`](https://github.com/python-gitlab/python-gitlab/commit/3ad612de8753e20f7359c16e5bce4c06772c9550))

* Implement archive/unarchive for a projet

The methods are called archive_ and unarchive_ to workaround a conflict
with the deprecated archive method. Method will be renamed when the
archive method is removed. ([`7ed34ed`](https://github.com/python-gitlab/python-gitlab/commit/7ed34ed79101d0d773ecb6e638b0a4da9c3fd10c))

* Fix the Project.archive call ([`565c35e`](https://github.com/python-gitlab/python-gitlab/commit/565c35efe4a4f9c86fba37a7c764ed97788eadd4))

* Project: add VISIBILITY_* constants

They should be there instead of having them in the Group class.
Variables in Group are keeped for compatibility. ([`2457823`](https://github.com/python-gitlab/python-gitlab/commit/24578231fabf79659ed5c8277a7a9f2af856cac9))

* Implement user emails support ([`0be4761`](https://github.com/python-gitlab/python-gitlab/commit/0be4761961cf145cf66a456d910596aa32912492))

* document users API ([`9ba2d89`](https://github.com/python-gitlab/python-gitlab/commit/9ba2d8957ea2742b4a3f0e00888e544649df1ee3))

* Add branches API documentation ([`cdd801e`](https://github.com/python-gitlab/python-gitlab/commit/cdd801ecc6e685ede6db02c9da45b581c07b162e))

* Merge pull request #128 from rafaeleyng/feat/add-note-events-to-project-hook

add `note_events` to project hooks attributes ([`c88c638`](https://github.com/python-gitlab/python-gitlab/commit/c88c6381036b8ef4668222329f543bc7d058f9c6))

* add `note_events` to project hooks attributes ([`ca662e2`](https://github.com/python-gitlab/python-gitlab/commit/ca662e2d5decbc78a817544227d1efccb5392761))

* MR: add (un)subscribe support ([`867b7ab`](https://github.com/python-gitlab/python-gitlab/commit/867b7abca1cec287a413c9fb190fb5ddd9337cfc))

* Merge branch &#39;label-subscribe&#39; ([`d340d31`](https://github.com/python-gitlab/python-gitlab/commit/d340d313392e730e7147690aff0cebe2af657c89))

* Add support for label (un)subscribe ([`6f29ff1`](https://github.com/python-gitlab/python-gitlab/commit/6f29ff1727f490e41787a893a0e46c06871041ce))

* add support for namespaces ([`79feb87`](https://github.com/python-gitlab/python-gitlab/commit/79feb87bd98caac008da2337c01fd7e3624d37f6))

* milestone: optional listing attrs ([`dbad3bd`](https://github.com/python-gitlab/python-gitlab/commit/dbad3bd007aaa0e4a19a9f3bc87924018f311290))

* update ProjectLabel attributes ([`c55fd4b`](https://github.com/python-gitlab/python-gitlab/commit/c55fd4b43d6576aff3c679b701c0f5be0cb98281))

* Add support for project-issue move ([`73627a2`](https://github.com/python-gitlab/python-gitlab/commit/73627a21bc94d6c37adaa36ef3ab0475a05a46f3))

* project issue: proper update attributes ([`ca68f6d`](https://github.com/python-gitlab/python-gitlab/commit/ca68f6de561cbe5f1e528260eff30ff5943cd39e))

* issues: add missing optional listing parameters ([`60c9910`](https://github.com/python-gitlab/python-gitlab/commit/60c99108646c5913a2d477e96b78556528d25f35))

* Merge branch &#39;master&#39; of github.com:gpocentek/python-gitlab ([`2e0ac3f`](https://github.com/python-gitlab/python-gitlab/commit/2e0ac3fa4a66a63921b2aeee81dcc942a0849985))

* Merge pull request #125 from gpocentek/issue-122

Add support for build artifacts and trace ([`80a1908`](https://github.com/python-gitlab/python-gitlab/commit/80a190888028db4eb1df0c4f827938e89b20f8a1))

* Add support for build artifacts and trace

Fixes #122 ([`b3e0974`](https://github.com/python-gitlab/python-gitlab/commit/b3e0974451b49ab64866dc131bff59e5471ea620))

* issues: add optional listing parameters ([`c85276a`](https://github.com/python-gitlab/python-gitlab/commit/c85276a6e6c5088ea6f2ecb13059488c9779ea2c))

* Add support for commit comments

https://github.com/gitlabhq/gitlabhq/blob/master/doc/api/commits.md ([`412e2bc`](https://github.com/python-gitlab/python-gitlab/commit/412e2bc7e00a5229974388f795caefa1f0896273))

* commit status: optional get attrs ([`547f385`](https://github.com/python-gitlab/python-gitlab/commit/547f38501177a8d67d35e0d55ca0f2dff38f2904))

* commit status: add optional context url ([`0b8ed5a`](https://github.com/python-gitlab/python-gitlab/commit/0b8ed5a1687f3b5704b516c1a0ded458ed4a9087))

* Make GroupProject more &#34;python-gitlabish&#34; ([`68d15fd`](https://github.com/python-gitlab/python-gitlab/commit/68d15fdfd7cd92adbf54873b75c42e46f35dd918))

* Merge branch &#39;master&#39; of https://github.com/missionrulz/python-gitlab into missionrulz-master ([`69e64a3`](https://github.com/python-gitlab/python-gitlab/commit/69e64a330292d149a60f606fd262942112021f94))

* typo in doc block ([`d9b9f92`](https://github.com/python-gitlab/python-gitlab/commit/d9b9f92bfa26fc69406efd32fe1cfa7929d6b667))

* add to __init__.py &amp; move manager after class declaration ([`8f707ac`](https://github.com/python-gitlab/python-gitlab/commit/8f707acd0fc77645860c441511126e0a7a2c8a47))

* move into own class &amp; create manager class ([`eb6c26f`](https://github.com/python-gitlab/python-gitlab/commit/eb6c26f51131fa171c71c19c28448e736f2f5243))

* update docblock ([`cd13aff`](https://github.com/python-gitlab/python-gitlab/commit/cd13aff8a0df9136ba3e289fbccd85de3f159bb5))

* list projects under group ([`d4e2cd6`](https://github.com/python-gitlab/python-gitlab/commit/d4e2cd6c618d137df645c182271f67c5ae7e8ff5))

* Merge pull request #124 from Condla/master

Fix: --title is required argument, when in reality optional ([`18de4ef`](https://github.com/python-gitlab/python-gitlab/commit/18de4ef22f5f801dd721d76d0721c5b4cd459c37))

* Fix --title is not a required argument anymore ([`899490b`](https://github.com/python-gitlab/python-gitlab/commit/899490b04055029196eff9e03b496131e2238e61))

* Fix that --title is a required argument, when trying to update a ProjectMilestone ([`bea8ea9`](https://github.com/python-gitlab/python-gitlab/commit/bea8ea9d0fa921cc5c4fdd1b948420f1f780770c))

* Fix --title is not a required argument anymore ([`c24f0d9`](https://github.com/python-gitlab/python-gitlab/commit/c24f0d9a3664c025e3284e056d5b4c007dcf5435))

* Merge pull request #121 from PeterMosmans/httpauthextended

Added HTTPauth support for even more methods :) ([`422b163`](https://github.com/python-gitlab/python-gitlab/commit/422b163075189eca466077c7320b466ab39f331e))

* pylint fix ([`40d7969`](https://github.com/python-gitlab/python-gitlab/commit/40d796988171967570d485d7ab709ad6ea466ecf))

* Added HTTPauth support for even more methods :) ([`59ed4fc`](https://github.com/python-gitlab/python-gitlab/commit/59ed4fc07947d80352f1656c5d8a280cddec8b0f))

* add HTTP auth options to doc ([`6220308`](https://github.com/python-gitlab/python-gitlab/commit/62203086b04264f04cf6e6681e132ed355bb9b87))

* Merge pull request #120 from PeterMosmans/basicauth

Added support for HTTP basic authentication ([`11f1e2d`](https://github.com/python-gitlab/python-gitlab/commit/11f1e2dfb746d1e28ceb1115fe02e45cb44df7f6))

* Added support for HTTP basic authentication ([`e9e48b9`](https://github.com/python-gitlab/python-gitlab/commit/e9e48b9188e00298573bb2f407a854c8bf8a6dff))

* project issue: doc and CLI for (un)subscribe ([`1b14f5c`](https://github.com/python-gitlab/python-gitlab/commit/1b14f5c9b1ff0af083abedff80eafb9adcae629c))

* Merge pull request #118 from IvicaArsov/issues_subscribe_unsubscribe

Add support for subscribe and unsubscribe in issues ([`7bbbfbd`](https://github.com/python-gitlab/python-gitlab/commit/7bbbfbdc534a4d26aa61b1b4287911c9f7c6f8a5))

* Add support for subscribe and unsubscribe in issues ([`d42687d`](https://github.com/python-gitlab/python-gitlab/commit/d42687db9f0c58ea8a08532fbf6c524b0cc5ed17))

* Merge branch &#39;master&#39; of github.com:gpocentek/python-gitlab ([`b8f19ca`](https://github.com/python-gitlab/python-gitlab/commit/b8f19ca9f64b737296782e74816f4b0b88a05d2f))

* Merge pull request #110 from chrwen-omicron/remove_next_url_from_cls_kwargs

Remove &#39;next_url&#39; from kwargs before passing it to the cls constructor. ([`05dd8dc`](https://github.com/python-gitlab/python-gitlab/commit/05dd8dc353fb5ebcb04cad72db19a8e08e0f7c56))

* Remove &#39;next_url&#39; from kwargs before passing it to the cls constructor.

The &#39;next_url&#39; argument causes problems in the _construct_url method if it
doesn&#39;t belong there. E.g. if you list all projects, change an attribute
of a project and then try to save it, the _construct_url will use the
&#39;next_url&#39; from the list method and the save will fail. ([`c261875`](https://github.com/python-gitlab/python-gitlab/commit/c261875cf167e6858d052dc983fb0dcb03e3ea40))

* version bump ([`0535808`](https://github.com/python-gitlab/python-gitlab/commit/0535808d5a82ffbcd5a7ea23ecc4d0c22dad34a1))

* update changelog and authors ([`57936af`](https://github.com/python-gitlab/python-gitlab/commit/57936af70758f35ea28ad060c4ead2d916a3b47e))

* Manage optional parameters for list() and get()

* List these elements in the API doc
* Implement for License objects ([`fd45397`](https://github.com/python-gitlab/python-gitlab/commit/fd4539715da589df5a81b333e71875289687922d))

* fix pep8 tests ([`417d27c`](https://github.com/python-gitlab/python-gitlab/commit/417d27cf7c9569d5057dcced5481a6b9c8dfde2a))

* implement list/get licenses ([`62e4fb9`](https://github.com/python-gitlab/python-gitlab/commit/62e4fb9b09efbf9080a6787bcbde09067a9b83ef))

* Merge branch &#39;master&#39; of github.com:gpocentek/python-gitlab ([`ee1620b`](https://github.com/python-gitlab/python-gitlab/commit/ee1620bcfe0533b70c9ceebb34968d3633e2613c))

* Merge pull request #113 from adamreid/master

Enable updates on ProjectIssueNotes ([`f5c75cb`](https://github.com/python-gitlab/python-gitlab/commit/f5c75cbf05ded3a326db6050c11dbdf67b5eca99))

* Merge branch &#39;master&#39; of https://github.com/gpocentek/python-gitlab ([`8edd7f7`](https://github.com/python-gitlab/python-gitlab/commit/8edd7f79050559062ac119797329d0a8dba57a06))

* Remove unnecessary canUpdate property from ProjectIssuesNote ([`111b7d9`](https://github.com/python-gitlab/python-gitlab/commit/111b7d9a4ee60176714b950d7ed9da86c6051feb))

* Enable updates on ProjectIssueNotes ([`5fe7e27`](https://github.com/python-gitlab/python-gitlab/commit/5fe7e27bb16a06271f87bf19473b8604df92b4f7))

* implement star/unstar for projects ([`1de6b7e`](https://github.com/python-gitlab/python-gitlab/commit/1de6b7e7641f2c0cb101a82385cee569aa786e3f))

* Deprecate Project.archive() ([`24c283f`](https://github.com/python-gitlab/python-gitlab/commit/24c283f5861f21e51489afc815bd9f31bff58bee))

* Rename some methods to better match the API URLs

Also deprecate the file_* methods in favor of the files manager. ([`45adb6e`](https://github.com/python-gitlab/python-gitlab/commit/45adb6e4dbe7667376639d68078754d6d72cb55c))

* ProjectFile: file_path is required for deletion ([`8ce8218`](https://github.com/python-gitlab/python-gitlab/commit/8ce8218e2fb155c933946d9959a9b53f6a905d21))

* Rework the Gitlab.delete method

Fixes #107 ([`0a1bb94`](https://github.com/python-gitlab/python-gitlab/commit/0a1bb94b58bfcf837f846be7bd4d4075ab16eea6))

* Revert &#34;enable python 3.5 tests for travis&#34;

This reverts commit 1915519f449f9b751aa9cd6bc584472602b58f36. ([`c3f5b3a`](https://github.com/python-gitlab/python-gitlab/commit/c3f5b3ac14c1767a5b65e7771496990f5ce6b9f0))

* Rework merge requests update

Fixes #76 ([`aff99b1`](https://github.com/python-gitlab/python-gitlab/commit/aff99b13fdfcfb68e8c9ae45d817d5ec20752626))

* enable python 3.5 tests for travis ([`1915519`](https://github.com/python-gitlab/python-gitlab/commit/1915519f449f9b751aa9cd6bc584472602b58f36))

* Enable deprecation warnings for gitlab only

Fixes #96 ([`d204e66`](https://github.com/python-gitlab/python-gitlab/commit/d204e6614d29d60a5d0790dde8f26d3efe78b9e8))

* Add new optional attributes for projects

Fixes #116 ([`f12c732`](https://github.com/python-gitlab/python-gitlab/commit/f12c732f5e0dff7db1048adf50f54bfdd63ca6fc))

* Drop the next_url attribute when listing

Fixes #106 ([`64af398`](https://github.com/python-gitlab/python-gitlab/commit/64af39818d02af1b40644d71fd047d6bc3f6e69e))

* Implement project contributors ([`1600770`](https://github.com/python-gitlab/python-gitlab/commit/1600770e1d01aaaa90dbfd602e073e4e4a578fc1))

* Implement project compare

Fixes #112 ([`250f348`](https://github.com/python-gitlab/python-gitlab/commit/250f34806b1414b5346b4eaf268eb2537d8017de))

* Add support for Project raw_blob ([`7a8f81b`](https://github.com/python-gitlab/python-gitlab/commit/7a8f81b32e47dab6da495f5cefffe48566934744))

* Merge pull request #108 from guyzmo/using_requests_session

Adding a Session instance for all HTTP requests ([`23e8146`](https://github.com/python-gitlab/python-gitlab/commit/23e8146a391e4269e9b3d57a553148963d412179))

* Adding a Session instance for all HTTP requests

The session instance will make it easier for setting up once headers, including
the authentication payload, and it&#39;s also making it easier to override HTTP queries
handling, when using [betamax](https://github.com/sigmavirus24/betamax) for recording
and replaying the test suites. ([`858352b`](https://github.com/python-gitlab/python-gitlab/commit/858352b9a337471401dd2c8d9552c13efab625e6))

* Add missing group creation parameters

description and visibility_level are optional parameters for group
creation. ([`61bc24f`](https://github.com/python-gitlab/python-gitlab/commit/61bc24fd341e53718f8b9c06c3ac1bbcd55d2530))

* Add deletion support for issues and MR

This is supported in gitlabhq master branch for admin users (soft
deletion). ([`9a9a4c4`](https://github.com/python-gitlab/python-gitlab/commit/9a9a4c41c02072bd7fad18f75702ec7bb7407ac6))

* add &#34;external&#34; parameter for users ([`349f66e`](https://github.com/python-gitlab/python-gitlab/commit/349f66e2959ae57c3399f44edf09da8a775067ce))

* MR: add support for closes_issues ([`571a382`](https://github.com/python-gitlab/python-gitlab/commit/571a382f0595ea7cfd5424b1e4f5009fcb531642))

* MR: add support for cancel_merge_when_build_succeeds ([`f6a51d6`](https://github.com/python-gitlab/python-gitlab/commit/f6a51d67c38c883775240d8c612d492bf023c2e4))

* minor docs fixes ([`ccbea3f`](https://github.com/python-gitlab/python-gitlab/commit/ccbea3f59a1be418ea5adf90d25dbfb49f72dfde))

* Add support for MergeRequest validation

Both API and CLI support this feature.

fixes #105 ([`43e8a2a`](https://github.com/python-gitlab/python-gitlab/commit/43e8a2a82deff4c95e156fc951f88ff6e95cf7b8))

* Update changelog and authors ([`bb463ae`](https://github.com/python-gitlab/python-gitlab/commit/bb463ae4e0ed79e472c0d594f76dc8177a29fb5c))

* version bump ([`754d5e5`](https://github.com/python-gitlab/python-gitlab/commit/754d5e5f66ac86baba02e7d63157c263510ec593))

* Gitlab.update(): use the proper attributes if defined ([`f8528cc`](https://github.com/python-gitlab/python-gitlab/commit/f8528cce8d79b13e90e1f87b56c8cdbe30b2067e))

* add a note about project search API ([`e48e4ac`](https://github.com/python-gitlab/python-gitlab/commit/e48e4aca9650b241d1f1e038fdcab125b7c95656))

* Merge branch &#39;master&#39; of github.com:gpocentek/python-gitlab ([`e46c188`](https://github.com/python-gitlab/python-gitlab/commit/e46c18898deb8579d4fee0e76bfc17abed12c512))

* Merge pull request #98 from Asher256/fix-unicode-syntax-py3

Fix the &#39;invalid syntax&#39; on Python 3.2, because of u&#39;password&#39; ([`aea678b`](https://github.com/python-gitlab/python-gitlab/commit/aea678b9398f87b6943f005ff207755aa8a982a4))

* Fix the &#39;invalid syntax&#39; on Python 3.2, because of u&#39;password&#39;

More informations regarding this issue:

Operating system: Debian Wheezy, with Python 3.2 and the last
version of python-gitlab.

The gitlab module raised this exception, because of the &#39;u&#39; (Unicode):

Traceback (most recent call last):
  File &#34;push_settings.py&#34;, line 14, in &lt;module&gt;
    from helper import ROOT_EMAIL, ADMINS, git, old_git
  File &#34;/opt/scripts/gitlab/helpers/helper.py&#34;, line 25, in &lt;module&gt;
    from gitlab import Gitlab
  File &#34;/opt/scripts/gitlab/helpers/gitlab/__init__.py&#34;, line 32, in &lt;module&gt;
    from gitlab.objects import *  # noqa
  File &#34;/opt/scripts/gitlab/helpers/gitlab/objects.py&#34;, line 546
    selfdict.pop(u&#39;password&#39;, None)
			   ^
SyntaxError: invalid syntax
It is a recent change:
01802c0 (Richard Hansen 2016-02-11 22:43:25 -0500 546) selfdict.pop(u&#39;password&#39;, None)
01802c0 (Richard Hansen 2016-02-11 22:43:25 -0500 547) otherdict.pop(u&#39;password&#39;, None)

To solve the issue, &#39;u&#39; was removed. ([`7ed84a7`](https://github.com/python-gitlab/python-gitlab/commit/7ed84a7b4ca73d1b0cc6be7db0c43958ff9f4c47))

* pep8 ignore H803 errors (git messages) ([`86ade4a`](https://github.com/python-gitlab/python-gitlab/commit/86ade4ac78fd14cc8f12be39c74ff60688a2fcf7))

* Re-implement _custom_list in the Gitlab class

Rename the method _raw_list. This adds support for the ``all=True``
option to enable automatic recursion and avoid pagination if requested
by the user.

Fixes #93 ([`453224a`](https://github.com/python-gitlab/python-gitlab/commit/453224aaf64c37196b7211de8dd4a60061954987))

* remove unused _returnClass attribute ([`44d0dc5`](https://github.com/python-gitlab/python-gitlab/commit/44d0dc54fb7edf7de4e50ca34d430fe734c0e8cc))

* CI: implement user get-by-username

fixes #95 ([`58433d2`](https://github.com/python-gitlab/python-gitlab/commit/58433d2b1854eb4e112c499d52d8dd0fd6dba094))

* CLI: fix discovery of method to execute ([`7260684`](https://github.com/python-gitlab/python-gitlab/commit/7260684d11e8ffe02461f761b6677d039b703a8d))

* Improve the doc for UserManager

Describe parameters, return values and exceptions for search() and
get_by_username(). ([`b79af1d`](https://github.com/python-gitlab/python-gitlab/commit/b79af1d8a8515a419267a8f8e8937c9134bcea3a))

* Implement &#34;user search&#34; CLI ([`073d8d5`](https://github.com/python-gitlab/python-gitlab/commit/073d8d5d84efa64ad2a13f8dc405e51840f47585))

* Merge branch &#39;rhansen-get-specific-user&#39; ([`6975ac6`](https://github.com/python-gitlab/python-gitlab/commit/6975ac64e8037044245005d57b8165d920e1b8cc))

* define UserManager.get_by_username() to get a user by username ([`ac2e534`](https://github.com/python-gitlab/python-gitlab/commit/ac2e534fb811f3c1295c742e74dcb14a3c1ff0c1))

* define UserManager.search() to search for users ([`8f59516`](https://github.com/python-gitlab/python-gitlab/commit/8f59516a4d7d5c6c654e8c2531092e217d13a4be))

* define GitlabObject.__eq__() and __ne__() equivalence methods ([`01802c0`](https://github.com/python-gitlab/python-gitlab/commit/01802c0ceb7c677ea0eb9c6a1b2382048b9fed86))

* define GitlabObject.as_dict() to dump object as a dict ([`f15a7cf`](https://github.com/python-gitlab/python-gitlab/commit/f15a7cfd7edbbc55ff4fb5d41995dee033517963))

* Merge pull request #89 from ExodusIntelligence/master

Adding new `ProjectHook` attributes: ([`81be3cf`](https://github.com/python-gitlab/python-gitlab/commit/81be3cf181f5e49ef20c2824eb8c48785f4ab922))

* Added missing comma ([`1f81c2d`](https://github.com/python-gitlab/python-gitlab/commit/1f81c2d7a93cc7c719bf8bda627020946aa975d3))

* Adding new `ProjectHook` attributes:

* `build_events`
* `enable_ssl_verification`

See the two links below:

* https://github.com/gitlabhq/gitlabhq/blob/master/doc/api/projects.md#add-project-hook
* https://github.com/pyapi-gitlab/pyapi-gitlab/pull/173 ([`db9bbf6`](https://github.com/python-gitlab/python-gitlab/commit/db9bbf6528e792976e80f870b2013199569a0021))

* Add a coverage tox env ([`2e1f84e`](https://github.com/python-gitlab/python-gitlab/commit/2e1f84ede56b73c5b6857515d24d061a60b509fb))

* Add some unit tests for CLI

Reorganize the cli.py code to ease the testing. ([`d2e30da`](https://github.com/python-gitlab/python-gitlab/commit/d2e30da81cafcff4295b067425b2d03e3fdf2556))

* Rework the CLI code

Add support for more subcommands. ([`8aa8d8c`](https://github.com/python-gitlab/python-gitlab/commit/8aa8d8cd054710e79d45c71c86eaf4358a152d7c))

* Merge pull request #90 from ms-boom/fix_custom_list

fix GitlabObject creation in _custom_list ([`f5ca0eb`](https://github.com/python-gitlab/python-gitlab/commit/f5ca0ebe2baca508462a4835dfca33f7c5d02d29))

* fix GitlabObject creation in _custom_list ([`293a9dc`](https://github.com/python-gitlab/python-gitlab/commit/293a9dc9b086568a043040f07fdf1aa574a52500))

* Add support for user block/unblock ([`e387de5`](https://github.com/python-gitlab/python-gitlab/commit/e387de528ad21766747b91bb7e1cd91f6e4642b5))

* bump version to cleanup my mess on pypi ([`942468d`](https://github.com/python-gitlab/python-gitlab/commit/942468d344eac2a70f73ed69a43c27a87baf78db))

* Update ChangeLog and AUTHORS ([`74d82d4`](https://github.com/python-gitlab/python-gitlab/commit/74d82d4109e65d541707638fc9d3efc110c6ef32))

* MANIFEST: add .j2 files in docs/ ([`a495eec`](https://github.com/python-gitlab/python-gitlab/commit/a495eecceac2a687fb99ab4c85b63be73ac3126d))

* CLI: fix {all,owned,search} project listing ([`522cfd1`](https://github.com/python-gitlab/python-gitlab/commit/522cfd1e218ac568c7763b6c3ea2b84e3aeddfd6))

* Partially revert 00ab7d00 ([`9ae26fe`](https://github.com/python-gitlab/python-gitlab/commit/9ae26fe859e11bdc86f8662b6cca34522946dadf))

* version bump ([`8642e9e`](https://github.com/python-gitlab/python-gitlab/commit/8642e9eec44ab6b9d00581a6d5b53e8d719abec7))

* Merge branch &#39;test-script-cleanups&#39; of https://github.com/rhansen/python-gitlab into rhansen-test-script-cleanups ([`01e7c06`](https://github.com/python-gitlab/python-gitlab/commit/01e7c06c09cab0ef8338cf9f2f1aadd7ab3594d7))

* don&#39;t suppress docker&#39;s standard error

While docker is quite noisy, suppressing stderr makes it difficult to
troubleshoot problems. ([`0024552`](https://github.com/python-gitlab/python-gitlab/commit/002455272224b5e66adc47e2390eb73114a693d3))

* wait for the docker container to stop before removing it ([`52e4377`](https://github.com/python-gitlab/python-gitlab/commit/52e437770784a9807cdb42407abb1651ae2de139))

* use &#39;docker stop&#39; instead of &#39;docker kill&#39;

The &#39;stop&#39; command first tries SIGTERM before resorting to SIGKILL,
which is a gentler way to stop processes.  (SIGTERM gives processes an
opportunity to clean up before exiting; SIGKILL can&#39;t be caught so it
is very abrupt.) ([`c56fc47`](https://github.com/python-gitlab/python-gitlab/commit/c56fc47501a55d895825f652b19e1f554169a976))

* add more log messages ([`2609cbb`](https://github.com/python-gitlab/python-gitlab/commit/2609cbb10fd6f8a28e74e388e0053ea0afe44ecf))

* define a testcase() function; use it for tests ([`37f6d42`](https://github.com/python-gitlab/python-gitlab/commit/37f6d42a60c6c37ab3b33518d04a268116757c4c))

* use ${CONFIG} instead of repeating the filename ([`033881e`](https://github.com/python-gitlab/python-gitlab/commit/033881e3195388b9f92765a68e5c713953f9086e))

* fix usage error message ([`bc7332f`](https://github.com/python-gitlab/python-gitlab/commit/bc7332f3462295320bf76e056a5ab6206ffa4d6b))

* improve error handling

Break up pipelines and check the exit status of non-basic commands to
ensure that any problems cause the scripts/testcases to fail right
away. ([`5dcceb8`](https://github.com/python-gitlab/python-gitlab/commit/5dcceb88a124f2ba8a6c4475bd2c87d629f54950))

* convert scripts to POSIX shell by eliminating bashisms ([`57f1ad5`](https://github.com/python-gitlab/python-gitlab/commit/57f1ad53e202861f2f7c858f970782a2351dcb76))

* quote underquoted variable expansions

This protects against word splitting if the variable contains IFS
characters, and it ensures that an empty variable doesn&#39;t become an
elided argument. ([`09ef253`](https://github.com/python-gitlab/python-gitlab/commit/09ef2538bde7486e3327784c5968c5ee2482394b))

* convert $GITLAB to a function

This makes it possible to quote the $CONFIG variable expansion. ([`c100a04`](https://github.com/python-gitlab/python-gitlab/commit/c100a04eba7d9cd401333882a82948e7f644cea2))

* convert $OK to a function

This makes it possible to quote the variable expansions. ([`8198e3f`](https://github.com/python-gitlab/python-gitlab/commit/8198e3f9c322422a3507418b456d772923024892))

* only run deactivate if it exists

The deactivate command only exists if activate is run, but cleanup()
might be called before activate is run if there is an error. ([`6b298c6`](https://github.com/python-gitlab/python-gitlab/commit/6b298c692a6513dddc64b616f0398cef596e028f))

* ensure that cleanup() runs if terminated by the user ([`17914a3`](https://github.com/python-gitlab/python-gitlab/commit/17914a3572954f605699ec5c74e0c31d96a5dab8))

* check if docker container is up when waiting for gitlab

There&#39;s no point in waiting for GitLab to come up if the docker
container died. ([`58106a0`](https://github.com/python-gitlab/python-gitlab/commit/58106a0fd16b119f20e4837194c4d7aab3ab89b4))

* error out if required utilities aren&#39;t installed ([`b21fdda`](https://github.com/python-gitlab/python-gitlab/commit/b21fdda7459d3b7a1d405a9f133581bf87355303))

* use the log functions for errors and status messages

This causes the error messages to go to standard error, and it makes
it easy to prefix all log messages if desired. ([`867fe2f`](https://github.com/python-gitlab/python-gitlab/commit/867fe2f8dee092e4034ea32b51eb960bcf585aa3))

* add logging and error handling helper functions ([`7c0e443`](https://github.com/python-gitlab/python-gitlab/commit/7c0e443437ef11c878cd2443751e8d2fc3598704))

* compact some case statements ([`dfc6c70`](https://github.com/python-gitlab/python-gitlab/commit/dfc6c7017549e94a9956179535d5c21a9fdd4639))

* move common code to build_test_env.sh

Note that build_test_env.sh now creates and prepares the Python
virtualenv (it didn&#39;t before). ([`26999bf`](https://github.com/python-gitlab/python-gitlab/commit/26999bf0132eeac7e5b78094c54e6436964007ef))

* wrap long lines

Use line continuations to keep lines shorter than 80 columns. ([`6df844a`](https://github.com/python-gitlab/python-gitlab/commit/6df844a49c2631fd38940db4679ab1cba760e4ab))

* Add docstrings to some methods ([`1b5c8f1`](https://github.com/python-gitlab/python-gitlab/commit/1b5c8f1b0bf9766ea09ef864b9bf4c1dc313f168))

* Fix the RTD requirements ([`2e5476e`](https://github.com/python-gitlab/python-gitlab/commit/2e5476e5cb465680b2e48308d92109c408b9f1ef))

* Automatic doc generation for BaseManager classes

Provide a sphinx extension that parses the required/optioanl attributes
and add infoo to the class docstring. ([`a2eca72`](https://github.com/python-gitlab/python-gitlab/commit/a2eca72246ab40a0d96f6389c99e3a0b54e9342e))

* travis lacks py35 support without tricks ([`770dd4b`](https://github.com/python-gitlab/python-gitlab/commit/770dd4b3fee1fe9f4e40a144777afb6030992149))

* add python 3.5 test env ([`920d248`](https://github.com/python-gitlab/python-gitlab/commit/920d24823c3d7381097e1f30e34c3be8cec45627))

* add support for project builds ([`ebf36b8`](https://github.com/python-gitlab/python-gitlab/commit/ebf36b81f122b0242dec8750f5d80ec58e5e4bbe))

* Fix Project.tree()

Add API tests for tree(), blob() and archive(). ([`fc8affd`](https://github.com/python-gitlab/python-gitlab/commit/fc8affd11c90d795a118f3def977a8dd37372ce0))

* Fix project update ([`141f21a`](https://github.com/python-gitlab/python-gitlab/commit/141f21a9982e3de54e8c8d6a5138cc08a91e1492))

* Rework the __version__ import

This simplifies the setup.py script

Also provide a --version option for CLI ([`00ab7d0`](https://github.com/python-gitlab/python-gitlab/commit/00ab7d00a553e68eea5668dbf455404925fef6e0))

* fix inclusion of api/*.rst ([`9f256a7`](https://github.com/python-gitlab/python-gitlab/commit/9f256a71aa070bf28c70b2242976fbb0bc758bc4))

* Add sudo support ([`3711f19`](https://github.com/python-gitlab/python-gitlab/commit/3711f198a4e02144d9d49b68420d24afc9f4f957))

* Fix the &#39;password&#39; requirement for User creation ([`c579c80`](https://github.com/python-gitlab/python-gitlab/commit/c579c8081af787945c24c75b9ed85b2f0d8bc6b9))

* Add support for application settings ([`16d50cd`](https://github.com/python-gitlab/python-gitlab/commit/16d50cd5d52617d9117409ccc9819d8429088e84))

* Implement project variables support ([`e5438c6`](https://github.com/python-gitlab/python-gitlab/commit/e5438c6440a2477c796427bc598b2b31b10dc762))

* implement project triggers support ([`c11bebd`](https://github.com/python-gitlab/python-gitlab/commit/c11bebd83dd0ef89645e1eefce2aa107dd79180a))

* Implement setting release info on a tag

Add the set_release_description() method to ProjectTag.
Add python API test for this method. ([`7981987`](https://github.com/python-gitlab/python-gitlab/commit/7981987141825c198d5664d843e86472b9e44f3f))

* API tests for tags ([`0814d86`](https://github.com/python-gitlab/python-gitlab/commit/0814d8664d58fadb136af3c4031ea6e7359eb8f5))

* ProjectTag supports deletion (gitlab 8.4.0) ([`339d329`](https://github.com/python-gitlab/python-gitlab/commit/339d3295a53c5ba82780879d9881b6279d9001e9))

* Implement ProjectMilestone.issues()

This lists the issues related to the milestone.

Add python API tests for issues. ([`db1fb89`](https://github.com/python-gitlab/python-gitlab/commit/db1fb89d70feee8ef45876ec8ac5f9ccf69457a5))

* fix ProjectLabel get and delete ([`1ecb739`](https://github.com/python-gitlab/python-gitlab/commit/1ecb7399ad2fb469781068208f787818aa52eec2))

* wait a little before running the python tests ([`9709d79`](https://github.com/python-gitlab/python-gitlab/commit/9709d79f98eccee2a9f821f9fcc9dfbd5b55b70b))

* fix the API test for decode() ([`c22a19e`](https://github.com/python-gitlab/python-gitlab/commit/c22a19e8f8221dbc16bbcfb17b669a31eac16d82))

* increase the timeout value for tests ([`4e21343`](https://github.com/python-gitlab/python-gitlab/commit/4e21343c26ab4c0897abd65ba67fa6f2b8490675))

* make connection exceptions more explicit ([`08d3ccf`](https://github.com/python-gitlab/python-gitlab/commit/08d3ccfa5d8c971afc85f5e1ba109b0785fe5e6e))

* add a decode method for ProjectFile ([`2eac071`](https://github.com/python-gitlab/python-gitlab/commit/2eac07139eb288cda2dd2d22d191ab3fc1053437))

* README is an RST file... ([`d3a5701`](https://github.com/python-gitlab/python-gitlab/commit/d3a5701e5d481da452185e7a07d7b53493ed9073))

* Update README with travis status ([`a4918a3`](https://github.com/python-gitlab/python-gitlab/commit/a4918a34b6b457e8c10c2fc2df939079e1ac4dcb))

* fix the test_create_unknown_path test ([`bf985b3`](https://github.com/python-gitlab/python-gitlab/commit/bf985b30038f8f097c46ab363b82efaab14cfab6))

* add a travis configuration file ([`e40d9ac`](https://github.com/python-gitlab/python-gitlab/commit/e40d9ac328bc5487ca15d2371399c8dfe3b91c51))

* Fix the json() method for python 3

Also add unit tests and fix pep8 test ([`d7271b1`](https://github.com/python-gitlab/python-gitlab/commit/d7271b12e91c90ad7216073354085ed2b0257f73))

* Merge branch &#39;rhansen-fix-json&#39; ([`982f54f`](https://github.com/python-gitlab/python-gitlab/commit/982f54fb174f23e60ed40577af2d62f281d83c10))

* Merge branch &#39;fix-json&#39; of https://github.com/rhansen/python-gitlab into rhansen-fix-json ([`26d73e2`](https://github.com/python-gitlab/python-gitlab/commit/26d73e2828db89f9464c291de7607b7e78c58ca4))

* skip BaseManager attributes when encoding to JSON

This fixes the following exception when calling User.json():

    TypeError: &lt;gitlab.objects.UserKeyManager object at 0x7f0477391ed0&gt; is not JSON serializable ([`ca6da62`](https://github.com/python-gitlab/python-gitlab/commit/ca6da62010ee88e1b03f7a5abbf69479103aa1e1))

* add a missing import statement

Add the import inside the function rather than at the top of the file
because otherwise it would introduce a circular dependency. ([`c95b3c3`](https://github.com/python-gitlab/python-gitlab/commit/c95b3c3b54c412cd5cc77c4d58816139363fb2d1))

* use a custom docker image for tests ([`3f38689`](https://github.com/python-gitlab/python-gitlab/commit/3f386891ecf15ac4f0da34bdda59cf8e8d2f6ff0))

* Add an initial set of API tests ([`7e4e1a3`](https://github.com/python-gitlab/python-gitlab/commit/7e4e1a32ec2481453475a5da5186d187e704cf19))

* include the docs in the tarball ([`bbcccaa`](https://github.com/python-gitlab/python-gitlab/commit/bbcccaa5407fa9d281f8b1268a653b6dff29d050))

* 0.11.1 release update ([`5c4f77f`](https://github.com/python-gitlab/python-gitlab/commit/5c4f77fc39ff8437dee86dd8a3c067f864d950ca))

* add some CLI tests ([`097171d`](https://github.com/python-gitlab/python-gitlab/commit/097171dd6d76fee3b09dc4a9a2f775ed7750790b))

* add unit tests for managers ([`6baea2f`](https://github.com/python-gitlab/python-gitlab/commit/6baea2f46e1e1ea1cb222b3ae414bffc4998d4e2))

* remove debugging print instruction ([`7e54a39`](https://github.com/python-gitlab/python-gitlab/commit/7e54a392d02bdeecfaf384c0b9aa742c6199284f))

* Fix discovery of parents object attrs for managers ([`0e0c81d`](https://github.com/python-gitlab/python-gitlab/commit/0e0c81d229f03397d4f342fe96fef2f1405b6124))

* remove &#34;=&#34; in examples for consistency ([`a4e29f8`](https://github.com/python-gitlab/python-gitlab/commit/a4e29f86d7851da12e40491d517c1af17da66336))

* (re)add CLI examples in the doc ([`1b64a47`](https://github.com/python-gitlab/python-gitlab/commit/1b64a4730b85cd1effec48d1751e088a80b82b77))

* Merge pull request #82 from cdbennett/commitstatus

Support setting commit status ([`02c5398`](https://github.com/python-gitlab/python-gitlab/commit/02c5398dcca9c3f3c8e7a661668d97affd1097d7))

* Support setting commit status

Support commit status updates.  Commit status can be set by a POST to
the appropriate commit URL.  The status can be updated by a subsequent
POST to the same URL with the same `name` and `ref`, but different
values for `state`, `description`, etc.

Note: Listing the commit statuses is not yet supported.  This is done
through a different path on the server, under the `repository` path.

Example of use from the CLI:

    # add a build status to a commit
    gitlab project-commit-status create --project-id 2 \
        --commit-id a43290c --state success --name ci/jenkins \
        --target-url http://server/build/123 \
        --description &#34;Jenkins build succeeded&#34; ([`3371008`](https://github.com/python-gitlab/python-gitlab/commit/33710088913c96db8eb22289e693682b41054e39))

* Support deletion without getting the object first

Use this feature in the CLI to avoid an extra API call to the server. ([`1d7ebea`](https://github.com/python-gitlab/python-gitlab/commit/1d7ebea727c2fa68135ef4290dfe51604d843688))

* cli.py: make internal functions private ([`e5821e6`](https://github.com/python-gitlab/python-gitlab/commit/e5821e6a39344d545ac230ac6d868a8f0aaeb46b))

* Add a script to build a test env

functional_tests.sh has been split in 2 scripts to make easier the run
of gitlab container. ([`572cfa9`](https://github.com/python-gitlab/python-gitlab/commit/572cfa94d8b7463237e0b938b01f2ca3408a2e30))

* Rework gitlab._sanitize

Make it a recursive function and eliminate _sanitize_dict.

Add unit tests. ([`03d8041`](https://github.com/python-gitlab/python-gitlab/commit/03d804153f20932226fd3b8a6a5daab5727e878a))

* Improve the API documentation. ([`4781fd7`](https://github.com/python-gitlab/python-gitlab/commit/4781fd7e4c3d9d5b343f0c1b0597a8a535d6bdbf))

* Rewrite the README

And link to the docs on RTD. ([`3e8cf4e`](https://github.com/python-gitlab/python-gitlab/commit/3e8cf4e9ea59b97bb1703b9cee1c3a3d9e6c7c42))

* Bump version

And update copyright years. ([`ca44878`](https://github.com/python-gitlab/python-gitlab/commit/ca44878787a3e907ea35fd4adbb0a5c3020b44ed))

* Update AUTHORS ([`0163499`](https://github.com/python-gitlab/python-gitlab/commit/0163499bace58a5487f4f09bef2f656fdb541871))

* Update ChangeLog for 0.11 ([`3fd64df`](https://github.com/python-gitlab/python-gitlab/commit/3fd64df1c731b516beb8fcfc181b0cdbf31c4776))

* add missing import ([`9c74442`](https://github.com/python-gitlab/python-gitlab/commit/9c74442f8ad36786b06e8cfdcda7919d382ad31f))

* document the API migration from 0.10 ([`610bde8`](https://github.com/python-gitlab/python-gitlab/commit/610bde8da2430d95efb6881246ae1decff43c2ca))

* implement group search in CLI ([`5ea6d0a`](https://github.com/python-gitlab/python-gitlab/commit/5ea6d0ab7a69000be8ed01eaf2c5a49a79e33215))

* Add support for groups search

Factorize the code to avoid duplication with the ProjectManager class.
Implement unit tests for the group search.

Original patchh from Daniel Serodio (PR #55). ([`5513d0f`](https://github.com/python-gitlab/python-gitlab/commit/5513d0f52cd488b14c94389a09d01877fa5596e0))

* unit tests for config parser ([`0ae315a`](https://github.com/python-gitlab/python-gitlab/commit/0ae315a4d1d154122208883bd006b2b882cb5113))

* Implement ProjectManager search/list methods

The existing Gitlab methods are deprecated.

Unit tests have been added. ([`689ecae`](https://github.com/python-gitlab/python-gitlab/commit/689ecae70585e79c281224162a0ba2ab3921242a))

* CLI: fix the discovery of possible actions ([`e48e149`](https://github.com/python-gitlab/python-gitlab/commit/e48e14948f886a7bb71b22f82d71c2572a09341e))

* Create a manager for ProjectFork objects ([`e8631c1`](https://github.com/python-gitlab/python-gitlab/commit/e8631c1d505690a04704a9c19ba4a2d8564c6ef4))

* Merge branch &#39;fgouteroux-add_fork_support&#39; ([`37912c1`](https://github.com/python-gitlab/python-gitlab/commit/37912c1ccd395b2831be0b6f4155264a1ebcb1fe))

* Merge branch &#39;add_fork_support&#39; of https://github.com/fgouteroux/python-gitlab into fgouteroux-add_fork_support ([`77d34b3`](https://github.com/python-gitlab/python-gitlab/commit/77d34b353a1dfb1892de316a58b461c26eead66b))

* add fork project support ([`cedf080`](https://github.com/python-gitlab/python-gitlab/commit/cedf080ff8553b6ef5cd7995f5ab3608aaeb3793))

* Deprecate the &#34;old&#34; Gitlab methods

Update the associated unit tests. ([`2bf9794`](https://github.com/python-gitlab/python-gitlab/commit/2bf9794c81487883c346850a79d6b7db1295fd95))

* README update ([`dc0099d`](https://github.com/python-gitlab/python-gitlab/commit/dc0099d7901bd381fabadb8be77b93e7258454b3))

* Provide a getting started doc for the API ([`2237d85`](https://github.com/python-gitlab/python-gitlab/commit/2237d854f3c83f176b03392debf9785c53b0738b))

* Remove extra dep on sphinx-argparse ([`64d6356`](https://github.com/python-gitlab/python-gitlab/commit/64d635676c410648906be963fd1521c4baf17f25))

* Rework the requirements for RTD ([`4a53627`](https://github.com/python-gitlab/python-gitlab/commit/4a536274d2728b38210b020ce7c5ab7ac9ab8cad))

* Document installation using pip and git ([`7523a61`](https://github.com/python-gitlab/python-gitlab/commit/7523a612ace8bfa770737b5218ccc899f59f85df))

* Document the CLI ([`0ee53e0`](https://github.com/python-gitlab/python-gitlab/commit/0ee53e0c5853c08b69d21ba6b89bd1bf8ee6bb18))

* add unit tests for BaseManager ([`2a93c62`](https://github.com/python-gitlab/python-gitlab/commit/2a93c629ef88ffbe2564d154fa32fc723a4b0ea9))

* GitLab -&gt; Gitlab (class names) ([`fdf295f`](https://github.com/python-gitlab/python-gitlab/commit/fdf295f99f4e7f68e360280f103a164f447adf15))

* fix pretty_print with managers ([`bef97fe`](https://github.com/python-gitlab/python-gitlab/commit/bef97fe3a06802971d67fb70c5215f200cf31147))

* README update ([`d0da618`](https://github.com/python-gitlab/python-gitlab/commit/d0da618a793ef974e1f547c2ac28481f3719c152))

* Implement managers to get access to resources

This changes the &#39;default&#39; API, using managers is the recommended way to
get/list/create objects. Additional operations will be implemented in
followup patchs.

Old methods are deprecated and will disappear in a while. ([`46f74e8`](https://github.com/python-gitlab/python-gitlab/commit/46f74e8e4e6cd093a3be4309802f5a72ed305080))

* update the docs copyright years ([`e5246bf`](https://github.com/python-gitlab/python-gitlab/commit/e5246bffd17eb9863516677a086928af40fba9f5))

* add missing copyright header ([`b66672e`](https://github.com/python-gitlab/python-gitlab/commit/b66672ee18506035d08453dbfc5b429bdc81702d))

* Split code in multiple files ([`8fa4455`](https://github.com/python-gitlab/python-gitlab/commit/8fa44554736c4155a1c3b013d29c0625277a2e07))

* remove deprecated methods ([`118b298`](https://github.com/python-gitlab/python-gitlab/commit/118b2985249b3b152064af57e03231f1e1c59622))

* python3: fix CLI error when arguments are missing ([`7c38ef6`](https://github.com/python-gitlab/python-gitlab/commit/7c38ef6f2f089c1fbf9fa0ade249bb460c96ee9d))

* fix the tests ([`1db3cc1`](https://github.com/python-gitlab/python-gitlab/commit/1db3cc1e4f7e8f3bfae1f2e8cdbd377701789eb4))

* Rename the _created attribute _from_api ([`2a76b74`](https://github.com/python-gitlab/python-gitlab/commit/2a76b7490ba3dc6de6080d2dab55be017c09db59))

* Provide a create method for GitlabObject&#39;s

Instead of using the constructor to do everything (get, list and
create), we now provide a class method for each action. This should make
code easier to read. ([`a636d5a`](https://github.com/python-gitlab/python-gitlab/commit/a636d5ab25d2b248d89363ac86ecad7a0b90f100))

* Add the CLI -g short option for --gitlab ([`7e61a28`](https://github.com/python-gitlab/python-gitlab/commit/7e61a28d74a8589bffcfb70e0f3622113f6442ae))

* Add a get method for GitlabObject

This change provides a way to implement GET for objects that don&#39;t
support it, but support LIST.

It is also a first step to a cleaner API. ([`74dc2ac`](https://github.com/python-gitlab/python-gitlab/commit/74dc2acc788fb6e2fdced0561d8959e2a9d0572f))

* functional_tests.sh: support python 2 and 3 ([`c580b1e`](https://github.com/python-gitlab/python-gitlab/commit/c580b1e69868e038ef61080aa6c6b92f112b4891))

* Move request return_code tests in _raise_error_from_response ([`81b0a06`](https://github.com/python-gitlab/python-gitlab/commit/81b0a0679cc3adf93af22c4580b2f67c934b290e))

* Version bump ([`38f17c1`](https://github.com/python-gitlab/python-gitlab/commit/38f17c1a04bdc668d3599555f85c891246893429))

* update AUTHORS and ChangeLog ([`e673dab`](https://github.com/python-gitlab/python-gitlab/commit/e673dab4f3a17a14bea38854ad10b83eef4fc18b))

* Add support for group members update

Closes #73 ([`99c4710`](https://github.com/python-gitlab/python-gitlab/commit/99c47108ee5dfa445801efdf5cda628ca7b97679))

* Merge branch &#39;master&#39; of github.com:gpocentek/python-gitlab ([`45becb9`](https://github.com/python-gitlab/python-gitlab/commit/45becb92f47c74cb6433cdb644da5e2052a337e8))

* Merge pull request #78 from cdbennett/fix_python3_sort_types

Use name as sort key to fix Python 3 TypeError ([`6f1fd7e`](https://github.com/python-gitlab/python-gitlab/commit/6f1fd7ea8d203b771e32393b5270a6af490b37a8))

* Use name as sort key to fix Python 3 TypeError

Sort types explicitly by name to fix unorderable types TypeError in
Python 3.

The call to sort() on cli.py line 259 produced the error:

    TypeError: unorderable types: type() &lt; type() ([`363b75e`](https://github.com/python-gitlab/python-gitlab/commit/363b75e73c2b66ab625811accdb9d639fb068675))

* Sanitize the id used to construct URLs

Closes #28 ([`5d88f68`](https://github.com/python-gitlab/python-gitlab/commit/5d88f68ddadddf98c42940a713817487058f8c17))

* try to fix the RTD build ([`acc1511`](https://github.com/python-gitlab/python-gitlab/commit/acc151190e32ddaf9198a10c5b816af2d36c0f19))

* Merge pull request #72 from pa4373/newuser-confirm-fix

Can bypassing confirm when creating new user now ([`d069381`](https://github.com/python-gitlab/python-gitlab/commit/d069381371c7b0eb88edbf56bc13b05e4b2664fa))

* Can bypassing confirm when creating new user ([`a0fe68b`](https://github.com/python-gitlab/python-gitlab/commit/a0fe68bc07c9b551a7daec87b31f481878f4d450))

* Test branch creation et deletion ([`f07de94`](https://github.com/python-gitlab/python-gitlab/commit/f07de9484d5f05fd09c47cba41665a858b485cf0))

* Fix GET/POST for project files ([`9c58013`](https://github.com/python-gitlab/python-gitlab/commit/9c58013a269d3da2beec947a152605fc3c926577))

* hide the action attribute ([`3270865`](https://github.com/python-gitlab/python-gitlab/commit/3270865977fcf5375b0d99e06ef6cf842eb406e9))

* Fix deletion of object not using &#39;id&#39; as ID

Closes #68 ([`e5aa69b`](https://github.com/python-gitlab/python-gitlab/commit/e5aa69baf90675777bcd10927cfb92e561343b75))

* README: add missing import in sample ([`d8fdbc4`](https://github.com/python-gitlab/python-gitlab/commit/d8fdbc4157623af8c2fabb4878e2de10a3efa933))

* setup.py: require requests&gt;=1

Closes #69 ([`21fdf1b`](https://github.com/python-gitlab/python-gitlab/commit/21fdf1b901f30b45251d918bd936b7453ce0ff46))

* Provide a Gitlab.from_config method

It provides the Gitlab object creation from the ~/.python-gitlab.cfg,
just like the CLI does. ([`fef8c7f`](https://github.com/python-gitlab/python-gitlab/commit/fef8c7f7bc9f4a853012a5294f0731cc7f266625))

* update README for list(all=True) ([`6cc8126`](https://github.com/python-gitlab/python-gitlab/commit/6cc8126381d0d241aeaca69d9932f0b425538f4f))

* don&#39;t list everything by default ([`a9e8da9`](https://github.com/python-gitlab/python-gitlab/commit/a9e8da98236df39249584bd2700a7bdc70c5a187))

* fix pep8 test ([`e93188e`](https://github.com/python-gitlab/python-gitlab/commit/e93188e2953929d27f2943ae964eab7e3babd6f2))

* Merge pull request #64 from jantman/issues/63

python-gitlab Issue #63 - implement pagination for list() ([`24d5035`](https://github.com/python-gitlab/python-gitlab/commit/24d5035558dec227d2a497d7bf5be3bbaafc0c00))

* issue #63 add unit tests for &#39;next&#39; link handling in list() ([`719526d`](https://github.com/python-gitlab/python-gitlab/commit/719526dc8b0fb7d577f0a5ffa80d8f0ca31a95c6))

* issue #63 - revert logging additions ([`f9654cd`](https://github.com/python-gitlab/python-gitlab/commit/f9654cd1c0dca5b75a2ae78634b06feea7cc3b62))

* python-gitlab Issue #63 - implement pagination for list() ([`33ceed6`](https://github.com/python-gitlab/python-gitlab/commit/33ceed61759e1eb5197154d16cd81030e138921d))

* Merge pull request #66 from stefanklug/master

Fix error when fetching single MergeRequests ([`adbe0a4`](https://github.com/python-gitlab/python-gitlab/commit/adbe0a4391f1e3b4d615ef7966dfa66e75b9a6fa))

* add support to update MergeRequestNotes ([`79d452d`](https://github.com/python-gitlab/python-gitlab/commit/79d452d3ebf73d4385eb3b259d7c0bab8f914241))

* fix url when fetching a single MergeRequest ([`227f71c`](https://github.com/python-gitlab/python-gitlab/commit/227f71ce49cc3e0a3537a52dd2fac1d8045110f4))

* Fix the update/delete CLI subcommands

Also update the testing tool to test these features.

Closes #62 ([`802c144`](https://github.com/python-gitlab/python-gitlab/commit/802c144cfd199684506b3404f03c3657c75e307d))

* fix delete and update CLI methods ([`e57b779`](https://github.com/python-gitlab/python-gitlab/commit/e57b7794d1e1ae6795f5b914132a2891dc0d9509))

* more README updates ([`0922ed5`](https://github.com/python-gitlab/python-gitlab/commit/0922ed5453aaa5e982012bab16d9517e28626977))

* Improve the README a bit

Fix typos
Detail which options are required in the [global] section (closes #61) ([`f6abd4d`](https://github.com/python-gitlab/python-gitlab/commit/f6abd4da5fc8958795995e892cc42be1bd352bea))

* 0.9.1 release ([`1f48e65`](https://github.com/python-gitlab/python-gitlab/commit/1f48e659838e18a08290575454a222d5df79f202))

* setup.py: restore the version discovery hack ([`9966616`](https://github.com/python-gitlab/python-gitlab/commit/9966616cd4947cfa27019b55cc442c08f3d5f564))

* functional_test.sh: use a venv ([`e12abf1`](https://github.com/python-gitlab/python-gitlab/commit/e12abf18b5f8438c55ff6e8f7e89476dc11438f7))

* fix setuptool sdist ([`73c68db`](https://github.com/python-gitlab/python-gitlab/commit/73c68dbe01bb278e0dc294400afb3e538b363168))

* add tools/ to MANIFEST.in ([`82ff055`](https://github.com/python-gitlab/python-gitlab/commit/82ff055b9871a18ae727119fe0280a3d6065df82))

* add test files to MANIFEST.in ([`32daf2a`](https://github.com/python-gitlab/python-gitlab/commit/32daf2afae52bdf085c943ca1fa9d6d238ad8164))

* add test-requirements.txt in MANIFEST.in ([`5c20201`](https://github.com/python-gitlab/python-gitlab/commit/5c20201114e0a260c4395f391eb665f3fe5fa0f6))

* remove executable flag on cli.py ([`b8ee8f8`](https://github.com/python-gitlab/python-gitlab/commit/b8ee8f85d5c49f895deb675294840d85065d1633))

* get ready for a 0.9 release ([`dce3193`](https://github.com/python-gitlab/python-gitlab/commit/dce3193e03baa746228a91bdfdeaecd7aa8d5e10))

* Provide a basic functional test script

This can be used to quickly test the correct behavior of the CLI. The
script is simple and doesn&#39;t test much for now, but it&#39;s a start. ([`1bc412e`](https://github.com/python-gitlab/python-gitlab/commit/1bc412e2b7fa285e89a8ac37f05f0b62f354bdf5))

* update copyright date ([`aae8e2d`](https://github.com/python-gitlab/python-gitlab/commit/aae8e2d429f71a4e7bb976e8be2cf92fc3225737))

* CLI: remove wrong attributes from the verbose output

These attributes comme from the command line arguments. ([`d254e64`](https://github.com/python-gitlab/python-gitlab/commit/d254e641c58d8784526882ae48662dfedeb6eb88))

* CLI: provide a --config-file option ([`711c5be`](https://github.com/python-gitlab/python-gitlab/commit/711c5be6f8210a40de056ba5359d61f877d925c8))

* Rename a few more private methods ([`bed3adf`](https://github.com/python-gitlab/python-gitlab/commit/bed3adf688cf2061bb684d285c92a27eec6124af))

* Move the CLI in the gitlab package

Setup an console_script entry point to create the executable script. ([`d7bea07`](https://github.com/python-gitlab/python-gitlab/commit/d7bea076257febf36cc6de50d170bc61f3c6a49a))

* Fix the tests when the host runs a web server ([`4c6c778`](https://github.com/python-gitlab/python-gitlab/commit/4c6c7785ba17d053548181fc2eafbe3356ea33f5))

* Projects can be updated

Also fix the projects special listing (all, owned, ...)

Closes #54 ([`7bdb1be`](https://github.com/python-gitlab/python-gitlab/commit/7bdb1be12e5038085c2cfb416a50d8015bf3db58))

* improve handling of id attributes in CLI

closes #31 ([`8b42559`](https://github.com/python-gitlab/python-gitlab/commit/8b425599bcda4f2c1bf893f78e8773653afacff7))

* rework (and fix) the CLI parsing ([`ede1224`](https://github.com/python-gitlab/python-gitlab/commit/ede1224dc3f47faf161111ca1a0911db13462b94))

* use more pythonic names for some methods ([`c2d1f8e`](https://github.com/python-gitlab/python-gitlab/commit/c2d1f8e4e9fe5d94076da8bc836a99b89f6fe9af))

* make the tests pass ([`0032d46`](https://github.com/python-gitlab/python-gitlab/commit/0032d468b5dc93b5bf9e639f382b4c869c5ef14c))

* setup tox for py27 and py34 tests ([`8634a4d`](https://github.com/python-gitlab/python-gitlab/commit/8634a4dba13a42abb54b968896810ecbd264a2a3))

* move the tests inside the package ([`03bbfa0`](https://github.com/python-gitlab/python-gitlab/commit/03bbfa0fbc6d113b8b744f4901571593d1cabd13))

* Merge branch &#39;tests&#39; of https://github.com/mjmaenpaa/python-gitlab into mjmaenpaa-tests

Conflicts:
	setup.py ([`0443256`](https://github.com/python-gitlab/python-gitlab/commit/04432561cb0e1a7e658cf771fd530835b4f463c8))

* Added tests.

Uses httmock library to abstract away requests-library.
Uses nose to actually run tests. ([`f458522`](https://github.com/python-gitlab/python-gitlab/commit/f45852205397d84a3ca2b9554ffaacae153791cc))

* Deprecate some Gitlab object methods

raw* methods should never have been exposed; replace them with _raw_*
methods

setCredentials and setToken are replaced with set_credentials and
set_token ([`b7d04b3`](https://github.com/python-gitlab/python-gitlab/commit/b7d04b3d3a4a27693b066bd7ed6bd57884d51618))

* sphinx: don&#39;t hardcode the version in conf.py ([`59173ce`](https://github.com/python-gitlab/python-gitlab/commit/59173ceb40c88ef41b106c0f0cb571aa49cb1098))

* gitlab is now a package ([`d2e5700`](https://github.com/python-gitlab/python-gitlab/commit/d2e5700c68f33b0872616fedc6a3320c84c81de6))

* add a tox target to build docs ([`105896f`](https://github.com/python-gitlab/python-gitlab/commit/105896f59bd3399c7d76934e515dab57bcd4f594))

* Add a tox configuration file

Run pep8 tests only for now, and fix pep8 errors. ([`82a88a7`](https://github.com/python-gitlab/python-gitlab/commit/82a88a714e3cf932798c15879fda0a7d6d7047f1))

* Merge pull request #58 from massimone88/master

Used argparse library ([`99cc43a`](https://github.com/python-gitlab/python-gitlab/commit/99cc43a9bb6038d3f1c9fe4976d938232b4c8207))

* change changelog, change, add my name on collaborators, change version ([`0d5b988`](https://github.com/python-gitlab/python-gitlab/commit/0d5b988e56794d8c52fa2c0e9d4023a8554d86fb))

* implemented argparse object for parsing the argument of the command line ([`d44b48d`](https://github.com/python-gitlab/python-gitlab/commit/d44b48df2951e0e9e21bf8a0c48b09f8c894ca13))

* Merge branch &#39;feature/impl_argparse&#39; into develop ([`fd473cd`](https://github.com/python-gitlab/python-gitlab/commit/fd473cd70384637693571fb71b86da08e87aae35))

* *clean import package
+add folder .idea to gitignore ([`23fe3c9`](https://github.com/python-gitlab/python-gitlab/commit/23fe3c9a87263b14c9c882bd1060de7232543616))

* bug fixed on requiredArguments ([`d099b11`](https://github.com/python-gitlab/python-gitlab/commit/d099b112dbb25c7cc219d8304adfaf4c8eb19eb7))

* remove &#34;gitlab&#34; of arguments because conflicts with &#34;gitlab&#34; attribute with GitlabObject class ([`bdc6f73`](https://github.com/python-gitlab/python-gitlab/commit/bdc6f73ca54cea41022c99cbb7f894f1eb04d545))

* remove forgotten argument ([`e6c85b5`](https://github.com/python-gitlab/python-gitlab/commit/e6c85b57405473784cd2dedd36df1bb906191e8f))

* improvement argument required for each action
add try/catch for error of parsing of not gitlabObject ([`2792091`](https://github.com/python-gitlab/python-gitlab/commit/2792091085b8977cd3564aa231bb1c0534b73a15))

* implement argparse library for parsing the arguments
create constans for action name
clean the code ([`9439ce4`](https://github.com/python-gitlab/python-gitlab/commit/9439ce472815db51f67187eeb2c0d6d3ee32f516))

* &#34;timeout&#34; option is an int, not a bool ([`2d48e71`](https://github.com/python-gitlab/python-gitlab/commit/2d48e71fe34ecb6bb28bf49285695326e5506456))

* require sphinxcontrib-napoleon to build the docs ([`990eeca`](https://github.com/python-gitlab/python-gitlab/commit/990eecac6f6c42ac0fde2e9af2f48ee20d9670fe))

* Make sphinx-configuration work with python2 ([`f22bfbd`](https://github.com/python-gitlab/python-gitlab/commit/f22bfbda178b19179b85a31bce46702e3f497427))

* Updated few gitlab.py docstrings as an example about how to document api ([`3005b3d`](https://github.com/python-gitlab/python-gitlab/commit/3005b3dabf1f4b51ba47f6ce4620a506641ccf43))

* Simple sphinx-project that automatically creates api documentation. ([`e822b0b`](https://github.com/python-gitlab/python-gitlab/commit/e822b0b06ba3ac615f465b9a66262aa799ebe1d4))

* ignore egg-info dirs ([`d0884b6`](https://github.com/python-gitlab/python-gitlab/commit/d0884b60904ed22a914721a71f9bf2aaecab45b7))

* add a requirements.txt file ([`13cd78a`](https://github.com/python-gitlab/python-gitlab/commit/13cd78ac0dd5f6a768a5f431956bc2a322408dae))

* Little documentation about sudo-usage ([`137ec47`](https://github.com/python-gitlab/python-gitlab/commit/137ec476c36cea9beeee3d61e8dbe3aa47c8d6ec))

* Forgot to add sudo-support to update ([`7d31e48`](https://github.com/python-gitlab/python-gitlab/commit/7d31e48c7f37514343dc48350ea0e88df3c0e712))

* Support labels in issues correctly ([`5d25344`](https://github.com/python-gitlab/python-gitlab/commit/5d25344635d69c3c2c9bdc286bf1236c0343eca8))

* Send proper json with correct content-type and support sudo-argument

Use json-encoder to create proper gitlab-compatible json
Send only attributes specified with requiredCreateAttrs and
optionalCreateAttrs
Send correct content-type header with json
Sudo, page &amp; per_page is supported for all methods by using **kwargs to
pass them
Changed rawPut to have same parameters as rawPost ([`96a44ef`](https://github.com/python-gitlab/python-gitlab/commit/96a44ef3ebf7d5ffed82baef1ee627ef0a409f3a))

* Update example about how to close issue in README ([`78c4b72`](https://github.com/python-gitlab/python-gitlab/commit/78c4b72de1bcfb836a66c1eaadb5d040564afa34))

* Added missing optionalCreateAttrs for ProjectIssue. Fixed typo in ProjectTag. ([`72eb744`](https://github.com/python-gitlab/python-gitlab/commit/72eb744c4408871178c05726570ef8fdca64bb8a))

* Improved error reporting

- Try to parse error response from gitlab.
- Use one function (_raiseErrorFromResponse) to parse and raise exceptions
  related to errors reported by gitlab. ([`8e13487`](https://github.com/python-gitlab/python-gitlab/commit/8e13487dfe7a480da8d40892699d0914bbb53f3d))

* Improved exception-classes.

- Added http status-code and gitlab error message to GitlabError-class.
- Added new GitlabOperationError-class to help separate connection and
authentication errors from other gitlab errors. ([`8351b2d`](https://github.com/python-gitlab/python-gitlab/commit/8351b2d5fcb66fa7b0a6fae6e88aa5ad81126a42))

* Raise NotImplementedError on all cases, where can*-boolean is False ([`555cc45`](https://github.com/python-gitlab/python-gitlab/commit/555cc45638f18bf74099fb8c8d6dca46a64fea73))

* No reason to have separate _getListOrObject-method in Gitlab-class.

Changed GitlabObject-class version of _getListOrObject to classmethod.
Removed _getListOrObject-method from Gitlab-class.
Changed Gitlab-class to use GitlabObject-class version of _getListOrObject ([`90ebbeb`](https://github.com/python-gitlab/python-gitlab/commit/90ebbebc6f6b63246ea403dd386287e114522868))

* bump version to 0.8 ([`296a72f`](https://github.com/python-gitlab/python-gitlab/commit/296a72f9f137c2d5ea54e8f72a5fbe9c9833ee85))

* &#34;Document&#34; the timeout option ([`39aa998`](https://github.com/python-gitlab/python-gitlab/commit/39aa99873e121b4e06ec0876b5b0219ac8944195))

* Update the Changelog ([`8be5365`](https://github.com/python-gitlab/python-gitlab/commit/8be5365ef198ddab12df78e9e7bd0ca971e81724))

* CLI: support a timout option ([`1672529`](https://github.com/python-gitlab/python-gitlab/commit/167252924823badfa82b5287c940c5925fb05a9e))

* make sure to not display both id and idAttr ([`9744475`](https://github.com/python-gitlab/python-gitlab/commit/9744475a9d100a1267ebe0be87acce8895cf3c57))

* ProjectLabel: use name as id attribute ([`f042d2f`](https://github.com/python-gitlab/python-gitlab/commit/f042d2f67c51c0de8d300ef6b1ee36ff5088cdc4))

* pretty_print: don&#39;t display private attributes ([`fa92155`](https://github.com/python-gitlab/python-gitlab/commit/fa9215504d8b6dae2c776733721c718f2a1f2e1a))

* Add Mika Mäenpää in the authors list ([`526f1be`](https://github.com/python-gitlab/python-gitlab/commit/526f1be10d06f4359a5b90e485be02632e5c929f))

* Merge pull request #45 from mjmaenpaa/labels_files

Classes for ProjectLabels and ProjectFiles ([`928b9f0`](https://github.com/python-gitlab/python-gitlab/commit/928b9f09291a45283ed371b931288b1caddb5b1c))

* Classes for ProjectLabels and ProjectFiles ([`ad63e17`](https://github.com/python-gitlab/python-gitlab/commit/ad63e17ce7b6fd8c8eef993a44a1b18cc73fc4be))

* Merge pull request #44 from mjmaenpaa/noid_objects

Support api-objects which don&#39;t have id in api response. ([`afe0ab4`](https://github.com/python-gitlab/python-gitlab/commit/afe0ab4b7ecf9a37b88a3d8f77a2c17d95e571d3))

* Fixed object creation in list ([`134fc7a`](https://github.com/python-gitlab/python-gitlab/commit/134fc7ac024aa96b1d22cc421a081df6cd2724f3))

* Support api-objects which don&#39;t have id in api response. ([`c3ab869`](https://github.com/python-gitlab/python-gitlab/commit/c3ab869711276522fe2997ba6e6332704a059d22))

* Merge pull request #43 from mjmaenpaa/url_delete_attrs

Moved url attributes to separate list. Added list for delete attributes. ([`f7dfad3`](https://github.com/python-gitlab/python-gitlab/commit/f7dfad38877f9886d891ed19a21188de61e5c5bc))

* Moved url attributes to separate list. Added list for delete attributes. ([`ea4c099`](https://github.com/python-gitlab/python-gitlab/commit/ea4c099532993cdb3ea547fcbd931127c03fdffa))

* Merge pull request #40 from mjmaenpaa/py3

Python3 compatibility ([`1eccc3b`](https://github.com/python-gitlab/python-gitlab/commit/1eccc3b38bdb6d0b53d76b6a5099db89dcb53871))

* Py3 compatibility with six ([`431e4bd`](https://github.com/python-gitlab/python-gitlab/commit/431e4bdf089354534f6877d39631ff23038e8866))

* Python 3 compatibility for cli-program ([`d714c4d`](https://github.com/python-gitlab/python-gitlab/commit/d714c4d35bc627d9113a4925f843c54d6123e621))

* Python3 compatibility ([`15c0da5`](https://github.com/python-gitlab/python-gitlab/commit/15c0da5552aa57340d25946bb41d0cd079ec495d))

* Merge pull request #42 from mjmaenpaa/constructUrl

Moved url-construction to separate function ([`221f418`](https://github.com/python-gitlab/python-gitlab/commit/221f41806d0dad67adada158a9352aa9e2f2036f))

* Moved url-construction to separate function ([`e14e3bf`](https://github.com/python-gitlab/python-gitlab/commit/e14e3bf0f675c54930af53c832ccd7ab98df89f3))

* Merge pull request #41 from mjmaenpaa/gitlab_get_exception

Gitlab.get() raised GitlabListError instead of GitlabGetError ([`9736e0b`](https://github.com/python-gitlab/python-gitlab/commit/9736e0b0893e298712d1ad356e3f8341852ef0f7))

* Gitlab.get() raised GitlabListError instead of GitlabGetError ([`ee54b3e`](https://github.com/python-gitlab/python-gitlab/commit/ee54b3e6927f6c8d3b5f9bcbec0e67b94be8566d))

* Merge pull request #39 from mjmaenpaa/timeout

Timeout support ([`9f134fc`](https://github.com/python-gitlab/python-gitlab/commit/9f134fcaf41594e2e37bf24f20cde128bd21364b))

* Timeout support ([`d2e591e`](https://github.com/python-gitlab/python-gitlab/commit/d2e591ec75aec916f3b37192ddcdc2163d558995))

* Merge pull request #38 from mjmaenpaa/currentuser_key

Changed CurrentUser.Key to use _getListOrObject-method like all other functions ([`4664ebd`](https://github.com/python-gitlab/python-gitlab/commit/4664ebd9125d4eb07ee2add768b89362c6902f81))

* CurrentUser.Key uses _getListOrObject-method ([`afcf1c2`](https://github.com/python-gitlab/python-gitlab/commit/afcf1c23c36a7aa0f65392892ca4abb973e35b43))

* Merge pull request #37 from mjmaenpaa/list_kwargs

No reason to add kwargs to object in Gitlab.list()-method ([`2c86085`](https://github.com/python-gitlab/python-gitlab/commit/2c860856689bac90bbda44d4812a27d5b22144c0))

* No reason to add kwargs to object in Gitlab.list()-method because GitlabObject
constructor can handle them. ([`40ce81e`](https://github.com/python-gitlab/python-gitlab/commit/40ce81e9b9cea0dd75c712ccac887afd37416996))

* Merge pull request #36 from mjmaenpaa/setFromDict

_setFromDict thinks False is None ([`4c5c39d`](https://github.com/python-gitlab/python-gitlab/commit/4c5c39de41221696fa1d63de13ec61ae88f85f9f))

* _setFromDict thinks False is None ([`3cf35ce`](https://github.com/python-gitlab/python-gitlab/commit/3cf35cedfff4784af9e7b882b85f71b22ec93c25))

* Merge pull request #34 from tekacs/master

Update .sort to use key for Python 3.x. ([`ff2d84c`](https://github.com/python-gitlab/python-gitlab/commit/ff2d84c5f4ab1f492781c2f821347f94754991be))

* Update .sort to use key for Python 3.x.

Rather than really dubious cmp function. ([`b483319`](https://github.com/python-gitlab/python-gitlab/commit/b48331928225347aeee83af1bc3c1dee64205f9b))

* Merge pull request #32 from patgmiller/master

refactor &#34;_sanitize&#34; for Python &lt; 2.7 ([`6c4fc34`](https://github.com/python-gitlab/python-gitlab/commit/6c4fc34438b49f856d388f32be445d380d72216a))

* refactor &#34;_sanitize&#34; for Python &lt; 2.7 ([`89d3fa0`](https://github.com/python-gitlab/python-gitlab/commit/89d3fa03ae859c85bfbdb6db3c913824b274cecb))

* changelog update ([`8846bf7`](https://github.com/python-gitlab/python-gitlab/commit/8846bf7aaf21168ae75b90321dd84eb543c43a3e))

* bump version ([`3f0ac43`](https://github.com/python-gitlab/python-gitlab/commit/3f0ac43d54a62d09010f8a67d34308532014bfed))

* update copyright years ([`c6f0a8d`](https://github.com/python-gitlab/python-gitlab/commit/c6f0a8d1c582a4ac92375c26a612288b001683e0))

* flake8 fixes ([`5d5e0f7`](https://github.com/python-gitlab/python-gitlab/commit/5d5e0f7f49ddc1908339c0537fd4490f1ce2a1ed))

* Fix handling of boolean values

Gitlab expects an int (1 or 0) as value for boolean attributes.
Transform python bool&#39;s into int&#39;s when creating or updating objects.

Closes #22 ([`d4803f9`](https://github.com/python-gitlab/python-gitlab/commit/d4803f9f0f9615358353bf5fe1f0024a9a0d74c3))

* Support namespace/name for project id

Closes #28 ([`34d6952`](https://github.com/python-gitlab/python-gitlab/commit/34d6952ba1ca011a8550a8a4ff65ba901871eb1e))

* update AUTHORS ([`d38f219`](https://github.com/python-gitlab/python-gitlab/commit/d38f219712302a4d16c37b44109c7970cbdc073d))

* Merge pull request #27 from cdleonard/master

Fix encoding errors on display and update with redirected output ([`2b5ea46`](https://github.com/python-gitlab/python-gitlab/commit/2b5ea468c68058a2d9141ecafda02263dd1845ca))

* Fix encoding error when updating with redirected output

When output is redirected sys.stdout.encoding is None. Fix this by
always encoding to utf-8, assuming gitlab handles that. The encoding
used by the local system is irrelevant here. ([`ec185cf`](https://github.com/python-gitlab/python-gitlab/commit/ec185cf416adce98e0a3ef338720091c0e2a53fe))

* Fix encoding error when printing to redirected output

When redirecting output to a file sys.stdout.encoding is None, so use
sys.getdefaultencoding() instead. ([`e236fd9`](https://github.com/python-gitlab/python-gitlab/commit/e236fd94c48b949bbbc8e0dc2d55ebfaa1ef0069))

* Support state_event in ProjectMilestone

Closes #30 ([`2281283`](https://github.com/python-gitlab/python-gitlab/commit/22812832021911dccdd93ced0ef1088441e3d227))

* add support for branches creation and deletion ([`97e2689`](https://github.com/python-gitlab/python-gitlab/commit/97e26896a7c2916b0f0d2c64934f280d4c9e5dc7))

* add support for UserKey listing and deletion ([`09e4a64`](https://github.com/python-gitlab/python-gitlab/commit/09e4a64cda0531f7dd45984625cf5e1c90bb430f))

* drop the module shebang ([`01335f3`](https://github.com/python-gitlab/python-gitlab/commit/01335f3b904a7ea4c1fee2d5b7f84f6420577834))

* Merge pull request #16 from locke105/master

Fix license classifier in setup.py ([`8ce3e30`](https://github.com/python-gitlab/python-gitlab/commit/8ce3e30ba1fd3f9c587746dbe050a528bc6e952a))

* Fix license classifier in setup.py ([`994e464`](https://github.com/python-gitlab/python-gitlab/commit/994e464607fd955f0c514b760a1a48c6af897e85))

* version bump

Update Changelog and AUTHORS ([`1fe783d`](https://github.com/python-gitlab/python-gitlab/commit/1fe783dba0e63796411bc6a358191a3144dc9bb8))

* projects listing: explicitly define arguments for pagination ([`4fcef67`](https://github.com/python-gitlab/python-gitlab/commit/4fcef67d7ef275d81c3c4db7dfd21cdea0310e60))

* Merge pull request #13 from dpasqualin/master

Add support for extra parameters when listing all projects (Refs #12) ([`4b882b7`](https://github.com/python-gitlab/python-gitlab/commit/4b882b7b6b4b303fc18c428a3da2a26e1001e5c2))

* Add support for extra parameters when listing all projects (Refs #12)

Signed-off-by: Diego Giovane Pasqualin &lt;dpasqualin@c3sl.ufpr.br&gt; ([`1b6c595`](https://github.com/python-gitlab/python-gitlab/commit/1b6c5952f06fe1236e1e75ae68f9c2325e78d372))

* ProjectMember: constructor should not create a User object ([`1c21423`](https://github.com/python-gitlab/python-gitlab/commit/1c214233360524fae06c9f6946e0956843a000f3))

* ids can be unicode

Fixes #15 ([`c6e371e`](https://github.com/python-gitlab/python-gitlab/commit/c6e371e7b2e2e499e32dd11feb81c013b8ab32c4))

* version bump ([`04574f3`](https://github.com/python-gitlab/python-gitlab/commit/04574f381d3d50afa86ec890681105f8f5a2a31e))

* support creation of projects for users ([`dc2bf5e`](https://github.com/python-gitlab/python-gitlab/commit/dc2bf5ea5ae827178e1e7a058e39b491ddebc01a))

* Merge branch &#39;ProjectFile&#39; ([`0ee6ca5`](https://github.com/python-gitlab/python-gitlab/commit/0ee6ca547b08e5d629e0671db87829d857e05544))

* Project: add methods for create/update/delete files ([`ba39e88`](https://github.com/python-gitlab/python-gitlab/commit/ba39e88e215b6a5ef16c58efb26e33148a7fa19e))

* support projects listing: search, all, owned ([`bd6b4ac`](https://github.com/python-gitlab/python-gitlab/commit/bd6b4aca6dea4b533c4ab15ee649be7b9aabd761))

* system hooks can&#39;t be updated ([`2b4924e`](https://github.com/python-gitlab/python-gitlab/commit/2b4924e2fb5ddf32f7ed5e4d9dc055e57612f9c2))

* Project.archive(): download tarball of the project ([`debe41a`](https://github.com/python-gitlab/python-gitlab/commit/debe41aee6eb53c11ea0e6870becc116947fe17d))

* define new optional attributes for user creation ([`1cc7b17`](https://github.com/python-gitlab/python-gitlab/commit/1cc7b176d80e58c1fb5eda2b79a27674b65c0a65))

* provide constants for access permissions in groups ([`7afd232`](https://github.com/python-gitlab/python-gitlab/commit/7afd2329e3ff3f8cbe13504627a4d24b123acea5))

* update AUTHORS and Changelog ([`962e806`](https://github.com/python-gitlab/python-gitlab/commit/962e806412293cfd44e3c37240b5fc1817e5b9db))

* Merge remote-tracking branch &#39;github-mrts/master&#39; ([`7fb7c47`](https://github.com/python-gitlab/python-gitlab/commit/7fb7c473c58cc2b4e7567d444ffff3b3ecdb3243))

* Add support for project events. ([`32d4224`](https://github.com/python-gitlab/python-gitlab/commit/32d422445388766e7cc4913a51bf8890487d4ce5))

* Fix comments. ([`6705928`](https://github.com/python-gitlab/python-gitlab/commit/6705928406667ee010f448e41c14cfa63c263178))

* add a Key() method for User objects ([`1969abb`](https://github.com/python-gitlab/python-gitlab/commit/1969abb3bbb61c4cbb8499496be9f48bd74cf558))

* Merge pull request #10 from ksmets/master

Add SSH key for user ([`e31bb9e`](https://github.com/python-gitlab/python-gitlab/commit/e31bb9ea26a5ab3299464f37e0931bfee8b7cb62))

* Add SSH key for user ([`909c10e`](https://github.com/python-gitlab/python-gitlab/commit/909c10e0d155b0fcfcd63129e2f5921a11d9c017))

* Merge pull request #8 from Itxaka/master

fixed the requirements auto install from setup.py ([`37e6648`](https://github.com/python-gitlab/python-gitlab/commit/37e6648fe4127a51601a9456a03bbaf8ff674c10))

* fixed the requirements auto install from setup.py ([`01ade72`](https://github.com/python-gitlab/python-gitlab/commit/01ade72edf9d5dec27b5676c7fb05e9a995c775a))

* version bump ([`5f0136c`](https://github.com/python-gitlab/python-gitlab/commit/5f0136c7f84c7c6235d360aee6104232639a1d63))

* Add support for Gitlab 6.1 group members ([`71c8750`](https://github.com/python-gitlab/python-gitlab/commit/71c87508a268fafbcb0043617ec3aa7ed0e733fd))

* minor syntax/pep8 updates ([`09ef68f`](https://github.com/python-gitlab/python-gitlab/commit/09ef68f3743bb32add0da7d5cd562dac5df00c26))

* drop leftovers from local tests ([`4f001b4`](https://github.com/python-gitlab/python-gitlab/commit/4f001b4fe53661c5069ce6c689363bae4b8f7b51))

* Implement Gitlab 6.1 new methods

 - Project: tree, blob
 - ProjectCommit: diff, blob ([`c9aedf2`](https://github.com/python-gitlab/python-gitlab/commit/c9aedf21464b4c219aac4f46b53d591dc4f1ef16))

* ProjectMergeRequest: fix Note() method ([`4006ab2`](https://github.com/python-gitlab/python-gitlab/commit/4006ab26ce73d03a8d74cfd978d93117ce8d68d6))

* Allow to get a project commit (GitLab 6.1) ([`6b0c678`](https://github.com/python-gitlab/python-gitlab/commit/6b0c678aa8a3081d17fc2852d64828f04f49b91b))

* Fix strings encoding (Closes #6) ([`64cead6`](https://github.com/python-gitlab/python-gitlab/commit/64cead6d48f8c6a65ca89f90abc2fa010a36adaf))

* version bump ([`ceda87a`](https://github.com/python-gitlab/python-gitlab/commit/ceda87a6cac2558caeecd9c7bc96c2a08cb36cf9))

* doc updates ([`b73c92d`](https://github.com/python-gitlab/python-gitlab/commit/b73c92dd022d6133c04fe98da68423ec5ae16e21))

* Merge branch &#39;header-private-token&#39; of https://github.com/dekimsey/python-gitlab into token_in_header ([`9adb4fa`](https://github.com/python-gitlab/python-gitlab/commit/9adb4fae912279b7635820029fe0b12013e6332e))

* Use PRIVATE-TOKEN header for passing the auth token ([`d39c471`](https://github.com/python-gitlab/python-gitlab/commit/d39c471b188ad1302f0ef6c5f7eac4c6e0d1b742))

* provide a ChangeLog ([`2d5342b`](https://github.com/python-gitlab/python-gitlab/commit/2d5342b54f723f621ada53acdfc5ff5d8b1b8b8b))

* provide a AUTHORS file ([`7c85fb7`](https://github.com/python-gitlab/python-gitlab/commit/7c85fb7e865a648b49494add224f286e2343e9ff))

* cli: support ssl_verify config option ([`147a569`](https://github.com/python-gitlab/python-gitlab/commit/147a569598e0151d69a662ee7b60ce2870f49e9e))

* Merge pull request #5 from marbindrakon/ssl_verify_option

Add ssl_verify option to Gitlab object. ([`bb7ba7a`](https://github.com/python-gitlab/python-gitlab/commit/bb7ba7ae49a6970b156e2c32b01c777f4518f76b))

* Add ssl_verify option to Gitlab object. Defauls to True ([`309f1fe`](https://github.com/python-gitlab/python-gitlab/commit/309f1fe0fbaca19a400ed521a27362adad89b4d5))

* Merge pull request #4 from erikjwaxx/master

Correct url for merge requests API. ([`7431d91`](https://github.com/python-gitlab/python-gitlab/commit/7431d91afe829cc7ca5469418d14f1106e10dbc5))

* Correct url for merge requests API. ([`5090ef4`](https://github.com/python-gitlab/python-gitlab/commit/5090ef4f8d3c83fdcb6edf51663cfed593ee8ba4))

* version bump ([`d1cd3dc`](https://github.com/python-gitlab/python-gitlab/commit/d1cd3dc8f8ed37e2c05060815158217ac16ac494))

* provide a pip requirements.txt ([`c6fd8e8`](https://github.com/python-gitlab/python-gitlab/commit/c6fd8e83dec1c3a7d658ab1d960ee23cb63ea432))

* drop some debug statements ([`2807006`](https://github.com/python-gitlab/python-gitlab/commit/2807006e57529a9eb0127ef40d0a48b8fbaa11af))

* include COPYING in distribution ([`d65b684`](https://github.com/python-gitlab/python-gitlab/commit/d65b684aa6ef18d779c95e578fb16bf87248c76d))

* Merge pull request #1 from dekimsey/team-api

Addded API for team access. ([`8f65cf8`](https://github.com/python-gitlab/python-gitlab/commit/8f65cf8837944ec2640f983ef61a0e73877bd3bf))

* Merge remote-tracking branch &#39;samcday/teams&#39; into team-api

Conflicts:
	gitlab.py ([`cb5b754`](https://github.com/python-gitlab/python-gitlab/commit/cb5b7542edde926f73be6e7a2ab55f944ccbca00))

* Basic team support. ([`5388d19`](https://github.com/python-gitlab/python-gitlab/commit/5388d19f8885d3ca2f93c5e07ed58a1b84a87475))

* Addded API for team access. ([`8a22958`](https://github.com/python-gitlab/python-gitlab/commit/8a22958e20a622400daecb288135793544ad01ad))

* improve pretty_print() ([`05ab473`](https://github.com/python-gitlab/python-gitlab/commit/05ab4732ceaee7d6d6c1f162b5925602b7c9ad44))

* manage project branch protection with the cmd line ([`53562b3`](https://github.com/python-gitlab/python-gitlab/commit/53562b33fdb1726644c939b78f5445b558c5952e))

* rework the script code organization ([`33c771d`](https://github.com/python-gitlab/python-gitlab/commit/33c771d5ecea84a38b59e75b6a2f6a099b2ba8b4))

* rework the cmd line options ([`02bd7cd`](https://github.com/python-gitlab/python-gitlab/commit/02bd7cd57d635bd30e105cda8b249ca5d656eb6c))

* make --verbose behave like --fancy ([`a9b5bf4`](https://github.com/python-gitlab/python-gitlab/commit/a9b5bf4ea97ac85a5fab9953a46aa9c70d209c2e))

* fix parsing of options ([`2321631`](https://github.com/python-gitlab/python-gitlab/commit/23216313f7ccb5ed1c51eca73681cd76d767f04f))

* gitlab: make the current-user option work ([`4c998ea`](https://github.com/python-gitlab/python-gitlab/commit/4c998eaa2a58efa25ae08bfe084c3ef76df98644))

* README: document --page and --per-page ([`a7f2065`](https://github.com/python-gitlab/python-gitlab/commit/a7f206570b2a1a4104a9d6017c9b594fb3e93e13))

* listing: list the --page and --per-page options ([`079c107`](https://github.com/python-gitlab/python-gitlab/commit/079c107bd36620d9751299843d113df47fd592a7))

* ProjectBranch: commit is an other object ([`7e7b29c`](https://github.com/python-gitlab/python-gitlab/commit/7e7b29c02cc8a1015fb56a7dac6488cf24873922))

* README: use - instead of _ in examples ([`b4bc9df`](https://github.com/python-gitlab/python-gitlab/commit/b4bc9dff52d2610523cefa47fd0d0aaf8f2d12c1))

* drop the debian/ dir from master ([`7be3d54`](https://github.com/python-gitlab/python-gitlab/commit/7be3d54f42ebcf6f952d38b1b88dab0dd440ed54))

* drop the tests dir, this is useless ([`7c358d3`](https://github.com/python-gitlab/python-gitlab/commit/7c358d32cadf3c7755c0b30d0133867b680edb9f))

* gitlab: be less verbose by default

Provide a --fancy option to output more data on list/get/create queries. ([`3b15c6d`](https://github.com/python-gitlab/python-gitlab/commit/3b15c6d87e0a70f0769ecfd310a2ed3480abfe2b))

* pretty_print: use - instead of _ ([`41b6dba`](https://github.com/python-gitlab/python-gitlab/commit/41b6dbadcc7725248763515f77ae0f6bd4186dad))

* id attr might not available ([`7175772`](https://github.com/python-gitlab/python-gitlab/commit/71757723088556c3bd7c325413269df946343117))

* allow to use dash (-) instead of underscore (_) in attribute names ([`5a20efb`](https://github.com/python-gitlab/python-gitlab/commit/5a20efbacbb8269b2c41ac26ba4a0bb492e42c9d))

* Merge branch &#39;master&#39; into debian ([`93d5147`](https://github.com/python-gitlab/python-gitlab/commit/93d514706268570ea0b50a6479f4bf1e013ba9ba))

* provide a manifest for distribution ([`1c1702d`](https://github.com/python-gitlab/python-gitlab/commit/1c1702d03d3895168d266ebf45f15396a05340ff))

* update version in changelog ([`d9d6e0c`](https://github.com/python-gitlab/python-gitlab/commit/d9d6e0c8e29f338d43dc4be6fcb1e5b04916cde1))

* Merge branch &#39;master&#39; into debian ([`23753df`](https://github.com/python-gitlab/python-gitlab/commit/23753dffb94c06fae61f0afd7e4e75350b6ae74c))

* gitlab: autogenerate some doc ([`39a4a20`](https://github.com/python-gitlab/python-gitlab/commit/39a4a20dff1607d2583484bca63bbcf35bf3d9d8))

* gitlab: update the object syntax ([`9ca47aa`](https://github.com/python-gitlab/python-gitlab/commit/9ca47aa3365648fc497055b9e6fca5caaa59e81c))

* provide debian packaging ([`ef44b84`](https://github.com/python-gitlab/python-gitlab/commit/ef44b849f9ea94e59905c3f50d025125077e1634))

* python 3 support ([`e7ba350`](https://github.com/python-gitlab/python-gitlab/commit/e7ba350fe948def59da8c4043df45a24f867f225))

* object creation: print the created object ([`c6174e5`](https://github.com/python-gitlab/python-gitlab/commit/c6174e5f5a1e7ba98ac0c38f0b33bc84dbe4f1bb))

* return explicit error message on 404 ([`a04a5a5`](https://github.com/python-gitlab/python-gitlab/commit/a04a5a5fda2e2400e56d2f05c2d3530728d73367))

* gitlab: warn the user if an action cannot be performed ([`34e4304`](https://github.com/python-gitlab/python-gitlab/commit/34e4304812c29f9ac3eec8bef69d6cf359fff6ae))

* minor syntax change: canGetList =&gt; canList ([`49eab91`](https://github.com/python-gitlab/python-gitlab/commit/49eab9194dfa1bd264cfb3e19c762c57b2094a01))

* setup a list of mandatory attributes for list and get methods ([`5dda6e6`](https://github.com/python-gitlab/python-gitlab/commit/5dda6e6539a083f9f341104f37b5e2f4ebb918b3))

* Manually parse the arguments

We can use a more common syntax (-- prefix for options) this way. ([`a8072d9`](https://github.com/python-gitlab/python-gitlab/commit/a8072d96feb0323d220b919ff1e5df657b9f564e))

* install the gitlab script ([`dd22ce1`](https://github.com/python-gitlab/python-gitlab/commit/dd22ce1fcc1a334aeab18ab1ae07d23a028287d8))

* describe the gitlab script in README ([`204f681`](https://github.com/python-gitlab/python-gitlab/commit/204f6818b77cc3425e9bb137380fcbdfaa5f15df))

* provide a basic CLI ([`a205914`](https://github.com/python-gitlab/python-gitlab/commit/a2059142b7c26aa13cf77c5b602c0941cdb30266))

* provide a ProjectSnippet.Content() method ([`72e097d`](https://github.com/python-gitlab/python-gitlab/commit/72e097d8b2d3cb2b2f3943c92791071a96a96eba))

* add a GitlabObject.pretty_print method ([`abf1b0d`](https://github.com/python-gitlab/python-gitlab/commit/abf1b0df06ef1a1806da00eb91d98c5fe7a4bd72))

* deal with ids as strings ([`bc9d440`](https://github.com/python-gitlab/python-gitlab/commit/bc9d44083e2e2cee47d04c5d3c7ef55de38b49ed))

* raise an exception if deletion fails ([`4ee9c8c`](https://github.com/python-gitlab/python-gitlab/commit/4ee9c8c72325e145b1349e325a335b744455d3da))

* Allow creation of objects using the &#34;hidden API&#34; ([`1d55e67`](https://github.com/python-gitlab/python-gitlab/commit/1d55e67b7335926435cb2298b675698cec1873d0))

* Check the needed attributes to create objects

Provide a required and optional arguments lists for each object that can
be created using the API ([`123a01e`](https://github.com/python-gitlab/python-gitlab/commit/123a01e3cfda762202d58acc46c45ab58da57708))

* add a json() method to GitlabObject&#39;s ([`8d65870`](https://github.com/python-gitlab/python-gitlab/commit/8d65870a24e0f28b19bef86f4e0a72782c20c2b8))

* implement project transfer support ([`1625e55`](https://github.com/python-gitlab/python-gitlab/commit/1625e55f7afe0080fbc9ddcebdbfb0702e38ded6))

* add support for project deploy keys ([`1e3061c`](https://github.com/python-gitlab/python-gitlab/commit/1e3061c826a643204cef425758996d01d3b40f74))

* support for system hooks ([`42bef0a`](https://github.com/python-gitlab/python-gitlab/commit/42bef0aa598af1517810813d1bf7e10cac121690))

* fix use of json() method from requests ([`af84700`](https://github.com/python-gitlab/python-gitlab/commit/af84700f1168ec13ca175b0eb9e64d6bd30df0a0))

* unittest for SSH keys ([`7631e5e`](https://github.com/python-gitlab/python-gitlab/commit/7631e5ef345e825a0cbb37660c785e6b30b85962))

* some unit tests! ([`967ea88`](https://github.com/python-gitlab/python-gitlab/commit/967ea8892366f4a7245b0f79316a9d4516186e8e))

* restore Gitlab.Issue() prototype ([`561f349`](https://github.com/python-gitlab/python-gitlab/commit/561f3498bfbc59d90b6ed610f944cd3084fcf8c1))

* move documentation and todo to README.md ([`c10b01e`](https://github.com/python-gitlab/python-gitlab/commit/c10b01e84a9a262c00e46d7a4f315d66bea4fb94))

* implement protect/unprotect for branches ([`a02180d`](https://github.com/python-gitlab/python-gitlab/commit/a02180d1fe47ebf823f91ea0caff9064b58d2f5a))

* typo ([`dd210be`](https://github.com/python-gitlab/python-gitlab/commit/dd210bef3cd64e5e51fa36960b8148ad5bddbeb7))

* never add page and per_page attributes to the objects ([`96bf2b1`](https://github.com/python-gitlab/python-gitlab/commit/96bf2b13299ebdc2e579117261c64d957405a78c))

* ids for single items might be str ([`928d4fa`](https://github.com/python-gitlab/python-gitlab/commit/928d4fa60706eb7394f5d30304ed2d5904d9bb50))

* add a pagination example ([`74ec951`](https://github.com/python-gitlab/python-gitlab/commit/74ec951c208763bd5d7ff395c35cf9f9d6985ba9))

* Allow to pass additional args to list constructors

This is needed mostly for pagination support. ([`0149020`](https://github.com/python-gitlab/python-gitlab/commit/014902019b7410dcd3ed05360e3469bceeaa2b99))

* spacing ([`571ab0e`](https://github.com/python-gitlab/python-gitlab/commit/571ab0e176a0e656a3487a138498932b4eb3e9fa))

* fix the token authentication ([`938b1e6`](https://github.com/python-gitlab/python-gitlab/commit/938b1e68af154ffaca825662a5f5927adbecf706))

* add a _ from private attibutes ([`523d764`](https://github.com/python-gitlab/python-gitlab/commit/523d764e39c1a5a27362a5b2245a572a39e0d292))

* docstrings for the Gitlab class ([`046baf2`](https://github.com/python-gitlab/python-gitlab/commit/046baf2bc70fdbc6cefa689cdc77c51f8d1fa7db))

* cosmetics: make pep8 happy ([`9b64650`](https://github.com/python-gitlab/python-gitlab/commit/9b646502ce694efe5c1ec17110f49d395e1af3cd))

* add missing raise keywork ([`4d11843`](https://github.com/python-gitlab/python-gitlab/commit/4d11843e7c04bdec8a8d814645d955be5149a227))

* add a setup.py script ([`0dd1ede`](https://github.com/python-gitlab/python-gitlab/commit/0dd1ede13875512f50d7cb76df48d712dc2bc5d5))

* fix LGPL header and provide module informations ([`96e341e`](https://github.com/python-gitlab/python-gitlab/commit/96e341ebc8a32c794bbc6978e0eed4c7cd12797a))

* rework authentication API ([`eb4cd36`](https://github.com/python-gitlab/python-gitlab/commit/eb4cd36fc329793e124f589abaf80587925d7a6b))

* Rework the API

objects can be created using the usual syntax, with one optioanl
argument (int to get one object, dict to create an object, nothing to
get a list of items).
A save() method creates/updates the object on the server.
A delete() method removes it from the server. ([`653843d`](https://github.com/python-gitlab/python-gitlab/commit/653843d7e5e426009f648730877919f1a9ff1758))

* link GitLab and User classes to their possible children ([`d1f80da`](https://github.com/python-gitlab/python-gitlab/commit/d1f80da4cf7f0282cddba20038828b12e4e32c6d))

* raise an exception on 401 return code ([`01152da`](https://github.com/python-gitlab/python-gitlab/commit/01152da8392e5fea16be7fa42a7320f95fd53ada))

* drop Session() and add a Gitlab.authenticate() method ([`c4920ee`](https://github.com/python-gitlab/python-gitlab/commit/c4920ee8ee91c27fa9603c36b4e98dfe5ec14244))

* create Note classes linked to parent objetcs ([`bf25928`](https://github.com/python-gitlab/python-gitlab/commit/bf2592814963a8ce356beeff1709afe60838174b))

* add support for notes ([`0172900`](https://github.com/python-gitlab/python-gitlab/commit/01729005fcd5d0a25f80937d6707a232a56634b5))

* implement the Session() method ([`f188dcb`](https://github.com/python-gitlab/python-gitlab/commit/f188dcb5eda4f5b638356501687477f0cc0177e9))

* add methods to Project objects to access related objects ([`ab82226`](https://github.com/python-gitlab/python-gitlab/commit/ab822269c02cefa1557635523db948fe496aea2b))

* store a mirror of the gitlab instance in created objects ([`02afd17`](https://github.com/python-gitlab/python-gitlab/commit/02afd17162fadba3f18b7f467fab4aeed4732b84))

* Rework object creation from json ([`1fddcd2`](https://github.com/python-gitlab/python-gitlab/commit/1fddcd2359801ca41d614bf39249ee8f4c9005d1))

* initial import ([`1d7e85d`](https://github.com/python-gitlab/python-gitlab/commit/1d7e85db13e74b7c056c0b59795b177fc2f6cbb7))

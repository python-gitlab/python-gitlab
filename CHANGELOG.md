# CHANGELOG


## v5.2.0 (2024-12-17)

### Chores

- **deps**: Update all non-major dependencies
  ([`1e02f23`](https://github.com/python-gitlab/python-gitlab/commit/1e02f232278a85f818230b8931e2627c80a50e38))

- **deps**: Update all non-major dependencies
  ([`6532e8c`](https://github.com/python-gitlab/python-gitlab/commit/6532e8c7a9114f5abbfd610c65bd70d09576b146))

- **deps**: Update all non-major dependencies
  ([`8046387`](https://github.com/python-gitlab/python-gitlab/commit/804638777f22b23a8b9ea54ffce19852ea6d9366))

- **deps**: Update codecov/codecov-action action to v5
  ([`735efff`](https://github.com/python-gitlab/python-gitlab/commit/735efff88cc8d59021cb5a746ba70b66548e7662))

- **deps**: Update dependency commitizen to v4
  ([`9306362`](https://github.com/python-gitlab/python-gitlab/commit/9306362a14cae32b13f59630ea9a964783fa8de8))

- **deps**: Update gitlab/gitlab-ee docker tag to v17.6.1-ee.0
  ([#3053](https://github.com/python-gitlab/python-gitlab/pull/3053),
  [`f2992ae`](https://github.com/python-gitlab/python-gitlab/commit/f2992ae57641379c4ed6ac1660e9c1f9237979af))

Co-authored-by: renovate[bot] <29139614+renovate[bot]@users.noreply.github.com>

- **deps**: Update gitlab/gitlab-ee docker tag to v17.6.2-ee.0
  ([#3065](https://github.com/python-gitlab/python-gitlab/pull/3065),
  [`db0db26`](https://github.com/python-gitlab/python-gitlab/commit/db0db26734533d1a95225dc1a5dd2ae0b03c6053))

Co-authored-by: renovate[bot] <29139614+renovate[bot]@users.noreply.github.com>

- **deps**: Update pre-commit hook commitizen-tools/commitizen to v4
  ([`a8518f1`](https://github.com/python-gitlab/python-gitlab/commit/a8518f1644b32039571afb4172738dcde169bec0))

- **docs**: Fix CHANGELOG tracebacks codeblocks
  ([`9fe372a`](https://github.com/python-gitlab/python-gitlab/commit/9fe372a8898fed25d8bca8eedcf42560448380e4))

With v5.1.0 CHANGELOG.md was updated that mangled v1.10.0 triple backtick codeblock Traceback output
  that made sphinx fail [1] with a non-zero return code.

The resulting docs appears to be processes as text after the failing line [2]. While reviewing other
  backtick codeblocks fix v1.8.0 [3] to the original traceback.

[1]
  https://github.com/python-gitlab/python-gitlab/actions/runs/12060608158/job/33631303063#step:5:204
  [2] https://python-gitlab.readthedocs.io/en/v5.1.0/changelog.html#v1-10-0-2019-07-22 [3]
  https://python-gitlab.readthedocs.io/en/v5.0.0/changelog.html#id258

- **renovate**: Pin httpx until respx is fixed
  ([`b70830d`](https://github.com/python-gitlab/python-gitlab/commit/b70830dd3ad76ff537a1f81e9f69de72271a2305))

### Documentation

- **api-usage**: Fix link to Gitlab REST API Authentication Docs
  ([#3059](https://github.com/python-gitlab/python-gitlab/pull/3059),
  [`f460d95`](https://github.com/python-gitlab/python-gitlab/commit/f460d95cbbb6fcf8d10bc70f53299438843032fd))

### Features

- **api**: Add project templates ([#3057](https://github.com/python-gitlab/python-gitlab/pull/3057),
  [`0d41da3`](https://github.com/python-gitlab/python-gitlab/commit/0d41da3cc8724ded8a3855409cf9c5d776a7f491))

* feat(api): Added project template classes to templates.py * feat(api): Added project template
  managers to Project in project.py * docs(merge_requests): Add example of creating mr with
  description template * test(templates): Added unit tests for templates * docs(templates): added
  section for project templates

- **graphql**: Add async client
  ([`288f39c`](https://github.com/python-gitlab/python-gitlab/commit/288f39c828eb6abd8f05744803142beffed3f288))


## v5.1.0 (2024-11-28)

### Chores

- **deps**: Update all non-major dependencies
  ([`9061647`](https://github.com/python-gitlab/python-gitlab/commit/9061647315f4e3e449cb8096c56b8baa1dbb4b23))

- **deps**: Update all non-major dependencies
  ([`62da12a`](https://github.com/python-gitlab/python-gitlab/commit/62da12aa79b11b64257cd4b1a6e403964966e224))

- **deps**: Update all non-major dependencies
  ([`7e62136`](https://github.com/python-gitlab/python-gitlab/commit/7e62136991f694be9c8c76c12f291c60f3607b44))

- **deps**: Update all non-major dependencies
  ([`d4b52e7`](https://github.com/python-gitlab/python-gitlab/commit/d4b52e789fd131475096817ffd6f5a8e1e5d07c6))

- **deps**: Update all non-major dependencies
  ([`541a7e3`](https://github.com/python-gitlab/python-gitlab/commit/541a7e3ec3f685eb7c841eeee3be0f1df3d09035))

- **deps**: Update dependency pytest-cov to v6
  ([`ffa88b3`](https://github.com/python-gitlab/python-gitlab/commit/ffa88b3a45fa5997cafd400cebd6f62acd43ba8e))

- **deps**: Update gitlab/gitlab-ee docker tag to v17.5.1-ee.0
  ([`8111f49`](https://github.com/python-gitlab/python-gitlab/commit/8111f49e4f91783dbc6d3f0c3fce6eb504f09bb4))

- **deps**: Update gitlab/gitlab-ee docker tag to v17.5.2-ee.0
  ([#3041](https://github.com/python-gitlab/python-gitlab/pull/3041),
  [`d39129b`](https://github.com/python-gitlab/python-gitlab/commit/d39129b659def10213821f3e46718c4086e77b4b))

Co-authored-by: renovate[bot] <29139614+renovate[bot]@users.noreply.github.com>

- **deps**: Update gitlab/gitlab-ee docker tag to v17.6.0-ee.0
  ([#3044](https://github.com/python-gitlab/python-gitlab/pull/3044),
  [`79113d9`](https://github.com/python-gitlab/python-gitlab/commit/79113d997b3d297fd8e06c6e6e10fe39480cb2f6))

Co-authored-by: renovate[bot] <29139614+renovate[bot]@users.noreply.github.com>

- **deps**: Update pre-commit hook maxbrunet/pre-commit-renovate to v39
  ([`11458e0`](https://github.com/python-gitlab/python-gitlab/commit/11458e0e0404d1b2496b505509ecb795366a7e64))

### Features

- **api**: Get single project approval rule
  ([`029695d`](https://github.com/python-gitlab/python-gitlab/commit/029695df80f7370f891e17664522dd11ea530881))

- **api**: Support list and delete for group service accounts
  ([#2963](https://github.com/python-gitlab/python-gitlab/pull/2963),
  [`499243b`](https://github.com/python-gitlab/python-gitlab/commit/499243b37cda0c7dcd4b6ce046d42e81845e2a4f))

- **cli**: Enable token rotation via CLI
  ([`0cb8171`](https://github.com/python-gitlab/python-gitlab/commit/0cb817153d8149dfdfa3dfc28fda84382a807ae2))

- **const**: Add new Planner role to access levels
  ([`bdc8852`](https://github.com/python-gitlab/python-gitlab/commit/bdc8852051c98b774fd52056992333ff3638f628))

- **files**: Add support for more optional flags
  ([`f51cd52`](https://github.com/python-gitlab/python-gitlab/commit/f51cd5251c027849effb7e6ad3a01806fb2bda67))

GitLab's Repository Files API supports additional flags that weren't implemented before. Notably,
  the "start_branch" flag is particularly useful, as previously one had to use the "project-branch"
  command alongside "project-file" to add a file on a separate branch.

[1] https://docs.gitlab.com/ee/api/repository_files.html


## v5.0.0 (2024-10-28)

### Bug Fixes

- **api**: Set _repr_attr for project approval rules to name attr
  ([#3011](https://github.com/python-gitlab/python-gitlab/pull/3011),
  [`1a68f1c`](https://github.com/python-gitlab/python-gitlab/commit/1a68f1c5ff93ad77c58276231ee33f58b7083a09))

Co-authored-by: Patrick Evans <patrick.evans@gehealthcare.com>

### Chores

- Add Python 3.13 as supported ([#3012](https://github.com/python-gitlab/python-gitlab/pull/3012),
  [`b565e78`](https://github.com/python-gitlab/python-gitlab/commit/b565e785d05a1e7f559bfcb0d081b3c2507340da))

Mark that Python 3.13 is supported.

Use Python 3.13 for the Mac and Windows tests.

Also remove the 'py38' tox environment. We no longer support Python 3.8.

- Add testing of Python 3.14
  ([`14d2a82`](https://github.com/python-gitlab/python-gitlab/commit/14d2a82969cd1b3509526eee29159f15862224a2))

Also fix __annotations__ not working in Python 3.14 by using the annotation on the 'class' instead
  of on the 'instance'

Closes: #3013

- Remove "v3" question from issue template
  ([#3017](https://github.com/python-gitlab/python-gitlab/pull/3017),
  [`482f2fe`](https://github.com/python-gitlab/python-gitlab/commit/482f2fe6ccae9239b3a010a70969d8d887cdb6b6))

python-gitlab hasn't supported the GitLab v3 API since 2018. The last version of python-gitlab to
  support it was v1.4

Support was removed in:

commit fe89b949922c028830dd49095432ba627d330186 Author: Gauvain Pocentek <gauvain@pocentek.net>

Date: Sat May 19 17:10:08 2018 +0200

Drop API v3 support

Drop the code, the tests, and update the documentation.

- **deps**: Update all non-major dependencies
  ([`1e4326b`](https://github.com/python-gitlab/python-gitlab/commit/1e4326b393be719616db5a08594facdabfbc1855))

- **deps**: Update all non-major dependencies
  ([`b3834dc`](https://github.com/python-gitlab/python-gitlab/commit/b3834dceb290c4c3bc97541aea38b02de53638df))

- **deps**: Update dependency ubuntu to v24
  ([`6fda15d`](https://github.com/python-gitlab/python-gitlab/commit/6fda15dff5e01c9982c9c7e65e302ff06416517e))

- **deps**: Update gitlab/gitlab-ee docker tag to v17.4.2-ee.0
  ([`1cdfe40`](https://github.com/python-gitlab/python-gitlab/commit/1cdfe40ac0a5334ee13d530e3f6f60352a621892))

- **deps**: Update gitlab/gitlab-ee docker tag to v17.5.0-ee.0
  ([`c02a392`](https://github.com/python-gitlab/python-gitlab/commit/c02a3927f5294778b1c98128e1e04bcbc40ed821))

### Documentation

- **users**: Update Gitlab docs links
  ([#3022](https://github.com/python-gitlab/python-gitlab/pull/3022),
  [`3739b5d`](https://github.com/python-gitlab/python-gitlab/commit/3739b5dd11bed66fb482cf6d2dc34382327a0265))

### Features

- Remove support for Python 3.8, require 3.9 or higher
  ([#3005](https://github.com/python-gitlab/python-gitlab/pull/3005),
  [`9734ad4`](https://github.com/python-gitlab/python-gitlab/commit/9734ad4bcbedcf4ee61317c12f47ddacf2ac208f))

Python 3.8 is End-of-Life (EOL) as of 2024-10 as stated in https://devguide.python.org/versions/ and
  https://peps.python.org/pep-0569/#lifespan

By dropping support for Python 3.8 and requiring Python 3.9 or higher it allows python-gitlab to
  take advantage of new features in Python 3.9, which are documented at:
  https://docs.python.org/3/whatsnew/3.9.html

Closes: #2968

BREAKING CHANGE: As of python-gitlab 5.0.0, Python 3.8 is no longer supported. Python 3.9 or higher
  is required.

### Testing

- Add test for `to_json()` method
  ([`f4bfe19`](https://github.com/python-gitlab/python-gitlab/commit/f4bfe19b5077089ea1d3bf07e8718d29de7d6594))

This should get us to 100% test coverage on `gitlab/base.py`

### BREAKING CHANGES

- As of python-gitlab 5.0.0, Python 3.8 is no longer supported. Python 3.9 or higher is required.


## v4.13.0 (2024-10-08)

### Chores

- **deps**: Update all non-major dependencies
  ([`c3efb37`](https://github.com/python-gitlab/python-gitlab/commit/c3efb37c050268de3f1ef5e24748ccd9487e346d))

- **deps**: Update dependency pre-commit to v4
  ([#3008](https://github.com/python-gitlab/python-gitlab/pull/3008),
  [`5c27546`](https://github.com/python-gitlab/python-gitlab/commit/5c27546d35ced76763ea8b0071b4ec4c896893a1))

Co-authored-by: renovate[bot] <29139614+renovate[bot]@users.noreply.github.com>

### Features

- **api**: Add support for project Pages API
  ([`0ee0e02`](https://github.com/python-gitlab/python-gitlab/commit/0ee0e02f1d1415895f6ab0f6d23b39b50a36446a))


## v4.12.2 (2024-10-01)

### Bug Fixes

- Raise GitlabHeadError in `project.files.head()` method
  ([#3006](https://github.com/python-gitlab/python-gitlab/pull/3006),
  [`9bf26df`](https://github.com/python-gitlab/python-gitlab/commit/9bf26df9d1535ca2881c43706a337a972b737fa0))

When an error occurs, raise `GitlabHeadError` in `project.files.head()` method.

Closes: #3004


## v4.12.1 (2024-09-30)

### Bug Fixes

- **ci**: Do not rely on GitLab.com runner arch variables
  ([#3003](https://github.com/python-gitlab/python-gitlab/pull/3003),
  [`c848d12`](https://github.com/python-gitlab/python-gitlab/commit/c848d12252763c32fc2b1c807e7d9887f391a761))

- **files**: Correctly raise GitlabGetError in get method
  ([`190ec89`](https://github.com/python-gitlab/python-gitlab/commit/190ec89bea12d7eec719a6ea4d15706cfdacd159))

### Chores

- **deps**: Update all non-major dependencies
  ([#3000](https://github.com/python-gitlab/python-gitlab/pull/3000),
  [`d3da326`](https://github.com/python-gitlab/python-gitlab/commit/d3da326828274ed0c5f76b01a068519d360995c8))

Co-authored-by: renovate[bot] <29139614+renovate[bot]@users.noreply.github.com>

- **deps**: Update gitlab/gitlab-ee docker tag to v17.4.1-ee.0
  ([`64eed5d`](https://github.com/python-gitlab/python-gitlab/commit/64eed5d388252135a42a252b9100ffc75d9fb0ea))


## v4.12.0 (2024-09-28)

### Bug Fixes

- **api**: Head requests for projectfilemanager
  ([#2977](https://github.com/python-gitlab/python-gitlab/pull/2977),
  [`96a18b0`](https://github.com/python-gitlab/python-gitlab/commit/96a18b065dac4ce612a128f03e2fc6d1b4ccd69e))

* fix(api): head requests for projectfilemanager

---------

Co-authored-by: Patrick Evans <patrick.evans@gehealthcare.com>

Co-authored-by: Nejc Habjan <hab.nejc@gmail.com>

### Chores

- Update pylint to 3.3.1 and resolve issues
  ([#2997](https://github.com/python-gitlab/python-gitlab/pull/2997),
  [`a0729b8`](https://github.com/python-gitlab/python-gitlab/commit/a0729b83e63bcd74f522bf57a87a5800b1cf19d1))

pylint 3.3.1 appears to have added "too-many-positional-arguments" check with a value of 5.

I don't disagree with this, but we have many functions which exceed this value. We might think about
  converting some of positional arguments over to keyword arguments in the future. But that is for
  another time.

For now disable the check across the project.

- **deps**: Update all non-major dependencies
  ([`ae132e7`](https://github.com/python-gitlab/python-gitlab/commit/ae132e7a1efef6b0ae2f2a7d335668784648e3c7))

- **deps**: Update all non-major dependencies
  ([`10ee58a`](https://github.com/python-gitlab/python-gitlab/commit/10ee58a01fdc8071f29ae0095d9ea8a4424fa728))

- **deps**: Update dependency types-setuptools to v75
  ([`a2ab54c`](https://github.com/python-gitlab/python-gitlab/commit/a2ab54ceb40eca1e6e71f7779a418591426b2b2c))

- **deps**: Update gitlab/gitlab-ee docker tag to v17.3.2-ee.0
  ([`5cd1ab2`](https://github.com/python-gitlab/python-gitlab/commit/5cd1ab202e3e7b64d626d2c4e62b1662a4285015))

- **deps**: Update gitlab/gitlab-ee docker tag to v17.4.0-ee.0
  ([`8601808`](https://github.com/python-gitlab/python-gitlab/commit/860180862d952ed25cf95df1a4f825664f7e1c4b))

### Features

- Introduce related_issues to merge requests
  ([#2996](https://github.com/python-gitlab/python-gitlab/pull/2996),
  [`174d992`](https://github.com/python-gitlab/python-gitlab/commit/174d992e49f1e5171fee8893a1713f30324bbf97))

- **build**: Build multi-arch images
  ([#2987](https://github.com/python-gitlab/python-gitlab/pull/2987),
  [`29f617d`](https://github.com/python-gitlab/python-gitlab/commit/29f617d7d368636791baf703ecdbd22583356674))


## v4.11.1 (2024-09-13)

### Bug Fixes

- **client**: Ensure type evaluations are postponed
  ([`b41b2de`](https://github.com/python-gitlab/python-gitlab/commit/b41b2de8884c2dc8c8be467f480c7161db6a1c87))


## v4.11.0 (2024-09-13)

### Chores

- **deps**: Update all non-major dependencies
  ([`fac8bf9`](https://github.com/python-gitlab/python-gitlab/commit/fac8bf9f3e2a0218f96337536d08dec9991bfc1a))

- **deps**: Update all non-major dependencies
  ([`88c7529`](https://github.com/python-gitlab/python-gitlab/commit/88c75297377dd1f1106b5bc673946cebd563e0a1))

- **deps**: Update dependency types-setuptools to v74
  ([`bdfaddb`](https://github.com/python-gitlab/python-gitlab/commit/bdfaddb89ae7ba351bd3a21c6cecc528772db4de))

- **pre-commit**: Add deps
  ([`fe5e608`](https://github.com/python-gitlab/python-gitlab/commit/fe5e608bc6cc04863bd4d1d9dbe101fffd88e954))

### Documentation

- **objects**: Fix typo in get latest pipeline
  ([`b9f5c12`](https://github.com/python-gitlab/python-gitlab/commit/b9f5c12d3ba6ca4e4321a81e7610d03fb4440c02))

### Features

- Add a minimal GraphQL client
  ([`d6b1b0a`](https://github.com/python-gitlab/python-gitlab/commit/d6b1b0a962bbf0f4e0612067fc075dbdcbb772f8))

- **api**: Add exclusive GET attrs for /groups/:id/members
  ([`d44ddd2`](https://github.com/python-gitlab/python-gitlab/commit/d44ddd2b00d78bb87ff6a4776e64e05e0c1524e1))

- **api**: Add exclusive GET attrs for /projects/:id/members
  ([`e637808`](https://github.com/python-gitlab/python-gitlab/commit/e637808bcb74498438109d7ed352071ebaa192d5))

- **client**: Add retry handling to GraphQL client
  ([`8898c38`](https://github.com/python-gitlab/python-gitlab/commit/8898c38b97ed36d9ff8f2f20dee27ef1448b9f83))

- **client**: Make retries configurable in GraphQL
  ([`145870e`](https://github.com/python-gitlab/python-gitlab/commit/145870e628ed3b648a0a29fc551a6f38469b684a))

### Refactoring

- **client**: Move retry logic into utility
  ([`3235c48`](https://github.com/python-gitlab/python-gitlab/commit/3235c48328c2866f7d46597ba3c0c2488e6c375c))


## v4.10.0 (2024-08-28)

### Chores

- **deps**: Update all non-major dependencies
  ([`2ade0d9`](https://github.com/python-gitlab/python-gitlab/commit/2ade0d9f4922226143e2e3835a7449fde9c49d66))

- **deps**: Update all non-major dependencies
  ([`0578bf0`](https://github.com/python-gitlab/python-gitlab/commit/0578bf07e7903037ffef6558e914766b6cf6f545))

- **deps**: Update all non-major dependencies
  ([`31786a6`](https://github.com/python-gitlab/python-gitlab/commit/31786a60da4b9a10dec0eab3a0b078aa1e94d809))

- **deps**: Update dependency myst-parser to v4
  ([`930d4a2`](https://github.com/python-gitlab/python-gitlab/commit/930d4a21b8afed833b4b2e6879606bbadaee19a1))

- **deps**: Update dependency sphinx to v8
  ([`cb65ffb`](https://github.com/python-gitlab/python-gitlab/commit/cb65ffb6957bf039f35926d01f15db559e663915))

- **deps**: Update dependency types-setuptools to v73
  ([`d55c045`](https://github.com/python-gitlab/python-gitlab/commit/d55c04502bee0fb42e2ef359cde3bc1b4b510b1a))

- **deps**: Update gitlab/gitlab-ee docker tag to v17.2.2-ee.0
  ([`b2275f7`](https://github.com/python-gitlab/python-gitlab/commit/b2275f767dd620c6cb2c27b0470f4e8151c76550))

- **deps**: Update gitlab/gitlab-ee docker tag to v17.3.0-ee.0
  ([`e5a46f5`](https://github.com/python-gitlab/python-gitlab/commit/e5a46f57de166f94e01f5230eb6ad91f319791e4))

- **deps**: Update gitlab/gitlab-ee docker tag to v17.3.1-ee.0
  ([`3fdd130`](https://github.com/python-gitlab/python-gitlab/commit/3fdd130a8e87137e5a048d5cb78e43aa476c8f34))

- **deps**: Update python-semantic-release/upload-to-gh-release digest to 17c75b7
  ([`12caaa4`](https://github.com/python-gitlab/python-gitlab/commit/12caaa496740cb15e6220511751b7a20e2d29d07))

- **release**: Track tags for renovate
  ([`d600444`](https://github.com/python-gitlab/python-gitlab/commit/d6004449ad5aaaf2132318a78523818996ec3e21))

### Documentation

- **faq**: Correct the attribute fetching example
  ([`43a16ac`](https://github.com/python-gitlab/python-gitlab/commit/43a16ac17ce78cf18e0fc10fa8229f052eed3946))

There is an example about object attributes in the FAQ. It shows how to properly fetch all
  attributes of all projects, by using list() followed by a get(id) call.

Unfortunately this example used a wrong variable name, which caused it not to work and which could
  have made it slightly confusing to readers. This commit fixes that, by changing the variable name.

Now the example uses one variable for two Python objects. As they correspond to the same GitLab
  object and the intended behavior is to obtain that very object, just with all attributes, this is
  fine and is probably what readers will find most useful in this context.

### Features

- **api**: Project/group hook test triggering
  ([`9353f54`](https://github.com/python-gitlab/python-gitlab/commit/9353f5406d6762d09065744bfca360ccff36defe))

Add the ability to trigger tests of project and group hooks.

Fixes #2924

### Testing

- **cli**: Allow up to 30 seconds for a project export
  ([`bdc155b`](https://github.com/python-gitlab/python-gitlab/commit/bdc155b716ef63ef1398ee1e6f5ca67da1109c13))

Before we allowed a maximum of around 15 seconds for the project-export. Often times the CI was
  failing with this value.

Change it to a maximum of around 30 seconds.


## v4.9.0 (2024-08-06)

### Chores

- **ci**: Make pre-commit check happy
  ([`67370d8`](https://github.com/python-gitlab/python-gitlab/commit/67370d8f083ddc34c0acf0c0b06742a194dfa735))

pre-commit incorrectly wants double back-quotes inside the code section. Rather than fight it, just
  use single quotes.

- **deps**: Update all non-major dependencies
  ([`f95ca26`](https://github.com/python-gitlab/python-gitlab/commit/f95ca26b411e5a8998eb4b81e41c061726271240))

- **deps**: Update all non-major dependencies
  ([`7adc86b`](https://github.com/python-gitlab/python-gitlab/commit/7adc86b2e202cad42776991f0ed8c81517bb37ad))

- **deps**: Update all non-major dependencies
  ([`e820db0`](https://github.com/python-gitlab/python-gitlab/commit/e820db0d9db42a826884b45a76267fee861453d4))

- **deps**: Update dependency types-setuptools to v71
  ([`d6a7dba`](https://github.com/python-gitlab/python-gitlab/commit/d6a7dba600923e582064a77579dea82281871c25))

- **deps**: Update gitlab/gitlab-ee docker tag to v17.2.1-ee.0
  ([`d13a656`](https://github.com/python-gitlab/python-gitlab/commit/d13a656565898886cc6ba11028b3bcb719c21f0f))

- **deps**: Update pre-commit hook maxbrunet/pre-commit-renovate to v38
  ([`f13968b`](https://github.com/python-gitlab/python-gitlab/commit/f13968be9e2bb532f3c1185c1fa4185c05335552))

- **deps**: Update python-semantic-release/upload-to-gh-release digest to 0dcddac
  ([`eb5c6f7`](https://github.com/python-gitlab/python-gitlab/commit/eb5c6f7fb6487da21c69582adbc69aaf36149143))

- **deps**: Update python-semantic-release/upload-to-gh-release digest to e2355e1
  ([`eb18552`](https://github.com/python-gitlab/python-gitlab/commit/eb18552e423e270a27a2b205bfd2f22fcb2eb949))

### Features

- **snippets**: Add support for listing all instance snippets
  ([`64ae61e`](https://github.com/python-gitlab/python-gitlab/commit/64ae61ed9ba60169037703041c2a9a71017475b9))


## v4.8.0 (2024-07-16)

### Bug Fixes

- Have `participants()` method use `http_list()`
  ([`d065275`](https://github.com/python-gitlab/python-gitlab/commit/d065275f2fe296dd00e9bbd0f676d1596f261a85))

Previously it was using `http_get()` but the `participants` API returns a list of participants. Also
  by using this then we will warn if only a subset of the participants are returned.

Closes: #2913

- Issues `closed_by()/related_merge_requests()` use `http_list`
  ([`de2e4dd`](https://github.com/python-gitlab/python-gitlab/commit/de2e4dd7e80c7b84fd41458117a85558fcbac32d))

The `closed_by()` and `related_merge_requests()` API calls return lists. So use the `http_list()`
  method.

This will also warn the user if only a subset of the data is returned.

- **cli**: Generate UserWarning if `list` does not return all entries
  ([`e5a4379`](https://github.com/python-gitlab/python-gitlab/commit/e5a43799b5039261d7034af909011444718a5814))

Previously in the CLI, calls to `list()` would have `get_all=False` by default. Therefore hiding the
  fact that not all items are being returned if there were more than 20 items.

Added `--no-get-all` option to `list` actions. Along with the already existing `--get-all`.

Closes: #2900

- **files**: Cr: add explicit comparison to `None`
  ([`51d8f88`](https://github.com/python-gitlab/python-gitlab/commit/51d8f888aca469cff1c5ee5e158fb259d2862017))

Co-authored-by: Nejc Habjan <hab.nejc@gmail.com>

- **files**: Make `ref` parameter optional in get raw file api
  ([`00640ac`](https://github.com/python-gitlab/python-gitlab/commit/00640ac11f77e338919d7e9a1457d111c82af371))

The `ref` parameter was made optional in gitlab v13.11.0.

### Chores

- Add `show_caller` argument to `utils.warn()`
  ([`7d04315`](https://github.com/python-gitlab/python-gitlab/commit/7d04315d7d9641d88b0649e42bf24dd160629af5))

This allows us to not add the caller's location to the UserWarning message.

- Use correct type-hint for `die()`
  ([`9358640`](https://github.com/python-gitlab/python-gitlab/commit/93586405fbfa61317dc75e186799549573bc0bbb))

- **ci**: Specify name of "stale" label
  ([`44f62c4`](https://github.com/python-gitlab/python-gitlab/commit/44f62c49106abce2099d5bb1f3f97b64971da406))

Saw the following error in the log: [#2618] Removing the label "Stale" from this issue...
  ##[error][#2618] Error when removing the label: "Label does not exist"

My theory is that the case doesn't match ("Stale" != "stale") and that is why it failed. Our label
  is "stale" so update this to match. Thought of changing the label name on GitHub but then would
  also require a change here to the "any-of-labels". So it seemed simpler to just change it here.

It is confusing though that it detected the label "stale", but then couldn't delete it.

- **ci**: Stale: allow issues/PRs that have stale label to be closed
  ([`2ab88b2`](https://github.com/python-gitlab/python-gitlab/commit/2ab88b25a64bd8e028cee2deeb842476de54b109))

If a `stale` label is manually applied, allow the issue or PR to be closed by the stale job.

Previously it would require the `stale` label and to also have one of 'need info' or 'Waiting for
  response' labels added.

- **ci**: Use codecov token when available
  ([`b74a6fb`](https://github.com/python-gitlab/python-gitlab/commit/b74a6fb5157e55d3e4471a0c5c8378fed8075edc))

- **deps**: Update all non-major dependencies
  ([`4a2b213`](https://github.com/python-gitlab/python-gitlab/commit/4a2b2133b52dac102d6f623bf028bdef6dd5a92f))

- **deps**: Update all non-major dependencies
  ([`0f59069`](https://github.com/python-gitlab/python-gitlab/commit/0f59069420f403a17f67a5c36c81485c9016b59b))

- **deps**: Update all non-major dependencies
  ([`cf87226`](https://github.com/python-gitlab/python-gitlab/commit/cf87226a81108fbed4f58751f1c03234cc57bcf1))

- **deps**: Update gitlab/gitlab-ee docker tag to v17.1.1-ee.0
  ([`5e98510`](https://github.com/python-gitlab/python-gitlab/commit/5e98510a6c918b33c0db0a7756e8a43a8bdd868a))

- **deps**: Update gitlab/gitlab-ee docker tag to v17.1.2-ee.0
  ([`6fedfa5`](https://github.com/python-gitlab/python-gitlab/commit/6fedfa546120942757ea48337ce7446914eb3813))

- **deps**: Update python-semantic-release/upload-to-gh-release digest to c7c3b69
  ([`23393fa`](https://github.com/python-gitlab/python-gitlab/commit/23393faa0642c66a991fd88f1d2d68aed1d2f172))

- **deps**: Update python-semantic-release/upload-to-gh-release digest to fe6cc89
  ([`3f3ad80`](https://github.com/python-gitlab/python-gitlab/commit/3f3ad80ef5bb2ed837adceae061291b2b5545ed3))

### Documentation

- Document how to use `sudo` if modifying an object
  ([`d509da6`](https://github.com/python-gitlab/python-gitlab/commit/d509da60155e9470dee197d91926850ea9548de9))

Add a warning about using `sudo` when saving.

Give an example of how to `get` an object, modify it, and then `save` it using `sudo`

Closes: #532

- Variables: add note about `filter` for updating
  ([`c378817`](https://github.com/python-gitlab/python-gitlab/commit/c378817389a9510ef508b5a3c90282e5fb60049f))

Add a note about using `filter` when updating a variable.

Closes: #2835

Closes: #1387

Closes: #1125

### Features

- **api**: Add support for commit sequence
  ([`1f97be2`](https://github.com/python-gitlab/python-gitlab/commit/1f97be2a540122cb872ff59500d85a35031cab5f))

- **api**: Add support for container registry protection rules
  ([`6d31649`](https://github.com/python-gitlab/python-gitlab/commit/6d31649190279a844bfa591a953b0556cd6fc492))

- **api**: Add support for package protection rules
  ([`6b37811`](https://github.com/python-gitlab/python-gitlab/commit/6b37811c3060620afd8b81e54a99d96e4e094ce9))

- **api**: Add support for project cluster agents
  ([`32dbc6f`](https://github.com/python-gitlab/python-gitlab/commit/32dbc6f2bee5b22d18c4793f135223d9b9824d15))

### Refactoring

- **package_protection_rules**: Add missing attributes
  ([`c307dd2`](https://github.com/python-gitlab/python-gitlab/commit/c307dd20e3df61b118b3b1a8191c0f1880bc9ed6))

### Testing

- **files**: Omit optional `ref` parameter in test case
  ([`9cb3396`](https://github.com/python-gitlab/python-gitlab/commit/9cb3396d3bd83e82535a2a173b6e52b4f8c020f4))

- **files**: Test with and without `ref` parameter in test case
  ([`f316b46`](https://github.com/python-gitlab/python-gitlab/commit/f316b466c04f8ff3c0cca06d0e18ddf2d62d033c))

- **fixtures**: Remove deprecated config option
  ([`2156949`](https://github.com/python-gitlab/python-gitlab/commit/2156949866ce95af542c127ba4b069e83fcc8104))

- **registry**: Disable functional tests for unavailable endpoints
  ([`ee393a1`](https://github.com/python-gitlab/python-gitlab/commit/ee393a16e1aa6dbf2f9785eb3ef486f7d5b9276f))


## v4.7.0 (2024-06-28)

### Bug Fixes

- Add ability to add help to custom_actions
  ([`9acd2d2`](https://github.com/python-gitlab/python-gitlab/commit/9acd2d23dd8c87586aa99c70b4b47fa47528472b))

Now when registering a custom_action can add help text if desired.

Also delete the VerticalHelpFormatter as no longer needed. When the help value is set to `None` or
  some other value, the actions will get printed vertically. Before when the help value was not set
  the actions would all get put onto one line.

### Chores

- Add a help message for `gitlab project-key enable`
  ([`1291dbb`](https://github.com/python-gitlab/python-gitlab/commit/1291dbb588d3a5a54ee54d9bb93c444ce23efa8c))

Add some help text for `gitlab project-key enable`. This both adds help text and shows how to use
  the new `help` feature.

Example:

$ gitlab project-key --help usage: gitlab project-key [-h] {list,get,create,update,delete,enable}
  ...

options: -h, --help show this help message and exit

action: {list,get,create,update,delete,enable} Action to execute on the GitLab resource. list List
  the GitLab resources get Get a GitLab resource create Create a GitLab resource update Update a
  GitLab resource delete Delete a GitLab resource enable Enable a deploy key for the project

- Sort CLI behavior-related args to remove
  ([`9b4b0ef`](https://github.com/python-gitlab/python-gitlab/commit/9b4b0efa1ccfb155aee8384de9e00f922b989850))

Sort the list of CLI behavior-related args that are to be removed.

- **deps**: Update all non-major dependencies
  ([`88de2f0`](https://github.com/python-gitlab/python-gitlab/commit/88de2f0fc52f4f02e1d44139f4404acf172624d7))

- **deps**: Update all non-major dependencies
  ([`a510f43`](https://github.com/python-gitlab/python-gitlab/commit/a510f43d990c3a3fd169854218b64d4eb9491628))

- **deps**: Update all non-major dependencies
  ([`d4fdf90`](https://github.com/python-gitlab/python-gitlab/commit/d4fdf90655c2cb5124dc2ecd8b449e1e16d0add5))

- **deps**: Update all non-major dependencies
  ([`d5de288`](https://github.com/python-gitlab/python-gitlab/commit/d5de28884f695a79e49605a698c4f17b868ddeb8))

- **deps**: Update dependency types-setuptools to v70
  ([`7767514`](https://github.com/python-gitlab/python-gitlab/commit/7767514a1ad4269a92a6610aa71aa8c595565a7d))

- **deps**: Update gitlab/gitlab-ee docker tag to v17.0.1-ee.0
  ([`df0ff4c`](https://github.com/python-gitlab/python-gitlab/commit/df0ff4c4c1497d6449488b8577ad7188b55c41a9))

- **deps**: Update gitlab/gitlab-ee docker tag to v17.0.2-ee.0
  ([`51779c6`](https://github.com/python-gitlab/python-gitlab/commit/51779c63e6a58e1ae68e9b1c3ffff998211d4e66))

- **deps**: Update python-semantic-release/upload-to-gh-release digest to 477a404
  ([`02a551d`](https://github.com/python-gitlab/python-gitlab/commit/02a551d82327b879b7a903b56b7962da552d1089))

- **deps**: Update python-semantic-release/upload-to-gh-release digest to 6b7558f
  ([`fd0f0b0`](https://github.com/python-gitlab/python-gitlab/commit/fd0f0b0338623a98e9368c30b600d603b966f8b7))

### Features

- Add `--no-mask-credentials` CLI argument
  ([`18aa1fc`](https://github.com/python-gitlab/python-gitlab/commit/18aa1fc074b9f477cf0826933184bd594b63b489))

This gives the ability to not mask credentials when using the `--debug` argument.

- **api**: Add support for latest pipeline
  ([`635f5a7`](https://github.com/python-gitlab/python-gitlab/commit/635f5a7128c780880824f69a9aba23af148dfeb4))


## v4.6.0 (2024-05-28)

### Bug Fixes

- Don't raise `RedirectError` for redirected `HEAD` requests
  ([`8fc13b9`](https://github.com/python-gitlab/python-gitlab/commit/8fc13b91d63d57c704d03b98920522a6469c96d7))

- Handle large number of approval rules
  ([`ef8f0e1`](https://github.com/python-gitlab/python-gitlab/commit/ef8f0e190b1add3bbba9a7b194aba2f3c1a83b2e))

Use `iterator=True` when going through the list of current approval rules. This allows it to handle
  more than the default of 20 approval rules.

Closes: #2825

- **cli**: Don't require `--id` when enabling a deploy key
  ([`98fc578`](https://github.com/python-gitlab/python-gitlab/commit/98fc5789d39b81197351660b7a3f18903c2b91ba))

No longer require `--id` when doing: gitlab project-key enable

Now only the --project-id and --key-id are required.

- **deps**: Update minimum dependency versions in pyproject.toml
  ([`37b5a70`](https://github.com/python-gitlab/python-gitlab/commit/37b5a704ef6b94774e54110ba3746a950e733986))

Update the minimum versions of the dependencies in the pyproject.toml file.

This is related to PR #2878

- **projects**: Fix 'import_project' file argument type for typings
  ([`33fbc14`](https://github.com/python-gitlab/python-gitlab/commit/33fbc14ea8432df7e637462379e567f4d0ad6c18))

Signed-off-by: Adrian DC <radian.dc@gmail.com>

### Chores

- Add an initial .git-blame-ignore-revs
  ([`74db84c`](https://github.com/python-gitlab/python-gitlab/commit/74db84ca878ec7029643ff7b00db55f9ea085e9b))

This adds the `.git-blame-ignore-revs` file which allows ignoring certain commits when doing a `git
  blame --ignore-revs`

Ignore the commit that requires keyword arguments for `register_custom_action()`

https://docs.github.com/en/repositories/working-with-files/using-files/viewing-a-file#ignore-commits-in-the-blame-view

- Add type info for ProjectFile.content
  ([`62fa271`](https://github.com/python-gitlab/python-gitlab/commit/62fa2719ea129b3428e5e67d3d3a493f9aead863))

Closes: #2821

- Correct type-hint for `job.trace()`
  ([`840572e`](https://github.com/python-gitlab/python-gitlab/commit/840572e4fa36581405b604a985d0e130fe43f4ce))

Closes: #2808

- Create a CustomAction dataclass
  ([`61d8679`](https://github.com/python-gitlab/python-gitlab/commit/61d867925772cf38f20360c9b40140ac3203efb9))

- Remove typing-extensions from requirements.txt
  ([`d569128`](https://github.com/python-gitlab/python-gitlab/commit/d56912835360a1b5a03a20390fb45cb5e8b49ce4))

We no longer support Python versions before 3.8. So it isn't needed anymore.

- Require keyword arguments for register_custom_action
  ([`7270523`](https://github.com/python-gitlab/python-gitlab/commit/7270523ad89a463c3542e072df73ba2255a49406))

This makes it more obvious when reading the code what each argument is for.

- Update commit reference in git-blame-ignore-revs
  ([`d0fd5ad`](https://github.com/python-gitlab/python-gitlab/commit/d0fd5ad5a70e7eb70aedba5a0d3082418c5ffa34))

- **cli**: Add ability to not add `_id_attr` as an argument
  ([`2037352`](https://github.com/python-gitlab/python-gitlab/commit/20373525c1a1f98c18b953dbef896b2570d3d191))

In some cases we don't want to have `_id_attr` as an argument.

Add ability to have it not be added as an argument.

- **cli**: Add some simple help for the standard operations
  ([`5a4a940`](https://github.com/python-gitlab/python-gitlab/commit/5a4a940f42e43ed066838503638fe612813e504f))

Add help for the following standard operations: * list: List the GitLab resources * get: Get a
  GitLab resource * create: Create a GitLab resource * update: Update a GitLab resource * delete:
  Delete a GitLab resource

For example: $ gitlab project-key --help usage: gitlab project-key [-h]
  {list,get,create,update,delete,enable} ...

options: -h, --help show this help message and exit

action: list get create update delete enable Action to execute on the GitLab resource. list List the
  GitLab resources get Get a GitLab resource create Create a GitLab resource update Update a GitLab
  resource delete Delete a GitLab resource

- **cli**: On the CLI help show the API endpoint of resources
  ([`f1ef565`](https://github.com/python-gitlab/python-gitlab/commit/f1ef5650c3201f3883eb04ad90a874e8adcbcde2))

This makes it easier for people to map CLI command names to the API.

Looks like this: $ gitlab --help <snip> The GitLab resource to manipulate. application API endpoint:
  /applications application-appearance API endpoint: /application/appearance application-settings
  API endpoint: /application/settings application-statistics API endpoint: /application/statistics
  <snip>

- **deps**: Update all non-major dependencies
  ([`4c7014c`](https://github.com/python-gitlab/python-gitlab/commit/4c7014c13ed63f994e05b498d63b93dc8ab90c2e))

- **deps**: Update all non-major dependencies
  ([`ba1eec4`](https://github.com/python-gitlab/python-gitlab/commit/ba1eec49556ee022de471aae8d15060189f816e3))

- **deps**: Update dependency requests to v2.32.0 [security]
  ([`1bc788c`](https://github.com/python-gitlab/python-gitlab/commit/1bc788ca979a36eeff2e35241bdefc764cf335ce))

- **deps**: Update gitlab/gitlab-ee docker tag to v17
  ([`5070d07`](https://github.com/python-gitlab/python-gitlab/commit/5070d07d13b9c87588dbfde3750340e322118779))

- **deps**: Update python-semantic-release/upload-to-gh-release digest to 673709c
  ([`1b550ac`](https://github.com/python-gitlab/python-gitlab/commit/1b550ac706c8c31331a7a9dac607aed49f5e1fcf))

### Features

- More usernames support for MR approvals
  ([`12d195a`](https://github.com/python-gitlab/python-gitlab/commit/12d195a35a1bd14947fbd6688a8ad1bd3fc21617))

I don't think commit a2b8c8ccfb5d went far enough to enable usernames support. We create and edit a
  lot of approval rules based on an external service (similar to CODE_OWNERS), but only have the
  usernames available, and currently, have to look up each user to get their user ID to populate
  user_ids for .set_approvers() calls. Would very much like to skip the lookup and just send the
  usernames, which this change should allow.

See: https://docs.gitlab.com/ee/api/merge_request_approvals.html#create-project-level-rule

Signed-off-by: Jarod Wilson <jarod@redhat.com>

- **api**: Add additional parameter to project/group iteration search
  ([#2796](https://github.com/python-gitlab/python-gitlab/pull/2796),
  [`623dac9`](https://github.com/python-gitlab/python-gitlab/commit/623dac9c8363c61dbf53f72af58835743e96656b))

Co-authored-by: Cristiano Casella <cristiano.casella@seacom.it>

Co-authored-by: Nejc Habjan <hab.nejc@gmail.com>

- **api**: Add support for gitlab service account
  ([#2851](https://github.com/python-gitlab/python-gitlab/pull/2851),
  [`b187dea`](https://github.com/python-gitlab/python-gitlab/commit/b187deadabbfdf0326ecd79a3ee64c9de10c53e0))

Co-authored-by: Nejc Habjan <hab.nejc@siemens.com>


## v4.5.0 (2024-05-13)

### Bug Fixes

- Consider `scope` an ArrayAttribute in PipelineJobManager
  ([`c5d0404`](https://github.com/python-gitlab/python-gitlab/commit/c5d0404ac9edfbfd328e7b4f07f554366377df3f))

List query params like 'scope' were not being handled correctly for pipeline/jobs endpoint. This
  change ensures multiple values are appended with '[]', resulting in the correct URL structure.

Signed-off-by: Guilherme Gallo <guilherme.gallo@collabora.com>

---

Background: If one queries for pipeline jobs with `scope=["failed", "success"]`

One gets: GET /api/v4/projects/176/pipelines/1113028/jobs?scope=success&scope=failed

But it is supposed to get: GET
  /api/v4/projects/176/pipelines/1113028/jobs?scope[]=success&scope[]=failed

The current version only considers the last element of the list argument.

- User.warn() to show correct filename of issue
  ([`529f1fa`](https://github.com/python-gitlab/python-gitlab/commit/529f1faacee46a88cb0a542306309eb835516796))

Previously would only go to the 2nd level of the stack for determining the offending filename and
  line number. When it should be showing the first filename outside of the python-gitlab source
  code. As we want it to show the warning for the user of the libraries code.

Update test to show it works as expected.

- **api**: Fix saving merge request approval rules
  ([`b8b3849`](https://github.com/python-gitlab/python-gitlab/commit/b8b3849b2d4d3f2d9e81e5cf4f6b53368f7f0127))

Closes #2548

- **api**: Update manual job status when playing it
  ([`9440a32`](https://github.com/python-gitlab/python-gitlab/commit/9440a3255018d6a6e49269caf4c878d80db508a8))

- **cli**: Allow exclusive arguments as optional
  ([#2770](https://github.com/python-gitlab/python-gitlab/pull/2770),
  [`7ec3189`](https://github.com/python-gitlab/python-gitlab/commit/7ec3189d6eacdb55925e8be886a44d7ee09eb9ca))

* fix(cli): allow exclusive arguments as optional

The CLI takes its arguments from the RequiredOptional, which has three fields: required, optional,
  and exclusive. In practice, the exclusive options are not defined as either required or optional,
  and would not be allowed in the CLI. This changes that, so that exclusive options are also added
  to the argument parser.

* fix(cli): inform argument parser that options are mutually exclusive

* fix(cli): use correct exclusive options, add unit test

Closes #2769

- **test**: Use different ids for merge request, approval rule, project
  ([`c23e6bd`](https://github.com/python-gitlab/python-gitlab/commit/c23e6bd5785205f0f4b4c80321153658fc23fb98))

The original bug was that the merge request identifier was used instead of the approval rule
  identifier. The test didn't notice that because it used `1` for all identifiers. Make these
  identifiers different so that a mixup will become apparent.

### Build System

- Add "--no-cache-dir" to pip commands in Dockerfile
  ([`4ef94c8`](https://github.com/python-gitlab/python-gitlab/commit/4ef94c8260e958873bb626e86d3241daa22f7ce6))

This would not leave cache files in the built docker image.

Additionally, also only build the wheel in the build phase.

On my machine, before this PR, size is 74845395; after this PR, size is 72617713.

### Chores

- Adapt style for black v24
  ([`4e68d32`](https://github.com/python-gitlab/python-gitlab/commit/4e68d32c77ed587ab42d229d9f44c3bc40d1d0e5))

- Add py312 & py313 to tox environment list
  ([`679ddc7`](https://github.com/python-gitlab/python-gitlab/commit/679ddc7587d2add676fd2398cb9673bd1ca272e3))

Even though there isn't a Python 3.13 at this time, this is done for the future. tox is already
  configured to just warn about missing Python versions, but not fail if they don't exist.

- Add tox `labels` to enable running groups of environments
  ([`d7235c7`](https://github.com/python-gitlab/python-gitlab/commit/d7235c74f8605f4abfb11eb257246864c7dcf709))

tox now has a feature of `labels` which allows running groups of environments using the command `tox
  -m LABEL_NAME`. For example `tox -m lint` which has been setup to run the linters.

Bumped the minimum required version of tox to be 4.0, which was released over a year ago.

- Update `mypy` to 1.9.0 and resolve one issue
  ([`dd00bfc`](https://github.com/python-gitlab/python-gitlab/commit/dd00bfc9c832aba0ed377573fe2e9120b296548d))

mypy 1.9.0 flagged one issue in the code. Resolve the issue. Current unit tests already check that a
  `None` value returns `text/plain`. So function is still working as expected.

- Update version of `black` for `pre-commit`
  ([`3501716`](https://github.com/python-gitlab/python-gitlab/commit/35017167a80809a49351f9e95916fafe61c7bfd5))

The version of `black` needs to be updated to be in sync with what is in `requirements-lint.txt`

- **deps**: Update all non-major dependencies
  ([`4f338ae`](https://github.com/python-gitlab/python-gitlab/commit/4f338aed9c583a20ff5944e6ccbba5737c18b0f4))

- **deps**: Update all non-major dependencies
  ([`65d0e65`](https://github.com/python-gitlab/python-gitlab/commit/65d0e6520dcbcf5a708a87960c65fdcaf7e44bf3))

- **deps**: Update all non-major dependencies
  ([`1f0343c`](https://github.com/python-gitlab/python-gitlab/commit/1f0343c1154ca8ae5b1f61de1db2343a2ad652ec))

- **deps**: Update all non-major dependencies
  ([`0e9f4da`](https://github.com/python-gitlab/python-gitlab/commit/0e9f4da30cea507fcf83746008d9de2ee5a3bb9d))

- **deps**: Update all non-major dependencies
  ([`d5b5fb0`](https://github.com/python-gitlab/python-gitlab/commit/d5b5fb00d8947ed9733cbb5a273e2866aecf33bf))

- **deps**: Update all non-major dependencies
  ([`14a3ffe`](https://github.com/python-gitlab/python-gitlab/commit/14a3ffe4cc161be51a39c204350b5cd45c602335))

- **deps**: Update all non-major dependencies
  ([`3c4dcca`](https://github.com/python-gitlab/python-gitlab/commit/3c4dccaf51695334a5057b85d5ff4045739d1ad1))

- **deps**: Update all non-major dependencies
  ([`04c569a`](https://github.com/python-gitlab/python-gitlab/commit/04c569a2130d053e35c1f2520ef8bab09f2f9651))

- **deps**: Update all non-major dependencies
  ([`3c4b27e`](https://github.com/python-gitlab/python-gitlab/commit/3c4b27e64f4b51746b866f240a1291c2637355cc))

- **deps**: Update all non-major dependencies
  ([`7dc2fa6`](https://github.com/python-gitlab/python-gitlab/commit/7dc2fa6e632ed2c9adeb6ed32c4899ec155f6622))

- **deps**: Update all non-major dependencies
  ([`48726fd`](https://github.com/python-gitlab/python-gitlab/commit/48726fde9b3c2424310ff590b366b9fdefa4a146))

- **deps**: Update codecov/codecov-action action to v4
  ([`d2be1f7`](https://github.com/python-gitlab/python-gitlab/commit/d2be1f7608acadcc2682afd82d16d3706b7f7461))

- **deps**: Update dependency black to v24
  ([`f59aee3`](https://github.com/python-gitlab/python-gitlab/commit/f59aee3ddcfaeeb29fcfab4cc6768dff6b5558cb))

- **deps**: Update dependency black to v24.3.0 [security]
  ([`f6e8692`](https://github.com/python-gitlab/python-gitlab/commit/f6e8692cfc84b5af2eb6deec4ae1c4935b42e91c))

- **deps**: Update dependency furo to v2024
  ([`f6fd02d`](https://github.com/python-gitlab/python-gitlab/commit/f6fd02d956529e2c4bce261fe7b3da1442aaea12))

- **deps**: Update dependency jinja2 to v3.1.4 [security]
  ([`8ea10c3`](https://github.com/python-gitlab/python-gitlab/commit/8ea10c360175453c721ad8e27386e642c2b68d88))

- **deps**: Update dependency myst-parser to v3
  ([`9289189`](https://github.com/python-gitlab/python-gitlab/commit/92891890eb4730bc240213a212d392bcb869b800))

- **deps**: Update dependency pytest to v8
  ([`253babb`](https://github.com/python-gitlab/python-gitlab/commit/253babb9a7f8a7d469440fcfe1b2741ddcd8475e))

- **deps**: Update dependency pytest-cov to v5
  ([`db32000`](https://github.com/python-gitlab/python-gitlab/commit/db3200089ea83588ea7ad8bd5a7175d81f580630))

- **deps**: Update dependency pytest-docker to v3
  ([`35d2aec`](https://github.com/python-gitlab/python-gitlab/commit/35d2aec04532919d6dd7b7090bc4d5209eddd10d))

- **deps**: Update gitlab/gitlab-ee docker tag to v16
  ([`ea8c4c2`](https://github.com/python-gitlab/python-gitlab/commit/ea8c4c2bc9f17f510415a697e0fb19cabff4135e))

- **deps**: Update gitlab/gitlab-ee docker tag to v16.11.1-ee.0
  ([`1ed8d6c`](https://github.com/python-gitlab/python-gitlab/commit/1ed8d6c21d3463b2ad09eb553871042e98090ffd))

- **deps**: Update gitlab/gitlab-ee docker tag to v16.11.2-ee.0
  ([`9be48f0`](https://github.com/python-gitlab/python-gitlab/commit/9be48f0bcc2d32b5e8489f62f963389d5d54b2f2))

- **deps**: Update python-semantic-release/python-semantic-release action to v9
  ([`e11d889`](https://github.com/python-gitlab/python-gitlab/commit/e11d889cd19ec1555b2bbee15355a8cdfad61d5f))

### Documentation

- Add FAQ about conflicting parameters
  ([`683ce72`](https://github.com/python-gitlab/python-gitlab/commit/683ce723352cc09e1a4b65db28be981ae6bb9f71))

We have received multiple issues lately about this. Add it to the FAQ.

- Correct rotate token example
  ([`c53e695`](https://github.com/python-gitlab/python-gitlab/commit/c53e6954f097ed10d52b40660d2fba73c2e0e300))

Rotate token returns a dict. Change example to print the entire dict.

Closes: #2836

- How to run smoke tests
  ([`2d1f487`](https://github.com/python-gitlab/python-gitlab/commit/2d1f4872390df10174f865f7a935bc73f7865fec))

Signed-off-by: Tim Knight <tim.knight1@engineering.digital.dwp.gov.uk>

- Note how to use the Docker image from within GitLab CI
  ([`6d4bffb`](https://github.com/python-gitlab/python-gitlab/commit/6d4bffb5aaa676d32fc892ef1ac002973bc040cb))

Ref: #2823

- **artifacts**: Fix argument indentation
  ([`c631eeb`](https://github.com/python-gitlab/python-gitlab/commit/c631eeb55556920f5975b1fa2b1a0354478ce3c0))

- **objects**: Minor rst formatting typo
  ([`57dfd17`](https://github.com/python-gitlab/python-gitlab/commit/57dfd1769b4e22b43dc0936aa3600cd7e78ba289))

To correctly format a code block have to use `::`

- **README**: Tweak GitLab CI usage docs
  ([`d9aaa99`](https://github.com/python-gitlab/python-gitlab/commit/d9aaa994568ad4896a1e8a0533ef0d1d2ba06bfa))

### Features

- **api**: Allow updating protected branches
  ([#2771](https://github.com/python-gitlab/python-gitlab/pull/2771),
  [`a867c48`](https://github.com/python-gitlab/python-gitlab/commit/a867c48baa6f10ffbfb785e624a6e3888a859571))

* feat(api): allow updating protected branches

Closes #2390

- **cli**: Allow skipping initial auth calls
  ([`001e596`](https://github.com/python-gitlab/python-gitlab/commit/001e59675f4a417a869f813d79c298a14268b87d))

- **job_token_scope**: Support Groups in job token allowlist API
  ([#2816](https://github.com/python-gitlab/python-gitlab/pull/2816),
  [`2d1b749`](https://github.com/python-gitlab/python-gitlab/commit/2d1b7499a93db2c9600b383e166f7463a5f22085))

* feat(job_token_scope): support job token access allowlist API

Signed-off-by: Tim Knight <tim.knight1@engineering.digital.dwp.gov.uk>

l.dwp.gov.uk> Co-authored-by: Nejc Habjan <nejc.habjan@siemens.com>

### Testing

- Don't use weak passwords
  ([`c64d126`](https://github.com/python-gitlab/python-gitlab/commit/c64d126142cc77eae4297b8deec27bb1d68b7a13))

Newer versions of GitLab will refuse to create a user with a weak password. In order for us to move
  to a newer GitLab version in testing use a stronger password for the tests that create a user.

- Remove approve step
  ([`48a6705`](https://github.com/python-gitlab/python-gitlab/commit/48a6705558c5ab6fb08c62a18de350a5985099f8))

Signed-off-by: Tim Knight <tim.knight1@engineering.digital.dwp.gov.uk>

- Tidy up functional tests
  ([`06266ea`](https://github.com/python-gitlab/python-gitlab/commit/06266ea5966c601c035ad8ce5840729e5f9baa57))

Signed-off-by: Tim Knight <tim.knight1@engineering.digital.dwp.gov.uk>

- Update api tests for GL 16.10
  ([`4bef473`](https://github.com/python-gitlab/python-gitlab/commit/4bef47301342703f87c1ce1d2920d54f9927a66a))

- Make sure we're testing python-gitlab functionality, make sure we're not awaiting on Gitlab Async
  functions - Decouple and improve test stability

Signed-off-by: Tim Knight <tim.knight1@engineering.digital.dwp.gov.uk>

- Update tests for gitlab 16.8 functionality
  ([`f8283ae`](https://github.com/python-gitlab/python-gitlab/commit/f8283ae69efd86448ae60d79dd8321af3f19ba1b))

- use programmatic dates for expires_at in tokens tests - set PAT for 16.8 into tests

Signed-off-by: Tim Knight <tim.knight1@engineering.digital.dwp.gov.uk>

- **functional**: Enable bulk import feature flag before test
  ([`b81da2e`](https://github.com/python-gitlab/python-gitlab/commit/b81da2e66ce385525730c089dbc2a5a85ba23287))

- **smoke**: Normalize all dist titles for smoke tests
  ([`ee013fe`](https://github.com/python-gitlab/python-gitlab/commit/ee013fe1579b001b4b30bae33404e827c7bdf8c1))


## v4.4.0 (2024-01-15)

### Bug Fixes

- **cli**: Support binary files with `@` notation
  ([`57749d4`](https://github.com/python-gitlab/python-gitlab/commit/57749d46de1d975aacb82758c268fc26e5e6ed8b))

Support binary files being used in the CLI with arguments using the `@` notation. For example
  `--avatar @/path/to/avatar.png`

Also explicitly catch the common OSError exception, which is the parent exception for things like:
  FileNotFoundError, PermissionError and more exceptions.

Remove the bare exception handling. We would rather have the full traceback of any exceptions that
  we don't know about and add them later if needed.

Closes: #2752

### Chores

- **ci**: Add Python 3.13 development CI job
  ([`ff0c11b`](https://github.com/python-gitlab/python-gitlab/commit/ff0c11b7b75677edd85f846a4dbdab08491a6bd7))

Add a job to test the development versions of Python 3.13.

- **ci**: Align upload and download action versions
  ([`dcca59d`](https://github.com/python-gitlab/python-gitlab/commit/dcca59d1a5966283c1120cfb639c01a76214d2b2))

- **deps**: Update actions/upload-artifact action to v4
  ([`7114af3`](https://github.com/python-gitlab/python-gitlab/commit/7114af341dd12b7fb63ffc08650c455ead18ab70))

- **deps**: Update all non-major dependencies
  ([`550f935`](https://github.com/python-gitlab/python-gitlab/commit/550f9355d29a502bb022f68dab6c902bf6913552))

- **deps**: Update all non-major dependencies
  ([`cbc13a6`](https://github.com/python-gitlab/python-gitlab/commit/cbc13a61e0f15880b49a3d0208cc603d7d0b57e3))

- **deps**: Update all non-major dependencies
  ([`369a595`](https://github.com/python-gitlab/python-gitlab/commit/369a595a8763109a2af8a95a8e2423ebb30b9320))

- **deps**: Update dependency flake8 to v7
  ([`20243c5`](https://github.com/python-gitlab/python-gitlab/commit/20243c532a8a6d28eee0caff5b9c30cc7376a162))

- **deps**: Update dependency jinja2 to v3.1.3 [security]
  ([`880913b`](https://github.com/python-gitlab/python-gitlab/commit/880913b67cce711d96e89ce6813e305e4ba10908))

- **deps**: Update pre-commit hook pycqa/flake8 to v7
  ([`9a199b6`](https://github.com/python-gitlab/python-gitlab/commit/9a199b6089152e181e71a393925e0ec581bc55ca))

### Features

- **api**: Add reviewer_details manager for mergrequest to get reviewers of merge request
  ([`adbd90c`](https://github.com/python-gitlab/python-gitlab/commit/adbd90cadffe1d9e9716a6e3826f30664866ad3f))

Those changes implements 'GET /projects/:id/merge_requests/:merge_request_iid/reviewers' gitlab API
  call. Naming for call is not reviewers because reviewers atribute already presen in merge request
  response

- **api**: Support access token rotate API
  ([`b13971d`](https://github.com/python-gitlab/python-gitlab/commit/b13971d5472cb228f9e6a8f2fa05a7cc94d03ebe))

- **api**: Support single resource access token get API
  ([`dae9e52`](https://github.com/python-gitlab/python-gitlab/commit/dae9e522a26041f5b3c6461cc8a5e284f3376a79))


## v4.3.0 (2023-12-28)

### Bug Fixes

- **cli**: Add ability to disable SSL verification
  ([`3fe9fa6`](https://github.com/python-gitlab/python-gitlab/commit/3fe9fa64d9a38bc77950046f2950660d8d7e27a6))

Add a `--no-ssl-verify` option to disable SSL verification

Closes: #2714

### Chores

- **deps**: Update actions/setup-python action to v5
  ([`fad1441`](https://github.com/python-gitlab/python-gitlab/commit/fad14413f4f27f1b6f902703b5075528aac52451))

- **deps**: Update actions/stale action to v9
  ([`c01988b`](https://github.com/python-gitlab/python-gitlab/commit/c01988b12c7745929d0c591f2fa265df2929a859))

- **deps**: Update all non-major dependencies
  ([`d7bdb02`](https://github.com/python-gitlab/python-gitlab/commit/d7bdb0257a5587455c3722f65c4a632f24d395be))

- **deps**: Update all non-major dependencies
  ([`9e067e5`](https://github.com/python-gitlab/python-gitlab/commit/9e067e5c67dcf9f5e6c3408b30d9e2525c768e0a))

- **deps**: Update all non-major dependencies
  ([`bb2af7b`](https://github.com/python-gitlab/python-gitlab/commit/bb2af7bfe8aa59ea8b9ad7ca2d6e56f4897b704a))

- **deps**: Update all non-major dependencies
  ([`5ef1b4a`](https://github.com/python-gitlab/python-gitlab/commit/5ef1b4a6c8edd34c381c6e08cd3893ef6c0685fd))

- **deps**: Update dependency types-setuptools to v69
  ([`de11192`](https://github.com/python-gitlab/python-gitlab/commit/de11192455f1c801269ecb3bdcbc7c5b769ff354))

### Documentation

- Fix rst link typo in CONTRIBUTING.rst
  ([`2b6da6e`](https://github.com/python-gitlab/python-gitlab/commit/2b6da6e63c82a61b8e21d193cfd46baa3fcf8937))

### Features

- **api**: Add support for the Draft notes API
  ([#2728](https://github.com/python-gitlab/python-gitlab/pull/2728),
  [`ebf9d82`](https://github.com/python-gitlab/python-gitlab/commit/ebf9d821cfc36071fca05d38b82c641ae30c974c))

* feat(api): add support for the Draft notes API

* fix(client): handle empty 204 reponses in PUT requests


## v4.2.0 (2023-11-28)

### Chores

- **deps**: Update all non-major dependencies
  ([`8aeb853`](https://github.com/python-gitlab/python-gitlab/commit/8aeb8531ebd3ddf0d1da3fd74597356ef65c00b3))

- **deps**: Update all non-major dependencies
  ([`9fe2335`](https://github.com/python-gitlab/python-gitlab/commit/9fe2335b9074feaabdb683b078ff8e12edb3959e))

- **deps**: Update all non-major dependencies
  ([`91e66e9`](https://github.com/python-gitlab/python-gitlab/commit/91e66e9b65721fa0e890a6664178d77ddff4272a))

- **deps**: Update all non-major dependencies
  ([`d0546e0`](https://github.com/python-gitlab/python-gitlab/commit/d0546e043dfeb988a161475de53d4ec7d756bdd9))

- **deps**: Update dessant/lock-threads action to v5
  ([`f4ce867`](https://github.com/python-gitlab/python-gitlab/commit/f4ce86770befef77c7c556fd5cfe25165f59f515))

### Features

- Add pipeline status as Enum
  ([`4954bbc`](https://github.com/python-gitlab/python-gitlab/commit/4954bbcd7e8433aac672405f3f4741490cb4561a))

https://docs.gitlab.com/ee/api/pipelines.html

- **api**: Add support for wiki attachments
  ([#2722](https://github.com/python-gitlab/python-gitlab/pull/2722),
  [`7b864b8`](https://github.com/python-gitlab/python-gitlab/commit/7b864b81fd348c6a42e32ace846d1acbcfc43998))

Added UploadMixin in mixin module Added UploadMixin dependency for Project, ProjectWiki, GroupWiki
  Added api tests for wiki upload Added unit test for mixin Added docs sections to wikis.rst


## v4.1.1 (2023-11-03)

### Bug Fixes

- **build**: Include py.typed in dists
  ([`b928639`](https://github.com/python-gitlab/python-gitlab/commit/b928639f7ca252e0abb8ded8f9f142316a4dc823))

### Chores

- **ci**: Add release id to workflow step
  ([`9270e10`](https://github.com/python-gitlab/python-gitlab/commit/9270e10d94101117bec300c756889e4706f41f36))

- **deps**: Update all non-major dependencies
  ([`32954fb`](https://github.com/python-gitlab/python-gitlab/commit/32954fb95dcc000100b48c4b0b137ebe2eca85a3))

### Documentation

- **users**: Add missing comma in v4 API create runner examples
  ([`b1b2edf`](https://github.com/python-gitlab/python-gitlab/commit/b1b2edfa05be8b957c796dc6d111f40c9f753dcf))

The examples which show usage of new runner registration api endpoint are missing commas. This
  change adds the missing commas.


## v4.1.0 (2023-10-28)

### Bug Fixes

- Remove depricated MergeStatus
  ([`c6c012b`](https://github.com/python-gitlab/python-gitlab/commit/c6c012b9834b69f1fe45689519fbcd92928cfbad))

### Chores

- Add source label to container image
  ([`7b19278`](https://github.com/python-gitlab/python-gitlab/commit/7b19278ac6b7a106bc518f264934c7878ffa49fb))

- **CHANGELOG**: Re-add v4.0.0 changes using old format
  ([`258a751`](https://github.com/python-gitlab/python-gitlab/commit/258a751049c8860e39097b26d852d1d889892d7a))

- **CHANGELOG**: Revert python-semantic-release format change
  ([`b5517e0`](https://github.com/python-gitlab/python-gitlab/commit/b5517e07da5109b1a43db876507d8000d87070fe))

- **deps**: Update all non-major dependencies
  ([`bf68485`](https://github.com/python-gitlab/python-gitlab/commit/bf68485613756e9916de1bb10c8c4096af4ffd1e))

- **rtd**: Revert to python 3.11 ([#2694](https://github.com/python-gitlab/python-gitlab/pull/2694),
  [`1113742`](https://github.com/python-gitlab/python-gitlab/commit/1113742d55ea27da121853130275d4d4de45fd8f))

### Continuous Integration

- Remove unneeded GitLab auth
  ([`fd7bbfc`](https://github.com/python-gitlab/python-gitlab/commit/fd7bbfcb9500131e5d3a263d7b97c8b59f80b7e2))

### Features

- Add Merge Request merge_status and detailed_merge_status values as constants
  ([`e18a424`](https://github.com/python-gitlab/python-gitlab/commit/e18a4248068116bdcb7af89897a0c4c500f7ba57))


## v4.0.0 (2023-10-17)

### Bug Fixes

- **cli**: Add _from_parent_attrs to user-project manager
  ([#2558](https://github.com/python-gitlab/python-gitlab/pull/2558),
  [`016d90c`](https://github.com/python-gitlab/python-gitlab/commit/016d90c3c22bfe6fc4e866d120d2c849764ef9d2))

- **cli**: Fix action display in --help when there are few actions
  ([`b22d662`](https://github.com/python-gitlab/python-gitlab/commit/b22d662a4fd8fb8a9726760b645d4da6197bfa9a))

fixes #2656

- **cli**: Remove deprecated `--all` option in favor of `--get-all`
  ([`e9d48cf`](https://github.com/python-gitlab/python-gitlab/commit/e9d48cf69e0dbe93f917e6f593d31327cd99f917))

BREAKING CHANGE: The `--all` option is no longer available in the CLI. Use `--get-all` instead.

- **client**: Support empty 204 responses in http_patch
  ([`e15349c`](https://github.com/python-gitlab/python-gitlab/commit/e15349c9a796f2d82f72efbca289740016c47716))

- **snippets**: Allow passing list of files
  ([`31c3c5e`](https://github.com/python-gitlab/python-gitlab/commit/31c3c5ea7cbafb4479825ec40bc34e3b8cb427fd))

### Chores

- Add package pipelines API link
  ([`2a2404f`](https://github.com/python-gitlab/python-gitlab/commit/2a2404fecdff3483a68f538c8cd6ba4d4fc6538c))

- Change `_update_uses` to `_update_method` and use an Enum
  ([`7073a2d`](https://github.com/python-gitlab/python-gitlab/commit/7073a2dfa3a4485d2d3a073d40122adbeff42b5c))

Change the name of the `_update_uses` attribute to `_update_method` and store an Enum in the
  attribute to indicate which type of HTTP method to use. At the moment it supports `POST` and
  `PUT`. But can in the future support `PATCH`.

- Fix test names
  ([`f1654b8`](https://github.com/python-gitlab/python-gitlab/commit/f1654b8065a7c8349777780e673aeb45696fccd0))

- Make linters happy
  ([`3b83d5d`](https://github.com/python-gitlab/python-gitlab/commit/3b83d5d13d136f9a45225929a0c2031dc28cdbed))

- Switch to docker-compose v2
  ([`713b5ca`](https://github.com/python-gitlab/python-gitlab/commit/713b5ca272f56b0fd7340ca36746e9649a416aa2))

Closes: #2625

- Update PyYAML to 6.0.1
  ([`3b8939d`](https://github.com/python-gitlab/python-gitlab/commit/3b8939d7669f391a5a7e36d623f8ad6303ba7712))

Fixes issue with CI having error: `AttributeError: cython_sources`

Closes: #2624

- **ci**: Adapt release workflow and config for v8
  ([`827fefe`](https://github.com/python-gitlab/python-gitlab/commit/827fefeeb7bf00e5d8fa142d7686ead97ca4b763))

- **ci**: Fix pre-commit deps and python version
  ([`1e7f257`](https://github.com/python-gitlab/python-gitlab/commit/1e7f257e79a7adf1e6f2bc9222fd5031340d26c3))

- **ci**: Follow upstream config for release build_command
  ([`3e20a76`](https://github.com/python-gitlab/python-gitlab/commit/3e20a76fdfc078a03190939bda303577b2ef8614))

- **ci**: Remove Python 3.13 dev job
  ([`e8c50f2`](https://github.com/python-gitlab/python-gitlab/commit/e8c50f28da7e3879f0dc198533041348a14ddc68))

- **ci**: Update release build for python-semantic-release v8
  ([#2692](https://github.com/python-gitlab/python-gitlab/pull/2692),
  [`bf050d1`](https://github.com/python-gitlab/python-gitlab/commit/bf050d19508978cbaf3e89d49f42162273ac2241))

- **deps**: Bring furo up to date with sphinx
  ([`a15c927`](https://github.com/python-gitlab/python-gitlab/commit/a15c92736f0cf78daf78f77fb318acc6c19036a0))

- **deps**: Bring myst-parser up to date with sphinx 7
  ([`da03e9c`](https://github.com/python-gitlab/python-gitlab/commit/da03e9c7dc1c51978e51fedfc693f0bce61ddaf1))

- **deps**: Pin pytest-console-scripts for 3.7
  ([`6d06630`](https://github.com/python-gitlab/python-gitlab/commit/6d06630cac1a601bc9a17704f55dcdc228285e88))

- **deps**: Update actions/checkout action to v3
  ([`e2af1e8`](https://github.com/python-gitlab/python-gitlab/commit/e2af1e8a964fe8603dddef90a6df62155f25510d))

- **deps**: Update actions/checkout action to v4
  ([`af13914`](https://github.com/python-gitlab/python-gitlab/commit/af13914e41f60cc2c4ef167afb8f1a10095e8a00))

- **deps**: Update actions/setup-python action to v4
  ([`e0d6783`](https://github.com/python-gitlab/python-gitlab/commit/e0d6783026784bf1e6590136da3b35051e7edbb3))

- **deps**: Update actions/upload-artifact action to v3
  ([`b78d6bf`](https://github.com/python-gitlab/python-gitlab/commit/b78d6bfd18630fa038f5f5bd8e473ec980495b10))

- **deps**: Update all non-major dependencies
  ([`1348a04`](https://github.com/python-gitlab/python-gitlab/commit/1348a040207fc30149c664ac0776e698ceebe7bc))

- **deps**: Update all non-major dependencies
  ([`ff45124`](https://github.com/python-gitlab/python-gitlab/commit/ff45124e657c4ac4ec843a13be534153a8b10a20))

- **deps**: Update all non-major dependencies
  ([`0d49164`](https://github.com/python-gitlab/python-gitlab/commit/0d491648d16f52f5091b23d0e3e5be2794461ade))

- **deps**: Update all non-major dependencies
  ([`6093dbc`](https://github.com/python-gitlab/python-gitlab/commit/6093dbcf07b9edf35379142ea58a190050cf7fe7))

- **deps**: Update all non-major dependencies
  ([`bb728b1`](https://github.com/python-gitlab/python-gitlab/commit/bb728b1c259dba5699467c9ec7a51b298a9e112e))

- **deps**: Update all non-major dependencies
  ([`9083787`](https://github.com/python-gitlab/python-gitlab/commit/9083787f0855d94803c633b0491db70f39a9867a))

- **deps**: Update all non-major dependencies
  ([`b6a3db1`](https://github.com/python-gitlab/python-gitlab/commit/b6a3db1a2b465a34842d1a544a5da7eee6430708))

- **deps**: Update all non-major dependencies
  ([`16f2d34`](https://github.com/python-gitlab/python-gitlab/commit/16f2d3428e673742a035856b1fb741502287cc1d))

- **deps**: Update all non-major dependencies
  ([`5b33ade`](https://github.com/python-gitlab/python-gitlab/commit/5b33ade92152e8ccb9db3eb369b003a688447cd6))

- **deps**: Update all non-major dependencies
  ([`3732841`](https://github.com/python-gitlab/python-gitlab/commit/37328416d87f50f64c9bdbdcb49e9b9a96d2d0ef))

- **deps**: Update all non-major dependencies
  ([`511f45c`](https://github.com/python-gitlab/python-gitlab/commit/511f45cda08d457263f1011b0d2e013e9f83babc))

- **deps**: Update all non-major dependencies
  ([`d4a7410`](https://github.com/python-gitlab/python-gitlab/commit/d4a7410e55c6a98a15f4d7315cc3d4fde0190bce))

- **deps**: Update all non-major dependencies
  ([`12846cf`](https://github.com/python-gitlab/python-gitlab/commit/12846cfe4a0763996297bb0a43aa958fe060f029))

- **deps**: Update all non-major dependencies
  ([`33d2aa2`](https://github.com/python-gitlab/python-gitlab/commit/33d2aa21035515711738ac192d8be51fd6106863))

- **deps**: Update all non-major dependencies
  ([`5ff56d8`](https://github.com/python-gitlab/python-gitlab/commit/5ff56d866c6fdac524507628cf8baf2c498347af))

- **deps**: Update all non-major dependencies
  ([`7586a5c`](https://github.com/python-gitlab/python-gitlab/commit/7586a5c80847caf19b16282feb25be470815729b))

- **deps**: Update all non-major dependencies to v23.9.1
  ([`a16b732`](https://github.com/python-gitlab/python-gitlab/commit/a16b73297a3372ce4f3ada3b4ea99680dbd511f6))

- **deps**: Update dependency build to v1
  ([`2e856f2`](https://github.com/python-gitlab/python-gitlab/commit/2e856f24567784ddc35ca6895d11bcca78b58ca4))

- **deps**: Update dependency commitizen to v3.10.0
  ([`becd8e2`](https://github.com/python-gitlab/python-gitlab/commit/becd8e20eb66ce4e606f22c15abf734a712c20c3))

- **deps**: Update dependency pylint to v3
  ([`491350c`](https://github.com/python-gitlab/python-gitlab/commit/491350c40a74bbb4945dfb9f2618bcc5420a4603))

- **deps**: Update dependency pytest-docker to v2
  ([`b87bb0d`](https://github.com/python-gitlab/python-gitlab/commit/b87bb0db1441d1345048664b15bd8122e6b95be4))

- **deps**: Update dependency setuptools to v68
  ([`0f06082`](https://github.com/python-gitlab/python-gitlab/commit/0f06082272f7dbcfd79f895de014cafed3205ff6))

- **deps**: Update dependency sphinx to v7
  ([`2918dfd`](https://github.com/python-gitlab/python-gitlab/commit/2918dfd78f562e956c5c53b79f437a381e51ebb7))

- **deps**: Update dependency types-setuptools to v68
  ([`bdd4eb6`](https://github.com/python-gitlab/python-gitlab/commit/bdd4eb694f8b56d15d33956cb982a71277ca907f))

- **deps**: Update dependency ubuntu to v22
  ([`8865552`](https://github.com/python-gitlab/python-gitlab/commit/88655524ac2053f5b7016457f8c9d06a4b888660))

- **deps**: Update pre-commit hook commitizen-tools/commitizen to v3.10.0
  ([`626c2f8`](https://github.com/python-gitlab/python-gitlab/commit/626c2f8879691e5dd4ce43118668e6a88bf6f7ad))

- **deps**: Update pre-commit hook maxbrunet/pre-commit-renovate to v36
  ([`db58cca`](https://github.com/python-gitlab/python-gitlab/commit/db58cca2e2b7d739b069904cb03f42c9bc1d3810))

- **deps**: Update pre-commit hook maxbrunet/pre-commit-renovate to v37
  ([`b4951cd`](https://github.com/python-gitlab/python-gitlab/commit/b4951cd273d599e6d93b251654808c6eded2a960))

- **deps**: Update pre-commit hook pycqa/pylint to v3
  ([`0f4a346`](https://github.com/python-gitlab/python-gitlab/commit/0f4a34606f4df643a5dbae1900903bcf1d47b740))

- **deps**: Update relekang/python-semantic-release action to v8
  ([`c57c85d`](https://github.com/python-gitlab/python-gitlab/commit/c57c85d0fc6543ab5a2322fc58ec1854afc4f54f))

- **helpers**: Fix previously undetected flake8 issue
  ([`bf8bd73`](https://github.com/python-gitlab/python-gitlab/commit/bf8bd73e847603e8ac5d70606f9393008eee1683))

- **rtd**: Fix docs build on readthedocs.io
  ([#2654](https://github.com/python-gitlab/python-gitlab/pull/2654),
  [`3d7139b`](https://github.com/python-gitlab/python-gitlab/commit/3d7139b64853cb0da46d0ef6a4bccc0175f616c2))

- **rtd**: Use readthedocs v2 syntax
  ([`6ce2149`](https://github.com/python-gitlab/python-gitlab/commit/6ce214965685a3e73c02e9b93446ad8d9a29262e))

### Documentation

- Correct error with back-ticks ([#2653](https://github.com/python-gitlab/python-gitlab/pull/2653),
  [`0b98dd3`](https://github.com/python-gitlab/python-gitlab/commit/0b98dd3e92179652806a7ae8ccc7ec5cddd2b260))

New linting package update detected the issue.

- **access_token**: Adopt token docs to 16.1
  ([`fe7a971`](https://github.com/python-gitlab/python-gitlab/commit/fe7a971ad3ea1e66ffc778936296e53825c69f8f))

expires_at is now required Upstream MR: https://gitlab.com/gitlab-org/gitlab/-/merge_requests/124964

- **advanced**: Document new netrc behavior
  ([`45b8930`](https://github.com/python-gitlab/python-gitlab/commit/45b89304d9745be1b87449805bf53d45bf740e90))

BREAKING CHANGE: python-gitlab now explicitly passes auth to requests, meaning it will only read
  netrc credentials if no token is provided, fixing a bug where netrc credentials took precedence
  over OAuth tokens. This also affects the CLI, where all environment variables now take precedence
  over netrc files.

- **files**: Fix minor typo in variable declaration
  ([`118ce42`](https://github.com/python-gitlab/python-gitlab/commit/118ce4282abc4397c4e9370407b1ab6866de9f97))

### Features

- Added iteration to issue and group filters
  ([`8d2d297`](https://github.com/python-gitlab/python-gitlab/commit/8d2d2971c3909fb5461a9f7b2d07508866cd456c))

- Officially support Python 3.12
  ([`2a69c0e`](https://github.com/python-gitlab/python-gitlab/commit/2a69c0ee0a86315a3ed4750f59bd6ab3e4199b8e))

- Remove support for Python 3.7, require 3.8 or higher
  ([`058d5a5`](https://github.com/python-gitlab/python-gitlab/commit/058d5a56c284c771f1fb5fad67d4ef2eeb4d1916))

Python 3.8 is End-of-Life (EOL) as of 2023-06-27 as stated in https://devguide.python.org/versions/
  and https://peps.python.org/pep-0537/

By dropping support for Python 3.7 and requiring Python 3.8 or higher it allows python-gitlab to
  take advantage of new features in Python 3.8, which are documented at:
  https://docs.python.org/3/whatsnew/3.8.html

BREAKING CHANGE: As of python-gitlab 4.0.0, Python 3.7 is no longer supported. Python 3.8 or higher
  is required.

- Use requests AuthBase classes
  ([`5f46cfd`](https://github.com/python-gitlab/python-gitlab/commit/5f46cfd235dbbcf80678e45ad39a2c3b32ca2e39))

- **api**: Add optional GET attrs for /projects/:id/ci/lint
  ([`40a102d`](https://github.com/python-gitlab/python-gitlab/commit/40a102d4f5c8ff89fae56cd9b7c8030c5070112c))

- **api**: Add ProjectPackagePipeline
  ([`5b4addd`](https://github.com/python-gitlab/python-gitlab/commit/5b4addda59597a5f363974e59e5ea8463a0806ae))

Add ProjectPackagePipeline, which is scheduled to be included in GitLab 16.0

- **api**: Add support for job token scope settings
  ([`59d6a88`](https://github.com/python-gitlab/python-gitlab/commit/59d6a880aacd7cf6f443227071bb8288efb958c4))

- **api**: Add support for new runner creation API
  ([#2635](https://github.com/python-gitlab/python-gitlab/pull/2635),
  [`4abcd17`](https://github.com/python-gitlab/python-gitlab/commit/4abcd1719066edf9ecc249f2da4a16c809d7b181))

Co-authored-by: Nejc Habjan <hab.nejc@gmail.com>

- **api**: Support project remote mirror deletion
  ([`d900910`](https://github.com/python-gitlab/python-gitlab/commit/d9009100ec762c307b46372243d93f9bc2de7a2b))

- **client**: Mask tokens by default when logging
  ([`1611d78`](https://github.com/python-gitlab/python-gitlab/commit/1611d78263284508326347843f634d2ca8b41215))

- **packages**: Allow uploading bytes and files
  ([`61e0fae`](https://github.com/python-gitlab/python-gitlab/commit/61e0faec2014919e0a2e79106089f6838be8ad0e))

This commit adds a keyword argument to GenericPackageManager.upload() to allow uploading bytes and
  file-like objects to the generic package registry. That necessitates changing file path to be a
  keyword argument as well, which then cascades into a whole slew of checks to not allow passing
  both and to not allow uploading file-like objects as JSON data.

Closes https://github.com/python-gitlab/python-gitlab/issues/1815

- **releases**: Add support for direct_asset_path
  ([`d054917`](https://github.com/python-gitlab/python-gitlab/commit/d054917ccb3bbcc9973914409b9e34ba9301663a))

This commit adds support for the “new” alias for `filepath`: `direct_asset_path` (added in 15.10) in
  release links API.

### Refactoring

- **artifacts**: Remove deprecated `artifact()`in favor of `artifacts.raw()`
  ([`90134c9`](https://github.com/python-gitlab/python-gitlab/commit/90134c949b38c905f9cacf3b4202c25dec0282f3))

BREAKING CHANGE: The deprecated `project.artifact()` method is no longer available. Use
  `project.artifacts.raw()` instead.

- **artifacts**: Remove deprecated `artifacts()`in favor of `artifacts.download()`
  ([`42639f3`](https://github.com/python-gitlab/python-gitlab/commit/42639f3ec88f3a3be32e36b97af55240e98c1d9a))

BREAKING CHANGE: The deprecated `project.artifacts()` method is no longer available. Use
  `project.artifacts.download()` instead.

- **build**: Build project using PEP 621
  ([`71fca8c`](https://github.com/python-gitlab/python-gitlab/commit/71fca8c8f5c7f3d6ab06dd4e6c0d91003705be09))

BREAKING CHANGE: python-gitlab now stores metadata in pyproject.toml as per PEP 621, with setup.py
  removed. pip version v21.1 or higher is required if you want to perform an editable install.

- **const**: Remove deprecated global constant import
  ([`e4a1f6e`](https://github.com/python-gitlab/python-gitlab/commit/e4a1f6e2d1c4e505f38f9fd948d0fea9520aa909))

BREAKING CHANGE: Constants defined in `gitlab.const` can no longer be imported globally from
  `gitlab`. Import them from `gitlab.const` instead.

- **groups**: Remove deprecated LDAP group link add/delete methods
  ([`5c8b7c1`](https://github.com/python-gitlab/python-gitlab/commit/5c8b7c1369a28d75261002e7cb6d804f7d5658c6))

BREAKING CHANGE: The deprecated `group.add_ldap_group_link()` and `group.delete_ldap_group_link()`
  methods are no longer available. Use `group.ldap_group_links.create()` and
  `group.ldap_group_links.delete()` instead.

- **lint**: Remove deprecated `lint()`in favor of `ci_lint.create()`
  ([`0b17a2d`](https://github.com/python-gitlab/python-gitlab/commit/0b17a2d24a3f9463dfbcab6b4fddfba2aced350b))

BREAKING CHANGE: The deprecated `lint()` method is no longer available. Use `ci_lint.create()`
  instead.

- **list**: `as_list` support is removed.
  ([`9b6d89e`](https://github.com/python-gitlab/python-gitlab/commit/9b6d89edad07979518a399229c6f55bffeb9af08))

In `list()` calls support for the `as_list` argument has been removed. `as_list` was previously
  deprecated and now the use of `iterator` will be required if wanting to have same functionality as
  using `as_list`

BREAKING CHANGE: Support for the deprecated `as_list` argument in `list()` calls has been removed.
  Use `iterator` instead.

- **projects**: Remove deprecated `project.transfer_project()` in favor of `project.transfer()`
  ([`27ed490`](https://github.com/python-gitlab/python-gitlab/commit/27ed490c22008eef383e1a346ad0c721cdcc6198))

BREAKING CHANGE: The deprecated `project.transfer_project()` method is no longer available. Use
  `project.transfer()` instead.

### Testing

- Add tests for token masking
  ([`163bfcf`](https://github.com/python-gitlab/python-gitlab/commit/163bfcf6c2c1ccc4710c91e6f75b51e630dfb719))

- Correct calls to `script_runner.run()`
  ([`cd04315`](https://github.com/python-gitlab/python-gitlab/commit/cd04315de86aca2bb471865b2754bb66e96f0119))

Warnings were being raised. Resolve those warnings.

- Fix failing tests that use 204 (No Content) plus content
  ([`3074f52`](https://github.com/python-gitlab/python-gitlab/commit/3074f522551b016451aa968f22a3dc5715db281b))

urllib3>=2 now checks for expected content length. Also codes 204 and 304 are set to expect a
  content length of 0 [1]

So in the unit tests stop setting content to return in these situations.

[1]
  https://github.com/urllib3/urllib3/blob/88a707290b655394aade060a8b7eaee83152dc8b/src/urllib3/response.py#L691-L693

- **cli**: Add test for user-project list
  ([`a788cff`](https://github.com/python-gitlab/python-gitlab/commit/a788cff7c1c651c512f15a9a1045c1e4d449d854))

### BREAKING CHANGES

- **advanced**: Python-gitlab now explicitly passes auth to requests, meaning it will only read
  netrc credentials if no token is provided, fixing a bug where netrc credentials took precedence
  over OAuth tokens. This also affects the CLI, where all environment variables now take precedence
  over netrc files.

- **build**: Python-gitlab now stores metadata in pyproject.toml as per PEP 621, with setup.py
  removed. pip version v21.1 or higher is required if you want to perform an editable install.


## v3.15.0 (2023-06-09)

### Chores

- Update copyright year to include 2023
  ([`511c6e5`](https://github.com/python-gitlab/python-gitlab/commit/511c6e507e4161531732ce4c323aeb4481504b08))

- Update sphinx from 5.3.0 to 6.2.1
  ([`c44a290`](https://github.com/python-gitlab/python-gitlab/commit/c44a29016b13e535621e71ec4f5392b4c9a93552))

- **ci**: Use OIDC trusted publishing for pypi.org
  ([#2559](https://github.com/python-gitlab/python-gitlab/pull/2559),
  [`7be09e5`](https://github.com/python-gitlab/python-gitlab/commit/7be09e52d75ed8ab723d7a65f5e99d98fe6f52b0))

* chore(ci): use OIDC trusted publishing for pypi.org

* chore(ci): explicitly install setuptools in tests

- **deps**: Update all non-major dependencies
  ([`e3de6ba`](https://github.com/python-gitlab/python-gitlab/commit/e3de6bac98edd8a4cb87229e639212b9fb1500f9))

- **deps**: Update dependency commitizen to v3
  ([`784d59e`](https://github.com/python-gitlab/python-gitlab/commit/784d59ef46703c9afc0b1e390f8c4194ee10bb0a))

- **deps**: Update dependency myst-parser to v1
  ([`9c39848`](https://github.com/python-gitlab/python-gitlab/commit/9c3984896c243ad082469ae69342e09d65b5b5ef))

- **deps**: Update dependency requests-toolbelt to v1
  ([`86eba06`](https://github.com/python-gitlab/python-gitlab/commit/86eba06736b7610d8c4e77cd96ae6071c40067d5))

- **deps**: Update dependency types-setuptools to v67
  ([`c562424`](https://github.com/python-gitlab/python-gitlab/commit/c56242413e0eb36e41981f577162be8b69e53b67))

- **deps**: Update pre-commit hook commitizen-tools/commitizen to v3
  ([`1591e33`](https://github.com/python-gitlab/python-gitlab/commit/1591e33f0b315c7eb544dc98a6567c33c2ac143f))

- **deps**: Update pre-commit hook maxbrunet/pre-commit-renovate to v35
  ([`8202e3f`](https://github.com/python-gitlab/python-gitlab/commit/8202e3fe01b34da3ff29a7f4189d80a2153f08a4))

### Documentation

- Remove exclusive EE about issue links
  ([`e0f6f18`](https://github.com/python-gitlab/python-gitlab/commit/e0f6f18f14c8c17ea038a7741063853c105e7fa3))

### Features

- Add support for `select="package_file"` in package upload
  ([`3a49f09`](https://github.com/python-gitlab/python-gitlab/commit/3a49f099d54000089e217b61ffcf60b6a28b4420))

Add ability to use `select="package_file"` when uploading a generic package as described in:
  https://docs.gitlab.com/ee/user/packages/generic_packages/index.html

Closes: #2557

- Usernames support for MR approvals
  ([`a2b8c8c`](https://github.com/python-gitlab/python-gitlab/commit/a2b8c8ccfb5d4fa4d134300861a3bfb0b10246ca))

This can be used instead of 'user_ids'

See: https://docs.gitlab.com/ee/api/merge_request_approvals.html#create-project-level-rule

- **api**: Add support for events scope parameter
  ([`348f56e`](https://github.com/python-gitlab/python-gitlab/commit/348f56e8b95c43a7f140f015d303131665b21772))


## v3.14.0 (2023-04-11)

### Bug Fixes

- Support int for `parent_id` in `import_group`
  ([`90f96ac`](https://github.com/python-gitlab/python-gitlab/commit/90f96acf9e649de9874cec612fc1b49c4a843447))

This will also fix other use cases where an integer is passed in to MultipartEncoder.

Added unit tests to show it works.

Closes: #2506

- **cli**: Add ability to escape at-prefixed parameter
  ([#2513](https://github.com/python-gitlab/python-gitlab/pull/2513),
  [`4f7c784`](https://github.com/python-gitlab/python-gitlab/commit/4f7c78436e62bfd21745c5289117e03ed896bc66))

* fix(cli): Add ability to escape at-prefixed parameter (#2511)

---------

Co-authored-by: Nejc Habjan <hab.nejc@gmail.com>

- **cli**: Display items when iterator is returned
  ([`33a04e7`](https://github.com/python-gitlab/python-gitlab/commit/33a04e74fc42d720c7be32172133a614f7268ec1))

- **cli**: Warn user when no fields are displayed
  ([`8bf53c8`](https://github.com/python-gitlab/python-gitlab/commit/8bf53c8b31704bdb31ffc5cf107cc5fba5dad457))

- **client**: Properly parse content-type when charset is present
  ([`76063c3`](https://github.com/python-gitlab/python-gitlab/commit/76063c386ef9caf84ba866515cb053f6129714d9))

### Chores

- Add Contributor Covenant 2.1 as Code of Conduct
  ([`fe334c9`](https://github.com/python-gitlab/python-gitlab/commit/fe334c91fcb6450f5b3b424c925bf48ec2a3c150))

See https://www.contributor-covenant.org/version/2/1/code_of_conduct/

- Add Python 3.12 testing
  ([`0867564`](https://github.com/python-gitlab/python-gitlab/commit/08675643e6b306d3ae101b173609a6c363c9f3df))

Add a unit test for Python 3.12. This will use the latest version of Python 3.12 that is available
  from https://github.com/actions/python-versions/

At this time it is 3.12.0-alpha.4 but will move forward over time until the final 3.12 release and
  updates. So 3.12.0, 3.12.1, ... will be matched.

- Add SECURITY.md
  ([`572ca3b`](https://github.com/python-gitlab/python-gitlab/commit/572ca3b6bfe190f8681eef24e72b15c1f8ba6da8))

- Remove `pre-commit` as a default `tox` environment
  ([#2470](https://github.com/python-gitlab/python-gitlab/pull/2470),
  [`fde2495`](https://github.com/python-gitlab/python-gitlab/commit/fde2495dd1e97fd2f0e91063946bb08490b3952c))

For users who use `tox` having `pre-commit` as part of the default environment list is redundant as
  it will run the same tests again that are being run in other environments. For example: black,
  flake8, pylint, and more.

- Use a dataclass to return values from `prepare_send_data`
  ([`f2b5e4f`](https://github.com/python-gitlab/python-gitlab/commit/f2b5e4fa375e88d6102a8d023ae2fe8206042545))

I found the tuple of three values confusing. So instead use a dataclass to return the three values.
  It is still confusing but a little bit less so.

Also add some unit tests

- **.github**: Actually make PR template the default
  ([`7a8a862`](https://github.com/python-gitlab/python-gitlab/commit/7a8a86278543a1419d07dd022196e4cb3db12d31))

- **ci**: Wait for all coverage reports in CI status
  ([`511764d`](https://github.com/python-gitlab/python-gitlab/commit/511764d2fc4e524eff0d7cf0987d451968e817d3))

- **contributing**: Refresh development docs
  ([`d387d91`](https://github.com/python-gitlab/python-gitlab/commit/d387d91401fdf933b1832ea2593614ea6b7d8acf))

- **deps**: Update actions/stale action to v8
  ([`7ac4b86`](https://github.com/python-gitlab/python-gitlab/commit/7ac4b86fe3d24c3347a1c44bd3db561d62a7bd3f))

- **deps**: Update all non-major dependencies
  ([`8b692e8`](https://github.com/python-gitlab/python-gitlab/commit/8b692e825d95cd338e305196d9ca4e6d87173a84))

- **deps**: Update all non-major dependencies
  ([`2f06999`](https://github.com/python-gitlab/python-gitlab/commit/2f069999c5dfd637f17d1ded300ea7628c0566c3))

- **deps**: Update all non-major dependencies
  ([#2493](https://github.com/python-gitlab/python-gitlab/pull/2493),
  [`07d03dc`](https://github.com/python-gitlab/python-gitlab/commit/07d03dc959128e05d21e8dfd79aa8e916ab5b150))

* chore(deps): update all non-major dependencies * chore(fixtures): downgrade GitLab for now *
  chore(deps): ungroup typing deps, group gitlab instead * chore(deps): downgrade argcomplete for
  now

---------

Co-authored-by: renovate[bot] <29139614+renovate[bot]@users.noreply.github.com>

Co-authored-by: Nejc Habjan <nejc.habjan@siemens.com>

- **deps**: Update black (23.1.0) and commitizen (2.40.0)
  ([#2479](https://github.com/python-gitlab/python-gitlab/pull/2479),
  [`44786ef`](https://github.com/python-gitlab/python-gitlab/commit/44786efad1dbb66c8242e61cf0830d58dfaff196))

Update the dependency versions: black: 23.1.0

commitizen: 2.40.0

They needed to be updated together as just updating `black` caused a dependency conflict.

Updated files by running `black` and committing the changes.

- **deps**: Update dependency coverage to v7
  ([#2501](https://github.com/python-gitlab/python-gitlab/pull/2501),
  [`aee73d0`](https://github.com/python-gitlab/python-gitlab/commit/aee73d05c8c9bd94fb7f01dfefd1bb6ad19c4eb2))

Co-authored-by: renovate[bot] <29139614+renovate[bot]@users.noreply.github.com>

- **deps**: Update dependency flake8 to v6
  ([#2502](https://github.com/python-gitlab/python-gitlab/pull/2502),
  [`3d4596e`](https://github.com/python-gitlab/python-gitlab/commit/3d4596e8cdebbc0ea214d63556b09eac40d42a9c))

Co-authored-by: renovate[bot] <29139614+renovate[bot]@users.noreply.github.com>

- **deps**: Update dependency furo to v2023
  ([`7a1545d`](https://github.com/python-gitlab/python-gitlab/commit/7a1545d52ed0ac8e2e42a2f260e8827181e94d88))

- **deps**: Update dependency pre-commit to v3
  ([#2508](https://github.com/python-gitlab/python-gitlab/pull/2508),
  [`7d779c8`](https://github.com/python-gitlab/python-gitlab/commit/7d779c85ffe09623c5d885b5a429b0242ad82f93))

Co-authored-by: renovate[bot] <29139614+renovate[bot]@users.noreply.github.com>

- **deps**: Update mypy (1.0.0) and responses (0.22.0)
  ([`9c24657`](https://github.com/python-gitlab/python-gitlab/commit/9c2465759386b60a478bd8f43e967182ed97d39d))

Update the `requirements-*` files.

In order to update mypy==1.0.0 we need to also update responses==0.22.0

Fix one issue found by `mypy`

Leaving updates for `precommit` to be done in a separate commit by someone.

- **deps**: Update pre-commit hook psf/black to v23
  ([`217a787`](https://github.com/python-gitlab/python-gitlab/commit/217a78780c3ae6e41fb9d76d4d841c5d576de45f))

- **github**: Add default pull request template
  ([`bf46c67`](https://github.com/python-gitlab/python-gitlab/commit/bf46c67db150f0657b791d94e6699321c9985f57))

- **pre-commit**: Bumping versions
  ([`e973729`](https://github.com/python-gitlab/python-gitlab/commit/e973729e007f664aa4fde873654ef68c21be03c8))

- **renovate**: Bring back custom requirements pattern
  ([`ae0b21c`](https://github.com/python-gitlab/python-gitlab/commit/ae0b21c1c2b74bf012e099ae1ff35ce3f40c6480))

- **renovate**: Do not ignore tests dir
  ([`5b8744e`](https://github.com/python-gitlab/python-gitlab/commit/5b8744e9c2241e0fdcdef03184afcb48effea90f))

- **renovate**: Swith to gitlab-ee
  ([`8da48ee`](https://github.com/python-gitlab/python-gitlab/commit/8da48ee0f32c293b4788ebd0ddb24018401ef7ad))

- **setup**: Depend on typing-extensions for 3.7 until EOL
  ([`3abc557`](https://github.com/python-gitlab/python-gitlab/commit/3abc55727d4d52307b9ce646fee172f94f7baf8d))

### Documentation

- Fix update badge behaviour
  ([`3d7ca1c`](https://github.com/python-gitlab/python-gitlab/commit/3d7ca1caac5803c2e6d60a3e5eba677957b3cfc6))

docs: fix update badge behaviour

Earlier: badge.image_link = new_link

Now: badge.image_url = new_image_url badge.link_url = new_link_url

- **advanced**: Clarify netrc, proxy behavior with requests
  ([`1da7c53`](https://github.com/python-gitlab/python-gitlab/commit/1da7c53fd3476a1ce94025bb15265f674af40e1a))

- **advanced**: Fix typo in Gitlab examples
  ([`1992790`](https://github.com/python-gitlab/python-gitlab/commit/19927906809c329788822f91d0abd8761a85c5c3))

- **objects**: Fix typo in pipeline schedules
  ([`3057f45`](https://github.com/python-gitlab/python-gitlab/commit/3057f459765d1482986f2086beb9227acc7fd15f))

### Features

- Add resource_weight_event for ProjectIssue
  ([`6e5ef55`](https://github.com/python-gitlab/python-gitlab/commit/6e5ef55747ddeabe6d212aec50d66442054c2352))

- **backends**: Use PEP544 protocols for structural subtyping
  ([#2442](https://github.com/python-gitlab/python-gitlab/pull/2442),
  [`4afeaff`](https://github.com/python-gitlab/python-gitlab/commit/4afeaff0361a966254a7fbf0120e93583d460361))

The purpose of this change is to track API changes described in
  https://github.com/python-gitlab/python-gitlab/blob/main/docs/api-levels.rst, for example, for
  package versioning and breaking change announcements in case of protocol changes.

This is MVP implementation to be used by #2435.

- **cli**: Add setting of `allow_force_push` for protected branch
  ([`929e07d`](https://github.com/python-gitlab/python-gitlab/commit/929e07d94d9a000e6470f530bfde20bb9c0f2637))

For the CLI: add `allow_force_push` as an optional argument for creating a protected branch.

API reference: https://docs.gitlab.com/ee/api/protected_branches.html#protect-repository-branches

Closes: #2466

- **client**: Add http_patch method
  ([#2471](https://github.com/python-gitlab/python-gitlab/pull/2471),
  [`f711d9e`](https://github.com/python-gitlab/python-gitlab/commit/f711d9e2bf78f58cee6a7c5893d4acfd2f980397))

In order to support some new API calls we need to support the HTTP `PATCH` method.

Closes: #2469

- **objects**: Support fetching PATs via id or `self` endpoint
  ([`19b38bd`](https://github.com/python-gitlab/python-gitlab/commit/19b38bd481c334985848be204eafc3f1ea9fe8a6))

- **projects**: Allow importing additional items from GitHub
  ([`ce84f2e`](https://github.com/python-gitlab/python-gitlab/commit/ce84f2e64a640e0d025a7ba3a436f347ad25e88e))

### Refactoring

- **client**: Let mypy know http_password is set
  ([`2dd177b`](https://github.com/python-gitlab/python-gitlab/commit/2dd177bf83fdf62f0e9bdcb3bc41d5e4f5631504))

### Testing

- **functional**: Clarify MR fixture factory name
  ([`d8fd1a8`](https://github.com/python-gitlab/python-gitlab/commit/d8fd1a83b588f4e5e61ca46a28f4935220c5b8c4))

- **meta**: Move meta suite into unit tests
  ([`847004b`](https://github.com/python-gitlab/python-gitlab/commit/847004be021b4a514e41bf28afb9d87e8643ddba))

They're always run with it anyway, so it makes no difference.

- **unit**: Consistently use inline fixtures
  ([`1bc56d1`](https://github.com/python-gitlab/python-gitlab/commit/1bc56d164a7692cf3aaeedfa1ed2fb869796df03))

- **unit**: Increase V4 CLI coverage
  ([`5748d37`](https://github.com/python-gitlab/python-gitlab/commit/5748d37365fdac105341f94eaccde8784d6f57e3))

- **unit**: Remove redundant package
  ([`4a9e3ee`](https://github.com/python-gitlab/python-gitlab/commit/4a9e3ee70f784f99f373f2fddde0155649ebe859))

- **unit**: Split the last remaining unittest-based classes into modules"
  ([`14e0f65`](https://github.com/python-gitlab/python-gitlab/commit/14e0f65a3ff05563df4977d792272f8444bf4312))


## v3.13.0 (2023-01-30)

### Bug Fixes

- Change return value to "None" in case getattr returns None to prevent error
  ([`3f86d36`](https://github.com/python-gitlab/python-gitlab/commit/3f86d36218d80b293b346b37f8be5efa6455d10c))

- Typo fixed in docs
  ([`ee5f444`](https://github.com/python-gitlab/python-gitlab/commit/ee5f444b16e4d2f645499ac06f5d81f22867f050))

- Use the ProjectIterationManager within the Project object
  ([`44f05dc`](https://github.com/python-gitlab/python-gitlab/commit/44f05dc017c5496e14db82d9650c6a0110b95cf9))

The Project object was previously using the GroupIterationManager resulting in the incorrect API
  endpoint being used. Utilize the correct ProjectIterationManager instead.

Resolves #2403

- **api**: Make description optional for releases
  ([`5579750`](https://github.com/python-gitlab/python-gitlab/commit/5579750335245011a3acb9456cb488f0fa1cda61))

- **client**: Regression - do not automatically get_next if page=# and
  ([`585e3a8`](https://github.com/python-gitlab/python-gitlab/commit/585e3a86c4cafa9ee73ed38676a78f3c34dbe6b2))

- **deps**: Bump requests-toolbelt to fix deprecation warning
  ([`faf842e`](https://github.com/python-gitlab/python-gitlab/commit/faf842e97d4858ff5ebd8ae6996e0cb3ca29881c))

### Chores

- Add a UserWarning if both `iterator=True` and `page=X` are used
  ([#2462](https://github.com/python-gitlab/python-gitlab/pull/2462),
  [`8e85791`](https://github.com/python-gitlab/python-gitlab/commit/8e85791c315822cd26d56c0c0f329cffae879644))

If a caller calls a `list()` method with both `iterator=True` (or `as_list=False`) and `page=X` then
  emit a `UserWarning` as the options are mutually exclusive.

- Add docs for schedule pipelines
  ([`9a9a6a9`](https://github.com/python-gitlab/python-gitlab/commit/9a9a6a98007df2992286a721507b02c48800bfed))

- Add test, docs, and helper for 409 retries
  ([`3e1c625`](https://github.com/python-gitlab/python-gitlab/commit/3e1c625133074ccd2fb88c429ea151bfda96aebb))

- Make backends private
  ([`1e629af`](https://github.com/python-gitlab/python-gitlab/commit/1e629af73e312fea39522334869c3a9b7e6085b9))

- Remove tox `envdir` values
  ([`3c7c7fc`](https://github.com/python-gitlab/python-gitlab/commit/3c7c7fc9d2375d3219fb078e18277d7476bae5e0))

tox > 4 no longer will re-use the tox directory :( What this means is that with the previous config
  if you ran: $ tox -e mypy; tox -e isort; tox -e mypy It would recreate the tox environment each
  time :(

By removing the `envdir` values it will have the tox environments in separate directories and not
  recreate them.

The have an FAQ entry about this: https://tox.wiki/en/latest/upgrading.html#re-use-of-environments

- Update attributes for create and update projects
  ([`aa44f2a`](https://github.com/python-gitlab/python-gitlab/commit/aa44f2aed8150f8c891837e06296c7bbef17c292))

- Use SPDX license expression in project metadata
  ([`acb3a4a`](https://github.com/python-gitlab/python-gitlab/commit/acb3a4ad1fa23c21b1d7f50e95913136beb61402))

- **ci**: Complete all unit tests even if one has failed
  ([#2438](https://github.com/python-gitlab/python-gitlab/pull/2438),
  [`069c6c3`](https://github.com/python-gitlab/python-gitlab/commit/069c6c30ff989f89356898b72835b4f4a792305c))

- **deps**: Update actions/download-artifact action to v3
  ([`64ca597`](https://github.com/python-gitlab/python-gitlab/commit/64ca5972468ab3b7e3a01e88ab9bb8e8bb9a3de1))

- **deps**: Update actions/stale action to v7
  ([`76eb024`](https://github.com/python-gitlab/python-gitlab/commit/76eb02439c0ae0f7837e3408948840c800fd93a7))

- **deps**: Update all non-major dependencies
  ([`ea7010b`](https://github.com/python-gitlab/python-gitlab/commit/ea7010b17cc2c29c2a5adeaf81f2d0064523aa39))

- **deps**: Update all non-major dependencies
  ([`122988c`](https://github.com/python-gitlab/python-gitlab/commit/122988ceb329d7162567cb4a325f005ea2013ef2))

- **deps**: Update all non-major dependencies
  ([`49c0233`](https://github.com/python-gitlab/python-gitlab/commit/49c023387970abea7688477c8ef3ff3a1b31b0bc))

- **deps**: Update all non-major dependencies
  ([`10c4f31`](https://github.com/python-gitlab/python-gitlab/commit/10c4f31ad1480647a6727380db68f67a4c645af9))

- **deps**: Update all non-major dependencies
  ([`bbd01e8`](https://github.com/python-gitlab/python-gitlab/commit/bbd01e80326ea9829b2f0278fedcb4464be64389))

- **deps**: Update all non-major dependencies
  ([`6682808`](https://github.com/python-gitlab/python-gitlab/commit/6682808034657b73c4b72612aeb009527c25bfa2))

- **deps**: Update all non-major dependencies
  ([`1816107`](https://github.com/python-gitlab/python-gitlab/commit/1816107b8d87614e7947837778978d8de8da450f))

- **deps**: Update all non-major dependencies
  ([`21e767d`](https://github.com/python-gitlab/python-gitlab/commit/21e767d8719372daadcea446f835f970210a6b6b))

- **deps**: Update dessant/lock-threads action to v4
  ([`337b25c`](https://github.com/python-gitlab/python-gitlab/commit/337b25c6fc1f40110ef7a620df63ff56a45579f1))

- **deps**: Update pre-commit hook maxbrunet/pre-commit-renovate to v34.48.4
  ([`985b971`](https://github.com/python-gitlab/python-gitlab/commit/985b971cf6d69692379805622a1bb1ff29ae308d))

- **deps**: Update pre-commit hook pycqa/flake8 to v6
  ([`82c61e1`](https://github.com/python-gitlab/python-gitlab/commit/82c61e1d2c3a8102c320558f46e423b09c6957aa))

- **tox**: Ensure test envs have all dependencies
  ([`63cf4e4`](https://github.com/python-gitlab/python-gitlab/commit/63cf4e4fa81d6c5bf6cf74284321bc3ce19bab62))

### Documentation

- **faq**: Describe and group common errors
  ([`4c9a072`](https://github.com/python-gitlab/python-gitlab/commit/4c9a072b053f12f8098e4ea6fc47e3f6ab4f8b07))

### Features

- Add keep_base_url when getting configuration from file
  ([`50a0301`](https://github.com/python-gitlab/python-gitlab/commit/50a03017f2ba8ec3252911dd1cf0ed7df42cfe50))

- Add resource iteration events (see https://docs.gitlab.com/ee/api/resource_iteration_events.html)
  ([`ef5feb4`](https://github.com/python-gitlab/python-gitlab/commit/ef5feb4d07951230452a2974da729a958bdb9d6a))

- Allow filtering pipelines by source
  ([`b6c0872`](https://github.com/python-gitlab/python-gitlab/commit/b6c08725042380d20ef5f09979bc29f2f6c1ab6f))

See: https://docs.gitlab.com/ee/api/pipelines.html#list-project-pipelines Added in GitLab 14.3

- Allow passing kwargs to Gitlab class when instantiating with `from_config`
  ([#2392](https://github.com/python-gitlab/python-gitlab/pull/2392),
  [`e88d34e`](https://github.com/python-gitlab/python-gitlab/commit/e88d34e38dd930b00d7bb48f0e1c39420e09fa0f))

- **api**: Add support for bulk imports API
  ([`043de2d`](https://github.com/python-gitlab/python-gitlab/commit/043de2d265e0e5114d1cd901f82869c003413d9b))

- **api**: Add support for resource groups
  ([`5f8b8f5`](https://github.com/python-gitlab/python-gitlab/commit/5f8b8f5be901e944dfab2257f9e0cc4b2b1d2cd5))

- **api**: Support listing pipelines triggered by pipeline schedules
  ([`865fa41`](https://github.com/python-gitlab/python-gitlab/commit/865fa417a20163b526596549b9afbce679fc2817))

- **client**: Automatically retry on HTTP 409 Resource lock
  ([`dced76a`](https://github.com/python-gitlab/python-gitlab/commit/dced76a9900c626c9f0b90b85a5e371101a24fb4))

Fixes: #2325

- **client**: Bootstrap the http backends concept
  ([#2391](https://github.com/python-gitlab/python-gitlab/pull/2391),
  [`91a665f`](https://github.com/python-gitlab/python-gitlab/commit/91a665f331c3ffc260db3470ad71fde0d3b56aa2))

- **group**: Add support for group restore API
  ([`9322db6`](https://github.com/python-gitlab/python-gitlab/commit/9322db663ecdaecf399e3192810d973c6a9a4020))

### Refactoring

- Add reason property to RequestsResponse
  ([#2439](https://github.com/python-gitlab/python-gitlab/pull/2439),
  [`b59b7bd`](https://github.com/python-gitlab/python-gitlab/commit/b59b7bdb221ac924b5be4227ef7201d79b40c98f))

- Migrate MultipartEncoder to RequestsBackend
  ([#2421](https://github.com/python-gitlab/python-gitlab/pull/2421),
  [`43b369f`](https://github.com/python-gitlab/python-gitlab/commit/43b369f28cb9009e02bc23e772383d9ea1ded46b))

- Move Response object to backends
  ([#2420](https://github.com/python-gitlab/python-gitlab/pull/2420),
  [`7d9ce0d`](https://github.com/python-gitlab/python-gitlab/commit/7d9ce0dfb9f5a71aaa7f9c78d815d7c7cbd21c1c))

- Move the request call to the backend
  ([#2413](https://github.com/python-gitlab/python-gitlab/pull/2413),
  [`283e7cc`](https://github.com/python-gitlab/python-gitlab/commit/283e7cc04ce61aa456be790a503ed64089a2c2b6))

- Moving RETRYABLE_TRANSIENT_ERROR_CODES to const
  ([`887852d`](https://github.com/python-gitlab/python-gitlab/commit/887852d7ef02bed6dff5204ace73d8e43a66e32f))

- Remove unneeded requests.utils import
  ([#2426](https://github.com/python-gitlab/python-gitlab/pull/2426),
  [`6fca651`](https://github.com/python-gitlab/python-gitlab/commit/6fca6512a32e9e289f988900e1157dfe788f54be))

### Testing

- **functional**: Do not require config file
  ([`43c2dda`](https://github.com/python-gitlab/python-gitlab/commit/43c2dda7aa8b167a451b966213e83d88d1baa1df))

- **unit**: Expand tests for pipeline schedules
  ([`c7cf0d1`](https://github.com/python-gitlab/python-gitlab/commit/c7cf0d1f172c214a11b30622fbccef57d9c86e93))


## v3.12.0 (2022-11-28)

### Bug Fixes

- Use POST method and return dict in `cancel_merge_when_pipeline_succeeds()`
  ([#2350](https://github.com/python-gitlab/python-gitlab/pull/2350),
  [`bd82d74`](https://github.com/python-gitlab/python-gitlab/commit/bd82d745c8ea9ff6ff078a4c961a2d6e64a2f63c))

* Call was incorrectly using a `PUT` method when should have used a `POST` method. * Changed return
  type to a `dict` as GitLab only returns {'status': 'success'} on success. Since the function
  didn't work previously, this should not impact anyone. * Updated the test fixture `merge_request`
  to add ability to create a pipeline. * Added functional test for
  `mr.cancel_merge_when_pipeline_succeeds()`

Fixes: #2349

- **cli**: Enable debug before doing auth
  ([`65abb85`](https://github.com/python-gitlab/python-gitlab/commit/65abb85be7fc8ef57b295296111dac0a97ed1c49))

Authentication issues are currently hard to debug since `--debug` only has effect after `gl.auth()`
  has been called.

For example, a 401 error is printed without any details about the actual HTTP request being sent:

$ gitlab --debug --server-url https://gitlab.com current-user get 401: 401 Unauthorized

By moving the call to `gl.enable_debug()` the usual debug logs get printed before the final error
  message.

Signed-off-by: Emanuele Aina <emanuele.aina@collabora.com>

- **cli**: Expose missing mr_default_target_self project attribute
  ([`12aea32`](https://github.com/python-gitlab/python-gitlab/commit/12aea32d1c0f7e6eac0d19da580bf6efde79d3e2))

Example::

gitlab project update --id 616 --mr-default-target-self 1

References:

* https://gitlab.com/gitlab-org/gitlab/-/merge_requests/58093 *
  https://gitlab.com/gitlab-org/gitlab/-/blob/v13.11.0-ee/doc/user/project/merge_requests/creating_merge_requests.md#new-merge-request-from-a-fork
  * https://gitlab.com/gitlab-org/gitlab/-/blob/v14.7.0-ee/doc/api/projects.md#get-single-project

### Chores

- Correct website for pylint
  ([`fcd72fe`](https://github.com/python-gitlab/python-gitlab/commit/fcd72fe243daa0623abfde267c7ab1c6866bcd52))

Use https://github.com/PyCQA/pylint as the website for pylint.

- Validate httpx package is not installed by default
  ([`0ecf3bb`](https://github.com/python-gitlab/python-gitlab/commit/0ecf3bbe28c92fd26a7d132bf7f5ae9481cbad30))

- **deps**: Update all non-major dependencies
  ([`d8a657b`](https://github.com/python-gitlab/python-gitlab/commit/d8a657b2b391e9ba3c20d46af6ad342a9b9a2f93))

- **deps**: Update all non-major dependencies
  ([`b2c6d77`](https://github.com/python-gitlab/python-gitlab/commit/b2c6d774b3f8fa72c5607bfa4fa0918283bbdb82))

- **deps**: Update pre-commit hook maxbrunet/pre-commit-renovate to v34
  ([`623e768`](https://github.com/python-gitlab/python-gitlab/commit/623e76811a16f0a8ae58dbbcebfefcfbef97c8d1))

- **deps**: Update pre-commit hook maxbrunet/pre-commit-renovate to v34.20.0
  ([`e6f1bd6`](https://github.com/python-gitlab/python-gitlab/commit/e6f1bd6333a884433f808b2a84670079f9a70f0a))

- **deps**: Update pre-commit hook maxbrunet/pre-commit-renovate to v34.24.0
  ([`a0553c2`](https://github.com/python-gitlab/python-gitlab/commit/a0553c29899f091209afe6366e8fb75fb9edef40))

### Documentation

- Use the term "log file" for getting a job log file
  ([`9d2b1ad`](https://github.com/python-gitlab/python-gitlab/commit/9d2b1ad10aaa78a5c28ece334293641c606291b5))

The GitLab docs refer to it as a log file: https://docs.gitlab.com/ee/api/jobs.html#get-a-log-file

"trace" is the endpoint name but not a common term people will think of for a "log file"

- **api**: Pushrules remove saying `None` is returned when not found
  ([`c3600b4`](https://github.com/python-gitlab/python-gitlab/commit/c3600b49e4d41b1c4f2748dd6f2a331c331d8706))

In `groups.pushrules.get()`, GitLab does not return `None` when no rules are found. GitLab returns a
  404.

Update docs to not say it will return `None`

Also update docs in `project.pushrules.get()` to be consistent. Not 100% sure if it returns `None`
  or returns a 404, but we don't need to document that.

Closes: #2368

- **groups**: Describe GitLab.com group creation limitation
  ([`9bd433a`](https://github.com/python-gitlab/python-gitlab/commit/9bd433a3eb508b53fbca59f3f445da193522646a))

### Features

- Add support for SAML group links
  ([#2367](https://github.com/python-gitlab/python-gitlab/pull/2367),
  [`1020ce9`](https://github.com/python-gitlab/python-gitlab/commit/1020ce965ff0cd3bfc283d4f0ad40e41e4d1bcee))

- Implement secure files API
  ([`d0a0348`](https://github.com/python-gitlab/python-gitlab/commit/d0a034878fabfd8409134aa8b7ffeeb40219683c))

- **api**: Add application statistics
  ([`6fcf3b6`](https://github.com/python-gitlab/python-gitlab/commit/6fcf3b68be095e614b969f5922ad8a67978cd4db))

- **api**: Add support for getting a project's pull mirror details
  ([`060cfe1`](https://github.com/python-gitlab/python-gitlab/commit/060cfe1465a99657c5f832796ab3aa03aad934c7))

Add the ability to get a project's pull mirror details. This was added in GitLab 15.5 and is a
  PREMIUM feature.

https://docs.gitlab.com/ee/api/projects.html#get-a-projects-pull-mirror-details

- **api**: Add support for remote project import
  ([#2348](https://github.com/python-gitlab/python-gitlab/pull/2348),
  [`e5dc72d`](https://github.com/python-gitlab/python-gitlab/commit/e5dc72de9b3cdf0a7944ee0961fbdc6784c7f315))

- **api**: Add support for remote project import from AWS S3
  ([#2357](https://github.com/python-gitlab/python-gitlab/pull/2357),
  [`892281e`](https://github.com/python-gitlab/python-gitlab/commit/892281e35e3d81c9e43ff6a974f920daa83ea8b2))

- **ci**: Re-run Tests on PR Comment workflow
  ([`034cde3`](https://github.com/python-gitlab/python-gitlab/commit/034cde31c7017923923be29c3f34783937febc0f))

- **groups**: Add LDAP link manager and deprecate old API endpoints
  ([`3a61f60`](https://github.com/python-gitlab/python-gitlab/commit/3a61f601adaec7751cdcfbbcb88aa544326b1730))

- **groups**: Add support for listing ldap_group_links
  ([#2371](https://github.com/python-gitlab/python-gitlab/pull/2371),
  [`ad7c8fa`](https://github.com/python-gitlab/python-gitlab/commit/ad7c8fafd56866002aa6723ceeba4c4bc071ca0d))

### Refactoring

- Explicitly use ProjectSecureFile
  ([`0c98b2d`](https://github.com/python-gitlab/python-gitlab/commit/0c98b2d8f4b8c1ac6a4b496282f307687b652759))

### Testing

- **api**: Fix flaky test `test_cancel_merge_when_pipeline_succeeds`
  ([`6525c17`](https://github.com/python-gitlab/python-gitlab/commit/6525c17b8865ead650a6e09f9bf625ca9881911b))

This is an attempt to fix the flaky test `test_cancel_merge_when_pipeline_succeeds`. Were seeing a:
  405 Method Not Allowed error when setting the MR to merge_when_pipeline_succeeds.

Closes: #2383


## v3.11.0 (2022-10-28)

### Bug Fixes

- Intermittent failure in test_merge_request_reset_approvals
  ([`3dde36e`](https://github.com/python-gitlab/python-gitlab/commit/3dde36eab40406948adca633f7197beb32b29552))

Have been seeing intermittent failures in the test:
  tests/functional/api/test_merge_requests.py::test_merge_request_reset_approvals

Also saw a failure in: tests/functional/cli/test_cli_v4.py::test_accept_request_merge[subprocess]

Add a call to `wait_for_sidekiq()` to hopefully resolve the issues.

- Remove `project.approvals.set_approvals()` method
  ([`91f08f0`](https://github.com/python-gitlab/python-gitlab/commit/91f08f01356ca5e38d967700a5da053f05b6fab0))

The `project.approvals.set_approvals()` method used the `/projects/:id/approvers` end point. That
  end point was removed from GitLab in the 13.11 release, on 2-Apr-2021 in commit
  27dc2f2fe81249bbdc25f7bd8fe799752aac05e6 via merge commit
  e482597a8cf1bae8e27abd6774b684fb90491835. It was deprecated on 19-Aug-2019.

See merge request: https://gitlab.com/gitlab-org/gitlab/-/merge_requests/57473

- Use epic id instead of iid for epic notes
  ([`97cae38`](https://github.com/python-gitlab/python-gitlab/commit/97cae38a315910972279f2d334e91fa54d9ede0c))

- **cli**: Handle list response for json/yaml output
  ([`9b88132`](https://github.com/python-gitlab/python-gitlab/commit/9b88132078ed37417c2a45369b4976c9c67f7882))

Handle the case with the CLI where a list response is returned from GitLab and json/yaml output is
  requested.

Add a functional CLI test to validate it works.

Closes: #2287

### Chores

- Add `not-callable` to pylint ignore list
  ([`f0c02a5`](https://github.com/python-gitlab/python-gitlab/commit/f0c02a553da05ea3fdca99798998f40cfd820983))

The `not-callable` error started showing up. Ignore this error as it is invalid. Also `mypy` tests
  for these issues.

Closes: #2334

- Add basic type checks to functional/api tests
  ([`5b642a5`](https://github.com/python-gitlab/python-gitlab/commit/5b642a5d4c934f0680fa99079484176d36641861))

- Add basic type checks to meta tests
  ([`545d6d6`](https://github.com/python-gitlab/python-gitlab/commit/545d6d60673c7686ec873a343b6afd77ec9062ec))

- Add basic typing to functional tests
  ([`ee143c9`](https://github.com/python-gitlab/python-gitlab/commit/ee143c9d6df0f1498483236cc228e12132bef132))

- Add basic typing to smoke tests
  ([`64e8c31`](https://github.com/python-gitlab/python-gitlab/commit/64e8c31e1d35082bc2e52582205157ae1a6c4605))

- Add basic typing to test root
  ([`0b2f6bc`](https://github.com/python-gitlab/python-gitlab/commit/0b2f6bcf454685786a89138b36b10fba649663dd))

- Add responses to pre-commit deps
  ([`4b8ddc7`](https://github.com/python-gitlab/python-gitlab/commit/4b8ddc74c8f7863631005e8eb9861f1e2f0a4cbc))

- Fix flaky test
  ([`fdd4114`](https://github.com/python-gitlab/python-gitlab/commit/fdd4114097ca69bbb4fd9c3117b83063b242f8f2))

- Narrow type hints for license API
  ([`50731c1`](https://github.com/python-gitlab/python-gitlab/commit/50731c173083460f249b1718cbe2288fc3c46c1a))

- Renovate and precommit cleanup
  ([`153d373`](https://github.com/python-gitlab/python-gitlab/commit/153d3739021d2375438fe35ce819c77142914567))

- Revert compose upgrade
  ([`dd04e8e`](https://github.com/python-gitlab/python-gitlab/commit/dd04e8ef7eee2793fba38a1eec019b00b3bb616e))

This reverts commit f825d70e25feae8cd9da84e768ec6075edbc2200.

- Simplify `wait_for_sidekiq` usage
  ([`196538b`](https://github.com/python-gitlab/python-gitlab/commit/196538ba3e233ba2acf6f816f436888ba4b1f52a))

Simplify usage of `wait_for_sidekiq` by putting the assert if it timed out inside the function
  rather than after calling it.

- Topic functional tests
  ([`d542eba`](https://github.com/python-gitlab/python-gitlab/commit/d542eba2de95f2cebcc6fc7d343b6daec95e4219))

- Update the issue templates
  ([`c15bd33`](https://github.com/python-gitlab/python-gitlab/commit/c15bd33f45fbd9d064f1e173c6b3ca1b216def2f))

* Have an option to go to the discussions * Have an option to go to the Gitter chat * Move the
  bug/issue template into the .github/ISSUE_TEMPLATE/ directory

- Use kwargs for http_request docs
  ([`124abab`](https://github.com/python-gitlab/python-gitlab/commit/124abab483ab6be71dbed91b8d518ae27355b9ae))

- **deps**: Group non-major upgrades to reduce noise
  ([`37d14bd`](https://github.com/python-gitlab/python-gitlab/commit/37d14bd9fd399a498d72a03b536701678af71702))

- **deps**: Pin and clean up test dependencies
  ([`60b9197`](https://github.com/python-gitlab/python-gitlab/commit/60b9197dfe327eb2310523bae04c746d34458fa3))

- **deps**: Pin dependencies
  ([`953f38d`](https://github.com/python-gitlab/python-gitlab/commit/953f38dcc7ccb2a9ad0ea8f1b9a9e06bd16b9133))

- **deps**: Pin GitHub Actions
  ([`8dbaa5c`](https://github.com/python-gitlab/python-gitlab/commit/8dbaa5cddef6d7527ded686553121173e33d2973))

- **deps**: Update all non-major dependencies
  ([`dde3642`](https://github.com/python-gitlab/python-gitlab/commit/dde3642bcd41ea17c4f301188cb571db31fe4da8))

- **deps**: Update all non-major dependencies
  ([`2966234`](https://github.com/python-gitlab/python-gitlab/commit/296623410ae0b21454ac11e48e5991329c359c4d))

- **deps**: Update black to v22.10.0
  ([`531ee05`](https://github.com/python-gitlab/python-gitlab/commit/531ee05bdafbb6fee8f6c9894af15fc89c67d610))

- **deps**: Update dependency commitizen to v2.35.0
  ([`4ce9559`](https://github.com/python-gitlab/python-gitlab/commit/4ce95594695d2e19a215719d535bc713cf381729))

- **deps**: Update dependency mypy to v0.981
  ([`da48849`](https://github.com/python-gitlab/python-gitlab/commit/da48849a303beb0d0292bccd43d54aacfb0c316b))

- **deps**: Update dependency pylint to v2.15.3
  ([`6627a60`](https://github.com/python-gitlab/python-gitlab/commit/6627a60a12471f794cb308e76e449b463b9ce37a))

- **deps**: Update dependency types-requests to v2.28.11.2
  ([`d47c0f0`](https://github.com/python-gitlab/python-gitlab/commit/d47c0f06317d6a63af71bb261d6bb4e83325f261))

- **deps**: Update pre-commit hook maxbrunet/pre-commit-renovate to v33
  ([`932bbde`](https://github.com/python-gitlab/python-gitlab/commit/932bbde7ff10dd0f73bc81b7e91179b93a64602b))

- **deps**: Update typing dependencies
  ([`81285fa`](https://github.com/python-gitlab/python-gitlab/commit/81285fafd2b3c643d130a84550a666d4cc480b51))

### Documentation

- Add minimal docs about the `enable_debug()` method
  ([`b4e9ab7`](https://github.com/python-gitlab/python-gitlab/commit/b4e9ab7ee395e575f17450c2dc0d519f7192e58e))

Add some minimal documentation about the `enable_debug()` method.

- **advanced**: Add hint on type narrowing
  ([`a404152`](https://github.com/python-gitlab/python-gitlab/commit/a40415290923d69d087dd292af902efbdfb5c258))

- **api**: Describe the list() and all() runners' functions
  ([`b6cc3f2`](https://github.com/python-gitlab/python-gitlab/commit/b6cc3f255532521eb259b42780354e03ce51458e))

- **api**: Describe use of lower-level methods
  ([`b7a6874`](https://github.com/python-gitlab/python-gitlab/commit/b7a687490d2690e6bd4706391199135e658e1dc6))

- **api**: Update `merge_requests.rst`: `mr_id` to `mr_iid`
  ([`b32234d`](https://github.com/python-gitlab/python-gitlab/commit/b32234d1f8c4492b6b2474f91be9479ad23115bb))

Typo: Author probably meant `mr_iid` (i.e. project-specific MR ID)

and **not** `mr_id` (i.e. server-wide MR ID)

Closes: https://github.com/python-gitlab/python-gitlab/issues/2295

Signed-off-by: Stavros Ntentos <133706+stdedos@users.noreply.github.com>

- **commits**: Fix commit create example for binary content
  ([`bcc1eb4`](https://github.com/python-gitlab/python-gitlab/commit/bcc1eb4571f76b3ca0954adb5525b26f05958e3f))

- **readme**: Add a basic feature list
  ([`b4d53f1`](https://github.com/python-gitlab/python-gitlab/commit/b4d53f1abb264cd9df8e4ac6560ab0895080d867))

### Features

- **api**: Add support for topics merge API
  ([`9a6d197`](https://github.com/python-gitlab/python-gitlab/commit/9a6d197f9d2a88bdba8dab1f9abaa4e081a14792))

- **build**: Officially support Python 3.11
  ([`74f66c7`](https://github.com/python-gitlab/python-gitlab/commit/74f66c71f3974cf68f5038f4fc3995e53d44aebe))

### Refactoring

- Migrate legacy EE tests to pytest
  ([`88c2505`](https://github.com/python-gitlab/python-gitlab/commit/88c2505b05dbcfa41b9e0458d4f2ec7dcc6f8169))

- Pre-commit trigger from tox
  ([`6e59c12`](https://github.com/python-gitlab/python-gitlab/commit/6e59c12fe761e8deea491d1507beaf00ca381cdc))

- Pytest-docker fixtures
  ([`3e4781a`](https://github.com/python-gitlab/python-gitlab/commit/3e4781a66577a6ded58f721739f8e9422886f9cd))

- **deps**: Drop compose v1 dependency in favor of v2
  ([`f825d70`](https://github.com/python-gitlab/python-gitlab/commit/f825d70e25feae8cd9da84e768ec6075edbc2200))

### Testing

- Enable skipping tests per GitLab plan
  ([`01d5f68`](https://github.com/python-gitlab/python-gitlab/commit/01d5f68295b62c0a8bd431a9cd31bf9e4e91e7d9))

- Fix `test_project_push_rules` test
  ([`8779cf6`](https://github.com/python-gitlab/python-gitlab/commit/8779cf672af1abd1a1f67afef20a61ae5876a724))

Make the `test_project_push_rules` test work.

- Use false instead of /usr/bin/false
  ([`51964b3`](https://github.com/python-gitlab/python-gitlab/commit/51964b3142d4d19f44705fde8e7e721233c53dd2))

On Debian systems false is located at /bin/false (coreutils package). This fixes unit test failure
  on Debian system:

FileNotFoundError: [Errno 2] No such file or directory: '/usr/bin/false'

/usr/lib/python3.10/subprocess.py:1845: FileNotFoundError


## v3.10.0 (2022-09-28)

### Bug Fixes

- **cli**: Add missing attribute for MR changes
  ([`20c46a0`](https://github.com/python-gitlab/python-gitlab/commit/20c46a0572d962f405041983e38274aeb79a12e4))

- **cli**: Add missing attributes for creating MRs
  ([`1714d0a`](https://github.com/python-gitlab/python-gitlab/commit/1714d0a980afdb648d203751dedf95ee95ac326e))

### Chores

- Bump GitLab docker image to 15.4.0-ee.0
  ([`b87a2bc`](https://github.com/python-gitlab/python-gitlab/commit/b87a2bc7cfacd3a3c4a18342c07b89356bf38d50))

* Use `settings.delayed_group_deletion=False` as that is the recommended method to turn off the
  delayed group deletion now. * Change test to look for `default` as `pages` is not mentioned in the
  docs[1]

[1] https://docs.gitlab.com/ee/api/sidekiq_metrics.html#get-the-current-queue-metrics

- **deps**: Update black to v22.8.0
  ([`86b0e40`](https://github.com/python-gitlab/python-gitlab/commit/86b0e4015a258433528de0a5b063defa3eeb3e26))

- **deps**: Update dependency commitizen to v2.32.2
  ([`31aea28`](https://github.com/python-gitlab/python-gitlab/commit/31aea286e0767148498af300e78db7dbdf715bda))

- **deps**: Update dependency commitizen to v2.32.5
  ([`e180f14`](https://github.com/python-gitlab/python-gitlab/commit/e180f14309fa728e612ad6259c2e2c1f328a140c))

- **deps**: Update dependency pytest to v7.1.3
  ([`ec7f26c`](https://github.com/python-gitlab/python-gitlab/commit/ec7f26cd0f61a3cbadc3a1193c43b54d5b71c82b))

- **deps**: Update dependency types-requests to v2.28.10
  ([`5dde7d4`](https://github.com/python-gitlab/python-gitlab/commit/5dde7d41e48310ff70a4cef0b6bfa2df00fd8669))

- **deps**: Update pre-commit hook commitizen-tools/commitizen to v2.32.2
  ([`31ba64f`](https://github.com/python-gitlab/python-gitlab/commit/31ba64f2849ce85d434cd04ec7b837ca8f659e03))

### Features

- Add reset_approvals api
  ([`88693ff`](https://github.com/python-gitlab/python-gitlab/commit/88693ff2d6f4eecf3c79d017df52738886e2d636))

Added the newly added reset_approvals merge request api.

Signed-off-by: Lucas Zampieri <lzampier@redhat.com>

- Add support for deployment approval endpoint
  ([`9c9eeb9`](https://github.com/python-gitlab/python-gitlab/commit/9c9eeb901b1f3acd3fb0c4f24014ae2ed7c975ec))

Add support for the deployment approval endpoint[1]

[1] https://docs.gitlab.com/ee/api/deployments.html#approve-or-reject-a-blocked-deployment Closes:
  #2253


## v3.9.0 (2022-08-28)

### Chores

- Fix issue if only run test_gitlab.py func test
  ([`98f1956`](https://github.com/python-gitlab/python-gitlab/commit/98f19564c2a9feb108845d33bf3631fa219e51c6))

Make it so can run just the test_gitlab.py functional test.

For example: $ tox -e api_func_v4 -- -k test_gitlab.py

- Only check for our UserWarning
  ([`bd4dfb4`](https://github.com/python-gitlab/python-gitlab/commit/bd4dfb4729377bf64c552ef6052095aa0b5658b8))

The GitHub CI is showing a ResourceWarning, causing our test to fail.

Update test to only look for our UserWarning which should not appear.

What was seen when debugging the GitHub CI: {message: ResourceWarning( "unclosed <socket.socket
  fd=12, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=6, laddr=('127.0.0.1',
  50862), raddr=('127.0.0.1', 8080)>" ), category: 'ResourceWarning', filename:
  '/home/runner/work/python-gitlab/python-gitlab/.tox/api_func_v4/lib/python3.10/site-packages/urllib3/poolmanager.py',
  lineno: 271, line: None }

- **ci**: Make pytest annotations work
  ([`f67514e`](https://github.com/python-gitlab/python-gitlab/commit/f67514e5ffdbe0141b91c88366ff5233e0293ca2))

- **deps**: Update dependency commitizen to v2.31.0
  ([`4ff0894`](https://github.com/python-gitlab/python-gitlab/commit/4ff0894870977f07657e80bfaa06387f2af87d10))

- **deps**: Update dependency commitizen to v2.32.1
  ([`9787c5c`](https://github.com/python-gitlab/python-gitlab/commit/9787c5cf01a518164b5951ec739abb1d410ff64c))

- **deps**: Update dependency types-requests to v2.28.8
  ([`8e5b86f`](https://github.com/python-gitlab/python-gitlab/commit/8e5b86fcc72bf30749228519f1b4a6e29a8dbbe9))

- **deps**: Update dependency types-requests to v2.28.9
  ([`be932f6`](https://github.com/python-gitlab/python-gitlab/commit/be932f6dde5f47fb3d30e654b82563cd719ae8ce))

- **deps**: Update dependency types-setuptools to v64
  ([`4c97f26`](https://github.com/python-gitlab/python-gitlab/commit/4c97f26287cc947ab5ee228a5862f2a20535d2ae))

- **deps**: Update pre-commit hook commitizen-tools/commitizen to v2.31.0
  ([`71d37d9`](https://github.com/python-gitlab/python-gitlab/commit/71d37d98721c0813b096124ed2ccf5487ab463b9))

- **deps**: Update pre-commit hook commitizen-tools/commitizen to v2.32.1
  ([`cdd6efe`](https://github.com/python-gitlab/python-gitlab/commit/cdd6efef596a1409d6d8a9ea13e04c943b8c4b6a))

- **deps**: Update pre-commit hook pycqa/flake8 to v5
  ([`835d884`](https://github.com/python-gitlab/python-gitlab/commit/835d884e702f1ee48575b3154136f1ef4b2f2ff2))

### Features

- Add support for merge_base API
  ([`dd4fbd5`](https://github.com/python-gitlab/python-gitlab/commit/dd4fbd5e43adbbc502624a8de0d30925d798dec0))


## v3.8.1 (2022-08-10)

### Bug Fixes

- **client**: Do not assume user attrs returned for auth()
  ([`a07547c`](https://github.com/python-gitlab/python-gitlab/commit/a07547cba981380935966dff2c87c2c27d6b18d9))

This is mostly relevant for people mocking the API in tests.

### Chores

- Add license badge to readme
  ([`9aecc9e`](https://github.com/python-gitlab/python-gitlab/commit/9aecc9e5ae1e2e254b8a27283a0744fe6fd05fb6))

- Consolidate license and authors
  ([`366665e`](https://github.com/python-gitlab/python-gitlab/commit/366665e89045eb24d47f730e2a5dea6229839e20))

- Remove broad Exception catching from `config.py`
  ([`0abc90b`](https://github.com/python-gitlab/python-gitlab/commit/0abc90b7b456d75869869618097f8fcb0f0d9e8d))

Change "except Exception:" catching to more granular exceptions.

A step in enabling the "broad-except" check in pylint.

- **deps**: Update dependency commitizen to v2.29.5
  ([`181390a`](https://github.com/python-gitlab/python-gitlab/commit/181390a4e07e3c62b86ade11d9815d36440f5817))

- **deps**: Update dependency flake8 to v5.0.4
  ([`50a4fec`](https://github.com/python-gitlab/python-gitlab/commit/50a4feca96210e890d8ff824c2c6bf3d57f21799))

- **deps**: Update dependency sphinx to v5
  ([`3f3396e`](https://github.com/python-gitlab/python-gitlab/commit/3f3396ee383c8e6f2deeb286f04184a67edb6d1d))


## v3.8.0 (2022-08-04)

### Bug Fixes

- Optionally keep user-provided base URL for pagination
  ([#2149](https://github.com/python-gitlab/python-gitlab/pull/2149),
  [`e2ea8b8`](https://github.com/python-gitlab/python-gitlab/commit/e2ea8b89a7b0aebdb1eb3b99196d7c0034076df8))

- **client**: Ensure encoded query params are never duplicated
  ([`1398426`](https://github.com/python-gitlab/python-gitlab/commit/1398426cd748fdf492fe6184b03ac2fcb7e4fd6e))

### Chores

- Change `_repr_attr` for Project to be `path_with_namespace`
  ([`7cccefe`](https://github.com/python-gitlab/python-gitlab/commit/7cccefe6da0e90391953734d95debab2fe07ea49))

Previously `_repr_attr` was `path` but that only gives the basename of the path. So
  https://gitlab.com/gitlab-org/gitlab would only show "gitlab". Using `path_with_namespace` it will
  now show "gitlab-org/gitlab"

- Enable mypy check `disallow_any_generics`
  ([`24d17b4`](https://github.com/python-gitlab/python-gitlab/commit/24d17b43da16dd11ab37b2cee561d9392c90f32e))

- Enable mypy check `no_implicit_optional`
  ([`64b208e`](https://github.com/python-gitlab/python-gitlab/commit/64b208e0e91540af2b645da595f0ef79ee7522e1))

- Enable mypy check `warn_return_any`
  ([`76ec4b4`](https://github.com/python-gitlab/python-gitlab/commit/76ec4b481fa931ea36a195ac474812c11babef7b))

Update code so that the `warn_return_any` check passes.

- Make code PEP597 compliant
  ([`433dba0`](https://github.com/python-gitlab/python-gitlab/commit/433dba02e0d4462ae84a73d8699fe7f3e07aa410))

Use `encoding="utf-8"` in `open()` and open-like functions.

https://peps.python.org/pep-0597/

- Use `urlunparse` instead of string replace
  ([`6d1b62d`](https://github.com/python-gitlab/python-gitlab/commit/6d1b62d4b248c4c021a59cd234c3a2b19e6fad07))

Use the `urlunparse()` function to reconstruct the URL without the query parameters.

- **ci**: Bump semantic-release for fixed commit parser
  ([`1e063ae`](https://github.com/python-gitlab/python-gitlab/commit/1e063ae1c4763c176be3c5e92da4ffc61cb5d415))

- **clusters**: Deprecate clusters support
  ([`b46b379`](https://github.com/python-gitlab/python-gitlab/commit/b46b3791707ac76d501d6b7b829d1370925fd614))

Cluster support was deprecated in GitLab 14.5 [1]. And disabled by default in GitLab 15.0 [2]

* Update docs to mark clusters as deprecated * Remove testing of clusters

[1] https://docs.gitlab.com/ee/api/project_clusters.html [2]
  https://gitlab.com/groups/gitlab-org/configure/-/epics/8

- **deps**: Update dependency commitizen to v2.29.2
  ([`30274ea`](https://github.com/python-gitlab/python-gitlab/commit/30274ead81205946a5a7560e592f346075035e0e))

- **deps**: Update dependency flake8 to v5
  ([`cdc384b`](https://github.com/python-gitlab/python-gitlab/commit/cdc384b8a2096e31aff12ea98383e2b1456c5731))

- **deps**: Update dependency types-requests to v2.28.6
  ([`54dd4c3`](https://github.com/python-gitlab/python-gitlab/commit/54dd4c3f857f82aa8781b0daf22fa2dd3c60c2c4))

- **deps**: Update pre-commit hook commitizen-tools/commitizen to v2.29.2
  ([`4988c02`](https://github.com/python-gitlab/python-gitlab/commit/4988c029e0dda89ff43375d1cd2f407abdbe3dc7))

- **topics**: 'title' is required when creating a topic
  ([`271f688`](https://github.com/python-gitlab/python-gitlab/commit/271f6880dbb15b56305efc1fc73924ac26fb97ad))

In GitLab >= 15.0 `title` is required when creating a topic.

### Documentation

- Describe self-revoking personal access tokens
  ([`5ea48fc`](https://github.com/python-gitlab/python-gitlab/commit/5ea48fc3c28f872dd1184957a6f2385da075281c))

### Features

- Support downloading archive subpaths
  ([`cadb0e5`](https://github.com/python-gitlab/python-gitlab/commit/cadb0e55347cdac149e49f611c99b9d53a105520))

- **client**: Warn user on misconfigured URL in `auth()`
  ([`0040b43`](https://github.com/python-gitlab/python-gitlab/commit/0040b4337bae815cfe1a06f8371a7a720146f271))

### Refactoring

- **client**: Factor out URL check into a helper
  ([`af21a18`](https://github.com/python-gitlab/python-gitlab/commit/af21a1856aa904f331859983493fe966d5a2969b))

- **client**: Remove handling for incorrect link header
  ([`77c04b1`](https://github.com/python-gitlab/python-gitlab/commit/77c04b1acb2815290bcd6f50c37d75329409e9d3))

This was a quirk only present in GitLab 13.0 and fixed with 13.1. See
  https://gitlab.com/gitlab-org/gitlab/-/merge_requests/33714 and
  https://gitlab.com/gitlab-org/gitlab/-/issues/218504 for more context.

### Testing

- Attempt to make functional test startup more reliable
  ([`67508e8`](https://github.com/python-gitlab/python-gitlab/commit/67508e8100be18ce066016dcb8e39fa9f0c59e51))

The functional tests have been erratic. Current theory is that we are starting the tests before the
  GitLab container is fully up and running.

* Add checking of the Health Check[1] endpoints. * Add a 20 second delay after we believe it is up
  and running. * Increase timeout from 300 to 400 seconds

[1] https://docs.gitlab.com/ee/user/admin_area/monitoring/health_check.html

- **functional**: Bump GitLab docker image to 15.2.0-ee.0
  ([`69014e9`](https://github.com/python-gitlab/python-gitlab/commit/69014e9be3a781be6742478af820ea097d004791))

Use the GitLab docker image 15.2.0-ee.0 in the functional testing.

- **unit**: Reproduce duplicate encoded query params
  ([`6f71c66`](https://github.com/python-gitlab/python-gitlab/commit/6f71c663a302b20632558b4c94be428ba831ee7f))


## v3.7.0 (2022-07-28)

### Bug Fixes

- Add `get_all` param (and `--get-all`) to allow passing `all` to API
  ([`7c71d5d`](https://github.com/python-gitlab/python-gitlab/commit/7c71d5db1199164b3fa9958e3c3bc6ec96efc78d))

- Enable epic notes
  ([`5fc3216`](https://github.com/python-gitlab/python-gitlab/commit/5fc3216788342a2325662644b42e8c249b655ded))

Add the notes attribute to GroupEpic

- Ensure path elements are escaped
  ([`5d9c198`](https://github.com/python-gitlab/python-gitlab/commit/5d9c198769b00c8e7661e62aaf5f930ed32ef829))

Ensure the path elements that are passed to the server are escaped. For example a "/" will be
  changed to "%2F"

Closes: #2116

- Results returned by `attributes` property to show updates
  ([`e5affc8`](https://github.com/python-gitlab/python-gitlab/commit/e5affc8749797293c1373c6af96334f194875038))

Previously the `attributes` method would show the original values in a Gitlab Object even if they
  had been updated. Correct this so that the updated value will be returned.

Also use copy.deepcopy() to ensure that modifying the dictionary returned can not also modify the
  object.

- Support array types for most resources
  ([`d9126cd`](https://github.com/python-gitlab/python-gitlab/commit/d9126cd802dd3cfe529fa940300113c4ead3054b))

- Use the [] after key names for array variables in `params`
  ([`1af44ce`](https://github.com/python-gitlab/python-gitlab/commit/1af44ce8761e6ee8a9467a3e192f6c4d19e5cefe))

1. If a value is of type ArrayAttribute then append '[]' to the name of the value for query
  parameters (`params`).

This is step 3 in a series of steps of our goal to add full support for the GitLab API data
  types[1]: * array * hash * array of hashes

Step one was: commit 5127b1594c00c7364e9af15e42d2e2f2d909449b Step two was: commit
  a57334f1930752c70ea15847a39324fa94042460

Fixes: #1698

[1] https://docs.gitlab.com/ee/api/#encoding-api-parameters-of-array-and-hash-types

- **cli**: Remove irrelevant MR approval rule list filters
  ([`0daec5f`](https://github.com/python-gitlab/python-gitlab/commit/0daec5fa1428a56a6a927b133613e8b296248167))

- **config**: Raise error when gitlab id provided but no config file found
  ([`ac46c1c`](https://github.com/python-gitlab/python-gitlab/commit/ac46c1cb291c03ad14bc76f5f16c9f98f2a5a82d))

- **config**: Raise error when gitlab id provided but no config section found
  ([`1ef7018`](https://github.com/python-gitlab/python-gitlab/commit/1ef70188da1e29cd8ba95bf58c994ba7dd3010c5))

- **runners**: Fix listing for /runners/all
  ([`c6dd57c`](https://github.com/python-gitlab/python-gitlab/commit/c6dd57c56e92abb6184badf4708f5f5e65c6d582))

### Chores

- Add a `lazy` boolean attribute to `RESTObject`
  ([`a7e8cfb`](https://github.com/python-gitlab/python-gitlab/commit/a7e8cfbae8e53d2c4b1fb75d57d42f00db8abd81))

This can be used to tell if a `RESTObject` was created using `lazy=True`.

Add a message to the `AttributeError` if attribute access fails for an instance created with
  `lazy=True`.

- Change name of API functional test to `api_func_v4`
  ([`8cf5cd9`](https://github.com/python-gitlab/python-gitlab/commit/8cf5cd935cdeaf36a6877661c8dfb0be6c69f587))

The CLI test is `cli_func_v4` and using `api_func_v4` matches with that naming convention.

- Enable mypy check `strict_equality`
  ([`a29cd6c`](https://github.com/python-gitlab/python-gitlab/commit/a29cd6ce1ff7fa7f31a386cea3e02aa9ba3fb6c2))

Enable the `mypy` `strict_equality` check.

- Enable using GitLab EE in functional tests
  ([`17c01ea`](https://github.com/python-gitlab/python-gitlab/commit/17c01ea55806c722523f2f9aef0175455ec942c5))

Enable using GitLab Enterprise Edition (EE) in the functional tests. This will allow us to add
  functional tests for EE only features in the functional tests.

- Fix misspelling
  ([`2d08fc8`](https://github.com/python-gitlab/python-gitlab/commit/2d08fc89fb67de25ad41f64c86a9b8e96e4c261a))

- Fixtures: after delete() wait to verify deleted
  ([`1f73b6b`](https://github.com/python-gitlab/python-gitlab/commit/1f73b6b20f08a0fe4ce4cf9195702a03656a54e1))

In our fixtures that create: - groups - project merge requests - projects - users

They delete the created objects after use. Now wait to ensure the objects are deleted before
  continuing as having unexpected objects existing can impact some of our tests.

- Make reset_gitlab() better
  ([`d87d6b1`](https://github.com/python-gitlab/python-gitlab/commit/d87d6b12fd3d73875559924cda3fd4b20402d336))

Saw issues in the CI where reset_gitlab() would fail. It would fail to delete the group that is
  created when GitLab starts up. Extending the timeout didn't fix the issue.

Changed the code to use the new `helpers.safe_delete()` function. Which will delete the resource and
  then make sure it is deleted before returning.

Also added some logging functionality that can be seen if logging is turned on in pytest.

- Revert "test(functional): simplify token creation"
  ([`4b798fc`](https://github.com/python-gitlab/python-gitlab/commit/4b798fc2fdc44b73790c493c329147013464de14))

This reverts commit 67ab24fe5ae10a9f8cc9122b1a08848e8927635d.

- Simplify multi-nested try blocks
  ([`e734470`](https://github.com/python-gitlab/python-gitlab/commit/e7344709d931e2b254d225d77ca1474bc69971f8))

Instead of have a multi-nested series of try blocks. Convert it to a more readable series of `if`
  statements.

- **authors**: Fix email and do the ABC
  ([`9833632`](https://github.com/python-gitlab/python-gitlab/commit/98336320a66d1859ba73e084a5e86edc3aa1643c))

- **ci_lint**: Add create attributes
  ([`6e1342f`](https://github.com/python-gitlab/python-gitlab/commit/6e1342fc0b7cf740b25a939942ea02cdd18a9625))

- **deps**: Update black to v22.6.0
  ([`82bd596`](https://github.com/python-gitlab/python-gitlab/commit/82bd59673c5c66da0cfa3b24d58b627946fe2cc3))

- **deps**: Update dependency commitizen to v2.28.0
  ([`8703dd3`](https://github.com/python-gitlab/python-gitlab/commit/8703dd3c97f382920075e544b1b9d92fab401cc8))

- **deps**: Update dependency commitizen to v2.29.0
  ([`c365be1`](https://github.com/python-gitlab/python-gitlab/commit/c365be1b908c5e4fda445680c023607bdf6c6281))

- **deps**: Update dependency mypy to v0.971
  ([`7481d27`](https://github.com/python-gitlab/python-gitlab/commit/7481d271512eaa234315bcdbaf329026589bfda7))

- **deps**: Update dependency pylint to v2.14.4
  ([`2cee2d4`](https://github.com/python-gitlab/python-gitlab/commit/2cee2d4a86e76d3f63f3608ed6a92e64813613d3))

- **deps**: Update dependency pylint to v2.14.5
  ([`e153636`](https://github.com/python-gitlab/python-gitlab/commit/e153636d74a0a622b0cc18308aee665b3eca58a4))

- **deps**: Update dependency requests to v2.28.1
  ([`be33245`](https://github.com/python-gitlab/python-gitlab/commit/be3324597aa3f22b0692d3afa1df489f2709a73e))

- **deps**: Update pre-commit hook commitizen-tools/commitizen to v2.28.0
  ([`d238e1b`](https://github.com/python-gitlab/python-gitlab/commit/d238e1b464c98da86677934bf99b000843d36747))

- **deps**: Update pre-commit hook commitizen-tools/commitizen to v2.29.0
  ([`ad8d62a`](https://github.com/python-gitlab/python-gitlab/commit/ad8d62ae9612c173a749d413f7a84e5b8c0167cf))

- **deps**: Update pre-commit hook pycqa/pylint to v2.14.4
  ([`5cd39be`](https://github.com/python-gitlab/python-gitlab/commit/5cd39be000953907cdc2ce877a6bf267d601b707))

- **deps**: Update pre-commit hook pycqa/pylint to v2.14.5
  ([`c75a1d8`](https://github.com/python-gitlab/python-gitlab/commit/c75a1d860709e17a7c3324c5d85c7027733ea1e1))

- **deps**: Update typing dependencies
  ([`f2209a0`](https://github.com/python-gitlab/python-gitlab/commit/f2209a0ea084eaf7fbc89591ddfea138d99527a6))

- **deps**: Update typing dependencies
  ([`e772248`](https://github.com/python-gitlab/python-gitlab/commit/e77224818e63e818c10a7fad69f90e16d618bdf7))

- **docs**: Convert tabs to spaces
  ([`9ea5520`](https://github.com/python-gitlab/python-gitlab/commit/9ea5520cec8979000d7f5dbcc950f2250babea96))

Some tabs snuck into the documentation. Convert them to 4-spaces.

### Documentation

- Describe fetching existing export status
  ([`9c5b8d5`](https://github.com/python-gitlab/python-gitlab/commit/9c5b8d54745a58b9fe72ba535b7868d1510379c0))

- Describe ROPC flow in place of password authentication
  ([`91c17b7`](https://github.com/python-gitlab/python-gitlab/commit/91c17b704f51e9a06b241d549f9a07a19c286118))

- Document CI Lint usage
  ([`d5de4b1`](https://github.com/python-gitlab/python-gitlab/commit/d5de4b1fe38bedc07862bd9446dfd48b92cb078d))

- Update return type of pushrules
  ([`53cbecc`](https://github.com/python-gitlab/python-gitlab/commit/53cbeccd581318ce4ff6bec0acf3caf935bda0cf))

Update the return type of pushrules to surround None with back-ticks to make it code-formatted.

- **authors**: Add John
  ([`e2afb84`](https://github.com/python-gitlab/python-gitlab/commit/e2afb84dc4a259e8f40b7cc83e56289983c7db47))

- **cli**: Showcase use of token scopes
  ([`4a6f8d6`](https://github.com/python-gitlab/python-gitlab/commit/4a6f8d67a94a3d104a24081ad1dbad5b2e3d9c3e))

- **projects**: Document export with upload to URL
  ([`03f5484`](https://github.com/python-gitlab/python-gitlab/commit/03f548453d84d99354aae7b638f5267e5d751c59))

- **readme**: Remove redundant `-v` that breaks the command
  ([`c523e18`](https://github.com/python-gitlab/python-gitlab/commit/c523e186cc48f6bcac5245e3109b50a3852d16ef))

- **users**: Add docs about listing a user's projects
  ([`065a1a5`](https://github.com/python-gitlab/python-gitlab/commit/065a1a5a32d34286df44800084285b30b934f911))

Add docs about listing a user's projects.

Update docs on the membership API to update the URL to the upstream docs and also add a note that it
  requires Administrator access to use.

### Features

- Add 'merge_pipelines_enabled' project attribute
  ([`fc33c93`](https://github.com/python-gitlab/python-gitlab/commit/fc33c934d54fb94451bd9b9ad65645c9c3d6fe2e))

Boolean. Enable or disable merge pipelines.

See: https://docs.gitlab.com/ee/api/projects.html#edit-project
  https://docs.gitlab.com/ee/ci/pipelines/merged_results_pipelines.html

- Add `asdict()` and `to_json()` methods to Gitlab Objects
  ([`08ac071`](https://github.com/python-gitlab/python-gitlab/commit/08ac071abcbc28af04c0fa655576e25edbdaa4e2))

Add an `asdict()` method that returns a dictionary representation copy of the Gitlab Object. This is
  a copy and changes made to it will have no impact on the Gitlab Object.

The `asdict()` method name was chosen as both the `dataclasses` and `attrs` libraries have an
  `asdict()` function which has the similar purpose of creating a dictionary represenation of an
  object.

Also add a `to_json()` method that returns a JSON string representation of the object.

Closes: #1116

- Add support for filtering jobs by scope
  ([`0e1c0dd`](https://github.com/python-gitlab/python-gitlab/commit/0e1c0dd795886ae4741136e64c33850b164084a1))

See: 'scope' here:

https://docs.gitlab.com/ee/api/jobs.html#list-project-jobs

- Add support for group and project invitations API
  ([`7afd340`](https://github.com/python-gitlab/python-gitlab/commit/7afd34027a26b5238a979e3303d8e5d8a0320a07))

- Add support for group push rules
  ([`b5cdc09`](https://github.com/python-gitlab/python-gitlab/commit/b5cdc097005c8a48a16e793a69c343198b14e035))

Add the GroupPushRules and GroupPushRulesManager classes.

Closes: #1259

- Add support for iterations API
  ([`194ee01`](https://github.com/python-gitlab/python-gitlab/commit/194ee0100c2868c1a9afb161c15f3145efb01c7c))

- Allow sort/ordering for project releases
  ([`b1dd284`](https://github.com/python-gitlab/python-gitlab/commit/b1dd284066b4b94482b9d41310ac48b75bcddfee))

See: https://docs.gitlab.com/ee/api/releases/#list-releases

- Support validating CI lint results
  ([`3b1ede4`](https://github.com/python-gitlab/python-gitlab/commit/3b1ede4a27cd730982d4c579437c5c689a8799e5))

- **api**: Add support for `get` for a MR approval rule
  ([`89c18c6`](https://github.com/python-gitlab/python-gitlab/commit/89c18c6255ec912db319f73f141b47ace87a713b))

In GitLab 14.10 they added support to get a single merge request approval rule [1]

Add support for it to ProjectMergeRequestApprovalRuleManager

[1]
  https://docs.gitlab.com/ee/api/merge_request_approvals.html#get-a-single-merge-request-level-rule

- **api**: Add support for instance-level registry repositories
  ([`284d739`](https://github.com/python-gitlab/python-gitlab/commit/284d73950ad5cf5dfbdec2f91152ed13931bd0ee))

- **cli**: Add a custom help formatter
  ([`005ba93`](https://github.com/python-gitlab/python-gitlab/commit/005ba93074d391f818c39e46390723a0d0d16098))

Add a custom argparse help formatter that overrides the output format to list items vertically.

The formatter is derived from argparse.HelpFormatter with minimal changes.

Co-authored-by: John Villalovos <john@sodarock.com>

Co-authored-by: Nejc Habjan <nejc.habjan@siemens.com>

- **cli**: Add support for global CI lint
  ([`3f67c4b`](https://github.com/python-gitlab/python-gitlab/commit/3f67c4b0fb0b9a39c8b93529a05b1541fcebcabe))

- **groups**: Add support for group-level registry repositories
  ([`70148c6`](https://github.com/python-gitlab/python-gitlab/commit/70148c62a3aba16dd8a9c29f15ed16e77c01a247))

- **groups**: Add support for shared projects API
  ([`66461ba`](https://github.com/python-gitlab/python-gitlab/commit/66461ba519a85bfbd3cba284a0c8de11a3ac7cde))

- **issues**: Add support for issue reorder API
  ([`8703324`](https://github.com/python-gitlab/python-gitlab/commit/8703324dc21a30757e15e504b7d20472f25d2ab9))

- **namespaces**: Add support for namespace existence API
  ([`4882cb2`](https://github.com/python-gitlab/python-gitlab/commit/4882cb22f55c41d8495840110be2d338b5545a04))

- **objects**: Add Project CI Lint support
  ([`b213dd3`](https://github.com/python-gitlab/python-gitlab/commit/b213dd379a4108ab32181b9d3700d2526d950916))

Add support for validating a project's CI configuration [1]

[1] https://docs.gitlab.com/ee/api/lint.html

- **projects**: Add support for project restore API
  ([`4794ecc`](https://github.com/python-gitlab/python-gitlab/commit/4794ecc45d7aa08785c622918d08bb046e7359ae))

### Refactoring

- Migrate services to integrations
  ([`a428051`](https://github.com/python-gitlab/python-gitlab/commit/a4280514546cc6e39da91d1671921b74b56c3283))

- **objects**: Move ci lint to separate file
  ([`6491f1b`](https://github.com/python-gitlab/python-gitlab/commit/6491f1bbb68ffe04c719eb9d326b7ca3e78eba84))

- **test-projects**: Apply suggestions and use fixtures
  ([`a51f848`](https://github.com/python-gitlab/python-gitlab/commit/a51f848db4204b2f37ae96fd235ae33cb7c2fe98))

- **test-projects**: Remove test_restore_project
  ([`9be0875`](https://github.com/python-gitlab/python-gitlab/commit/9be0875c3793324b4c4dde29519ee62b39a8cc18))

### Testing

- Add more tests for container registries
  ([`f6b6e18`](https://github.com/python-gitlab/python-gitlab/commit/f6b6e18f96f4cdf67c8c53ae79e6a8259dcce9ee))

- Add test to show issue fixed
  ([`75bec7d`](https://github.com/python-gitlab/python-gitlab/commit/75bec7d543dd740c50452b21b0b4509377cd40ce))

https://github.com/python-gitlab/python-gitlab/issues/1698 has been fixed. Add test to show that.

- Allow `podman` users to run functional tests
  ([`ff215b7`](https://github.com/python-gitlab/python-gitlab/commit/ff215b7056ce2adf2b85ecc1a6c3227d2b1a5277))

Users of `podman` will likely have `DOCKER_HOST` set to something like
  `unix:///run/user/1000/podman/podman.sock`

Pass this environment variable so that it will be used during the functional tests.

- Always ensure clean config environment
  ([`8d4f13b`](https://github.com/python-gitlab/python-gitlab/commit/8d4f13b192afd5d4610eeaf2bbea71c3b6a25964))

- Fix broken test if user had config files
  ([`864fc12`](https://github.com/python-gitlab/python-gitlab/commit/864fc1218e6366b9c1d8b1b3832e06049c238d8c))

Use `monkeypatch` to ensure that no config files are reported for the test.

Closes: #2172

- **api_func_v4**: Catch deprecation warning for `gl.lint()`
  ([`95fe924`](https://github.com/python-gitlab/python-gitlab/commit/95fe9247fcc9cba65c4afef934f816be06027ff5))

Catch the deprecation warning for the call to `gl.lint()`, so it won't show up in the log.

- **cli**: Add tests for token scopes
  ([`263fe3d`](https://github.com/python-gitlab/python-gitlab/commit/263fe3d24836b34dccdcee0221bd417e0b74fb2e))

- **ee**: Add an EE specific test
  ([`10987b3`](https://github.com/python-gitlab/python-gitlab/commit/10987b3089d4fe218dd2116dd871e0a070db3f7f))

- **functional**: Replace len() calls with list membership checks
  ([`97e0eb9`](https://github.com/python-gitlab/python-gitlab/commit/97e0eb9267202052ed14882258dceca0f6c4afd7))

- **functional**: Simplify token creation
  ([`67ab24f`](https://github.com/python-gitlab/python-gitlab/commit/67ab24fe5ae10a9f8cc9122b1a08848e8927635d))

- **functional**: Use both get_all and all in list() tests
  ([`201298d`](https://github.com/python-gitlab/python-gitlab/commit/201298d7b5795b7d7338793da8033dc6c71d6572))

- **projects**: Add unit tests for projects
  ([`67942f0`](https://github.com/python-gitlab/python-gitlab/commit/67942f0d46b7d445f28f80d3f57aa91eeea97a24))


## v3.6.0 (2022-06-28)

### Bug Fixes

- **base**: Do not fail repr() on lazy objects
  ([`1efb123`](https://github.com/python-gitlab/python-gitlab/commit/1efb123f63eab57600228b75a1744f8787c16671))

- **cli**: Fix project export download for CLI
  ([`5d14867`](https://github.com/python-gitlab/python-gitlab/commit/5d1486785793b02038ac6f527219801744ee888b))

Since ac1c619cae6481833f5df91862624bf0380fef67 we delete parent arg keys from the args dict so this
  has been trying to access the wrong attribute.

- **cli**: Project-merge-request-approval-rule
  ([`15a242c`](https://github.com/python-gitlab/python-gitlab/commit/15a242c3303759b77b380c5b3ff9d1e0bf2d800c))

Using the CLI the command: gitlab project-merge-request-approval-rule list --mr-iid 1 --project-id
  foo/bar

Would raise an exception. This was due to the fact that `_id_attr` and `_repr_attr` were set for
  keys which are not returned in the response.

Add a unit test which shows the `repr` function now works. Before it did not.

This is an EE feature so we can't functional test it.

Closes: #2065

### Chores

- Add link to Commitizen in Github workflow
  ([`d08d07d`](https://github.com/python-gitlab/python-gitlab/commit/d08d07deefae345397fc30280c4f790c7e61cbe2))

Add a link to the Commitizen website in the Github workflow. Hopefully this will help people when
  their job fails.

- Bump mypy pre-commit hook
  ([`0bbcad7`](https://github.com/python-gitlab/python-gitlab/commit/0bbcad7612f60f7c7b816c06a244ad8db9da68d9))

- Correct ModuleNotFoundError() arguments
  ([`0b7933c`](https://github.com/python-gitlab/python-gitlab/commit/0b7933c5632c2f81c89f9a97e814badf65d1eb38))

Previously in commit 233b79ed442aac66faf9eb4b0087ea126d6dffc5 I had used the `name` argument for
  `ModuleNotFoundError()`. This basically is the equivalent of not passing any message to
  `ModuleNotFoundError()`. So when the exception was raised it wasn't very helpful.

Correct that and add a unit-test that shows we get the message we expect.

- Enable 'consider-using-sys-exit' pylint check
  ([`0afcc3e`](https://github.com/python-gitlab/python-gitlab/commit/0afcc3eca4798801ff3635b05b871e025078ef31))

Enable the 'consider-using-sys-exit' pylint check and fix errors raised.

- Enable pylint check "raise-missing-from"
  ([`1a2781e`](https://github.com/python-gitlab/python-gitlab/commit/1a2781e477471626e2b00129bef5169be9c7cc06))

Enable the pylint check "raise-missing-from" and fix errors detected.

- Enable pylint check: "attribute-defined-outside-init"
  ([`d6870a9`](https://github.com/python-gitlab/python-gitlab/commit/d6870a981259ee44c64210a756b63dc19a6f3957))

Enable the pylint check: "attribute-defined-outside-init" and fix errors detected.

- Enable pylint check: "no-else-return"
  ([`d0b0811`](https://github.com/python-gitlab/python-gitlab/commit/d0b0811211f69f08436dcf7617c46617fe5c0b8b))

Enable the pylint check "no-else-return" and fix the errors detected.

- Enable pylint check: "no-self-use"
  ([`80aadaf`](https://github.com/python-gitlab/python-gitlab/commit/80aadaf4262016a8181b5150ca7e17c8139c15fa))

Enable the pylint check "no-self-use" and fix the errors detected.

- Enable pylint check: "redefined-outer-name",
  ([`1324ce1`](https://github.com/python-gitlab/python-gitlab/commit/1324ce1a439befb4620953a4df1f70b74bf70cbd))

Enable the pylint check "redefined-outer-name" and fix the errors detected.

- Enable pylint checks
  ([`1e89164`](https://github.com/python-gitlab/python-gitlab/commit/1e8916438f7c4f67bd7745103b870d84f6ba2d01))

Enable the pylint checks: * unnecessary-pass * unspecified-encoding

Update code to resolve errors found

- Enable pylint checks which require no changes
  ([`50fdbc4`](https://github.com/python-gitlab/python-gitlab/commit/50fdbc474c524188952e0ef7c02b0bd92df82357))

Enabled the pylint checks that don't require any code changes. Previously these checks were
  disabled.

- Fix issue found with pylint==2.14.3
  ([`eeab035`](https://github.com/python-gitlab/python-gitlab/commit/eeab035ab715e088af73ada00e0a3b0c03527187))

A new error was reported when running pylint==2.14.3: gitlab/client.py:488:0: W1404: Implicit string
  concatenation found in call (implicit-str-concat)

Fixed this issue.

- Have `EncodedId` creation always return `EncodedId`
  ([`a1a246f`](https://github.com/python-gitlab/python-gitlab/commit/a1a246fbfcf530732249a263ee42757a862181aa))

There is no reason to return an `int` as we can always return a `str` version of the `int`

Change `EncodedId` to always return an `EncodedId`. This removes the need to have `mypy` ignore the
  error raised.

- Move `RequiredOptional` to the `gitlab.types` module
  ([`7d26530`](https://github.com/python-gitlab/python-gitlab/commit/7d26530640eb406479f1604cb64748d278081864))

By having `RequiredOptional` in the `gitlab.base` module it makes it difficult with circular
  imports. Move it to the `gitlab.types` module which has no dependencies on any other gitlab
  module.

- Move `utils._validate_attrs` inside `types.RequiredOptional`
  ([`9d629bb`](https://github.com/python-gitlab/python-gitlab/commit/9d629bb97af1e14ce8eb4679092de2393e1e3a05))

Move the `validate_attrs` function to be inside the `RequiredOptional` class. It makes sense for it
  to be part of the class as it is working on data related to the class.

- Patch sphinx for explicit re-exports
  ([`06871ee`](https://github.com/python-gitlab/python-gitlab/commit/06871ee05b79621f0a6fea47243783df105f64d6))

- Remove use of '%' string formatter in `gitlab/utils.py`
  ([`0c5a121`](https://github.com/python-gitlab/python-gitlab/commit/0c5a1213ba3bb3ec4ed5874db4588d21969e9e80))

Replace usage with f-string

- Rename `__call__()` to `run()` in GitlabCLI
  ([`6189437`](https://github.com/python-gitlab/python-gitlab/commit/6189437d2c8d18f6c7d72aa7743abd6d36fb4efa))

Less confusing to have it be a normal method.

- Rename `whaction` and `action` to `resource_action` in CLI
  ([`fb3f28a`](https://github.com/python-gitlab/python-gitlab/commit/fb3f28a053f0dcf0a110bb8b6fd11696b4ba3dd9))

Rename the variables `whaction` and `action` to `resource_action` to improve code-readability.

- Rename `what` to `gitlab_resource`
  ([`c86e471`](https://github.com/python-gitlab/python-gitlab/commit/c86e471dead930468172f4b7439ea6fa207f12e8))

Naming a variable `what` makes it difficult to understand what it is used for.

Rename it to `gitlab_resource` as that is what is being stored.

The Gitlab documentation talks about them being resources:
  https://docs.gitlab.com/ee/api/api_resources.html

This will improve code readability.

- Require f-strings
  ([`96e994d`](https://github.com/python-gitlab/python-gitlab/commit/96e994d9c5c1abd11b059fe9f0eec7dac53d2f3a))

We previously converted all string formatting to use f-strings. Enable pylint check to enforce this.

- Update type-hints return signature for GetWithoutIdMixin methods
  ([`aa972d4`](https://github.com/python-gitlab/python-gitlab/commit/aa972d49c57f2ebc983d2de1cfb8d18924af6734))

Commit f0152dc3cc9a42aa4dc3c0014b4c29381e9b39d6 removed situation where `get()` in a
  `GetWithoutIdMixin` based class could return `None`

Update the type-hints to no longer return `Optional` AKA `None`

- Use multiple processors when running PyLint
  ([`7f2240f`](https://github.com/python-gitlab/python-gitlab/commit/7f2240f1b9231e8b856706952ec84234177a495b))

Use multiple processors when running PyLint. On my system it took about 10.3 seconds to run PyLint
  before this change. After this change it takes about 5.8 seconds to run PyLint.

- **ci**: Increase timeout for docker container to come online
  ([`bda020b`](https://github.com/python-gitlab/python-gitlab/commit/bda020bf5f86d20253f39698c3bb32f8d156de60))

Have been seeing timeout issues more and more. Increase timeout from 200 seconds to 300 seconds (5
  minutes).

- **ci**: Pin 3.11 to beta.1
  ([`7119f2d`](https://github.com/python-gitlab/python-gitlab/commit/7119f2d228115fe83ab23612e189c9986bb9fd1b))

- **cli**: Ignore coverage on exceptions triggering cli.die
  ([`98ccc3c`](https://github.com/python-gitlab/python-gitlab/commit/98ccc3c2622a3cdb24797fd8790e921f5f2c1e6a))

- **cli**: Rename "object" to "GitLab resource"
  ([`62e64a6`](https://github.com/python-gitlab/python-gitlab/commit/62e64a66dab4b3704d80d19a5dbc68b025b18e3c))

Make the parser name more user friendly by renaming from generic "object" to "GitLab resource"

- **deps**: Ignore python-semantic-release updates
  ([`f185b17`](https://github.com/python-gitlab/python-gitlab/commit/f185b17ff5aabedd32d3facd2a46ebf9069c9692))

- **deps**: Update actions/setup-python action to v4
  ([`77c1f03`](https://github.com/python-gitlab/python-gitlab/commit/77c1f0352adc8488041318e5dfd2fa98a5b5af62))

- **deps**: Update dependency commitizen to v2.27.1
  ([`456f9f1`](https://github.com/python-gitlab/python-gitlab/commit/456f9f14453f2090fdaf88734fe51112bf4e7fde))

- **deps**: Update dependency mypy to v0.960
  ([`8c016c7`](https://github.com/python-gitlab/python-gitlab/commit/8c016c7a53c543d07d16153039053bb370a6945b))

- **deps**: Update dependency mypy to v0.961
  ([`f117b2f`](https://github.com/python-gitlab/python-gitlab/commit/f117b2f92226a507a8adbb42023143dac0cc07fc))

- **deps**: Update dependency pylint to v2.14.3
  ([`9a16bb1`](https://github.com/python-gitlab/python-gitlab/commit/9a16bb158f3cb34a4c4cb7451127fbc7c96642e2))

- **deps**: Update dependency requests to v2.28.0
  ([`d361f4b`](https://github.com/python-gitlab/python-gitlab/commit/d361f4bd4ec066452a75cf04f64334234478bb02))

- **deps**: Update pre-commit hook commitizen-tools/commitizen to v2.27.1
  ([`22c5db4`](https://github.com/python-gitlab/python-gitlab/commit/22c5db4bcccf592f5cf7ea34c336208c21769896))

- **deps**: Update pre-commit hook pycqa/pylint to v2.14.3
  ([`d1fe838`](https://github.com/python-gitlab/python-gitlab/commit/d1fe838b65ccd1a68fb6301bbfd06cd19425a75c))

- **deps**: Update typing dependencies
  ([`acc5c39`](https://github.com/python-gitlab/python-gitlab/commit/acc5c3971f13029288dff2909692a0171f4a66f7))

- **deps**: Update typing dependencies
  ([`aebf9c8`](https://github.com/python-gitlab/python-gitlab/commit/aebf9c83a4cbf7cf4243cb9b44375ca31f9cc878))

- **deps**: Update typing dependencies
  ([`f3f79c1`](https://github.com/python-gitlab/python-gitlab/commit/f3f79c1d3afa923405b83dcea905fec213201452))

- **docs**: Ignore nitpicky warnings
  ([`1c3efb5`](https://github.com/python-gitlab/python-gitlab/commit/1c3efb50bb720a87b95307f4d6642e3b7f28f6f0))

- **gitlab**: Fix implicit re-exports for mpypy
  ([`981b844`](https://github.com/python-gitlab/python-gitlab/commit/981b8448dbadc63d70867dc069e33d4c4d1cfe95))

- **mixins**: Remove None check as http_get always returns value
  ([`f0152dc`](https://github.com/python-gitlab/python-gitlab/commit/f0152dc3cc9a42aa4dc3c0014b4c29381e9b39d6))

- **workflows**: Explicitly use python-version
  ([`eb14475`](https://github.com/python-gitlab/python-gitlab/commit/eb1447588dfbbdfe724fca9009ea5451061b5ff0))

### Documentation

- Documentation updates to reflect addition of mutually exclusive attributes
  ([`24b720e`](https://github.com/python-gitlab/python-gitlab/commit/24b720e49636044f4be7e4d6e6ce3da341f2aeb8))

- Drop deprecated setuptools build_sphinx
  ([`048d66a`](https://github.com/python-gitlab/python-gitlab/commit/048d66af51cef385b22d223ed2a5cd30e2256417))

- Use `as_list=False` or `all=True` in Getting started
  ([`de8c6e8`](https://github.com/python-gitlab/python-gitlab/commit/de8c6e80af218d93ca167f8b5ff30319a2781d91))

In the "Getting started with the API" section of the documentation, use either `as_list=False` or
  `all=True` in the example usages of the `list()` method.

Also add a warning about the fact that `list()` by default does not return all items.

- **api**: Add separate section for advanced usage
  ([`22ae101`](https://github.com/python-gitlab/python-gitlab/commit/22ae1016f39256b8e2ca02daae8b3c7130aeb8e6))

- **api**: Document usage of head() methods
  ([`f555bfb`](https://github.com/python-gitlab/python-gitlab/commit/f555bfb363779cc6c8f8036f6d6cfa302e15d4fe))

- **api**: Fix incorrect docs for merge_request_approvals
  ([#2094](https://github.com/python-gitlab/python-gitlab/pull/2094),
  [`5583eaa`](https://github.com/python-gitlab/python-gitlab/commit/5583eaa108949386c66290fecef4d064f44b9e83))

* docs(api): fix incorrect docs for merge_request_approvals

The `set_approvers()` method is on the `ProjectApprovalManager` class. It is not part of the
  `ProjectApproval` class.

The docs were previously showing to call `set_approvers` using a `ProjectApproval` instance, which
  would fail. Correct the documentation.

This was pointed out by a question on the Gitter channel.

Co-authored-by: Nejc Habjan <nejc.habjan@siemens.com>

- **api**: Stop linking to python-requests.org
  ([`49c7e83`](https://github.com/python-gitlab/python-gitlab/commit/49c7e83f768ee7a3fec19085a0fa0a67eadb12df))

- **api-usage**: Add import os in example
  ([`2194a44`](https://github.com/python-gitlab/python-gitlab/commit/2194a44be541e9d2c15d3118ba584a4a173927a2))

- **ext**: Fix rendering for RequiredOptional dataclass
  ([`4d431e5`](https://github.com/python-gitlab/python-gitlab/commit/4d431e5a6426d0fd60945c2d1ff00a00a0a95b6c))

- **projects**: Document 404 gotcha with unactivated integrations
  ([`522ecff`](https://github.com/python-gitlab/python-gitlab/commit/522ecffdb6f07e6c017139df4eb5d3fc42a585b7))

- **projects**: Provide more detailed import examples
  ([`8f8611a`](https://github.com/python-gitlab/python-gitlab/commit/8f8611a1263b8c19fd19ce4a904a310b0173b6bf))

- **usage**: Refer to upsteam docs instead of custom attributes
  ([`ae7d3b0`](https://github.com/python-gitlab/python-gitlab/commit/ae7d3b09352b2a1bd287f95d4587b04136c7a4ed))

- **variables**: Instruct users to follow GitLab rules for values
  ([`194b6be`](https://github.com/python-gitlab/python-gitlab/commit/194b6be7ccec019fefc04754f98b9ec920c29568))

### Features

- Add support for Protected Environments
  ([`1dc9d0f`](https://github.com/python-gitlab/python-gitlab/commit/1dc9d0f91757eed9f28f0c7172654b9b2a730216))

- https://docs.gitlab.com/ee/api/protected_environments.html -
  https://github.com/python-gitlab/python-gitlab/issues/1130

no write operation are implemented yet as I have no use case right now and am not sure how it should
  be done

- Support mutually exclusive attributes and consolidate validation to fix board lists
  ([#2037](https://github.com/python-gitlab/python-gitlab/pull/2037),
  [`3fa330c`](https://github.com/python-gitlab/python-gitlab/commit/3fa330cc341bbedb163ba757c7f6578d735c6efb))

add exclusive tuple to RequiredOptional data class to support for mutually exclusive attributes

consolidate _check_missing_create_attrs and _check_missing_update_attrs from mixins.py into
  _validate_attrs in utils.py

change _create_attrs in board list manager classes from required=('label_ld',) to
  exclusive=('label_id','asignee_id','milestone_id')

closes https://github.com/python-gitlab/python-gitlab/issues/1897

- **api**: Convert gitlab.const to Enums
  ([`c3c6086`](https://github.com/python-gitlab/python-gitlab/commit/c3c6086c548c03090ccf3f59410ca3e6b7999791))

This allows accessing the elements by value, i.e.:

import gitlab.const gitlab.const.AccessLevel(20)

- **api**: Implement HEAD method
  ([`90635a7`](https://github.com/python-gitlab/python-gitlab/commit/90635a7db3c9748745471d2282260418e31c7797))

- **api**: Support head() method for get and list endpoints
  ([`ce9216c`](https://github.com/python-gitlab/python-gitlab/commit/ce9216ccc542d834be7f29647c7ee98c2ca5bb01))

- **client**: Introduce `iterator=True` and deprecate `as_list=False` in `list()`
  ([`cdc6605`](https://github.com/python-gitlab/python-gitlab/commit/cdc6605767316ea59e1e1b849683be7b3b99e0ae))

`as_list=False` is confusing as it doesn't explain what is being returned. Replace it with
  `iterator=True` which more clearly explains to the user that an iterator/generator will be
  returned.

This maintains backward compatibility with `as_list` but does issue a DeprecationWarning if
  `as_list` is set.

- **docker**: Provide a Debian-based slim image
  ([`384031c`](https://github.com/python-gitlab/python-gitlab/commit/384031c530e813f55da52f2b2c5635ea935f9d91))

- **downloads**: Allow streaming downloads access to response iterator
  ([#1956](https://github.com/python-gitlab/python-gitlab/pull/1956),
  [`b644721`](https://github.com/python-gitlab/python-gitlab/commit/b6447211754e126f64e12fc735ad74fe557b7fb4))

* feat(downloads): allow streaming downloads access to response iterator

Allow access to the underlying response iterator when downloading in streaming mode by specifying
  `iterator=True`.

Update type annotations to support this change.

* docs(api-docs): add iterator example to artifact download

Document the usage of the `iterator=True` option when downloading artifacts

* test(packages): add tests for streaming downloads

- **users**: Add approve and reject methods to User
  ([`f57139d`](https://github.com/python-gitlab/python-gitlab/commit/f57139d8f1dafa6eb19d0d954b3634c19de6413c))

As requested in #1604.

Co-authored-by: John Villalovos <john@sodarock.com>

- **users**: Add ban and unban methods
  ([`0d44b11`](https://github.com/python-gitlab/python-gitlab/commit/0d44b118f85f92e7beb1a05a12bdc6e070dce367))

### Refactoring

- Avoid possible breaking change in iterator
  ([#2107](https://github.com/python-gitlab/python-gitlab/pull/2107),
  [`212ddfc`](https://github.com/python-gitlab/python-gitlab/commit/212ddfc9e9c5de50d2507cc637c01ceb31aaba41))

Commit b6447211754e126f64e12fc735ad74fe557b7fb4 inadvertently introduced a possible breaking change
  as it added a new argument `iterator` and added it in between existing (potentially positional)
  arguments.

This moves the `iterator` argument to the end of the argument list and requires it to be a
  keyword-only argument.

- Do not recommend plain gitlab.const constants
  ([`d652133`](https://github.com/python-gitlab/python-gitlab/commit/d65213385a6f497c2595d3af3a41756919b9c9a1))

- Remove no-op id argument in GetWithoutIdMixin
  ([`0f2a602`](https://github.com/python-gitlab/python-gitlab/commit/0f2a602d3a9d6579f5fdfdf945a236ae44e93a12))

- **mixins**: Extract custom type transforms into utils
  ([`09b3b22`](https://github.com/python-gitlab/python-gitlab/commit/09b3b2225361722f2439952d2dbee6a48a9f9fd9))

### Testing

- Add more tests for RequiredOptional
  ([`ce40fde`](https://github.com/python-gitlab/python-gitlab/commit/ce40fde9eeaabb4a30c5a87d9097b1d4eced1c1b))

- Add tests and clean up usage for new enums
  ([`323ab3c`](https://github.com/python-gitlab/python-gitlab/commit/323ab3c5489b0d35f268bc6c22ade782cade6ba4))

- Increase client coverage
  ([`00aec96`](https://github.com/python-gitlab/python-gitlab/commit/00aec96ed0b60720362c6642b416567ff39aef09))

- Move back to using latest Python 3.11 version
  ([`8c34781`](https://github.com/python-gitlab/python-gitlab/commit/8c347813e7aaf26a33fe5ae4ae73448beebfbc6c))

- **api**: Add tests for HEAD method
  ([`b0f02fa`](https://github.com/python-gitlab/python-gitlab/commit/b0f02facef2ea30f24dbfb3c52974f34823e9bba))

- **cli**: Improve coverage for custom actions
  ([`7327f78`](https://github.com/python-gitlab/python-gitlab/commit/7327f78073caa2fb8aaa6bf0e57b38dd7782fa57))

- **gitlab**: Increase unit test coverage
  ([`df072e1`](https://github.com/python-gitlab/python-gitlab/commit/df072e130aa145a368bbdd10be98208a25100f89))

- **pylint**: Enable pylint "unused-argument" check
  ([`23feae9`](https://github.com/python-gitlab/python-gitlab/commit/23feae9b0906d34043a784a01d31d1ff19ebc9a4))

Enable the pylint "unused-argument" check and resolve issues it found.

* Quite a few functions were accepting `**kwargs` but not then passing them on through to the next
  level. Now pass `**kwargs` to next level. * Other functions had no reason to accept `**kwargs`, so
  remove it * And a few other fixes.


## v3.5.0 (2022-05-28)

### Bug Fixes

- Duplicate subparsers being added to argparse
  ([`f553fd3`](https://github.com/python-gitlab/python-gitlab/commit/f553fd3c79579ab596230edea5899dc5189b0ac6))

Python 3.11 added an additional check in the argparse libary which detected duplicate subparsers
  being added. We had duplicate subparsers being added.

Make sure we don't add duplicate subparsers.

Closes: #2015

- **cli**: Changed default `allow_abbrev` value to fix arguments collision problem
  ([#2013](https://github.com/python-gitlab/python-gitlab/pull/2013),
  [`d68cacf`](https://github.com/python-gitlab/python-gitlab/commit/d68cacfeda5599c62a593ecb9da2505c22326644))

fix(cli): change default `allow_abbrev` value to fix argument collision

### Chores

- Add `cz` to default tox environment list and skip_missing_interpreters
  ([`ba8c052`](https://github.com/python-gitlab/python-gitlab/commit/ba8c0522dc8a116e7a22c42e21190aa205d48253))

Add the `cz` (`comittizen`) check by default.

Set skip_missing_interpreters = True so that when a user runs tox and doesn't have a specific
  version of Python it doesn't mark it as an error.

- Exclude `build/` directory from mypy check
  ([`989a12b`](https://github.com/python-gitlab/python-gitlab/commit/989a12b79ac7dff8bf0d689f36ccac9e3494af01))

The `build/` directory is created by the tox environment `twine-check`. When the `build/` directory
  exists `mypy` will have an error.

- Rename the test which runs `flake8` to be `flake8`
  ([`78b4f99`](https://github.com/python-gitlab/python-gitlab/commit/78b4f995afe99c530858b7b62d3eee620f3488f2))

Previously the test was called `pep8`. The test only runs `flake8` so call it `flake8` to be more
  precise.

- Run the `pylint` check by default in tox
  ([`55ace1d`](https://github.com/python-gitlab/python-gitlab/commit/55ace1d67e75fae9d74b4a67129ff842de7e1377))

Since we require `pylint` to pass in the CI. Let's run it by default in tox.

- **ci**: Fix prefix for action version
  ([`1c02189`](https://github.com/python-gitlab/python-gitlab/commit/1c021892e94498dbb6b3fa824d6d8c697fb4db7f))

- **ci**: Pin semantic-release version
  ([`0ea61cc`](https://github.com/python-gitlab/python-gitlab/commit/0ea61ccecae334c88798f80b6451c58f2fbb77c6))

- **ci**: Replace commitlint with commitizen
  ([`b8d15fe`](https://github.com/python-gitlab/python-gitlab/commit/b8d15fed0740301617445e5628ab76b6f5b8baeb))

- **deps**: Update dependency pylint to v2.13.8
  ([`b235bb0`](https://github.com/python-gitlab/python-gitlab/commit/b235bb00f3c09be5bb092a5bb7298e7ca55f2366))

- **deps**: Update dependency pylint to v2.13.9
  ([`4224950`](https://github.com/python-gitlab/python-gitlab/commit/422495073492fd52f4f3b854955c620ada4c1daa))

- **deps**: Update dependency types-requests to v2.27.23
  ([`a6fed8b`](https://github.com/python-gitlab/python-gitlab/commit/a6fed8b4a0edbe66bf29cd7a43d51d2f5b8b3e3a))

- **deps**: Update dependency types-requests to v2.27.24
  ([`f88e3a6`](https://github.com/python-gitlab/python-gitlab/commit/f88e3a641ebb83818e11713eb575ebaa597440f0))

- **deps**: Update dependency types-requests to v2.27.25
  ([`d6ea47a`](https://github.com/python-gitlab/python-gitlab/commit/d6ea47a175c17108e5388213abd59c3e7e847b02))

- **deps**: Update pre-commit hook pycqa/pylint to v2.13.8
  ([`1835593`](https://github.com/python-gitlab/python-gitlab/commit/18355938d1b410ad5e17e0af4ef0667ddb709832))

- **deps**: Update pre-commit hook pycqa/pylint to v2.13.9
  ([`1e22790`](https://github.com/python-gitlab/python-gitlab/commit/1e2279028533c3dc15995443362e290a4d2c6ae0))

- **renovate**: Set schedule to reduce noise
  ([`882fe7a`](https://github.com/python-gitlab/python-gitlab/commit/882fe7a681ae1c5120db5be5e71b196ae555eb3e))

### Documentation

- Add missing Admin access const value
  ([`3e0d4d9`](https://github.com/python-gitlab/python-gitlab/commit/3e0d4d9006e2ca6effae2b01cef3926dd0850e52))

As shown here, Admin access is set to 60:
  https://docs.gitlab.com/ee/api/protected_branches.html#protected-branches-api

- Update issue example and extend API usage docs
  ([`aad71d2`](https://github.com/python-gitlab/python-gitlab/commit/aad71d282d60dc328b364bcc951d0c9b44ab13fa))

- **CONTRIBUTING.rst**: Fix link to conventional-changelog commit format documentation
  ([`2373a4f`](https://github.com/python-gitlab/python-gitlab/commit/2373a4f13ee4e5279a424416cdf46782a5627067))

- **merge_requests**: Add new possible merge request state and link to the upstream docs
  ([`e660fa8`](https://github.com/python-gitlab/python-gitlab/commit/e660fa8386ed7783da5c076bc0fef83e6a66f9a8))

The actual documentation do not mention the locked state for a merge request

### Features

- Display human-readable attribute in `repr()` if present
  ([`6b47c26`](https://github.com/python-gitlab/python-gitlab/commit/6b47c26d053fe352d68eb22a1eaf4b9a3c1c93e7))

- **objects**: Support get project storage endpoint
  ([`8867ee5`](https://github.com/python-gitlab/python-gitlab/commit/8867ee59884ae81d6457ad6e561a0573017cf6b2))

- **ux**: Display project.name_with_namespace on project repr
  ([`e598762`](https://github.com/python-gitlab/python-gitlab/commit/e5987626ca1643521b16658555f088412be2a339))

This change the repr from:

$ gitlab.projects.get(id=some_id) <Project id:some_id>

To:

$ gitlab.projects.get(id=some_id) <Project id:some_id name_with_namespace:"group_name /
  project_name">

This is especially useful when working on random projects or listing of projects since users
  generally don't remember projects ids.

### Testing

- **projects**: Add tests for list project methods
  ([`fa47829`](https://github.com/python-gitlab/python-gitlab/commit/fa47829056a71e6b9b7f2ce913f2aebc36dc69e9))


## v3.4.0 (2022-04-28)

### Bug Fixes

- Add 52x range to retry transient failures and tests
  ([`c3ef1b5`](https://github.com/python-gitlab/python-gitlab/commit/c3ef1b5c1eaf1348a18d753dbf7bda3c129e3262))

- Add ChunkedEncodingError to list of retryable exceptions
  ([`7beb20f`](https://github.com/python-gitlab/python-gitlab/commit/7beb20ff7b7b85fb92fc6b647d9c1bdb7568f27c))

- Also retry HTTP-based transient errors
  ([`3b49e4d`](https://github.com/python-gitlab/python-gitlab/commit/3b49e4d61e6f360f1c787aa048edf584aec55278))

- Avoid passing redundant arguments to API
  ([`3431887`](https://github.com/python-gitlab/python-gitlab/commit/34318871347b9c563d01a13796431c83b3b1d58c))

- **cli**: Add missing filters for project commit list
  ([`149d244`](https://github.com/python-gitlab/python-gitlab/commit/149d2446fcc79b31d3acde6e6d51adaf37cbb5d3))

### Chores

- **client**: Remove duplicate code
  ([`5cbbf26`](https://github.com/python-gitlab/python-gitlab/commit/5cbbf26e6f6f3ce4e59cba735050e3b7f9328388))

- **deps**: Update black to v22.3.0
  ([`8d48224`](https://github.com/python-gitlab/python-gitlab/commit/8d48224c89cf280e510fb5f691e8df3292577f64))

- **deps**: Update codecov/codecov-action action to v3
  ([`292e91b`](https://github.com/python-gitlab/python-gitlab/commit/292e91b3cbc468c4a40ed7865c3c98180c1fe864))

- **deps**: Update dependency mypy to v0.950
  ([`241e626`](https://github.com/python-gitlab/python-gitlab/commit/241e626c8e88bc1b6b3b2fc37e38ed29b6912b4e))

- **deps**: Update dependency pylint to v2.13.3
  ([`0ae3d20`](https://github.com/python-gitlab/python-gitlab/commit/0ae3d200563819439be67217a7fc0e1552f07c90))

- **deps**: Update dependency pylint to v2.13.4
  ([`a9a9392`](https://github.com/python-gitlab/python-gitlab/commit/a9a93921b795eee0db16e453733f7c582fa13bc9))

- **deps**: Update dependency pylint to v2.13.5
  ([`5709675`](https://github.com/python-gitlab/python-gitlab/commit/570967541ecd46bfb83461b9d2c95bb0830a84fa))

- **deps**: Update dependency pylint to v2.13.7
  ([`5fb2234`](https://github.com/python-gitlab/python-gitlab/commit/5fb2234dddf73851b5de7af5d61b92de022a892a))

- **deps**: Update dependency pytest to v7.1.2
  ([`fd3fa23`](https://github.com/python-gitlab/python-gitlab/commit/fd3fa23bd4f7e0d66b541780f94e15635851e0db))

- **deps**: Update dependency types-requests to v2.27.16
  ([`ad799fc`](https://github.com/python-gitlab/python-gitlab/commit/ad799fca51a6b2679e2bcca8243a139e0bd0acf5))

- **deps**: Update dependency types-requests to v2.27.21
  ([`0fb0955`](https://github.com/python-gitlab/python-gitlab/commit/0fb0955b93ee1c464b3a5021bc22248103742f1d))

- **deps**: Update dependency types-requests to v2.27.22
  ([`22263e2`](https://github.com/python-gitlab/python-gitlab/commit/22263e24f964e56ec76d8cb5243f1cad1d139574))

- **deps**: Update dependency types-setuptools to v57.4.12
  ([`6551353`](https://github.com/python-gitlab/python-gitlab/commit/65513538ce60efdde80e5e0667b15739e6d90ac1))

- **deps**: Update pre-commit hook pycqa/pylint to v2.13.3
  ([`8f0a3af`](https://github.com/python-gitlab/python-gitlab/commit/8f0a3af46a1f49e6ddba31ee964bbe08c54865e0))

- **deps**: Update pre-commit hook pycqa/pylint to v2.13.4
  ([`9d0b252`](https://github.com/python-gitlab/python-gitlab/commit/9d0b25239773f98becea3b5b512d50f89631afb5))

- **deps**: Update pre-commit hook pycqa/pylint to v2.13.5
  ([`17d5c6c`](https://github.com/python-gitlab/python-gitlab/commit/17d5c6c3ba26f8b791ec4571726c533f5bbbde7d))

- **deps**: Update pre-commit hook pycqa/pylint to v2.13.7
  ([`1396221`](https://github.com/python-gitlab/python-gitlab/commit/1396221a96ea2f447b0697f589a50a9c22504c00))

- **deps**: Update typing dependencies
  ([`c12466a`](https://github.com/python-gitlab/python-gitlab/commit/c12466a0e7ceebd3fb9f161a472bbbb38e9bd808))

- **deps**: Update typing dependencies
  ([`d27cc6a`](https://github.com/python-gitlab/python-gitlab/commit/d27cc6a1219143f78aad7e063672c7442e15672e))

- **deps**: Upgrade gitlab-ce to 14.9.2-ce.0
  ([`d508b18`](https://github.com/python-gitlab/python-gitlab/commit/d508b1809ff3962993a2279b41b7d20e42d6e329))

### Documentation

- **api-docs**: Docs fix for application scopes
  ([`e1ad93d`](https://github.com/python-gitlab/python-gitlab/commit/e1ad93df90e80643866611fe52bd5c59428e7a88))

### Features

- Emit a warning when using a `list()` method returns max
  ([`1339d64`](https://github.com/python-gitlab/python-gitlab/commit/1339d645ce58a2e1198b898b9549ba5917b1ff12))

A common cause of issues filed and questions raised is that a user will call a `list()` method and
  only get 20 items. As this is the default maximum of items that will be returned from a `list()`
  method.

To help with this we now emit a warning when the result from a `list()` method is greater-than or
  equal to 20 (or the specified `per_page` value) and the user is not using either `all=True`,
  `all=False`, `as_list=False`, or `page=X`.

- **api**: Re-add topic delete endpoint
  ([`d1d96bd`](https://github.com/python-gitlab/python-gitlab/commit/d1d96bda5f1c6991c8ea61dca8f261e5b74b5ab6))

This reverts commit e3035a799a484f8d6c460f57e57d4b59217cd6de.

- **objects**: Support getting project/group deploy tokens by id
  ([`fcd37fe`](https://github.com/python-gitlab/python-gitlab/commit/fcd37feff132bd5b225cde9d5f9c88e62b3f1fd6))

- **user**: Support getting user SSH key by id
  ([`6f93c05`](https://github.com/python-gitlab/python-gitlab/commit/6f93c0520f738950a7c67dbeca8d1ac8257e2661))


## v3.3.0 (2022-03-28)

### Bug Fixes

- Support RateLimit-Reset header
  ([`4060146`](https://github.com/python-gitlab/python-gitlab/commit/40601463c78a6f5d45081700164899b2559b7e55))

Some endpoints are not returning the `Retry-After` header when rate-limiting occurrs. In those cases
  use the `RateLimit-Reset` [1] header, if available.

Closes: #1889

[1]
  https://docs.gitlab.com/ee/user/admin_area/settings/user_and_ip_rate_limits.html#response-headers

### Chores

- **deps**: Update actions/checkout action to v3
  ([`7333cbb`](https://github.com/python-gitlab/python-gitlab/commit/7333cbb65385145a14144119772a1854b41ea9d8))

- **deps**: Update actions/setup-python action to v3
  ([`7f845f7`](https://github.com/python-gitlab/python-gitlab/commit/7f845f7eade3c0cdceec6bfe7b3d087a8586edc5))

- **deps**: Update actions/stale action to v5
  ([`d841185`](https://github.com/python-gitlab/python-gitlab/commit/d8411853e224a198d0ead94242acac3aadef5adc))

- **deps**: Update actions/upload-artifact action to v3
  ([`18a0eae`](https://github.com/python-gitlab/python-gitlab/commit/18a0eae11c480d6bd5cf612a94e56cb9562e552a))

- **deps**: Update black to v22
  ([`3f84f1b`](https://github.com/python-gitlab/python-gitlab/commit/3f84f1bb805691b645fac2d1a41901abefccb17e))

- **deps**: Update dependency mypy to v0.931
  ([`33646c1`](https://github.com/python-gitlab/python-gitlab/commit/33646c1c4540434bed759d903c9b83af4e7d1a82))

- **deps**: Update dependency mypy to v0.940
  ([`dd11084`](https://github.com/python-gitlab/python-gitlab/commit/dd11084dd281e270a480b338aba88b27b991e58e))

- **deps**: Update dependency mypy to v0.941
  ([`3a9d4f1`](https://github.com/python-gitlab/python-gitlab/commit/3a9d4f1dc2069e29d559967e1f5498ccadf62591))

- **deps**: Update dependency mypy to v0.942
  ([`8ba0f8c`](https://github.com/python-gitlab/python-gitlab/commit/8ba0f8c6b42fa90bd1d7dd7015a546e8488c3f73))

- **deps**: Update dependency pylint to v2.13.0
  ([`5fa403b`](https://github.com/python-gitlab/python-gitlab/commit/5fa403bc461ed8a4d183dcd8f696c2a00b64a33d))

- **deps**: Update dependency pylint to v2.13.1
  ([`eefd724`](https://github.com/python-gitlab/python-gitlab/commit/eefd724545de7c96df2f913086a7f18020a5470f))

- **deps**: Update dependency pylint to v2.13.2
  ([`10f15a6`](https://github.com/python-gitlab/python-gitlab/commit/10f15a625187f2833be72d9bf527e75be001d171))

- **deps**: Update dependency pytest to v7
  ([`ae8d70d`](https://github.com/python-gitlab/python-gitlab/commit/ae8d70de2ad3ceb450a33b33e189bb0a3f0ff563))

- **deps**: Update dependency pytest to v7.1.0
  ([`27c7e33`](https://github.com/python-gitlab/python-gitlab/commit/27c7e3350839aaf5c06a15c1482fc2077f1d477a))

- **deps**: Update dependency pytest to v7.1.1
  ([`e31f2ef`](https://github.com/python-gitlab/python-gitlab/commit/e31f2efe97995f48c848f32e14068430a5034261))

- **deps**: Update dependency pytest-console-scripts to v1.3
  ([`9c202dd`](https://github.com/python-gitlab/python-gitlab/commit/9c202dd5a2895289c1f39068f0ea09812f28251f))

- **deps**: Update dependency pytest-console-scripts to v1.3.1
  ([`da392e3`](https://github.com/python-gitlab/python-gitlab/commit/da392e33e58d157169e5aa3f1fe725457e32151c))

- **deps**: Update dependency requests to v2.27.1
  ([`95dad55`](https://github.com/python-gitlab/python-gitlab/commit/95dad55b0cb02fd30172b5b5b9b05a25473d1f03))

- **deps**: Update dependency sphinx to v4.4.0
  ([`425d161`](https://github.com/python-gitlab/python-gitlab/commit/425d1610ca19be775d9fdd857e61d8b4a4ae4db3))

- **deps**: Update dependency sphinx to v4.5.0
  ([`36ab769`](https://github.com/python-gitlab/python-gitlab/commit/36ab7695f584783a4b3272edd928de3b16843a36))

- **deps**: Update dependency types-requests to v2.27.12
  ([`8cd668e`](https://github.com/python-gitlab/python-gitlab/commit/8cd668efed7bbbca370634e8c8cb10e3c7a13141))

- **deps**: Update dependency types-requests to v2.27.14
  ([`be6b54c`](https://github.com/python-gitlab/python-gitlab/commit/be6b54c6028036078ef09013f6c51c258173f3ca))

- **deps**: Update dependency types-requests to v2.27.15
  ([`2e8ecf5`](https://github.com/python-gitlab/python-gitlab/commit/2e8ecf569670afc943e8a204f3b2aefe8aa10d8b))

- **deps**: Update dependency types-setuptools to v57.4.10
  ([`b37fc41`](https://github.com/python-gitlab/python-gitlab/commit/b37fc4153a00265725ca655bc4482714d6b02809))

- **deps**: Update pre-commit hook alessandrojcm/commitlint-pre-commit-hook to v8
  ([`5440780`](https://github.com/python-gitlab/python-gitlab/commit/544078068bc9d7a837e75435e468e4749f7375ac))

- **deps**: Update pre-commit hook pycqa/pylint to v2.13.0
  ([`9fe60f7`](https://github.com/python-gitlab/python-gitlab/commit/9fe60f7b8fa661a8bba61c04fcb5b54359ac6778))

- **deps**: Update pre-commit hook pycqa/pylint to v2.13.1
  ([`1d0c6d4`](https://github.com/python-gitlab/python-gitlab/commit/1d0c6d423ce9f6c98511578acbb0f08dc4b93562))

- **deps**: Update pre-commit hook pycqa/pylint to v2.13.2
  ([`14d367d`](https://github.com/python-gitlab/python-gitlab/commit/14d367d60ab8f1e724c69cad0f39c71338346948))

- **deps**: Update typing dependencies
  ([`21e7c37`](https://github.com/python-gitlab/python-gitlab/commit/21e7c3767aa90de86046a430c7402f0934950e62))

- **deps**: Update typing dependencies
  ([`37a7c40`](https://github.com/python-gitlab/python-gitlab/commit/37a7c405c975359e9c1f77417e67063326c82a42))

### Code Style

- Reformat for black v22
  ([`93d4403`](https://github.com/python-gitlab/python-gitlab/commit/93d4403f0e46ed354cbcb133821d00642429532f))

### Documentation

- Add pipeline test report summary support
  ([`d78afb3`](https://github.com/python-gitlab/python-gitlab/commit/d78afb36e26f41d727dee7b0952d53166e0df850))

- Fix typo and incorrect style
  ([`2828b10`](https://github.com/python-gitlab/python-gitlab/commit/2828b10505611194bebda59a0e9eb41faf24b77b))

- **chore**: Include docs .js files in sdist
  ([`3010b40`](https://github.com/python-gitlab/python-gitlab/commit/3010b407bc9baabc6cef071507e8fa47c0f1624d))

### Features

- **object**: Add pipeline test report summary support
  ([`a97e0cf`](https://github.com/python-gitlab/python-gitlab/commit/a97e0cf81b5394b3a2b73d927b4efe675bc85208))


## v3.2.0 (2022-02-28)

### Bug Fixes

- Remove custom `delete` method for labels
  ([`0841a2a`](https://github.com/python-gitlab/python-gitlab/commit/0841a2a686c6808e2f3f90960e529b26c26b268f))

The usage of deleting was incorrect according to the current API. Remove custom `delete()` method as
  not needed.

Add tests to show it works with labels needing to be encoded.

Also enable the test_group_labels() test function. Previously it was disabled.

Add ability to do a `get()` for group labels.

Closes: #1867

- **services**: Use slug for id_attr instead of custom methods
  ([`e30f39d`](https://github.com/python-gitlab/python-gitlab/commit/e30f39dff5726266222b0f56c94f4ccfe38ba527))

### Chores

- Correct type-hints for per_page attrbute
  ([`e825653`](https://github.com/python-gitlab/python-gitlab/commit/e82565315330883823bd5191069253a941cb2683))

There are occasions where a GitLab `list()` call does not return the `x-per-page` header. For
  example the listing of custom attributes.

Update the type-hints to reflect that.

- Create a custom `warnings.warn` wrapper
  ([`6ca9aa2`](https://github.com/python-gitlab/python-gitlab/commit/6ca9aa2960623489aaf60324b4709848598aec91))

Create a custom `warnings.warn` wrapper that will walk the stack trace to find the first frame
  outside of the `gitlab/` path to print the warning against. This will make it easier for users to
  find where in their code the error is generated from

- Create new ArrayAttribute class
  ([`a57334f`](https://github.com/python-gitlab/python-gitlab/commit/a57334f1930752c70ea15847a39324fa94042460))

Create a new ArrayAttribute class. This is to indicate types which are sent to the GitLab server as
  arrays https://docs.gitlab.com/ee/api/#array

At this stage it is identical to the CommaSeparatedListAttribute class but will be used later to
  support the array types sent to GitLab.

This is the second step in a series of steps of our goal to add full support for the GitLab API data
  types[1]: * array * hash * array of hashes

Step one was: commit 5127b1594c00c7364e9af15e42d2e2f2d909449b

[1] https://docs.gitlab.com/ee/api/#encoding-api-parameters-of-array-and-hash-types

Related: #1698

- Require kwargs for `utils.copy_dict()`
  ([`7cf35b2`](https://github.com/python-gitlab/python-gitlab/commit/7cf35b2c0e44732ca02b74b45525cc7c789457fb))

The non-keyword arguments were a tiny bit confusing as the destination was first and the source was
  second.

Change the order and require key-word only arguments to ensure we don't silently break anyone.

- **ci**: Do not run release workflow in forks
  ([`2b6edb9`](https://github.com/python-gitlab/python-gitlab/commit/2b6edb9a0c62976ff88a95a953e9d3f2c7f6f144))

### Code Style

- **objects**: Add spacing to docstrings
  ([`700d25d`](https://github.com/python-gitlab/python-gitlab/commit/700d25d9bd812a64f5f1287bf50e8ddc237ec553))

### Documentation

- Add delete methods for runners and project artifacts
  ([`5e711fd`](https://github.com/python-gitlab/python-gitlab/commit/5e711fdb747fb3dcde1f5879c64dfd37bf25f3c0))

- Add retry_transient infos
  ([`bb1f054`](https://github.com/python-gitlab/python-gitlab/commit/bb1f05402887c78f9898fbd5bd66e149eff134d9))

Co-authored-by: Nejc Habjan <hab.nejc@gmail.com>

- Add transient errors retry info
  ([`b7a1266`](https://github.com/python-gitlab/python-gitlab/commit/b7a126661175a3b9b73dbb4cb88709868d6d871c))

- Enable gitter chat directly in docs
  ([`bd1ecdd`](https://github.com/python-gitlab/python-gitlab/commit/bd1ecdd5ad654b01b34e7a7a96821cc280b3ca67))

- Revert "chore: add temporary banner for v3"
  ([#1864](https://github.com/python-gitlab/python-gitlab/pull/1864),
  [`7a13b9b`](https://github.com/python-gitlab/python-gitlab/commit/7a13b9bfa4aead6c731f9a92e0946dba7577c61b))

This reverts commit a349793307e3a975bb51f864b48e5e9825f70182.

Co-authored-by: Wadim Klincov <wadim.klincov@siemens.com>

- **artifacts**: Deprecate artifacts() and artifact() methods
  ([`64d01ef`](https://github.com/python-gitlab/python-gitlab/commit/64d01ef23b1269b705350106d8ddc2962a780dce))

### Features

- **artifacts**: Add support for project artifacts delete API
  ([`c01c034`](https://github.com/python-gitlab/python-gitlab/commit/c01c034169789e1d20fd27a0f39f4c3c3628a2bb))

- **merge_request_approvals**: Add support for deleting MR approval rules
  ([`85a734f`](https://github.com/python-gitlab/python-gitlab/commit/85a734fec3111a4a5c4f0ddd7cb36eead96215e9))

- **mixins**: Allow deleting resources without IDs
  ([`0717517`](https://github.com/python-gitlab/python-gitlab/commit/0717517212b616cfd52cfd38dd5c587ff8f9c47c))

- **objects**: Add a complete artifacts manager
  ([`c8c2fa7`](https://github.com/python-gitlab/python-gitlab/commit/c8c2fa763558c4d9906e68031a6602e007fec930))

### Testing

- **functional**: Fix GitLab configuration to support pagination
  ([`5b7d00d`](https://github.com/python-gitlab/python-gitlab/commit/5b7d00df466c0fe894bafeb720bf94ffc8cd38fd))

When pagination occurs python-gitlab uses the URL provided by the GitLab server to use for the next
  request.

We had previously set the GitLab server configuraiton to say its URL was `http://gitlab.test` which
  is not in DNS. Set the hostname in the URL to `http://127.0.0.1:8080` which is the correct URL for
  the GitLab server to be accessed while doing functional tests.

Closes: #1877

- **objects**: Add tests for project artifacts
  ([`8ce0336`](https://github.com/python-gitlab/python-gitlab/commit/8ce0336325b339fa82fe4674a528f4bb59963df7))

- **runners**: Add test for deleting runners by auth token
  ([`14b88a1`](https://github.com/python-gitlab/python-gitlab/commit/14b88a13914de6ee54dd2a3bd0d5960a50578064))

- **services**: Add functional tests for services
  ([`2fea2e6`](https://github.com/python-gitlab/python-gitlab/commit/2fea2e64c554fd92d14db77cc5b1e2976b27b609))

- **unit**: Clean up MR approvals fixtures
  ([`0eb4f7f`](https://github.com/python-gitlab/python-gitlab/commit/0eb4f7f06c7cfe79c5d6695be82ac9ca41c8057e))


## v3.1.1 (2022-01-28)

### Bug Fixes

- **cli**: Allow custom methods in managers
  ([`8dfed0c`](https://github.com/python-gitlab/python-gitlab/commit/8dfed0c362af2c5e936011fd0b488b8b05e8a8a0))

- **cli**: Make 'per_page' and 'page' type explicit
  ([`d493a5e`](https://github.com/python-gitlab/python-gitlab/commit/d493a5e8685018daa69c92e5942cbe763e5dac62))

- **cli**: Make 'timeout' type explicit
  ([`bbb7df5`](https://github.com/python-gitlab/python-gitlab/commit/bbb7df526f4375c438be97d8cfa0d9ea9d604e7d))

- **objects**: Make resource access tokens and repos available in CLI
  ([`e0a3a41`](https://github.com/python-gitlab/python-gitlab/commit/e0a3a41ce60503a25fa5c26cf125364db481b207))

### Chores

- Always use context manager for file IO
  ([`e8031f4`](https://github.com/python-gitlab/python-gitlab/commit/e8031f42b6804415c4afee4302ab55462d5848ac))

- Consistently use open() encoding and file descriptor
  ([`dc32d54`](https://github.com/python-gitlab/python-gitlab/commit/dc32d54c49ccc58c01cd436346a3fbfd4a538778))

- Create return type-hints for `get_id()` & `encoded_id`
  ([`0c3a1d1`](https://github.com/python-gitlab/python-gitlab/commit/0c3a1d163895f660340a6c2b2f196ad996542518))

Create return type-hints for `RESTObject.get_id()` and `RESTObject.encoded_id`. Previously was
  saying they return Any. Be more precise in saying they can return either: None, str, or int.

- Don't explicitly pass args to super()
  ([`618267c`](https://github.com/python-gitlab/python-gitlab/commit/618267ced7aaff46d8e03057fa0cab48727e5dc0))

- Remove old-style classes
  ([`ae2a015`](https://github.com/python-gitlab/python-gitlab/commit/ae2a015db1017d3bf9b5f1c5893727da9b0c937f))

- Remove redundant list comprehension
  ([`271cfd3`](https://github.com/python-gitlab/python-gitlab/commit/271cfd3651e4e9cda974d5c3f411cecb6dca6c3c))

- Rename `gitlab/__version__.py` -> `gitlab/_version.py`
  ([`b981ce7`](https://github.com/python-gitlab/python-gitlab/commit/b981ce7fed88c5d86a3fffc4ee3f99be0b958c1d))

It is confusing to have a `gitlab/__version__.py` because we also create a variable
  `gitlab.__version__` which can conflict with `gitlab/__version__.py`.

For example in `gitlab/const.py` we have to know that `gitlab.__version__` is a module and not the
  variable due to the ordering of imports. But in most other usage `gitlab.__version__` is a version
  string.

To reduce confusion make the name of the version file `gitlab/_version.py`.

- Rename `types.ListAttribute` to `types.CommaSeparatedListAttribute`
  ([`5127b15`](https://github.com/python-gitlab/python-gitlab/commit/5127b1594c00c7364e9af15e42d2e2f2d909449b))

This name more accurately describes what the type is. Also this is the first step in a series of
  steps of our goal to add full support for the GitLab API data types[1]: * array * hash * array of
  hashes

[1] https://docs.gitlab.com/ee/api/#encoding-api-parameters-of-array-and-hash-types

- Use dataclass for RequiredOptional
  ([`30117a3`](https://github.com/python-gitlab/python-gitlab/commit/30117a3b6a8ee24362de798b2fa596a343b8774f))

- **tests**: Use method `projects.transfer()`
  ([`e5af2a7`](https://github.com/python-gitlab/python-gitlab/commit/e5af2a720cb5f97e5a7a5f639095fad76a48f218))

When doing the functional tests use the new function `projects.transfer` instead of the deprecated
  function `projects.transfer_project()`

### Code Style

- Use f-strings where applicable
  ([`cfed622`](https://github.com/python-gitlab/python-gitlab/commit/cfed62242e93490b8548c79f4ad16bd87de18e3e))

- Use literals to declare data structures
  ([`019a40f`](https://github.com/python-gitlab/python-gitlab/commit/019a40f840da30c74c1e74522a7707915061c756))

### Documentation

- Enhance release docs for CI_JOB_TOKEN usage
  ([`5d973de`](https://github.com/python-gitlab/python-gitlab/commit/5d973de8a5edd08f38031cf9be2636b0e12f008d))

- **changelog**: Add missing changelog items
  ([`01755fb`](https://github.com/python-gitlab/python-gitlab/commit/01755fb56a5330aa6fa4525086e49990e57ce50b))

### Testing

- Add a meta test to make sure that v4/objects/ files are imported
  ([`9c8c804`](https://github.com/python-gitlab/python-gitlab/commit/9c8c8043e6d1d9fadb9f10d47d7f4799ab904e9c))

Add a test to make sure that all of the `gitlab/v4/objects/` files are imported in
  `gitlab/v4/objects/__init__.py`

- Convert usage of `match_querystring` to `match`
  ([`d16e41b`](https://github.com/python-gitlab/python-gitlab/commit/d16e41bda2c355077cbdc419fe2e1d994fdea403))

In the `responses` library the usage of `match_querystring` is deprecated. Convert to using `match`

- Remove usage of httpmock library
  ([`5254f19`](https://github.com/python-gitlab/python-gitlab/commit/5254f193dc29d8854952aada19a72e5b4fc7ced0))

Convert all usage of the `httpmock` library to using the `responses` library.

- Use 'responses' in test_mixins_methods.py
  ([`208da04`](https://github.com/python-gitlab/python-gitlab/commit/208da04a01a4b5de8dc34e62c87db4cfa4c0d9b6))

Convert from httmock to responses in test_mixins_methods.py

This leaves only one file left to convert


## v3.1.0 (2022-01-14)

### Bug Fixes

- Broken URL for FAQ about attribute-error-list
  ([`1863f30`](https://github.com/python-gitlab/python-gitlab/commit/1863f30ea1f6fb7644b3128debdbb6b7bb218836))

The URL was missing a 'v' before the version number and thus the page did not exist.

Previously the URL for python-gitlab 3.0.0 was:
  https://python-gitlab.readthedocs.io/en/3.0.0/faq.html#attribute-error-list

Which does not exist.

Change it to: https://python-gitlab.readthedocs.io/en/v3.0.0/faq.html#attribute-error-list add the
  'v' --------------------------^

- Change to `http_list` for some ProjectCommit methods
  ([`497e860`](https://github.com/python-gitlab/python-gitlab/commit/497e860d834d0757d1c6532e107416c6863f52f2))

Fix the type-hints and use `http_list()` for the ProjectCommits methods: - diff() - merge_requests()
  - refs()

This will enable using the pagination support we have for lists.

Closes: #1805

Closes: #1231

- Remove custom URL encoding
  ([`3d49e5e`](https://github.com/python-gitlab/python-gitlab/commit/3d49e5e6a2bf1c9a883497acb73d7ce7115b804d))

We were using `str.replace()` calls to take care of URL encoding issues.

Switch them to use our `utils._url_encode()` function which itself uses `urllib.parse.quote()`

Closes: #1356

- Remove default arguments for mergerequests.merge()
  ([`8e589c4`](https://github.com/python-gitlab/python-gitlab/commit/8e589c43fa2298dc24b97423ffcc0ce18d911e3b))

The arguments `should_remove_source_branch` and `merge_when_pipeline_succeeds` are optional
  arguments. We should not be setting any default value for them.

https://docs.gitlab.com/ee/api/merge_requests.html#accept-mr

Closes: #1750

- Use url-encoded ID in all paths
  ([`12435d7`](https://github.com/python-gitlab/python-gitlab/commit/12435d74364ca881373d690eab89d2e2baa62a49))

Make sure all usage of the ID in the URL path is encoded. Normally it isn't an issue as most IDs are
  integers or strings which don't contain a slash ('/'). But when the ID is a string with a slash
  character it will break things.

Add a test case that shows this fixes wikis issue with subpages which use the slash character.

Closes: #1079

- **api**: Services: add missing `lazy` parameter
  ([`888f332`](https://github.com/python-gitlab/python-gitlab/commit/888f3328d3b1c82a291efbdd9eb01f11dff0c764))

Commit 8da0b758c589f608a6ae4eeb74b3f306609ba36d added the `lazy` parameter to the services `get()`
  method but missed then using the `lazy` parameter when it called `super(...).get(...)`

Closes: #1828

- **cli**: Add missing list filters for environments
  ([`6f64d40`](https://github.com/python-gitlab/python-gitlab/commit/6f64d4098ed4a890838c6cf43d7a679e6be4ac6c))

- **cli**: Url-encode path components of the URL
  ([`ac1c619`](https://github.com/python-gitlab/python-gitlab/commit/ac1c619cae6481833f5df91862624bf0380fef67))

In the CLI we need to make sure the components put into the path portion of the URL are url-encoded.
  Otherwise they will be interpreted as part of the path. For example can specify the project ID as
  a path, but in the URL it must be url-encoded or it doesn't work.

Also stop adding the components of the path as query parameters in the URL.

Closes: #783

Closes: #1498

- **members**: Use new *All objects for *AllManager managers
  ([`755e0a3`](https://github.com/python-gitlab/python-gitlab/commit/755e0a32e8ca96a3a3980eb7d7346a1a899ad58b))

Change it so that:

GroupMemberAllManager uses GroupMemberAll object ProjectMemberAllManager uses ProjectMemberAll
  object

Create GroupMemberAll and ProjectMemberAll objects that do not support any Mixin type methods.
  Previously we were using GroupMember and ProjectMember which support the `save()` and `delete()`
  methods but those methods will not work with objects retrieved using the `/members/all/` API
  calls.

`list()` API calls: [1] GET /groups/:id/members/all GET /projects/:id/members/all

`get()` API calls: [2] GET /groups/:id/members/all/:user_id GET /projects/:id/members/all/:user_id

Closes: #1825

Closes: #848

[1]
  https://docs.gitlab.com/ee/api/members.html#list-all-members-of-a-group-or-project-including-inherited-and-invited-members
  [2]
  https://docs.gitlab.com/ee/api/members.html#get-a-member-of-a-group-or-project-including-inherited-and-invited-members

### Chores

- Add `pprint()` and `pformat()` methods to RESTObject
  ([`d69ba04`](https://github.com/python-gitlab/python-gitlab/commit/d69ba0479a4537bbc7a53f342661c1984382f939))

This is useful in debugging and testing. As can easily print out the values from an instance in a
  more human-readable form.

- Add a stale workflow
  ([`2c036a9`](https://github.com/python-gitlab/python-gitlab/commit/2c036a992c9d7fdf6ccf0d3132d9b215c6d197f5))

Use the stale action to close issues and pull-requests with no activity.

Issues: It will mark them as stale after 60 days and then close

them once they have been stale for 15 days.

Pull-Requests: It will mark pull-requests as stale after 90 days and then close

https://github.com/actions/stale

Closes: #1649

- Add EncodedId string class to use to hold URL-encoded paths
  ([`a2e7c38`](https://github.com/python-gitlab/python-gitlab/commit/a2e7c383e10509b6eb0fa8760727036feb0807c8))

Add EncodedId string class. This class returns a URL-encoded string but ensures it will only
  URL-encode it once even if recursively called.

Also added some functional tests of 'lazy' objects to make sure they work.

- Add functional test of mergerequest.get()
  ([`a92b55b`](https://github.com/python-gitlab/python-gitlab/commit/a92b55b81eb3586e4144f9332796c94747bf9cfe))

Add a functional test of test mergerequest.get() and mergerequest.get(..., lazy=True)

Closes: #1425

- Add logging to `tests/functional/conftest.py`
  ([`a1ac9ae`](https://github.com/python-gitlab/python-gitlab/commit/a1ac9ae63828ca2012289817410d420da066d8df))

I have found trying to debug issues in the functional tests can be difficult. Especially when trying
  to figure out failures in the CI running on Github.

Add logging to `tests/functional/conftest.py` to have a better understanding of what is happening
  during a test run which is useful when trying to troubleshoot issues in the CI.

- Add temporary banner for v3
  ([`a349793`](https://github.com/python-gitlab/python-gitlab/commit/a349793307e3a975bb51f864b48e5e9825f70182))

- Fix functional test failure if config present
  ([`c9ed3dd`](https://github.com/python-gitlab/python-gitlab/commit/c9ed3ddc1253c828dc877dcd55000d818c297ee7))

Previously c8256a5933d745f70c7eea0a7d6230b51bac0fbc was done to fix this but it missed two other
  failures.

- Fix missing comma
  ([`7c59fac`](https://github.com/python-gitlab/python-gitlab/commit/7c59fac12fe69a1080cc227512e620ac5ae40b13))

There was a missing comma which meant the strings were concatenated instead of being two separate
  strings.

- Ignore intermediate coverage artifacts
  ([`110ae91`](https://github.com/python-gitlab/python-gitlab/commit/110ae9100b407356925ac2d2ffc65e0f0d50bd70))

- Replace usage of utils._url_encode() with utils.EncodedId()
  ([`b07eece`](https://github.com/python-gitlab/python-gitlab/commit/b07eece0a35dbc48076c9ec79f65f1e3fa17a872))

utils.EncodedId() has basically the same functionalityy of using utils._url_encode(). So remove
  utils._url_encode() as we don't need it.

- **dist**: Add docs *.md files to sdist
  ([`d9457d8`](https://github.com/python-gitlab/python-gitlab/commit/d9457d860ae7293ca218ab25e9501b0f796caa57))

build_sphinx to fail due to setup.cfg warning-is-error

- **docs**: Use admonitions consistently
  ([`55c67d1`](https://github.com/python-gitlab/python-gitlab/commit/55c67d1fdb81dcfdf8f398b3184fc59256af513d))

- **groups**: Use encoded_id for group path
  ([`868f243`](https://github.com/python-gitlab/python-gitlab/commit/868f2432cae80578d99db91b941332302dd31c89))

- **objects**: Use `self.encoded_id` where applicable
  ([`75758bf`](https://github.com/python-gitlab/python-gitlab/commit/75758bf26bca286ec57d5cef2808560c395ff7ec))

Updated a few remaining usages of `self.id` to use `self.encoded_id` as for the most part we
  shouldn't be using `self.id`

There are now only a few (4 lines of code) remaining uses of `self.id`, most of which seem that they
  should stay that way.

- **objects**: Use `self.encoded_id` where could be a string
  ([`c3c3a91`](https://github.com/python-gitlab/python-gitlab/commit/c3c3a914fa2787ae6a1368fe6550585ee252c901))

Updated a few remaining usages of `self.id` to use `self.encoded_id` where it could be a string
  value.

- **projects**: Fix typing for transfer method
  ([`0788fe6`](https://github.com/python-gitlab/python-gitlab/commit/0788fe677128d8c25db1cc107fef860a5a3c2a42))

Co-authored-by: John Villalovos <john@sodarock.com>

### Continuous Integration

- Don't fail CI if unable to upload the code coverage data
  ([`d5b3744`](https://github.com/python-gitlab/python-gitlab/commit/d5b3744c26c8c78f49e69da251cd53da70b180b3))

If a CI job can't upload coverage results to codecov.com it causes the CI to fail and code can't be
  merged.

### Documentation

- Update project access token API reference link
  ([`73ae955`](https://github.com/python-gitlab/python-gitlab/commit/73ae9559dc7f4fba5c80862f0f253959e60f7a0c))

- **cli**: Make examples more easily navigable by generating TOC
  ([`f33c523`](https://github.com/python-gitlab/python-gitlab/commit/f33c5230cb25c9a41e9f63c0846c1ecba7097ee7))

### Features

- Add support for Group Access Token API
  ([`c01b7c4`](https://github.com/python-gitlab/python-gitlab/commit/c01b7c494192c5462ec673848287ef2a5c9bd737))

See https://docs.gitlab.com/ee/api/group_access_tokens.html

- Add support for Groups API method `transfer()`
  ([`0007006`](https://github.com/python-gitlab/python-gitlab/commit/0007006c184c64128caa96b82dafa3db0ea1101f))

- **api**: Add `project.transfer()` and deprecate `transfer_project()`
  ([`259668a`](https://github.com/python-gitlab/python-gitlab/commit/259668ad8cb54348e4a41143a45f899a222d2d35))

- **api**: Return result from `SaveMixin.save()`
  ([`e6258a4`](https://github.com/python-gitlab/python-gitlab/commit/e6258a4193a0e8d0c3cf48de15b926bebfa289f3))

Return the new object data when calling `SaveMixin.save()`.

Also remove check for `None` value when calling `self.manager.update()` as that method only returns
  a dictionary.

Closes: #1081

### Testing

- **groups**: Enable group transfer tests
  ([`57bb67a`](https://github.com/python-gitlab/python-gitlab/commit/57bb67ae280cff8ac6e946cd3f3797574a574f4a))


## v3.0.0 (2022-01-05)

### Bug Fixes

- Handle situation where GitLab does not return values
  ([`cb824a4`](https://github.com/python-gitlab/python-gitlab/commit/cb824a49af9b0d155b89fe66a4cfebefe52beb7a))

If a query returns more than 10,000 records than the following values are NOT returned:
  x.total_pages x.total

Modify the code to allow no value to be set for these values. If there is not a value returned the
  functions will now return None.

Update unit test so no longer `xfail`

https://docs.gitlab.com/ee/user/gitlab_com/index.html#pagination-response-headers

Closes #1686

- Raise error if there is a 301/302 redirection
  ([`d56a434`](https://github.com/python-gitlab/python-gitlab/commit/d56a4345c1ae05823b553e386bfa393541117467))

Before we raised an error if there was a 301, 302 redirect but only from an http URL to an https
  URL. But we didn't raise an error for any other redirects.

This caused two problems:

1. PUT requests that are redirected get changed to GET requests which don't perform the desired
  action but raise no error. This is because the GET response succeeds but since it wasn't a PUT it
  doesn't update. See issue: https://github.com/python-gitlab/python-gitlab/issues/1432 2. POST
  requests that are redirected also got changed to GET requests. They also caused hard to debug
  tracebacks for the user. See issue: https://github.com/python-gitlab/python-gitlab/issues/1477

Correct this by always raising a RedirectError exception and improve the exception message to let
  them know what was redirected.

Closes: #1485

Closes: #1432

Closes: #1477

- Stop encoding '.' to '%2E'
  ([`702e41d`](https://github.com/python-gitlab/python-gitlab/commit/702e41dd0674e76b292d9ea4f559c86f0a99edfe))

Forcing the encoding of '.' to '%2E' causes issues. It also goes against the RFC:
  https://datatracker.ietf.org/doc/html/rfc3986.html#section-2.3

From the RFC: For consistency, percent-encoded octets in the ranges of ALPHA (%41-%5A and %61-%7A),
  DIGIT (%30-%39), hyphen (%2D), period (%2E), underscore (%5F), or tilde (%7E) should not be
  created by URI producers...

Closes #1006 Related #1356 Related #1561

BREAKING CHANGE: stop encoding '.' to '%2E'. This could potentially be a breaking change for users
  who have incorrectly configured GitLab servers which don't handle period '.' characters correctly.

- **api**: Delete invalid 'project-runner get' command
  ([#1628](https://github.com/python-gitlab/python-gitlab/pull/1628),
  [`905781b`](https://github.com/python-gitlab/python-gitlab/commit/905781bed2afa33634b27842a42a077a160cffb8))

* fix(api): delete 'group-runner get' and 'group-runner delete' commands

Co-authored-by: Léo GATELLIER <git@leogatellier.fr>

- **api**: Replace deprecated attribute in delete_in_bulk()
  ([#1536](https://github.com/python-gitlab/python-gitlab/pull/1536),
  [`c59fbdb`](https://github.com/python-gitlab/python-gitlab/commit/c59fbdb0e9311fa84190579769e3c5c6aeb07fe5))

BREAKING CHANGE: The deprecated `name_regex` attribute has been removed in favor of
  `name_regex_delete`. (see https://gitlab.com/gitlab-org/gitlab/-/commit/ce99813cf54)

- **build**: Do not include docs in wheel package
  ([`68a97ce`](https://github.com/python-gitlab/python-gitlab/commit/68a97ced521051afb093cf4fb6e8565d9f61f708))

- **build**: Do not package tests in wheel
  ([`969dccc`](https://github.com/python-gitlab/python-gitlab/commit/969dccc084e833331fcd26c2a12ddaf448575ab4))

- **objects**: Rename confusing `to_project_id` argument
  ([`ce4bc0d`](https://github.com/python-gitlab/python-gitlab/commit/ce4bc0daef355e2d877360c6e496c23856138872))

BREAKING CHANGE: rename confusing `to_project_id` argument in transfer_project to `project_id`
  (`--project-id` in CLI). This is used for the source project, not for the target namespace.

### Chores

- Add .env as a file that search tools should not ignore
  ([`c9318a9`](https://github.com/python-gitlab/python-gitlab/commit/c9318a9f73c532bee7ba81a41de1fb521ab25ced))

The `.env` file was not set as a file that should not be ignored by search tools. We want to have
  the search tools search any `.env` files.

- Add and document optional parameters for get MR
  ([`bfa3dbe`](https://github.com/python-gitlab/python-gitlab/commit/bfa3dbe516cfa8824b720ba4c52dd05054a855d7))

Add and document (some of the) optional parameters that can be done for a
  `project.merge_requests.get()`

Closes #1775

- Add get() methods for GetWithoutIdMixin based classes
  ([`d27c50a`](https://github.com/python-gitlab/python-gitlab/commit/d27c50ab9d55dd715a7bee5b0c61317f8565c8bf))

Add the get() methods for the GetWithoutIdMixin based classes.

Update the tests/meta/test_ensure_type_hints.py tests to check to ensure that the get methods are
  defined with the correct return type.

- Add initial pylint check
  ([`041091f`](https://github.com/python-gitlab/python-gitlab/commit/041091f37f9ab615e121d5aafa37bf23ef72ba13))

Initial pylint check is added. A LONG list of disabled checks is also added. In the future we should
  work through the list and resolve the errors or disable them on a more granular level.

- Add Python 3.11 testing
  ([`b5ec192`](https://github.com/python-gitlab/python-gitlab/commit/b5ec192157461f7feb326846d4323c633658b861))

Add a unit test for Python 3.11. This will use the latest version of Python 3.11 that is available
  from https://github.com/actions/python-versions/

At this time it is 3.11.0-alpha.2 but will move forward over time until the final 3.11 release and
  updates. So 3.11.0, 3.11.1, ... will be matched.

- Add running unit tests on windows/macos
  ([`ad5d60c`](https://github.com/python-gitlab/python-gitlab/commit/ad5d60c305857a8e8c06ba4f6db788bf918bb63f))

Add running the unit tests on windows-latest and macos-latest with Python 3.10.

- Add test case to show branch name with period works
  ([`ea97d7a`](https://github.com/python-gitlab/python-gitlab/commit/ea97d7a68dd92c6f43dd1f307d63b304137315c4))

Add a test case to show that a branch name with a period can be fetched with a `get()`

Closes: #1715

- Add type hints for gitlab/v4/objects/commits.py
  ([`dc096a2`](https://github.com/python-gitlab/python-gitlab/commit/dc096a26f72afcebdac380675749a6991aebcd7c))

- Add type-hints to gitlab/v4/objects/epics.py
  ([`d4adf8d`](https://github.com/python-gitlab/python-gitlab/commit/d4adf8dfd2879b982ac1314e89df76cb61f2dbf9))

- Add type-hints to gitlab/v4/objects/files.py
  ([`0c22bd9`](https://github.com/python-gitlab/python-gitlab/commit/0c22bd921bc74f48fddd0ff7d5e7525086264d54))

- Add type-hints to gitlab/v4/objects/geo_nodes.py
  ([`13243b7`](https://github.com/python-gitlab/python-gitlab/commit/13243b752fecc54ba8fc0967ba9a223b520f4f4b))

- Add type-hints to gitlab/v4/objects/groups.py
  ([`94dcb06`](https://github.com/python-gitlab/python-gitlab/commit/94dcb066ef3ff531778ef4efb97824f010b4993f))

* Add type-hints to gitlab/v4/objects/groups.py * Have share() function update object attributes. *
  Add 'get()' method so that type-checkers will understand that getting a group is of type Group.

- Add type-hints to gitlab/v4/objects/issues.py
  ([`93e39a2`](https://github.com/python-gitlab/python-gitlab/commit/93e39a2947c442fb91f5c80b34008ca1d27cdf71))

- Add type-hints to gitlab/v4/objects/jobs.py
  ([`e8884f2`](https://github.com/python-gitlab/python-gitlab/commit/e8884f21cee29a0ce4428ea2c4b893d1ab922525))

- Add type-hints to gitlab/v4/objects/labels.py
  ([`d04e557`](https://github.com/python-gitlab/python-gitlab/commit/d04e557fb09655a0433363843737e19d8e11c936))

- Add type-hints to gitlab/v4/objects/merge_request_approvals.py
  ([`cf3a99a`](https://github.com/python-gitlab/python-gitlab/commit/cf3a99a0c4cf3dc51e946bf29dc44c21b3be9dac))

- Add type-hints to gitlab/v4/objects/merge_requests.py
  ([`f9c0ad9`](https://github.com/python-gitlab/python-gitlab/commit/f9c0ad939154375b9940bf41a7e47caab4b79a12))

* Add type-hints to gitlab/v4/objects/merge_requests.py * Add return value to
  cancel_merge_when_pipeline_succeeds() function as GitLab docs show it returns a value. * Add
  return value to approve() function as GitLab docs show it returns a value. * Add 'get()' method so
  that type-checkers will understand that getting a project merge request is of type
  ProjectMergeRequest.

- Add type-hints to gitlab/v4/objects/milestones.py
  ([`8b6078f`](https://github.com/python-gitlab/python-gitlab/commit/8b6078faf02fcf9d966e2b7d1d42722173534519))

- Add type-hints to gitlab/v4/objects/pipelines.py
  ([`cb3ad6c`](https://github.com/python-gitlab/python-gitlab/commit/cb3ad6ce4e2b4a8a3fd0e60031550484b83ed517))

- Add type-hints to gitlab/v4/objects/repositories.py
  ([`00d7b20`](https://github.com/python-gitlab/python-gitlab/commit/00d7b202efb3a2234cf6c5ce09a48397a40b8388))

- Add type-hints to gitlab/v4/objects/services.py
  ([`8da0b75`](https://github.com/python-gitlab/python-gitlab/commit/8da0b758c589f608a6ae4eeb74b3f306609ba36d))

- Add type-hints to gitlab/v4/objects/sidekiq.py
  ([`a91a303`](https://github.com/python-gitlab/python-gitlab/commit/a91a303e2217498293cf709b5e05930d41c95992))

- Add type-hints to gitlab/v4/objects/snippets.py
  ([`f256d4f`](https://github.com/python-gitlab/python-gitlab/commit/f256d4f6c675576189a72b4b00addce440559747))

- Add type-hints to gitlab/v4/objects/users.py
  ([`88988e3`](https://github.com/python-gitlab/python-gitlab/commit/88988e3059ebadd3d1752db60c2d15b7e60e7c46))

Adding type-hints to gitlab/v4/objects/users.py

- Add type-hints to multiple files in gitlab/v4/objects/
  ([`8b75a77`](https://github.com/python-gitlab/python-gitlab/commit/8b75a7712dd1665d4b3eabb0c4594e80ab5e5308))

Add and/or check type-hints for the following files gitlab.v4.objects.access_requests
  gitlab.v4.objects.applications gitlab.v4.objects.broadcast_messages gitlab.v4.objects.deployments
  gitlab.v4.objects.keys gitlab.v4.objects.merge_trains gitlab.v4.objects.namespaces
  gitlab.v4.objects.pages gitlab.v4.objects.personal_access_tokens
  gitlab.v4.objects.project_access_tokens gitlab.v4.objects.tags gitlab.v4.objects.templates
  gitlab.v4.objects.triggers

Add a 'get' method with the correct type for Managers derived from GetMixin.

- Add type-hints to setup.py and check with mypy
  ([`06184da`](https://github.com/python-gitlab/python-gitlab/commit/06184daafd5010ba40bb39a0768540b7e98bd171))

- Attempt to be more informative for missing attributes
  ([`1839c9e`](https://github.com/python-gitlab/python-gitlab/commit/1839c9e7989163a5cc9a201241942b7faca6e214))

A commonly reported issue from users on Gitter is that they get an AttributeError for an attribute
  that should be present. This is often caused due to the fact that they used the `list()` method to
  retrieve the object and objects retrieved this way often only have a subset of the full data.

Add more details in the AttributeError message that explains the situation to users. This will
  hopefully allow them to resolve the issue.

Update the FAQ in the docs to add a section discussing the issue.

Closes #1138

- Attempt to fix flaky functional test
  ([`487b9a8`](https://github.com/python-gitlab/python-gitlab/commit/487b9a875a18bb3b4e0d49237bb7129d2c6dba2f))

Add an additional check to attempt to solve the flakiness of the
  test_merge_request_should_remove_source_branch() test.

- Check setup.py with mypy
  ([`77cb7a8`](https://github.com/python-gitlab/python-gitlab/commit/77cb7a8f64f25191d84528cc61e1d246296645c9))

Prior commit 06184daafd5010ba40bb39a0768540b7e98bd171 fixed the type-hints for setup.py. But missed
  removing 'setup' from the exclude list in pyproject.toml for mypy checks.

Remove 'setup' from the exclude list in pyproject.toml from mypy checks.

- Clean up install docs
  ([`a5d8b7f`](https://github.com/python-gitlab/python-gitlab/commit/a5d8b7f2a9cf019c82bef1a166d2dc24f93e1992))

- Convert to using type-annotations for managers
  ([`d8de4dc`](https://github.com/python-gitlab/python-gitlab/commit/d8de4dc373dc608be6cf6ba14a2acc7efd3fa7a7))

Convert our manager usage to be done via type annotations.

Now to define a manager to be used in a RESTObject subclass can simply do: class
  ExampleClass(CRUDMixin, RESTObject): my_manager: MyManager

Any type-annotation that annotates it to be of type *Manager (with the exception of RESTManager)
  will cause the manager to be created on the object.

- Correct test_groups.py test
  ([`9c878a4`](https://github.com/python-gitlab/python-gitlab/commit/9c878a4090ddb9c0ef63d06b57eb0e4926276e2f))

The test was checking twice if the same group3 was not in the returned list. Should have been
  checking for group3 and group4.

Also added a test that only skipped one group and checked that the group was not in the returned
  list and a non-skipped group was in the list.

- Create a 'tests/meta/' directory and put test_mro.py in it
  ([`94feb8a`](https://github.com/python-gitlab/python-gitlab/commit/94feb8a5534d43a464b717275846faa75783427e))

The 'test_mro.py' file is not really a unit test but more of a 'meta' check on the validity of the
  code base.

- Enable 'warn_redundant_casts' for mypy
  ([`f40e9b3`](https://github.com/python-gitlab/python-gitlab/commit/f40e9b3517607c95f2ce2735e3b08ffde8d61e5a))

Enable 'warn_redundant_casts'for mypy and resolve one issue.

- Enable mypy for tests/meta/*
  ([`ba7707f`](https://github.com/python-gitlab/python-gitlab/commit/ba7707f6161463260710bd2b109b172fd63472a1))

- Enable subset of the 'mypy --strict' options that work
  ([`a86d049`](https://github.com/python-gitlab/python-gitlab/commit/a86d0490cadfc2f9fe5490879a1258cf264d5202))

Enable the subset of the 'mypy --strict' options that work with no changes to the code.

- Enforce type-hints on most files in gitlab/v4/objects/
  ([`7828ba2`](https://github.com/python-gitlab/python-gitlab/commit/7828ba2fd13c833c118a673bac09b215587ba33b))

* Add type-hints to some of the files in gitlab/v4/objects/ * Fix issues detected when adding
  type-hints * Changed mypy exclusion to explicitly list the 13 files that have not yet had
  type-hints added.

- Ensure get() methods have correct type-hints
  ([`46773a8`](https://github.com/python-gitlab/python-gitlab/commit/46773a82565cef231dc3391c12f296ac307cb95c))

Fix classes which don't have correct 'get()' methods for classes derived from GetMixin.

Add a unit test which verifies that classes have the correct return type in their 'get()' method.

- Ensure reset_gitlab() succeeds
  ([`0aa0b27`](https://github.com/python-gitlab/python-gitlab/commit/0aa0b272a90b11951f900b290a8154408eace1de))

Ensure reset_gitlab() succeeds by waiting to make sure everything has been deleted as expected. If
  the timeout is exceeded fail the test.

Not using `wait_for_sidekiq` as it didn't work. During testing I didn't see any sidekiq processes as
  being busy even though not everything was deleted.

- Fix functional test failure if config present
  ([`c8256a5`](https://github.com/python-gitlab/python-gitlab/commit/c8256a5933d745f70c7eea0a7d6230b51bac0fbc))

Fix functional test failure if config present and configured with token.

Closes: #1791

- Fix issue with adding type-hints to 'manager' attribute
  ([`9a451a8`](https://github.com/python-gitlab/python-gitlab/commit/9a451a892d37e0857af5c82c31a96d68ac161738))

When attempting to add type-hints to the the 'manager' attribute into a RESTObject derived class it
  would break things.

This was because our auto-manager creation code would automatically add the specified annotated
  manager to the 'manager' attribute. This breaks things.

Now check in our auto-manager creation if our attribute is called 'manager'. If so we ignore it.

- Fix pylint error "expression-not-assigned"
  ([`a90eb23`](https://github.com/python-gitlab/python-gitlab/commit/a90eb23cb4903ba25d382c37ce1c0839642ba8fd))

Fix pylint error "expression-not-assigned" and remove check from the disabled list.

And I personally think it is much more readable now and is less lines of code.

- Fix renovate setup for gitlab docker image
  ([`49af15b`](https://github.com/python-gitlab/python-gitlab/commit/49af15b3febda5af877da06c3d8c989fbeede00a))

- Fix type-check issue shown by new requests-types
  ([`0ee9aa4`](https://github.com/python-gitlab/python-gitlab/commit/0ee9aa4117b1e0620ba3cade10ccb94944754071))

types-requests==2.25.9 changed a type-hint. Update code to handle this change.

- Fix typo in MR documentation
  ([`2254222`](https://github.com/python-gitlab/python-gitlab/commit/2254222094d218b31a6151049c7a43e19c593a97))

- Fix unit test if config file exists locally
  ([`c80b3b7`](https://github.com/python-gitlab/python-gitlab/commit/c80b3b75aff53ae228ec05ddf1c1e61d91762846))

Closes #1764

- Generate artifacts for the docs build in the CI
  ([`85b43ae`](https://github.com/python-gitlab/python-gitlab/commit/85b43ae4a96b72e2f29e36a0aca5321ed78f28d2))

When building the docs store the created documentation as an artifact so that it can be viewed.

This will create a html-docs.zip file which can be downloaded containing the contents of the
  `build/sphinx/html/` directory. It can be downloaded, extracted, and then viewed. This can be
  useful in reviewing changes to the documentation.

See https://github.com/actions/upload-artifact for more information on how this works.

- Github workflow: cancel prior running jobs on new push
  ([`fd81569`](https://github.com/python-gitlab/python-gitlab/commit/fd8156991556706f776c508c373224b54ef4e14f))

If new new push is done to a pull-request, then cancel any already running github workflow jobs in
  order to conserve resources.

- Have renovate upgrade black version
  ([#1700](https://github.com/python-gitlab/python-gitlab/pull/1700),
  [`21228cd`](https://github.com/python-gitlab/python-gitlab/commit/21228cd14fe18897485728a01c3d7103bff7f822))

renovate is not upgrading the `black` package. There is an open issue[1] about this.

Also change .commitlintrc.json to allow 200 character footer lines in the commit message. Otherwise
  would be forced to split the URL across multiple lines making it un-clickable :(

Use suggested work-arounds from:
  https://github.com/renovatebot/renovate/issues/7167#issuecomment-904106838
  https://github.com/scop/bash-completion/blob/e7497f6ee8232065ec11450a52a1f244f345e2c6/renovate.json#L34-L38

[1] https://github.com/renovatebot/renovate/issues/7167

- Improve type-hinting for managers
  ([`c9b5d3b`](https://github.com/python-gitlab/python-gitlab/commit/c9b5d3bac8f7c1f779dd57653f718dd0fac4db4b))

The 'managers' are dynamically created. This unfortunately means that we don't have any type-hints
  for them and so editors which understand type-hints won't know that they are valid attributes.

* Add the type-hints for the managers we define. * Add a unit test that makes sure that the
  type-hints and the '_managers' attribute are kept in sync with each other. * Add unit test that
  makes sure specified managers in '_managers' have a name ending in 'Managers' to keep with current
  convention. * Make RESTObject._managers always present with a default value of None. * Fix a
  type-issue revealed now that mypy knows what the type is

- Remove '# type: ignore' for new mypy version
  ([`34a5f22`](https://github.com/python-gitlab/python-gitlab/commit/34a5f22c81590349645ce7ba46d4153d6de07d8c))

mypy 0.920 now understands the type of 'http.client.HTTPConnection.debuglevel' so we remove the
  'type: ignore' comment to make mypy pass

- Remove duplicate/no-op tests from meta/test_ensure_type_hints
  ([`a2f59f4`](https://github.com/python-gitlab/python-gitlab/commit/a2f59f4e3146b8871a9a1d66ee84295b44321ecb))

Before we were generating 725 tests for the meta/test_ensure_type_hints.py tests. Which isn't a huge
  concern as it was fairly fast. But when we had a failure we would usually get two failures for
  each problem as the same test was being run multiple times.

Changed it so that: 1. Don't add tests that are not for *Manager classes 2. Use a set so that we
  don't have duplicate tests.

After doing that our generated test count in meta/test_ensure_type_hints.py went from 725 to 178
  tests.

Additionally removed the parsing of `pyproject.toml` to generate files to ignore as we have finished
  adding type-hints to all files in gitlab/v4/objects/. This also means we no longer use the toml
  library so remove installation of `types-toml`.

To determine the test count the following command was run: $ tox -e py39 -- -k
  test_ensure_type_hints

- Remove pytest-console-scripts specific config
  ([`e80dcb1`](https://github.com/python-gitlab/python-gitlab/commit/e80dcb1dc09851230b00f8eb63e0c78fda060392))

Remove the pytest-console-scripts specific config from the global '[pytest]' config section.

Use the command line option `--script-launch-mode=subprocess`

Closes #1713

- Rename `master` branch to `main`
  ([`545f8ed`](https://github.com/python-gitlab/python-gitlab/commit/545f8ed24124837bf4e55aa34e185270a4b7aeff))

BREAKING CHANGE: As of python-gitlab 3.0.0, the default branch for development has changed from
  `master` to `main`.

- Run pre-commit on changes to the config file
  ([`5f10b3b`](https://github.com/python-gitlab/python-gitlab/commit/5f10b3b96d83033805757d72269ad0a771d797d4))

If .pre-commit-config.yaml or .github/workflows/pre_commit.yml are updated then run pre-commit.

- Set pre-commit mypy args to empty list
  ([`b67a6ad`](https://github.com/python-gitlab/python-gitlab/commit/b67a6ad1f81dce4670f9820750b411facc01a048))

https://github.com/pre-commit/mirrors-mypy/blob/master/.pre-commit-hooks.yaml

Sets some default args which seem to be interfering with things. Plus we set all of our args in the
  `pyproject.toml` file.

- Skip a functional test if not using >= py3.9
  ([`ac9b595`](https://github.com/python-gitlab/python-gitlab/commit/ac9b59591a954504d4e6e9b576b7a43fcb2ddaaa))

One of the tests requires Python 3.9 or higher to run. Mark the test to be skipped if running Python
  less than 3.9.

- Update version in docker-compose.yml
  ([`79321aa`](https://github.com/python-gitlab/python-gitlab/commit/79321aa0e33f0f4bd2ebcdad47769a1a6e81cba8))

When running with docker-compose on Ubuntu 20.04 I got the error:

$ docker-compose up ERROR: The Compose file './docker-compose.yml' is invalid because:

networks.gitlab-network value Additional properties are not allowed ('name' was unexpected)

Changing the version in the docker-compose.yml file fro '3' to '3.5' resolved the issue.

- Use constants from gitlab.const module
  ([`6b8067e`](https://github.com/python-gitlab/python-gitlab/commit/6b8067e668b6a37a19e07d84e9a0d2d2a99b4d31))

Have code use constants from the gitlab.const module instead of from the top-level gitlab module.

- **api**: Temporarily remove topic delete endpoint
  ([`e3035a7`](https://github.com/python-gitlab/python-gitlab/commit/e3035a799a484f8d6c460f57e57d4b59217cd6de))

It is not yet available upstream.

- **ci**: Add workflow to lock old issues
  ([`a7d64fe`](https://github.com/python-gitlab/python-gitlab/commit/a7d64fe5696984aae0c9d6d6b1b51877cc4634cf))

- **ci**: Enable renovate for pre-commit
  ([`1ac4329`](https://github.com/python-gitlab/python-gitlab/commit/1ac432900d0f87bb83c77aa62757f8f819296e3e))

- **ci**: Wait for all coverage jobs before posting comment
  ([`c7fdad4`](https://github.com/python-gitlab/python-gitlab/commit/c7fdad42f68927d79e0d1963ade3324370b9d0e2))

- **deps**: Update dependency argcomplete to v2
  ([`c6d7e9a`](https://github.com/python-gitlab/python-gitlab/commit/c6d7e9aaddda2f39262b695bb98ea4d90575fcce))

- **deps**: Update dependency black to v21
  ([`5bca87c`](https://github.com/python-gitlab/python-gitlab/commit/5bca87c1e3499eab9b9a694c1f5d0d474ffaca39))

- **deps**: Update dependency black to v21.12b0
  ([`ab841b8`](https://github.com/python-gitlab/python-gitlab/commit/ab841b8c63183ca20b866818ab2f930a5643ba5f))

- **deps**: Update dependency flake8 to v4
  ([`79785f0`](https://github.com/python-gitlab/python-gitlab/commit/79785f0bee2ef6cc9872f816a78c13583dfb77ab))

- **deps**: Update dependency isort to v5.10.0
  ([`ae62468`](https://github.com/python-gitlab/python-gitlab/commit/ae6246807004b84d3b2acd609a70ce220a0ecc21))

- **deps**: Update dependency isort to v5.10.1
  ([`2012975`](https://github.com/python-gitlab/python-gitlab/commit/2012975ea96a1d3924d6be24aaf92a025e6ab45b))

- **deps**: Update dependency mypy to v0.920
  ([`a519b2f`](https://github.com/python-gitlab/python-gitlab/commit/a519b2ffe9c8a4bb42d6add5117caecc4bf6ec66))

- **deps**: Update dependency mypy to v0.930
  ([`ccf8190`](https://github.com/python-gitlab/python-gitlab/commit/ccf819049bf2a9e3be0a0af2a727ab53fc016488))

- **deps**: Update dependency requests to v2.27.0
  ([`f8c3d00`](https://github.com/python-gitlab/python-gitlab/commit/f8c3d009db3aca004bbd64894a795ee01378cd26))

- **deps**: Update dependency sphinx to v4
  ([`73745f7`](https://github.com/python-gitlab/python-gitlab/commit/73745f73e5180dd21f450ac4d8cbcca19930e549))

- **deps**: Update dependency sphinx to v4.3.0
  ([`57283fc`](https://github.com/python-gitlab/python-gitlab/commit/57283fca5890f567626235baaf91ca62ae44ff34))

- **deps**: Update dependency sphinx to v4.3.1
  ([`93a3893`](https://github.com/python-gitlab/python-gitlab/commit/93a3893977d4e3a3e1916a94293e66373b1458fb))

- **deps**: Update dependency sphinx to v4.3.2
  ([`2210e56`](https://github.com/python-gitlab/python-gitlab/commit/2210e56da57a9e82e6fd2977453b2de4af14bb6f))

- **deps**: Update dependency types-pyyaml to v5.4.10
  ([`bdb6cb9`](https://github.com/python-gitlab/python-gitlab/commit/bdb6cb932774890752569ebbc86509e011728ae6))

- **deps**: Update dependency types-pyyaml to v6
  ([`0b53c0a`](https://github.com/python-gitlab/python-gitlab/commit/0b53c0a260ab2ec2c5ddb12ca08bfd21a24f7a69))

- **deps**: Update dependency types-pyyaml to v6.0.1
  ([`a544cd5`](https://github.com/python-gitlab/python-gitlab/commit/a544cd576c127ba1986536c9ea32daf2a42649d4))

- **deps**: Update dependency types-requests to v2.25.12
  ([`205ad5f`](https://github.com/python-gitlab/python-gitlab/commit/205ad5fe0934478eb28c014303caa178f5b8c7ec))

- **deps**: Update dependency types-requests to v2.25.9
  ([`e3912ca`](https://github.com/python-gitlab/python-gitlab/commit/e3912ca69c2213c01cd72728fd669724926fd57a))

- **deps**: Update dependency types-requests to v2.26.0
  ([`7528d84`](https://github.com/python-gitlab/python-gitlab/commit/7528d84762f03b668e9d63a18a712d7224943c12))

- **deps**: Update dependency types-requests to v2.26.2
  ([`ac7e329`](https://github.com/python-gitlab/python-gitlab/commit/ac7e32989a1e7b217b448f57bf2943ff56531983))

- **deps**: Update dependency types-setuptools to v57.4.3
  ([`ec2c68b`](https://github.com/python-gitlab/python-gitlab/commit/ec2c68b0b41ac42a2bca61262a917a969cbcbd09))

- **deps**: Update pre-commit hook alessandrojcm/commitlint-pre-commit-hook to v6
  ([`fb9110b`](https://github.com/python-gitlab/python-gitlab/commit/fb9110b1849cea8fa5eddf56f1dbfc1c75f10ad9))

- **deps**: Update pre-commit hook psf/black to v21
  ([`b86e819`](https://github.com/python-gitlab/python-gitlab/commit/b86e819e6395a84755aaf42334b17567a1bed5fd))

- **deps**: Update pre-commit hook pycqa/flake8 to v4
  ([`98a5592`](https://github.com/python-gitlab/python-gitlab/commit/98a5592ae7246bf927beb3300211007c0fadba2f))

- **deps**: Update pre-commit hook pycqa/isort to v5.10.1
  ([`8ac4f4a`](https://github.com/python-gitlab/python-gitlab/commit/8ac4f4a2ba901de1ad809e4fc2fe787e37703a50))

- **deps**: Update python docker tag to v3.10
  ([`b3d6d91`](https://github.com/python-gitlab/python-gitlab/commit/b3d6d91fed4e5b8424e1af9cadb2af5b6cd8162f))

- **deps**: Update typing dependencies
  ([`1f95613`](https://github.com/python-gitlab/python-gitlab/commit/1f9561314a880048227b6f3ecb2ed59e60200d19))

- **deps**: Update typing dependencies
  ([`8d4c953`](https://github.com/python-gitlab/python-gitlab/commit/8d4c95358c9e61c1cfb89562252498093f56d269))

- **deps**: Update typing dependencies
  ([`4170dbe`](https://github.com/python-gitlab/python-gitlab/commit/4170dbe00112378a523b0fdf3208e8fa4bc5ef00))

- **deps**: Update typing dependencies
  ([`4eb8ec8`](https://github.com/python-gitlab/python-gitlab/commit/4eb8ec874083adcf86a1781c7866f9dd014f6d27))

- **deps**: Upgrade gitlab-ce to 14.3.2-ce.0
  ([`5a1678f`](https://github.com/python-gitlab/python-gitlab/commit/5a1678f43184bd459132102cc13cf8426fe0449d))

- **deps**: Upgrade mypy pre-commit hook
  ([`e19e4d7`](https://github.com/python-gitlab/python-gitlab/commit/e19e4d7cdf9cd04359cd3e95036675c81f4e1dc5))

- **docs**: Link to main, not master
  ([`af0cb4d`](https://github.com/python-gitlab/python-gitlab/commit/af0cb4d18b8bfbc0624ea2771d73544dc1b24b54))

- **docs**: Load autodoc-typehints module
  ([`bd366ab`](https://github.com/python-gitlab/python-gitlab/commit/bd366ab9e4b552fb29f7a41564cc180a659bba2f))

- **docs**: Use builtin autodoc hints
  ([`5e9c943`](https://github.com/python-gitlab/python-gitlab/commit/5e9c94313f6714a159993cefb488aca3326e3e66))

- **objects**: Remove non-existing trigger ownership method
  ([`8dc7f40`](https://github.com/python-gitlab/python-gitlab/commit/8dc7f40044ce8c478769f25a87c5ceb1aa76b595))

- **tests**: Apply review suggestions
  ([`381c748`](https://github.com/python-gitlab/python-gitlab/commit/381c748415396e0fe54bb1f41a3303bab89aa065))

### Documentation

- Add links to the GitLab API docs
  ([`e3b5d27`](https://github.com/python-gitlab/python-gitlab/commit/e3b5d27bde3e104e520d976795cbcb1ae792fb05))

Add links to the GitLab API docs for merge_requests.py as it contains code which spans two different
  API documentation pages.

- Consolidate changelogs and remove v3 API docs
  ([`90da8ba`](https://github.com/python-gitlab/python-gitlab/commit/90da8ba0342ebd42b8ec3d5b0d4c5fbb5e701117))

- Correct documentation for updating discussion note
  ([`ee66f4a`](https://github.com/python-gitlab/python-gitlab/commit/ee66f4a777490a47ad915a3014729a9720bf909b))

Closes #1777

- Correct documented return type
  ([`acabf63`](https://github.com/python-gitlab/python-gitlab/commit/acabf63c821745bd7e43b7cd3d799547b65e9ed0))

repository_archive() returns 'bytes' not 'str'

https://docs.gitlab.com/ee/api/repositories.html#get-file-archive

Fixes: #1584

- Fix a few typos
  ([`7ea4ddc`](https://github.com/python-gitlab/python-gitlab/commit/7ea4ddc4248e314998fd27eea17c6667f5214d1d))

There are small typos in: - docs/gl_objects/deploy_tokens.rst - gitlab/base.py - gitlab/mixins.py -
  gitlab/v4/objects/features.py - gitlab/v4/objects/groups.py - gitlab/v4/objects/packages.py -
  gitlab/v4/objects/projects.py - gitlab/v4/objects/sidekiq.py - gitlab/v4/objects/todos.py

Fixes: - Should read `treatment` rather than `reatment`. - Should read `transferred` rather than
  `transfered`. - Should read `registered` rather than `registred`. - Should read `occurred` rather
  than `occured`. - Should read `overridden` rather than `overriden`. - Should read `marked` rather
  than `maked`. - Should read `instantiate` rather than `instanciate`. - Should read `function`
  rather than `fonction`.

- Fix API delete key example
  ([`b31bb05`](https://github.com/python-gitlab/python-gitlab/commit/b31bb05c868793e4f0cb4573dad6bf9ca01ed5d9))

- Only use type annotations for documentation
  ([`b7dde0d`](https://github.com/python-gitlab/python-gitlab/commit/b7dde0d7aac8dbaa4f47f9bfb03fdcf1f0b01c41))

- Rename documentation files to match names of code files
  ([`ee3f865`](https://github.com/python-gitlab/python-gitlab/commit/ee3f8659d48a727da5cd9fb633a060a9231392ff))

Rename the merge request related documentation files to match the code files. This will make it
  easier to find the documentation quickly.

Rename: `docs/gl_objects/mrs.rst -> `docs/gl_objects/merge_requests.rst`
  `docs/gl_objects/mr_approvals.rst -> `docs/gl_objects/merge_request_approvals.rst`

- Switch to Furo and refresh introduction pages
  ([`ee6b024`](https://github.com/python-gitlab/python-gitlab/commit/ee6b024347bf8a178be1a0998216f2a24c940cee))

- Update docs to use gitlab.const for constants
  ([`b3b0b5f`](https://github.com/python-gitlab/python-gitlab/commit/b3b0b5f1da5b9da9bf44eac33856ed6eadf37dd6))

Update the docs to use gitlab.const to access constants.

- Use annotations for return types
  ([`79e785e`](https://github.com/python-gitlab/python-gitlab/commit/79e785e765f4219fe6001ef7044235b82c5e7754))

- **api**: Clarify job token usage with auth()
  ([`3f423ef`](https://github.com/python-gitlab/python-gitlab/commit/3f423efab385b3eb1afe59ad12c2da7eaaa11d76))

See issue #1620

- **api**: Document the update method for project variables
  ([`7992911`](https://github.com/python-gitlab/python-gitlab/commit/7992911896c62f23f25742d171001f30af514a9a))

- **pipelines**: Document take_ownership method
  ([`69461f6`](https://github.com/python-gitlab/python-gitlab/commit/69461f6982e2a85dcbf95a0b884abd3f4050c1c7))

- **project**: Remove redundant encoding parameter
  ([`fed613f`](https://github.com/python-gitlab/python-gitlab/commit/fed613f41a298e79a975b7f99203e07e0f45e62c))

### Features

- Add delete on package_file object
  ([`124667b`](https://github.com/python-gitlab/python-gitlab/commit/124667bf16b1843ae52e65a3cc9b8d9235ff467e))

- Add support for `projects.groups.list()`
  ([`68ff595`](https://github.com/python-gitlab/python-gitlab/commit/68ff595967a5745b369a93d9d18fef48b65ebedb))

Add support for `projects.groups.list()` endpoint.

Closes #1717

- Add support for `squash_option` in Projects
  ([`a246ce8`](https://github.com/python-gitlab/python-gitlab/commit/a246ce8a942b33c5b23ac075b94237da09013fa2))

There is an optional `squash_option` parameter which can be used when creating Projects and
  UserProjects.

Closes #1744

- Allow global retry_transient_errors setup
  ([`3b1d3a4`](https://github.com/python-gitlab/python-gitlab/commit/3b1d3a41da7e7228f3a465d06902db8af564153e))

`retry_transient_errors` can now be set through the Gitlab instance and global configuration

Documentation for API usage has been updated and missing tests have been added.

- Default to gitlab.com if no URL given
  ([`8236281`](https://github.com/python-gitlab/python-gitlab/commit/823628153ec813c4490e749e502a47716425c0f1))

BREAKING CHANGE: python-gitlab will now default to gitlab.com if no URL is given

- Remove support for Python 3.6, require 3.7 or higher
  ([`414009d`](https://github.com/python-gitlab/python-gitlab/commit/414009daebe19a8ae6c36f050dffc690dff40e91))

Python 3.6 is End-of-Life (EOL) as of 2021-12 as stated in https://www.python.org/dev/peps/pep-0494/

By dropping support for Python 3.6 and requiring Python 3.7 or higher it allows python-gitlab to
  take advantage of new features in Python 3.7, which are documented at:
  https://docs.python.org/3/whatsnew/3.7.html

Some of these new features that may be useful to python-gitlab are: * PEP 563, postponed evaluation
  of type annotations. * dataclasses: PEP 557 – Data Classes * importlib.resources * PEP 562,
  customization of access to module attributes. * PEP 560, core support for typing module and
  generic types. * PEP 565, improved DeprecationWarning handling

BREAKING CHANGE: As of python-gitlab 3.0.0, Python 3.6 is no longer supported. Python 3.7 or higher
  is required.

- **api**: Add merge request approval state
  ([`f41b093`](https://github.com/python-gitlab/python-gitlab/commit/f41b0937aec5f4a5efba44155cc2db77c7124e5e))

Add support for merge request approval state

- **api**: Add merge trains
  ([`fd73a73`](https://github.com/python-gitlab/python-gitlab/commit/fd73a738b429be0a2642d5b777d5e56a4c928787))

Add support for merge trains

- **api**: Add project label promotion
  ([`6d7c88a`](https://github.com/python-gitlab/python-gitlab/commit/6d7c88a1fe401d271a34df80943634652195b140))

Adds a mixin that allows the /promote endpoint to be called.

Signed-off-by: Raimund Hook <raimund.hook@exfo.com>

- **api**: Add project milestone promotion
  ([`f068520`](https://github.com/python-gitlab/python-gitlab/commit/f0685209f88d1199873c1f27d27f478706908fd3))

Adds promotion to Project Milestones

Signed-off-by: Raimund Hook <raimund.hook@exfo.com>

- **api**: Add support for epic notes
  ([`7f4edb5`](https://github.com/python-gitlab/python-gitlab/commit/7f4edb53e9413f401c859701d8c3bac4a40706af))

Added support for notes on group epics

Signed-off-by: Raimund Hook <raimund.hook@exfo.com>

- **api**: Add support for Topics API
  ([`e7559bf`](https://github.com/python-gitlab/python-gitlab/commit/e7559bfa2ee265d7d664d7a18770b0a3e80cf999))

- **api**: Support file format for repository archive
  ([`83dcabf`](https://github.com/python-gitlab/python-gitlab/commit/83dcabf3b04af63318c981317778f74857279909))

- **build**: Officially support and test python 3.10
  ([`c042ddc`](https://github.com/python-gitlab/python-gitlab/commit/c042ddc79ea872fc8eb8fe4e32f4107a14ffed2d))

- **cli**: Allow options from args and environment variables
  ([`ca58008`](https://github.com/python-gitlab/python-gitlab/commit/ca58008607385338aaedd14a58adc347fa1a41a0))

BREAKING-CHANGE: The gitlab CLI will now accept CLI arguments

and environment variables for its global options in addition to configuration file options. This may
  change behavior for some workflows such as running inside GitLab CI and with certain environment
  variables configured.

- **cli**: Do not require config file to run CLI
  ([`92a893b`](https://github.com/python-gitlab/python-gitlab/commit/92a893b8e230718436582dcad96175685425b1df))

BREAKING CHANGE: A config file is no longer needed to run the CLI. python-gitlab will default to
  https://gitlab.com with no authentication if there is no config file provided. python-gitlab will
  now also only look for configuration in the provided PYTHON_GITLAB_CFG path, instead of merging it
  with user- and system-wide config files. If the environment variable is defined and the file
  cannot be opened, python-gitlab will now explicitly fail.

- **docker**: Remove custom entrypoint from image
  ([`80754a1`](https://github.com/python-gitlab/python-gitlab/commit/80754a17f66ef4cd8469ff0857e0fc592c89796d))

This is no longer needed as all of the configuration is handled by the CLI and can be passed as
  arguments.

- **objects**: List starred projects of a user
  ([`47a5606`](https://github.com/python-gitlab/python-gitlab/commit/47a56061421fc8048ee5cceaf47ac031c92aa1da))

- **objects**: Support Create and Revoke personal access token API
  ([`e19314d`](https://github.com/python-gitlab/python-gitlab/commit/e19314dcc481b045ba7a12dd76abedc08dbdf032))

- **objects**: Support delete package files API
  ([`4518046`](https://github.com/python-gitlab/python-gitlab/commit/45180466a408cd51c3ea4fead577eb0e1f3fe7f8))

### Refactoring

- Deprecate accessing constants from top-level namespace
  ([`c0aa0e1`](https://github.com/python-gitlab/python-gitlab/commit/c0aa0e1c9f7d7914e3062fe6503da870508b27cf))

We are planning on adding enumerated constants into gitlab/const.py, but if we do that than they
  will end up being added to the top-level gitlab namespace. We really want to get users to start
  using `gitlab.const.` to access the constant values in the future.

Add the currently defined constants to a list that should not change. Use a module level __getattr__
  function so that we can deprecate access to the top-level constants.

Add a unit test which verifies we generate a warning when accessing the top-level constants.

- Use f-strings for string formatting
  ([`7925c90`](https://github.com/python-gitlab/python-gitlab/commit/7925c902d15f20abaecdb07af213f79dad91355b))

- Use new-style formatting for named placeholders
  ([`c0d8810`](https://github.com/python-gitlab/python-gitlab/commit/c0d881064f7c90f6a510db483990776ceb17b9bd))

- **objects**: Remove deprecated branch protect methods
  ([`9656a16`](https://github.com/python-gitlab/python-gitlab/commit/9656a16f9f34a1aeb8ea0015564bad68ffb39c26))

BREAKING CHANGE: remove deprecated branch protect methods in favor of the more complete protected
  branches API.

- **objects**: Remove deprecated constants defined in objects
  ([`3f320af`](https://github.com/python-gitlab/python-gitlab/commit/3f320af347df05bba9c4d0d3bdb714f7b0f7b9bf))

BREAKING CHANGE: remove deprecated constants defined in gitlab.v4.objects, and use only gitlab.const
  module

- **objects**: Remove deprecated members.all() method
  ([`4d7b848`](https://github.com/python-gitlab/python-gitlab/commit/4d7b848e2a826c58e91970a1d65ed7d7c3e07166))

BREAKING CHANGE: remove deprecated members.all() method in favor of members_all.list()

- **objects**: Remove deprecated pipelines() method
  ([`c4f5ec6`](https://github.com/python-gitlab/python-gitlab/commit/c4f5ec6c615e9f83d533a7be0ec19314233e1ea0))

BREAKING CHANGE: remove deprecated pipelines() methods in favor of pipelines.list()

- **objects**: Remove deprecated project.issuesstatistics
  ([`ca7777e`](https://github.com/python-gitlab/python-gitlab/commit/ca7777e0dbb82b5d0ff466835a94c99e381abb7c))

BREAKING CHANGE: remove deprecated project.issuesstatistics in favor of project.issues_statistics

- **objects**: Remove deprecated tag release API
  ([`2b8a94a`](https://github.com/python-gitlab/python-gitlab/commit/2b8a94a77ba903ae97228e7ffa3cc2bf6ceb19ba))

BREAKING CHANGE: remove deprecated tag release API. This was removed in GitLab 14.0

### Testing

- Drop httmock dependency in test_gitlab.py
  ([`c764bee`](https://github.com/python-gitlab/python-gitlab/commit/c764bee191438fc4aa2e52d14717c136760d2f3f))

- Reproduce missing pagination headers in tests
  ([`501f9a1`](https://github.com/python-gitlab/python-gitlab/commit/501f9a1588db90e6d2c235723ba62c09a669b5d2))

- **api**: Fix current user mail count in newer gitlab
  ([`af33aff`](https://github.com/python-gitlab/python-gitlab/commit/af33affa4888fa83c31557ae99d7bbd877e9a605))

- **build**: Add smoke tests for sdist & wheel package
  ([`b8a47ba`](https://github.com/python-gitlab/python-gitlab/commit/b8a47bae3342400a411fb9bf4bef3c15ba91c98e))

- **cli**: Improve basic CLI coverage
  ([`6b892e3`](https://github.com/python-gitlab/python-gitlab/commit/6b892e3dcb18d0f43da6020b08fd4ba891da3670))


## v2.10.1 (2021-08-28)

### Bug Fixes

- **deps**: Upgrade requests to 2.25.0 (see CVE-2021-33503)
  ([`ce995b2`](https://github.com/python-gitlab/python-gitlab/commit/ce995b256423a0c5619e2a6c0d88e917aad315ba))

- **mixins**: Improve deprecation warning
  ([`57e0187`](https://github.com/python-gitlab/python-gitlab/commit/57e018772492a8522b37d438d722c643594cf580))

Also note what should be changed

### Chores

- Define root dir in mypy, not tox
  ([`7a64e67`](https://github.com/python-gitlab/python-gitlab/commit/7a64e67c8ea09c5e4e041cc9d0807f340d0e1310))

- Fix mypy pre-commit hook
  ([`bd50df6`](https://github.com/python-gitlab/python-gitlab/commit/bd50df6b963af39b70ea2db50fb2f30b55ddc196))

- **deps**: Group typing requirements with mypy additional_dependencies
  ([`38597e7`](https://github.com/python-gitlab/python-gitlab/commit/38597e71a7dd12751b028f9451587f781f95c18f))

- **deps**: Update codecov/codecov-action action to v2
  ([`44f4fb7`](https://github.com/python-gitlab/python-gitlab/commit/44f4fb78bb0b5a18a4703b68a9657796bf852711))

- **deps**: Update dependency isort to v5.9.3
  ([`ab46e31`](https://github.com/python-gitlab/python-gitlab/commit/ab46e31f66c36d882cdae0b02e702b37e5a6ff4e))

- **deps**: Update dependency types-pyyaml to v5.4.7
  ([`ec8be67`](https://github.com/python-gitlab/python-gitlab/commit/ec8be67ddd37302f31b07185cb4778093e549588))

- **deps**: Update dependency types-pyyaml to v5.4.8
  ([`2ae1dd7`](https://github.com/python-gitlab/python-gitlab/commit/2ae1dd7d91f4f90123d9dd8ea92c61b38383e31c))

- **deps**: Update dependency types-requests to v2.25.1
  ([`a2d133a`](https://github.com/python-gitlab/python-gitlab/commit/a2d133a995d3349c9b0919dd03abaf08b025289e))

- **deps**: Update dependency types-requests to v2.25.2
  ([`4782678`](https://github.com/python-gitlab/python-gitlab/commit/47826789a5f885a87ae139b8c4d8da9d2dacf713))

- **deps**: Update precommit hook pycqa/isort to v5.9.3
  ([`e1954f3`](https://github.com/python-gitlab/python-gitlab/commit/e1954f355b989007d13a528f1e49e9410256b5ce))

- **deps**: Update typing dependencies
  ([`34fc210`](https://github.com/python-gitlab/python-gitlab/commit/34fc21058240da564875f746692b3fb4c3f7c4c8))

- **deps**: Update wagoid/commitlint-github-action action to v4
  ([`ae97196`](https://github.com/python-gitlab/python-gitlab/commit/ae97196ce8f277082ac28fcd39a9d11e464e6da9))

### Documentation

- **mergequests**: Gl.mergequests.list documentation was missleading
  ([`5b5a7bc`](https://github.com/python-gitlab/python-gitlab/commit/5b5a7bcc70a4ddd621cbd59e134e7004ad2d9ab9))


## v2.10.0 (2021-07-28)

### Bug Fixes

- **api**: Do not require Release name for creation
  ([`98cd03b`](https://github.com/python-gitlab/python-gitlab/commit/98cd03b7a3085356b5f0f4fcdb7dc729b682f481))

Stop requiring a `name` attribute for creating a Release, since a release name has not been required
  since GitLab 12.5.

### Chores

- **deps**: Update dependency isort to v5.9.2
  ([`d5dcf1c`](https://github.com/python-gitlab/python-gitlab/commit/d5dcf1cb7e703ec732e12e41d2971726f27a4bdc))

- **deps**: Update dependency requests to v2.26.0
  ([`d3ea203`](https://github.com/python-gitlab/python-gitlab/commit/d3ea203dc0e4677b7f36c0f80e6a7a0438ea6385))

- **deps**: Update precommit hook pycqa/isort to v5.9.2
  ([`521cddd`](https://github.com/python-gitlab/python-gitlab/commit/521cdddc5260ef2ba6330822ec96efc90e1c03e3))

### Documentation

- Add example for mr.merge_ref
  ([`b30b8ac`](https://github.com/python-gitlab/python-gitlab/commit/b30b8ac27d98ed0a45a13775645d77b76e828f95))

Signed-off-by: Matej Focko <mfocko@redhat.com>

- **project**: Add example on getting a single project using name with namespace
  ([`ef16a97`](https://github.com/python-gitlab/python-gitlab/commit/ef16a979031a77155907f4160e4f5e159d839737))

- **readme**: Move contributing docs to CONTRIBUTING.rst
  ([`edf49a3`](https://github.com/python-gitlab/python-gitlab/commit/edf49a3d855b1ce4e2bd8a7038b7444ff0ab5fdc))

Move the Contributing section of README.rst to CONTRIBUTING.rst, so it is recognized by GitHub and
  shown when new contributors make pull requests.

### Features

- **api**: Add `name_regex_keep` attribute in `delete_in_bulk()`
  ([`e49ff3f`](https://github.com/python-gitlab/python-gitlab/commit/e49ff3f868cbab7ff81115f458840b5f6d27d96c))

- **api**: Add merge_ref for merge requests
  ([`1e24ab2`](https://github.com/python-gitlab/python-gitlab/commit/1e24ab247cc783ae240e94f6cb379fef1e743a52))

Support merge_ref on merge requests that returns commit of attempted merge of the MR.

Signed-off-by: Matej Focko <mfocko@redhat.com>

### Testing

- **functional**: Add mr.merge_ref tests
  ([`a9924f4`](https://github.com/python-gitlab/python-gitlab/commit/a9924f48800f57fa8036e3ebdf89d1e04b9bf1a1))

- Add test for using merge_ref on non-merged MR - Add test for using merge_ref on MR with conflicts

Signed-off-by: Matej Focko <mfocko@redhat.com>


## v2.9.0 (2021-06-28)

### Chores

- Add new required type packages for mypy
  ([`a7371e1`](https://github.com/python-gitlab/python-gitlab/commit/a7371e19520325a725813e328004daecf9259dd2))

New version of mypy flagged errors for missing types. Install the recommended type-* packages that
  resolve the issues.

- Add type-hints to gitlab/v4/objects/projects.py
  ([`872dd6d`](https://github.com/python-gitlab/python-gitlab/commit/872dd6defd8c299e997f0f269f55926ce51bd13e))

Adding type-hints to gitlab/v4/objects/projects.py

- Skip EE test case in functional tests
  ([`953f207`](https://github.com/python-gitlab/python-gitlab/commit/953f207466c53c28a877f2a88da9160acef40643))

- **deps**: Update dependency isort to v5.9.1
  ([`0479dba`](https://github.com/python-gitlab/python-gitlab/commit/0479dba8a26d2588d9616dbeed351b0256f4bf87))

- **deps**: Update dependency mypy to v0.902
  ([`19c9736`](https://github.com/python-gitlab/python-gitlab/commit/19c9736de06d032569020697f15ea9d3e2b66120))

- **deps**: Update dependency mypy to v0.910
  ([`02a56f3`](https://github.com/python-gitlab/python-gitlab/commit/02a56f397880b3939b8e737483ac6f95f809ac9c))

- **deps**: Update dependency types-pyyaml to v0.1.8
  ([`e566767`](https://github.com/python-gitlab/python-gitlab/commit/e56676730d3407efdf4255b3ca7ee13b7c36eb53))

- **deps**: Update dependency types-pyyaml to v0.1.9
  ([`1f5b3c0`](https://github.com/python-gitlab/python-gitlab/commit/1f5b3c03b2ae451dfe518ed65ec2bec4e80c09d1))

- **deps**: Update dependency types-pyyaml to v5
  ([`5c22634`](https://github.com/python-gitlab/python-gitlab/commit/5c226343097427b3f45a404db5b78d61143074fb))

- **deps**: Update dependency types-requests to v0.1.11
  ([`6ba629c`](https://github.com/python-gitlab/python-gitlab/commit/6ba629c71a4cf8ced7060580a6e6643738bc4186))

- **deps**: Update dependency types-requests to v0.1.12
  ([`f84c2a8`](https://github.com/python-gitlab/python-gitlab/commit/f84c2a885069813ce80c18542fcfa30cc0d9b644))

- **deps**: Update dependency types-requests to v0.1.13
  ([`c3ddae2`](https://github.com/python-gitlab/python-gitlab/commit/c3ddae239aee6694a09c864158e355675567f3d2))

- **deps**: Update dependency types-requests to v2
  ([`a81a926`](https://github.com/python-gitlab/python-gitlab/commit/a81a926a0979e3272abfb2dc40d2f130d3a0ba5a))

- **deps**: Update precommit hook pycqa/isort to v5.9.1
  ([`c57ffe3`](https://github.com/python-gitlab/python-gitlab/commit/c57ffe3958c1475c8c79bb86fc4b101d82350d75))

### Documentation

- Make Gitlab class usable for intersphinx
  ([`8753add`](https://github.com/python-gitlab/python-gitlab/commit/8753add72061ea01c508a42d16a27388b1d92677))

- **release**: Add update example
  ([`6254a5f`](https://github.com/python-gitlab/python-gitlab/commit/6254a5ff6f43bd7d0a26dead304465adf1bd0886))

- **tags**: Remove deprecated functions
  ([`1b1a827`](https://github.com/python-gitlab/python-gitlab/commit/1b1a827dd40b489fdacdf0a15b0e17a1a117df40))

### Features

- **api**: Add group hooks
  ([`4a7e9b8`](https://github.com/python-gitlab/python-gitlab/commit/4a7e9b86aa348b72925bce3af1e5d988b8ce3439))

- **api**: Add MR pipeline manager in favor of pipelines() method
  ([`954357c`](https://github.com/python-gitlab/python-gitlab/commit/954357c49963ef51945c81c41fd4345002f9fb98))

- **api**: Add support for creating/editing reviewers in project merge requests
  ([`676d1f6`](https://github.com/python-gitlab/python-gitlab/commit/676d1f6565617a28ee84eae20e945f23aaf3d86f))

- **api**: Remove responsibility for API inconsistencies for MR reviewers
  ([`3d985ee`](https://github.com/python-gitlab/python-gitlab/commit/3d985ee8cdd5d27585678f8fbb3eb549818a78eb))

- **release**: Allow to update release
  ([`b4c4787`](https://github.com/python-gitlab/python-gitlab/commit/b4c4787af54d9db6c1f9e61154be5db9d46de3dd))

Release API now supports PUT.

### Testing

- **releases**: Add unit-tests for release update
  ([`5b68a5a`](https://github.com/python-gitlab/python-gitlab/commit/5b68a5a73eb90316504d74d7e8065816f6510996))

- **releases**: Integration for release PUT
  ([`13bf61d`](https://github.com/python-gitlab/python-gitlab/commit/13bf61d07e84cd719931234c3ccbb9977c8f6416))


## v2.8.0 (2021-06-10)

### Bug Fixes

- Add a check to ensure the MRO is correct
  ([`565d548`](https://github.com/python-gitlab/python-gitlab/commit/565d5488b779de19a720d7a904c6fc14c394a4b9))

Add a check to ensure the MRO (Method Resolution Order) is correct for classes in gitlab.v4.objects
  when doing type-checking.

An example of an incorrect definition: class ProjectPipeline(RESTObject, RefreshMixin,
  ObjectDeleteMixin): ^^^^^^^^^^ This should be at the end.

Correct way would be: class ProjectPipeline(RefreshMixin, ObjectDeleteMixin, RESTObject): Correctly
  at the end ^^^^^^^^^^

Also fix classes which have the issue.

- Catch invalid type used to initialize RESTObject
  ([`c7bcc25`](https://github.com/python-gitlab/python-gitlab/commit/c7bcc25a361f9df440f9c972672e5eec3b057625))

Sometimes we have errors where we don't get a dictionary passed to RESTObject.__init__() method.
  This breaks things but in confusing ways.

Check in the __init__() method and raise an exception if it occurs.

- Change mr.merge() to use 'post_data'
  ([`cb6a3c6`](https://github.com/python-gitlab/python-gitlab/commit/cb6a3c672b9b162f7320c532410713576fbd1cdc))

MR https://github.com/python-gitlab/python-gitlab/pull/1121 changed mr.merge() to use 'query_data'.
  This appears to have been wrong.

From the Gitlab docs they state it should be sent in a payload body
  https://docs.gitlab.com/ee/api/README.html#request-payload since mr.merge() is a PUT request.

> Request Payload

> API Requests can use parameters sent as query strings or as a > payload body. GET requests usually
  send a query string, while PUT > or POST requests usually send the payload body

Fixes: #1452

Related to: #1120

- Ensure kwargs are passed appropriately for ObjectDeleteMixin
  ([`4e690c2`](https://github.com/python-gitlab/python-gitlab/commit/4e690c256fc091ddf1649e48dbbf0b40cc5e6b95))

- Functional project service test
  ([#1500](https://github.com/python-gitlab/python-gitlab/pull/1500),
  [`093db9d`](https://github.com/python-gitlab/python-gitlab/commit/093db9d129e0a113995501755ab57a04e461c745))

chore: fix functional project service test

- Iids not working as a list in projects.issues.list()
  ([`45f806c`](https://github.com/python-gitlab/python-gitlab/commit/45f806c7a7354592befe58a76b7e33a6d5d0fe6e))

Set the 'iids' values as type ListAttribute so it will pass the list as a comma-separated string,
  instead of a list.

Add a functional test.

Closes: #1407

- **cli**: Add missing list filter for jobs
  ([`b3d1c26`](https://github.com/python-gitlab/python-gitlab/commit/b3d1c267cbe6885ee41b3c688d82890bb2e27316))

- **cli**: Fix parsing CLI objects to classnames
  ([`4252070`](https://github.com/python-gitlab/python-gitlab/commit/42520705a97289ac895a6b110d34d6c115e45500))

- **objects**: Add missing group attributes
  ([`d20ff4f`](https://github.com/python-gitlab/python-gitlab/commit/d20ff4ff7427519c8abccf53e3213e8929905441))

- **objects**: Allow lists for filters for in all objects
  ([`603a351`](https://github.com/python-gitlab/python-gitlab/commit/603a351c71196a7f516367fbf90519f9452f3c55))

- **objects**: Return server data in cancel/retry methods
  ([`9fed061`](https://github.com/python-gitlab/python-gitlab/commit/9fed06116bfe5df79e6ac5be86ae61017f9a2f57))

### Chores

- Add a functional test for issue #1120
  ([`7d66115`](https://github.com/python-gitlab/python-gitlab/commit/7d66115573c6c029ce6aa00e244f8bdfbb907e33))

Going to switch to putting parameters from in the query string to having them in the 'data' body
  section. Add a functional test to make sure that we don't break anything.

https://github.com/python-gitlab/python-gitlab/issues/1120

- Add a merge_request() pytest fixture and use it
  ([`8be2838`](https://github.com/python-gitlab/python-gitlab/commit/8be2838a9ee3e2440d066e2c4b77cb9b55fc3da2))

Added a pytest.fixture for merge_request(). Use this fixture in
  tools/functional/api/test_merge_requests.py

- Add an isort tox environment and run isort in CI
  ([`dda646e`](https://github.com/python-gitlab/python-gitlab/commit/dda646e8f2ecb733e37e6cffec331b783b64714e))

* Add an isort tox environment * Run the isort tox environment using --check in the Github CI

https://pycqa.github.io/isort/

- Add functional test mr.merge() with long commit message
  ([`cd5993c`](https://github.com/python-gitlab/python-gitlab/commit/cd5993c9d638c2a10879d7e3ac36db06df867e54))

Functional test to show that https://github.com/python-gitlab/python-gitlab/issues/1452 is fixed.

Added a functional test to ensure that we can use large commit message (10_000+ bytes) in mr.merge()

Related to: #1452

- Add missing linters to pre-commit and pin versions
  ([`85bbd1a`](https://github.com/python-gitlab/python-gitlab/commit/85bbd1a5db5eff8a8cea63b2b192aae66030423d))

- Add missing optional create parameter for approval_rules
  ([`06a6001`](https://github.com/python-gitlab/python-gitlab/commit/06a600136bdb33bdbd84233303652afb36fb8a1b))

Add missing optional create parameter ('protected_branch_ids') to the project approvalrules.

https://docs.gitlab.com/ee/api/merge_request_approvals.html#create-project-level-rule

- Add type-hints to gitlab/v4/cli.py
  ([`2673af0`](https://github.com/python-gitlab/python-gitlab/commit/2673af0c09a7c5669d8f62c3cc42f684a9693a0f))

* Add type-hints to gitlab/v4/cli.py * Add required type-hints to other files based on adding
  type-hints to gitlab/v4/cli.py

- Apply suggestions
  ([`fe7d19d`](https://github.com/python-gitlab/python-gitlab/commit/fe7d19de5aeba675dcb06621cf36ab4169391158))

- Apply typing suggestions
  ([`a11623b`](https://github.com/python-gitlab/python-gitlab/commit/a11623b1aa6998e6520f3975f0f3f2613ceee5fb))

Co-authored-by: John Villalovos <john@sodarock.com>

- Clean up tox, pre-commit and requirements
  ([`237b97c`](https://github.com/python-gitlab/python-gitlab/commit/237b97ceb0614821e59ea041f43a9806b65cdf8c))

- Correct a type-hint
  ([`046607c`](https://github.com/python-gitlab/python-gitlab/commit/046607cf7fd95c3d25f5af9383fdf10a5bba42c1))

- Fix import ordering using isort
  ([`f3afd34`](https://github.com/python-gitlab/python-gitlab/commit/f3afd34260d681bbeec974b67012b90d407b7014))

Fix the import ordering using isort.

https://pycqa.github.io/isort/

- Have black run at the top-level
  ([`429d6c5`](https://github.com/python-gitlab/python-gitlab/commit/429d6c55602f17431201de17e63cdb2c68ac5d73))

This will ensure everything is formatted with black, including setup.py.

- Have flake8 check the entire project
  ([`ab343ef`](https://github.com/python-gitlab/python-gitlab/commit/ab343ef6da708746aa08a972b461a5e51d898f8b))

Have flake8 run at the top-level of the projects instead of just the gitlab directory.

- Make certain dotfiles searchable by ripgrep
  ([`e4ce078`](https://github.com/python-gitlab/python-gitlab/commit/e4ce078580f7eac8cf1c56122e99be28e3830247))

By explicitly NOT excluding the dotfiles we care about to the .gitignore file we make those files
  searchable by tools like ripgrep.

By default dotfiles are ignored by ripgrep and other search tools (not grep)

- Make Get.*Mixin._optional_get_attrs always present
  ([`3c1a0b3`](https://github.com/python-gitlab/python-gitlab/commit/3c1a0b3ba1f529fab38829c9d355561fd36f4f5d))

Always create GetMixin/GetWithoutIdMixin._optional_get_attrs attribute with a default value of
  tuple()

This way we don't need to use hasattr() and we will know the type of the attribute.

- Move 'gitlab/tests/' dir to 'tests/unit/'
  ([`1ac0722`](https://github.com/python-gitlab/python-gitlab/commit/1ac0722bc086b18c070132a0eb53747bbdf2ce0a))

Move the 'gitlab/tests/' directory to 'tests/unit/' so we have all the tests located under the
  'tests/' directory.

- Mypy: Disallow untyped definitions
  ([`6aef2da`](https://github.com/python-gitlab/python-gitlab/commit/6aef2dadf715e601ae9c302be0ad9958345a97f2))

Be more strict and don't allow untyped definitions on the files we check.

Also this adds type-hints for two of the decorators so that now functions/methods decorated by them
  will have their types be revealed correctly.

- Remove commented-out print
  ([`0357c37`](https://github.com/python-gitlab/python-gitlab/commit/0357c37fb40fb6aef175177fab98d0eadc26b667))

- Rename 'tools/functional/' to 'tests/functional/'
  ([`502715d`](https://github.com/python-gitlab/python-gitlab/commit/502715d99e02105c39b2c5cf0e7457b3256eba0d))

Rename the 'tools/functional/' directory to 'tests/functional/'

This makes more sense as these are functional tests and not tools.

This was dicussed in: https://github.com/python-gitlab/python-gitlab/discussions/1468

- Simplify functional tests
  ([`df9b5f9`](https://github.com/python-gitlab/python-gitlab/commit/df9b5f9226f704a603a7e49c78bc4543b412f898))

Add a helper function to have less code duplication in the functional testing.

- Sync create and update attributes for Projects
  ([`0044bd2`](https://github.com/python-gitlab/python-gitlab/commit/0044bd253d86800a7ea8ef0a9a07e965a65cc6a5))

Sync the create attributes with: https://docs.gitlab.com/ee/api/projects.html#create-project

Sync the update attributes with documentation at:
  https://docs.gitlab.com/ee/api/projects.html#edit-project

As a note the ordering of the attributes was done to match the ordering of the attributes in the
  documentation.

Closes: #1497

- Use built-in function issubclass() instead of getmro()
  ([`81f6386`](https://github.com/python-gitlab/python-gitlab/commit/81f63866593a0486b03a4383d87ef7bc01f4e45f))

Code was using inspect.getmro() to replicate the functionality of the built-in function issubclass()

Switch to using issubclass()

- **ci**: Automate releases
  ([`0ef497e`](https://github.com/python-gitlab/python-gitlab/commit/0ef497e458f98acee36529e8bda2b28b3310de69))

- **ci**: Ignore .python-version from pyenv
  ([`149953d`](https://github.com/python-gitlab/python-gitlab/commit/149953dc32c28fe413c9f3a0066575caeab12bc8))

- **ci**: Ignore debug and type_checking in coverage
  ([`885b608`](https://github.com/python-gitlab/python-gitlab/commit/885b608194a55bd60ef2a2ad180c5caa8f15f8d2))

- **ci**: Use admin PAT for release workflow
  ([`d175d41`](https://github.com/python-gitlab/python-gitlab/commit/d175d416d5d94f4806f4262e1f11cfee99fb0135))

- **deps**: Update dependency docker-compose to v1.29.2
  ([`fc241e1`](https://github.com/python-gitlab/python-gitlab/commit/fc241e1ffa995417a969354e37d8fefc21bb4621))

- **deps**: Update gitlab/gitlab-ce docker tag to v13.11.2-ce.0
  ([`434d15d`](https://github.com/python-gitlab/python-gitlab/commit/434d15d1295187d1970ebef01f4c8a44a33afa31))

- **deps**: Update gitlab/gitlab-ce docker tag to v13.11.3-ce.0
  ([`f0b52d8`](https://github.com/python-gitlab/python-gitlab/commit/f0b52d829db900e98ab93883b20e6bd8062089c6))

- **deps**: Update gitlab/gitlab-ce docker tag to v13.11.4-ce.0
  ([`4223269`](https://github.com/python-gitlab/python-gitlab/commit/4223269608c2e58b837684d20973e02eb70e04c9))

- **deps**: Update precommit hook alessandrojcm/commitlint-pre-commit-hook to v5
  ([`9ff349d`](https://github.com/python-gitlab/python-gitlab/commit/9ff349d21ed40283d60692af5d19d86ed7e72958))

- **docs**: Fix import order for readthedocs build
  ([`c3de1fb`](https://github.com/python-gitlab/python-gitlab/commit/c3de1fb8ec17f5f704a19df4a56a668570e6fe0a))

### Code Style

- Clean up test run config
  ([`dfa40c1`](https://github.com/python-gitlab/python-gitlab/commit/dfa40c1ef85992e85c1160587037e56778ab49c0))

### Documentation

- Fail on warnings during sphinx build
  ([`cbd4d52`](https://github.com/python-gitlab/python-gitlab/commit/cbd4d52b11150594ec29b1ce52348c1086a778c8))

This is useful when docs aren't included in the toctree and don't show up on RTD.

- Fix typo in http_delete docstring
  ([`5226f09`](https://github.com/python-gitlab/python-gitlab/commit/5226f095c39985d04c34e7703d60814e74be96f8))

- **api**: Add behavior in local attributes when updating objects
  ([`38f65e8`](https://github.com/python-gitlab/python-gitlab/commit/38f65e8e9994f58bdc74fe2e0e9b971fc3edf723))

### Features

- Add code owner approval as attribute
  ([`fdc46ba`](https://github.com/python-gitlab/python-gitlab/commit/fdc46baca447e042d3b0a4542970f9758c62e7b7))

The python API was missing the field code_owner_approval_required as implemented in the GitLab REST
  API.

- Add feature to get inherited member for project/group
  ([`e444b39`](https://github.com/python-gitlab/python-gitlab/commit/e444b39f9423b4a4c85cdb199afbad987df026f1))

- Add keys endpoint
  ([`a81525a`](https://github.com/python-gitlab/python-gitlab/commit/a81525a2377aaed797af0706b00be7f5d8616d22))

- Add support for lists of integers to ListAttribute
  ([`115938b`](https://github.com/python-gitlab/python-gitlab/commit/115938b3e5adf9a2fb5ecbfb34d9c92bf788035e))

Previously ListAttribute only support lists of integers. Now be more flexible and support lists of
  items which can be coerced into strings, for example integers.

This will help us fix issue #1407 by using ListAttribute for the 'iids' field.

- Indicate that we are a typed package
  ([`e4421ca`](https://github.com/python-gitlab/python-gitlab/commit/e4421caafeeb0236df19fe7b9233300727e1933b))

By adding the file: py.typed it indicates that python-gitlab is a typed package and contains
  type-hints.

https://www.python.org/dev/peps/pep-0561/

- **api**: Add deployment mergerequests interface
  ([`fbbc0d4`](https://github.com/python-gitlab/python-gitlab/commit/fbbc0d400015d7366952a66e4401215adff709f0))

- **objects**: Add pipeline test report support
  ([`ee9f96e`](https://github.com/python-gitlab/python-gitlab/commit/ee9f96e61ab5da0ecf469c21cccaafc89130a896))

- **objects**: Add support for billable members
  ([`fb0b083`](https://github.com/python-gitlab/python-gitlab/commit/fb0b083a0e536a6abab25c9ad377770cc4290fe9))

- **objects**: Add support for descendant groups API
  ([`1b70580`](https://github.com/python-gitlab/python-gitlab/commit/1b70580020825adf2d1f8c37803bc4655a97be41))

- **objects**: Add support for generic packages API
  ([`79d88bd`](https://github.com/python-gitlab/python-gitlab/commit/79d88bde9e5e6c33029e4a9f26c97404e6a7a874))

- **objects**: Add support for Group wikis
  ([#1484](https://github.com/python-gitlab/python-gitlab/pull/1484),
  [`74f5e62`](https://github.com/python-gitlab/python-gitlab/commit/74f5e62ef5bfffc7ba21494d05dbead60b59ecf0))

feat(objects): add support for Group wikis

- **objects**: Support all issues statistics endpoints
  ([`f731707`](https://github.com/python-gitlab/python-gitlab/commit/f731707f076264ebea65afc814e4aca798970953))

### Testing

- **api**: Fix issues test
  ([`8e5b0de`](https://github.com/python-gitlab/python-gitlab/commit/8e5b0de7d9b1631aac4e9ac03a286dfe80675040))

Was incorrectly using the issue 'id' vs 'iid'.

- **cli**: Add more real class scenarios
  ([`8cf5031`](https://github.com/python-gitlab/python-gitlab/commit/8cf5031a2caf2f39ce920c5f80316cc774ba7a36))

- **cli**: Replace assignment expression
  ([`11ae11b`](https://github.com/python-gitlab/python-gitlab/commit/11ae11bfa5f9fcb903689805f8d35b4d62ab0c90))

This is a feature added in 3.8, removing it allows for the test to run with lower python versions.

- **functional**: Add test for skip_groups list filter
  ([`a014774`](https://github.com/python-gitlab/python-gitlab/commit/a014774a6a2523b73601a1930c44ac259d03a50e))

- **functional**: Explicitly remove deploy tokens on reset
  ([`19a55d8`](https://github.com/python-gitlab/python-gitlab/commit/19a55d80762417311dcebde3f998f5ebc7e78264))

Deploy tokens would remain in the instance if the respective project or group was deleted without
  explicitly revoking the deploy tokens first.

- **functional**: Force delete users on reset
  ([`8f81456`](https://github.com/python-gitlab/python-gitlab/commit/8f814563beb601715930ed3b0f89c3871e6e2f33))

Timing issues between requesting group deletion and GitLab enacting that deletion resulted in errors
  while attempting to delete a user which was the sole owner of said group (see: test_groups). Pass
  the 'hard_delete' parameter to ensure user deletion.

- **functional**: Optionally keep containers running post-tests
  ([`4c475ab`](https://github.com/python-gitlab/python-gitlab/commit/4c475abe30c36217da920477f3748e26f3395365))

Additionally updates token creation to make use of `first_or_create()`, to avoid errors from the
  script caused by GitLab constraints preventing duplicate tokens with the same value.

- **functional**: Start tracking functional test coverage
  ([`f875786`](https://github.com/python-gitlab/python-gitlab/commit/f875786ce338b329421f772b181e7183f0fcb333))


## v2.7.1 (2021-04-26)

### Bug Fixes

- **files**: Do not url-encode file paths twice
  ([`8e25cec`](https://github.com/python-gitlab/python-gitlab/commit/8e25cecce3c0a19884a8d231ee1a672b80e94398))


## v2.7.0 (2021-04-25)

### Bug Fixes

- Argument type was not a tuple as expected
  ([`062f8f6`](https://github.com/python-gitlab/python-gitlab/commit/062f8f6a917abc037714129691a845c16b070ff6))

While adding type-hints mypy flagged this as an issue. The third argument to register_custom_action
  is supposed to be a tuple. It was being passed as a string rather than a tuple of strings.

- Better real life token lookup example
  ([`9ef8311`](https://github.com/python-gitlab/python-gitlab/commit/9ef83118efde3d0f35d73812ce8398be2c18ebff))

- Checking if RESTManager._from_parent_attrs is set
  ([`8224b40`](https://github.com/python-gitlab/python-gitlab/commit/8224b4066e84720d7efed3b7891c47af73cc57ca))

Prior to commit 3727cbd21fc40b312573ca8da56e0f6cf9577d08 RESTManager._from_parent_attrs did not
  exist unless it was explicitly set. But commit 3727cbd21fc40b312573ca8da56e0f6cf9577d08 set it to
  a default value of {}.

So the checks using hasattr() were no longer valid.

Update the checks to check if RESTManager._from_parent_attrs has a value.

- Correct ProjectFile.decode() documentation
  ([`b180baf`](https://github.com/python-gitlab/python-gitlab/commit/b180bafdf282cd97e8f7b6767599bc42d5470bfa))

ProjectFile.decode() returns 'bytes' and not 'str'.

Update the method's doc-string and add a type-hint.

ProjectFile.decode() returns the result of a call to base64.b64decode()

The docs for that function state it returns 'bytes':
  https://docs.python.org/3/library/base64.html#base64.b64decode

Fixes: #1403

- Correct some type-hints in gitlab/mixins.py
  ([`8bd3124`](https://github.com/python-gitlab/python-gitlab/commit/8bd312404cf647674baea792547705ef1948043d))

Commit baea7215bbbe07c06b2ca0f97a1d3d482668d887 introduced type-hints for gitlab/mixins.py.

After starting to add type-hints to gitlab/v4/objects/users.py discovered a few errors.

Main error was using '=' instead of ':'. For example: _parent = Optional[...] should be _parent:
  Optional[...]

Resolved those issues.

- Extend wait timeout for test_delete_user()
  ([`19fde8e`](https://github.com/python-gitlab/python-gitlab/commit/19fde8ed0e794d33471056e2c07539cde70a8699))

Have been seeing intermittent failures of the test_delete_user() functional test. Have made the
  following changes to hopefully resolve the issue and if it still fails to know better why the
  failure occurred.

* Extend the wait timeout for test_delete_user() from 30 to 60 tries of 0.5 seconds each.

* Modify wait_for_sidekiq() to return True if sidekiq process terminated. Return False if the
  timeout expired.

* Modify wait_for_sidekiq() to loop through all processes instead of assuming there is only one
  process. If all processes are not busy then return.

* Modify wait_for_sidekiq() to sleep at least once before checking for processes being busy.

* Check for True being returned in test_delete_user() call to wait_for_sidekiq()

- Handle tags like debian/2%2.6-21 as identifiers
  ([`b4dac5c`](https://github.com/python-gitlab/python-gitlab/commit/b4dac5ce33843cf52badeb9faf0f7f52f20a9a6a))

Git refnames are relatively free-form and can contain all sort for special characters, not just `/`
  and `#`, see http://git-scm.com/docs/git-check-ref-format

In particular, Debian's DEP-14 standard for storing packaging in git repositories mandates the use
  of the `%` character in tags in some cases like `debian/2%2.6-21`.

Unfortunately python-gitlab currently only escapes `/` to `%2F` and in some cases `#` to `%23`. This
  means that when using the commit API to retrieve information about the `debian/2%2.6-21` tag only
  the slash is escaped before being inserted in the URL path and the `%` is left untouched,
  resulting in something like `/api/v4/projects/123/repository/commits/debian%2F2%2.6-21`. When
  urllib3 seees that it detects the invalid `%` escape and then urlencodes the whole string,
  resulting in `/api/v4/projects/123/repository/commits/debian%252F2%252.6-21`, where the original
  `/` got escaped twice and produced `%252F`.

To avoid the issue, fully urlencode identifiers and parameters to avoid the urllib3 auto-escaping in
  all cases.

Signed-off-by: Emanuele Aina <emanuele.aina@collabora.com>

- Handling config value in _get_values_from_helper
  ([`9dfb4cd`](https://github.com/python-gitlab/python-gitlab/commit/9dfb4cd97e6eb5bbfc29935cbb190b70b739cf9f))

- Honor parameter value passed
  ([`c2f8f0e`](https://github.com/python-gitlab/python-gitlab/commit/c2f8f0e7db9529e1f1f32d790a67d1e20d2fe052))

Gitlab allows setting the defaults for MR to delete the source. Also the inline help of the CLI
  suggest that a boolean is expected, but no matter what value you set, it will always delete.

- Let the homedir be expanded in path of helper
  ([`fc7387a`](https://github.com/python-gitlab/python-gitlab/commit/fc7387a0a6039bc58b2a741ac9b73d7068375be7))

- Linting issues and test
  ([`b04dd2c`](https://github.com/python-gitlab/python-gitlab/commit/b04dd2c08b69619bb58832f40a4c4391e350a735))

- Make secret helper more user friendly
  ([`fc2798f`](https://github.com/python-gitlab/python-gitlab/commit/fc2798fc31a08997c049f609c19dd4ab8d75964e))

- Only add query_parameters to GitlabList once
  ([`ca2c3c9`](https://github.com/python-gitlab/python-gitlab/commit/ca2c3c9dee5dc61ea12af5b39d51b1606da32f9c))

Fixes #1386

- Only append kwargs as query parameters
  ([`b9ecc9a`](https://github.com/python-gitlab/python-gitlab/commit/b9ecc9a8c5d958bd7247946c4e8d29c18163c578))

Some arguments to `http_request` were being read from kwargs, but kwargs is where this function
  creates query parameters from, by default. In the absence of a `query_parameters` param, the
  function would construct URLs with query parameters such as `retry_transient_errors=True` despite
  those parameters having no meaning to the API to which the request was sent.

This change names those arguments that are specific to `http_request` so that they do not end up as
  query parameters read from kwargs.

- Remove duplicate class definitions in v4/objects/users.py
  ([`7c4e625`](https://github.com/python-gitlab/python-gitlab/commit/7c4e62597365e8227b8b63ab8ba0c94cafc7abc8))

The classes UserStatus and UserStatusManager were each declared twice. Remove the duplicate
  declarations.

- Test_update_group() dependency on ordering
  ([`e78a8d6`](https://github.com/python-gitlab/python-gitlab/commit/e78a8d6353427bad0055f116e94f471997ee4979))

Since there are two groups we can't depend on the one we changed to always be the first one
  returned.

Instead fetch the group we want and then test our assertion against that group.

- Tox pep8 target, so that it can run
  ([`f518e87`](https://github.com/python-gitlab/python-gitlab/commit/f518e87b5492f2f3c201d4d723c07c746a385b6e))

Previously running the pep8 target would fail as flake8 was not installed.

Now install flake8 for the pep8 target.

NOTE: Running the pep8 target fails as there are many warnings/errors.

But it does allow us to run it and possibly work on reducing these warnings/errors in the future.

In addition, add two checks to the ignore list as black takes care of formatting. The two checks
  added to the ignore list are: * E501: line too long * W503: line break before binary operator

- Undefined name errors
  ([`48ec9e0`](https://github.com/python-gitlab/python-gitlab/commit/48ec9e0f6a2d2da0a24ef8292c70dc441836a913))

Discovered that there were some undefined names.

- Update doc for token helper
  ([`3ac6fa1`](https://github.com/python-gitlab/python-gitlab/commit/3ac6fa12b37dd33610ef2206ef4ddc3b20d9fd3f))

- Update user's bool data and avatar
  ([`3ba27ff`](https://github.com/python-gitlab/python-gitlab/commit/3ba27ffb6ae995c27608f84eef0abe636e2e63da))

If we want to update email, avatar and do not send email confirmation change (`skip_reconfirmation`
  = True), `MultipartEncoder` will try to encode everything except None and bytes. So it tries to
  encode bools. Casting bool's values to their stringified int representation fix it.

- Wrong variable name
  ([`15ec41c`](https://github.com/python-gitlab/python-gitlab/commit/15ec41caf74e264d757d2c64b92427f027194b82))

Discovered this when I ran flake8 on the file. Unfortunately I was the one who introduced this wrong
  variable name :(

- **objects**: Add single get endpoint for instance audit events
  ([`c3f0a6f`](https://github.com/python-gitlab/python-gitlab/commit/c3f0a6f158fbc7d90544274b9bf09d5ac9ac0060))

- **types**: Prevent __dir__ from producing duplicates
  ([`5bf7525`](https://github.com/python-gitlab/python-gitlab/commit/5bf7525d2d37968235514d1b93a403d037800652))

### Chores

- Add _create_attrs & _update_attrs to RESTManager
  ([`147f05d`](https://github.com/python-gitlab/python-gitlab/commit/147f05d43d302d9a04bc87d957c79ce9e54cdaed))

Add the attributes: _create_attrs and _update_attrs to the RESTManager class. This is so that we
  stop using getattr() if we don't need to.

This also helps with type-hints being available for these attributes.

- Add additional type-hints for gitlab/base.py
  ([`ad72ef3`](https://github.com/python-gitlab/python-gitlab/commit/ad72ef35707529058c7c680f334c285746b2f690))

Add type-hints for the variables which are set via self.__dict__

mypy doesn't see them when they are assigned via self.__dict__. So declare them in the class
  definition.

- Add and fix some type-hints in gitlab/client.py
  ([`8837207`](https://github.com/python-gitlab/python-gitlab/commit/88372074a703910ba533237e6901e5af4c26c2bd))

Was able to figure out better type-hints for gitlab/client.py

- Add test
  ([`f8cf1e1`](https://github.com/python-gitlab/python-gitlab/commit/f8cf1e110401dcc6b9b176beb8675513fc1c7d17))

- Add type hints to gitlab/base.py
  ([`3727cbd`](https://github.com/python-gitlab/python-gitlab/commit/3727cbd21fc40b312573ca8da56e0f6cf9577d08))

- Add type hints to gitlab/base.py:RESTManager
  ([`9c55593`](https://github.com/python-gitlab/python-gitlab/commit/9c55593ae6a7308176710665f8bec094d4cadc2e))

Add some additional type hints to gitlab/base.py

- Add type hints to gitlab/utils.py
  ([`acd9294`](https://github.com/python-gitlab/python-gitlab/commit/acd9294fac52a636a016a7a3c14416b10573da28))

- Add type-hints for gitlab/mixins.py
  ([`baea721`](https://github.com/python-gitlab/python-gitlab/commit/baea7215bbbe07c06b2ca0f97a1d3d482668d887))

* Added type-hints for gitlab/mixins.py * Changed use of filter with a lambda expression to
  list-comprehension. mypy was not able to understand the previous code. Also list-comprehension is
  better :)

- Add type-hints to gitlab/cli.py
  ([`10b7b83`](https://github.com/python-gitlab/python-gitlab/commit/10b7b836d31fbe36a7096454287004b46a7799dd))

- Add type-hints to gitlab/client.py
  ([`c9e5b4f`](https://github.com/python-gitlab/python-gitlab/commit/c9e5b4f6285ec94d467c7c10c45f4e2d5f656430))

Adding some initial type-hints to gitlab/client.py

- Add type-hints to gitlab/config.py
  ([`213e563`](https://github.com/python-gitlab/python-gitlab/commit/213e5631b1efce11f8a1419cd77df5d9da7ec0ac))

- Add type-hints to gitlab/const.py
  ([`a10a777`](https://github.com/python-gitlab/python-gitlab/commit/a10a7777caabd6502d04f3947a317b5b0ac869f2))

- Bump version to 2.7.0
  ([`34c4052`](https://github.com/python-gitlab/python-gitlab/commit/34c4052327018279c9a75d6b849da74eccc8819b))

- Del 'import *' in gitlab/v4/objects/project_access_tokens.py
  ([`9efbe12`](https://github.com/python-gitlab/python-gitlab/commit/9efbe1297d8d32419b8f04c3758ca7c83a95f199))

Remove usage of 'import *' in gitlab/v4/objects/project_access_tokens.py.

- Disallow incomplete type defs
  ([`907634f`](https://github.com/python-gitlab/python-gitlab/commit/907634fe4d0d30706656b8bc56260b5532613e62))

Don't allow a partially annotated function definition. Either none of the function is annotated or
  all of it must be.

Update code to ensure no-more partially annotated functions.

Update gitlab/cli.py with better type-hints. Changed Tuple[Any, ...] to Tuple[str, ...]

- Explicitly import gitlab.v4.objects/cli
  ([`233b79e`](https://github.com/python-gitlab/python-gitlab/commit/233b79ed442aac66faf9eb4b0087ea126d6dffc5))

As we only support the v4 Gitlab API, explicitly import gitlab.v4.objects and gitlab.v4.clie instead
  of dynamically importing it depending on the API version.

This has the added benefit of mypy being able to type check the Gitlab __init__() function as
  currently it will fail if we enable type checking of __init__() it will fail.

Also, this also helps by not confusing tools like pyinstaller/cx_freeze with dynamic imports so you
  don't need hooks for standalone executables. And according to https://docs.gitlab.com/ee/api/,

"GraphQL co-exists with the current v4 REST API. If we have a v5 API, this should be a compatibility
  layer on top of GraphQL."

- Fix E711 error reported by flake8
  ([`630901b`](https://github.com/python-gitlab/python-gitlab/commit/630901b30911af01da5543ca609bd27bc5a1a44c))

E711: Comparison to none should be 'if cond is none:'

https://www.flake8rules.com/rules/E711.html

- Fix E712 errors reported by flake8
  ([`83670a4`](https://github.com/python-gitlab/python-gitlab/commit/83670a49a3affd2465f8fcbcc3c26141592c1ccd))

E712: Comparison to true should be 'if cond is true:' or 'if cond:'

https://www.flake8rules.com/rules/E712.html

- Fix E741/E742 errors reported by flake8
  ([`380f227`](https://github.com/python-gitlab/python-gitlab/commit/380f227a1ecffd5e22ae7aefed95af3b5d830994))

Fixes to resolve errors for: https://www.flake8rules.com/rules/E741.html Do not use variables named
  'I', 'O', or 'l' (E741)

https://www.flake8rules.com/rules/E742.html Do not define classes named 'I', 'O', or 'l' (E742)

- Fix F401 errors reported by flake8
  ([`ff21eb6`](https://github.com/python-gitlab/python-gitlab/commit/ff21eb664871904137e6df18308b6e90290ad490))

F401: Module imported but unused

https://www.flake8rules.com/rules/F401.html

- Fix F841 errors reported by flake8
  ([`40f4ab2`](https://github.com/python-gitlab/python-gitlab/commit/40f4ab20ba0903abd3d5c6844fc626eb264b9a6a))

Local variable name is assigned to but never used

https://www.flake8rules.com/rules/F841.html

- Fix package file test naming
  ([`8c80268`](https://github.com/python-gitlab/python-gitlab/commit/8c802680ae7d3bff13220a55efeed9ca79104b10))

- Fix typo in mr events
  ([`c5e6fb3`](https://github.com/python-gitlab/python-gitlab/commit/c5e6fb3bc74c509f35f973e291a7551b2b64dba5))

- Have _create_attrs & _update_attrs be a namedtuple
  ([`aee1f49`](https://github.com/python-gitlab/python-gitlab/commit/aee1f496c1f414c1e30909767d53ae624fe875e7))

Convert _create_attrs and _update_attrs to use a NamedTuple (RequiredOptional) to help with code
  readability. Update all code to use the NamedTuple.

- Import audit events in objects
  ([`35a190c`](https://github.com/python-gitlab/python-gitlab/commit/35a190cfa0902d6a298aba0a3135c5a99edfe0fa))

- Improve type-hints for gitlab/base.py
  ([`cbd43d0`](https://github.com/python-gitlab/python-gitlab/commit/cbd43d0b4c95e46fc3f1cffddc6281eced45db4a))

Determined the base class for obj_cls and adding type-hints for it.

- Make _types always present in RESTManager
  ([`924f83e`](https://github.com/python-gitlab/python-gitlab/commit/924f83eb4b5e160bd231efc38e2eea0231fa311f))

We now create _types = {} in RESTManager class.

By making _types always present in RESTManager it makes the code simpler. We no longer have to do:
  types = getattr(self, "_types", {})

And the type checker now understands the type.

- Make lint happy
  ([`7a7c9fd`](https://github.com/python-gitlab/python-gitlab/commit/7a7c9fd932def75a2f2c517482784e445d83881a))

- Make lint happy
  ([`b5f43c8`](https://github.com/python-gitlab/python-gitlab/commit/b5f43c83b25271f7aff917a9ce8826d39ff94034))

- Make lint happy
  ([`732e49c`](https://github.com/python-gitlab/python-gitlab/commit/732e49c6547c181de8cc56e93b30dc399e87091d))

- Make ListMixin._list_filters always present
  ([`8933113`](https://github.com/python-gitlab/python-gitlab/commit/89331131b3337308bacb0c4013e80a4809f3952c))

Always create ListMixin._list_filters attribute with a default value of tuple().

This way we don't need to use hasattr() and we will know the type of the attribute.

- Make RESTObject._short_print_attrs always present
  ([`6d55120`](https://github.com/python-gitlab/python-gitlab/commit/6d551208f4bc68d091a16323ae0d267fbb6003b6))

Always create RESTObject._short_print_attrs with a default value of None.

This way we don't need to use hasattr() and we will know the type of the attribute.

- Put assert statements inside 'if TYPE_CHECKING:'
  ([`b562458`](https://github.com/python-gitlab/python-gitlab/commit/b562458f063c6be970f58c733fe01ec786798549))

To be safe that we don't assert while running, put the assert statements, which are used by mypy to
  check that types are correct, inside an 'if TYPE_CHECKING:' block.

Also, instead of asserting that the item is a dict, instead assert that it is not a
  requests.Response object. Theoretically the JSON could return as a list or dict, though at this
  time we are assuming a dict.

- Remove import of gitlab.utils from __init__.py
  ([`39b9183`](https://github.com/python-gitlab/python-gitlab/commit/39b918374b771f1d417196ca74fa04fe3968c412))

Initially when extracting out the gitlab/client.py code we tried to remove this but functional tests
  failed.

Later we fixed the functional test that was failing, so now remove the unneeded import.

- Remove Python 2 code
  ([`b5d4e40`](https://github.com/python-gitlab/python-gitlab/commit/b5d4e408830caeef86d4c241ac03a6e8781ef189))

httplib is a Python 2 library. It was renamed to http.client in Python 3.

https://docs.python.org/2.7/library/httplib.html

- Remove unused ALLOWED_KEYSET_ENDPOINTS variable
  ([`3d5d5d8`](https://github.com/python-gitlab/python-gitlab/commit/3d5d5d8b13fc8405e9ef3e14be1fd8bd32235221))

The variable ALLOWED_KEYSET_ENDPOINTS was added in commit f86ef3bbdb5bffa1348a802e62b281d3f31d33ad.

Then most of that commit was removed in commit e71fe16b47835aa4db2834e98c7ffc6bdec36723, but
  ALLOWED_KEYSET_ENDPOINTS was missed.

- Remove unused function _construct_url()
  ([`009d369`](https://github.com/python-gitlab/python-gitlab/commit/009d369f08e46d1e059b98634ff8fe901357002d))

The function _construct_url() was used by the v3 API. All usage of the function was removed in
  commit fe89b949922c028830dd49095432ba627d330186

- Remove unused function sanitize_parameters()
  ([`443b934`](https://github.com/python-gitlab/python-gitlab/commit/443b93482e29fecc12fdbd2329427b37b05ba425))

The function sanitize_parameters() was used when the v3 API was in use. Since v3 API support has
  been removed there are no more users of this function.

- Remove usage of 'from ... import *'
  ([`c83eaf4`](https://github.com/python-gitlab/python-gitlab/commit/c83eaf4f395300471311a67be34d8d306c2b3861))

In gitlab/v4/objects/*.py remove usage of: * from gitlab.base import * * from gitlab.mixins import *

Change them to: * from gitlab.base import CLASS_NAME * from gitlab.mixins import CLASS_NAME

Programmatically update code to explicitly import needed classes only.

After the change the output of: $ flake8 gitlab/v4/objects/*py | grep 'REST\|Mixin'

Is empty. Before many messages about unable to determine if it was a valid name.

- Remove usage of 'from ... import *' in client.py
  ([`bf0c8c5`](https://github.com/python-gitlab/python-gitlab/commit/bf0c8c5d123a7ad0587cb97c3aafd97ab2a9dabf))

In gitlab/client.py remove usage of: * from gitlab.const import * * from gitlab.exceptions import *

Change them to: * import gitlab.const * import gitlab.exceptions

Update code to explicitly reference things in gitlab.const and gitlab.exceptions

A flake8 run no longer lists any undefined variables. Before it listed possible undefined variables.

- Remove usage of getattr()
  ([`2afd18a`](https://github.com/python-gitlab/python-gitlab/commit/2afd18aa28742a3267742859a88be6912a803874))

Remove usage of getattr(self, "_update_uses_post", False)

Instead add it to class and set default value to False.

Add a tests that shows it is set to True for the ProjectMergeRequestApprovalManager and
  ProjectApprovalManager classes.

- **api**: Move repository endpoints into separate module
  ([`1ed154c`](https://github.com/python-gitlab/python-gitlab/commit/1ed154c276fb2429d3b45058b9314d6391dbff02))

- **ci**: Deduplicate PR jobs
  ([`63918c3`](https://github.com/python-gitlab/python-gitlab/commit/63918c364e281f9716885a0f9e5401efcd537406))

- **config**: Allow simple commands without external script
  ([`91ffb8e`](https://github.com/python-gitlab/python-gitlab/commit/91ffb8e97e213d2f14340b952630875995ecedb2))

- **deps**: Update dependency docker-compose to v1.28.3
  ([`2358d48`](https://github.com/python-gitlab/python-gitlab/commit/2358d48acbe1c378377fb852b41ec497217d2555))

- **deps**: Update dependency docker-compose to v1.28.4
  ([`8938484`](https://github.com/python-gitlab/python-gitlab/commit/89384846445be668ca6c861f295297d048cae914))

- **deps**: Update dependency docker-compose to v1.28.5
  ([`f4ab558`](https://github.com/python-gitlab/python-gitlab/commit/f4ab558f2cd85fe716e24f3aa4ede5db5b06e7c4))

- **deps**: Update dependency docker-compose to v1.28.6
  ([`46b05d5`](https://github.com/python-gitlab/python-gitlab/commit/46b05d525d0ade6f2aadb6db23fadc85ad48cd3d))

- **deps**: Update dependency docker-compose to v1.29.1
  ([`a89ec43`](https://github.com/python-gitlab/python-gitlab/commit/a89ec43ee7a60aacd1ac16f0f1f51c4abeaaefef))

- **deps**: Update dependency sphinx to v3.4.3
  ([`37c992c`](https://github.com/python-gitlab/python-gitlab/commit/37c992c09bfd25f3ddcb026f830f3a79c39cb70d))

- **deps**: Update dependency sphinx to v3.5.0
  ([`188c5b6`](https://github.com/python-gitlab/python-gitlab/commit/188c5b692fc195361c70f768cc96c57b3686d4b7))

- **deps**: Update dependency sphinx to v3.5.1
  ([`f916f09`](https://github.com/python-gitlab/python-gitlab/commit/f916f09d3a9cac07246035066d4c184103037026))

- **deps**: Update dependency sphinx to v3.5.2
  ([`9dee5c4`](https://github.com/python-gitlab/python-gitlab/commit/9dee5c420633bc27e1027344279c47862f7b16da))

- **deps**: Update dependency sphinx to v3.5.4
  ([`a886d28`](https://github.com/python-gitlab/python-gitlab/commit/a886d28a893ac592b930ce54111d9ae4e90f458e))

- **deps**: Update gitlab/gitlab-ce docker tag to v13.10.0-ce.0
  ([`5221e33`](https://github.com/python-gitlab/python-gitlab/commit/5221e33768fe1e49456d5df09e3f50b46933c8a4))

- **deps**: Update gitlab/gitlab-ce docker tag to v13.10.1-ce.0
  ([`1995361`](https://github.com/python-gitlab/python-gitlab/commit/1995361d9a767ad5af5338f4555fa5a3914c7374))

- **deps**: Update gitlab/gitlab-ce docker tag to v13.10.3-ce.0
  ([`eabe091`](https://github.com/python-gitlab/python-gitlab/commit/eabe091945d3fe50472059431e599117165a815a))

- **deps**: Update gitlab/gitlab-ce docker tag to v13.11.0-ce.0
  ([`711896f`](https://github.com/python-gitlab/python-gitlab/commit/711896f20ff81826c58f1f86dfb29ad860e1d52a))

- **deps**: Update gitlab/gitlab-ce docker tag to v13.11.1-ce.0
  ([`3088714`](https://github.com/python-gitlab/python-gitlab/commit/308871496041232f555cf4cb055bf7f4aaa22b23))

- **deps**: Update gitlab/gitlab-ce docker tag to v13.8.2-ce.0
  ([`7c12038`](https://github.com/python-gitlab/python-gitlab/commit/7c120384762e23562a958ae5b09aac324151983a))

- **deps**: Update gitlab/gitlab-ce docker tag to v13.8.3-ce.0
  ([`e6c20f1`](https://github.com/python-gitlab/python-gitlab/commit/e6c20f18f3bd1dabdf181a070b9fdbfe4a442622))

- **deps**: Update gitlab/gitlab-ce docker tag to v13.8.4-ce.0
  ([`832cb88`](https://github.com/python-gitlab/python-gitlab/commit/832cb88992cd7af4903f8b780e9475c03c0e6e56))

- **deps**: Update gitlab/gitlab-ce docker tag to v13.9.0-ce.0
  ([`3aef19c`](https://github.com/python-gitlab/python-gitlab/commit/3aef19c51713bdc7ca0a84752da3ca22329fd4c4))

- **deps**: Update gitlab/gitlab-ce docker tag to v13.9.1-ce.0
  ([`f6fd995`](https://github.com/python-gitlab/python-gitlab/commit/f6fd99530d70f2a7626602fd9132b628bb968eab))

- **deps**: Update gitlab/gitlab-ce docker tag to v13.9.2-ce.0
  ([`933ba52`](https://github.com/python-gitlab/python-gitlab/commit/933ba52475e5dae4cf7c569d8283e60eebd5b7b6))

- **deps**: Update gitlab/gitlab-ce docker tag to v13.9.3-ce.0
  ([`2ddf45f`](https://github.com/python-gitlab/python-gitlab/commit/2ddf45fed0b28e52d31153d9b1e95d0cae05e9f5))

- **deps**: Update gitlab/gitlab-ce docker tag to v13.9.4-ce.0
  ([`939f769`](https://github.com/python-gitlab/python-gitlab/commit/939f769e7410738da2e1c5d502caa765f362efdd))

- **deps**: Update precommit hook alessandrojcm/commitlint-pre-commit-hook to v4
  ([`505a8b8`](https://github.com/python-gitlab/python-gitlab/commit/505a8b8d7f16e609f0cde70be88a419235130f2f))

- **deps**: Update wagoid/commitlint-github-action action to v3
  ([`b3274cf`](https://github.com/python-gitlab/python-gitlab/commit/b3274cf93dfb8ae85e4a636a1ffbfa7c48f1c8f6))

- **objects**: Make Project refreshable
  ([`958a6aa`](https://github.com/python-gitlab/python-gitlab/commit/958a6aa83ead3fb6be6ec61bdd894ad78346e7bd))

Helps getting the real state of the project from the server.

- **objects**: Remove noisy deprecation warning for audit events
  ([`2953642`](https://github.com/python-gitlab/python-gitlab/commit/29536423e3e8866eda7118527a49b120fefb4065))

It's mostly an internal thing anyway and can be removed in 3.0.0

- **tests**: Remove unused URL segment
  ([`66f0b6c`](https://github.com/python-gitlab/python-gitlab/commit/66f0b6c23396b849f8653850b099e664daa05eb4))

### Documentation

- Add docs and examples for custom user agent
  ([`a69a214`](https://github.com/python-gitlab/python-gitlab/commit/a69a214ef7f460cef7a7f44351c4861503f9902e))

- Add information about the gitter community
  ([`6ff67e7`](https://github.com/python-gitlab/python-gitlab/commit/6ff67e7327b851fa67be6ad3d82f88ff7cce0dc9))

Add a section in the README.rst about the gitter community. The badge already exists and is useful
  but very easy to miss.

- Change travis-ci badge to githubactions
  ([`2ba5ba2`](https://github.com/python-gitlab/python-gitlab/commit/2ba5ba244808049aad1ee3b42d1da258a9db9f61))

- **api**: Add examples for resource state events
  ([`4d00c12`](https://github.com/python-gitlab/python-gitlab/commit/4d00c12723d565dc0a83670f62e3f5102650d822))

- **api**: Add release links API docs
  ([`36d65f0`](https://github.com/python-gitlab/python-gitlab/commit/36d65f03db253d710938c2d827c1124c94a40506))

### Features

- Add an initial mypy test to tox.ini
  ([`fdec039`](https://github.com/python-gitlab/python-gitlab/commit/fdec03976a17e0708459ba2fab22f54173295f71))

Add an initial mypy test to test gitlab/base.py and gitlab/__init__.py

- Add personal access token API
  ([`2bb16fa`](https://github.com/python-gitlab/python-gitlab/commit/2bb16fac18a6a91847201c174f3bf1208338f6aa))

See: https://docs.gitlab.com/ee/api/personal_access_tokens.html

- Add project audit endpoint
  ([`6660dbe`](https://github.com/python-gitlab/python-gitlab/commit/6660dbefeeffc2b39ddfed4928a59ed6da32ddf4))

- Add ProjectPackageFile
  ([`b9d469b`](https://github.com/python-gitlab/python-gitlab/commit/b9d469bc4e847ae0301be28a0c70019a7f6ab8b6))

Add ProjectPackageFile and the ability to list project package package_files.

Fixes #1372

- Import from bitbucket server
  ([`ff3013a`](https://github.com/python-gitlab/python-gitlab/commit/ff3013a2afeba12811cb3d860de4d0ea06f90545))

I'd like to use this libary to automate importing Bitbucket Server repositories into GitLab. There
  is a [GitLab API
  endpoint](https://docs.gitlab.com/ee/api/import.html#import-repository-from-bitbucket-server) to
  do this, but it is not exposed through this library.

* Add an `import_bitbucket_server` method to the `ProjectManager`. This method calls this GitLab API
  endpoint: https://docs.gitlab.com/ee/api/import.html#import-repository-from-bitbucket-server *
  Modify `import_gitlab` method docstring for python3 compatibility * Add a skipped stub test for
  the existing `import_github` method

- Option to add a helper to lookup token
  ([`8ecf559`](https://github.com/python-gitlab/python-gitlab/commit/8ecf55926f8e345960560e5c5dd6716199cfb0ec))

- **api,cli**: Make user agent configurable
  ([`4bb201b`](https://github.com/python-gitlab/python-gitlab/commit/4bb201b92ef0dcc14a7a9c83e5600ba5b118fc33))

- **issues**: Add missing get verb to IssueManager
  ([`f78ebe0`](https://github.com/python-gitlab/python-gitlab/commit/f78ebe065f73b29555c2dcf17b462bb1037a153e))

- **objects**: Add Release Links API support
  ([`28d7518`](https://github.com/python-gitlab/python-gitlab/commit/28d751811ffda45ff0b1c35e0599b655f3a5a68b))

- **objects**: Add support for group audit events API
  ([`2a0fbdf`](https://github.com/python-gitlab/python-gitlab/commit/2a0fbdf9fe98da6c436230be47b0ddb198c7eca9))

- **objects**: Add support for resource state events API
  ([`d4799c4`](https://github.com/python-gitlab/python-gitlab/commit/d4799c40bd12ed85d4bb834464fdb36c4dadcab6))

- **projects**: Add project access token api
  ([`1becef0`](https://github.com/python-gitlab/python-gitlab/commit/1becef0253804f119c8a4d0b8b1c53deb2f4d889))

- **users**: Add follow/unfollow API
  ([`e456869`](https://github.com/python-gitlab/python-gitlab/commit/e456869d98a1b7d07e6f878a0d6a9719c1b10fd4))

### Refactoring

- Move Gitlab and GitlabList to gitlab/client.py
  ([`53a7645`](https://github.com/python-gitlab/python-gitlab/commit/53a764530cc3c6411034a3798f794545881d341e))

Move the classes Gitlab and GitlabList from gitlab/__init__.py to the newly created gitlab/client.py
  file.

Update one test case that was depending on requests being defined in gitlab/__init__.py

- **api**: Explicitly export classes for star imports
  ([`f05c287`](https://github.com/python-gitlab/python-gitlab/commit/f05c287512a9253c7f7d308d3437240ac8257452))

- **objects**: Move instance audit events where they belong
  ([`48ba88f`](https://github.com/python-gitlab/python-gitlab/commit/48ba88ffb983207da398ea2170c867f87a8898e9))

- **v4**: Split objects and managers per API resource
  ([`a5a48ad`](https://github.com/python-gitlab/python-gitlab/commit/a5a48ad08577be70c6ca511d3b4803624e5c2043))

### Testing

- Don't add duplicate fixture
  ([`5d94846`](https://github.com/python-gitlab/python-gitlab/commit/5d9484617e56b89ac5e17f8fc94c0b1eb46d4b89))

Co-authored-by: Nejc Habjan <hab.nejc@gmail.com>

- **api**: Add functional test for release links API
  ([`ab2a1c8`](https://github.com/python-gitlab/python-gitlab/commit/ab2a1c816d83e9e308c0c9c7abf1503438b0b3be))

- **api,cli**: Add tests for custom user agent
  ([`c5a37e7`](https://github.com/python-gitlab/python-gitlab/commit/c5a37e7e37a62372c250dfc8c0799e847eecbc30))

- **object**: Add test for __dir__ duplicates
  ([`a8e591f`](https://github.com/python-gitlab/python-gitlab/commit/a8e591f742f777f8747213b783271004e5acc74d))

- **objects**: Add tests for resource state events
  ([`10225cf`](https://github.com/python-gitlab/python-gitlab/commit/10225cf26095efe82713136ddde3330e7afc6d10))

- **objects**: Add unit test for instance audit events
  ([`84e3247`](https://github.com/python-gitlab/python-gitlab/commit/84e3247d0cd3ddb1f3aa0ac91fb977c3e1e197b5))


## v2.6.0 (2021-01-29)

### Bug Fixes

- Docs changed using the consts
  ([`650b65c`](https://github.com/python-gitlab/python-gitlab/commit/650b65c389c686bcc9a9cef81b6ca2a509d8cad2))

- Typo
  ([`9baa905`](https://github.com/python-gitlab/python-gitlab/commit/9baa90535b5a8096600f9aec96e528f4d2ac7d74))

- **api**: Add missing runner access_level param
  ([`92669f2`](https://github.com/python-gitlab/python-gitlab/commit/92669f2ef2af3cac1c5f06f9299975060cc5e64a))

- **api**: Use RetrieveMixin for ProjectLabelManager
  ([`1a14395`](https://github.com/python-gitlab/python-gitlab/commit/1a143952119ce8e964cc7fcbfd73b8678ee2da74))

Allows to get a single label from a project, which was missing before even though the GitLab API has
  the ability to.

- **base**: Really refresh object
  ([`e1e0d8c`](https://github.com/python-gitlab/python-gitlab/commit/e1e0d8cbea1fed8aeb52b4d7cccd2e978faf2d3f))

This fixes and error, where deleted attributes would not show up

Fixes #1155

- **cli**: Add missing args for project lists
  ([`c73e237`](https://github.com/python-gitlab/python-gitlab/commit/c73e23747d24ffef3c1a2a4e5f4ae24252762a71))

- **cli**: Write binary data to stdout buffer
  ([`0733ec6`](https://github.com/python-gitlab/python-gitlab/commit/0733ec6cad5c11b470ce6bad5dc559018ff73b3c))

### Chores

- Added constants for search API
  ([`8ef53d6`](https://github.com/python-gitlab/python-gitlab/commit/8ef53d6f6180440582d1cca305fd084c9eb70443))

- Added docs for search scopes constants
  ([`7565bf0`](https://github.com/python-gitlab/python-gitlab/commit/7565bf059b240c9fffaf6959ee168a12d0fedd77))

- Allow overriding docker-compose env vars for tag
  ([`27109ca`](https://github.com/python-gitlab/python-gitlab/commit/27109cad0d97114b187ce98ce77e4d7b0c7c3270))

- Apply suggestions
  ([`65ce026`](https://github.com/python-gitlab/python-gitlab/commit/65ce02675d9c9580860df91b41c3cf5e6bb8d318))

- Move .env into docker-compose dir
  ([`55cbd1c`](https://github.com/python-gitlab/python-gitlab/commit/55cbd1cbc28b93673f73818639614c61c18f07d1))

- Offically support and test 3.9
  ([`62dd07d`](https://github.com/python-gitlab/python-gitlab/commit/62dd07df98341f35c8629e8f0a987b35b70f7fe6))

- Remove unnecessary random function
  ([`d4ee0a6`](https://github.com/python-gitlab/python-gitlab/commit/d4ee0a6085d391ed54d715a5ed4b0082783ca8f3))

- Simplified search scope constants
  ([`16fc048`](https://github.com/python-gitlab/python-gitlab/commit/16fc0489b2fe24e0356e9092c9878210b7330a72))

- Use helper fixtures for test directories
  ([`40ec2f5`](https://github.com/python-gitlab/python-gitlab/commit/40ec2f528b885290fbb3e2d7ef0f5f8615219326))

- **ci**: Add .readthedocs.yml
  ([`0ad441e`](https://github.com/python-gitlab/python-gitlab/commit/0ad441eee5f2ac1b7c05455165e0085045c24b1d))

- **ci**: Add coverage and docs jobs
  ([`2de64cf`](https://github.com/python-gitlab/python-gitlab/commit/2de64cfa469c9d644a2950d3a4884f622ed9faf4))

- **ci**: Add pytest PR annotations
  ([`8f92230`](https://github.com/python-gitlab/python-gitlab/commit/8f9223041481976522af4c4f824ad45e66745f29))

- **ci**: Fix copy/paste oopsie
  ([`c6241e7`](https://github.com/python-gitlab/python-gitlab/commit/c6241e791357d3f90e478c456cc6d572b388e6d1))

- **ci**: Fix typo in matrix
  ([`5e1547a`](https://github.com/python-gitlab/python-gitlab/commit/5e1547a06709659c75d40a05ac924c51caffcccf))

- **ci**: Force colors in pytest runs
  ([`1502079`](https://github.com/python-gitlab/python-gitlab/commit/150207908a72869869d161ecb618db141e3a9348))

- **ci**: Pin docker-compose install for tests
  ([`1f7a2ab`](https://github.com/python-gitlab/python-gitlab/commit/1f7a2ab5bd620b06eb29146e502e46bd47432821))

This ensures python-dotenv with expected behavior for .env processing

- **ci**: Pin os version
  ([`cfa27ac`](https://github.com/python-gitlab/python-gitlab/commit/cfa27ac6453f20e1d1f33973aa8cbfccff1d6635))

- **ci**: Reduce renovate PR noise
  ([`f4d7a55`](https://github.com/python-gitlab/python-gitlab/commit/f4d7a5503f3a77f6aa4d4e772c8feb3145044fec))

- **ci**: Replace travis with Actions
  ([`8bb73a3`](https://github.com/python-gitlab/python-gitlab/commit/8bb73a3440b79df93c43214c31332ad47ab286d8))

- **cli**: Remove python2 code
  ([`1030e0a`](https://github.com/python-gitlab/python-gitlab/commit/1030e0a7e13c4ec3fdc48b9010e9892833850db9))

- **deps**: Pin dependencies
  ([`14d8f77`](https://github.com/python-gitlab/python-gitlab/commit/14d8f77601a1ee4b36888d68f0102dd1838551f2))

- **deps**: Pin dependency requests-toolbelt to ==0.9.1
  ([`4d25f20`](https://github.com/python-gitlab/python-gitlab/commit/4d25f20e8f946ab58d1f0c2ef3a005cb58dc8b6c))

- **deps**: Update dependency requests to v2.25.1
  ([`9c2789e`](https://github.com/python-gitlab/python-gitlab/commit/9c2789e4a55822d7c50284adc89b9b6bfd936a72))

- **deps**: Update gitlab/gitlab-ce docker tag to v13.3.3-ce.0
  ([`667bf01`](https://github.com/python-gitlab/python-gitlab/commit/667bf01b6d3da218df6c4fbdd9c7b9282a2aaff9))

- **deps**: Update gitlab/gitlab-ce docker tag to v13.3.4-ce.0
  ([`e94c4c6`](https://github.com/python-gitlab/python-gitlab/commit/e94c4c67f21ecaa2862f861953c2d006923d3280))

- **deps**: Update gitlab/gitlab-ce docker tag to v13.3.5-ce.0
  ([`c88d870`](https://github.com/python-gitlab/python-gitlab/commit/c88d87092f39d11ecb4f52ab7cf49634a0f27e80))

- **deps**: Update gitlab/gitlab-ce docker tag to v13.3.6-ce.0
  ([`57b5782`](https://github.com/python-gitlab/python-gitlab/commit/57b5782219a86153cc3425632e232db3f3c237d7))

- **deps**: Update gitlab/gitlab-ce docker tag to v13.4.3-ce.0
  ([`bc17889`](https://github.com/python-gitlab/python-gitlab/commit/bc178898776d2d61477ff773248217adfac81f56))

- **deps**: Update gitlab/gitlab-ce docker tag to v13.5.0-ce.0
  ([`fc205cc`](https://github.com/python-gitlab/python-gitlab/commit/fc205cc593a13ec2ce5615293a9c04c262bd2085))

- **deps**: Update gitlab/gitlab-ce docker tag to v13.5.1-ce.0
  ([`348e860`](https://github.com/python-gitlab/python-gitlab/commit/348e860a9128a654eff7624039da2c792a1c9124))

- **deps**: Update gitlab/gitlab-ce docker tag to v13.5.2-ce.0
  ([`4a6831c`](https://github.com/python-gitlab/python-gitlab/commit/4a6831c6aa6eca8e976be70df58187515e43f6ce))

- **deps**: Update gitlab/gitlab-ce docker tag to v13.5.3-ce.0
  ([`d1b0b08`](https://github.com/python-gitlab/python-gitlab/commit/d1b0b08e4efdd7be2435833a28d12866fe098d44))

- **deps**: Update gitlab/gitlab-ce docker tag to v13.5.4-ce.0
  ([`265dbbd`](https://github.com/python-gitlab/python-gitlab/commit/265dbbdd37af88395574564aeb3fd0350288a18c))

- **deps**: Update gitlab/gitlab-ce docker tag to v13.8.1-ce.0
  ([`9854d6d`](https://github.com/python-gitlab/python-gitlab/commit/9854d6da84c192f765e0bc80d13bc4dae16caad6))

- **deps**: Update python docker tag to v3.9
  ([`1fc65e0`](https://github.com/python-gitlab/python-gitlab/commit/1fc65e072003a2d1ebc29d741e9cef1860b5ff78))

- **docs**: Always edit the file directly on master
  ([`35e43c5`](https://github.com/python-gitlab/python-gitlab/commit/35e43c54cd282f06dde0d24326641646fc3fa29e))

There is no way to edit the raw commit

- **test**: Remove hacking dependencies
  ([`9384493`](https://github.com/python-gitlab/python-gitlab/commit/9384493942a4a421aced4bccc7c7291ff30af886))

### Documentation

- Add Project Merge Request approval rule documentation
  ([`449fc26`](https://github.com/python-gitlab/python-gitlab/commit/449fc26ffa98ef5703d019154f37a4959816f607))

- Clean up grammar and formatting in documentation
  ([`aff9bc7`](https://github.com/python-gitlab/python-gitlab/commit/aff9bc737d90e1a6e91ab8efa40a6756c7ce5cba))

- **cli**: Add auto-generated CLI reference
  ([`6c21fc8`](https://github.com/python-gitlab/python-gitlab/commit/6c21fc83d3d6173bffb60e686ec579f875f8bebe))

- **cli**: Add example for job artifacts download
  ([`375b29d`](https://github.com/python-gitlab/python-gitlab/commit/375b29d3ab393f7b3fa734c5320736cdcba5df8a))

- **cli**: Use inline anonymous references for external links
  ([`f2cf467`](https://github.com/python-gitlab/python-gitlab/commit/f2cf467443d1c8a1a24a8ebf0ec1ae0638871336))

There doesn't seem to be an obvious way to use an alias for identical text labels that link to
  different targets. With inline links we can work around this shortcoming. Until we know better.

- **cli-usage**: Fixed term
  ([`d282a99`](https://github.com/python-gitlab/python-gitlab/commit/d282a99e29abf390c926dcc50984ac5523d39127))

- **groups**: Add example for creating subgroups
  ([`92eb4e3`](https://github.com/python-gitlab/python-gitlab/commit/92eb4e3ca0ccd83dba2067ccc4ce206fd17be020))

- **issues**: Add admin, project owner hint
  ([`609c03b`](https://github.com/python-gitlab/python-gitlab/commit/609c03b7139db8af5524ebeb741fd5b003e17038))

Closes #1101

- **projects**: Correct fork docs
  ([`54921db`](https://github.com/python-gitlab/python-gitlab/commit/54921dbcf117f6b939e0c467738399be0d661a00))

Closes #1126

- **readme**: Also add hint to delete gitlab-runner-test
  ([`8894f2d`](https://github.com/python-gitlab/python-gitlab/commit/8894f2da81d885c1e788a3b21686212ad91d5bf2))

Otherwise the whole testsuite will refuse to run

- **readme**: Update supported Python versions
  ([`20b1e79`](https://github.com/python-gitlab/python-gitlab/commit/20b1e791c7a78633682b2d9f7ace8eb0636f2424))

### Features

- Add MINIMAL_ACCESS constant
  ([`49eb3ca`](https://github.com/python-gitlab/python-gitlab/commit/49eb3ca79172905bf49bab1486ecb91c593ea1d7))

A "minimal access" access level was
  [introduced](https://gitlab.com/gitlab-org/gitlab/-/issues/220203) in GitLab 13.5.

- Added support for pipeline bridges
  ([`05cbdc2`](https://github.com/python-gitlab/python-gitlab/commit/05cbdc224007e9dda10fc2f6f7d63c82cf36dec0))

- Adds support for project merge request approval rules
  ([#1199](https://github.com/python-gitlab/python-gitlab/pull/1199),
  [`c6fbf39`](https://github.com/python-gitlab/python-gitlab/commit/c6fbf399ec5cbc92f995a5d61342f295be68bd79))

- Support multipart uploads
  ([`2fa3004`](https://github.com/python-gitlab/python-gitlab/commit/2fa3004d9e34cc4b77fbd6bd89a15957898e1363))

- Unit tests added
  ([`f37ebf5`](https://github.com/python-gitlab/python-gitlab/commit/f37ebf5fd792c8e8a973443a1df386fa77d1248f))

- **api**: Add support for user identity provider deletion
  ([`e78e121`](https://github.com/python-gitlab/python-gitlab/commit/e78e121575deb7b5ce490b2293caa290860fc3e9))

- **api**: Added wip filter param for merge requests
  ([`d6078f8`](https://github.com/python-gitlab/python-gitlab/commit/d6078f808bf19ef16cfebfaeabb09fbf70bfb4c7))

- **api**: Added wip filter param for merge requests
  ([`aa6e80d`](https://github.com/python-gitlab/python-gitlab/commit/aa6e80d58d765102892fadb89951ce29d08e1dab))

- **tests**: Test label getter
  ([`a41af90`](https://github.com/python-gitlab/python-gitlab/commit/a41af902675a07cd4772bb122c152547d6d570f7))

### Refactoring

- **tests**: Split functional tests
  ([`61e43eb`](https://github.com/python-gitlab/python-gitlab/commit/61e43eb186925feede073c7065e5ae868ffbb4ec))

### Testing

- Add test_project_merge_request_approvals.py
  ([`9f6335f`](https://github.com/python-gitlab/python-gitlab/commit/9f6335f7b79f52927d5c5734e47f4b8d35cd6c4a))

- Add unit tests for badges API
  ([`2720b73`](https://github.com/python-gitlab/python-gitlab/commit/2720b7385a3686d3adaa09a3584d165bd7679367))

- Add unit tests for resource label events API
  ([`e9a211c`](https://github.com/python-gitlab/python-gitlab/commit/e9a211ca8080e07727d0217e1cdc2851b13a85b7))

- Ignore failing test for now
  ([`4b4e253`](https://github.com/python-gitlab/python-gitlab/commit/4b4e25399f35e204320ac9f4e333b8cf7b262595))

- **cli**: Add test for job artifacts download
  ([`f4e7950`](https://github.com/python-gitlab/python-gitlab/commit/f4e79501f1be1394873042dd65beda49e869afb8))

- **env**: Replace custom scripts with pytest and docker-compose
  ([`79489c7`](https://github.com/python-gitlab/python-gitlab/commit/79489c775141c4ddd1f7aecae90dae8061d541fe))


## v2.5.0 (2020-09-01)

### Bug Fixes

- Implement Gitlab's behavior change for owned=True
  ([`9977799`](https://github.com/python-gitlab/python-gitlab/commit/99777991e0b9d5a39976d08554dea8bb7e514019))

- Tests fail when using REUSE_CONTAINER option
  ([`0078f89`](https://github.com/python-gitlab/python-gitlab/commit/0078f8993c38df4f02da9aaa3f7616d1c8b97095))

Fixes #1146

- Wrong reconfirmation parameter when updating user's email
  ([`b5c267e`](https://github.com/python-gitlab/python-gitlab/commit/b5c267e110b2d7128da4f91c62689456d5ce275f))

Since version 10.3 (and later), param to not send (re)confirmation when updating an user is
  `skip_reconfirmation` (and not `skip_confirmation`).

See:

* https://gitlab.com/gitlab-org/gitlab-foss/-/merge_requests/15175?tab= *
  https://docs.gitlab.com/11.11/ee/api/users.html#user-modification *
  https://docs.gitlab.com/ee/api/users.html#user-modification

### Chores

- Bump python-gitlab to 2.5.0
  ([`56fef01`](https://github.com/python-gitlab/python-gitlab/commit/56fef0180431f442ada5ce62352e4e813288257d))

- Make latest black happy with existing code
  ([`6961479`](https://github.com/python-gitlab/python-gitlab/commit/696147922552a8e6ddda3a5b852ee2de6b983e37))

- Make latest black happy with existing code
  ([`4039c8c`](https://github.com/python-gitlab/python-gitlab/commit/4039c8cfc6c7783270f0da1e235ef5d70b420ba9))

- Make latest black happy with existing code
  ([`d299753`](https://github.com/python-gitlab/python-gitlab/commit/d2997530bc3355048143bc29580ef32fc21dac3d))

- Remove remnants of python2 imports
  ([`402566a`](https://github.com/python-gitlab/python-gitlab/commit/402566a665dfdf0862f15a7e59e4d804d1301c77))

- Remove unnecessary import
  ([`f337b7a`](https://github.com/python-gitlab/python-gitlab/commit/f337b7ac43e49f9d3610235749b1e2a21731352d))

- Run unittest2pytest on all unit tests
  ([`11383e7`](https://github.com/python-gitlab/python-gitlab/commit/11383e70f74c70e6fe8a56f18b5b170db982f402))

- Update tools dir for latest black version
  ([`c2806d8`](https://github.com/python-gitlab/python-gitlab/commit/c2806d8c0454a83dfdafd1bdbf7e10bb28d205e0))

- Update tools dir for latest black version
  ([`f245ffb`](https://github.com/python-gitlab/python-gitlab/commit/f245ffbfad6f1d1f66d386a4b00b3a6ff3e74daa))

- **ci**: Pin gitlab-ce version for renovate
  ([`cb79fb7`](https://github.com/python-gitlab/python-gitlab/commit/cb79fb72e899e65a1ad77ccd508f1a1baca30309))

- **ci**: Use fixed black version
  ([`9565684`](https://github.com/python-gitlab/python-gitlab/commit/9565684c86cb018fb22ee0b29345d2cd130f3fd7))

- **deps**: Update gitlab/gitlab-ce docker tag to v13.3.2-ce.0
  ([`9fd778b`](https://github.com/python-gitlab/python-gitlab/commit/9fd778b4a7e92a7405ac2f05c855bafbc51dc6a8))

- **deps**: Update python docker tag to v3.8
  ([`a8070f2`](https://github.com/python-gitlab/python-gitlab/commit/a8070f2d9a996e57104f29539069273774cf5493))

- **env**: Add pre-commit and commit-msg hooks
  ([`82070b2`](https://github.com/python-gitlab/python-gitlab/commit/82070b2d2ed99189aebb1d595430ad5567306c4c))

- **test**: Use pathlib for paths
  ([`5a56b6b`](https://github.com/python-gitlab/python-gitlab/commit/5a56b6b55f761940f80491eddcdcf17d37215cfd))

### Documentation

- Additional project file delete example
  ([`9e94b75`](https://github.com/python-gitlab/python-gitlab/commit/9e94b7511de821619e8bcf66a3ae1f187f15d594))

Showing how to delete without having to pull the file

- **api**: Add example for latest pipeline job artifacts
  ([`d20f022`](https://github.com/python-gitlab/python-gitlab/commit/d20f022a8fe29a6086d30aa7616aa1dac3e1bb17))

- **cli**: Add examples for group-project list
  ([`af86dcd`](https://github.com/python-gitlab/python-gitlab/commit/af86dcdd28ee1b16d590af31672c838597e3f3ec))

- **packages**: Add examples for Packages API and cli usage
  ([`a47dfcd`](https://github.com/python-gitlab/python-gitlab/commit/a47dfcd9ded3a0467e83396f21e6dcfa232dfdd7))

- **variables**: Add docs for instance-level variables
  ([`ad4b87c`](https://github.com/python-gitlab/python-gitlab/commit/ad4b87cb3d6802deea971e6574ae9afe4f352e31))

### Features

- Add share/unshare group with group
  ([`7c6e541`](https://github.com/python-gitlab/python-gitlab/commit/7c6e541dc2642740a6ec2d7ed7921aca41446b37))

- Add support to resource milestone events
  ([`88f8cc7`](https://github.com/python-gitlab/python-gitlab/commit/88f8cc78f97156d5888a9600bdb8721720563120))

Fixes #1154

- **api**: Add endpoint for latest ref artifacts
  ([`b7a07fc`](https://github.com/python-gitlab/python-gitlab/commit/b7a07fca775b278b1de7d5cb36c8421b7d9bebb7))

- **api**: Add support for instance variables
  ([`4492fc4`](https://github.com/python-gitlab/python-gitlab/commit/4492fc42c9f6e0031dd3f3c6c99e4c58d4f472ff))

- **api**: Add support for Packages API
  ([`71495d1`](https://github.com/python-gitlab/python-gitlab/commit/71495d127d30d2f4c00285485adae5454a590584))

### Refactoring

- Rewrite unit tests for objects with responses
  ([`204782a`](https://github.com/python-gitlab/python-gitlab/commit/204782a117f77f367dee87aa2c70822587829147))

- Split unit tests by GitLab API resources
  ([`76b2cad`](https://github.com/python-gitlab/python-gitlab/commit/76b2cadf1418e4ea2ac420ebba5a4b4f16fbd4c7))

- Turn objects module into a package
  ([`da8af6f`](https://github.com/python-gitlab/python-gitlab/commit/da8af6f6be6886dca4f96390632cf3b91891954e))

### Testing

- Add unit tests for resource milestone events API
  ([`1317f4b`](https://github.com/python-gitlab/python-gitlab/commit/1317f4b62afefcb2504472d5b5d8e24f39b0d86f))

Fixes #1154

- **api**: Add tests for variables API
  ([`66d108d`](https://github.com/python-gitlab/python-gitlab/commit/66d108de9665055921123476426fb6716c602496))

- **packages**: Add tests for Packages API
  ([`7ea178b`](https://github.com/python-gitlab/python-gitlab/commit/7ea178bad398c8c2851a4584f4dca5b8adc89d29))


## v2.4.0 (2020-07-09)

### Bug Fixes

- Add masked parameter for variables command
  ([`b6339bf`](https://github.com/python-gitlab/python-gitlab/commit/b6339bf85f3ae11d31bf03c4132f6e7b7c343900))

- Do not check if kwargs is none
  ([`a349b90`](https://github.com/python-gitlab/python-gitlab/commit/a349b90ea6016ec8fbe91583f2bbd9832b41a368))

Co-authored-by: Traian Nedelea <tron1point0@pm.me>

- Make query kwargs consistent between call in init and next
  ([`72ffa01`](https://github.com/python-gitlab/python-gitlab/commit/72ffa0164edc44a503364f9b7e25c5b399f648c3))

- Pass kwargs to subsequent queries in gitlab list
  ([`1d011ac`](https://github.com/python-gitlab/python-gitlab/commit/1d011ac72aeb18b5f31d10e42ffb49cf703c3e3a))

- **merge**: Parse arguments as query_data
  ([`878098b`](https://github.com/python-gitlab/python-gitlab/commit/878098b74e216b4359e0ce012ff5cd6973043a0a))

### Chores

- Bump version to 2.4.0
  ([`1606310`](https://github.com/python-gitlab/python-gitlab/commit/1606310a880f8a8a2a370db27511b57732caf178))

### Documentation

- **pipelines**: Simplify download
  ([`9a068e0`](https://github.com/python-gitlab/python-gitlab/commit/9a068e00eba364eb121a2d7d4c839e2f4c7371c8))

This uses a context instead of inventing your own stream handler which makes the code simpler and
  should be fine for most use cases.

Signed-off-by: Paul Spooren <mail@aparcar.org>

### Features

- Added NO_ACCESS const
  ([`dab4d0a`](https://github.com/python-gitlab/python-gitlab/commit/dab4d0a1deec6d7158c0e79b9eef20d53c0106f0))

This constant is useful for cases where no access is granted, e.g. when creating a protected branch.

The `NO_ACCESS` const corresponds to the definition in
  https://docs.gitlab.com/ee/api/protected_branches.html


## v2.3.1 (2020-06-09)

### Bug Fixes

- Disable default keyset pagination
  ([`e71fe16`](https://github.com/python-gitlab/python-gitlab/commit/e71fe16b47835aa4db2834e98c7ffc6bdec36723))

Instead we set pagination to offset on the other paths

### Chores

- Bump version to 2.3.1
  ([`870e7ea`](https://github.com/python-gitlab/python-gitlab/commit/870e7ea12ee424eb2454dd7d4b7906f89fbfea64))


## v2.3.0 (2020-06-08)

### Bug Fixes

- Use keyset pagination by default for /projects > 50000
  ([`f86ef3b`](https://github.com/python-gitlab/python-gitlab/commit/f86ef3bbdb5bffa1348a802e62b281d3f31d33ad))

Workaround for https://gitlab.com/gitlab-org/gitlab/-/issues/218504. Remove this in 13.1

- **config**: Fix duplicate code
  ([`ee2df6f`](https://github.com/python-gitlab/python-gitlab/commit/ee2df6f1757658cae20cc1d9dd75be599cf19997))

Fixes #1094

- **project**: Add missing project parameters
  ([`ad8c67d`](https://github.com/python-gitlab/python-gitlab/commit/ad8c67d65572a9f9207433e177834cc66f8e48b3))

### Chores

- Bring commit signatures up to date with 12.10
  ([`dc382fe`](https://github.com/python-gitlab/python-gitlab/commit/dc382fe3443a797e016f8c5f6eac68b7b69305ab))

- Bump to 2.3.0
  ([`01ff865`](https://github.com/python-gitlab/python-gitlab/commit/01ff8658532e7a7d3b53ba825c7ee311f7feb1ab))

- Correctly render rst
  ([`f674bf2`](https://github.com/python-gitlab/python-gitlab/commit/f674bf239e6ced4f420bee0a642053f63dace28b))

- Fix typo in docstring
  ([`c20f5f1`](https://github.com/python-gitlab/python-gitlab/commit/c20f5f15de84d1b1bbb12c18caf1927dcfd6f393))

- Remove old builds-email service
  ([`c60e2df`](https://github.com/python-gitlab/python-gitlab/commit/c60e2df50773535f5cfdbbb974713f28828fd827))

- Use pytest for unit tests and coverage
  ([`9787a40`](https://github.com/python-gitlab/python-gitlab/commit/9787a407b700f18dadfb4153b3ba1375a615b73c))

- **ci**: Add codecov integration to Travis
  ([`e230568`](https://github.com/python-gitlab/python-gitlab/commit/e2305685dea2d99ca389f79dc40e40b8d3a1fee0))

- **services**: Update available service attributes
  ([`7afc357`](https://github.com/python-gitlab/python-gitlab/commit/7afc3570c02c5421df76e097ce33d1021820a3d6))

- **test**: Remove outdated token test
  ([`e6c9fe9`](https://github.com/python-gitlab/python-gitlab/commit/e6c9fe920df43ae2ab13f26310213e8e4db6b415))

### Continuous Integration

- Add a test for creating and triggering pipeline schedule
  ([`9f04560`](https://github.com/python-gitlab/python-gitlab/commit/9f04560e59f372f80ac199aeee16378d8f80610c))

- Lint fixes
  ([`930122b`](https://github.com/python-gitlab/python-gitlab/commit/930122b1848b3d42af1cf8567a065829ec0eb44f))

### Documentation

- Update authors
  ([`ac0c84d`](https://github.com/python-gitlab/python-gitlab/commit/ac0c84de02a237db350d3b21fe74d0c24d85a94e))

- **readme**: Add codecov badge for master
  ([`e21b2c5`](https://github.com/python-gitlab/python-gitlab/commit/e21b2c5c6a600c60437a41f231fea2adcfd89fbd))

- **readme**: Update test docs
  ([`6e2b1ec`](https://github.com/python-gitlab/python-gitlab/commit/6e2b1ec947a6e352b412fd4e1142006621dd76a4))

- **remote_mirrors**: Fix create command
  ([`bab91fe`](https://github.com/python-gitlab/python-gitlab/commit/bab91fe86fc8d23464027b1c3ab30619e520235e))

- **remote_mirrors**: Fix create command
  ([`1bb4e42`](https://github.com/python-gitlab/python-gitlab/commit/1bb4e42858696c9ac8cbfc0f89fa703921b969f3))

### Features

- Add group runners api
  ([`4943991`](https://github.com/python-gitlab/python-gitlab/commit/49439916ab58b3481308df5800f9ffba8f5a8ffd))

- Add play command to project pipeline schedules
  ([`07b9988`](https://github.com/python-gitlab/python-gitlab/commit/07b99881dfa6efa9665245647460e99846ccd341))

fix: remove version from setup

feat: add pipeline schedule play error exception

docs: add documentation for pipeline schedule play

- Allow an environment variable to specify config location
  ([`401e702`](https://github.com/python-gitlab/python-gitlab/commit/401e702a9ff14bf4cc33b3ed3acf16f3c60c6945))

It can be useful (especially in scripts) to specify a configuration location via an environment
  variable. If the "PYTHON_GITLAB_CFG" environment variable is defined, treat its value as the path
  to a configuration file and include it in the set of default configuration locations.

- **api**: Added support in the GroupManager to upload Group avatars
  ([`28eb7ea`](https://github.com/python-gitlab/python-gitlab/commit/28eb7eab8fbe3750fb56e85967e8179b7025f441))

- **services**: Add project service list API
  ([`fc52221`](https://github.com/python-gitlab/python-gitlab/commit/fc5222188ad096932fa89bb53f03f7118926898a))

Can be used to list available services It was introduced in GitLab 12.7

- **types**: Add __dir__ to RESTObject to expose attributes
  ([`cad134c`](https://github.com/python-gitlab/python-gitlab/commit/cad134c078573c009af18160652182e39ab5b114))

### Testing

- Disable test until Gitlab 13.1
  ([`63ae77a`](https://github.com/python-gitlab/python-gitlab/commit/63ae77ac1d963e2c45bbed7948d18313caf2c016))

- **cli**: Convert shell tests to pytest test cases
  ([`c4ab4f5`](https://github.com/python-gitlab/python-gitlab/commit/c4ab4f57e23eed06faeac8d4fa9ffb9ce5d47e48))

- **runners**: Add all runners unit tests
  ([`127fa5a`](https://github.com/python-gitlab/python-gitlab/commit/127fa5a2134aee82958ce05357d60513569c3659))


## v2.2.0 (2020-04-07)

### Bug Fixes

- Add missing import_project param
  ([`9b16614`](https://github.com/python-gitlab/python-gitlab/commit/9b16614ba6444b212b3021a741b9c184ac206af1))

- **types**: Do not split single value string in ListAttribute
  ([`a26e585`](https://github.com/python-gitlab/python-gitlab/commit/a26e58585b3d82cf1a3e60a3b7b3bfd7f51d77e5))

### Chores

- Bump to 2.2.0
  ([`22d4b46`](https://github.com/python-gitlab/python-gitlab/commit/22d4b465c3217536cb444dafe5c25e9aaa3aa7be))

- Clean up for black and flake8
  ([`4fede5d`](https://github.com/python-gitlab/python-gitlab/commit/4fede5d692fdd4477a37670b7b35268f5d1c4bf0))

- Fix typo in allow_failures
  ([`265bbdd`](https://github.com/python-gitlab/python-gitlab/commit/265bbddacc25d709a8f13807ed04cae393d9802d))

- Flatten test_import_github
  ([`b8ea96c`](https://github.com/python-gitlab/python-gitlab/commit/b8ea96cc20519b751631b27941d60c486aa4188c))

- Improve and document testing against different images
  ([`98d3f77`](https://github.com/python-gitlab/python-gitlab/commit/98d3f770c4cc7e15493380e1a2201c63f0a332a2))

- Move test_import_github into TestProjectImport
  ([`a881fb7`](https://github.com/python-gitlab/python-gitlab/commit/a881fb71eebf744bcbe232869f622ea8a3ac975f))

- Pass environment variables in tox
  ([`e06d33c`](https://github.com/python-gitlab/python-gitlab/commit/e06d33c1bcfa71e0c7b3e478d16b3a0e28e05a23))

- Remove references to python2 in test env
  ([`6e80723`](https://github.com/python-gitlab/python-gitlab/commit/6e80723e5fa00e8b870ec25d1cb2484d4b5816ca))

- Rename ExportMixin to DownloadMixin
  ([`847da60`](https://github.com/python-gitlab/python-gitlab/commit/847da6063b4c63c8133e5e5b5b45e5b4f004bdc4))

- Use raise..from for chained exceptions
  ([#939](https://github.com/python-gitlab/python-gitlab/pull/939),
  [`79fef26`](https://github.com/python-gitlab/python-gitlab/commit/79fef262c3e05ff626981c891d9377abb1e18533))

- **group**: Update group_manager attributes
  ([#1062](https://github.com/python-gitlab/python-gitlab/pull/1062),
  [`fa34f5e`](https://github.com/python-gitlab/python-gitlab/commit/fa34f5e20ecbd3f5d868df2fa9e399ac6559c5d5))

* chore(group): update group_manager attributes

Co-Authored-By: Nejc Habjan <hab.nejc@gmail.com>

- **mixins**: Factor out export download into ExportMixin
  ([`6ce5d1f`](https://github.com/python-gitlab/python-gitlab/commit/6ce5d1f14060a403f05993d77bf37720c25534ba))

### Documentation

- Add docs for Group Import/Export API
  ([`8c3d744`](https://github.com/python-gitlab/python-gitlab/commit/8c3d744ec6393ad536b565c94f120b3e26b6f3e8))

- Fix comment of prev_page()
  ([`b066b41`](https://github.com/python-gitlab/python-gitlab/commit/b066b41314f55fbdc4ee6868d1e0aba1e5620a48))

Co-Authored-By: Nejc Habjan <hab.nejc@gmail.com>

- Fix comment of prev_page()
  ([`ac6b2da`](https://github.com/python-gitlab/python-gitlab/commit/ac6b2daf8048f4f6dea14bbf142b8f3a00726443))

Co-Authored-By: Nejc Habjan <hab.nejc@gmail.com>

- Fix comment of prev_page()
  ([`7993c93`](https://github.com/python-gitlab/python-gitlab/commit/7993c935f62e67905af558dd06394764e708cafe))

### Features

- Add create from template args to ProjectManager
  ([`f493b73`](https://github.com/python-gitlab/python-gitlab/commit/f493b73e1fbd3c3f1a187fed2de26030f00a89c9))

This commit adds the v4 Create project attributes necessary to create a project from a project,
  instance, or group level template as documented in
  https://docs.gitlab.com/ee/api/projects.html#create-project

- Add support for commit GPG signature API
  ([`da7a809`](https://github.com/python-gitlab/python-gitlab/commit/da7a809772233be27fa8e563925dd2e44e1ce058))

- **api**: Add support for Gitlab Deploy Token API
  ([`01de524`](https://github.com/python-gitlab/python-gitlab/commit/01de524ce39a67b549b3157bf4de827dd0568d6b))

- **api**: Add support for Group Import/Export API
  ([#1037](https://github.com/python-gitlab/python-gitlab/pull/1037),
  [`6cb9d92`](https://github.com/python-gitlab/python-gitlab/commit/6cb9d9238ea3cc73689d6b71e991f2ec233ee8e6))

- **api**: Add support for remote mirrors API
  ([#1056](https://github.com/python-gitlab/python-gitlab/pull/1056),
  [`4cfaa2f`](https://github.com/python-gitlab/python-gitlab/commit/4cfaa2fd44b64459f6fc268a91d4469284c0e768))

### Testing

- Add unit tests for Project Export
  ([`600dc86`](https://github.com/python-gitlab/python-gitlab/commit/600dc86f34b6728b37a98b44e6aba73044bf3191))

- Add unit tests for Project Import
  ([`f7aad5f`](https://github.com/python-gitlab/python-gitlab/commit/f7aad5f78c49ad1a4e05a393bcf236b7bbad2f2a))

- Create separate module for commit tests
  ([`8c03771`](https://github.com/python-gitlab/python-gitlab/commit/8c037712a53c1c54e46298fbb93441d9b7a7144a))

- Move mocks to top of module
  ([`0bff713`](https://github.com/python-gitlab/python-gitlab/commit/0bff71353937a451b1092469330034062d24ff71))

- Prepare base project test class for more tests
  ([`915587f`](https://github.com/python-gitlab/python-gitlab/commit/915587f72de85b45880a2f1d50bdae1a61eb2638))

- **api**: Add tests for group export/import API
  ([`e7b2d6c`](https://github.com/python-gitlab/python-gitlab/commit/e7b2d6c873f0bfd502d06c9bd239cedc465e51c5))

- **types**: Reproduce get_for_api splitting strings
  ([#1057](https://github.com/python-gitlab/python-gitlab/pull/1057),
  [`babd298`](https://github.com/python-gitlab/python-gitlab/commit/babd298eca0586dce134d65586bf50410aacd035))


## v2.1.2 (2020-03-09)

### Chores

- Bump version to 2.1.2
  ([`ad7e2bf`](https://github.com/python-gitlab/python-gitlab/commit/ad7e2bf7472668ffdcc85eec30db4139b92595a6))


## v2.1.1 (2020-03-09)

### Bug Fixes

- **docs**: Additional project statistics example
  ([`5ae5a06`](https://github.com/python-gitlab/python-gitlab/commit/5ae5a0627f85abba23cda586483630cefa7cf36c))

### Chores

- Bump version to 2.1.1
  ([`6c5458a`](https://github.com/python-gitlab/python-gitlab/commit/6c5458a3bfc3208ad2d7cc40e1747f7715abe449))

- **user**: Update user attributes to 12.8
  ([`666f880`](https://github.com/python-gitlab/python-gitlab/commit/666f8806eb6b3455ea5531b08cdfc022916616f0))


## v2.1.0 (2020-03-08)

### Bug Fixes

- Do not require empty data dict for create()
  ([`99d959f`](https://github.com/python-gitlab/python-gitlab/commit/99d959f74d06cca8df3f2d2b3a4709faba7799cb))

- Remove null values from features POST data, because it fails
  ([`1ec1816`](https://github.com/python-gitlab/python-gitlab/commit/1ec1816d7c76ae079ad3b3e3b7a1bae70e0dd95b))

- Remove trailing slashes from base URL
  ([#913](https://github.com/python-gitlab/python-gitlab/pull/913),
  [`2e396e4`](https://github.com/python-gitlab/python-gitlab/commit/2e396e4a84690c2ea2ea7035148b1a6038c03301))

- Return response with commit data
  ([`b77b945`](https://github.com/python-gitlab/python-gitlab/commit/b77b945c7e0000fad4c422a5331c7e905e619a33))

- **docs**: Fix typo in user memberships example
  ([`33889bc`](https://github.com/python-gitlab/python-gitlab/commit/33889bcbedb4aa421ea5bf83c13abe3168256c62))

- **docs**: Update to new set approvers call for # of approvers
  ([`8e0c526`](https://github.com/python-gitlab/python-gitlab/commit/8e0c52620af47a9e2247eeb7dcc7a2e677822ff4))

to set the # of approvers for an MR you need to use the same function as for setting the approvers
  id.

- **docs and tests**: Update docs and tests for set_approvers
  ([`2cf12c7`](https://github.com/python-gitlab/python-gitlab/commit/2cf12c7973e139c4932da1f31c33bb7658b132f7))

Updated the docs with the new set_approvers arguments, and updated tests with the arg as well.

- **objects**: Add default name data and use http post
  ([`70c0cfb`](https://github.com/python-gitlab/python-gitlab/commit/70c0cfb686177bc17b796bf4d7eea8b784cf9651))

Updating approvers new api needs a POST call. Also It needs a name of the new rule, defaulting this
  to 'name'.

- **objects**: Update set_approvers function call
  ([`65ecadc`](https://github.com/python-gitlab/python-gitlab/commit/65ecadcfc724a7086e5f84dbf1ecc9f7a02e5ed8))

Added a miss paramter update to the set_approvers function

- **objects**: Update to new gitlab api for path, and args
  ([`e512cdd`](https://github.com/python-gitlab/python-gitlab/commit/e512cddd30f3047230e8eedb79d98dc06e93a77b))

Updated the gitlab path for set_approvers to approvers_rules, added default arg for rule type, and
  added arg for # of approvals required.

- **projects**: Correct copy-paste error
  ([`adc9101`](https://github.com/python-gitlab/python-gitlab/commit/adc91011e46dfce909b7798b1257819ec09d01bd))

### Chores

- Bump version to 2.1.0
  ([`47cb58c`](https://github.com/python-gitlab/python-gitlab/commit/47cb58c24af48c77c372210f9e791edd2c2c98b0))

- Ensure developers use same gitlab image as Travis
  ([`fab17fc`](https://github.com/python-gitlab/python-gitlab/commit/fab17fcd6258b8c3aa3ccf6c00ab7b048b6beeab))

- Fix broken requests links
  ([`b392c21`](https://github.com/python-gitlab/python-gitlab/commit/b392c21c669ae545a6a7492044479a401c0bcfb3))

Another case of the double slash rewrite.

### Code Style

- Fix black violations
  ([`ad3e833`](https://github.com/python-gitlab/python-gitlab/commit/ad3e833671c49db194c86e23981215b13b96bb1d))

### Documentation

- Add reference for REQUESTS_CA_BUNDLE
  ([`37e8d5d`](https://github.com/python-gitlab/python-gitlab/commit/37e8d5d2f0c07c797e347a7bc1441882fe118ecd))

- **pagination**: Clear up pagination docs
  ([`1609824`](https://github.com/python-gitlab/python-gitlab/commit/16098244ad7c19867495cf4f0fda0c83fe54cd2b))

Co-Authored-By: Mitar <mitar.git@tnode.com>

### Features

- Add capability to control GitLab features per project or group
  ([`7f192b4`](https://github.com/python-gitlab/python-gitlab/commit/7f192b4f8734e29a63f1c79be322c25d45cfe23f))

- Add support for commit revert API
  ([#991](https://github.com/python-gitlab/python-gitlab/pull/991),
  [`5298964`](https://github.com/python-gitlab/python-gitlab/commit/5298964ee7db8a610f23de2d69aad8467727ca97))

- Add support for user memberships API
  ([#1009](https://github.com/python-gitlab/python-gitlab/pull/1009),
  [`c313c2b`](https://github.com/python-gitlab/python-gitlab/commit/c313c2b01d796418539e42d578fed635f750cdc1))

- Use keyset pagination by default for `all=True`
  ([`99b4484`](https://github.com/python-gitlab/python-gitlab/commit/99b4484da924f9378518a1a1194e1a3e75b48073))

- **api**: Add support for GitLab OAuth Applications API
  ([`4e12356`](https://github.com/python-gitlab/python-gitlab/commit/4e12356d6da58c9ef3d8bf9ae67e8aef8fafac0a))

### Performance Improvements

- Prepare environment when gitlab is reconfigured
  ([`3834d9c`](https://github.com/python-gitlab/python-gitlab/commit/3834d9cf800a0659433eb640cb3b63a947f0ebda))

### Testing

- Add unit tests for base URLs with trailing slashes
  ([`32844c7`](https://github.com/python-gitlab/python-gitlab/commit/32844c7b27351b08bb86d8f9bd8fe9cf83917a5a))

- Add unit tests for revert commit API
  ([`d7a3066`](https://github.com/python-gitlab/python-gitlab/commit/d7a3066e03164af7f441397eac9e8cfef17c8e0c))

- Remove duplicate resp_get_project
  ([`cb43695`](https://github.com/python-gitlab/python-gitlab/commit/cb436951b1fde9c010e966819c75d0d7adacf17d))

- Use lazy object in unit tests
  ([`31c6562`](https://github.com/python-gitlab/python-gitlab/commit/31c65621ff592dda0ad3bf854db906beb8a48e9a))


## v2.0.1 (2020-02-05)

### Chores

- Bump to 2.1.0
  ([`a6c0660`](https://github.com/python-gitlab/python-gitlab/commit/a6c06609123a9f4cba1a8605b9c849e4acd69809))

There are a few more features in there

- Bump version to 2.0.1
  ([`8287a0d`](https://github.com/python-gitlab/python-gitlab/commit/8287a0d993a63501fc859702fc8079a462daa1bb))

- Revert to 2.0.1
  ([`272db26`](https://github.com/python-gitlab/python-gitlab/commit/272db2655d80fb81fbe1d8c56f241fe9f31b47e0))

I've misread the tag

- **user**: Update user attributes
  ([`27375f6`](https://github.com/python-gitlab/python-gitlab/commit/27375f6913547cc6e00084e5e77b0ad912b89910))

This also workarounds an GitLab issue, where private_profile, would reset to false if not supplied

### Documentation

- **auth**: Remove email/password auth
  ([`c9329bb`](https://github.com/python-gitlab/python-gitlab/commit/c9329bbf028c5e5ce175e99859c9e842ab8234bc))


## v2.0.0 (2020-01-26)

### Bug Fixes

- **projects**: Adjust snippets to match the API
  ([`e104e21`](https://github.com/python-gitlab/python-gitlab/commit/e104e213b16ca702f33962d770784f045f36cf10))

### Chores

- Add PyYaml as extra require
  ([`7ecd518`](https://github.com/python-gitlab/python-gitlab/commit/7ecd5184e62bf1b1f377db161b26fa4580af6b4c))

- Build_sphinx needs sphinx >= 1.7.6
  ([`528dfab`](https://github.com/python-gitlab/python-gitlab/commit/528dfab211936ee7794f9227311f04656a4d5252))

Stepping thru Sphinx versions from 1.6.5 to 1.7.5 build_sphinx fails. Once Sphinx == 1.7.6
  build_sphinx finished.

- Bump minimum required requests version
  ([`3f78aa3`](https://github.com/python-gitlab/python-gitlab/commit/3f78aa3c0d3fc502f295986d4951cfd0eee80786))

for security reasons

- Bump to 2.0.0
  ([`c817dcc`](https://github.com/python-gitlab/python-gitlab/commit/c817dccde8c104dcb294bbf1590c7e3ae9539466))

Dropping support for legacy python requires a new major version

- Drop legacy python tests
  ([`af8679a`](https://github.com/python-gitlab/python-gitlab/commit/af8679ac5c2c2b7774d624bdb1981d0e2374edc1))

Support dropped for: 2.7, 3.4, 3.5

- Enforce python version requirements
  ([`70176db`](https://github.com/python-gitlab/python-gitlab/commit/70176dbbb96a56ee7891885553eb13110197494c))

### Documentation

- Fix snippet get in project
  ([`3a4ff2f`](https://github.com/python-gitlab/python-gitlab/commit/3a4ff2fbf51d5f7851db02de6d8f0e84508b11a0))

- **projects**: Add raw file download docs
  ([`939e9d3`](https://github.com/python-gitlab/python-gitlab/commit/939e9d32e6e249e2a642d2bf3c1a34fde288c842))

Fixes #969

### Features

- Add appearance API
  ([`4c4ac5c`](https://github.com/python-gitlab/python-gitlab/commit/4c4ac5ca1e5cabc4ea4b12734a7b091bc4c224b5))

- Add autocompletion support
  ([`973cb8b`](https://github.com/python-gitlab/python-gitlab/commit/973cb8b962e13280bcc8473905227cf351661bf0))

- Add global order_by option to ease pagination
  ([`d187925`](https://github.com/python-gitlab/python-gitlab/commit/d1879253dae93e182710fe22b0a6452296e2b532))

- Support keyset pagination globally
  ([`0b71ba4`](https://github.com/python-gitlab/python-gitlab/commit/0b71ba4d2965658389b705c1bb0d83d1ff2ee8f2))

### Refactoring

- Remove six dependency
  ([`9fb4645`](https://github.com/python-gitlab/python-gitlab/commit/9fb46454c6dab1a86ab4492df2368ed74badf7d6))

- Support new list filters
  ([`bded2de`](https://github.com/python-gitlab/python-gitlab/commit/bded2de51951902444bc62aa016a3ad34aab799e))

This is most likely only useful for the CLI

### Testing

- Add project snippet tests
  ([`0952c55`](https://github.com/python-gitlab/python-gitlab/commit/0952c55a316fc8f68854badd68b4fc57658af9e7))

- Adjust functional tests for project snippets
  ([`ac0ea91`](https://github.com/python-gitlab/python-gitlab/commit/ac0ea91f22b08590f85a2b0ffc17cd41ae6e0ff7))


## v1.15.0 (2019-12-16)

### Bug Fixes

- Ignore all parameter, when as_list=True
  ([`137d72b`](https://github.com/python-gitlab/python-gitlab/commit/137d72b3bc00588f68ca13118642ecb5cd69e6ac))

Closes #962

### Chores

- Bump version to 1.15.0
  ([`2a01326`](https://github.com/python-gitlab/python-gitlab/commit/2a01326e8e02bbf418b3f4c49ffa60c735b107dc))

- **ci**: Use correct crane ci
  ([`18913dd`](https://github.com/python-gitlab/python-gitlab/commit/18913ddce18f78e7432f4d041ab4bd071e57b256))

### Code Style

- Format with the latest black version
  ([`06a8050`](https://github.com/python-gitlab/python-gitlab/commit/06a8050571918f0780da4c7d6ae514541118cf1a))

### Documentation

- Added docs for statistics
  ([`8c84cbf`](https://github.com/python-gitlab/python-gitlab/commit/8c84cbf6374e466f21d175206836672b3dadde20))

- **projects**: Fix file deletion docs
  ([`1c4f1c4`](https://github.com/python-gitlab/python-gitlab/commit/1c4f1c40185265ae73c52c6d6c418e02ab33204e))

The function `file.delete()` requires `branch` argument in addition to `commit_message`.

### Features

- Access project's issues statistics
  ([`482e57b`](https://github.com/python-gitlab/python-gitlab/commit/482e57ba716c21cd7b315e5803ecb3953c479b33))

Fixes #966

- Add support for /import/github
  ([`aa4d41b`](https://github.com/python-gitlab/python-gitlab/commit/aa4d41b70b2a66c3de5a7dd19b0f7c151f906630))

Addresses python-gitlab/python-gitlab#952

This adds a method to the `ProjectManager` called `import_github`, which maps to the
  `/import/github` API endpoint. Calling `import_github` will trigger an import operation from
  <repo_id> into <target_namespace>, using <personal_access_token> to authenticate against github.
  In practice a gitlab server may take many 10's of seconds to respond to this API call, so we also
  take the liberty of increasing the default timeout (only for this method invocation).

Unfortunately since `import` is a protected keyword in python, I was unable to follow the endpoint
  structure with the manager namespace. I'm open to suggestions on a more sensible interface.

I'm successfully using this addition to batch-import hundreds of github repositories into gitlab.

- Add variable_type to groups ci variables
  ([`0986c93`](https://github.com/python-gitlab/python-gitlab/commit/0986c93177cde1f3be77d4f73314c37b14bba011))

This adds the ci variables types for create/update requests.

See https://docs.gitlab.com/ee/api/group_level_variables.html#create-variable

- Add variable_type/protected to projects ci variables
  ([`4724c50`](https://github.com/python-gitlab/python-gitlab/commit/4724c50e9ec0310432c70f07079b1e03ab3cc666))

This adds the ci variables types and protected flag for create/update requests.

See https://docs.gitlab.com/ee/api/project_level_variables.html#create-variable

- Adding project stats
  ([`db0b00a`](https://github.com/python-gitlab/python-gitlab/commit/db0b00a905c14d52eaca831fcc9243f33d2f092d))

Fixes #967

- Allow cfg timeout to be overrided via kwargs
  ([`e9a8289`](https://github.com/python-gitlab/python-gitlab/commit/e9a8289a381ebde7c57aa2364258d84b4771d276))

On startup, the `timeout` parameter is loaded from config and stored on the base gitlab object
  instance. This instance parameter is used as the timeout for all API requests (it's passed into
  the `session` object when making HTTP calls).

This change allows any API method to specify a `timeout` argument to `**kwargs` that will override
  the global timeout value. This was somewhat needed / helpful for the `import_github` method.

I have also updated the docs accordingly.

- Nicer stacktrace
  ([`697cda2`](https://github.com/python-gitlab/python-gitlab/commit/697cda241509dd76adc1249b8029366cfc1d9d6e))

- Retry transient HTTP errors
  ([`59fe271`](https://github.com/python-gitlab/python-gitlab/commit/59fe2714741133989a7beed613f1eeb67c18c54e))

Fixes #970

### Testing

- Added tests for statistics
  ([`8760efc`](https://github.com/python-gitlab/python-gitlab/commit/8760efc89bac394b01218b48dd3fcbef30c8b9a2))

- Test that all is ignored, when as_list=False
  ([`b5e88f3`](https://github.com/python-gitlab/python-gitlab/commit/b5e88f3e99e2b07e0bafe7de33a8899e97c3bb40))


## v1.14.0 (2019-12-07)

### Bug Fixes

- Added missing attributes for project approvals
  ([`460ed63`](https://github.com/python-gitlab/python-gitlab/commit/460ed63c3dc4f966d6aae1415fdad6de125c6327))

Reference: https://docs.gitlab.com/ee/api/merge_request_approvals.html#change-configuration

Missing attributes: * merge_requests_author_approval * merge_requests_disable_committers_approval

- **labels**: Ensure label.save() works
  ([`727f536`](https://github.com/python-gitlab/python-gitlab/commit/727f53619dba47f0ab770e4e06f1cb774e14f819))

Otherwise, we get: File "gitlabracadabra/mixins/labels.py", line 67, in _process_labels
  current_label.save() File "gitlab/exceptions.py", line 267, in wrapped_f return f(*args, **kwargs)
  File "gitlab/v4/objects.py", line 896, in save self._update_attrs(server_data) File
  "gitlab/base.py", line 131, in _update_attrs self.__dict__["_attrs"].update(new_attrs) TypeError:
  'NoneType' object is not iterable

Because server_data is None.

- **project-fork**: Copy create fix from ProjectPipelineManager
  ([`516307f`](https://github.com/python-gitlab/python-gitlab/commit/516307f1cc9e140c7d85d0ed0c419679b314f80b))

- **project-fork**: Correct path computation for project-fork list
  ([`44a7c27`](https://github.com/python-gitlab/python-gitlab/commit/44a7c2788dd19c1fe73d7449bd7e1370816fd36d))

### Chores

- Bump version to 1.14.0
  ([`164fa4f`](https://github.com/python-gitlab/python-gitlab/commit/164fa4f360a1bb0ecf5616c32a2bc31c78c2594f))

- **ci**: Switch to crane docker image
  ([#944](https://github.com/python-gitlab/python-gitlab/pull/944),
  [`e0066b6`](https://github.com/python-gitlab/python-gitlab/commit/e0066b6b7c5ce037635f6a803ea26707d5684ef5))

### Documentation

- Add project and group cluster examples
  ([`d15801d`](https://github.com/python-gitlab/python-gitlab/commit/d15801d7e7742a43ad9517f0ac13b6dba24c6283))

- Fix typo
  ([`d9871b1`](https://github.com/python-gitlab/python-gitlab/commit/d9871b148c7729c9e401f43ff6293a5e65ce1838))

- **changelog**: Add notice for release-notes on Github
  ([#938](https://github.com/python-gitlab/python-gitlab/pull/938),
  [`de98e57`](https://github.com/python-gitlab/python-gitlab/commit/de98e572b003ee4cf2c1ef770a692f442c216247))

- **pipelines_and_jobs**: Add pipeline custom variables usage example
  ([`b275eb0`](https://github.com/python-gitlab/python-gitlab/commit/b275eb03c5954ca24f249efad8125d1eacadd3ac))

- **readme**: Fix Docker image reference
  ([`b9a40d8`](https://github.com/python-gitlab/python-gitlab/commit/b9a40d822bcff630a4c92c395c134f8c002ed1cb))

v1.8.0 is not available. ``` Unable to find image
  'registry.gitlab.com/python-gitlab/python-gitlab:v1.8.0' locally docker: Error response from
  daemon: manifest for registry.gitlab.com/python-gitlab/python-gitlab:v1.8.0 not found: manifest
  unknown: manifest unknown.

```

- **snippets**: Fix snippet docs
  ([`bbaa754`](https://github.com/python-gitlab/python-gitlab/commit/bbaa754673c4a0bffece482fe33e4875ddadc2dc))

Fixes #954

### Features

- Add audit endpoint
  ([`2534020`](https://github.com/python-gitlab/python-gitlab/commit/2534020b1832f28339ef466d6dd3edc21a521260))

- Add project and group clusters
  ([`ebd053e`](https://github.com/python-gitlab/python-gitlab/commit/ebd053e7bb695124c8117a95eab0072db185ddf9))

- Add support for include_subgroups filter
  ([`adbcd83`](https://github.com/python-gitlab/python-gitlab/commit/adbcd83fa172af2f3929ba063a0e780395b102d8))


## v1.13.0 (2019-11-02)

### Bug Fixes

- **projects**: Support `approval_rules` endpoint for projects
  ([`2cef2bb`](https://github.com/python-gitlab/python-gitlab/commit/2cef2bb40b1f37b97bb2ee9894ab3b9970cef231))

The `approvers` API endpoint is deprecated [1]. GitLab instead uses the `approval_rules` API
  endpoint to modify approval settings for merge requests. This adds the functionality for
  project-level merge request approval settings.

Note that there does not exist an endpoint to 'get' a single approval rule at this moment - only
  'list'.

[1] https://docs.gitlab.com/ee/api/merge_request_approvals.html

### Chores

- Bump version to 1.13.0
  ([`d0750bc`](https://github.com/python-gitlab/python-gitlab/commit/d0750bc01ed12952a4d259a13b3917fa404fd435))

- **ci**: Update latest docker image for every tag
  ([`01cbc7a`](https://github.com/python-gitlab/python-gitlab/commit/01cbc7ad04a875bea93a08c0ce563ab5b4fe896b))

- **dist**: Add test data
  ([`3133ed7`](https://github.com/python-gitlab/python-gitlab/commit/3133ed7d1df6f49de380b35331bbcc67b585a61b))

Closes #907

- **setup**: We support 3.8 ([#924](https://github.com/python-gitlab/python-gitlab/pull/924),
  [`6048175`](https://github.com/python-gitlab/python-gitlab/commit/6048175ef2c21fda298754e9b07515b0a56d66bd))

* chore(setup): we support 3.8

* style: format with black

### Documentation

- Projects get requires id
  ([`5bd8947`](https://github.com/python-gitlab/python-gitlab/commit/5bd8947bd16398aed218f07458aef72e67f2d130))

Also, add an example value for project_id to the other projects.get() example.

- **project**: Fix group project example
  ([`e680943`](https://github.com/python-gitlab/python-gitlab/commit/e68094317ff6905049e464a59731fe4ab23521de))

GroupManager.search is removed since 9a66d78, use list(search='keyword') instead

### Features

- Add deployment creation
  ([`ca256a0`](https://github.com/python-gitlab/python-gitlab/commit/ca256a07a2cdaf77a5c20e307d334b82fd0fe861))

Added in GitLab 12.4

Fixes #917

- Add users activate, deactivate functionality
  ([`32ad669`](https://github.com/python-gitlab/python-gitlab/commit/32ad66921e408f6553b9d60b6b4833ed3180f549))

These were introduced in GitLab 12.4

- Send python-gitlab version as user-agent
  ([`c22d49d`](https://github.com/python-gitlab/python-gitlab/commit/c22d49d084d1e03426cfab0d394330f8ab4bd85a))

- **auth**: Remove deprecated session auth
  ([`b751cdf`](https://github.com/python-gitlab/python-gitlab/commit/b751cdf424454d3859f3f038b58212e441faafaf))

- **doc**: Remove refs to api v3 in docs
  ([`6beeaa9`](https://github.com/python-gitlab/python-gitlab/commit/6beeaa993f8931d6b7fe682f1afed2bd4c8a4b73))

- **test**: Unused unittest2, type -> isinstance
  ([`33b1801`](https://github.com/python-gitlab/python-gitlab/commit/33b180120f30515d0f76fcf635cb8c76045b1b42))

### Testing

- Remove warning about open files from test_todo()
  ([`d6419aa`](https://github.com/python-gitlab/python-gitlab/commit/d6419aa86d6ad385e15d685bf47242bb6c67653e))

When running unittests python warns that the json file from test_todo() was still open. Use with to
  open, read, and create encoded json data that is used by resp_get_todo().

- **projects**: Support `approval_rules` endpoint for projects
  ([`94bac44`](https://github.com/python-gitlab/python-gitlab/commit/94bac4494353e4f597df0251f0547513c011e6de))


## v1.12.1 (2019-10-07)

### Bug Fixes

- Fix not working without auth
  ([`03b7b5b`](https://github.com/python-gitlab/python-gitlab/commit/03b7b5b07e1fd2872e8968dd6c29bc3161c6c43a))


## v1.12.0 (2019-10-06)

### Bug Fixes

- **cli**: Fix cli command user-project list
  ([`c17d7ce`](https://github.com/python-gitlab/python-gitlab/commit/c17d7ce14f79c21037808894d8c7ba1117779130))

- **labels**: Don't mangle label name on update
  ([`1fb6f73`](https://github.com/python-gitlab/python-gitlab/commit/1fb6f73f4d501c2b6c86c863d40481e1d7a707fe))

- **todo**: Mark_all_as_done doesn't return anything
  ([`5066e68`](https://github.com/python-gitlab/python-gitlab/commit/5066e68b398039beb5e1966ba1ed7684d97a8f74))

### Chores

- Bump to 1.12.0
  ([`4648128`](https://github.com/python-gitlab/python-gitlab/commit/46481283a9985ae1b07fe686ec4a34e4a1219b66))

- **ci**: Build test images on tag
  ([`0256c67`](https://github.com/python-gitlab/python-gitlab/commit/0256c678ea9593c6371ffff60663f83c423ca872))

### Code Style

- Format with black
  ([`fef085d`](https://github.com/python-gitlab/python-gitlab/commit/fef085dca35d6b60013d53a3723b4cbf121ab2ae))

### Documentation

- **project**: Add submodule docs
  ([`b5969a2`](https://github.com/python-gitlab/python-gitlab/commit/b5969a2dcea77fa608cc29be7a5f39062edd3846))

- **projects**: Add note about project list
  ([`44407c0`](https://github.com/python-gitlab/python-gitlab/commit/44407c0f59b9602b17cfb93b5e1fa37a84064766))

Fixes #795

- **repository-tags**: Fix typo
  ([`3024c5d`](https://github.com/python-gitlab/python-gitlab/commit/3024c5dc8794382e281b83a8266be7061069e83e))

Closes #879

- **todo**: Correct todo docs
  ([`d64edcb`](https://github.com/python-gitlab/python-gitlab/commit/d64edcb4851ea62e72e3808daf7d9b4fdaaf548b))

### Features

- Add support for job token
  ([`cef3aa5`](https://github.com/python-gitlab/python-gitlab/commit/cef3aa51a6928338c6755c3e6de78605fae8e59e))

See https://docs.gitlab.com/ee/api/jobs.html#get-job-artifacts for usage

- **ci**: Improve functionnal tests
  ([`eefceac`](https://github.com/python-gitlab/python-gitlab/commit/eefceace2c2094ef41d3da2bf3c46a58a450dcba))

- **project**: Add file blame api
  ([`f5b4a11`](https://github.com/python-gitlab/python-gitlab/commit/f5b4a113a298d33cb72f80c94d85bdfec3c4e149))

https://docs.gitlab.com/ee/api/repository_files.html#get-file-blame-from-repository

- **project**: Implement update_submodule
  ([`4d1e377`](https://github.com/python-gitlab/python-gitlab/commit/4d1e3774706f336e87ebe70e1b373ddb37f34b45))

- **user**: Add status api
  ([`62c9fe6`](https://github.com/python-gitlab/python-gitlab/commit/62c9fe63a47ddde2792a4a5e9cd1c7aa48661492))

### Refactoring

- Remove obsolete test image
  ([`a14c02e`](https://github.com/python-gitlab/python-gitlab/commit/a14c02ef85bd4d273b8c7f0f6bd07680c91955fa))

Follow up of #896

- Remove unused code, simplify string format
  ([`c7ff676`](https://github.com/python-gitlab/python-gitlab/commit/c7ff676c11303a00da3a570bf2893717d0391f20))

### Testing

- Re-enabled py_func_v4 test
  ([`49d84ba`](https://github.com/python-gitlab/python-gitlab/commit/49d84ba7e95fa343e622505380b3080279b83f00))

- **func**: Disable commit test
  ([`c9c76a2`](https://github.com/python-gitlab/python-gitlab/commit/c9c76a257d2ed3b394f499253d890c2dd9a01e24))

GitLab seems to be randomly failing here

- **status**: Add user status test
  ([`fec4f9c`](https://github.com/python-gitlab/python-gitlab/commit/fec4f9c23b8ba33bb49dca05d9c3e45cb727e0af))

- **submodules**: Correct test method
  ([`e59356f`](https://github.com/python-gitlab/python-gitlab/commit/e59356f6f90d5b01abbe54153441b6093834aa11))

- **todo**: Add unittests
  ([`7715567`](https://github.com/python-gitlab/python-gitlab/commit/77155678a5d8dbbf11d00f3586307694042d3227))


## v1.11.0 (2019-08-31)

### Bug Fixes

- Add project and group label update without id to fix cli
  ([`a3d0d7c`](https://github.com/python-gitlab/python-gitlab/commit/a3d0d7c1e7b259a25d9dc84c0b1de5362c80abb8))

- Remove empty dict default arguments
  ([`8fc8e35`](https://github.com/python-gitlab/python-gitlab/commit/8fc8e35c63d7ebd80408ae002693618ca16488a7))

Signed-off-by: Frantisek Lachman <flachman@redhat.com>

- Remove empty list default arguments
  ([`6e204ce`](https://github.com/python-gitlab/python-gitlab/commit/6e204ce819fc8bdd5359325ed7026a48d63f8103))

Signed-off-by: Frantisek Lachman <flachman@redhat.com>

- **projects**: Avatar uploading for projects
  ([`558ace9`](https://github.com/python-gitlab/python-gitlab/commit/558ace9b007ff9917734619c05a7c66008a4c3f0))

### Chores

- Bump package version
  ([`37542cd`](https://github.com/python-gitlab/python-gitlab/commit/37542cd28aa94ba01d5d289d950350ec856745af))

### Features

- Add methods to retrieve an individual project environment
  ([`29de40e`](https://github.com/python-gitlab/python-gitlab/commit/29de40ee6a20382c293d8cdc8d831b52ad56a657))

- Group labels with subscriptable mixin
  ([`4a9ef9f`](https://github.com/python-gitlab/python-gitlab/commit/4a9ef9f0fa26e01fc6c97cf88b2a162e21f61cce))

### Testing

- Add group label cli tests
  ([`f7f24bd`](https://github.com/python-gitlab/python-gitlab/commit/f7f24bd324eaf33aa3d1d5dd12719237e5bf9816))


## v1.10.0 (2019-07-22)

### Bug Fixes

- Convert # to %23 in URLs
  ([`14f5385`](https://github.com/python-gitlab/python-gitlab/commit/14f538501bfb47c92e02e615d0817675158db3cf))

Refactor a bit to handle this change, and add unit tests.

Closes #779

- Docker entry point argument passing
  ([`67ab637`](https://github.com/python-gitlab/python-gitlab/commit/67ab6371e69fbf137b95fd03105902206faabdac))

Fixes the problem of passing spaces in the arguments to the docker entrypoint.

Before this fix, there was virtually no way to pass spaces in arguments such as task description.

- Enable use of YAML in the CLI
  ([`ad0b476`](https://github.com/python-gitlab/python-gitlab/commit/ad0b47667f98760d6a802a9d08b2da8f40d13e87))

In order to use the YAML output, PyYaml needs to be installed on the docker image. This commit adds
  the installation to the dockerfile as a separate layer.

- Handle empty 'Retry-After' header from GitLab
  ([`7a3724f`](https://github.com/python-gitlab/python-gitlab/commit/7a3724f3fca93b4f55aed5132cf46d3718c4f594))

When requests are throttled (HTTP response code 429), python-gitlab assumed that 'Retry-After'
  existed in the response headers. This is not always the case and so the request fails due to a
  KeyError. The change in this commit adds a rudimentary exponential backoff to the 'http_request'
  method, which defaults to 10 retries but can be set to -1 to retry without bound.

- Improve pickle support
  ([`b4b5dec`](https://github.com/python-gitlab/python-gitlab/commit/b4b5decb7e49ac16d98d56547a874fb8f9d5492b))

- Pep8 errors
  ([`334f9ef`](https://github.com/python-gitlab/python-gitlab/commit/334f9efb18c95bb5df3271d26fa0a55b7aec1c7a))

Errors have not been detected by broken travis runs.

- Re-add merge request pipelines
  ([`877ddc0`](https://github.com/python-gitlab/python-gitlab/commit/877ddc0dbb664cd86e870bb81d46ca614770b50e))

- Remove decode() on error_message string
  ([`16bda20`](https://github.com/python-gitlab/python-gitlab/commit/16bda20514e036e51bef210b565671174cdeb637))

The integration tests failed because a test called 'decode()' on a string-type variable - the
  GitLabException class handles byte-to-string conversion already in its __init__. This commit
  removes the call to 'decode()' in the test.

``` Traceback (most recent call last): File "./tools/python_test_v4.py", line 801, in <module>
  assert 'Retry later' in error_message.decode() AttributeError: 'str' object has no attribute
  'decode'

```

- Use python2 compatible syntax for super
  ([`b08efcb`](https://github.com/python-gitlab/python-gitlab/commit/b08efcb9d155c20fa938534dd2d912f5191eede6))

- **api**: Avoid parameter conflicts with python and gitlab
  ([`4bd027a`](https://github.com/python-gitlab/python-gitlab/commit/4bd027aac41c41f7e22af93c7be0058d2faf7fb4))

Provide another way to send data to gitlab with a new `query_parameters` argument. This parameter
  can be used to explicitly define the dict of items to send to the server, so that **kwargs are
  only used to specify python-gitlab specific parameters.

Closes #566 Closes #629

- **api**: Don't try to parse raw downloads
  ([`35a6d85`](https://github.com/python-gitlab/python-gitlab/commit/35a6d85acea4776e9c4ad23ff75259481a6bcf8d))

http_get always tries to interpret the retrieved data if the content-type is json. In some cases
  (artifact download for instance) this is not the expected behavior.

This patch changes http_get and download methods to always get the raw data without parsing.

Closes #683

- **api**: Make *MemberManager.all() return a list of objects
  ([`d74ff50`](https://github.com/python-gitlab/python-gitlab/commit/d74ff506ca0aadaba3221fc54cbebb678240564f))

Fixes #699

- **api**: Make reset_time_estimate() work again
  ([`cb388d6`](https://github.com/python-gitlab/python-gitlab/commit/cb388d6e6d5ec6ef1746edfffb3449c17e31df34))

Closes #672

- **cli**: Allow --recursive parameter in repository tree
  ([`7969a78`](https://github.com/python-gitlab/python-gitlab/commit/7969a78ce8605c2b0195734e54c7d12086447304))

Fixes #718 Fixes #731

- **cli**: Don't fail when the short print attr value is None
  ([`8d1552a`](https://github.com/python-gitlab/python-gitlab/commit/8d1552a0ad137ca5e14fabfc75f7ca034c2a78ca))

Fixes #717 Fixes #727

- **cli**: Exit on config parse error, instead of crashing
  ([`6ad9da0`](https://github.com/python-gitlab/python-gitlab/commit/6ad9da04496f040ae7d95701422434bc935a5a80))

* Exit and hint user about possible errors * test: adjust test cases to config missing error

- **cli**: Fix update value for key not working
  ([`b766203`](https://github.com/python-gitlab/python-gitlab/commit/b7662039d191ebb6a4061c276e78999e2da7cd3f))

- **cli**: Print help and usage without config file
  ([`6bb4d17`](https://github.com/python-gitlab/python-gitlab/commit/6bb4d17a92832701b9f064a6577488cc42d20645))

Fixes #560

- **docker**: Use docker image with current sources
  ([`06e8ca8`](https://github.com/python-gitlab/python-gitlab/commit/06e8ca8747256632c8a159f760860b1ae8f2b7b5))

### Chores

- Add a tox job to run black
  ([`c27fa48`](https://github.com/python-gitlab/python-gitlab/commit/c27fa486698e441ebc16448ee93e5539cb885ced))

Allow lines to be 88 chars long for flake8.

- Bump package version to 1.10.0
  ([`c7c8470`](https://github.com/python-gitlab/python-gitlab/commit/c7c847056b6d24ba7a54b93837950b7fdff6c477))

- Disable failing travis test
  ([`515aa9a`](https://github.com/python-gitlab/python-gitlab/commit/515aa9ac2aba132d1dfde0418436ce163fca2313))

- Move checks back to travis
  ([`b764525`](https://github.com/python-gitlab/python-gitlab/commit/b7645251a0d073ca413bba80e87884cc236e63f2))

- Release tags to PyPI automatically
  ([`3133b48`](https://github.com/python-gitlab/python-gitlab/commit/3133b48a24ce3c9e2547bf2a679d73431dfbefab))

Fixes #609

- **ci**: Add automatic GitLab image pushes
  ([`95c9b6d`](https://github.com/python-gitlab/python-gitlab/commit/95c9b6dd489fc15c7dfceffca909917f4f3d4312))

- **ci**: Don't try to publish existing release
  ([`b4e818d`](https://github.com/python-gitlab/python-gitlab/commit/b4e818db7887ff1ec337aaf392b5719f3931bc61))

- **ci**: Fix gitlab PyPI publish
  ([`3e37df1`](https://github.com/python-gitlab/python-gitlab/commit/3e37df16e2b6a8f1beffc3a595abcb06fd48a17c))

- **ci**: Rebuild test image, when something changed
  ([`2fff260`](https://github.com/python-gitlab/python-gitlab/commit/2fff260a8db69558f865dda56f413627bb70d861))

- **ci**: Update the GitLab version in the test image
  ([`c410699`](https://github.com/python-gitlab/python-gitlab/commit/c41069992de392747ccecf8c282ac0549932ccd1))

- **ci**: Use reliable ci system
  ([`724a672`](https://github.com/python-gitlab/python-gitlab/commit/724a67211bc83d67deef856800af143f1dbd1e78))

- **setup**: Add 3.7 to supported python versions
  ([`b1525c9`](https://github.com/python-gitlab/python-gitlab/commit/b1525c9a4ca2d8c6c14d745638b3292a71763aeb))

- **tests**: Add rate limit tests
  ([`e216f06`](https://github.com/python-gitlab/python-gitlab/commit/e216f06d4d25d37a67239e93a8e2e400552be396))

### Code Style

- Format with black again
  ([`22b5082`](https://github.com/python-gitlab/python-gitlab/commit/22b50828d6936054531258f3dc17346275dd0aee))

### Documentation

- Add a note for python 3.5 for file content update
  ([`ca014f8`](https://github.com/python-gitlab/python-gitlab/commit/ca014f8c3e4877a4cc1ae04e1302fb57d39f47c4))

The data passed to the JSON serializer must be a string with python 3. Document this in the
  exemples.

Fix #175

- Add an example of trigger token usage
  ([`ea1eefe`](https://github.com/python-gitlab/python-gitlab/commit/ea1eefef2896420ae4e4d248155e4c5d33b4034e))

Closes #752

- Add ApplicationSettings API
  ([`ab7d794`](https://github.com/python-gitlab/python-gitlab/commit/ab7d794251bcdbafce69b1bde0628cd3b710d784))

- Add builds-related API docs
  ([`8e6a944`](https://github.com/python-gitlab/python-gitlab/commit/8e6a9442324926ed1dec0a8bfaf77792e4bdb10f))

- Add deploy keys API
  ([`ea089e0`](https://github.com/python-gitlab/python-gitlab/commit/ea089e092439a8fe95b50c3d0592358550389b51))

- Add labales API
  ([`31882b8`](https://github.com/python-gitlab/python-gitlab/commit/31882b8a57f3f4c7e4c4c4b319af436795ebafd3))

- Add licenses API
  ([`4540614`](https://github.com/python-gitlab/python-gitlab/commit/4540614a38067944c628505225bb15928d8e3c93))

- Add milestones API
  ([`7411907`](https://github.com/python-gitlab/python-gitlab/commit/74119073dae18214df1dd67ded6cd57abda335d4))

- Add missing =
  ([`391417c`](https://github.com/python-gitlab/python-gitlab/commit/391417cd47d722760dfdaab577e9f419c5dca0e0))

- Add missing requiredCreateAttrs
  ([`b08d74a`](https://github.com/python-gitlab/python-gitlab/commit/b08d74ac3efb505961971edb998ce430e430d652))

- Add MR API
  ([`5614a7c`](https://github.com/python-gitlab/python-gitlab/commit/5614a7c9bf62aede3804469b6781f45d927508ea))

- Add MR approvals in index
  ([`0b45afb`](https://github.com/python-gitlab/python-gitlab/commit/0b45afbeed13745a2f9d8a6ec7d09704a6ab44fb))

- Add pipeline deletion
  ([`2bb2571`](https://github.com/python-gitlab/python-gitlab/commit/2bb257182c237384d60b8d90cbbff5a0598f283b))

- Add project members doc
  ([`dcf31a4`](https://github.com/python-gitlab/python-gitlab/commit/dcf31a425217efebe56d4cbc8250dceb3844b2fa))

- Commits API
  ([`07c5594`](https://github.com/python-gitlab/python-gitlab/commit/07c55943eebb302bc1b8feaf482d929c83e9ebe1))

- Crossref improvements
  ([`6f9f42b`](https://github.com/python-gitlab/python-gitlab/commit/6f9f42b64cb82929af60e299c70773af6d406a6e))

- Do not use the :option: markup
  ([`368017c`](https://github.com/python-gitlab/python-gitlab/commit/368017c01f15013ab4cc9405c246a86e67f3b067))

- Document hooks API
  ([`b21dca0`](https://github.com/python-gitlab/python-gitlab/commit/b21dca0acb2c12add229a1742e0c552aa50618c1))

- Document projects API
  ([`967595f`](https://github.com/python-gitlab/python-gitlab/commit/967595f504b8de076ae9218a96c3b8dd6273b9d6))

- Fix "required" attribute
  ([`e64d0b9`](https://github.com/python-gitlab/python-gitlab/commit/e64d0b997776387f400eaec21c37ce6e58d49095))

- Fix invalid Raise attribute in docstrings
  ([`95a3fe6`](https://github.com/python-gitlab/python-gitlab/commit/95a3fe6907676109e1cd2f52ca8f5ad17e0d01d0))

- Fork relationship API
  ([`21f48b3`](https://github.com/python-gitlab/python-gitlab/commit/21f48b357130720551d5cccbc62f5275fe970378))

- Groups API documentation
  ([`4d871aa`](https://github.com/python-gitlab/python-gitlab/commit/4d871aadfaa9f57f5ae9f8b49f8367a5ef58545d))

- Improve the pagination section
  ([`29e2efe`](https://github.com/python-gitlab/python-gitlab/commit/29e2efeae22ce5fa82e3541360b234e0053a65c2))

- Issues API
  ([`41cbc32`](https://github.com/python-gitlab/python-gitlab/commit/41cbc32621004aab2cae5f7c14fc60005ef7b966))

- Notes API
  ([`3e026d2`](https://github.com/python-gitlab/python-gitlab/commit/3e026d2ee62eba3ad92ff2cdd53db19f5e0e9f6a))

- Project repository API
  ([`71a2a4f`](https://github.com/python-gitlab/python-gitlab/commit/71a2a4fb84321e73418fda1ce4e4d47177af928c))

- Project search API
  ([`e4cd04c`](https://github.com/python-gitlab/python-gitlab/commit/e4cd04c225e2160f02a8f292dbd4c0f6350769e4))

- Re-order api examples
  ([`5d149a2`](https://github.com/python-gitlab/python-gitlab/commit/5d149a2262653b729f0105639ae5027ae5a109ea))

`Pipelines and Jobs` and `Protected Branches` are out of order in contents and sometimes hard to
  find when looking for examples.

- Remove the build warning about _static
  ([`764d3ca`](https://github.com/python-gitlab/python-gitlab/commit/764d3ca0087f0536c48c9e1f60076af211138b9b))

- Remove v3 support
  ([`7927663`](https://github.com/python-gitlab/python-gitlab/commit/792766319f7c43004460fc9b975549be55430987))

- Repository files API
  ([`f00340f`](https://github.com/python-gitlab/python-gitlab/commit/f00340f72935b6fd80df7b62b811644b63049b5a))

- Snippets API
  ([`35b7f75`](https://github.com/python-gitlab/python-gitlab/commit/35b7f750c7e38a39cd4cb27195d9aa4807503b29))

- Start a FAQ
  ([`c305459`](https://github.com/python-gitlab/python-gitlab/commit/c3054592f79caa782ec79816501335e9a5c4e9ed))

- System hooks API
  ([`5c51bf3`](https://github.com/python-gitlab/python-gitlab/commit/5c51bf3d49302afe4725575a83d81a8c9eeb8779))

- Tags API
  ([`dd79eda`](https://github.com/python-gitlab/python-gitlab/commit/dd79eda78f91fc7e1e9a08b1e70ef48e3b4bb06d))

- Trigger_pipeline only accept branches and tags as ref
  ([`d63748a`](https://github.com/python-gitlab/python-gitlab/commit/d63748a41cc22bba93a9adf0812e7eb7b74a0161))

Fixes #430

- **api-usage**: Add rate limit documentation
  ([`ad4de20`](https://github.com/python-gitlab/python-gitlab/commit/ad4de20fe3a2fba2d35d4204bf5b0b7f589d4188))

- **api-usage**: Fix project group example
  ([`40a1bf3`](https://github.com/python-gitlab/python-gitlab/commit/40a1bf36c2df89daa1634e81c0635c1a63831090))

Fixes #798

- **cli**: Add PyYAML requirement notice
  ([`d29a489`](https://github.com/python-gitlab/python-gitlab/commit/d29a48981b521bf31d6f0304b88f39a63185328a))

Fixes #606

- **groups**: Fix typo
  ([`ac2d65a`](https://github.com/python-gitlab/python-gitlab/commit/ac2d65aacba5c19eca857290c5b47ead6bb4356d))

Fixes #635

- **projects**: Add mention about project listings
  ([`f604b25`](https://github.com/python-gitlab/python-gitlab/commit/f604b2577b03a6a19641db3f2060f99d24cc7073))

Having exactly 20 internal and 5 private projects in the group spent some time debugging this issue.

Hopefully that helped: https://github.com/python-gitlab/python-gitlab/issues/93

Imho should be definitely mention about `all=True` parameter.

- **projects**: Fix typo
  ([`c6bcfe6`](https://github.com/python-gitlab/python-gitlab/commit/c6bcfe6d372af6557547a408a8b0a39b909f0cdf))

- **projects**: Fix typo in code sample
  ([`b93f2a9`](https://github.com/python-gitlab/python-gitlab/commit/b93f2a9ea9661521878ac45d70c7bd9a5a470548))

Fixes #630

- **readme**: Add docs build information
  ([`6585c96`](https://github.com/python-gitlab/python-gitlab/commit/6585c967732fe2a53c6ad6d4d2ab39aaa68258b0))

- **readme**: Add more info about commitlint, code-format
  ([`286f703`](https://github.com/python-gitlab/python-gitlab/commit/286f7031ed542c97fb8792f61012d7448bee2658))

- **readme**: Fix six url
  ([`0bc30f8`](https://github.com/python-gitlab/python-gitlab/commit/0bc30f840c9c30dd529ae85bdece6262d2702c94))

six URL was pointing to 404

- **readme**: Provide commit message guidelines
  ([`bed8e1b`](https://github.com/python-gitlab/python-gitlab/commit/bed8e1ba80c73b1d976ec865756b62e66342ce32))

Fixes #660

- **setup**: Use proper readme on PyPI
  ([`6898097`](https://github.com/python-gitlab/python-gitlab/commit/6898097c45d53a3176882a3d9cb86c0015f8d491))

- **snippets**: Fix project-snippets layout
  ([`7feb97e`](https://github.com/python-gitlab/python-gitlab/commit/7feb97e9d89b4ef1401d141be3d00b9d0ff6b75c))

Fixes #828

### Features

- Add endpoint to get the variables of a pipeline
  ([`564de48`](https://github.com/python-gitlab/python-gitlab/commit/564de484f5ef4c76261057d3d2207dc747da020b))

It adds a new endpoint which was released in the Gitlab CE 11.11.

Signed-off-by: Agustin Henze <tin@redhat.com>

- Add mr rebase method
  ([`bc4280c`](https://github.com/python-gitlab/python-gitlab/commit/bc4280c2fbff115bd5e29a6f5012ae518610f626))

- Add support for board update
  ([`908d79f`](https://github.com/python-gitlab/python-gitlab/commit/908d79fa56965e7b3afcfa23236beef457cfa4b4))

Closes #801

- Add support for issue.related_merge_requests
  ([`90a3631`](https://github.com/python-gitlab/python-gitlab/commit/90a363154067bcf763043124d172eaf705c8fe90))

Closes #794

- Added approve & unapprove method for Mergerequests
  ([`53f7de7`](https://github.com/python-gitlab/python-gitlab/commit/53f7de7bfe0056950a8e7271632da3f89e3ba3b3))

Offical GitLab API supports this for GitLab EE

- Bump version to 1.9.0
  ([`aaed448`](https://github.com/python-gitlab/python-gitlab/commit/aaed44837869bd2ce22b6f0d2e1196b1d0e626a6))

- Get artifact by ref and job
  ([`cda1174`](https://github.com/python-gitlab/python-gitlab/commit/cda117456791977ad300a1dd26dec56009dac55e))

- Implement artifacts deletion
  ([`76b6e1f`](https://github.com/python-gitlab/python-gitlab/commit/76b6e1fc0f42ad00f21d284b4ca2c45d6020fd19))

Closes #744

- Obey the rate limit
  ([`2abf9ab`](https://github.com/python-gitlab/python-gitlab/commit/2abf9abacf834da797f2edf6866e12886d642b9d))

done by using the retry-after header

Fixes #166

- **GitLab Update**: Delete ProjectPipeline
  ([#736](https://github.com/python-gitlab/python-gitlab/pull/736),
  [`768ce19`](https://github.com/python-gitlab/python-gitlab/commit/768ce19c5e5bb197cddd4e3871c175e935c68312))

* feat(GitLab Update): delete ProjectPipeline

As of Gitlab 11.6 it is now possible to delete a pipeline -
  https://docs.gitlab.com/ee/api/pipelines.html#delete-a-pipeline

### Refactoring

- Format everything black
  ([`318d277`](https://github.com/python-gitlab/python-gitlab/commit/318d2770cbc90ae4d33170274e214b9d828bca43))

- Rename MASTER_ACCESS
  ([`c38775a`](https://github.com/python-gitlab/python-gitlab/commit/c38775a5d52620a9c2d506d7b0952ea7ef0a11fc))

to MAINTAINER_ACCESS to follow GitLab 11.0 docs

See: https://docs.gitlab.com/ce/user/permissions.html#project-members-permissions

### Testing

- Add project releases test
  ([`8ff8af0`](https://github.com/python-gitlab/python-gitlab/commit/8ff8af0d02327125fbfe1cfabe0a09f231e64788))

Fixes #762

- Always use latest version to test
  ([`82b0fc6`](https://github.com/python-gitlab/python-gitlab/commit/82b0fc6f3884f614912a6440f4676dfebee12d8e))

- Increase speed by disabling the rate limit faster
  ([`497f56c`](https://github.com/python-gitlab/python-gitlab/commit/497f56c3e1b276fb9499833da0cebfb3b756d03b))

- Minor test fixes
  ([`3b523f4`](https://github.com/python-gitlab/python-gitlab/commit/3b523f4c39ba4b3eacc9e76fcb22de7b426d2f45))

- Update the tests for GitLab 11.11
  ([`622854f`](https://github.com/python-gitlab/python-gitlab/commit/622854fc22c31eee988f8b7f59dbc033ff9393d6))

Changes in GitLab make the functional tests fail:

* Some actions add new notes and discussions: do not use hardcoded values in related listing asserts
  * The feature flag API is buggy (errors 500): disable the tests for now

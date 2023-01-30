# Changelog

<!--next-version-placeholder-->

## v3.13.0 (2023-01-30)
### Feature
* **group:** Add support for group restore API ([`9322db6`](https://github.com/python-gitlab/python-gitlab/commit/9322db663ecdaecf399e3192810d973c6a9a4020))
* **client:** Automatically retry on HTTP 409 Resource lock ([`dced76a`](https://github.com/python-gitlab/python-gitlab/commit/dced76a9900c626c9f0b90b85a5e371101a24fb4))
* **api:** Add support for bulk imports API ([`043de2d`](https://github.com/python-gitlab/python-gitlab/commit/043de2d265e0e5114d1cd901f82869c003413d9b))
* **api:** Add support for resource groups ([`5f8b8f5`](https://github.com/python-gitlab/python-gitlab/commit/5f8b8f5be901e944dfab2257f9e0cc4b2b1d2cd5))
* **api:** Support listing pipelines triggered by pipeline schedules ([`865fa41`](https://github.com/python-gitlab/python-gitlab/commit/865fa417a20163b526596549b9afbce679fc2817))
* Allow filtering pipelines by source ([`b6c0872`](https://github.com/python-gitlab/python-gitlab/commit/b6c08725042380d20ef5f09979bc29f2f6c1ab6f))
* **client:** Bootstrap the http backends concept ([#2391](https://github.com/python-gitlab/python-gitlab/issues/2391)) ([`91a665f`](https://github.com/python-gitlab/python-gitlab/commit/91a665f331c3ffc260db3470ad71fde0d3b56aa2))
* Add resource iteration events (see https://docs.gitlab.com/ee/api/resource_iteration_events.html) ([`ef5feb4`](https://github.com/python-gitlab/python-gitlab/commit/ef5feb4d07951230452a2974da729a958bdb9d6a))
* Allow passing kwargs to Gitlab class when instantiating with `from_config` ([#2392](https://github.com/python-gitlab/python-gitlab/issues/2392)) ([`e88d34e`](https://github.com/python-gitlab/python-gitlab/commit/e88d34e38dd930b00d7bb48f0e1c39420e09fa0f))
* Add keep_base_url when getting configuration from file ([`50a0301`](https://github.com/python-gitlab/python-gitlab/commit/50a03017f2ba8ec3252911dd1cf0ed7df42cfe50))

### Fix
* **client:** Regression - do not automatically get_next if page=# and ([`585e3a8`](https://github.com/python-gitlab/python-gitlab/commit/585e3a86c4cafa9ee73ed38676a78f3c34dbe6b2))
* Change return value to "None" in case getattr returns None to prevent error ([`3f86d36`](https://github.com/python-gitlab/python-gitlab/commit/3f86d36218d80b293b346b37f8be5efa6455d10c))
* **deps:** Bump requests-toolbelt to fix deprecation warning ([`faf842e`](https://github.com/python-gitlab/python-gitlab/commit/faf842e97d4858ff5ebd8ae6996e0cb3ca29881c))
* Use the ProjectIterationManager within the Project object ([`44f05dc`](https://github.com/python-gitlab/python-gitlab/commit/44f05dc017c5496e14db82d9650c6a0110b95cf9))
* **api:** Make description optional for releases ([`5579750`](https://github.com/python-gitlab/python-gitlab/commit/5579750335245011a3acb9456cb488f0fa1cda61))

### Documentation
* **faq:** Describe and group common errors ([`4c9a072`](https://github.com/python-gitlab/python-gitlab/commit/4c9a072b053f12f8098e4ea6fc47e3f6ab4f8b07))

## v3.12.0 (2022-11-28)
### Feature
* Add support for SAML group links ([#2367](https://github.com/python-gitlab/python-gitlab/issues/2367)) ([`1020ce9`](https://github.com/python-gitlab/python-gitlab/commit/1020ce965ff0cd3bfc283d4f0ad40e41e4d1bcee))
* **groups:** Add LDAP link manager and deprecate old API endpoints ([`3a61f60`](https://github.com/python-gitlab/python-gitlab/commit/3a61f601adaec7751cdcfbbcb88aa544326b1730))
* **groups:** Add support for listing ldap_group_links ([#2371](https://github.com/python-gitlab/python-gitlab/issues/2371)) ([`ad7c8fa`](https://github.com/python-gitlab/python-gitlab/commit/ad7c8fafd56866002aa6723ceeba4c4bc071ca0d))
* Implement secure files API ([`d0a0348`](https://github.com/python-gitlab/python-gitlab/commit/d0a034878fabfd8409134aa8b7ffeeb40219683c))
* **ci:** Re-Run Tests on PR Comment workflow ([`034cde3`](https://github.com/python-gitlab/python-gitlab/commit/034cde31c7017923923be29c3f34783937febc0f))
* **api:** Add support for getting a project's pull mirror details ([`060cfe1`](https://github.com/python-gitlab/python-gitlab/commit/060cfe1465a99657c5f832796ab3aa03aad934c7))
* **api:** Add support for remote project import from AWS S3 ([#2357](https://github.com/python-gitlab/python-gitlab/issues/2357)) ([`892281e`](https://github.com/python-gitlab/python-gitlab/commit/892281e35e3d81c9e43ff6a974f920daa83ea8b2))
* **api:** Add support for remote project import ([#2348](https://github.com/python-gitlab/python-gitlab/issues/2348)) ([`e5dc72d`](https://github.com/python-gitlab/python-gitlab/commit/e5dc72de9b3cdf0a7944ee0961fbdc6784c7f315))
* **api:** Add application statistics ([`6fcf3b6`](https://github.com/python-gitlab/python-gitlab/commit/6fcf3b68be095e614b969f5922ad8a67978cd4db))

### Fix
* **cli:** Enable debug before doing auth ([`65abb85`](https://github.com/python-gitlab/python-gitlab/commit/65abb85be7fc8ef57b295296111dac0a97ed1c49))
* **cli:** Expose missing mr_default_target_self project attribute ([`12aea32`](https://github.com/python-gitlab/python-gitlab/commit/12aea32d1c0f7e6eac0d19da580bf6efde79d3e2))
* Use POST method and return dict in `cancel_merge_when_pipeline_succeeds()` ([#2350](https://github.com/python-gitlab/python-gitlab/issues/2350)) ([`bd82d74`](https://github.com/python-gitlab/python-gitlab/commit/bd82d745c8ea9ff6ff078a4c961a2d6e64a2f63c))

### Documentation
* Use the term "log file" for getting a job log file ([`9d2b1ad`](https://github.com/python-gitlab/python-gitlab/commit/9d2b1ad10aaa78a5c28ece334293641c606291b5))
* **groups:** Describe GitLab.com group creation limitation ([`9bd433a`](https://github.com/python-gitlab/python-gitlab/commit/9bd433a3eb508b53fbca59f3f445da193522646a))
* **api:** Pushrules remove saying `None` is returned when not found ([`c3600b4`](https://github.com/python-gitlab/python-gitlab/commit/c3600b49e4d41b1c4f2748dd6f2a331c331d8706))

## v3.11.0 (2022-10-28)
### Feature
* **build:** Officially support Python 3.11 ([`74f66c7`](https://github.com/python-gitlab/python-gitlab/commit/74f66c71f3974cf68f5038f4fc3995e53d44aebe))
* **api:** Add support for topics merge API ([`9a6d197`](https://github.com/python-gitlab/python-gitlab/commit/9a6d197f9d2a88bdba8dab1f9abaa4e081a14792))

### Fix
* Remove `project.approvals.set_approvals()` method ([`91f08f0`](https://github.com/python-gitlab/python-gitlab/commit/91f08f01356ca5e38d967700a5da053f05b6fab0))
* Use epic id instead of iid for epic notes ([`97cae38`](https://github.com/python-gitlab/python-gitlab/commit/97cae38a315910972279f2d334e91fa54d9ede0c))
* **cli:** Handle list response for json/yaml output ([`9b88132`](https://github.com/python-gitlab/python-gitlab/commit/9b88132078ed37417c2a45369b4976c9c67f7882))
* Intermittent failure in test_merge_request_reset_approvals ([`3dde36e`](https://github.com/python-gitlab/python-gitlab/commit/3dde36eab40406948adca633f7197beb32b29552))

### Documentation
* **advanced:** Add hint on type narrowing ([`a404152`](https://github.com/python-gitlab/python-gitlab/commit/a40415290923d69d087dd292af902efbdfb5c258))
* Add minimal docs about the `enable_debug()` method ([`b4e9ab7`](https://github.com/python-gitlab/python-gitlab/commit/b4e9ab7ee395e575f17450c2dc0d519f7192e58e))
* **commits:** Fix commit create example for binary content ([`bcc1eb4`](https://github.com/python-gitlab/python-gitlab/commit/bcc1eb4571f76b3ca0954adb5525b26f05958e3f))
* **readme:** Add a basic feature list ([`b4d53f1`](https://github.com/python-gitlab/python-gitlab/commit/b4d53f1abb264cd9df8e4ac6560ab0895080d867))
* **api:** Describe use of lower-level methods ([`b7a6874`](https://github.com/python-gitlab/python-gitlab/commit/b7a687490d2690e6bd4706391199135e658e1dc6))
* **api:** Describe the list() and all() runners' functions ([`b6cc3f2`](https://github.com/python-gitlab/python-gitlab/commit/b6cc3f255532521eb259b42780354e03ce51458e))
* **api:** Update `merge_requests.rst`: `mr_id` to `mr_iid` ([`b32234d`](https://github.com/python-gitlab/python-gitlab/commit/b32234d1f8c4492b6b2474f91be9479ad23115bb))

## v3.10.0 (2022-09-28)
### Feature
* Add reset_approvals api ([`88693ff`](https://github.com/python-gitlab/python-gitlab/commit/88693ff2d6f4eecf3c79d017df52738886e2d636))
* Add support for deployment approval endpoint ([`9c9eeb9`](https://github.com/python-gitlab/python-gitlab/commit/9c9eeb901b1f3acd3fb0c4f24014ae2ed7c975ec))

### Fix
* **cli:** Add missing attributes for creating MRs ([`1714d0a`](https://github.com/python-gitlab/python-gitlab/commit/1714d0a980afdb648d203751dedf95ee95ac326e))
* **cli:** Add missing attribute for MR changes ([`20c46a0`](https://github.com/python-gitlab/python-gitlab/commit/20c46a0572d962f405041983e38274aeb79a12e4))

## v3.9.0 (2022-08-28)
### Feature
* Add support for merge_base API ([`dd4fbd5`](https://github.com/python-gitlab/python-gitlab/commit/dd4fbd5e43adbbc502624a8de0d30925d798dec0))

## v3.8.1 (2022-08-10)
### Fix
* **client:** Do not assume user attrs returned for auth() ([`a07547c`](https://github.com/python-gitlab/python-gitlab/commit/a07547cba981380935966dff2c87c2c27d6b18d9))

## v3.8.0 (2022-08-04)
### Feature
* **client:** Warn user on misconfigured URL in `auth()` ([`0040b43`](https://github.com/python-gitlab/python-gitlab/commit/0040b4337bae815cfe1a06f8371a7a720146f271))
* Support downloading archive subpaths ([`cadb0e5`](https://github.com/python-gitlab/python-gitlab/commit/cadb0e55347cdac149e49f611c99b9d53a105520))

### Fix
* **client:** Ensure encoded query params are never duplicated ([`1398426`](https://github.com/python-gitlab/python-gitlab/commit/1398426cd748fdf492fe6184b03ac2fcb7e4fd6e))
* Optionally keep user-provided base URL for pagination ([#2149](https://github.com/python-gitlab/python-gitlab/issues/2149)) ([`e2ea8b8`](https://github.com/python-gitlab/python-gitlab/commit/e2ea8b89a7b0aebdb1eb3b99196d7c0034076df8))

### Documentation
* Describe self-revoking personal access tokens ([`5ea48fc`](https://github.com/python-gitlab/python-gitlab/commit/5ea48fc3c28f872dd1184957a6f2385da075281c))

## v3.7.0 (2022-07-28)
### Feature
* Allow sort/ordering for project releases ([`b1dd284`](https://github.com/python-gitlab/python-gitlab/commit/b1dd284066b4b94482b9d41310ac48b75bcddfee))
* **cli:** Add a custom help formatter ([`005ba93`](https://github.com/python-gitlab/python-gitlab/commit/005ba93074d391f818c39e46390723a0d0d16098))
* Add support for iterations API ([`194ee01`](https://github.com/python-gitlab/python-gitlab/commit/194ee0100c2868c1a9afb161c15f3145efb01c7c))
* **groups:** Add support for shared projects API ([`66461ba`](https://github.com/python-gitlab/python-gitlab/commit/66461ba519a85bfbd3cba284a0c8de11a3ac7cde))
* **issues:** Add support for issue reorder API ([`8703324`](https://github.com/python-gitlab/python-gitlab/commit/8703324dc21a30757e15e504b7d20472f25d2ab9))
* **namespaces:** Add support for namespace existence API ([`4882cb2`](https://github.com/python-gitlab/python-gitlab/commit/4882cb22f55c41d8495840110be2d338b5545a04))
* Add support for group and project invitations API ([`7afd340`](https://github.com/python-gitlab/python-gitlab/commit/7afd34027a26b5238a979e3303d8e5d8a0320a07))
* **projects:** Add support for project restore API ([`4794ecc`](https://github.com/python-gitlab/python-gitlab/commit/4794ecc45d7aa08785c622918d08bb046e7359ae))
* Add support for filtering jobs by scope ([`0e1c0dd`](https://github.com/python-gitlab/python-gitlab/commit/0e1c0dd795886ae4741136e64c33850b164084a1))
* Add `asdict()` and `to_json()` methods to Gitlab Objects ([`08ac071`](https://github.com/python-gitlab/python-gitlab/commit/08ac071abcbc28af04c0fa655576e25edbdaa4e2))
* **api:** Add support for instance-level registry repositories ([`284d739`](https://github.com/python-gitlab/python-gitlab/commit/284d73950ad5cf5dfbdec2f91152ed13931bd0ee))
* **groups:** Add support for group-level registry repositories ([`70148c6`](https://github.com/python-gitlab/python-gitlab/commit/70148c62a3aba16dd8a9c29f15ed16e77c01a247))
* Add 'merge_pipelines_enabled' project attribute ([`fc33c93`](https://github.com/python-gitlab/python-gitlab/commit/fc33c934d54fb94451bd9b9ad65645c9c3d6fe2e))
* Support validating CI lint results ([`3b1ede4`](https://github.com/python-gitlab/python-gitlab/commit/3b1ede4a27cd730982d4c579437c5c689a8799e5))
* **cli:** Add support for global CI lint ([`3f67c4b`](https://github.com/python-gitlab/python-gitlab/commit/3f67c4b0fb0b9a39c8b93529a05b1541fcebcabe))
* **objects:** Add Project CI Lint support ([`b213dd3`](https://github.com/python-gitlab/python-gitlab/commit/b213dd379a4108ab32181b9d3700d2526d950916))
* Add support for group push rules ([`b5cdc09`](https://github.com/python-gitlab/python-gitlab/commit/b5cdc097005c8a48a16e793a69c343198b14e035))
* **api:** Add support for `get` for a MR approval rule ([`89c18c6`](https://github.com/python-gitlab/python-gitlab/commit/89c18c6255ec912db319f73f141b47ace87a713b))

### Fix
* Support array types for most resources ([`d9126cd`](https://github.com/python-gitlab/python-gitlab/commit/d9126cd802dd3cfe529fa940300113c4ead3054b))
* Use the [] after key names for array variables in `params` ([`1af44ce`](https://github.com/python-gitlab/python-gitlab/commit/1af44ce8761e6ee8a9467a3e192f6c4d19e5cefe))
* **runners:** Fix listing for /runners/all ([`c6dd57c`](https://github.com/python-gitlab/python-gitlab/commit/c6dd57c56e92abb6184badf4708f5f5e65c6d582))
* **config:** Raise error when gitlab id provided but no config section found ([`1ef7018`](https://github.com/python-gitlab/python-gitlab/commit/1ef70188da1e29cd8ba95bf58c994ba7dd3010c5))
* **config:** Raise error when gitlab id provided but no config file found ([`ac46c1c`](https://github.com/python-gitlab/python-gitlab/commit/ac46c1cb291c03ad14bc76f5f16c9f98f2a5a82d))
* Add `get_all` param (and `--get-all`) to allow passing `all` to API ([`7c71d5d`](https://github.com/python-gitlab/python-gitlab/commit/7c71d5db1199164b3fa9958e3c3bc6ec96efc78d))
* Results returned by `attributes` property to show updates ([`e5affc8`](https://github.com/python-gitlab/python-gitlab/commit/e5affc8749797293c1373c6af96334f194875038))
* Enable epic notes ([`5fc3216`](https://github.com/python-gitlab/python-gitlab/commit/5fc3216788342a2325662644b42e8c249b655ded))
* **cli:** Remove irrelevant MR approval rule list filters ([`0daec5f`](https://github.com/python-gitlab/python-gitlab/commit/0daec5fa1428a56a6a927b133613e8b296248167))
* Ensure path elements are escaped ([`5d9c198`](https://github.com/python-gitlab/python-gitlab/commit/5d9c198769b00c8e7661e62aaf5f930ed32ef829))

### Documentation
* **cli:** Showcase use of token scopes ([`4a6f8d6`](https://github.com/python-gitlab/python-gitlab/commit/4a6f8d67a94a3d104a24081ad1dbad5b2e3d9c3e))
* **projects:** Document export with upload to URL ([`03f5484`](https://github.com/python-gitlab/python-gitlab/commit/03f548453d84d99354aae7b638f5267e5d751c59))
* Describe fetching existing export status ([`9c5b8d5`](https://github.com/python-gitlab/python-gitlab/commit/9c5b8d54745a58b9fe72ba535b7868d1510379c0))
* **authors:** Add John ([`e2afb84`](https://github.com/python-gitlab/python-gitlab/commit/e2afb84dc4a259e8f40b7cc83e56289983c7db47))
* Document CI Lint usage ([`d5de4b1`](https://github.com/python-gitlab/python-gitlab/commit/d5de4b1fe38bedc07862bd9446dfd48b92cb078d))
* **users:** Add docs about listing a user's projects ([`065a1a5`](https://github.com/python-gitlab/python-gitlab/commit/065a1a5a32d34286df44800084285b30b934f911))
* Update return type of pushrules ([`53cbecc`](https://github.com/python-gitlab/python-gitlab/commit/53cbeccd581318ce4ff6bec0acf3caf935bda0cf))
* Describe ROPC flow in place of password authentication ([`91c17b7`](https://github.com/python-gitlab/python-gitlab/commit/91c17b704f51e9a06b241d549f9a07a19c286118))
* **readme:** Remove redundant `-v` that breaks the command ([`c523e18`](https://github.com/python-gitlab/python-gitlab/commit/c523e186cc48f6bcac5245e3109b50a3852d16ef))

## v3.6.0 (2022-06-28)
### Feature
* **downloads:** Allow streaming downloads access to response iterator ([#1956](https://github.com/python-gitlab/python-gitlab/issues/1956)) ([`b644721`](https://github.com/python-gitlab/python-gitlab/commit/b6447211754e126f64e12fc735ad74fe557b7fb4))
* **api:** Support head() method for get and list endpoints ([`ce9216c`](https://github.com/python-gitlab/python-gitlab/commit/ce9216ccc542d834be7f29647c7ee98c2ca5bb01))
* **api:** Implement HEAD method ([`90635a7`](https://github.com/python-gitlab/python-gitlab/commit/90635a7db3c9748745471d2282260418e31c7797))
* **users:** Add approve and reject methods to User ([`f57139d`](https://github.com/python-gitlab/python-gitlab/commit/f57139d8f1dafa6eb19d0d954b3634c19de6413c))
* **api:** Convert gitlab.const to Enums ([`c3c6086`](https://github.com/python-gitlab/python-gitlab/commit/c3c6086c548c03090ccf3f59410ca3e6b7999791))
* Add support for Protected Environments ([`1dc9d0f`](https://github.com/python-gitlab/python-gitlab/commit/1dc9d0f91757eed9f28f0c7172654b9b2a730216))
* **users:** Add ban and unban methods ([`0d44b11`](https://github.com/python-gitlab/python-gitlab/commit/0d44b118f85f92e7beb1a05a12bdc6e070dce367))
* **docker:** Provide a Debian-based slim image ([`384031c`](https://github.com/python-gitlab/python-gitlab/commit/384031c530e813f55da52f2b2c5635ea935f9d91))
* Support mutually exclusive attributes and consolidate validation to fix board lists ([#2037](https://github.com/python-gitlab/python-gitlab/issues/2037)) ([`3fa330c`](https://github.com/python-gitlab/python-gitlab/commit/3fa330cc341bbedb163ba757c7f6578d735c6efb))
* **client:** Introduce `iterator=True` and deprecate `as_list=False` in `list()` ([`cdc6605`](https://github.com/python-gitlab/python-gitlab/commit/cdc6605767316ea59e1e1b849683be7b3b99e0ae))

### Fix
* **base:** Do not fail repr() on lazy objects ([`1efb123`](https://github.com/python-gitlab/python-gitlab/commit/1efb123f63eab57600228b75a1744f8787c16671))
* **cli:** Project-merge-request-approval-rule ([`15a242c`](https://github.com/python-gitlab/python-gitlab/commit/15a242c3303759b77b380c5b3ff9d1e0bf2d800c))
* **cli:** Fix project export download for CLI ([`5d14867`](https://github.com/python-gitlab/python-gitlab/commit/5d1486785793b02038ac6f527219801744ee888b))

### Documentation
* **api:** Add separate section for advanced usage ([`22ae101`](https://github.com/python-gitlab/python-gitlab/commit/22ae1016f39256b8e2ca02daae8b3c7130aeb8e6))
* **api:** Document usage of head() methods ([`f555bfb`](https://github.com/python-gitlab/python-gitlab/commit/f555bfb363779cc6c8f8036f6d6cfa302e15d4fe))
* **projects:** Provide more detailed import examples ([`8f8611a`](https://github.com/python-gitlab/python-gitlab/commit/8f8611a1263b8c19fd19ce4a904a310b0173b6bf))
* **projects:** Document 404 gotcha with unactivated integrations ([`522ecff`](https://github.com/python-gitlab/python-gitlab/commit/522ecffdb6f07e6c017139df4eb5d3fc42a585b7))
* **variables:** Instruct users to follow GitLab rules for values ([`194b6be`](https://github.com/python-gitlab/python-gitlab/commit/194b6be7ccec019fefc04754f98b9ec920c29568))
* **api:** Stop linking to python-requests.org ([`49c7e83`](https://github.com/python-gitlab/python-gitlab/commit/49c7e83f768ee7a3fec19085a0fa0a67eadb12df))
* **api:** Fix incorrect docs for merge_request_approvals ([#2094](https://github.com/python-gitlab/python-gitlab/issues/2094)) ([`5583eaa`](https://github.com/python-gitlab/python-gitlab/commit/5583eaa108949386c66290fecef4d064f44b9e83))
* **api-usage:** Add import os in example ([`2194a44`](https://github.com/python-gitlab/python-gitlab/commit/2194a44be541e9d2c15d3118ba584a4a173927a2))
* Drop deprecated setuptools build_sphinx ([`048d66a`](https://github.com/python-gitlab/python-gitlab/commit/048d66af51cef385b22d223ed2a5cd30e2256417))
* **usage:** Refer to upsteam docs instead of custom attributes ([`ae7d3b0`](https://github.com/python-gitlab/python-gitlab/commit/ae7d3b09352b2a1bd287f95d4587b04136c7a4ed))
* **ext:** Fix rendering for RequiredOptional dataclass ([`4d431e5`](https://github.com/python-gitlab/python-gitlab/commit/4d431e5a6426d0fd60945c2d1ff00a00a0a95b6c))
* Documentation updates to reflect addition of mutually exclusive attributes ([`24b720e`](https://github.com/python-gitlab/python-gitlab/commit/24b720e49636044f4be7e4d6e6ce3da341f2aeb8))
* Use `as_list=False` or `all=True` in Getting started ([`de8c6e8`](https://github.com/python-gitlab/python-gitlab/commit/de8c6e80af218d93ca167f8b5ff30319a2781d91))

## v3.5.0 (2022-05-28)
### Feature
* **objects:** Support get project storage endpoint ([`8867ee5`](https://github.com/python-gitlab/python-gitlab/commit/8867ee59884ae81d6457ad6e561a0573017cf6b2))
* Display human-readable attribute in `repr()` if present ([`6b47c26`](https://github.com/python-gitlab/python-gitlab/commit/6b47c26d053fe352d68eb22a1eaf4b9a3c1c93e7))
* **ux:** Display project.name_with_namespace on project repr ([`e598762`](https://github.com/python-gitlab/python-gitlab/commit/e5987626ca1643521b16658555f088412be2a339))

### Fix
* **cli:** Changed default `allow_abbrev` value to fix arguments collision problem ([#2013](https://github.com/python-gitlab/python-gitlab/issues/2013)) ([`d68cacf`](https://github.com/python-gitlab/python-gitlab/commit/d68cacfeda5599c62a593ecb9da2505c22326644))
* Duplicate subparsers being added to argparse ([`f553fd3`](https://github.com/python-gitlab/python-gitlab/commit/f553fd3c79579ab596230edea5899dc5189b0ac6))

### Documentation
* Update issue example and extend API usage docs ([`aad71d2`](https://github.com/python-gitlab/python-gitlab/commit/aad71d282d60dc328b364bcc951d0c9b44ab13fa))
* **CONTRIBUTING.rst:** Fix link to conventional-changelog commit format documentation ([`2373a4f`](https://github.com/python-gitlab/python-gitlab/commit/2373a4f13ee4e5279a424416cdf46782a5627067))
* Add missing Admin access const value ([`3e0d4d9`](https://github.com/python-gitlab/python-gitlab/commit/3e0d4d9006e2ca6effae2b01cef3926dd0850e52))
* **merge_requests:** Add new possible merge request state and link to the upstream docs ([`e660fa8`](https://github.com/python-gitlab/python-gitlab/commit/e660fa8386ed7783da5c076bc0fef83e6a66f9a8))

## v3.4.0 (2022-04-28)
### Feature
* Emit a warning when using a `list()` method returns max ([`1339d64`](https://github.com/python-gitlab/python-gitlab/commit/1339d645ce58a2e1198b898b9549ba5917b1ff12))
* **objects:** Support getting project/group deploy tokens by id ([`fcd37fe`](https://github.com/python-gitlab/python-gitlab/commit/fcd37feff132bd5b225cde9d5f9c88e62b3f1fd6))
* **user:** Support getting user SSH key by id ([`6f93c05`](https://github.com/python-gitlab/python-gitlab/commit/6f93c0520f738950a7c67dbeca8d1ac8257e2661))
* **api:** Re-add topic delete endpoint ([`d1d96bd`](https://github.com/python-gitlab/python-gitlab/commit/d1d96bda5f1c6991c8ea61dca8f261e5b74b5ab6))

### Fix
* Add ChunkedEncodingError to list of retryable exceptions ([`7beb20f`](https://github.com/python-gitlab/python-gitlab/commit/7beb20ff7b7b85fb92fc6b647d9c1bdb7568f27c))
* Avoid passing redundant arguments to API ([`3431887`](https://github.com/python-gitlab/python-gitlab/commit/34318871347b9c563d01a13796431c83b3b1d58c))
* **cli:** Add missing filters for project commit list ([`149d244`](https://github.com/python-gitlab/python-gitlab/commit/149d2446fcc79b31d3acde6e6d51adaf37cbb5d3))
* Add 52x range to retry transient failures and tests ([`c3ef1b5`](https://github.com/python-gitlab/python-gitlab/commit/c3ef1b5c1eaf1348a18d753dbf7bda3c129e3262))
* Also retry HTTP-based transient errors ([`3b49e4d`](https://github.com/python-gitlab/python-gitlab/commit/3b49e4d61e6f360f1c787aa048edf584aec55278))

### Documentation
* **api-docs:** Docs fix for application scopes ([`e1ad93d`](https://github.com/python-gitlab/python-gitlab/commit/e1ad93df90e80643866611fe52bd5c59428e7a88))

## v3.3.0 (2022-03-28)
### Feature
* **object:** Add pipeline test report summary support ([`a97e0cf`](https://github.com/python-gitlab/python-gitlab/commit/a97e0cf81b5394b3a2b73d927b4efe675bc85208))

### Fix
* Support RateLimit-Reset header ([`4060146`](https://github.com/python-gitlab/python-gitlab/commit/40601463c78a6f5d45081700164899b2559b7e55))

### Documentation
* Fix typo and incorrect style ([`2828b10`](https://github.com/python-gitlab/python-gitlab/commit/2828b10505611194bebda59a0e9eb41faf24b77b))
* Add pipeline test report summary support ([`d78afb3`](https://github.com/python-gitlab/python-gitlab/commit/d78afb36e26f41d727dee7b0952d53166e0df850))
* **chore:** Include docs .js files in sdist ([`3010b40`](https://github.com/python-gitlab/python-gitlab/commit/3010b407bc9baabc6cef071507e8fa47c0f1624d))

## v3.2.0 (2022-02-28)
### Feature
* **merge_request_approvals:** Add support for deleting MR approval rules ([`85a734f`](https://github.com/python-gitlab/python-gitlab/commit/85a734fec3111a4a5c4f0ddd7cb36eead96215e9))
* **artifacts:** Add support for project artifacts delete API ([`c01c034`](https://github.com/python-gitlab/python-gitlab/commit/c01c034169789e1d20fd27a0f39f4c3c3628a2bb))
* **mixins:** Allow deleting resources without IDs ([`0717517`](https://github.com/python-gitlab/python-gitlab/commit/0717517212b616cfd52cfd38dd5c587ff8f9c47c))
* **objects:** Add a complete artifacts manager ([`c8c2fa7`](https://github.com/python-gitlab/python-gitlab/commit/c8c2fa763558c4d9906e68031a6602e007fec930))

### Fix
* **services:** Use slug for id_attr instead of custom methods ([`e30f39d`](https://github.com/python-gitlab/python-gitlab/commit/e30f39dff5726266222b0f56c94f4ccfe38ba527))
* Remove custom `delete` method for labels ([`0841a2a`](https://github.com/python-gitlab/python-gitlab/commit/0841a2a686c6808e2f3f90960e529b26c26b268f))

### Documentation
* Enable gitter chat directly in docs ([`bd1ecdd`](https://github.com/python-gitlab/python-gitlab/commit/bd1ecdd5ad654b01b34e7a7a96821cc280b3ca67))
* Add delete methods for runners and project artifacts ([`5e711fd`](https://github.com/python-gitlab/python-gitlab/commit/5e711fdb747fb3dcde1f5879c64dfd37bf25f3c0))
* Add retry_transient infos ([`bb1f054`](https://github.com/python-gitlab/python-gitlab/commit/bb1f05402887c78f9898fbd5bd66e149eff134d9))
* Add transient errors retry info ([`b7a1266`](https://github.com/python-gitlab/python-gitlab/commit/b7a126661175a3b9b73dbb4cb88709868d6d871c))
* **artifacts:** Deprecate artifacts() and artifact() methods ([`64d01ef`](https://github.com/python-gitlab/python-gitlab/commit/64d01ef23b1269b705350106d8ddc2962a780dce))
* Revert "chore: add temporary banner for v3" ([#1864](https://github.com/python-gitlab/python-gitlab/issues/1864)) ([`7a13b9b`](https://github.com/python-gitlab/python-gitlab/commit/7a13b9bfa4aead6c731f9a92e0946dba7577c61b))

## v3.1.1 (2022-01-28)
### Fix
* **cli:** Make 'per_page' and 'page' type explicit ([`d493a5e`](https://github.com/python-gitlab/python-gitlab/commit/d493a5e8685018daa69c92e5942cbe763e5dac62))
* **cli:** Make 'timeout' type explicit ([`bbb7df5`](https://github.com/python-gitlab/python-gitlab/commit/bbb7df526f4375c438be97d8cfa0d9ea9d604e7d))
* **cli:** Allow custom methods in managers ([`8dfed0c`](https://github.com/python-gitlab/python-gitlab/commit/8dfed0c362af2c5e936011fd0b488b8b05e8a8a0))
* **objects:** Make resource access tokens and repos available in CLI ([`e0a3a41`](https://github.com/python-gitlab/python-gitlab/commit/e0a3a41ce60503a25fa5c26cf125364db481b207))

### Documentation
* Enhance release docs for CI_JOB_TOKEN usage ([`5d973de`](https://github.com/python-gitlab/python-gitlab/commit/5d973de8a5edd08f38031cf9be2636b0e12f008d))
* **changelog:** Add missing changelog items ([`01755fb`](https://github.com/python-gitlab/python-gitlab/commit/01755fb56a5330aa6fa4525086e49990e57ce50b))

## v3.1.0 (2022-01-14)
### Feature
* add support for Group Access Token API ([`c01b7c4`](https://github.com/python-gitlab/python-gitlab/commit/c01b7c494192c5462ec673848287ef2a5c9bd737))
* Add support for Groups API method `transfer()` ([`0007006`](https://github.com/python-gitlab/python-gitlab/commit/0007006c184c64128caa96b82dafa3db0ea1101f))
* **api:** Add `project.transfer()` and deprecate `transfer_project()` ([`259668a`](https://github.com/python-gitlab/python-gitlab/commit/259668ad8cb54348e4a41143a45f899a222d2d35))
* **api:** Return result from `SaveMixin.save()` ([`e6258a4`](https://github.com/python-gitlab/python-gitlab/commit/e6258a4193a0e8d0c3cf48de15b926bebfa289f3))

### Fix
* **cli:** Add missing list filters for environments ([`6f64d40`](https://github.com/python-gitlab/python-gitlab/commit/6f64d4098ed4a890838c6cf43d7a679e6be4ac6c))
* Use url-encoded ID in all paths ([`12435d7`](https://github.com/python-gitlab/python-gitlab/commit/12435d74364ca881373d690eab89d2e2baa62a49))
* **members:** Use new *All objects for *AllManager managers ([`755e0a3`](https://github.com/python-gitlab/python-gitlab/commit/755e0a32e8ca96a3a3980eb7d7346a1a899ad58b))
* **api:** Services: add missing `lazy` parameter ([`888f332`](https://github.com/python-gitlab/python-gitlab/commit/888f3328d3b1c82a291efbdd9eb01f11dff0c764))
* broken URL for FAQ about attribute-error-list ([`1863f30`](https://github.com/python-gitlab/python-gitlab/commit/1863f30ea1f6fb7644b3128debdbb6b7bb218836))
* remove default arguments for mergerequests.merge() ([`8e589c4`](https://github.com/python-gitlab/python-gitlab/commit/8e589c43fa2298dc24b97423ffcc0ce18d911e3b))
* remove custom URL encoding ([`3d49e5e`](https://github.com/python-gitlab/python-gitlab/commit/3d49e5e6a2bf1c9a883497acb73d7ce7115b804d))

### Documentation
* **cli:** make examples more easily navigable by generating TOC ([`f33c523`](https://github.com/python-gitlab/python-gitlab/commit/f33c5230cb25c9a41e9f63c0846c1ecba7097ee7))
* update project access token API reference link ([`73ae955`](https://github.com/python-gitlab/python-gitlab/commit/73ae9559dc7f4fba5c80862f0f253959e60f7a0c))

## v3.0.0 (2022-01-05)
### Feature
* **docker:** Remove custom entrypoint from image ([`80754a1`](https://github.com/python-gitlab/python-gitlab/commit/80754a17f66ef4cd8469ff0857e0fc592c89796d))
* **cli:** Allow options from args and environment variables ([`ca58008`](https://github.com/python-gitlab/python-gitlab/commit/ca58008607385338aaedd14a58adc347fa1a41a0))
* **api:** Support file format for repository archive ([`83dcabf`](https://github.com/python-gitlab/python-gitlab/commit/83dcabf3b04af63318c981317778f74857279909))
* Add support for `squash_option` in Projects ([`a246ce8`](https://github.com/python-gitlab/python-gitlab/commit/a246ce8a942b33c5b23ac075b94237da09013fa2))
* **cli:** Do not require config file to run CLI ([`92a893b`](https://github.com/python-gitlab/python-gitlab/commit/92a893b8e230718436582dcad96175685425b1df))
* **api:** Add support for Topics API ([`e7559bf`](https://github.com/python-gitlab/python-gitlab/commit/e7559bfa2ee265d7d664d7a18770b0a3e80cf999))
* Add delete on package_file object ([`124667b`](https://github.com/python-gitlab/python-gitlab/commit/124667bf16b1843ae52e65a3cc9b8d9235ff467e))
* Add support for `projects.groups.list()` ([`68ff595`](https://github.com/python-gitlab/python-gitlab/commit/68ff595967a5745b369a93d9d18fef48b65ebedb))
* **api:** Add support for epic notes ([`7f4edb5`](https://github.com/python-gitlab/python-gitlab/commit/7f4edb53e9413f401c859701d8c3bac4a40706af))
* Remove support for Python 3.6, require 3.7 or higher ([`414009d`](https://github.com/python-gitlab/python-gitlab/commit/414009daebe19a8ae6c36f050dffc690dff40e91))
* **api:** Add project milestone promotion ([`f068520`](https://github.com/python-gitlab/python-gitlab/commit/f0685209f88d1199873c1f27d27f478706908fd3))
* **api:** Add merge trains ([`fd73a73`](https://github.com/python-gitlab/python-gitlab/commit/fd73a738b429be0a2642d5b777d5e56a4c928787))
* **api:** Add merge request approval state ([`f41b093`](https://github.com/python-gitlab/python-gitlab/commit/f41b0937aec5f4a5efba44155cc2db77c7124e5e))
* **api:** Add project label promotion ([`6d7c88a`](https://github.com/python-gitlab/python-gitlab/commit/6d7c88a1fe401d271a34df80943634652195b140))
* **objects:** Support delete package files API ([`4518046`](https://github.com/python-gitlab/python-gitlab/commit/45180466a408cd51c3ea4fead577eb0e1f3fe7f8))
* **objects:** List starred projects of a user ([`47a5606`](https://github.com/python-gitlab/python-gitlab/commit/47a56061421fc8048ee5cceaf47ac031c92aa1da))
* **build:** Officially support and test python 3.10 ([`c042ddc`](https://github.com/python-gitlab/python-gitlab/commit/c042ddc79ea872fc8eb8fe4e32f4107a14ffed2d))
* **objects:** Support Create and Revoke personal access token API ([`e19314d`](https://github.com/python-gitlab/python-gitlab/commit/e19314dcc481b045ba7a12dd76abedc08dbdf032))
* Default to gitlab.com if no URL given ([`8236281`](https://github.com/python-gitlab/python-gitlab/commit/823628153ec813c4490e749e502a47716425c0f1))
* Allow global retry_transient_errors setup ([`3b1d3a4`](https://github.com/python-gitlab/python-gitlab/commit/3b1d3a41da7e7228f3a465d06902db8af564153e))

### Fix
* Handle situation where GitLab does not return values ([`cb824a4`](https://github.com/python-gitlab/python-gitlab/commit/cb824a49af9b0d155b89fe66a4cfebefe52beb7a))
* Stop encoding '.' to '%2E' ([`702e41d`](https://github.com/python-gitlab/python-gitlab/commit/702e41dd0674e76b292d9ea4f559c86f0a99edfe))
* **build:** Do not include docs in wheel package ([`68a97ce`](https://github.com/python-gitlab/python-gitlab/commit/68a97ced521051afb093cf4fb6e8565d9f61f708))
* **api:** Delete invalid 'project-runner get' command ([#1628](https://github.com/python-gitlab/python-gitlab/issues/1628)) ([`905781b`](https://github.com/python-gitlab/python-gitlab/commit/905781bed2afa33634b27842a42a077a160cffb8))
* **api:** Replace deprecated attribute in delete_in_bulk() ([#1536](https://github.com/python-gitlab/python-gitlab/issues/1536)) ([`c59fbdb`](https://github.com/python-gitlab/python-gitlab/commit/c59fbdb0e9311fa84190579769e3c5c6aeb07fe5))
* **objects:** Rename confusing `to_project_id` argument ([`ce4bc0d`](https://github.com/python-gitlab/python-gitlab/commit/ce4bc0daef355e2d877360c6e496c23856138872))
* Raise error if there is a 301/302 redirection ([`d56a434`](https://github.com/python-gitlab/python-gitlab/commit/d56a4345c1ae05823b553e386bfa393541117467))
* **build:** Do not package tests in wheel ([`969dccc`](https://github.com/python-gitlab/python-gitlab/commit/969dccc084e833331fcd26c2a12ddaf448575ab4))

### Breaking
* The gitlab CLI will now accept CLI arguments and environment variables for its global options in addition to configuration file options. This may change behavior for some workflows such as running inside GitLab CI and with certain environment variables configured.  ([`ca58008`](https://github.com/python-gitlab/python-gitlab/commit/ca58008607385338aaedd14a58adc347fa1a41a0))
* stop encoding '.' to '%2E'. This could potentially be a breaking change for users who have incorrectly configured GitLab servers which don't handle period '.' characters correctly.  ([`702e41d`](https://github.com/python-gitlab/python-gitlab/commit/702e41dd0674e76b292d9ea4f559c86f0a99edfe))
* A config file is no longer needed to run the CLI. python-gitlab will default to https://gitlab.com with no authentication if there is no config file provided. python-gitlab will now also only look for configuration in the provided PYTHON_GITLAB_CFG path, instead of merging it with user- and system-wide config files. If the environment variable is defined and the file cannot be opened, python-gitlab will now explicitly fail.  ([`92a893b`](https://github.com/python-gitlab/python-gitlab/commit/92a893b8e230718436582dcad96175685425b1df))
* As of python-gitlab 3.0.0, Python 3.6 is no longer supported. Python 3.7 or higher is required.  ([`414009d`](https://github.com/python-gitlab/python-gitlab/commit/414009daebe19a8ae6c36f050dffc690dff40e91))
* As of python-gitlab 3.0.0, the default branch for development has changed from `master` to `main`.  ([`545f8ed`](https://github.com/python-gitlab/python-gitlab/commit/545f8ed24124837bf4e55aa34e185270a4b7aeff))
* remove deprecated branch protect methods in favor of the more complete protected branches API.  ([`9656a16`](https://github.com/python-gitlab/python-gitlab/commit/9656a16f9f34a1aeb8ea0015564bad68ffb39c26))
* The deprecated `name_regex` attribute has been removed in favor of `name_regex_delete`. (see https://gitlab.com/gitlab-org/gitlab/-/commit/ce99813cf54) ([`c59fbdb`](https://github.com/python-gitlab/python-gitlab/commit/c59fbdb0e9311fa84190579769e3c5c6aeb07fe5))
* rename confusing `to_project_id` argument in transfer_project to `project_id` (`--project-id` in CLI). This is used for the source project, not for the target namespace.  ([`ce4bc0d`](https://github.com/python-gitlab/python-gitlab/commit/ce4bc0daef355e2d877360c6e496c23856138872))
* remove deprecated constants defined in gitlab.v4.objects, and use only gitlab.const module  ([`3f320af`](https://github.com/python-gitlab/python-gitlab/commit/3f320af347df05bba9c4d0d3bdb714f7b0f7b9bf))
* remove deprecated tag release API. This was removed in GitLab 14.0  ([`2b8a94a`](https://github.com/python-gitlab/python-gitlab/commit/2b8a94a77ba903ae97228e7ffa3cc2bf6ceb19ba))
* remove deprecated project.issuesstatistics in favor of project.issues_statistics  ([`ca7777e`](https://github.com/python-gitlab/python-gitlab/commit/ca7777e0dbb82b5d0ff466835a94c99e381abb7c))
* remove deprecated members.all() method in favor of members_all.list()  ([`4d7b848`](https://github.com/python-gitlab/python-gitlab/commit/4d7b848e2a826c58e91970a1d65ed7d7c3e07166))
* remove deprecated pipelines() methods in favor of pipelines.list()  ([`c4f5ec6`](https://github.com/python-gitlab/python-gitlab/commit/c4f5ec6c615e9f83d533a7be0ec19314233e1ea0))
* python-gitlab will now default to gitlab.com if no URL is given  ([`8236281`](https://github.com/python-gitlab/python-gitlab/commit/823628153ec813c4490e749e502a47716425c0f1))
* raise error if there is a 301/302 redirection ([`d56a434`](https://github.com/python-gitlab/python-gitlab/commit/d56a4345c1ae05823b553e386bfa393541117467))

### Documentation
* Switch to Furo and refresh introduction pages ([`ee6b024`](https://github.com/python-gitlab/python-gitlab/commit/ee6b024347bf8a178be1a0998216f2a24c940cee))
* Correct documentation for updating discussion note ([`ee66f4a`](https://github.com/python-gitlab/python-gitlab/commit/ee66f4a777490a47ad915a3014729a9720bf909b))
* Rename documentation files to match names of code files ([`ee3f865`](https://github.com/python-gitlab/python-gitlab/commit/ee3f8659d48a727da5cd9fb633a060a9231392ff))
* **project:** Remove redundant encoding parameter ([`fed613f`](https://github.com/python-gitlab/python-gitlab/commit/fed613f41a298e79a975b7f99203e07e0f45e62c))
* Use annotations for return types ([`79e785e`](https://github.com/python-gitlab/python-gitlab/commit/79e785e765f4219fe6001ef7044235b82c5e7754))
* Update docs to use gitlab.const for constants ([`b3b0b5f`](https://github.com/python-gitlab/python-gitlab/commit/b3b0b5f1da5b9da9bf44eac33856ed6eadf37dd6))
* Only use type annotations for documentation ([`b7dde0d`](https://github.com/python-gitlab/python-gitlab/commit/b7dde0d7aac8dbaa4f47f9bfb03fdcf1f0b01c41))
* Add links to the GitLab API docs ([`e3b5d27`](https://github.com/python-gitlab/python-gitlab/commit/e3b5d27bde3e104e520d976795cbcb1ae792fb05))
* Fix API delete key example ([`b31bb05`](https://github.com/python-gitlab/python-gitlab/commit/b31bb05c868793e4f0cb4573dad6bf9ca01ed5d9))
* **pipelines:** Document take_ownership method ([`69461f6`](https://github.com/python-gitlab/python-gitlab/commit/69461f6982e2a85dcbf95a0b884abd3f4050c1c7))
* **api:** Document the update method for project variables ([`7992911`](https://github.com/python-gitlab/python-gitlab/commit/7992911896c62f23f25742d171001f30af514a9a))
* **api:** Clarify job token usage with auth() ([`3f423ef`](https://github.com/python-gitlab/python-gitlab/commit/3f423efab385b3eb1afe59ad12c2da7eaaa11d76))
* Fix a few typos ([`7ea4ddc`](https://github.com/python-gitlab/python-gitlab/commit/7ea4ddc4248e314998fd27eea17c6667f5214d1d))
* Consolidate changelogs and remove v3 API docs ([`90da8ba`](https://github.com/python-gitlab/python-gitlab/commit/90da8ba0342ebd42b8ec3d5b0d4c5fbb5e701117))
* Correct documented return type ([`acabf63`](https://github.com/python-gitlab/python-gitlab/commit/acabf63c821745bd7e43b7cd3d799547b65e9ed0))

## v2.10.1 (2021-08-28)
### Fix
* **mixins:** Improve deprecation warning ([`57e0187`](https://github.com/python-gitlab/python-gitlab/commit/57e018772492a8522b37d438d722c643594cf580))
* **deps:** Upgrade requests to 2.25.0 (see CVE-2021-33503) ([`ce995b2`](https://github.com/python-gitlab/python-gitlab/commit/ce995b256423a0c5619e2a6c0d88e917aad315ba))

### Documentation
* **mergequests:** Gl.mergequests.list documentation was missleading ([`5b5a7bc`](https://github.com/python-gitlab/python-gitlab/commit/5b5a7bcc70a4ddd621cbd59e134e7004ad2d9ab9))

## v2.10.0 (2021-07-28)
### Feature
* **api:** Add merge_ref for merge requests ([`1e24ab2`](https://github.com/python-gitlab/python-gitlab/commit/1e24ab247cc783ae240e94f6cb379fef1e743a52))
* **api:** Add `name_regex_keep` attribute in `delete_in_bulk()` ([`e49ff3f`](https://github.com/python-gitlab/python-gitlab/commit/e49ff3f868cbab7ff81115f458840b5f6d27d96c))

### Fix
* **api:** Do not require Release name for creation ([`98cd03b`](https://github.com/python-gitlab/python-gitlab/commit/98cd03b7a3085356b5f0f4fcdb7dc729b682f481))

### Documentation
* **readme:** Move contributing docs to CONTRIBUTING.rst ([`edf49a3`](https://github.com/python-gitlab/python-gitlab/commit/edf49a3d855b1ce4e2bd8a7038b7444ff0ab5fdc))
* Add example for mr.merge_ref ([`b30b8ac`](https://github.com/python-gitlab/python-gitlab/commit/b30b8ac27d98ed0a45a13775645d77b76e828f95))
* **project:** Add example on getting a single project using name with namespace ([`ef16a97`](https://github.com/python-gitlab/python-gitlab/commit/ef16a979031a77155907f4160e4f5e159d839737))

## v2.9.0 (2021-06-28)
### Feature
* **release:** Allow to update release ([`b4c4787`](https://github.com/python-gitlab/python-gitlab/commit/b4c4787af54d9db6c1f9e61154be5db9d46de3dd))
* **api:** Add group hooks ([`4a7e9b8`](https://github.com/python-gitlab/python-gitlab/commit/4a7e9b86aa348b72925bce3af1e5d988b8ce3439))
* **api:** Remove responsibility for API inconsistencies for MR reviewers ([`3d985ee`](https://github.com/python-gitlab/python-gitlab/commit/3d985ee8cdd5d27585678f8fbb3eb549818a78eb))
* **api:** Add MR pipeline manager and deprecate pipelines() method ([`954357c`](https://github.com/python-gitlab/python-gitlab/commit/954357c49963ef51945c81c41fd4345002f9fb98))
* **api:** Add support for creating/editing reviewers in project merge requests ([`676d1f6`](https://github.com/python-gitlab/python-gitlab/commit/676d1f6565617a28ee84eae20e945f23aaf3d86f))

### Documentation
* **tags:** Remove deprecated functions ([`1b1a827`](https://github.com/python-gitlab/python-gitlab/commit/1b1a827dd40b489fdacdf0a15b0e17a1a117df40))
* **release:** Add update example ([`6254a5f`](https://github.com/python-gitlab/python-gitlab/commit/6254a5ff6f43bd7d0a26dead304465adf1bd0886))
* Make Gitlab class usable for intersphinx ([`8753add`](https://github.com/python-gitlab/python-gitlab/commit/8753add72061ea01c508a42d16a27388b1d92677))

## v2.8.0 (2021-06-10)
### Feature
* Add keys endpoint ([`a81525a`](https://github.com/python-gitlab/python-gitlab/commit/a81525a2377aaed797af0706b00be7f5d8616d22))
* **objects:** Add support for Group wikis ([#1484](https://github.com/python-gitlab/python-gitlab/issues/1484)) ([`74f5e62`](https://github.com/python-gitlab/python-gitlab/commit/74f5e62ef5bfffc7ba21494d05dbead60b59ecf0))
* **objects:** Add support for generic packages API ([`79d88bd`](https://github.com/python-gitlab/python-gitlab/commit/79d88bde9e5e6c33029e4a9f26c97404e6a7a874))
* **api:** Add deployment mergerequests interface ([`fbbc0d4`](https://github.com/python-gitlab/python-gitlab/commit/fbbc0d400015d7366952a66e4401215adff709f0))
* **objects:** Support all issues statistics endpoints ([`f731707`](https://github.com/python-gitlab/python-gitlab/commit/f731707f076264ebea65afc814e4aca798970953))
* **objects:** Add support for descendant groups API ([`1b70580`](https://github.com/python-gitlab/python-gitlab/commit/1b70580020825adf2d1f8c37803bc4655a97be41))
* **objects:** Add pipeline test report support ([`ee9f96e`](https://github.com/python-gitlab/python-gitlab/commit/ee9f96e61ab5da0ecf469c21cccaafc89130a896))
* **objects:** Add support for billable members ([`fb0b083`](https://github.com/python-gitlab/python-gitlab/commit/fb0b083a0e536a6abab25c9ad377770cc4290fe9))
* Add feature to get inherited member for project/group ([`e444b39`](https://github.com/python-gitlab/python-gitlab/commit/e444b39f9423b4a4c85cdb199afbad987df026f1))
* Add code owner approval as attribute ([`fdc46ba`](https://github.com/python-gitlab/python-gitlab/commit/fdc46baca447e042d3b0a4542970f9758c62e7b7))
* Indicate that we are a typed package ([`e4421ca`](https://github.com/python-gitlab/python-gitlab/commit/e4421caafeeb0236df19fe7b9233300727e1933b))
* Add support for lists of integers to ListAttribute ([`115938b`](https://github.com/python-gitlab/python-gitlab/commit/115938b3e5adf9a2fb5ecbfb34d9c92bf788035e))

### Fix
* Catch invalid type used to initialize RESTObject ([`c7bcc25`](https://github.com/python-gitlab/python-gitlab/commit/c7bcc25a361f9df440f9c972672e5eec3b057625))
* Functional project service test ([#1500](https://github.com/python-gitlab/python-gitlab/issues/1500)) ([`093db9d`](https://github.com/python-gitlab/python-gitlab/commit/093db9d129e0a113995501755ab57a04e461c745))
* Ensure kwargs are passed appropriately for ObjectDeleteMixin ([`4e690c2`](https://github.com/python-gitlab/python-gitlab/commit/4e690c256fc091ddf1649e48dbbf0b40cc5e6b95))
* **cli:** Add missing list filter for jobs ([`b3d1c26`](https://github.com/python-gitlab/python-gitlab/commit/b3d1c267cbe6885ee41b3c688d82890bb2e27316))
* Change mr.merge() to use 'post_data' ([`cb6a3c6`](https://github.com/python-gitlab/python-gitlab/commit/cb6a3c672b9b162f7320c532410713576fbd1cdc))
* **cli:** Fix parsing CLI objects to classnames ([`4252070`](https://github.com/python-gitlab/python-gitlab/commit/42520705a97289ac895a6b110d34d6c115e45500))
* **objects:** Return server data in cancel/retry methods ([`9fed061`](https://github.com/python-gitlab/python-gitlab/commit/9fed06116bfe5df79e6ac5be86ae61017f9a2f57))
* **objects:** Add missing group attributes ([`d20ff4f`](https://github.com/python-gitlab/python-gitlab/commit/d20ff4ff7427519c8abccf53e3213e8929905441))
* **objects:** Allow lists for filters for in all objects ([`603a351`](https://github.com/python-gitlab/python-gitlab/commit/603a351c71196a7f516367fbf90519f9452f3c55))
* Iids not working as a list in projects.issues.list() ([`45f806c`](https://github.com/python-gitlab/python-gitlab/commit/45f806c7a7354592befe58a76b7e33a6d5d0fe6e))
* Add a check to ensure the MRO is correct ([`565d548`](https://github.com/python-gitlab/python-gitlab/commit/565d5488b779de19a720d7a904c6fc14c394a4b9))

### Documentation
* Fix typo in http_delete docstring ([`5226f09`](https://github.com/python-gitlab/python-gitlab/commit/5226f095c39985d04c34e7703d60814e74be96f8))
* **api:** Add behavior in local attributes when updating objects ([`38f65e8`](https://github.com/python-gitlab/python-gitlab/commit/38f65e8e9994f58bdc74fe2e0e9b971fc3edf723))
* Fail on  warnings during sphinx build ([`cbd4d52`](https://github.com/python-gitlab/python-gitlab/commit/cbd4d52b11150594ec29b1ce52348c1086a778c8))

## v2.7.1 (2021-04-26)

* fix(files): do not url-encode file paths twice

## v2.7.0 (2021-04-25)

### Bug Fixes

* update user's bool data and avatar (3ba27ffb)
* argument type was not a tuple as expected (062f8f6a)
* correct some type-hints in gitlab/mixins.py (8bd31240)
* only append kwargs as query parameters (b9ecc9a8)
* only add query_parameters to GitlabList once (1386)
* checking if RESTManager._from_parent_attrs is set (8224b406)
* handling config value in _get_values_from_helper (9dfb4cd9)
* let the homedir be expanded in path of helper (fc7387a0)
* make secret helper more user friendly (fc2798fc)
* linting issues and test (b04dd2c0)
* handle tags like debian/2%2.6-21 as identifiers (b4dac5ce)
* remove duplicate class definitions in v4/objects/users.py (7c4e6259)
* wrong variable name (15ec41ca)
* tox pep8 target, so that it can run (f518e87b)
* undefined name errors (48ec9e0f)
* extend wait timeout for test_delete_user() (19fde8ed)
* test_update_group() dependency on ordering (e78a8d63)
* honor parameter value passed (c2f8f0e7)
* **objects:**  add single get endpoint for instance audit events (c3f0a6f1)
* **types:**  prevent __dir__ from producing duplicates (5bf7525d)

### Features

* add ProjectPackageFile (#1372)
* add option to add a helper to lookup token (8ecf5592)
* add project audit endpoint (6660dbef)
* add personal access token API (2bb16fac)
* add import from bitbucket server (ff3013a2)
* **api,cli:**  make user agent configurable (4bb201b9)
* **issues:**  add missing get verb to IssueManager (f78ebe06)
* **objects:**
  * add support for resource state events API (d4799c40)
  * add support for group audit events API (2a0fbdf9)
  * add Release Links API support (28d75181)
* **projects:**  add project access token api (1becef02)
* **users:**  add follow/unfollow API (e456869d)

### Documentation
* correct ProjectFile.decode() documentation (b180bafd)
* update doc for token helper (3ac6fa12)
* better real life token lookup example (9ef83118)

## v2.6.0 (2021-01-29)

### Features

* support multipart uploads (2fa3004d)
* add MINIMAL_ACCESS constant (49eb3ca7)
* unit tests added (f37ebf5f)
* added support for pipeline bridges (05cbdc22)
* adds support for project merge request approval rules (#1199) (c6fbf399)
* **api:**
  * added wip filter param for merge requests (d6078f80)
  * added wip filter param for merge requests (aa6e80d5)
  * add support for user identity provider deletion (e78e1215)
* **tests:**  test label getter (a41af902)

### Bug Fixes

* docs changed using the consts (650b65c3)
* typo (9baa9053)
* **api:**
  * use RetrieveMixin for ProjectLabelManager (1a143952)
  * add missing runner access_level param (92669f2e)
* **base:**  really refresh object (e1e0d8cb), closes (#1155)
* **cli:**
  * write binary data to stdout buffer (0733ec6c)
  * add missing args for project lists (c73e2374)

## v2.5.0 (2020-09-01)

### Features

* add support to resource milestone events (88f8cc78), closes #1154
* add share/unshare group with group (7c6e541d)
* add support for instance variables (4492fc42)
* add support for Packages API (71495d12)
* add endpoint for latest ref artifacts (b7a07fca)

### Bug Fixes

* wrong reconfirmation parameter when updating user's email (b5c267e1)
* tests fail when using REUSE_CONTAINER option ([0078f899](https://github.com/python-gitlab/python-gitlab/commit/0078f8993c38df4f02da9aaa3f7616d1c8b97095), closes #1146
* implement Gitlab's behavior change for owned=True (99777991)

## v2.4.0 (2020-07-09)

### Bug Fixes

* do not check if kwargs is none (a349b90e)
* make query kwargs consistent between call in init and next (72ffa016)
* pass kwargs to subsequent queries in gitlab list (1d011ac7)
* **merge:**  parse arguments as query_data (878098b7)

### Features

* add NO_ACCESS const (dab4d0a1)
* add masked parameter for variables command (b6339bf8)

## v2.3.1 (2020-06-09)

* revert keyset pagination by default

## v2.3.0 (2020-06-08)

### Features

* add group runners api (49439916)
* add play command to project pipeline schedules (07b99881)
* allow an environment variable to specify config location (401e702a)
* **api:**  added support in the GroupManager to upload Group avatars (28eb7eab)
* **services:**  add project service list API (fc522218)
* **types:**  add __dir__ to RESTObject to expose attributes (cad134c0)

### Bug Fixes

* use keyset pagination by default for /projects > 50000 (f86ef3bb)
* **config:**  fix duplicate code (ee2df6f1), closes (#1094)
* **project:**  add missing project parameters (ad8c67d6)

## v2.2.0 (2020-04-07)

### Bug Fixes

* add missing import_project param (9b16614b)
* **types:**  do not split single value string in ListAttribute (a26e5858)

### Features

* add commit GPG signature API (da7a8097)
* add create from template args to ProjectManager (f493b73e)
* add remote mirrors API (#1056) (4cfaa2fd)
* add Gitlab Deploy Token API (01de524c)
* add Group Import/Export API (#1037) (6cb9d923)

## v2.1.2 (2020-03-09)

### Bug Fixes

* Fix regression, when using keyset pagination with merge requests. Related to https://github.com/python-gitlab/python-gitlab/issues/1044

## v2.1.1 (2020-03-09)

### Bug Fixes

**users**: update user attributes

This change was made to migate an issue in Gitlab (again). Fix available in: https://gitlab.com/gitlab-org/gitlab/-/merge_requests/26792

## v2.1.0 (2020-03-08)

### Bug Fixes

* do not require empty data dict for create() (99d959f7)
* remove trailing slashes from base URL (#913) (2e396e4a)
* return response with commit data (b77b945c)
* remove null values from features POST data, because it fails with HTTP 500 (1ec1816d)
* **docs:**
  * fix typo in user memberships example (33889bcb)
  * update to new set approvers call for # of approvers (8e0c5262)
  * update docs and tests for set_approvers (2cf12c79)
* **objects:**
  * add default name data and use http post (70c0cfb6)
  * update set_approvers function call (65ecadcf)
  * update to new gitlab api for path, and args (e512cddd)

### Features

* add support for user memberships API (#1009) (c313c2b0)
* add support for commit revert API (#991) (5298964e)
* add capability to control GitLab features per project or group (7f192b4f)
* use keyset pagination by default for `all=True` (99b4484d)
* add support for GitLab OAuth Applications API (4e12356d)

## v2.0.1 (2020-02-05)

### Changes

* **users:**  update user attributes

This change was made to migate an issue in Gitlab. See: https://gitlab.com/gitlab-org/gitlab/issues/202070

## v2.0.0 (2020-01-26)

### This releases drops support for python < 3.6

### Bug Fixes

* **projects:**  adjust snippets to match the API (e104e213)

### Features

* add global order_by option to ease pagination (d1879253)
* support keyset pagination globally (0b71ba4d)
* add appearance API (4c4ac5ca)
* add autocompletion support (973cb8b9)

## v1.15.0 (2019-12-16)

### Bug Fixes

* ignore all parameter, when as_list=True 137d72b3, closes #962

### Features

* allow cfg timeout to be overrided via kwargs e9a8289a
* add support for /import/github aa4d41b7
* nicer stacktrace 697cda24
* retry transient HTTP errors 59fe2714, closes #970
* access project's issues statistics 482e57ba, closes #966
* adding project stats db0b00a9, closes #967
* add variable_type/protected to projects ci variables 4724c50e
* add variable_type to groups ci variables 0986c931

## v1.14.0 (2019-12-07)

### Bug Fixes

* added missing attributes for project approvals 460ed63c
* **labels:**  ensure label.save() works 727f5361
* **project-fork:**
  * copy create fix from ProjectPipelineManager 516307f1
  * correct path computation for project-fork list 44a7c278

### Features

* add audit endpoint 2534020b
* add project and group clusters ebd053e7
* add support for include_subgroups filter adbcd83f


## v1.13.0 (2019-11-02)

### Features

* add users activate, deactivate functionality (32ad6692)
* send python-gitlab version as user-agent (c22d49d0)
* add deployment creation (ca256a07), closes [#917]
* **auth:**  remove deprecated session auth (b751cdf4)
* **doc:**  remove refs to api v3 in docs (6beeaa99)
* **test:**  unused unittest2, type -> isinstance (33b18012)

### Bug Fixes

* **projects:**  support `approval_rules` endpoint for projects (2cef2bb4)

## v1.12.1 (2019-10-07)

### Bug Fixes

fix: fix not working without auth provided

## v1.12.0 (2019-10-06)

### Features

* add support for job token
* **project:**
  * implement update_submodule
  * add file blame api
* **user:**  add status api

### Bug Fixes

* **cli:**  fix cli command user-project list
* **labels:**  don't mangle label name on update
* **todo:**  mark_all_as_done doesn't return anything

## v1.11.0 (2019-08-31)

### Features

* add methods to retrieve an individual project environment
* group labels with subscriptable mixin

### Bug Fixes

* projects: avatar uploading for projects
* remove empty list default arguments 
* remove empty dict default arguments
* add project and group label update without id to fix cli

## v1.10.0 (2019-07-22)

### Features

* add mr rebase method bc4280c2
* get artifact by ref and job cda11745
* add support for board update 908d79fa, closes #801
* add support for issue.related_merge_requests 90a36315, closes #794

### Bug Fixes

* improve pickle support b4b5decb
* **cli:**
  * allow --recursive parameter in repository tree 7969a78c, closes #718, #731
  * don't fail when the short print attr value is None 8d1552a0, closes #717, #727
  * fix update value for key not working b7662039


## v1.9.0 (2019-06-19)

### Features

* implement artifacts deletion
* add endpoint to get the variables of a pipeline
* delete ProjectPipeline
* implement __eq__ and __hash__ methods
* Allow runpy invocation of CLI tool (python -m gitlab)
* add project releases api
* merged new release & registry apis

### Bug Fixes

* convert # to %23 in URLs
* pep8 errors
* use python2 compatible syntax for super
* Make MemberManager.all() return a list of objects
* %d replaced by %s
* Re-enable command specific help messages
* dont ask for id attr if this is \*Manager originating custom action
* fix -/_ replacament for \*Manager custom actions
* fix repository_id marshaling in cli
* register cli action for delete_in_bulk

## v1.8.0 (2019-02-22)

* docs(setup): use proper readme on PyPI
* docs(readme): provide commit message guidelines
* fix(api): make reset_time_estimate() work again
* fix: handle empty 'Retry-After' header from GitLab
* fix: remove decode() on error_message string
* chore: release tags to PyPI automatically
* fix(api): avoid parameter conflicts with python and gitlab
* fix(api): Don't try to parse raw downloads
* feat: Added approve & unapprove method for Mergerequests
* fix all kwarg behaviour

## v1.7.0 (2018-12-09)

* **docs:** Fix the owned/starred usage documentation
* **docs:** Add a warning about http to https redirects
* Fix the https redirection test
* **docs:** Add a note about GroupProject limited API
* Add missing comma in ProjectIssueManager _create_attrs
* More flexible docker image
* Add project protected tags management
* **cli:** Print help and usage without config file
* Rename MASTER_ACCESS to MAINTAINER_ACCESS
* **docs:** Add docs build information
* Use docker image with current sources
* **docs:** Add PyYAML requirement notice
* Add Gitter badge to README
* **docs:** Add an example of pipeline schedule vars listing
* **cli:** Exit on config parse error, instead of crashing
* Add support for resource label events
* **docs:** Fix the milestone filetring doc (iid -> iids)
* **docs:** Fix typo in custom attributes example
* Improve error message handling in exceptions
* Add support for members all() method
* Add access control options to protected branch creation

## v1.6.0 (2018-08-25)

* **docs:** Don't use hardcoded values for ids
* **docs:** Improve the snippets examples
* **cli:** Output: handle bytes in API responses
* **cli:** Fix the case where we have nothing to print
* Project import: fix the override_params parameter
* Support group and global MR listing
* Implement MR.pipelines()
* MR: add the squash attribute for create/update
* Added support for listing forks of a project
* **docs:** Add/update notes about read-only objects
* Raise an exception on https redirects for PUT/POST
* **docs:** Add a FAQ
* **cli:** Fix the project-export download

## v1.5.1 (2018-06-23)

* Fix the ProjectPipelineJob base class (regression)

## v1.5.0 (2018-06-22)

* Drop API v3 support
* Drop GetFromListMixin
* Update the sphinx extension for v4 objects
* Add support for user avatar upload
* Add support for project import/export
* Add support for the search API
* Add a global per_page config option
* Add support for the discussions API
* Add support for merged branches deletion
* Add support for Project badges
* Implement user_agent_detail for snippets
* Implement commit.refs()
* Add commit.merge_requests() support
* Deployment: add list filters
* Deploy key: add missing attributes
* Add support for environment stop()
* Add feature flags deletion support
* Update some group attributes
* Issues: add missing attributes and methods
* Fix the participants() decorator
* Add support for group boards
* Implement the markdown rendering API
* Update MR attributes
* Add pipeline listing filters
* Add missing project attributes
* Implement runner jobs listing
* Runners can be created (registered)
* Implement runner token validation
* Update the settings attributes
* Add support for the gitlab CI lint API
* Add support for group badges
* Fix the IssueManager path to avoid redirections
* time_stats(): use an existing attribute if available
* Make ProjectCommitStatus.create work with CLI
* Tests: default to python 3
* ProjectPipelineJob was defined twice
* Silence logs/warnings in unittests
* Add support for MR approval configuration (EE)
* Change post_data default value to None
* Add geo nodes API support (EE)
* Add support for issue links (EE)
* Add support for LDAP groups (EE)
* Add support for board creation/deletion (EE)
* Add support for Project.pull_mirror (EE)
* Add project push rules configuration (EE)
* Add support for the EE license API
* Add support for the LDAP groups API (EE)
* Add support for epics API (EE)
* Fix the non-verbose output of ProjectCommitComment

## v1.4.0 (2018-05-19)

* Require requests>=2.4.2
* ProjectKeys can be updated
* Add support for unsharing projects (v3/v4)
* **cli:** fix listing for json and yaml output
* Fix typos in documentation
* Introduce RefreshMixin
* **docs:** Fix the time tracking examples
* **docs:** Commits: add an example of binary file creation
* **cli:** Allow to read args from files
* Add support for recursive tree listing
* **cli:** Restore the --help option behavior
* Add basic unit tests for v4 CLI
* **cli:** Fix listing of strings
* Support downloading a single artifact file
* Update docs copyright years
* Implement attribute types to handle special cases
* **docs:** fix GitLab reference for notes
* Expose additional properties for Gitlab objects
* Fix the impersonation token deletion example
* feat: obey the rate limit
* Fix URL encoding on branch methods
* **docs:** add a code example for listing commits of a MR
* **docs:** update service.available() example for API v4
* **tests:** fix functional tests for python3
* api-usage: bit more detail for listing with `all`
* More efficient .get() for group members
* Add docs for the `files` arg in http_*
* Deprecate GetFromListMixin

## v1.3.0 (2018-02-18)

* Add support for pipeline schedules and schedule variables
* Clarify information about supported python version
* Add manager for jobs within a pipeline
* Fix wrong tag example
* Update the groups documentation
* Add support for MR participants API
* Add support for getting list of user projects
* Add Gitlab and User events support
* Make trigger_pipeline return the pipeline
* Config: support api_version in the global section
* Gitlab can be used as context manager
* Default to API v4
* Add a simplified example for streamed artifacts
* Add documentation about labels update

## v1.2.0 (2018-01-01)

* Add mattermost service support
* Add users custom attributes support
* **doc:** Fix project.triggers.create example with v4 API
* Oauth token support
* Remove deprecated objects/methods
* Rework authentication args handling
* Add support for oauth and anonymous auth in config/CLI
* Add support for impersonation tokens API
* Add support for user activities
* Update user docs with gitlab URLs
* **docs:** Bad arguments in projects file documentation
* Add support for user_agent_detail (issues)
* Add a SetMixin
* Add support for project housekeeping
* Expected HTTP response for subscribe is 201
* Update pagination docs for ProjectCommit
* Add doc to get issue from iid
* Make todo() raise GitlabTodoError on error
* Add support for award emojis
* Update project services docs for v4
* Avoid sending empty update data to issue.save
* **docstrings:** Explicitly document pagination arguments
* **docs:** Add a note about password auth being removed from GitLab
* Submanagers: allow having undefined parameters
* ProjectFile.create(): don't modify the input data
* Update testing tools for /session removal
* Update groups tests
* Allow per_page to be used with generators
* Add groups listing attributes
* Add support for subgroups listing
* Add supported python versions in setup.py
* Add support for pagesdomains
* Add support for features flags
* Add support for project and group custom variables
* Add support for user/group/project filter by custom attribute
* Respect content of REQUESTS_CA_BUNDLE and \*_proxy envvars

## v1.1.0 (2017-11-03)

* Fix trigger variables in v4 API
* Make the delete() method handle / in ids
* **docs:** update the file upload samples
* Tags release description: support / in tag names
* **docs:** improve the labels usage documentation
* Add support for listing project users
* ProjectFileManager.create: handle / in file paths
* Change ProjectUser and GroupProject base class
* **docs:** document `get_create_attrs` in the API tutorial
* Document the Gitlab session parameter
* ProjectFileManager: custom update() method
* Project: add support for printing_merge_request_link_enabled attr
* Update the ssl_verify docstring
* Add support for group milestones
* Add support for GPG keys
* Add support for wiki pages
* Update the repository_blob documentation
* Fix the CLI for objects without ID (API v4)
* Add a contributed Dockerfile
* Pagination generators: expose more information
* Module's base objects serialization
* **doc:** Add sample code for client-side certificates

## v1.0.2 (2017-09-29)

* **docs:** remove example usage of submanagers
* Properly handle the labels attribute in ProjectMergeRequest
* ProjectFile: handle / in path for delete() and save()

## v1.0.1 (2017-09-21)

* Tags can be retrieved by ID
* Add the server response in GitlabError exceptions
* Add support for project file upload
* Minor typo fix in "Switching to v4" documentation
* Fix password authentication for v4
* Fix the labels attrs on MR and issues
* Exceptions: use a proper error message
* Fix http_get method in get artifacts and job trace
* CommitStatus: `sha` is parent attribute
* Fix a couple listing calls to allow proper pagination
* Add missing doc file

## v1.0.0 (2017-09-08)

* Support for API v4. See
  http://python-gitlab.readthedocs.io/en/master/switching-to-v4.html
* Support SSL verification via internal CA bundle
* Docs: Add link to gitlab docs on obtaining a token
* Added dependency injection support for Session
* Fixed repository_compare examples
* Fix changelog and release notes inclusion in sdist
* Missing expires_at in GroupMembers update
* Add lower-level methods for Gitlab()

## v0.21.2 (2017-06-11)

* Install doc: use sudo for system commands
* **v4:** Make MR work properly
* Remove extra_attrs argument from `_raw_list`
* **v4:** Make project issues work properly
* Fix urlencode() usage (python 2/3) (#268)
* Fixed spelling mistake (#269)
* Add new event types to ProjectHook

## v0.21.1 (2017-05-25)

* Fix the manager name for jobs in the Project class
* Fix the docs

## v0.21 (2017-05-24)

* Add time_stats to ProjectMergeRequest
* Update User options for creation and update (#246)
* Add milestone.merge_requests() API
* Fix docs typo (s/correspnding/corresponding/)
* Support milestone start date (#251)
* Add support for priority attribute in labels (#256)
* Add support for nested groups (#257)
* Make GroupProjectManager a subclass of ProjectManager (#255)
* Available services: return a list instead of JSON (#258)
* MR: add support for time tracking features (#248)
* Fixed repository_tree and repository_blob path encoding (#265)
* Add 'search' attribute to projects.list()
* Initial gitlab API v4 support
* Reorganise the code to handle v3 and v4 objects
* Allow 202 as delete return code
* Deprecate parameter related methods in gitlab.Gitlab

## v0.20 (2017-03-25)

* Add time tracking support (#222)
* Improve changelog (#229, #230)
* Make sure that manager objects are never overwritten (#209)
* Include chanlog and release notes in docs
* Add DeployKey{,Manager} classes (#212)
* Add support for merge request notes deletion (#227)
* Properly handle extra args when listing with all=True (#233)
* Implement pipeline creation API (#237)
* Fix spent_time methods
* Add 'delete source branch' option when creating MR (#241)
* Provide API wrapper for cherry picking commits (#236)
* Stop listing if recursion limit is hit (#234)

## v0.19 (2017-02-21)

* Update project.archive() docs
* Support the scope attribute in runners.list()
* Add support for project runners
* Add support for commit creation
* Fix install doc
* Add builds-email and pipelines-email services
* Deploy keys: rework enable/disable
* Document the dynamic aspect of objects
* Add pipeline_events to ProjectHook attrs
* Add due_date attribute to ProjectIssue
* Handle settings.domain_whitelist, partly
* {Project,Group}Member: support expires_at attribute

## v0.18 (2016-12-27)

* Fix JIRA service editing for GitLab 8.14+
* Add jira_issue_transition_id to the JIRA service optional fields
* Added support for Snippets (new API in Gitlab 8.15)
* **docs:** update pagination section
* **docs:** artifacts example: open file in wb mode
* **CLI:** ignore empty arguments
* **CLI:** Fix wrong use of arguments
* **docs:** Add doc for snippets
* Fix duplicated data in API docs
* Update known attributes for projects
* sudo: always use strings

## v0.17 (2016-12-02)

* README: add badges for pypi and RTD
* Fix ProjectBuild.play (raised error on success)
* Pass kwargs to the object factory
* Add .tox to ignore to respect default tox settings
* Convert response list to single data source for iid requests
* Add support for boards API
* Add support for Gitlab.version()
* Add support for broadcast messages API
* Add support for the notification settings API
* Don't overwrite attributes returned by the server
* Fix bug when retrieving changes for merge request
* Feature: enable / disable the deploy key in a project
* Docs: add a note for python 3.5 for file content update
* ProjectHook: support the token attribute
* Rework the API documentation
* Fix docstring for http_{username,password}
* Build managers on demand on GitlabObject's
* API docs: add managers doc in GitlabObject's
* Sphinx ext: factorize the build methods
* Implement `__repr__` for gitlab objects
* Add a 'report a bug' link on doc
* Remove deprecated methods
* Implement merge requests diff support
* Make the manager objects creation more dynamic
* Add support for templates API
* Add attr 'created_at' to ProjectIssueNote
* Add attr 'updated_at' to ProjectIssue
* CLI: add support for project all --all
* Add support for triggering a new build
* Rework requests arguments (support latest requests release)
* Fix `should_remove_source_branch`

## v0.16 (2016-10-16)

* Add the ability to fork to a specific namespace
* JIRA service - add api_url to optional attributes
* Fix bug: Missing coma concatenates array values
* docs: branch protection notes
* Create a project in a group
* Add only_allow_merge_if_build_succeeds option to project objects
* Add support for --all in CLI
* Fix examples for file modification
* Use the plural merge_requests URL everywhere
* Rework travis and tox setup
* Workaround gitlab setup failure in tests
* Add ProjectBuild.erase()
* Implement ProjectBuild.play()

## v0.15.1 (2016-10-16)

* docs: improve the pagination section
* Fix and test pagination
* 'path' is an existing gitlab attr, don't use it as method argument

## v0.15 (2016-08-28)

* Add a basic HTTP debug method
* Run more tests in travis
* Fix fork creation documentation
* Add more API examples in docs
* Update the ApplicationSettings attributes
* Implement the todo API
* Add sidekiq metrics support
* Move the constants at the gitlab root level
* Remove methods marked as deprecated 7 months ago
* Refactor the Gitlab class
* Remove _get_list_or_object() and its tests
* Fix canGet attribute (typo)
* Remove unused ProjectTagReleaseManager class
* Add support for project services API
* Add support for project pipelines
* Add support for access requests
* Add support for project deployments

## v0.14 (2016-08-07)

* Remove 'next_url' from kwargs before passing it to the cls constructor.
* List projects under group
* Add support for subscribe and unsubscribe in issues
* Project issue: doc and CLI for (un)subscribe
* Added support for HTTP basic authentication
* Add support for build artifacts and trace
* --title is a required argument for ProjectMilestone
* Commit status: add optional context url
* Commit status: optional get attrs
* Add support for commit comments
* Issues: add optional listing parameters
* Issues: add missing optional listing parameters
* Project issue: proper update attributes
* Add support for project-issue move
* Update ProjectLabel attributes
* Milestone: optional listing attrs
* Add support for namespaces
* Add support for label (un)subscribe
* MR: add (un)subscribe support
* Add `note_events` to project hooks attributes
* Add code examples for a bunch of resources
* Implement user emails support
* Project: add VISIBILITY_* constants
* Fix the Project.archive call
* Implement archive/unarchive for a projet
* Update ProjectSnippet attributes
* Fix ProjectMember update
* Implement sharing project with a group
* Implement CLI for project archive/unarchive/share
* Implement runners global API
* Gitlab: add managers for build-related resources
* Implement ProjectBuild.keep_artifacts
* Allow to stream the downloads when appropriate
* Groups can be updated
* Replace Snippet.Content() with a new content() method
* CLI: refactor _die()
* Improve commit statuses and comments
* Add support from listing group issues
* Added a new project attribute to enable the container registry.
* Add a contributing section in README
* Add support for global deploy key listing
* Add support for project environments
* MR: get list of changes and commits
* Fix the listing of some resources
* MR: fix updates
* Handle empty messages from server in exceptions
* MR (un)subscribe: don't fail if state doesn't change
* MR merge(): update the object

## v0.13 (2016-05-16)

* Add support for MergeRequest validation
* MR: add support for cancel_merge_when_build_succeeds
* MR: add support for closes_issues
* Add "external" parameter for users
* Add deletion support for issues and MR
* Add missing group creation parameters
* Add a Session instance for all HTTP requests
* Enable updates on ProjectIssueNotes
* Add support for Project raw_blob
* Implement project compare
* Implement project contributors
* Drop the next_url attribute when listing
* Remove unnecessary canUpdate property from ProjectIssuesNote
* Add new optional attributes for projects
* Enable deprecation warnings for gitlab only
* Rework merge requests update
* Rework the Gitlab.delete method
* ProjectFile: file_path is required for deletion
* Rename some methods to better match the API URLs
* Deprecate the file_* methods in favor of the files manager
* Implement star/unstar for projects
* Implement list/get licenses
* Manage optional parameters for list() and get()

## v0.12.2 (2016-03-19)

* Add new `ProjectHook` attributes
* Add support for user block/unblock
* Fix GitlabObject creation in _custom_list
* Add support for more CLI subcommands
* Add some unit tests for CLI
* Add a coverage tox env
* Define `GitlabObject.as_dict()` to dump object as a dict
* Define `GitlabObject.__eq__()` and `__ne__()` equivalence methods
* Define UserManager.search() to search for users
* Define UserManager.get_by_username() to get a user by username
* Implement "user search" CLI
* Improve the doc for UserManager
* CLI: implement user get-by-username
* Re-implement _custom_list in the Gitlab class
* Fix the 'invalid syntax' error on Python 3.2
* Gitlab.update(): use the proper attributes if defined

## v0.12.1 (2016-02-03)

* Fix a broken upload to pypi

## v0.12 (2016-02-03)

* Improve documentation
* Improve unit tests
* Improve test scripts
* Skip BaseManager attributes when encoding to JSON
* Fix the json() method for python 3
* Add Travis CI support
* Add a decode method for ProjectFile
* Make connection exceptions more explicit
* Fix ProjectLabel get and delete
* Implement ProjectMilestone.issues()
* ProjectTag supports deletion
* Implement setting release info on a tag
* Implement project triggers support
* Implement project variables support
* Add support for application settings
* Fix the 'password' requirement for User creation
* Add sudo support
* Fix project update
* Fix Project.tree()
* Add support for project builds

## v0.11.1 (2016-01-17)

* Fix discovery of parents object attrs for managers
* Support setting commit status
* Support deletion without getting the object first
* Improve the documentation

## v0.11 (2016-01-09)

* functional_tests.sh: support python 2 and 3
* Add a get method for GitlabObject
* CLI: Add the -g short option for --gitlab
* Provide a create method for GitlabObject's
* Rename the `_created` attribute `_from_api`
* More unit tests
* CLI: fix error when arguments are missing (python 3)
* Remove deprecated methods
* Implement managers to get access to resources
* Documentation improvements
* Add fork project support
* Deprecate the "old" Gitlab methods
* Add support for groups search

## v0.10 (2015-12-29)

* Implement pagination for list() (#63)
* Fix url when fetching a single MergeRequest
* Add support to update MergeRequestNotes
* API: Provide a Gitlab.from_config method
* setup.py: require requests>=1 (#69)
* Fix deletion of object not using 'id' as ID (#68)
* Fix GET/POST for project files
* Make 'confirm' an optional attribute for user creation
* Python 3 compatibility fixes
* Add support for group members update (#73)

## v0.9.2 (2015-07-11)

* CLI: fix the update and delete subcommands (#62)

## v0.9.1 (2015-05-15)

* Fix the setup.py script

## v0.9 (2015-05-15)

* Implement argparse library for parsing argument on CLI
* Provide unit tests and (a few) functional tests
* Provide PEP8 tests
* Use tox to run the tests
* CLI: provide a --config-file option
* Turn the gitlab module into a proper package
* Allow projects to be updated
* Use more pythonic names for some methods
* Deprecate some Gitlab object methods:
  * `raw*` methods should never have been exposed; replace them with `_raw_*` methods
  * setCredentials and setToken are replaced with set_credentials and set_token
* Sphinx: don't hardcode the version in `conf.py`

## v0.8 (2014-10-26)

* Better python 2.6 and python 3 support
* Timeout support in HTTP requests
* Gitlab.get() raised GitlabListError instead of GitlabGetError
* Support api-objects which don't have id in api response
* Add ProjectLabel and ProjectFile classes
* Moved url attributes to separate list
* Added list for delete attributes

## v0.7 (2014-08-21)

* Fix license classifier in `setup.py`
* Fix encoding error when printing to redirected output
* Fix encoding error when updating with redirected output
* Add support for UserKey listing and deletion
* Add support for branches creation and deletion
* Support state_event in ProjectMilestone (#30)
* Support namespace/name for project id (#28)
* Fix handling of boolean values (#22)

## v0.6 (2014-01-16)

* IDs can be unicode (#15)
* ProjectMember: constructor should not create a User object
* Add support for extra parameters when listing all projects (#12)
* Projects listing: explicitly define arguments for pagination

## v0.5 (2013-12-26)

* Add SSH key for user
* Fix comments
* Add support for project events
* Support creation of projects for users
* Project: add methods for create/update/delete files
* Support projects listing: search, all, owned
* System hooks can't be updated
* Project.archive(): download tarball of the project
* Define new optional attributes for user creation
* Provide constants for access permissions in groups

## v0.4 (2013-09-26)

* Fix strings encoding (Closes #6)
* Allow to get a project commit (GitLab 6.1)
* ProjectMergeRequest: fix Note() method
* Gitlab 6.1 methods: diff, blob (commit), tree, blob (project)
* Add support for Gitlab 6.1 group members

## v0.3 (2013-08-27)

* Use PRIVATE-TOKEN header for passing the auth token
* provide an AUTHORS file
* cli: support ssl_verify config option
* Add ssl_verify option to Gitlab object. Defaults to True
* Correct url for merge requests API.

## v0.2 (2013-08-08)

* provide a pip requirements.txt
* drop some debug statements

## v0.1 (2013-07-08)

* Initial release

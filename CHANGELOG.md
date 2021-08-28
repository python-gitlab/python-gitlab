# Changelog

<!--next-version-placeholder-->

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
* **api:** Add MR pipeline manager in favor of pipelines() method ([`954357c`](https://github.com/python-gitlab/python-gitlab/commit/954357c49963ef51945c81c41fd4345002f9fb98))
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

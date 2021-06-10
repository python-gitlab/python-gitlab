# Changelog

<!--next-version-placeholder-->

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

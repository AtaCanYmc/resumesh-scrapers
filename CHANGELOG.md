# Changelog

## [0.2.0](https://github.com/AtaCanYmc/resumesh-scrapers/compare/v0.1.0...v0.2.0) (2026-07-23)


### Features

* add Security Policy document and include Beautiful Soup as a dependency ([a05fe07](https://github.com/AtaCanYmc/resumesh-scrapers/commit/a05fe07993d186c39bdba742401ae2b94ee633da))
* arch improves ([91c5705](https://github.com/AtaCanYmc/resumesh-scrapers/commit/91c57052630463f3dae770706991893a2fa329f7))
* **behance:** add Behance scraper service and project model ([3cf9d26](https://github.com/AtaCanYmc/resumesh-scrapers/commit/3cf9d26923ca8f4ec1d58ed11214fdd1b7c74956))
* **behance:** enhance project card selectors and add tests for BehanceScraperService ([ea45cde](https://github.com/AtaCanYmc/resumesh-scrapers/commit/ea45cdef07b57162d280f7b983b226f532db4c84))
* **docs:** update README and __init__.py for new scraper services and improved architecture ([4f01c71](https://github.com/AtaCanYmc/resumesh-scrapers/commit/4f01c713e10c9eabff2cf9c6845e1aba386448b2))
* **errors:** add custom exceptions for NPM and PyPI scraper services ([b861bfb](https://github.com/AtaCanYmc/resumesh-scrapers/commit/b861bfb708ada95471e3f9392c77e2fb9a57a1da))
* **github:** implement repository parsing logic and update model field names ([fe45a7b](https://github.com/AtaCanYmc/resumesh-scrapers/commit/fe45a7ba82df4bb464137a9703e4309593ed61bb))
* **init:** add Behance and Substack scraper services to the module ([b7ec1b8](https://github.com/AtaCanYmc/resumesh-scrapers/commit/b7ec1b84364ba202ee1f76cda370363b8d2793c3))
* **init:** add NPM and PyPI scraper services to the module ([5e56627](https://github.com/AtaCanYmc/resumesh-scrapers/commit/5e56627bd7aa1fbb9c43bcbfb588b29c5cae7801))
* **models:** add Pydantic models for article platforms, Behance, GitHub, npm, and PyPI ([428ddaf](https://github.com/AtaCanYmc/resumesh-scrapers/commit/428ddaf50ac4412a3f349977d40e567da189a387))
* **npm, pypi:** add NPM and PyPI scraper services with models for package data ([9966048](https://github.com/AtaCanYmc/resumesh-scrapers/commit/9966048654cb652fdf4ee505572c74b07892bf64))
* **npm:** add custom exceptions for NPM scraper and set default for yanked field ([1587e20](https://github.com/AtaCanYmc/resumesh-scrapers/commit/1587e20a6d251884f754f6b70bddda031cab86a7))
* **scrapers:** add Behance, Dev.to, GitHub, Medium, npm, PyPI, and Substack scrapers with logging ([bdeca09](https://github.com/AtaCanYmc/resumesh-scrapers/commit/bdeca096c1a5bcc91a0fd9053edc61cc58c0d485))
* **scrapers:** extend example script to include npm and PyPI data fetching ([6b5e365](https://github.com/AtaCanYmc/resumesh-scrapers/commit/6b5e365473f4c8c1da04df0b0ce832ae27e96702))
* **substack:** implement Substack scraper service and error handling ([5444cc7](https://github.com/AtaCanYmc/resumesh-scrapers/commit/5444cc7c36897c6b195267685b9019da177eb551))


### Bug Fixes

* correct URL formatting in API requests for Dev.to and GitHub scrapers ([66f380b](https://github.com/AtaCanYmc/resumesh-scrapers/commit/66f380b55b90774b5d46e5191160825be38a9253))

## 0.1.0 (2026-07-14)


### Features

* add initial tests for DevTo, GitHub, and Medium scrapers ([556f5cc](https://github.com/AtaCanYmc/resumesh-scrapers/commit/556f5cc70f591c9c8974d7570a2482f94fbba006))
* **ci:** add continuous deployment workflow for publishing to PyPI and TestPyPI ([4b2a9ec](https://github.com/AtaCanYmc/resumesh-scrapers/commit/4b2a9ecb565a1c3ea98fb48c1662550ed2449bb1))
* **ci:** add linting and build steps to CI configuration ([82298f6](https://github.com/AtaCanYmc/resumesh-scrapers/commit/82298f6e1bdf372748c67dd61a2348ec00c41c81))


### Bug Fixes

* **tests:** update network error handling in DevTo and Medium scraper tests ([0e25207](https://github.com/AtaCanYmc/resumesh-scrapers/commit/0e25207152ad8ba7107309c6053a07fc911434d1))

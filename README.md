autopush integration tests
============================

Automated tests for the autopush server.

[![license](https://img.shields.io/badge/license-MPL%202.0-blue.svg)](https://github.com/rpappalax/autopush-integration-tests/tree/master#license)
[![travis](https://img.shields.io/travis/rpappalax/autopush-integration-tests.svg?label=travis)](http://travis-ci.org/rpappalax/autopush-integration-tests/)
[![updates](https://pyup.io/repos/github/rpappalax/autopush-integration-tests/shield.svg)](https://pyup.io/repos/github/rpappalax/autopush-integration-tests)
[![Python 3](https://pyup.io/repos/github/rpappalax/autopush-integration-tests/python-3-shield.svg)](https://pyup.io/repos/github/rpappalax/autopush-integration-tests/)


Summary
---------

A variety of tests are used to verify the integrity of [Mozilla's autopush service](https://autopush.readthedocs.io/)].
This repository contains integration tests used largely for deployment verification.

Other tests / test tools used for testing autopush include:
For API testing: [ap-loadtester](https://github.com/mozilla-service/ap-loadtester) 
For loadtesting (API testing at scale): [ardere](https://github.com/loads/ardere) 


autopush integration tests will live here.  For now, use bash scripts in /scripts for
manual verification of push deployment


Setup
---------

* make install

Run Tests
---------

* make test 

Docker
---------

If you want to run/deploy tests inside a docker container, you will need to have Docker installed locally.
Then:

* make docker-build
* make docker-test

Optionally, push a tag to DockerHub:

* make docker-tag
* make docker-push


Jenkins
-------

These tests can run on Jenkins as defined in [Jenkinsfile](Jenkinsfile).
The tests are invoked by Jenkins with the parameterized command defined in this [run](run) file.
The Jenkins pipeline job should be with the following syntax:  <project-name>.<test-type>.<test-environment>
Example:  autopush.integration-tests.stage


License
-------
This software is licensed under the [MPL] 2.0:

    This Source Code Form is subject to the terms of the Mozilla Public
    License, v. 2.0. If a copy of the MPL was not distributed with this
    file, You can obtain one at http://mozilla.org/MPL/2.0/.

[MPL]: http://www.mozilla.org/MPL/2.0/

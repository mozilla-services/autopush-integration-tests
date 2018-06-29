autopush integration tests
============================

Automated tests for the autopush server.

[![license](https://img.shields.io/badge/license-MPL%202.0-blue.svg)](https://github.com/mozilla-services/autopush-integration-tests/tree/master#license)
[![travis](https://img.shields.io/travis/mozilla-services/autopush-integration-tests.svg?label=travis)](http://travis-ci.org/mozilla-services/autopush-integration-tests/)
[![updates](https://pyup.io/repos/github/mozilla-services/autopush-integration-tests/shield.svg)](https://pyup.io/repos/github/mozilla-services/autopush-integration-tests)
[![Python 3](https://pyup.io/repos/github/mozilla-services/autopush-integration-tests/python-3-shield.svg)](https://pyup.io/repos/github/mozilla-services/autopush-integration-tests/)


Summary
---------

A variety of tests are used to verify the integrity of [Mozilla's autopush service](https://autopush.readthedocs.io/).
This repository contains integration tests used largely for deployment verification.

Other tests / test tools used for testing autopush include:
For API testing: [ap-loadtester](https://github.com/mozilla-service/ap-loadtester)



Setup
---------

This repository uses [Pipenv](https://pipenv.readthedocs.io/en/latest/)
to manage it's Python dependencies. Please follow the directions from Pipenv
on how to install it.

Once Pipenv is installed:

* Use the command `pipenv install` to create a Python virtual environment and
install the required dependencies
* Once the virtual environment is created, use the command `pipenv shell`
to use the virtual environment


Run Tests
---------

To run the current set of tests, please use the following command:

`pytest -v --env=<ENV> --api-version=<API_VERSION> tests/`

* `<ENV>` is `stage`, `production`, or `dev` depending on what
environment you are testing.

If you want the results of this testrun to be recorded to our TestRail
instance, please check the output of `pytest -h` to get a list
of the values that will need to be passed in as additional
parameters.

License
-------
This software is licensed under the [MPL] 2.0:

    This Source Code Form is subject to the terms of the Mozilla Public
    License, v. 2.0. If a copy of the MPL was not distributed with this
    file, You can obtain one at http://mozilla.org/MPL/2.0/.

[MPL]: http://www.mozilla.org/MPL/2.0/

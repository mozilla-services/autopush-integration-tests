import datetime
import ipgetter
import pytest
from pytest_testrail.plugin import pytestrail

from tests.client import request_rest
from tests.sentry import (issue_resolve_all, issue_items)
from tests.timeout import verify_timeout
from conftest import (HOST_UPDATES, ISSUE_TITLE, SENTRY_TOKEN, log)


TIMEOUT = 300


@pytest.fixture
def project_slug(env):
    return 'autopush-{0}'.format(env)


@pytest.fixture
def assert_ok(msg='assert OK'):
    print(msg)
    return True


@pytest.fixture
def test_setup(env, project_slug):
    log.header('SETUP')
    print('resolving any LogCheckErrors before testing')
    issue_resolve_all(ISSUE_TITLE, SENTRY_TOKEN, project_slug)


@pytest.fixture
def test_teardown(env, project_slug):
    log.header('TEARDOWN')
    print('resolving any LogCheckErrors post testing')
    issue_resolve_all(ISSUE_TITLE, SENTRY_TOKEN, project_slug)


@pytest.mark.timeout(TIMEOUT)
@pytestrail.case('C10692')
def test_sentry_check(request, release_version, env, project_slug): # noqa
    """Verifies autopush Sentry error trigger mechanism is working end-2-end

    STEPS:
    1. Force an error on autopush server
    2. get latest release number from github.com/mozilla-services/autopush
    3. Verify that error info is being properly logged to Sentry from
       autopush server in a timely way
    """

    test_setup(env, project_slug)

    log.header('AUTOPUSH HOST')
    print('Force and verify error on autopush host')

    url = 'https://{0}/v1/err/crit'.format(HOST_UPDATES)
    UTC_NOW = datetime.datetime.utcnow()
    resp = request_rest(url, 'GET')

    assert resp['message'] == 'FAILURE:Success' and \
        assert_ok('FAILURE:Success'), 'Forced /err/crit unsuccessful!'
    assert resp['error'] == 'Test Failure' and \
        assert_ok('Test Failure - OK'), 'Unexpected error message!'

    log.header('SENTRY HOST')
    print('Verify error logs on Sentry host')

    issues = issue_items(ISSUE_TITLE, project_slug)

    for item in issues:

        # verify error originates from this host
        # (autopush will post originator's IP to Sentry)
        if item[0] == 'remote_ip':
            ip_ext = ipgetter.myip()
            ip_remote = item[1]
            assert ip_ext == ip_remote and \
                assert_ok('IP address match!'), \
                'IP addresses don\'t match!'

        if item[0] == 'release_project_name':
            release_project_name = item[1]
            assert release_project_name == project_slug and \
                assert_ok('Project slug matches!'), \
                'Project slug doesn\'t match!'

        if item[0] == 'release_version':
            release_version_sentry = item[1]
            release_version_github = release_version
            assert release_version_sentry == release_version_github and \
                assert_ok('Release version matches!'), \
                'Release version doesn\'t match!'

        # verify error event falls within allowable time boundary
        # of test start
        if item[0] == 'last_event':
            sentry_last_event = item[1]
            time_verified = verify_timeout(UTC_NOW, sentry_last_event)
            assert time_verified and \
                assert_ok('Last event within time boundary!'), \
                'Last event not within time boundary!'

    test_teardown(env, project_slug)

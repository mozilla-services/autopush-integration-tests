import datetime
import ipgetter
import pytest

from tests.client import request_rest
from tests.sentry import (
    issue_resolve_all,
    issue_items,
)
from tests.timeout import verify_timeout
from conftest import (ISSUE_TITLE, SENTRY_TOKEN, PROJECT_SLUG, log)


class TestSentry(object):

    @classmethod
    def setup_class(cls):
        log.header('SETUP')
        print('resolving any LogCheckErrors before testing')
        issue_resolve_all(ISSUE_TITLE, SENTRY_TOKEN, PROJECT_SLUG)

    @classmethod
    def teardown_class(cls):
        pass

    def assert_ok(self, msg='assert OK'):
        print(msg)
        return True

    @pytest.mark.nondestructive
    def test_sentry_check(self, variables, request, release_version): # noqa
        """ Force an error on autopush server, then check that
        it gets logged to Sentry. """

        log.header('AUTOPUSH HOST')
        print('Force and verify error on autopush host')

        url_push_host_updates = variables['HOST_UPDATES']
        url = 'https://{0}/v1/err/crit'.format(url_push_host_updates)
        UTC_NOW = datetime.datetime.utcnow()
        resp = request_rest(url, 'GET')

        assert resp['message'] == 'FAILURE:Success' and \
            self.assert_ok('FAILURE:Success'), \
            'Forced /err/crit unsuccessful!'
        assert resp['error'] == 'Test Failure' and \
            self.assert_ok('Test Failure - OK'), \
            'Unexpected error message!'

        log.header('SENTRY HOST')
        print('Verify error logs on Sentry host')

        issues = issue_items(variables, PROJECT_SLUG, ISSUE_TITLE)
        for item in issues:
            # verify error originates from this host
            if item[0] == 'remote_ip':
                ip_ext = ipgetter.myip()
                ip_remote = item[1]
                assert ip_ext == ip_remote and \
                    self.assert_ok('IP address match!'), \
                    'IP addresses don\'t match!'
            # verify release_project_name
            if item[0] == 'release_project_name':
                release_project_name = item[1]
                assert release_project_name == PROJECT_SLUG and \
                    self.assert_ok('Project slug matches!'), \
                    'Project slug doesn\'t match!'
            # verify autopush release_version
            if item[0] == 'release_version':
                release_version_sentry = item[1]
                release_version_github = release_version
                assert release_version_sentry == release_version_github and \
                    self.assert_ok('Release version matches!'), \
                    'Release version doesn\'t match!'
            # verify this event falls within an allowable time boundary
            # of test start
            if item[0] == 'last_event':
                sentry_last_event = item[1]
                time_verified = verify_timeout(UTC_NOW, sentry_last_event)
                assert time_verified and \
                    self.assert_ok('Last event within time boundary!'), \
                    'Last event not within time boundary!'

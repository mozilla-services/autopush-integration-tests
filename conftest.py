import os
import pytest
from outlawg import Outlawg
import requests


GITHUB_ORG = 'mozilla-services'
GITHUB_REPO = 'autopush'
PROJECT_SLUG = 'autopush-stage'
ISSUE_TITLE = 'LogCheckError: LogCheck'
SENTRY_TOKEN = os.environ['SENTRY_TOKEN']
HOST_SENTRY = os.environ['HOST_SENTRY']


log = Outlawg()


class NotFoundError(Exception):
    def __init__(self, url):
        err_header = self.output.get_header('ERROR')
        err_msg = '{0}\nNothing found at: \n{1}\nABORTING!\n\n'.format(err_header, url)  # noqa
        Exception.__init__(err_msg)


def get_tags(url):
    """Get all tags as json from Github API."""

    req = requests.get(url)
    try:
        if 'Not Found' in req.text:
            raise NotFoundError(url)
    except NotFoundError():
        pass
    else:
        return req


@pytest.fixture(scope='session')
def release_version():
    # print('Call github API for release tag')
    log.header('GITHUB API')
    print('get release tag')
    url = 'https://api.github.com/repos/{0}/{1}/releases/latest'.format(GITHUB_ORG, GITHUB_REPO)  # noqa
    req = get_tags(url)
    return req.json()['tag_name']

import os
import configparser
import ssl

from outlawg import Outlawg
import pytest
import requests


GITHUB_API = 'api.github.com'
GITHUB_ORG = 'mozilla-services'
GITHUB_REPO = 'autopush'
ISSUE_TITLE = 'LogCheckError: LogCheck'
SENTRY_TOKEN = os.environ['SENTRY_TOKEN']
HOST_SENTRY = os.environ['HOST_SENTRY']
HOST_UPDATES = os.environ['HOST_UPDATES']


log = Outlawg()


class NotFoundError(Exception):
    def __init__(self, url):
        err_header = self.output.get_header('ERROR')
        err_msg = '{0}\nNothing found at: \n{1}\nABORTING!\n\n'.format(err_header, url)  # noqa
        Exception.__init__(err_msg)


# Hack because of how SSL certificates are verified by default in Python
if hasattr(ssl, '_create_unverified_context'):
    ssl._create_default_https_context = ssl._create_unverified_context


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


@pytest.fixture()
def env(request):
    return request.config.getoption("--env")


@pytest.fixture()
def api_version(request):
    return request.config.getoption("--api-version")


@pytest.fixture()
def conf():
    config = configparser.ConfigParser()
    config.read('manifest.ini')
    return config


@pytest.fixture(scope='session')
def release_version():
    log.header('GITHUB API')
    print('get latest {0} release tag'.format(GITHUB_REPO))
    url = 'https://{0}/repos/{1}/{2}/releases/latest'.format(GITHUB_API, GITHUB_ORG, GITHUB_REPO)  # noqa
    req = get_tags(url)
    return req.json()['tag_name']


def pytest_addoption(parser):
    parser.addoption(
        "--env",
        dest="env",
        default="stage",
        help="Environment tests are running in: dev | stage | prod"
    )
    parser.addoption(
        "--api-version",
        dest="apiversion",
        default="0.0.0",
        help="Version of the autopush service API we are testing against"
    )

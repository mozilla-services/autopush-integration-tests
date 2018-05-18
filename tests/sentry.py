import json

from tests.client import request_rest
from conftest import (HOST_SENTRY, SENTRY_TOKEN)


ORGANIZATION = 'operations'


def format_json(j):
    return json.dumps(j, indent=4)


def remote_ip(client_info):
    """Parse external IP from 'remote_ip' params
    NOTE:
        the json for this section in the Sentry API is inexplicably
    double-wrapped in additional quotes, hence the heinous parsing"""

    IP_INTERNAL_PREFIX = ['10', '172', '192']
    remote_ips = client_info.replace("'", '').replace(' ', '').split(',')

    for item in remote_ips:
        if item.split('.')[0] not in IP_INTERNAL_PREFIX:
            return item
    return 'IP NOT FOUND'


def url_projects_list():
    return '{0}/api/0/projects/'.format(HOST_SENTRY)


def url_issues_list(project_slug):
    return '{0}/api/0/projects/{1}/{2}/issues/'.format(
        HOST_SENTRY, ORGANIZATION, project_slug)


def url_issue_update(num_issue):
    return '{0}/api/0/issues/{1}/'.format(HOST_SENTRY, num_issue)


def url_organizations():
    return '{0}/api/0/url_organizations/{1}/projects/'.format(
        HOST_SENTRY, ORGANIZATION)


def issue_id_latest(issue_title, SENTRY_TOKEN, project_slug):
    url = url_issues_list(project_slug)
    issues = request_rest(url, 'GET', SENTRY_TOKEN)

    for issue in issues:
        if issue['title'] == issue_title:
            return issue['id']
        else:
            return None


def issue_items(issue_title, project_slug):
    # TODO: convert this list of lists into a dict
    """Gather the issue items we wish to verify into a single list"""
    params = []
    issue_id = issue_id_latest(issue_title, SENTRY_TOKEN, project_slug)
    url = '{0}/api/0/issues/{1}/'.format(HOST_SENTRY, issue_id)
    resp = request_rest(url, 'GET', SENTRY_TOKEN)

    params.append(['release_project_name', resp['project']['name']])
    params.append(['release_version', resp['lastRelease']['version']])
    params.append(['last_event', resp['lastRelease']['lastEvent']])
    params.append(['error_value', resp['metadata']['value']])
    params.append(['error_type', resp['metadata']['type']])

    # remote_ip only available from events_latest, hence another query to API
    url = '{0}/api/0/issues/{1}/events/latest/'.format(HOST_SENTRY, issue_id)
    resp = request_rest(url, 'GET', SENTRY_TOKEN)
    r = resp['context']['client_info']["'remote_ip'"]

    # NOTE: remote_ip is sadly double-quoted on the Sentry API
    ip = remote_ip(r)
    params.append(['remote_ip', ip])
    return params


def issue_resolve_all(issue_title, SENTRY_TOKEN, project_slug):
    url = url_issues_list(project_slug)
    issues = request_rest(url, 'GET', SENTRY_TOKEN)
    resp = format_json(issues)

    for issue in issues:
        if issue['title'] == issue_title:
            url = url_issue_update(issue['id'])
            resp = request_rest(
                url, 'PUT', SENTRY_TOKEN, {"status": "resolved"})
            resp = format_json(resp)
    return resp


def issues_list_all(SENTRY_TOKEN, project_slug):
    url = url_issues_list(project_slug)
    resp = request_rest(url, 'GET', SENTRY_TOKEN)
    return json.dumps(resp, indent=4)

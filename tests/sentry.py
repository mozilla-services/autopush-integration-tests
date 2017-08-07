import json

from tests.client import request_rest
from conftest import (HOST_SENTRY, SENTRY_TOKEN)


ORGANIZATION = 'operations'


def format_json(j):
    return json.dumps(j, indent=4)


def url_projects_list():
    return '{0}/api/0/projects/'.format(HOST_SENTRY)


def url_issues_list(PROJECT_SLUG):
    return '{0}/api/0/projects/{1}/{2}/issues/'.format(
        HOST_SENTRY, ORGANIZATION, PROJECT_SLUG)


def url_issue_update(num_issue):
    return '{0}/api/0/issues/{1}/'.format(HOST_SENTRY, num_issue)


def url_organizations():
    return '{0}/api/0/url_organizations/{1}/projects/'.format(
        HOST_SENTRY, ORGANIZATION)


def issue_id_latest(project_slug, issue_title, SENTRY_TOKEN):
    url = url_issues_list(project_slug)
    issues = request_rest(url, 'GET', SENTRY_TOKEN)

    for issue in issues:
        if issue['title'] == issue_title:
            return issue['id']
        else:
            return None


def issue_items(variables, project_slug, issue_title):
    params = []
    ip = ''
    issue_id = issue_id_latest(project_slug, issue_title, SENTRY_TOKEN)
    url = '{0}/api/0/issues/{1}/events/latest/'.format(HOST_SENTRY, issue_id)
    resp = request_rest(url, 'GET', SENTRY_TOKEN)
    params.append(['release_project_name',
                  resp['release']['projects'][0]['name']])
    params.append(['release_version',
                  resp['release']['version']])
    params.append(['last_event', resp['release']['lastEvent']])
    params.append(['error_value', resp['metadata']['value']])
    params.append(['error_type', resp['metadata']['type']])
    r = resp['context']['client_info']
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


def string_clean(s):
        s = str(s)
        return s.replace('"', '').replace("'", "")


def remote_ip(obj_client_info):
    remote_ip = []
    for key, val in obj_client_info.iteritems():
        key_new = string_clean(key)
        val_new = string_clean(val)
        if key_new == 'remote_ip':
            ips = val_new.split(',')
            remote_ip = [ip for ip in ips if '172' not in ip]
    return remote_ip[0]

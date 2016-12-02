import os
import pytest
import requests
from ticket_helper import format_results, ticket_update


def api_response(variables, path):
    URL = 'https://{0}/{1}'.format(variables['HOST_UPDATES'], path)
    return requests.get(URL)


@pytest.mark.nondestructive
def test_status_check(variables, ticket_num, request):
    name_test = request.node.name
    status = api_response(variables, 'status').json()
    assert('OK' == status['status'])
    assert(variables['VERSION'] == status['version'])
    ticket_update(name_test, ticket_num, status)


@pytest.mark.nondestructive
def test_health_check(variables, ticket_num, request):
    name_test = request.node.name
    r = api_response(variables, 'health')
    status = r.json()
    ROUTER = variables['ROUTER']
    STORAGE = variables['STORAGE']

    assert(0 == status['clients'])
    assert('OK' == status[ROUTER]['status'])
    assert('OK' == status[STORAGE]['status'])
    assert('OK' == status['status'])
    assert(variables['VERSION'] == status['version'])
    ticket_update(name_test, ticket_num, status)

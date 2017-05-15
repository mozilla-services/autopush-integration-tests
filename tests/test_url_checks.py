import pytest
import requests
from tests.ticket_helper import format_results
import globals as gbl


def api_response(variables, path):
    URL = 'https://{0}/{1}'.format(variables['HOST_UPDATES'], path)
    return requests.get(URL)


def ticket_update(name_test, status):
    print('UPDATING TICKET #{0}'.format(gbl.ticket_num))
    comments = format_results(name_test, status)
    print(comments)


@pytest.mark.nondestructive
def test_status_check(variables, request):
    name_test = request.node.name
    status = api_response(variables, 'status').json()
    assert('OK' == status['status'])
    assert(gbl.release_num == status['version'])
    if gbl.ticket_num:
        ticket_update(gbl.ticket_num, name_test, status)


@pytest.mark.nondestructive
def test_health_check(variables, request):
    name_test = request.node.name
    status = api_response(variables, 'health').json()
    ROUTER = variables['ROUTER']
    STORAGE = variables['STORAGE']

    assert(0 == status['clients'])
    assert('OK' == status[ROUTER]['status'])
    assert('OK' == status[STORAGE]['status'])
    assert('OK' == status['status'])
    assert(gbl.release_num == status['version'])
    if gbl.ticket_num:
        ticket_update(gbl.ticket_num, name_test, status)

import pytest
import requests

#HOST = 'autopush.stage.mozaws.net'
#HOST_UPDATES = 'updates-autopush.stage.mozaws.net'
#ROUTER = 'stage.autopush.routerv2'
#STORAGE = 'stage.autopush.storage'


@pytest.mark.nondestructive
def test_status(variables):
    #URL = 'https://{0}/status'.format(HOST_UPDATES)
    URL = 'https://{0}/status'.format(variables['HOST_UPDATES'])
    r = requests.get(URL)
    status = r.json()
    assert('OK' == status['status'])
    assert(release_num == status['version'])


@pytest.mark.nondestructive
def test_health(variables):
    # demo_param = request.config.getoption('demo_param')
    #URL = 'https://{0}/health'.format(HOST_UPDATES)
    ROUTER = variables['ROUTER']
    STORAGE = variables['STORAGE']
    URL = 'https://{0}/health'.format(variables['HOST_UPDATES'])
    r = requests.get(URL)
    status = r.json()

    assert(0 == status['clients'])
    assert('OK' == status[ROUTER]['status'])
    assert('OK' == status[STORAGE]['status'])
    assert('OK' == status['status'])
    assert(release_num == status['version'])

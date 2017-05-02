# use pytest variables plugin
# json, or yaml files
# has object with keys/vals
# mult files: dev, stage,
# --variables=stage.json
# must specify on the command line
# json file top level keys are dev, stage, prod
# could create own hook in pytest suite to call: "env=dev"
#


import pytest
import requests

# INPUTS
# VERSION = '1.20.0'
# VERSION = variables['VERSION']

# STAGE
HOST = 'autopush.stage.mozaws.net'
HOST_UPDATES = 'updates-autopush.stage.mozaws.net'
ROUTER = 'stage.autopush.routerv2'
STORAGE = 'stage.autopush.storage'


@pytest.mark.nondestructive
def test_status(variables):
    URL = 'https://{0}/status'.format(HOST_UPDATES)
    r = requests.get(URL)
    status = r.json()
    assert('OK' == status['status'])
    assert(variables['VERSION'] == status['version'])
    # assert(VERSION == status['version'])


@pytest.mark.nondestructive
def test_health(variables):
    # demo_param = request.config.getoption('demo_param')
    URL = 'https://{0}/health'.format(HOST_UPDATES)
    r = requests.get(URL)
    status = r.json()

    assert(0 == status['clients'])
    assert('OK' == status[ROUTER]['status'])
    assert('OK' == status[STORAGE]['status'])
    assert('OK' == status['status'])
    assert(variables['VERSION'] == status['version'])
    # assert(VERSION == status['version'])

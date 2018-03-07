import requests

from pytest_testrail.plugin import pytestrail


@pytestrail.case('C10691')
def test_status_endpoint(api_version, conf, env):
    response = requests.get(conf.get(env, 'server_url') + "/status")
    data = response.json()
    assert 'status' in data
    assert 'version' in data
    assert data['status'] == 'OK'

    if api_version != '0.0.0':
        assert api_version == data['version']

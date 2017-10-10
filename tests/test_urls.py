import requests


def test_health(api_version, conf, env):
    response = requests.get(conf.get(env, 'server_url') + "/health")
    router = conf.get(env, 'router')
    data = response.json()

    assert 'version' in data
    assert 'clients' in data

    if api_version != '0.0.0':
        assert api_version == data['version']

    assert data[router]['status'] == 'OK'
    assert data['storage']['status'] == 'OK'


def test_status(api_version, conf, env):
    response = requests.get(conf.get(env, 'server_url') + "/status")
    data = response.json()
    assert 'status' in data
    assert 'version' in data
    assert data['status'] == 'OK'

    if api_version != '0.0.0':
        assert api_version == data['version']

import requests


def test_health(apiversion, conf, env):
    response = requests.get(conf.get(env, 'server_url') + "/health")
    router = conf.get(env, 'router')
    data = response.json()

    assert 'version' in data
    assert 'clients' in data

    if apiversion != '0.0.0':
        assert apiversion == data['version']

    assert data[router]['status'] == 'OK'
    assert data['storage']['status'] == 'OK'


def test_status(apiversion, conf, env):
    response = requests.get(conf.get(env, 'server_url') + "/status")
    data = response.json()
    assert 'status' in data
    assert 'version' in data
    assert data['status'] == 'OK'

    if apiversion != '0.0.0':
        assert apiversion == data['version']

import requests


def test_generate_logcheck_error(conf, env):
    response = requests.get(conf.get(env, 'server_url') + "/v1/err/crit")
    data = response.json()

    assert data['code'] == 418
    assert data['errno'] == 999
    assert data['error'] == 'Test Failure'
    assert data['message'] == 'FAILURE:Success'

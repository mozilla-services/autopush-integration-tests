import json
import requests


def test_status_endpoint(api_version, conf, env):
    response = requests.get(conf.get(env, "server_url") + "/status")
    data = response.json()
    assert "status" in data
    assert "version" in data
    assert data["status"] == "OK"

    if api_version != "0.0.0":
        assert api_version == data["version"]


def test_rs_status_endpoint(rs_api_version, conf, env):
    response = requests.get(conf.get(env, "rs_server_url") + "/__version__")
    data = json.loads(response.json())
    print(data)

    if rs_api_version != "0.0.0":
        assert rs_api_version == data["version"]

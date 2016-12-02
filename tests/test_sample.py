import requests


HOST_UPDATES = 'updates-autopush.stage.mozaws.net'


def func(x):
    return x + 1


class DemoTest:

    def test_answer(self, variables):
        host = variables['HOST_UPDATES']
        print(host)
        assert func(3) == 4

    def test_status(self, variables):
        URL = 'https://{0}/status'.format(HOST_UPDATES)
        r = requests.get(URL)
        status = r.json()
        print(status)
        # assert(status['status'] == 'OK')

"""Request handler for Sentry"""
import json
import time
import requests


WAIT = 7


class UnsupportedMethodError(Exception):
    def __init__(self, method):
        msg = 'ERROR! REST method: {0} - unsupported. Aborting!'.format(method)
        Exception.__init__(self, msg)


def request_rest(url, method='GET', auth='', data=''):

    headers = {'Content-Type': 'application/json'}

    if method == 'GET':
        r = requests.get(url, auth=(auth, ''))
    elif method == 'DELETE':
        r = requests.delete(url, auth=(auth, ''), headers=headers)
    elif method == 'PUT':
        r = requests.put(
            url,
            auth=(auth, ''),
            data=json.dumps(data),
            headers=headers
        )
    else:
        raise UnsupportedMethodError(method)

    # Sentry occasionally lags. Allow some time for update.
    time.sleep(WAIT)
    try:
        return r.json()
    except ValueError as e:
        import pprint
        print('----------------------')
        pprint.pprint(r.text)
        print('----------------------')
        return json.loads(r)

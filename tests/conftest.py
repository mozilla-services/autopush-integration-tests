# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os

import pytest


@pytest.fixture(scope='session')
def ticket_num(request):
    """Returns the ticket number"""
    config = request.config
    return config.getoption('ticket_num')


def pytest_addoption(parser):
    parser.addini('ticket_num', help='Ticket number')
    parser.addoption(
        '--ticket-num',
        metavar='ticket',
        default=os.getenv('TICKET_NUM', None),
        help='Ticket number the tests should use')

import os
import pytest

import globals as gbl


@pytest.fixture(scope='session')
def rel_num():
    gbl.release_num = ''


@pytest.fixture(scope='session')
def ticket_num():
    """Returns the ticket number"""
    # config = request.config
    # return config.getoption('ticket_num')
    gbl.ticket_num = '12345668'


def pytest_addoption(parser):
    parser.addini('ticket_num', help='Ticket number')
    parser.addoption(
        '--ticket-num',
        metavar='ticket',
        default=os.getenv('TICKET_NUM', None),
        help='Ticket number the tests should use')

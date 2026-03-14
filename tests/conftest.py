#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

from os import path
from codecs import open

import pytest
import responses
from click.testing import CliRunner


ROOT = path.join(path.dirname(path.abspath(__file__)), 'responses')


@pytest.fixture
def mock_api():
    # The responses library returns mocked responses in FIFO order for the
    # same URL. The order here must match the order of calls in the tests.

    # 1st sign call: mission not yet done -> redeem -> get balance
    with open(path.join(ROOT, 'mission_todo.html'), encoding='utf-8') as f:
        mock_mission_todo_body = f.read()
    responses.add(responses.GET, 'https://www.v2ex.com/mission/daily',
                  body=mock_mission_todo_body)
    with open(path.join(ROOT, 'once.html'), encoding='utf-8') as f:
        mock_once_body = f.read()
    responses.add(responses.GET, 'https://www.v2ex.com/mission/daily/redeem?once=51947',
                  body=mock_once_body)
    with open(path.join(ROOT, 'balance.html'), encoding='utf-8') as f:
        mock_balance_body = f.read()
    responses.add(responses.GET, 'https://www.v2ex.com/balance',
                  body=mock_balance_body)

    # 2nd sign call: mission already completed today
    with open(path.join(ROOT, 'mission_complete.html'), encoding='utf-8') as f:
        mock_mission_body = f.read()
    responses.add(responses.GET, 'https://www.v2ex.com/mission/daily',
                  body=mock_mission_body)

    responses.start()
    yield responses
    responses.stop()
    responses.reset()


@pytest.fixture(scope='function')
def runner(mock_api):
    return CliRunner()

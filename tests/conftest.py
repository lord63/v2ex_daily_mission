#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

from os import path
from codecs import open

import pytest
import responses
from click.testing import CliRunner


ROOT = path.join(path.dirname(path.abspath(__file__)), 'responses')


@pytest.yield_fixture
def mock_api():

    with open(path.join(ROOT, 'signin.html'), encoding='utf-8') as f:
        mock_signin_body = f.read()
    responses.add(responses.POST, 'https://www.v2ex.com/signin',
                  body=mock_signin_body)
    responses.add(responses.GET, 'https://www.v2ex.com/signin',
                  body=mock_signin_body)

    with open(path.join(ROOT, 'once.html'), encoding='utf-8') as f:
        mock_once_body = f.read()
    responses.add(responses.GET,
                  'https://www.v2ex.com/mission/daily/redeem?once=51947',
                  body=mock_once_body)

    with open(path.join(ROOT, 'balance.html'), encoding='utf-8') as f:
        mock_balance_body = f.read()
    responses.add(responses.GET, 'https://www.v2ex.com/balance',
                  body=mock_balance_body)

    with open(path.join(ROOT, 'mission.html'), encoding='utf-8') as f:
        mock_mission_body = f.read()
    responses.add(responses.GET, 'https://www.v2ex.com/mission/daily',
                  body=mock_mission_body)

    responses.start()
    yield responses
    responses.stop()


@pytest.fixture(scope='function')
def runner(mock_api):
    return CliRunner()

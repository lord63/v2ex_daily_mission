#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Tests for getting the right params to sign in
"""

from __future__ import absolute_import

import json
import re

import pytest

from v2ex_daily_mission.v2ex import V2ex


@pytest.mark.usefixtures('mock_api')
class TestLast():
    def test_sign(self, runner):
        with open('./v2ex_config.json') as f:
            config = json.loads(f.read())
        v2ex = V2ex(config)
        response = v2ex.session.get(v2ex.signin_url, verify=False)
        assert v2ex._get_captcha_url(response.text) == 'https://www.v2ex.com/_captcha?once=94612'

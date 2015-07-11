#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Tests for the `v2ex last` function
"""

from __future__ import absolute_import, unicode_literals

import pytest

from v2ex_daily_mission.cli import cli


@pytest.mark.usefixtures('mock_api')
class TestGetMoney():
    def test_get_money(self, runner):
        result = runner.invoke(cli, ['--config', './tests/v2ex_config.json',
                                     'sign'])
        assert result.exit_code == 0
        assert result.output.strip() == (
            'You have completed the mission today.')

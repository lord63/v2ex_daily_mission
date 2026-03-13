#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Tests for the `v2ex sign` function
"""

from __future__ import absolute_import

from unittest import mock

import pytest

from v2ex_daily_mission.cli import cli


@pytest.mark.usefixtures('mock_api')
class TestGetMoney():
    # balance.html: nth-of-type(2) selects the row with date 20150620
    @mock.patch('v2ex_daily_mission.v2ex.V2ex._today', return_value='20150620')
    def test_get_money(self, mock_today, runner):
        result = runner.invoke(
            cli, ['--config', './tests/v2ex_config.json', 'sign'])
        assert result.exit_code == 0
        assert "Today:" in result.output
        assert "Total:" in result.output

        result = runner.invoke(
            cli, ['--config', './tests/v2ex_config.json', 'sign'])
        assert result.exit_code == 0
        assert result.output.strip() == "You have completed the mission today."

    @mock.patch('v2ex_daily_mission.v2ex.V2ex._today', return_value='20260314')
    def test_cookie_expired(self, mock_today, runner):
        result = runner.invoke(
            cli, ["--config", "./tests/v2ex_config.json", "sign"])
        assert "cookie expired" in result.output

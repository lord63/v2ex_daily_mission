#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Tests for the `v2ex last` function
"""

from __future__ import absolute_import

import re

import pytest

from v2ex_daily_mission.cli import cli


@pytest.mark.usefixtures('mock_api')
class TestLast():
    def test_last(self, runner):
        result = runner.invoke(cli, ['--config', './tests/v2ex_config.json',
                                     'last'])
        day = int(re.search(r'\d+', result.output).group())
        assert result.exit_code == 0
        assert day == 334

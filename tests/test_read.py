#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Tests for the `v2ex read` function
"""

from __future__ import absolute_import

import pytest

from v2ex_daily_mission.cli import cli


@pytest.mark.usefixtures('mock_api')
class TestRead():
    def test_read_log_file(self, runner):
        result = runner.invoke(cli, ['--config', './tests/v2ex_config.json',
                                     'read'])
        assert result.exit_code == 0
        assert len(result.output.strip().split('\n')) == 5

    def test_read_log_file_with_parameter(self, runner):
        result = runner.invoke(cli, ['--config', './tests/v2ex_config.json',
                                     'read', '-c', '1'])
        assert result.exit_code == 0
        assert len(result.output.strip().split('\n')) == 1

#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import requests

from v2ex_daily_mission.notifier.abc import Notifier


class NoneNotifier(Notifier):
    def __init__(self, config):
        self.config = config

    def send_notification(self):
        pass

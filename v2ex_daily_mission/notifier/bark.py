#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import requests

from v2ex_daily_mission.notifier.abc import Notifier, NotificationSendFailedException


class BarkNotifier(Notifier):
    def __init__(self, config):
        self.config = config

    def send_notification(self):
        url = self.config['notifier']['bark']['url']
        try:
            response = requests.get(url)
            if response.json()['code'] != 200:
                raise NotificationSendFailedException(
                    "bark notification send failed, response: {}".format(response.text)
                )
        except requests.RequestException as e:
            raise NotificationSendFailedException(
                "bark notification send failed, error: {}".format(e)
            )

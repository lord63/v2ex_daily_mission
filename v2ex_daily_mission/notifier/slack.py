#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
import json

import requests

from v2ex_daily_mission.notifier.abc import Notifier, NotificationSendFailedException


class SlackNotifier(Notifier):
    def __init__(self, config):
        self.config = config

    def send_notification(self):
        url = self.config['notifier']['slack']['url']
        data = {
            "text": "v2ex_daily_mission: sign failed."
        }
        try:
            response = requests.post(url, data=json.dumps(data))
            if response.text != 'ok':
                raise NotificationSendFailedException(
                    "slack notification send failed, response: {}".format(response.text)
                )
        except requests.RequestException as e:
            raise NotificationSendFailedException(
                "slack notification send failed, error: {}".format(e)
            )

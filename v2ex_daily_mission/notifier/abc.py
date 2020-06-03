#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

from abc import ABC, abstractmethod


class NotificationSendFailedException(Exception):
    pass


class Notifier(ABC):
    @abstractmethod
    def send_notification(self):
        pass

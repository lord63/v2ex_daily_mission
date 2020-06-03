#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import sys
import abc
from abc import abstractmethod

if sys.version_info >= (3, 4):
    ABC = abc.ABC
else:
    ABC = abc.ABCMeta('ABC', (), {})


class NotificationSendFailedException(Exception):
    pass


class Notifier(ABC):
    @abstractmethod
    def send_notification(self):
        pass

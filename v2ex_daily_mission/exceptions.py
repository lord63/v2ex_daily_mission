#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import


class CookieExpiredError(Exception):
    """Raised when the V2EX cookie has expired or is invalid."""

    def __init__(self):
        super(CookieExpiredError, self).__init__(
            "cookie expired, please renew it.")

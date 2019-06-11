#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import logging
import os

import requests
from requests.packages import urllib3
from bs4 import BeautifulSoup


# Disable urllib3 warning, see lord63/a_bunch_of_code#9.
urllib3.disable_warnings()


class V2ex(object):
    def __init__(self, config):
        self.signin_url = 'https://www.v2ex.com/signin'
        self.balance_url = 'https://www.v2ex.com/balance'
        self.mission_url = 'https://www.v2ex.com/mission/daily'
        self.config = config
        self.session = requests.Session()
        self.session.headers.update(
            {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux \
             x86_64; rv:28.0) Gecko/20100101 Firefox/28.0'})
        self.cookie = self._make_cookie(config)
        logging.basicConfig(
            filename=os.path.join(config['log_directory'], 'v2ex.log'),
            level='INFO',
            format='%(asctime)s [%(levelname)s] %(message)s')
        # Disable log message from the requests library.
        requests_log = logging.getLogger("requests")
        requests_log.setLevel(logging.WARNING)

    def _make_cookie(self, config):
        return dict([i.split('=', 1) for i in config["cookie"].split('; ')])

    def get_money(self):
        """Complete daily mission then get the money."""
        response = self.session.get(self.mission_url, verify=False, cookies=self.cookie)
        soup = BeautifulSoup(response.text, 'html.parser')
        onclick = soup.find('input', class_='super normal button')['onclick']
        url = onclick.split('=', 1)[1][2:-2]

        if url == '/balance':
            return "You have completed the mission today."
        else:
            headers = {'Referer': 'https://www.v2ex.com/mission/daily'}
            data = {'once': url.split('=')[-1]}
            self.session.get('https://www.v2ex.com'+url, verify=False,
                             headers=headers, data=data, cookies=self.cookie,)
            balance = self._get_balance()
            return balance

    def _get_balance(self):
        """Get to know how much you totally have and how much you get today."""
        response = self.session.get(self.balance_url, verify=False, cookies=self.cookie)
        soup = BeautifulSoup(response.text, 'html.parser')
        first_line = soup.select(
            "table.data tr:nth-of-type(2)")[0].text.strip().split('\n')
        total, today = first_line[-2:]
        logging.info('%-26sTotal:%-8s', today, total)
        return '\n'.join([u"Today: {0}".format(today),
                          "Total: {0}".format(total)])

    def get_last(self):
        """Get to know how long you have kept signing in."""
        response = self.session.get(self.mission_url, verify=False, cookies=self.cookie)
        soup = BeautifulSoup(response.text, 'html.parser')
        last = soup.select('#Main div')[-1].text
        return last

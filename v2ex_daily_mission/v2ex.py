#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import logging
import os

import requests
from requests.packages import urllib3
from lxml import html


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
        logging.basicConfig(
            filename=os.path.join(config['log_directory'], 'v2ex.log'),
            level='INFO',
            format='%(asctime)s [%(levelname)s] %(message)s')
        # Disable log message from the requests library.
        requests_log = logging.getLogger("requests")
        requests_log.setLevel(logging.WARNING)

    def login(self):
        """Login v2ex, otherwise we can't complete the mission."""
        response = self.session.get(self.signin_url, verify=False)
        login_data = {
            'u': self.config['username'],
            'p': self.config['password'],
            'once': self.get_once(response.text),
            'next': '/'
        }
        headers = {'Referer': 'https://www.v2ex.com/signin'}
        self.session.post(self.signin_url, headers=headers, data=login_data)

    def get_once(self, page_text):
        """Get once which will be used when you login."""
        tree = html.fromstring(page_text)
        once = tree.xpath('//input[@name="once"]/@value')[0]
        return once

    def get_money(self):
        """Complete daily mission then get the money."""
        response = self.session.get(self.mission_url, verify=False)
        tree = html.fromstring(response.text)

        raw_once = tree.xpath('//input[@type="button"]/@onclick')[0]
        once = raw_once.split('=', 1)[1][2:-2]
        if once == '/balance':
            return "You have completed the mission today."
        else:
            headers = {'Referer': 'https://www.v2ex.com/mission/daily'}
            data = {'once': once.split('=')[-1]}
            self.session.get('https://www.v2ex.com'+once, verify=False,
                             headers=headers, data=data)
            balance = self.get_balance()
            return balance

    def get_balance(self):
        """Get to know how much you totally have and how much you get today."""
        response = self.session.get(self.balance_url, verify=False)
        tree = html.fromstring(response.text)
        total = tree.xpath(
            '//table[@class="data"]/tr[2]/td[4]/text()')[0].strip()
        today = tree.xpath(
            '//table[@class="data"]/tr[2]/td[5]/span/text()')[0].strip()
        logging.info('%-26sTotal:%-8s', today, total)
        return '\n'.join(["Today: {0}".format(today.encode('utf-8')),
                          "Total: {0}".format(total)])

    def get_last(self):
        """Get to know how long you have kept signing in."""
        response = self.session.get(self.mission_url, verify=False)
        tree = html.fromstring(response.text)
        last = tree.xpath(
            '//div[@id="Main"]/div[@class="box"]/div[3]/text()')[0].strip()
        return last

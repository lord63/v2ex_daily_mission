#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals, print_function

import logging
import os
import sys

import requests
from requests.packages import urllib3
from lxml import html


# set the session and header.
session = requests.Session()
session.headers.update({'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux \
                        x86_64; rv:28.0) Gecko/20100101 Firefox/28.0'})
# disable urllib3 warning, see #9
urllib3.disable_warnings()


class V2ex(object):
    def __init__(self, config):
        self.signin_url = 'https://www.v2ex.com/signin'
        self.balance_url = 'https://www.v2ex.com/balance'
        self.mission_url = 'https://www.v2ex.com/mission/daily'
        self.config = config
        # set log
        logging.basicConfig(
            filename=os.path.join(config['log_directory'], 'v2ex.log'),
            level='INFO',
            format='%(asctime)s [%(levelname)s] %(message)s')
        # disable log message from the requests library
        requests_log = logging.getLogger("requests")
        requests_log.setLevel(logging.WARNING)

    def login(self):
        """login v2ex, otherwise we can't complete the mission"""
        r = session.get(self.signin_url, verify=False)
        login_data = {
            'u': self.config['username'],
            'p': self.config['password'],
            'once': self.get_once(r.text),
            'next': '/'
        }
        headers = {'Referer': 'https://www.v2ex.com/signin'}
        session.post(self.signin_url, headers=headers, data=login_data)

    def get_once(self, page_text):
        """get once which will be used when you login"""
        tree = html.fromstring(page_text)
        once = tree.xpath('//input[@name="once"]/@value')[0]
        return once

    def get_money(self):
        """complete daily mission then get the money"""
        r = session.get(self.mission_url, verify=False)
        tree = html.fromstring(r.text)

        raw_once = tree.xpath('//input[@type="button"]/@onclick')[0]
        once = raw_once.split('=', 1)[1][2:-2]
        if once == '/balance':
            sys.exit("You have completed the mission today.")
        else:
            headers = {'Referer': 'https://www.v2ex.com/mission/daily'}
            data = {'once': once.split('=')[-1]}
            session.get('https://www.v2ex.com'+once, verify=False,
                        headers=headers, data=data)
            self.get_balance()

    def get_balance(self):
        """get to know how much you totally have and how much you get today"""
        r = session.get(self.balance_url, verify=False)
        tree = html.fromstring(r.text)
        total = tree.xpath(
            '//table[@class="data"]/tr[2]/td[4]/text()')[0].strip()
        today = tree.xpath(
            '//table[@class="data"]/tr[2]/td[5]/span/text()')[0].strip()
        logging.info('%-26sTotal:%-8s', today, total)
        print("Today: {0}".format(today))
        print("Total: {0}".format(total))

    def get_last(self):
        """get to know how long you have kept signing in"""
        r = session.get(self.mission_url, verify=False)
        tree = html.fromstring(r.text)
        last = tree.xpath(
            '//div[@id="Main"]/div[@class="box"]/div[3]/text()')[0].strip()
        print(last)

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
        user_param, password_param = self._get_hashed_params(response.text)
        login_data = {
            user_param: self.config['username'],
            password_param: self.config['password'],
            'once': self._get_once(response.text),
            'next': '/'
        }
        headers = {'Referer': 'https://www.v2ex.com/signin'}
        self.session.post(self.signin_url, headers=headers, data=login_data)

    def _get_hashed_params(self, page_text):
        """Get hashed params which will be used when you login, see issue#10"""
        soup = BeautifulSoup(page_text, 'html.parser')
        return [tag['name'] for tag in soup.find_all('input', class_='sl')]

    def _get_once(self, page_text):
        """Get once which will be used when you login."""
        soup = BeautifulSoup(page_text, 'html.parser')
        once = soup.find('input', attrs={'name': 'once'})['value']
        return once

    def get_money(self):
        """Complete daily mission then get the money."""
        response = self.session.get(self.mission_url, verify=False)
        soup = BeautifulSoup(response.text, 'html.parser')
        onclick = soup.find('input', class_='super normal button')['onclick']
        url = onclick.split('=', 1)[1][2:-2]

        if url == '/balance':
            return "You have completed the mission today."
        else:
            headers = {'Referer': 'https://www.v2ex.com/mission/daily'}
            data = {'once': url.split('=')[-1]}
            self.session.get('https://www.v2ex.com'+url, verify=False,
                             headers=headers, data=data)
            balance = self._get_balance()
            return balance

    def _get_balance(self):
        """Get to know how much you totally have and how much you get today."""
        response = self.session.get(self.balance_url, verify=False)
        soup = BeautifulSoup(response.text, 'html.parser')
        first_line = soup.select(
            "table.data tr:nth-of-type(2)")[0].text.strip().split('\n')
        total, today = first_line[-2:]
        logging.info('%-26sTotal:%-8s', today, total)
        return '\n'.join([u"Today: {0}".format(today),
                          "Total: {0}".format(total)])

    def get_last(self):
        """Get to know how long you have kept signing in."""
        response = self.session.get(self.mission_url, verify=False)
        soup = BeautifulSoup(response.text, 'html.parser')
        last = soup.select('#Main div')[-1].text
        return last

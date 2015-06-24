#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals, print_function

from collections import deque
import logging
import os
import sys
import json

import requests
from requests.packages import urllib3
from lxml import html
from terminal import Command

from v2ex_daily_mission import __version__


# set the session and header.
session = requests.Session()
session.headers.update({'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; \
                   rv:28.0) Gecko/20100101 Firefox/28.0'})
# disable urllib3 warning, see #9
urllib3.disable_warnings()


def get_once(page_text):
    """get once which will be used when you login"""
    tree = html.fromstring(page_text)
    once = tree.xpath('//input[@name="once"]/@value')[0]
    return once


def login(signin_url, config):
    """login v2ex, otherwise we can't complete the mission"""
    r = session.get(signin_url, verify=False)
    login_data = {
        'u': config['username'],
        'p': config['password'],
        'once': get_once(r.text),
        'next': '/'
    }
    headers = {'Referer': 'https://www.v2ex.com/signin'}
    session.post(signin_url, headers=headers, data=login_data)


def get_money(mission_url, balance_url):
    """complete daily mission then get the money"""
    r = session.get(mission_url, verify=False)
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
        get_balance(balance_url)


def get_balance(balance_url):
    """get to know how much you totally have and how much you get today"""
    r = session.get(balance_url, verify=False)
    tree = html.fromstring(r.text)
    total = tree.xpath('//table[@class="data"]/tr[2]/td[4]/text()')[0].strip()
    today = tree.xpath(
        '//table[@class="data"]/tr[2]/td[5]/span/text()')[0].strip()
    logging.info('%-26sTotal:%-8s', today, total)
    print("Today: {0}".format(today))
    print("Total: {0}".format(total))


def main():
    signin_url = 'https://www.v2ex.com/signin'
    balance_url = 'https://www.v2ex.com/balance'
    mission_url = 'https://www.v2ex.com/mission/daily'

    # get the configuration
    try:
        with open(os.path.join(sys.path[0], 'v2ex_config.json')) as f:
            config = json.load(f)
    except IOError:
        sys.exit("Don't forget your config.json.\nPlease read "
                 "https://github.com/lord63/v2ex_daily_mission.")

    command = Command('v2ex_daily_mission',
                      description='complete the mission and get money',
                      version=__version__)

    # subcommand
    @command.action
    def read(count=config['count']):
        """
        read log file

        :param count: read the count of the recent days
        :option count: -c, --count [count]
        """
        file_path = os.path.join(config['log_directory'], 'v2ex.log')
        for line in deque(open(file_path), int(count)):
            print(line, end="")

    @command.action
    def last():
        """how long you have kept signing in"""
        login(signin_url, config)
        r = session.get(mission_url, verify=False)
        tree = html.fromstring(r.text)
        last = tree.xpath(
            '//div[@id="Main"]/div[@class="box"]/div[3]/text()')[0].strip()
        print(last)

    command.parse()

    # set log
    logging.basicConfig(
        filename=os.path.join(config['log_directory'], 'v2ex.log'),
        level='INFO',
        format='%(asctime)s [%(levelname)s] %(message)s')
    # disable log message from the requests library
    requests_log = logging.getLogger("requests")
    requests_log.setLevel(logging.WARNING)

    if len(sys.argv) == 1:
        try:
            login(signin_url, config)
            get_money(mission_url, balance_url)
        except KeyError:
            print('Keyerror, please check your config file.')
        except IndexError:
            print('Please check your username and password.')


if __name__ == '__main__':
    main()

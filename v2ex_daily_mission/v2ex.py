#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals, print_function

from collections import deque
import logging
import os
from os import path
import sys
import json

import requests
from requests.packages import urllib3
from lxml import html
import click

from v2ex_daily_mission import __version__


# set the session and header.
session = requests.Session()
session.headers.update({'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux \
                        x86_64; rv:28.0) Gecko/20100101 Firefox/28.0'})
# disable urllib3 warning, see #9
urllib3.disable_warnings()


class Config(object):
    def load_config(self, path):
        try:
            with open(path) as f:
                self.config = json.load(f)
        except IOError:
            sys.exit("Don't forget your config.json.\nPlease read "
                     "https://github.com/lord63/v2ex_daily_mission.")


pass_config = click.make_pass_decorator(Config, ensure=True)


def read_config(ctx, param, given_path):
    cfg = ctx.ensure_object(Config)
    if given_path is None:
        given_path = path.join(sys.path[0], 'v2ex_config.json')
    cfg.load_config(given_path)
    return given_path


class V2ex(object):
    def __init__(self, config):
        self.signin_url = 'https://www.v2ex.com/signin'
        self.balance_url = 'https://www.v2ex.com/balance'
        self.mission_url = 'https://www.v2ex.com/mission/daily'
        self.config = config
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


@click.group(context_settings={'help_option_names': ('-h', '--help')})
@click.version_option(__version__, '-v', '--version', message='%(version)s')
@click.option('--config', type=click.Path(exists=True, dir_okay=False),
              callback=read_config, expose_value=False,
              help='specify the config file path')
def cli():
    """Complete daily mission, get money, for V2EX."""
    pass


@cli.command()
@pass_config
def sign(conf):
    """sign in and get money"""
    try:
        v2ex = V2ex(conf.config)
        v2ex.login()
        v2ex.get_money()
    except KeyError:
        print('Keyerror, please check your config file.')
    except IndexError:
        print('Please check your username and password.')


@cli.command()
@click.option('--count', '-c', default=5, help="the count of days.")
@pass_config
def read(conf, count):
    """read log file"""
    file_path = os.path.join(conf.config['log_directory'], 'v2ex.log')
    for line in deque(open(file_path), int(count)):
        print(line.decode('utf-8'), end="")


@cli.command()
@pass_config
def last(conf):
    """how long you have kept signing in"""
    try:
        v2ex = V2ex(conf.config)
        v2ex.login()
        v2ex.get_last()
    except KeyError:
        print('Keyerror, please check your config file.')
    except IndexError:
        print('Please check your username and password.')

#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from collections import deque
import os
from os import path
import sys
import json

import click

from v2ex_daily_mission import __version__
from v2ex_daily_mission.v2ex import V2ex


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
        balance = v2ex.get_money()
        click.echo(balance)
    except KeyError:
        click.echo('Keyerror, please check your config file.')
    except IndexError:
        click.echo('Please check your username and password.')


@cli.command()
@click.option('--count', '-c', default=5, help="the count of days.")
@pass_config
def read(conf, count):
    """read log file"""
    file_path = os.path.join(conf.config['log_directory'], 'v2ex.log')
    for line in deque(open(file_path), int(count)):
        click.echo(line.decode('utf-8'), nl=False)


@cli.command()
@pass_config
def last(conf):
    """how long you have kept signing in"""
    try:
        v2ex = V2ex(conf.config)
        v2ex.login()
        last_date = v2ex.get_last()
        click.echo(last_date)
    except KeyError:
        click.echo('Keyerror, please check your config file.')
    except IndexError:
        click.echo('Please check your username and password.')

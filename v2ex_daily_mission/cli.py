#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

from collections import deque
import os
from os import path
import sys
import json
from codecs import open

import click

from v2ex_daily_mission import __version__
from v2ex_daily_mission.v2ex import V2ex
from v2ex_daily_mission.notifier import BarkNotifier, NoneNotifier, SlackNotifier


class Config(object):
    def __init__(self):
        self.config = {}

    def load_config(self, config_path):
        with open(config_path, encoding='utf-8') as f:
            self.config = json.load(f)


pass_config = click.make_pass_decorator(Config, ensure=True)


def read_config(ctx, param, config_path):
    """Callback that is used whenever --config is passed."""
    if sys.argv[1] == 'init':
        return
    cfg = ctx.ensure_object(Config)
    if config_path is None:
        config_path = path.join(sys.path[0], 'v2ex_config.json')
    if not path.exists(config_path):
        sys.exit("Can't find config file at {0}.\nPlease read "
                 "https://github.com/lord63/v2ex_daily_mission "
                 "to follow the guide.".format(config_path))
    cfg.load_config(config_path)
    return config_path


def initialize_nitifier(config):
    if 'notifier' not in config:
        return NoneNotifier(config)
    if 'bark' in config['notifier']:
        return BarkNotifier(config)
    elif 'slack' in config['notifier']:
        return SlackNotifier(config)
    return NoneNotifier(config)


@click.group(context_settings={'help_option_names': ('-h', '--help')})
@click.version_option(__version__, '-V', '--version', message='%(version)s')
@click.option('--config',
              type=click.Path(exists=True, dir_okay=False, resolve_path=True),
              callback=read_config, expose_value=False,
              help='Specify the config file path.')
def cli():
    """Complete daily mission, get money, for V2EX."""
    pass


@cli.command()
@click.option(
    '--directory', default=sys.path[0],
    type=click.Path(exists=True, file_okay=False, resolve_path=True),
    help='the config file path directory.')
def init(directory):
    """Init the config fle."""
    cookie = click.prompt("Input your cookie")

    log_directory = click.prompt("Input your log directory")
    if not path.exists(log_directory):
        sys.exit("Invalid log directory, please have a check.")

    notifier = click.prompt(
        "Input your notifier",
        default='none',
        type=click.Choice(['bark', 'slack', 'none'], case_sensitive=False),
        show_choices=True,
        show_default=True
    )
    if notifier != 'none':
        notifier_url = click.prompt("Input your notifier url")

    config = {
        "cookie": cookie,
        "log_directory": path.abspath(log_directory)
    }
    if notifier != 'none':
        config['notifier'] = {notifier: {'url': notifier_url}}

    config_file_path = path.join(directory, 'v2ex_config.json')
    with open(config_file_path, 'w') as f:
        json.dump(config, f)
    click.echo("Init the config file at: {0}".format(config_file_path))


@cli.command()
@pass_config
def sign(conf):
    """Sign in and get money."""
    notifier = initialize_nitifier(conf.config)
    try:
        v2ex = V2ex(conf.config)
        balance = v2ex.get_money()
        click.echo(balance)
    except KeyError:
        notifier.send_notification()
        click.echo('Keyerror, please check your config file.')
    except IndexError:
        notifier.send_notification()
        click.echo('Please check your username and password.')
    except Exception as e:
        notifier.send_notification()
        click.echo('Sign failed, error: {}.'.format(e))


@cli.command()
@click.option('--count', '-c', default=5, help="the count of days.")
@pass_config
def read(conf, count):
    """Read log file."""
    file_path = os.path.join(path.abspath(conf.config['log_directory']),
                             'v2ex.log')
    for line in deque(open(file_path, encoding='utf-8'), int(count)):
        click.echo(line, nl=False)


@cli.command()
@pass_config
def last(conf):
    """How long you have kept signing in."""
    try:
        v2ex = V2ex(conf.config)
        last_date = v2ex.get_last()
        click.echo(last_date)
    except KeyError:
        click.echo('Keyerror, please check your config file.')
    except IndexError:
        click.echo('Please check your username and password.')


@cli.command()
@pass_config
def notify(conf):
    """Test notify send"""
    notifier = initialize_nitifier(conf.config)
    if isinstance(notifier, NoneNotifier):
        click.echo("There is no notifier configuration.")
        return
    notifier.send_notification()
    click.echo("send notification success.")

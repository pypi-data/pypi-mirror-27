#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    agent.cli
    ~~~~~~~~~~~~

    This module is the main of agent.

    :copyright: (c) 2017 by Ma Fei.
"""
import logging
import os
import signal

import click
from apscheduler.schedulers.background import BackgroundScheduler
from pyunitreport import __version__ as pyu_version

import agent
import agent.config as config
from agent.consts import AgentStatus
from agent.exc import GracefulExitException
from agent.qualityplatform import server_api
from agent.server.api import start_server, stop_server
from agent.util.sentry import Sentry

logger = logging.getLogger(__name__)

sentry = Sentry()

scheduler = BackgroundScheduler()
logging.getLogger("apscheduler").setLevel(logging.ERROR)


def output_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo("Version: {}".format(agent.__version__))
    click.echo("PyUnitReport version: {}".format(pyu_version))
    ctx.exit()


@click.command()
@click.option(
    '-v',
    '--version',
    is_flag=True,
    is_eager=True,
    callback=output_version,
    expose_value=False,
    help="show the version of this tool")
@click.option(
    '-e',
    '--environment',
    default='prod',
    help='select a development environment such as alpha|beta|prod')
@click.option(
    '-l',
    '--log',
    default='INFO',
    help='Specify logging level, default is INFO')
def parse_command(environment, log):
    log_level = getattr(logging, log.upper())
    logging.basicConfig(level=log_level)

    config.qualityplatform['api_url'] = config.qualityplatform_env_api_url.get(environment)
    config.sentry_url['url'] = config.sentry_env_url.get(environment)
    logger.info(config.sentry_url.get('url'))
    config.agent['port'] = config.agent_env_port.get(environment)
    start_agent_client()


def check_devices_cron():
    server_api.register_agent(AgentStatus.online.value)


def signal_handler(signum, frame):
    server_api.unregister_agent(config.agent['agent_id'])
    stop_server()
    scheduler.shutdown()
    logger.info("main process(%d) got GracefulExitException" % os.getpid())
    os._exit(0)


def start_agent_client():
    agent_data = server_api.register_agent(AgentStatus.online.value)
    if agent_data:
        config.agent['agent_id'] = agent_data.get('id')
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    try:
        scheduler.add_job(check_devices_cron, 'interval', seconds=15)
        scheduler.start()
        start_server()
    except GracefulExitException:
        sentry.client.captureException()


def main():
    print("A Terminal Tools For agent Agent")
    parse_command()


if __name__ == "__main__":
    main()

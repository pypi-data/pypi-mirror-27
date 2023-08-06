# -*- coding: utf-8 -*-
# ###
# Copyright (c) 2015, Rice University
# This software is subject to the provisions of the GNU Affero General
# Public License version 3 (AGPLv3).
# See LICENCE.txt for details.
# ###
from __future__ import print_function
import argparse
import logging
import os
import signal
import sys

import pkg_resources
import psycopg2

from . import commands, utils, logger


DEFAULTS = {
    }


def main(argv=sys.argv[1:]):
    # psycopg2 / libpq doesn't respond to SIGINT (ctrl-c):
    # https://github.com/psycopg/psycopg2/issues/333
    # To get around this problem, using code from:
    # http://initd.org/psycopg/articles/2014/07/20/cancelling-postgresql-statements-python/ # noqa
    psycopg2.extensions.set_wait_callback(utils.wait_select_inter)

    parser = argparse.ArgumentParser(description='DB Migrator')

    parser.add_argument('--verbose', '-v', action='store_true')
    parser.add_argument('--quiet', '-q', action='store_true')

    parser.add_argument('--migrations-directory',
                        action='append',
                        default=[])

    parser.add_argument('--config')

    parser.add_argument('--db-connection-string',
                        help='a psycopg2 db connection string')

    parser.add_argument('--db-config-ini-key',
                        help='the name of the ini key for the db connection '
                             'string in the config file')

    parser.add_argument(
        '--super-user',
        default='postgres',
        help='postgres username for super user connections, defaults to '
             '"postgres"')

    parser.add_argument(
        '--context',
        action='append',
        default=[],
        help='Name of the python package containing the migrations')

    version = pkg_resources.require('db-migrator')[0].version
    parser.add_argument('-V', action='version', version=version,
                        help='Show version information')

    subparsers = parser.add_subparsers(help='commands')
    commands.load_cli(subparsers)

    args = parser.parse_args(argv)
    args = vars(args)

    if args.get('config'):
        if not os.path.exists(args['config']):
            raise Exception('config file not found')
        utils.get_settings_from_config(args['config'], [
            'migrations-directory',
            'db-connection-string',
            ], args)
        if args.get('db_config_ini_key'):
            utils.get_settings_from_config(args['config'], [
                args['db_config_ini_key']], args)
            args['db_connection_string'] = args.get(
                args['db_config_ini_key'].replace('-', '_'))

    if not args.get('context') and not args.get('migrations_directory'):
        args['context'] = [os.path.basename(os.path.abspath(os.path.curdir))]
        logger.warning('context undefined, using current directory name "{}"'
                       .format(args['context']))
    utils.get_settings_from_entry_points(args, args['context'])

    for name, value in DEFAULTS.items():
        if not args.get(name):
            args[name] = value

    if 'cmmd' not in args:
        parser.print_help()
        return parser.error('command missing')

    if args.get('migrations_directory'):
        if not isinstance(args['migrations_directory'], list):
            args['migrations_directory'] = [args['migrations_directory']]
        args['migrations_directory'] = [
            os.path.relpath(md) for md in args['migrations_directory']]
    else:
        logger.warning('migrations directory undefined')

    if args.get('verbose'):
        logger.setLevel(logging.DEBUG)

    if args.get('quiet'):
        logger.setLevel(logging.ERROR)

    logger.debug('args: {}'.format(args))
    utils.set_settings(args)

    return args['cmmd'](**args)

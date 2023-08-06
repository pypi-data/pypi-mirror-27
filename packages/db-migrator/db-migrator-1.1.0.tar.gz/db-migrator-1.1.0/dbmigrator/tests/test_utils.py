# -*- coding: utf-8 -*-
# ###
# Copyright (c) 2016, Rice University
# This software is subject to the provisions of the GNU Affero General
# Public License version 3 (AGPLv3).
# See LICENCE.txt for details.
# ###

import datetime
import os.path
import tempfile
import unittest
try:
    from unittest import mock
except ImportError:
    import mock

import psycopg2

from . import testing
from ..utils import db_connect


logger = mock.Mock()


class UtilsTestCase(unittest.TestCase):
    def setUp(self):
        import dbmigrator
        _logger = dbmigrator.utils.logger
        self.addCleanup(setattr, dbmigrator.utils, 'logger', _logger)
        dbmigrator.utils.logger = logger
        with db_connect(testing.db_connection_string) as db_conn:
            with db_conn.cursor() as cursor:
                cursor.execute("""
CREATE TABLE schema_migrations (
    version TEXT NOT NULL,
    applied TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
)""")
        dbmigrator.utils.set_settings({
            'db_connection_string': testing.db_connection_string,
        })

    def tearDown(self):
        with db_connect(testing.db_connection_string) as db_conn:
            with db_conn.cursor() as cursor:
                cursor.execute('DROP TABLE IF EXISTS a_table')
                cursor.execute('DROP TABLE IF EXISTS schema_migrations')

    def test_super_user(self):
        from ..utils import super_user, with_cursor

        def cleanup():
            with db_connect(testing.db_connection_string,
                            user='postgres') as db_conn:
                with db_conn.cursor() as cursor:
                    cursor.execute('DROP TABLE IF EXISTS super_table')

        self.addCleanup(cleanup)

        with db_connect(testing.db_connection_string) as db_conn:
            with db_conn.cursor() as cursor:
                cursor.execute('SELECT current_user')
                self.assertEqual('travis', cursor.fetchone()[0])

                with super_user() as super_cursor:
                    super_cursor.execute('SELECT current_user')
                    self.assertEqual('postgres', super_cursor.fetchone()[0])

                    super_cursor.execute('CREATE TABLE super_table (id TEXT)')
                    super_cursor.execute(
                        'GRANT ALL PRIVILEGES ON TABLE super_table TO travis')
                    super_cursor.execute(
                        "INSERT INTO super_table VALUES ('62')")

                cursor.execute('SELECT current_user')
                self.assertEqual('travis', cursor.fetchone()[0])

                cursor.execute('SELECT * FROM super_table')
                self.assertEqual('62', cursor.fetchone()[0])

    def test_get_settings_from_entry_points(self):
        from ..utils import get_settings_from_entry_points

        testing.install_test_packages()

        contexts = testing.test_packages
        settings = {
            'db_connection_string': testing.db_connection_string,
            }

        get_settings_from_entry_points(settings, contexts)

        self.assertEqual(
            settings,
            {'migrations_directory': testing.test_migrations_directories,
             'db_connection_string': testing.db_connection_string,
             })

    def test_get_settings_from_config(self):
        from ..utils import get_settings_from_config

        tmp_dir = tempfile.gettempdir()

        settings = {
            'migrations_directory': tmp_dir,
            }

        get_settings_from_config(
            testing.test_config_path,
            ['db-connection-string', 'migrations-directory', 'does-not-exist'],
            settings)

        self.assertEqual(
            settings,
            {'db_connection_string': testing.db_connection_string,
             'migrations_directory': tmp_dir})

    def test_with_cursor(self):
        from ..utils import with_cursor

        self.called = False

        @with_cursor
        def func(cursor, arg_1, kwarg_1='kwarg_1', kwarg_2='kwarg_2',
                 db_connection_string=None):
            self.assertTrue(isinstance(cursor, psycopg2.extensions.cursor))
            self.assertEqual(arg_1, 'arg_1')
            self.assertEqual(kwarg_1, 'called')
            self.assertEqual(kwarg_2, 'kwarg_2')
            self.assertEqual(
                db_connection_string, testing.db_connection_string)
            self.called = True

        func('arg_1', kwarg_1='called',
             db_connection_string=testing.db_connection_string)
        self.assertTrue(self.called)

        with self.assertRaises(Exception) as cm:
            func('')

        self.assertEqual(str(cm.exception), 'db-connection-string missing')

    def test_import_migration(self):
        from ..utils import import_migration

        migration_path = os.path.join(
            testing.test_data_path, 'package-a', 'package_a', 'migrations',
            '20160228202637_add_table.py')

        migration = import_migration(migration_path)
        self.assertIn('up', dir(migration))
        self.assertIn('down', dir(migration))

        with db_connect(testing.db_connection_string) as db_conn:
            with db_conn.cursor() as cursor:
                try:
                    cursor.execute('SELECT * FROM a_table')
                    self.fail('a_table should not be in the database before '
                              'the migration is run')
                except psycopg2.ProgrammingError as e:
                    self.assertIn('relation "a_table" does not exist', str(e))

        with db_connect(testing.db_connection_string) as db_conn:
            with db_conn.cursor() as cursor:
                # Run the migration.
                migration.up(cursor)

                # Try accessing a_table created by the migration.
                cursor.execute('SELECT * FROM a_table')

                # Roll back the migration.
                migration.down(cursor)

        with db_connect(testing.db_connection_string) as db_conn:
            with db_conn.cursor() as cursor:
                try:
                    cursor.execute('SELECT * FROM a_table')
                    self.fail('a_table should not be in the database after '
                              'the migration is rolled back')
                except psycopg2.ProgrammingError as e:
                    self.assertIn('relation "a_table" does not exist', str(e))

    def test_get_migrations(self):
        from ..utils import get_migrations

        migrations = get_migrations(testing.test_migrations_directories)

        self.assertEqual(
            list(migrations),
            [('20160228202637', 'add_table'),
             ('20160228210326', 'initial_data'),
             ('20160228212456', 'cool_stuff')])

    def test_get_migrations_no_migrations_directories(self):
        from ..utils import get_migrations

        migrations = get_migrations([])

        self.assertEqual(list(migrations), [])

    def test_get_pending_migrations(self):
        from ..utils import get_pending_migrations

        with db_connect(testing.db_connection_string) as db_conn:
            with db_conn.cursor() as cursor:
                migrations = list(get_pending_migrations(
                    testing.test_migrations_directories, cursor))

        self.assertEqual(migrations, [
            ('20160228202637', 'add_table'),
            ('20160228210326', 'initial_data'),
            ('20160228212456', 'cool_stuff')])

    def test_run_migration(self):
        from ..utils import run_migration, get_pending_migrations

        with db_connect(testing.db_connection_string) as db_conn:
            with db_conn.cursor() as cursor:
                migrations = list(get_pending_migrations(
                    testing.test_migrations_directories, cursor,
                    import_modules=True))
                version, name, migration = list(migrations)[0]

                run_migration(cursor, version, name, migration)

                after_migrations = list(get_pending_migrations(
                    testing.test_migrations_directories, cursor))

        logger.info.assert_called_with(
            'Running migration {} {}'.format(version, name))

        self.assertNotIn((version, name), after_migrations)

    def test_rollback_migration(self):
        from ..utils import (
            rollback_migration, run_migration, get_pending_migrations)

        with db_connect(testing.db_connection_string) as db_conn:
            with db_conn.cursor() as cursor:
                migrations = list(get_pending_migrations(
                    testing.test_migrations_directories, cursor,
                    import_modules=True))
                version, name, migration = list(migrations)[0]

                run_migration(cursor, version, name, migration)

                rollback_migration(cursor, version, name, migration)

                after_migrations = list(get_pending_migrations(
                    testing.test_migrations_directories, cursor))

        logger.info.assert_called_with(
            'Rolling back migration {} {}'.format(version, name))

        self.assertIn((version, name), after_migrations)

    def test_timestamp(self):
        from ..utils import timestamp

        now = datetime.datetime(2016, 2, 28, 22, 51, 56)

        with mock.patch('datetime.datetime') as mock_datetime:
            mock_datetime.utcnow.return_value = now
            self.assertEqual(timestamp(), '20160228225156')

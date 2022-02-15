import sqlite3
from unittest import TestCase
from unittest.mock import patch, Mock

from repository import DBRepository


class TestDBRepository(TestCase):

    def _create_shared_db_con(self):
        return sqlite3.connect("file:mem1?mode=memory&cache=shared", uri=True)

    def test_create_tb_user(self):
        test_con = self._create_shared_db_con()
        code_con = self._create_shared_db_con()
        recreate_con = self._create_shared_db_con()

        connect_patcher = patch('sqlite3.connect')
        connect = connect_patcher.start()
        connect.side_effect = [code_con, recreate_con]

        repo = DBRepository()

        created = repo.create_tb_user()
        self.assertTrue(created)

        repo.create_tb_user()

        connect.assert_called_with("user.db")

        cur = test_con.cursor()
        cur.execute("SELECT sql FROM sqlite_schema WHERE name='TB_USER'")
        r = cur.fetchone()

        connect_patcher.stop()

        test_con.close()

    def test_create_user(self):
        test_con = self._create_shared_db_con()
        test_con.row_factory = sqlite3.Row
        create_con = self._create_shared_db_con()
        insert_con = self._create_shared_db_con()

        connect_patcher = patch('sqlite3.connect')
        connect = connect_patcher.start()
        # Provide a new connection, since the previous one was closed
        connect.side_effect = [create_con, insert_con]

        repo = DBRepository()
        repo.create_tb_user()

        email = 'some@conestoga.ca'
        password = 'CRYPT0P4SS'

        created = repo.create_user(email, password)

        self.assertTrue(created)

        cur = test_con.cursor()
        cur.execute('SELECT USER_ID, LOGIN, "CRYPTOGRAPHIC PASSWORD", ACCESS_COUNT FROM TB_USER')
        r = cur.fetchone()

        self.assertEqual(1, r['USER_ID'])
        self.assertEqual(email, r['LOGIN'])
        self.assertEqual(password, r["CRYPTOGRAPHIC PASSWORD"])
        self.assertEqual(0, r['ACCESS_COUNT'])

        test_con.close()

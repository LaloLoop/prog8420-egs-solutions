import sqlite3
from unittest import TestCase
from unittest.mock import patch, Mock

from db_asserts import assert_user_record
from repository import DBRepository

ORIGINAL_CONNECT = sqlite3.connect


def create_shared_db_con(*args, **kwargs):
    return ORIGINAL_CONNECT("file:mem1?mode=memory&cache=shared", uri=True)


class TestDBRepository(TestCase):

    def setUp(self) -> None:
        self.test_con = create_shared_db_con()
        connect_patcher = patch('sqlite3.connect', wraps=create_shared_db_con)
        self.connect_patcher = connect_patcher

        self.connect = connect_patcher.start()

        self.repo = DBRepository()

    def tearDown(self) -> None:
        self.connect_patcher.stop()
        self.test_con.close()

    def _create_db(self):
        created = self.repo.create_tb_user()
        self.assertTrue(created)

    def _create_user(self):
        email = 'some@conestoga.ca'
        password = 'CRYPT0P4SS'

        created = self.repo.create_user(email, password)

        self.assertTrue(created)

        return (email, password)

    def test_create_tb_user(self):
        self._create_db()

        self.repo.create_tb_user()

        self.connect.assert_called_with("user.db")

        cur = self.test_con.cursor()
        cur.execute("SELECT sql FROM sqlite_schema WHERE name='TB_USER'")
        r = cur.fetchone()

        self.assertIsNotNone(r)

    def test_create_user(self):

        self._create_db()

        email, password = self._create_user()

        assert_user_record(email, password, con=self.test_con)

    def test_find_user_with_credentials(self):

        self._create_db()
        email, password = self._create_user()

        user_record = self.repo.find_user_with_credentials(email, password)

        self.assertEqual(email, user_record.email)
        self.assertEqual(0, user_record.access_count)

    def test_update_access_count(self):
        self._create_db()
        email, password = self._create_user()

        updated = self.repo.update_access_count(email, password)

        self.assertTrue(updated)

        assert_user_record(email, password, access_count=1, con=self.test_con)

import os.path
import sqlite3
from subprocess import Popen, PIPE, STDOUT, run
from unittest import TestCase

import pexpect


class TestE2E(TestCase):

    def setUp(self) -> None:
        self._cleanup_db()

    def tearDown(self) -> None:
        self._cleanup_db()

    def _cleanup_db(self):
        db_path = "user.db"
        if os.path.exists(db_path):
            os.remove(db_path)

    def test_with_create_with_pexpect(self):

        email = "test@conestoga.ca"
        password = "MARCOS442021"
        ciphered_pass = "CTLMHP557978"

        child = pexpect.spawn('python main.py')
        child.expect('New user?')
        child.sendline("Y")
        child.expect('email: ')
        child.sendline(email)
        child.expect('password: ')
        child.sendline(password)
        child.expect('New user?')
        child.sendline("exit")

        con = sqlite3.connect('./user.db')
        con.row_factory = sqlite3.Row
        cur = con.cursor()

        cur.execute('SELECT USER_ID, LOGIN, "CRYPTOGRAPHIC PASSWORD", ACCESS_COUNT FROM TB_USER')

        r = cur.fetchone()

        self.assertEqual(1, r['USER_ID'])
        self.assertEqual(email, r['LOGIN'])
        self.assertEqual(ciphered_pass, r["CRYPTOGRAPHIC PASSWORD"])
        self.assertEqual(0, r['ACCESS_COUNT'])

        con.close()

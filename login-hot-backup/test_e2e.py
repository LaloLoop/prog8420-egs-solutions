import os.path
import sqlite3
from subprocess import Popen, PIPE, STDOUT, run
from unittest import TestCase

import pexpect

from db_asserts import assert_user_record


class TestE2E(TestCase):

    def setUp(self) -> None:
        self._cleanup_db()
        self._child = pexpect.spawn('python main.py', timeout=3)

    def tearDown(self) -> None:
        self._cleanup_db()

    def _cleanup_db(self):
        db_path = "user.db"
        if os.path.exists(db_path):
            os.remove(db_path)

    def _create_user(self, email, password):
        child = self._child
        child.expect('New user?')
        child.sendline("Y")
        child.expect('email: ')
        child.sendline(email)
        child.expect('password: ')
        child.sendline(password)

    def _exit(self):
        self._child.expect('New user?')
        self._child.sendline("exit")

    def test_create_user(self):
        email = "test@conestoga.ca"
        password = "MARCOS442021"
        ciphered_pass = "CTLMHP557978"

        self._create_user(email, password)
        self._exit()

        assert_user_record(email, ciphered_pass)

    def test_login(self):
        email = 'lalo@conestoga.ca'
        password = 'MY5UP3RP455'

        self._create_user(email, password)

        child = self._child

        for i in range(1, 3):
            child.expect('New user?')
            child.sendline("N")
            child.expect('email: ')
            child.sendline(email)
            child.expect('password: ')
            child.sendline(password)
            child.expect(f"{email} has logged in {i} time\(s\)")

        self._exit()

        child.wait()

        assert not child.isalive()

        child.close()

        self.assertEqual(0, child.exitstatus)

        assert_user_record(email, 'CY4UJ6LJ544', access_count=2)



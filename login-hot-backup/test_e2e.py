import os.path
from unittest import TestCase

import pexpect

from db_asserts import assert_user_record, assert_db_backup, assert_empty_db, assert_no_backup
from testing_helpers import random_string_from


def _cleanup_file(db_path):
    if os.path.exists(db_path):
        os.remove(db_path)


class TestE2E(TestCase):

    def setUp(self) -> None:
        self._files = ["user.db", 'userdb-backup.csv']
        self._cleanup_files()
        self._child = pexpect.spawn('python main.py', timeout=3)

    def tearDown(self) -> None:
        self._cleanup_files()

    def _cleanup_files(self):
        for path in self._files:
            _cleanup_file(path)

    def _create_user(self, email, password):
        child = self._child
        child.expect('New user?')
        child.sendline("Y")
        child.expect('email: ')
        child.sendline(email)
        child.expect('Please confirm your email: ')
        child.sendline(email)
        child.expect('password: ')
        child.sendline(password)
        child.expect('Please confirm your password: ')
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

        assert_db_backup()

    def test_create_user_validations(self):
        valid_email = "lalo@gmail.com"
        valid_pass = "P4S5W0RD"

        child = self._child
        child.sendline("Y")
        child.sendline("")
        child.expect("Please provide your email")
        child.sendline(random_string_from(valid_email))
        child.expect("Please input a valid email, e.g. user@domain.com")
        child.sendline(valid_email)
        child.sendline(valid_email)
        child.sendline("")
        child.expect("Please provide your password")
        child.sendline("somP455")
        child.expect("Provide a 4 or more uppercase letters password, no special characters are allowed")
        child.sendline(valid_pass)
        child.sendline(valid_pass)

        self._exit()

    def test_login_validations(self):
        email = "sam@yahoo.com"
        password = "54MST0WN"

        self._create_user(email, password)

        child = self._child
        child.sendline("N")
        child.sendline("")
        child.expect("Please provide your email")
        child.sendline(random_string_from(email))
        child.expect("Please input a valid email, e.g. user@domain.com")
        child.sendline(email)
        child.sendline("")
        child.expect("Please provide your password")
        child.sendline(random_string_from(password.lower()))
        child.expect("Provide a 4 or more uppercase letters password, no special characters are allowed")
        child.sendline(password)

        self._exit()

    def test_user_doesnt_exist(self):
        email = "nonexistent@email.com"
        password = "S0M3P455"

        child = self._child
        child.sendline("N")
        child.sendline(email)
        child.sendline(password)
        child.expect("User does not exist")

        self._exit()

        assert_empty_db()
        assert_no_backup()

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

        assert_db_backup()

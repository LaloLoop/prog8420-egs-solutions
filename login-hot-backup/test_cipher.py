from unittest import TestCase

from cipher import PasswordCipher


class TestPasswordCipher(TestCase):

    def test_cipher(self):
        cipher = PasswordCipher()

        password = 'SOM3P4S5'
        ciphered_pass = cipher.cipher(password)

        self.assertIsNotNone(ciphered_pass)
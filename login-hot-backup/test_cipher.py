from unittest import TestCase

from cipher import PasswordCipher


class TestPasswordCipher(TestCase):

    def test_cipher(self):
        cipher = PasswordCipher()

        password = 'MARCOS442021'
        ciphered_pass = cipher.cipher(password)

        self.assertEqual('CTLMHP557978', ciphered_pass)
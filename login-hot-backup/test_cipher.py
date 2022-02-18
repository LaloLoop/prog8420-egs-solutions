from unittest import TestCase

from cipher import PasswordCipher


class TestPasswordCipher(TestCase):

    def setUp(self) -> None:
        self.cipher = PasswordCipher()

    def test_cipher(self):
        password = 'MARCOS442021'
        ciphered_pass = self.cipher.cipher(password)

        self.assertEqual('CTLMHP557978', ciphered_pass)

    def test_cipher_with_unmapped_values(self):
        password = 'n0t_M4pp3d'

        cipher_pass = self.cipher.cipher(password)

        self.assertEqual('*9**C5**6*', cipher_pass)
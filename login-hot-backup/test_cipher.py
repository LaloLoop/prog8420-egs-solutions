from unittest import TestCase
from unittest.mock import patch

from cipher import PasswordCipher, DEFAULT_MAPPING, XLSXCipher


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


class TestXLSXCipher(TestCase):

    @patch('cipher.XLSXParser')
    def test_cipher(self, XLSXParser):
        parser = XLSXParser.return_value

        parser.load.return_value = {'_': 'C', '*': '0', 'M': 'A'}

        test_password = "_*M"

        cipher = XLSXCipher()

        ciphered_pass = cipher.cipher(test_password)

        parser.load.assert_called_once()
        self.assertEqual("C0A", ciphered_pass)

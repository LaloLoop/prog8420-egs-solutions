from unittest import TestCase
from unittest.mock import patch, DEFAULT

from controller import Controller


class TestController(TestCase):

    def setUp(self) -> None:
        self.controller = Controller()

    def test_exit(self):
        self.assertTrue(self.controller.is_running())

        self.controller.exit()

        self.assertFalse(self.controller.is_running())

    def test_get_state(self):
        self.assertEqual({'context': 'init'}, self.controller.get_state())

    def test_prompt_user_info(self):
        self.controller.prompt_user_info()
        self.assertEqual({'context': 'prompt_user_info'}, self.controller.get_state())

    @patch.multiple('controller', PasswordCipher=DEFAULT, DBRepository=DEFAULT, autospec=True)
    def test_create_user(self, PasswordCipher, DBRepository):

        self.controller._cipher = PasswordCipher.return_value
        self.controller._repo = DBRepository.return_value
        self.controller._state = {'context': 'prompt_user_info'}

        email = 'lalo@conestoga.ca'
        password = 'SOM3P455'
        ciphered_password = 'ciphered-pass'

        cipher = PasswordCipher.return_value
        repo = DBRepository.return_value

        cipher.cipher.return_value = ciphered_password
        repo.create_user.return_value = True

        created = self.controller.create_user(email, password)

        self.assertTrue(created)

        cipher.cipher.assert_called_once_with(password)
        repo.create_user.assert_called_once_with(email, ciphered_password)

        self.assertEqual({'context': 'init'}, self.controller.get_state())

    def test_login(self):
        self.controller.login()

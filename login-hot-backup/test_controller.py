from unittest import TestCase
from unittest.mock import patch, DEFAULT, Mock

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

    def test_prompt_login_info(self):
        self.controller.prompt_login_info()
        self.assertEqual({'context': 'prompt_login_info'}, self.controller.get_state())

    @patch('controller.DBRepository', autospec=True)
    def test_init_db(self, repo):
        self.controller._repo = repo
        self.controller.init_db()

        repo.create_tb_user.assert_called_once()

    @patch.multiple('controller', PasswordCipher=DEFAULT, DBRepository=DEFAULT, DBExporter=DEFAULT, autospec=True)
    def test_create_user(self, PasswordCipher, DBRepository, DBExporter):
        cipher = PasswordCipher.return_value
        repo = DBRepository.return_value
        exporter = DBExporter.return_value

        self.controller._exporter = exporter
        self.controller._cipher = cipher
        self.controller._repo = repo
        self.controller._state = {'context': 'prompt_user_info'}

        email = 'lalo@conestoga.ca'
        password = 'SOM3P455'
        ciphered_password = 'PHC6J544'

        cipher.cipher.return_value = ciphered_password
        repo.create_user.return_value = True
        exporter.export.return_value = True

        created = self.controller.create_user(email, password)

        self.assertTrue(created)

        cipher.cipher.assert_called_once_with(password)
        repo.create_user.assert_called_once_with(email, ciphered_password)

        exporter.export.assert_called_once()

        self.assertEqual({'context': 'init'}, self.controller.get_state())

    @patch.multiple('controller', PasswordCipher=DEFAULT, DBRepository=DEFAULT, DBExporter=DEFAULT)
    def test_login(self, PasswordCipher, DBRepository, DBExporter):
        cipher = PasswordCipher.return_value
        repo = DBRepository.return_value
        exporter = DBExporter.return_value

        self.controller._exporter = exporter
        self.controller._cipher = cipher
        self.controller._repo = repo

        self.controller._state = {'context': 'prompt_login_info'}

        email = 'ed@conestoga.ca'
        password = '1NCR3D1BL3P455'
        ciphered_password = '8GML6E8IB6J544'

        user_record = Mock()
        user_record.email = email
        user_record.access_count = 1

        cipher.cipher.return_value = ciphered_password
        repo.find_user_with_credentials.return_value = user_record
        exporter.export.return_value = True

        logged_user = self.controller.login(email, password)

        self.assertIs(user_record, logged_user)

        cipher.cipher.assert_called_once_with(password)
        repo.update_access_count.assert_called_once_with(email, ciphered_password)
        repo.find_user_with_credentials.assert_called_once_with(email, ciphered_password)

        exporter.export.assert_called_once()

        self.assertEqual({'context': 'init'}, self.controller.get_state())

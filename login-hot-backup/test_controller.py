from unittest import TestCase

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

    def test_create_user(self):
        email = 'lalo@conestoga.ca'
        password = 'SOM3P455'

        self.controller.create_user(email, password)

    def test_login(self):
        self.controller.login()
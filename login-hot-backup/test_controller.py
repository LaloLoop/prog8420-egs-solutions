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
        self.assertEqual({}, self.controller.get_state())

    def test_create_user(self):
        self.controller.create_user()

    def test_login(self):
        self.controller.login()
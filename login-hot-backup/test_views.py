from unittest import TestCase
from unittest.mock import Mock, patch

from views import MenuView


class TestMenu(TestCase):

    def setUp(self) -> None:
        self.controller = Mock()
        self.state = {
            'context': 'init'
        }
        self.view = MenuView(self.controller)

    @patch('views.input')
    def test_Y_calls_create_user(self, input):
        input.side_effect = ["Y", "y"]

        self.view.display(self.state)
        self.view.display(self.state)

        input.assert_called_with("New user?")
        self.assertEqual(2, self.controller.create_user.call_count)

    @patch('views.input')
    def test_N_calls_login(self, input):
        input.side_effect = ["N", "n"]

        self.view.display(self.state)
        self.view.display(self.state)

        self.assertEqual(2, self.controller.login.call_count)

    @patch('views.input')
    def test_exit_calls_exit(self, input):
        input.return_value = "exit"

        self.view.display(self.state)

        self.controller.exit.assert_called()

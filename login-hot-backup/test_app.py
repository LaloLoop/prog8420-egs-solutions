from unittest import TestCase
from unittest.mock import Mock, patch, DEFAULT

from app import App


class TestApp(TestCase):

    @patch.multiple('app', MainView=DEFAULT, Controller=DEFAULT)
    def test_app_is_running(self, MainView, Controller):
        controller = Controller.return_value
        view = MainView.return_value

        state = Mock()
        controller.is_running.side_effect = [True, False]
        controller.get_state.return_value = state

        app = App()

        exit_code = app.run()

        self.assertEqual(exit_code, 0)
        controller.get_state.assert_called()
        view.display.assert_called_with(state)

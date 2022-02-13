from unittest import TestCase
from unittest.mock import Mock

from app import App


class TestApp(TestCase):

    def test_app_is_running(self):
        controller = Mock()
        view = Mock()

        state = Mock()
        controller.is_running.side_effect = [True, False]
        controller.get_state.return_value = state

        app = App(view, controller)

        exit_code = app.run()

        self.assertEqual(exit_code, 0)
        controller.get_state.assert_called()
        view.display.assert_called_with(state)

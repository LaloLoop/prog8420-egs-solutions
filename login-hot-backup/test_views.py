from unittest import TestCase
from unittest.mock import Mock, patch, call, DEFAULT

import views
from controller import Controller
from views import MenuView, CreateUserView, MainView, ViewFactory


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
        self.assertEqual(2, self.controller.prompt_user_info.call_count)

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


class TestCreateUserView(TestCase):

    def setUp(self) -> None:
        self.controller = Mock(spec=Controller)
        self.view = CreateUserView(self.controller)

    @patch('views.input')
    def test_capture_user_info(self, input):
        user_email = 'eduardo@conestoga.ca'
        password = 'SECUREP455'
        input.side_effect = [user_email, password]

        state = {
            'context': 'prompt_user_info'
        }

        self.view.display(state)

        self.controller.create_user.called_with(user_email, password)
        input_calls = [call("email: "), call("password: ")]
        input.assert_has_calls(input_calls)


class TestMainView(TestCase):

    @patch('views.ViewFactory', autospec=True)
    def test_main_view_calls_children(self, ViewFactory):
        controller = Mock(spec=Controller)
        factory_instance = ViewFactory.return_value
        product_view = Mock()
        factory_instance.get_view.return_value = product_view

        state = {'context': 'context2'}

        view = MainView(controller)
        view.display(state)

        ViewFactory.assert_called_with(controller)

        factory_instance.get_view.assert_called_with('context2')
        product_view.display.assert_called_with(state)


class TestViewFactory(TestCase):

    def test_get_create_user_view(self):
        controller = Mock()
        view_mapping = {
            'init': MenuView,
            'prompt_user_info': CreateUserView
        }

        for context, viewClass in view_mapping.items():
            Original = viewClass
            className = 'views.' + viewClass.__name__
            print(className)
            patcher = patch(className, spec=True)
            MockClass = patcher.start()

            view_factory = ViewFactory(controller)
            product_view = view_factory.get_view(context)

            MockClass.assert_called_with(controller)

            self.assertIsInstance(product_view, Original)
            patcher.stop()


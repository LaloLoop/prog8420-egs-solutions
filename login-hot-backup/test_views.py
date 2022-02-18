from unittest import TestCase
from unittest.mock import Mock, patch, call, DEFAULT

import views
from controller import Controller
from views import MenuView, CreateUserView, CreateValidatedUserView, MainView, ViewFactory, LoginView


class TestMenu(TestCase):

    def setUp(self) -> None:
        self.controller = Mock(spec=Controller)
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

        self.assertEqual(2, self.controller.prompt_login_info.call_count)

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


class TestValidatedUserView(TestCase):

    def setUp(self):
        self.controller = Mock(spec=Controller)
        self.view = CreateValidatedUserView(self.controller)

    @patch.multiple('views', input=DEFAULT, print=DEFAULT)
    def test_capture_user_info(self, input, print):
        email = 'eduardo@conestoga.ca'
        password = 'EXP3CT4DP4SS'

        input.side_effect = ['', 'my_email', email, email,
                             '', 'my_password', password, password]

        state = {
            'context': 'prompt_user_info'
        }

        self.view.display(state)

        input_calls = [
            call("email: "),
            # Please provide an email
            call("email: "),
            # Please input a valid email
            call("email: "),
            call("Please confirm your email: "),
            call("password: "),
            # Please provide a password
            call("password: "),
            # Password invalid
            call("password: "),
            call("Please confirm your password: ")
        ]
        input.assert_has_calls(input_calls)

        print_calls = [
            call('Please provide your email'),
            call('Please input a valid email, e.g. user@domain.com'),
            call('Please provide your password'),
            call('Provide a 4 or more uppercase letters password, no special characters are allowed'),
        ]

        print.assert_has_calls(print_calls)
        self.controller.create_user.called_once_with(email, password)


class TestLoginView(TestCase):

    def setUp(self) -> None:
        self._controller = Mock(spec=Controller)

    @patch('views.LoginValidatedInputView')
    def test_render_subview(self, PromptView):
        view = LoginView(self._controller)
        subview = PromptView.return_value

        state = {}

        view.display(state)

        PromptView.assert_called_once_with(view)
        subview.display.assert_called_once_with(state)

    @patch('views.print')
    def test_login_called(self, mocked_print):
        email = 'some@email.com'
        password = 'MYP455'

        user_record = Mock()
        user_record.email = email
        user_record.access_count = 1

        self._controller.login.return_value = user_record

        view = LoginView(self._controller)

        view.create_user(email, password)

        self._controller.login.asser_called_once_with(email, password)

        mocked_print.assert_called_once_with(f"{user_record.email} has logged in {user_record.access_count} time(s)")

    @patch('views.print')
    def test_login_nonexistent_user(self, mocked_print):
        self._controller.login.return_value = None

        view = LoginView(self._controller)

        view.create_user('not@auser.com', 'idontexist')

        mocked_print.assert_called_once_with("User does not exist")


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
            'prompt_user_info': CreateValidatedUserView,
            'prompt_login_info': LoginView,
        }

        for context, viewClass in view_mapping.items():
            Original = viewClass
            className = 'views.' + viewClass.__name__
            patcher = patch(className, spec=True)
            MockClass = patcher.start()

            view_factory = ViewFactory(controller)
            product_view = view_factory.get_view(context)

            MockClass.assert_any_call(controller)

            self.assertIsInstance(product_view, Original)
            patcher.stop()

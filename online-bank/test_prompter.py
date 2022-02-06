from unittest import TestCase, mock
from unittest.mock import call, Mock, patch, DEFAULT

from entities import User, Account
from prompters import Prompter, UserInfoPrompter, MainPrompter, MenuPrompter, DepositPrompter
from render import AccountsRenderer
from store import Store


class TestPrompter(TestCase):

    @mock.patch('prompters.input', create=True)
    def test_prompt(self, mocked_input):
        prompter = Prompter()

        mocked_input.side_effect = ["", "success"]

        state = {}
        done = prompter.prompt(state)

        self.assertFalse(done)
        mocked_input.assert_called_with("What's on your mind?")

        done = prompter.prompt(state)
        self.assertEqual(mocked_input.call_count, 2)

        self.assertTrue(done)


class TestUserInfoPrompter(TestCase):

    @mock.patch('prompters.input', create=True)
    def test_prompter(self, mocked_input):
        mocked_input.side_effect = ['Eduardo', 'Gutierrez']

        state = {
            'context': 'prompt_user_info'
        }

        store = Mock(spec=Store)

        prompter = UserInfoPrompter(store=store)
        done = prompter.prompt(state)

        calls = [
            call("What's your first name? "), call("And, your last name? ")
        ]

        self.assertEqual(mocked_input.call_count, 2)
        mocked_input.assert_has_calls(calls)

        self.assertTrue(done)

        store.dispatch.assert_called_with({
            'type': 'user/create',
            'payload': {
                'name': 'Eduardo',
                'last_name': 'Gutierrez'
            }
        })

    @patch.multiple('prompters', input=DEFAULT, print=DEFAULT, create=True)
    def test_prompter_waits_for_valid_input(self, input, print):
        input.side_effect = ['', 'Eduardo', '', 'Gutierrez']

        state = {
            'context': 'prompt_user_info'
        }

        store = Mock(spec=Store)

        prompter = UserInfoPrompter(store=store)
        done = prompter.prompt(state)

        self.assertEqual(4, input.call_count)

        calls = [
            call('You should enter your name, otherwise, how will I know how to call you?'),
            call("There's more than one \"Eduardo\" in this world, please tell us your last name.")
        ]

        print.assert_has_calls(calls)

        store.dispatch.assert_called_with({
            'type': 'user/create',
            'payload': {
                'name': 'Eduardo',
                'last_name': 'Gutierrez'
            }
        })

        self.assertTrue(done)

    @patch('prompters.input')
    def test_prompter_only_activates_on_prompt_user_info(self, mocked_input):
        state = {
            'context': 'something_else'
        }

        store = Mock(spec=Store)

        prompter = UserInfoPrompter(store=store)
        done = prompter.prompt(state)

        self.assertFalse(done)


class TestMainPrompter(TestCase):

    def test_main_prompter(self):
        state = {}
        store = Mock(spec=Store)

        prompt1 = Mock(spec=Prompter)
        prompt1.prompt.return_value = False

        prompt2 = Mock(spec=Prompter)
        prompt2.prompt.return_value = True

        main_prompter = MainPrompter(store, prompters=[prompt1, prompt2])
        main_prompter.prompt(state)

        prompt1.prompt.assert_called_once_with(state)
        prompt2.prompt.assert_called_once_with(state)


class TestMenuPrompter(TestCase):

    @patch.multiple('prompters', input=DEFAULT, print=DEFAULT, create=True)
    def test_menu_exit(self, input, print):
        input.side_effect = ['2', '1', 'y']

        state = {
            'menu': {
                'exit': {'type': 'program/terminate'}
            }
        }
        store = Mock(spec=Store)

        prompter = MenuPrompter(store)
        done = prompter.prompt(state)

        self.assertTrue(done)
        print_calls = [
            call("Sorry, I cannot help you with that at the moment, please choose another option"),
            call("This is an in memory Bank, your data will be lost, are you sure?"),
            call("Ok, hope you enjoyed your virtual 💸. Bye! 👋🏼")
        ]
        print.assert_has_calls(print_calls)

        self.assertEqual(input.call_count, 3)
        input_calls = [call("> "), call("> "), call("(y/N)> ")]
        input.assert_has_calls(input_calls)

        store.dispatch.assert_called_with({
            'type': 'program/terminate'
        })

    @patch.multiple('prompters', input=DEFAULT, print=DEFAULT)
    def test_menu_exit_cancel(self, input, print):
        input.side_effect = ['1', 'N']

        state = {
            'menu': {
                'exit': {'type': 'program/terminate'}
            }
        }
        store = Mock(spec=Store)

        prompter = MenuPrompter(store)
        done = prompter.prompt(state)

        self.assertTrue(done)
        print_calls = [
            call("This is an in memory Bank, your data will be lost, are you sure?"),
            call("Thanks for keeping us in business!")
        ]
        print.assert_has_calls(print_calls)

        self.assertEqual(input.call_count, 2)
        input_calls = [call("> "), call("(y/N)> ")]
        input.assert_has_calls(input_calls)

        store.dispatch.assert_called_with({
            'type': 'program/terminate_cancel'
        })

    @patch.multiple('prompters', input=DEFAULT, print=DEFAULT, sleep=DEFAULT, create=True)
    def test_menu_create_account_selected(self, input, print, sleep):
        input.side_effect = ['1']

        state = {
            'menu': {
                'create_account': {'type': 'account/create'},
            }
        }
        store = Mock(spec=Store)

        prompter = MenuPrompter(store)
        done = prompter.prompt(state)

        self.assertTrue(done)

        print.assert_called_once_with("Creating account...")
        sleep.assert_called_with(1)

        store.dispatch.assert_called_with(state['menu']['create_account'])

    @patch('prompters.input')
    def test_menu_create_user_selected(self, mocked_input):
        mocked_input.return_value = '1'

        state = {
            'menu': {
                'prompt_user_info': {'type': 'user/prompt_info'}
            }
        }

        store = Mock(spec=Store)

        prompter = MenuPrompter(store)
        done = prompter.prompt(state)

        self.assertTrue(done)

        store.dispatch.assert_called_once_with(state['menu']['prompt_user_info'])

    @patch('prompters.input')
    def test_menu_doest_not_prompt_without_menu(self, mocked_input):
        state = {
            'menu': {}
        }

        store = Mock(spec=Store)

        prompter = MenuPrompter(store)
        done = prompter.prompt(state)

        self.assertFalse(done)

        store.dispatch.assert_not_called()
        mocked_input.assert_not_called()


class TestDepositPrompter(TestCase):

    @patch.multiple('prompters', input=DEFAULT, print=DEFAULT, sleep=DEFAULT)
    def test_deposit_flow(self, input, print, sleep):
        input.side_effect = ['1', '300']
        accounts_str = "\n| ID | Balance |\n| 1  | 0 |\n| 2  | 250  |\n"
        single_account_str = "\n| ID | sBalance |\n| 1  | 300 |\n"

        accounts_renderer = Mock(spec=AccountsRenderer)
        accounts_renderer.render_table_from_state.return_value = accounts_str
        accounts_renderer.render_by_id.return_value = single_account_str

        store = Mock(spec=Store)

        state = {
            'context': 'prompt_deposit_info',
        }

        prompter = DepositPrompter(store, accounts_renderer)
        done = prompter.prompt(state)

        self.assertTrue(done)

        print_calls = [
            call("Which account would you like to deposit to?"),
            call(accounts_str),
            call('Great! How much money do you want to deposit?'),
            call('Making deposit...'),
            call("Here's your account detail"),
            call(single_account_str)
        ]
        print.assert_has_calls(print_calls)

        input_calls = [call("> "), call("> ")]
        input.assert_has_calls(input_calls)

        sleep.assert_called_once_with(1)

        store.dispatch.assert_called_once_with({
            'type': 'account/deposit',
            'payload': {
                'id': 1,
                'amount': 300
            }
        })

        accounts_renderer.render_table_from_state.assert_called_once_with(state)
        accounts_renderer.render_by_id.assert_called_once_with(state, account_id=1)

    @patch.multiple('prompters', input=DEFAULT, print=DEFAULT, sleep=DEFAULT)
    def test_deposit_validates_numeric_input(self, input, print, sleep):
        input.side_effect = ['no', '1', '', '300']

        accounts_renderer = Mock()
        accounts_renderer.render_table_from_state.return_value = 'account info'
        accounts_renderer.render_by_id.return_value = 'single account'

        state = {
            'context': 'prompt_deposit_info',
        }

        store = Mock(spec=Store)

        prompter = DepositPrompter(store, accounts_renderer)
        done = prompter.prompt(state)

        self.assertTrue(done)

        print_calls = [
            call("Which account would you like to deposit to?"),
            call('account info'),
            call('That\'s not a valid ID, have a look again'),
            call("Which account would you like to deposit to?"),
            call('account info'),
            call('Great! How much money do you want to deposit?'),
            call("Wait a minute, that does not look like a number."),
            call("Great! How much money do you want to deposit?"),
            call('Making deposit...'),
            call("Here's your account detail"),
            call('single account')
        ]
        print.assert_has_calls(print_calls)

        input_calls = [call("> "), call("> ")]
        input.assert_has_calls(input_calls)

    def test_deposit_does_not_prompt_if_not_in_state(self):
        state = {
            'context': 'some_other'
        }

        store = Mock(spec=Store)
        accounts_renderer = Mock()

        prompter = DepositPrompter(store, accounts_renderer)

        done = prompter.prompt(state)

        self.assertFalse(done)
        store.dispatch.assert_not_called()
        accounts_renderer.render.assert_not_called()
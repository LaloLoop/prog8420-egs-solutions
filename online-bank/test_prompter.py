from unittest import TestCase, mock
from unittest.mock import call, Mock, patch, DEFAULT

from entities import User, Account
from prompters import Prompter, UserInfoPrompter, MainPrompter, MenuPrompter, DepositPrompter, WithdrawPrompter, \
    TransferPrompter
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

    @patch.multiple('prompters', get_user_account_by_id=DEFAULT)
    def setUp(self, get_user_account_by_id) -> None:
        self.account_selector = get_user_account_by_id
        self.account_selector.side_effect = [Mock(spec=Account)]

    @patch.multiple('prompters', input=DEFAULT, print=DEFAULT, sleep=DEFAULT)
    def test_deposit_flow(self, input, print, sleep):
        input.side_effect = ['1', '300']
        accounts_str = "\n| ID | Balance |\n| 1  | 0 |\n| 2  | 250  |\n"
        single_account_str = "\n| ID | Balance |\n| 1  | 300 |\n"

        accounts_renderer = Mock(spec=AccountsRenderer)
        accounts_renderer.render_table_from_state.return_value = accounts_str
        accounts_renderer.render_by_id.return_value = single_account_str

        store = Mock(spec=Store)

        state = {
            'context': 'prompt_deposit_info',
        }

        prompter = DepositPrompter(store, accounts_renderer, self.account_selector)
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
        input.side_effect = ['no', '1', '', '-300', '300']

        accounts_renderer = Mock()
        accounts_renderer.render_table_from_state.return_value = 'account info'
        accounts_renderer.render_by_id.return_value = 'single account'

        state = {
            'context': 'prompt_deposit_info',
        }

        store = Mock(spec=Store)

        prompter = DepositPrompter(store, accounts_renderer, self.account_selector)
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
            call("The amount has to be greater than 0"),
            call("Great! How much money do you want to deposit?"),
            call('Making deposit...'),
            call("Here's your account detail"),
            call('single account')
        ]
        print.assert_has_calls(print_calls)

        input_calls = [call("> "), call("> "), call("> "), call("> ")]
        input.assert_has_calls(input_calls)

    def test_deposit_does_not_prompt_if_not_in_state(self):
        state = {
            'context': 'some_other'
        }

        store = Mock(spec=Store)
        accounts_renderer = Mock()

        prompter = DepositPrompter(store, accounts_renderer, self.account_selector)

        done = prompter.prompt(state)

        self.assertFalse(done)
        store.dispatch.assert_not_called()
        accounts_renderer.render.assert_not_called()

    @patch.multiple('prompters', input=DEFAULT, print=DEFAULT, sleep=DEFAULT)
    def test_withdraw_validates_account_id(self, input, print, sleep):
        input.side_effect = ['2', '1', '10']

        accounts_renderer = Mock()
        accounts_renderer.render_table_from_state.return_value = 'account info'
        accounts_renderer.render_by_id.return_value = 'single account'
        self.account_selector.side_effect = [None, Mock(Account)]

        state = {
            'context': 'prompt_deposit_info',
        }

        store = Mock(spec=Store)
        store.state = state

        prompter = DepositPrompter(store, accounts_renderer, self.account_selector)
        done = prompter.prompt(state)

        self.assertTrue(done)

        print_calls = [
            call("Which account would you like to deposit to?"),
            call('account info'),
            call("That account does not exist, please pick a valid one"),
            call("Which account would you like to deposit to?"),
            call('account info'),
            call('Great! How much money do you want to deposit?'),
            call('Making deposit...'),
            call("Here's your account detail"),
            call('single account')
        ]
        print.assert_has_calls(print_calls)

        input_calls = [call("> "), call("> "), call("> ")]
        input.assert_has_calls(input_calls)


class TestWithdrawPrompter(TestCase):

    @patch.multiple('prompters', input=DEFAULT, print=DEFAULT, sleep=DEFAULT, get_user_account_by_id=DEFAULT)
    def test_only_prompts_on_prompt_withdraw_info(self, input, print, sleep, get_user_account_by_id):
        state = {
            'context': 'test'
        }

        accounts_renderer = Mock(spec=AccountsRenderer)
        store = Mock(spec=Store)

        prompter = WithdrawPrompter(store, accounts_renderer, get_user_account_by_id)

        done = prompter.prompt(state)

        self.assertFalse(done)
        accounts_renderer.render_table_from_state.assert_not_called()
        store.dispatch.assert_not_called()
        input.assert_not_called()
        print.assert_not_called()
        sleep.assert_not_called()
        get_user_account_by_id.assert_not_called()

    @patch.multiple('prompters', input=DEFAULT, print=DEFAULT, sleep=DEFAULT, get_user_account_by_id=DEFAULT)
    def test_withdraw_flow(self, input, print, sleep, get_user_account_by_id):
        input.side_effect = ['1', '100']
        accounts_str = "\n| ID | Balance |\n| 1  | 100 |\n| 2  | 250  |\n"

        accounts_renderer = Mock(spec=AccountsRenderer)
        accounts_renderer.render_table_from_state.return_value = accounts_str
        get_user_account_by_id.return_value = Mock(spec=Account)

        store = Mock(spec=Store)

        state = {
            'context': 'prompt_withdraw_info'
        }

        store.state = state

        prompter = WithdrawPrompter(store, accounts_renderer, get_user_account_by_id)

        done = prompter.prompt(state)

        self.assertTrue(done)

        get_user_account_by_id.assert_called_once_with(state, account_id=1)

        print_calls = [
            call("Which account would you like to withdraw from?"),
            call(accounts_str),
            call("How much money would you like to withdraw?"),
            call("Getting your money..."),
            call("You've withdrawn $100")
        ]
        print.assert_has_calls(print_calls)

        input_calls = [call("> "), call("> ")]
        input.assert_has_calls(input_calls)

        store.dispatch.assert_called_with({
            'type': 'account/withdraw',
            'payload': {
                'id': 1,
                'amount': 100
            }
        })

        sleep.assert_called_once_with(1)

    @patch.multiple('prompters', input=DEFAULT, print=DEFAULT, sleep=DEFAULT, get_user_account_by_id=DEFAULT)
    def test_withdraw_validates_numeric_input(self, input, print, sleep, get_user_account_by_id):
        input.side_effect = ['hi', '1', '', '100']

        accounts_renderer = Mock(spec=AccountsRenderer)
        accounts_renderer.render_table_from_state.return_value = 'account info'
        accounts_renderer.render_by_id.return_value = 'single account'
        get_user_account_by_id.return_value = Mock(spec=Account)

        state = {
            'context': 'prompt_withdraw_info',
        }

        store = Mock(spec=Store)
        store.state = state

        prompter = WithdrawPrompter(store, accounts_renderer, get_user_account_by_id)
        done = prompter.prompt(state)

        self.assertTrue(done)

        print_calls = [
            call("Which account would you like to withdraw from?"),
            call('account info'),
            call('That\'s not a numeric ID, have a look again'),
            call("Which account would you like to withdraw from?"),
            call('account info'),
            call("How much money would you like to withdraw?"),
            call("Hold your horses, please give a number."),
            call("How much money would you like to withdraw?"),
            call("Getting your money..."),
            call("You've withdrawn $100")
        ]

        print.assert_has_calls(print_calls)

        input_calls = [call("> "), call("> "), call("> "), call("> ")]
        input.assert_has_calls(input_calls)

    @patch.multiple('prompters', input=DEFAULT, print=DEFAULT, sleep=DEFAULT, get_user_account_by_id=DEFAULT)
    def test_withdraw_validates_negative_numbers(self, input, print, sleep, get_user_account_by_id):
        input.side_effect = ['1', '-100', '100']

        accounts_renderer = Mock()
        accounts_renderer.render_table_from_state.return_value = 'account info'
        accounts_renderer.render_by_id.return_value = 'single account'
        get_user_account_by_id.return_value = Mock(spec=Account)

        state = {
            'context': 'prompt_withdraw_info',
        }

        store = Mock(spec=Store)
        store.state = state

        prompter = WithdrawPrompter(store, accounts_renderer, get_user_account_by_id)
        done = prompter.prompt(state)

        self.assertTrue(done)

        print_calls = [
            call("Which account would you like to withdraw from?"),
            call('account info'),
            call("How much money would you like to withdraw?"),
            call("Your amount has to be greater than 0"),
            call("How much money would you like to withdraw?"),
            call("Getting your money..."),
            call("You've withdrawn $100")
        ]

        print.assert_has_calls(print_calls)

        input_calls = [call("> "), call("> "), call("> ")]
        input.assert_has_calls(input_calls)

    @patch.multiple('prompters', input=DEFAULT, print=DEFAULT, sleep=DEFAULT, get_user_account_by_id=DEFAULT)
    def test_withdraw_notifies_error(self, input, print, sleep, get_user_account_by_id):
        input.side_effect = ['1', '1000']

        accounts_renderer = Mock()
        accounts_renderer.render_table_from_state.return_value = 'account info'
        accounts_renderer.render_by_id.return_value = 'single account'
        get_user_account_by_id.return_value = Mock(spec=Account)

        state = {
            'context': 'prompt_withdraw_info',
        }

        store = Mock(spec=Store)
        store.state = {**state, 'error': 'some_error'}

        prompter = WithdrawPrompter(store, accounts_renderer, get_user_account_by_id)
        done = prompter.prompt(state)

        self.assertTrue(done)

        print_calls = [
            call("Which account would you like to withdraw from?"),
            call('account info'),
            call("How much money would you like to withdraw?"),
            call("Getting your money..."),
            call("I could not get your money. some_error")
        ]

        print.assert_has_calls(print_calls)

        input_calls = [call("> "), call("> ")]
        input.assert_has_calls(input_calls)

    @patch.multiple('prompters', input=DEFAULT, print=DEFAULT, sleep=DEFAULT, get_user_account_by_id=DEFAULT)
    def test_withdraw_validates_account_id(self, input, print, sleep, get_user_account_by_id):
        input.side_effect = ['2', '1', '10']

        accounts_renderer = Mock()
        accounts_renderer.render_table_from_state.return_value = 'account info'
        accounts_renderer.render_by_id.return_value = 'single account'
        get_user_account_by_id.side_effect = [None, Mock(Account)]

        state = {
            'context': 'prompt_withdraw_info',
        }

        store = Mock(spec=Store)
        store.state = state

        prompter = WithdrawPrompter(store, accounts_renderer, get_user_account_by_id)
        done = prompter.prompt(state)

        self.assertTrue(done)

        print_calls = [
            call("Which account would you like to withdraw from?"),
            call('account info'),
            call("That account does not exist, please pick a valid one"),
            call("Which account would you like to withdraw from?"),
            call('account info'),
            call("How much money would you like to withdraw?"),
            call("Getting your money..."),
            call(f"You've withdrawn $10")
        ]

        print.assert_has_calls(print_calls)

        input_calls = [call("> "), call("> ")]
        input.assert_has_calls(input_calls)

        account_by_id_calls = [
            call(state, account_id=2),
            call(state, account_id=1)
        ]

        get_user_account_by_id.assert_has_calls(account_by_id_calls)


class TestTransferPrompter(TestCase):

    @patch.multiple('prompters', input=DEFAULT, print=DEFAULT, sleep=DEFAULT, get_user_account_by_id=DEFAULT)
    def test_only_prompts_on_prompt_transfer_info(self, input, print, sleep, get_user_account_by_id):
        state = {
            'context': 'test'
        }

        accounts_renderer = Mock(spec=AccountsRenderer)
        store = Mock(spec=Store)

        prompter = TransferPrompter(store, accounts_renderer, get_user_account_by_id)

        done = prompter.prompt(state)

        self.assertFalse(done)
        accounts_renderer.render_table_from_state.assert_not_called()
        store.dispatch.assert_not_called()
        input.assert_not_called()
        print.assert_not_called()
        sleep.assert_not_called()
        get_user_account_by_id.assert_not_called()

    @patch.multiple('prompters', input=DEFAULT, print=DEFAULT, sleep=DEFAULT, get_user_account_by_id=DEFAULT)
    def test_transfer_flow(self, input, print, sleep, get_user_account_by_id):
        input.side_effect = ['1', '100', '2']
        account_str = "accounts_summary"

        accounts_renderer = Mock(spec=AccountsRenderer)
        accounts_renderer.render_table_from_state.return_value = account_str
        get_user_account_by_id.return_value = Mock(spec=Account)

        store = Mock(spec=Store)

        state = {
            'context': 'prompt_transfer_info'
        }

        store.state = state

        prompter = TransferPrompter(store, accounts_renderer, get_user_account_by_id)
        done = prompter.prompt(state)

        self.assertTrue(done)

        print_calls = [
            call('Please provide the source account'),
            call(account_str),
            call('How much money do you want to transfer?'),
            call('What\'s the destination account?'),
            call(account_str),
            call('Working on it...'),
            call('Done! the money has been transferred')
        ]
        print.assert_has_calls(print_calls)

        input_calls = [call("> "), call("> "), call("> ")]
        input.assert_has_calls(input_calls)

        store.dispatch.assert_called_with({
            'type': 'account/transfer',
            'payload': {
                'source_acct_id': 1,
                'dest_acct_id': 2,
                'amount': 100
            }
        })

        sleep.assert_called_once_with(1)

    @patch.multiple('prompters', input=DEFAULT, print=DEFAULT, sleep=DEFAULT, get_user_account_by_id=DEFAULT)
    def test_transfer_validates_numeric_input(self, input, print, sleep, get_user_account_by_id):
        input.side_effect = ['blah', '1', 'hundred', '-100', '0', '100', 'two', '2']
        input_calls = [call("> "), call("> "), call("> "), call("> "), call("> "), call("> ")]
        print_calls = [
            call('Please provide the source account'),
            call("accounts_info"),
            call("Please provide a numeric ID"),
            call('Please provide the source account'),
            call("accounts_info"),
            call('How much money do you want to transfer?'),
            call("Please provide a numeric amount"),
            call('How much money do you want to transfer?'),
            call('I see what you did there. The amount cannot be negative'),
            call('How much money do you want to transfer?'),
            call('Your amount has to be greater than 0'),
            call('How much money do you want to transfer?'),
            call('What\'s the destination account?'),
            call("accounts_info"),
            call("Please provide a numeric ID"),
            call('What\'s the destination account?'),
            call("accounts_info"),
            call('Working on it...'),
            call('Done! the money has been transferred')
        ]

        accounts_renderer = Mock(spec=AccountsRenderer)
        accounts_renderer.render_table_from_state.return_value='accounts_info'
        get_user_account_by_id.return_value = Mock(spec=Account)

        store = Mock(spec=Store)

        state = {
            'context': 'prompt_transfer_info'
        }

        store.state = state

        prompter = TransferPrompter(store, accounts_renderer, get_user_account_by_id)
        done = prompter.prompt(state)

        self.assertTrue(done)

        print.assert_has_calls(print_calls)
        input.assert_has_calls(input_calls)

        store.dispatch.assert_called_with({
            'type': 'account/transfer',
            'payload': {
                'source_acct_id': 1,
                'dest_acct_id': 2,
                'amount': 100
            }
        })

        sleep.assert_called_once_with(1)

    @patch.multiple('prompters', input=DEFAULT, print=DEFAULT, sleep=DEFAULT, get_user_account_by_id=DEFAULT)
    def test_transfer_validates_existing_account(self, input, print, sleep, get_user_account_by_id):
        input.side_effect = ['3', '2', '10', '4', '1']

        accounts_renderer = Mock()
        accounts_renderer.render_table_from_state.return_value = 'accounts info'
        get_user_account_by_id.side_effect = [None, Mock(spec=Account), None, Mock(spec=Account)]

        state = {
            'context': 'prompt_transfer_info'
        }

        account_by_id_calls = [
            call(state, 3),
            call(state, 2),
            call(state, 4),
            call(state, 1),
        ]

        store = Mock(spec=Store)
        store.state = state

        prompter = TransferPrompter(store, accounts_renderer, get_user_account_by_id)
        done = prompter.prompt(state)

        self.assertTrue(done)

        print_calls = [
            call('Please provide the source account'),
            call("accounts info"),
            call("Sorry, that account does not exist, please choose a valid ID"),
            call('Please provide the source account'),
            call("accounts info"),
            call('How much money do you want to transfer?'),
            call('What\'s the destination account?'),
            call("accounts info"),
            call("Sorry, that account does not exist, please choose a valid ID"),
            call('What\'s the destination account?'),
            call("accounts info"),
            call('Working on it...'),
            call('Done! the money has been transferred')
        ]
        input_calls = [
            call("> "),
            call("> "),
            call("> "),
            call("> "),
            call("> ")
        ]

        print.assert_has_calls(print_calls)
        input.assert_has_calls(input_calls)

        get_user_account_by_id.assert_has_calls(account_by_id_calls)

    @patch.multiple('prompters', input=DEFAULT, print=DEFAULT, sleep=DEFAULT, get_user_account_by_id=DEFAULT)
    def test_transfer_shows_errors_if_any(self, input, print, sleep, get_user_account_by_id):
        input.side_effect = ['1', '100', '2']
        accounts_renderer = Mock(spec=AccountsRenderer)
        accounts_renderer.render_table_from_state.return_value = 'accounts info'
        get_user_account_by_id.side_effect = [Mock(spec=Account), Mock(spec=Account)]

        state = {
            'context': 'prompt_transfer_info',
        }

        store = Mock(spec=Store)
        store.state = {**state, 'error': 'some_error'}

        prompter = TransferPrompter(store, accounts_renderer, get_user_account_by_id)
        done = prompter.prompt(state)

        self.assertTrue(done)

        print_calls = [
            call('Please provide the source account'),
            call("accounts info"),
            call('How much money do you want to transfer?'),
            call('What\'s the destination account?'),
            call("accounts info"),
            call('Working on it...'),
            call('I could not complete your transfer. some_error')
        ]

        print.assert_has_calls(print_calls)

        input_calls = [call("> "), call("> ")]
        input.assert_has_calls(input_calls)


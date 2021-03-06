from unittest import TestCase, mock
from unittest.mock import Mock, patch, DEFAULT

from entities import Bank, User, Account

from reducers import main_reducer, user_reducer, bank_reducer, STATE_MAPPING, exit_reducer, account_created, \
    menu_reducer, error_reducer, SINGLE_ACCOUNT_MENU, MULTIPLE_ACCOUNT_MENU


class TestMainReducer(TestCase):
    @patch.multiple(
        'reducers',
        user_reducer=DEFAULT,
        bank_reducer=DEFAULT,
        exit_reducer=DEFAULT,
        account_created=DEFAULT,
        menu_reducer=DEFAULT,
        error_reducer=DEFAULT
    )
    def test_main_reducer(self, user_reducer, bank_reducer, exit_reducer, account_created, menu_reducer, error_reducer):
        bank = Mock(spec=Bank)
        user = Mock(spec=User)

        test_state = {'bank': bank}
        bank_reducer.return_value = test_state

        test_state = {**test_state, 'session': user}
        user_reducer.return_value = test_state

        test_state = {**test_state, 'exit': False}
        exit_reducer.return_value = test_state

        test_state = {**test_state, 'account_created': False}
        account_created.return_value = test_state

        test_state = {**test_state, 'context': 'some', 'menu': {}}
        menu_reducer.return_value = test_state

        test_state = {**test_state, 'error': ''}
        error_reducer.return_value = test_state

        action = {'type': 'some/action'}

        STATE_MAPPING['bank'] = bank_reducer
        STATE_MAPPING['session'] = user_reducer
        STATE_MAPPING['exit'] = exit_reducer
        STATE_MAPPING['account_created'] = account_created
        STATE_MAPPING['menu'] = menu_reducer
        STATE_MAPPING['error'] = error_reducer

        original_state = {}
        state = main_reducer(original_state, action)

        bank_reducer.assert_called_once_with(original_state, action)
        exp_state = {
            'bank': bank
        }
        user_reducer.assert_called_once_with(exp_state, action)
        exp_state = {
            **exp_state,
            'session': user
        }
        exit_reducer.assert_called_once_with(exp_state, action)
        exp_state = {
            **exp_state,
            'exit': False
        }
        account_created.assert_called_once_with(exp_state, action)
        exp_state = {
            **exp_state,
            'account_created': False
        }
        menu_reducer.assert_called_once_with(exp_state, action)
        exp_state = {
            **exp_state,
            'menu': {},
            'context': 'some'
        }
        error_reducer.assert_called_once_with(exp_state, action)

        self.assertEqual({
            'session': user,
            'bank': bank,
            'exit': False,
            'account_created': False,
            'context': 'some',
            'menu': {},
            'error': ''
        }, state)


class TestBankReducer(TestCase):

    def test_bank_reducer(self):
        state = {}
        action = {'type': 'init'}

        state = bank_reducer(state, action)

        self.assertIsInstance(state['bank'], Bank)

    def test_adds_account(self):
        user = Mock(spec=User)
        bank = Mock(spec=Bank)
        state = {
            'session': user,
            'bank': bank
        }

        action = {'type': 'account/create'}

        state = bank_reducer(state, action)

        user.create_account.assert_called_with(bank)

        self.assertTrue(state['account_created'])

    def test_makes_deposit(self):
        user = Mock(spec=User)
        account1 = Mock(spec=Account)
        account1.id = 1
        account1.balance = 0
        account2 = Mock(spec=Account)
        account2.id = 2
        account2.balance = 0
        user.accounts = [account1, account2]

        state = {
            'session': user
        }

        action = {'type': 'account/deposit', 'payload': {'id': 2, 'amount': 100}}

        bank_reducer(state, action)

        account2.deposit.assert_called_with(100)

    def test_makes_withdraw(self):
        user = Mock(spec=User)
        account = Mock(spec=Account)
        account.id = 1
        account.balance = 100

        user.accounts = [account]

        state = {
            'session': user
        }

        action = {'type': 'account/withdraw', 'payload': {'id': 1, 'amount': 100}}

        bank_reducer(state, action)

        account.withdraw.assert_called_with(100)

    def test_errors_with_negative_withdraw(self):
        user = Mock(spec=User)
        account = Mock(spec=Account)
        account.id = 1
        account.balance = 50

        user.accounts = [account]

        account.withdraw.return_value = 0

        state = {
            'session': user
        }

        action = {'type': 'account/withdraw', 'payload': {'id': 1, 'amount': 100}}

        state = bank_reducer(state, action)

        self.assertEqual({'session': user, 'error': 'Uh oh, you can withdraw at most $50'}, state)

        account.balance = 0

        state = bank_reducer(state, action)

        self.assertEqual({'session': user, 'error': 'Not enough funds to withdraw $100'}, state)

        account.balance = 100

        state = bank_reducer(state, action)

        self.assertEqual({'session': user, 'error': ''}, state)

    def test_transfer(self):
        user = Mock(spec=User)
        account1 = Mock(spec=Account)
        account1.id = 1
        account1.balance = 100

        account2 = Mock(spec=Account)
        account2.id = 2
        account2.balance = 200
        account2.transfer.return_value = 100

        amount = 100

        user.accounts = [account1, account2]

        state = {
            'session': user
        }

        action = {'type': 'account/transfer', 'payload': {'source_acct_id': 2, 'amount': amount, 'dest_acct_id': 1}}

        bank_reducer(state, action)

        account2.transfer.assert_called_with(account1, amount)

    def test_transfer_fails_with_account_not_found(self):
        user = Mock(spec=User)
        account1 = Mock(spec=Account)
        account1.id = 1

        user.accounts = [account1]

        state = {
            'session': user
        }

        action = {
            'type': 'account/transfer',
            'payload': {'source_acct_id': 2, 'dest_acct_id': 1, 'amount': 100}
        }

        new_state = bank_reducer(state, action)

        self.assertEqual(new_state, {**state, 'error': 'Could not find source account with id: 2'})

        action = {
            'type': 'account/transfer',
            'payload': {
                'source_acct_id': 1,
                'dest_acct_id': 2,
                'amount': 100
            }
        }

        new_state = bank_reducer(state, action)

        self.assertEqual(new_state, {**state, 'error': 'Could not find destination account with id: 2'})

    def test_transfer_fails_with_insufficient_funds(self):
        account1 = Mock(spec=Account)
        account1.id = 1
        account1.transfer.return_value = 0
        account2 = Mock(spec=Account)
        account2.id = 2

        user = Mock(spec=User)
        user.accounts = [account1, account2]

        amount = 200

        state = {
            'session': user
        }

        action = {
            'type': 'account/transfer',
            'payload': {
                'source_acct_id': 1,
                'dest_acct_id': 2,
                'amount': amount
            }
        }

        new_state = bank_reducer(state, action)

        self.assertEqual(new_state, {**state, 'error': 'Could not perform transfer, insufficient funds'})

    def test_transfer_fails_with_same_account(self):
        state = {}
        action = {
            'type': 'account/transfer',
            'payload': {
                'source_acct_id': 1,
                'dest_acct_id': 1,
                'amount': 10
            }
        }

        new_state = bank_reducer(state, action)

        self.assertEqual(new_state, {'error': 'Source and destination account must be different'})


class TestUserReducer(TestCase):

    def test_user_reducer_inits(self):
        state = {}
        action = {'type': 'init'}

        state = user_reducer(state, action)

        self.assertEqual(state, {'session': None})

    def test_user_reducer(self):
        bank = Mock(spec=Bank)
        bank.create_user.return_value = User(name='Eduardo', last_name='Gutierrez')

        state = {
            'session': None,
            'bank': bank
        }
        action = {'type': 'user/create', 'payload': {
            'name': 'Eduardo',
            'last_name': 'Gutierrez'
        }}

        state = user_reducer(state, action)

        bank.create_user.assert_called_once_with('Eduardo', 'Gutierrez')

        self.assertIsNotNone(state['session'])
        sess_user = state['session']
        self.assertEqual('Eduardo', sess_user.name)
        self.assertEqual('Gutierrez', sess_user.last_name)


class TestUIReducers(TestCase):

    def test_exit_reducer(self):
        state = {}
        action = {'type': 'init'}

        state = exit_reducer(state, action)

        self.assertFalse(state['exit'])

        action = {'type': 'program/terminate'}

        state = exit_reducer(state, action)

        self.assertTrue(state['exit'])

    def test_account_created(self):
        state = {}
        action = {'type': 'init'}

        state = account_created(state, action)

        self.assertFalse(state['account_created'])

        action = {'type': 'account/create'}
        state = {'account_created': True}
        state = account_created(state, action)

        self.assertTrue(state['account_created'])

        action = {'type': 'another/action'}

        state = account_created(state, action)

        self.assertFalse(state['account_created'])

    def test_error_reducer(self):
        state = {}
        action = {'type': 'init'}

        state = error_reducer(state, action)

        self.assertEqual(state['error'], '')

        action = {'type': 'account/withdraw'}
        state = {'error': 'some descriptive error'}

        state = error_reducer(state, action)

        self.assertEqual(state['error'], 'some descriptive error')

        action = {'type': 'account/transfer'}
        state = error_reducer(state, action)
        self.assertEqual(state['error'], 'some descriptive error')

        action = {'type': 'another/action'}
        state = error_reducer(state, action)

        self.assertEqual({
            'error': ''
        }, state)


class TestMenuReducer(TestCase):
    def test_menu_inits(self):
        state = {}
        action = {'type': 'init'}

        state = menu_reducer(state, action)

        self.assertEqual({
            'context': 'missing_user_account',
            'menu': {
                'prompt_user_info': {
                    'type': 'user/prompt_info'
                },
                'exit': {
                    'type': 'program/terminate'
                }
            }
        }, state)

    def test_menu_disables_on_user_info(self):
        state = {
            'context': 'missing_user_account',
            'menu': {
                'some': {}
            }
        }
        action = {'type': 'user/prompt_info'}

        state = menu_reducer(state, action)

        self.assertEqual({
            'context': 'prompt_user_info',
            'menu': {}
        }, state)

    def test_menu_disables_on_deposit_info(self):
        state = {
            'context': 'single_account',
            'menu': {
                'some': {}
            }
        }
        action = {'type': 'account/prompt_deposit_info'}

        state = menu_reducer(state, action)

        self.assertEqual({
            'context': 'prompt_deposit_info',
            'menu': {}
        }, state)

    def test_menu_disables_on_withdraw_info(self):
        state = {
            'context': 'single_account',
            'menu': {
                'some': {}
            }
        }
        action = {'type': 'account/prompt_withdraw_info'}

        state = menu_reducer(state, action)

        self.assertEqual({
            'context': 'prompt_withdraw_info',
            'menu': {}
        }, state)

    def test_menu_disables_on_transfer_info(self):
        state = {
            'context': 'multiple_account',
            'menu': {
                'some': {}
            }
        }
        action = {'type': 'account/prompt_transfer_info'}

        state = menu_reducer(state, action)

        self.assertEqual({
            'context': 'prompt_transfer_info',
            'menu': {}
        }, state)

    def test_menu_no_account_when_user_create(self):
        state = {
            'context': 'missing_user_account',
        }

        action = {'type': 'user/create'}

        state = menu_reducer(state, action)

        self.assertEqual({
            'context': 'no_accounts',
            'menu': {
                'create_account': {
                    'type': 'account/create'
                },
                'exit': {
                    'type': 'program/terminate'
                }
            }
        }, state)

    def test_menu_single_account_when_account_create(self):
        user = Mock(spec=User)
        account1 = Mock(spec=Account)
        user.accounts = [account1]

        state = {
            'context': 'no_accounts',
            'session': user
        }

        expected_state = {
            'context': 'single_account',
            'session': user,
            'menu': SINGLE_ACCOUNT_MENU
        }

        action = {'type': 'account/create'}
        actual_state = menu_reducer(state, action)
        self.assertEqual(expected_state, actual_state)

        action = {'type': 'account/deposit'}
        actual_state = menu_reducer(state, action)
        self.assertEqual(expected_state, actual_state)

        action = {'type': 'account/withdraw'}
        actual_state = menu_reducer(state, action)
        self.assertEqual(expected_state, actual_state)

    def test_menu_multiple_account_when_account_create(self):
        user = Mock(spec=User)
        account1 = Mock(spec=Account)
        account2 = Mock(spec=Account)
        user.accounts = [account1, account2]

        state = {
            'context': 'single_account',
            'session': user,
            'menu': SINGLE_ACCOUNT_MENU
        }

        expected_state = {
            'context': 'multiple_account',
            'session': user,
            'menu': MULTIPLE_ACCOUNT_MENU
        }

        action = {'type': 'account/create'}

        actual_state = menu_reducer(state, action)
        self.assertEqual(expected_state, actual_state)

        action = {'type': 'account/transfer'}
        actual_state = menu_reducer(state, action)
        self.assertEqual(expected_state, actual_state)

        action = {'type': 'account/deposit'}
        actual_state = menu_reducer(state, action)
        self.assertEqual(expected_state, actual_state)

        action = {'type': 'account/withdraw'}
        actual_state = menu_reducer(state, action)
        self.assertEqual(expected_state, actual_state)



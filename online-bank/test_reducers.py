from unittest import TestCase, mock
from unittest.mock import Mock, patch, DEFAULT

from entities import Bank, User

from reducers import main_reducer, user_reducer, bank_reducer, STATE_MAPPING, exit_reducer, account_created, \
    menu_reducer


class TestMainReducer(TestCase):
    @patch.multiple(
        'reducers',
        user_reducer=DEFAULT,
        bank_reducer=DEFAULT,
        exit_reducer=DEFAULT,
        account_created=DEFAULT,
        menu_reducer=DEFAULT
    )
    def test_main_reducer(self, user_reducer, bank_reducer, exit_reducer, account_created, menu_reducer):
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

        action = {'type': 'some/action'}

        STATE_MAPPING['bank'] = bank_reducer
        STATE_MAPPING['session'] = user_reducer
        STATE_MAPPING['exit'] = exit_reducer
        STATE_MAPPING['account_created'] = account_created
        STATE_MAPPING['menu'] = menu_reducer

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

        self.assertEqual({
            'session': user,
            'bank': bank,
            'exit': False,
            'account_created': False,
            'context': 'some',
            'menu': {}
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
        state = {
            'context': 'no_accounts'
        }

        action = {'type': 'account/create'}

        state = menu_reducer(state, action)

        self.assertEqual({
            'context': 'single_account',
            'menu': {
                'deposit': {
                    'type': 'account/prompt_deposit_info'
                },
                'withdraw': {
                    'type': 'account/prompt_withdraw_info'
                },
                'create_account': {
                    'type': 'account/create'
                },
                'exit': {
                    'type': 'program/terminate'
                }
            }
        }, state)
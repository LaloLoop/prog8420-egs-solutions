from unittest import TestCase
from unittest.mock import Mock

from entities import User, Account
from render import Renderer, WelcomeRenderer, MenuRenderer, MainRenderer, AccountsRenderer


class TestRenderer(TestCase):
    def test_render(self):
        r = Renderer()
        state = {'some': 'value', 'another': 'value'}

        result = r.render(state)

        self.assertEqual(result, "\nRender called from root class Renderer\nState keys: ['some', 'another']\n")


class TestWelcomeRenderer(TestCase):
    def test_render(self):
        welcome_renderer = WelcomeRenderer()

        state = {'session': None}

        result = welcome_renderer.render(state)

        self.assertEqual(result, "\nWelcome to online banking!\n")


class TestMenuRenderer(TestCase):
    def test_render(self):
        state = {
            'context': 'missing_user_account',
            'menu': {
                'prompt_user_info': {},
                'exit': {}
            }
        }

        menu_renderer = MenuRenderer()
        result = menu_renderer.render(state)

        self.assertEqual("\nPlease create a user to begin.\n1. Create my user\n2. Exit\n", result)

    def test_render_non_account_menu(self):
        state = {
            'context': 'no_accounts',
            'menu': {
                'create_account': {},
                'exit': {}
            }
        }

        menu_renderer = MenuRenderer()
        result = menu_renderer.render(state)

        self.assertEqual(
            "Your user is setup and you can now create a Bank account!\n1. Create account\n2. Exit\n",
            result
        )

    def test_render_account_available(self):
        state = {
            'context': 'single_account',
            'menu': {
                'deposit': {},
                'withdraw': {},
                'create_account': {},
                'exit': {}
            }
        }

        renderer = MenuRenderer()
        result = renderer.render(state)

        self.assertEqual(
            "\nHow may I help you?\n1. Deposit\n2. Withdraw\n3. Create account\n4. Exit\n",
            result
        )


class TestMainRenderer(TestCase):
    def test_render(self):
        state = {
            'salute': 'Hallo',
            'person': 'Eduardo'
        }

        class Renderer1(Renderer):
            def render(self, state):
                return f"\n{state['salute']}, "

        class Renderer2(Renderer):
            def render(self, state):
                return f"{state['person']}!\n"

        mr = MainRenderer(renderers=[Renderer1(), Renderer2()])

        self.assertEqual("\nHallo, Eduardo!\n", mr.render(state))


class TestAccountsRenderer(TestCase):
    def test_render(self):
        account = Mock(spec=Account)
        account.id = 1
        account.balance = 0
        user = Mock(spec=User)
        user.accounts = [account]

        state = {
            'context': 'some',
            'session': user,
            'account_created': False
        }

        renderer = AccountsRenderer()
        result = renderer.render(state)

        self.assertEqual("", result)

        state['account_created'] = True
        state['context'] = 'single_account'

        result = renderer.render(state)

        self.assertEqual(f"\nYour account was successfully created\n\n| Acct No. | Balance |\n| {account.id} | "
                         f"{account.balance} |\n\n", result)

    def test_render_accounts(self):
        user = Mock(spec=User)
        user.accounts = []

        state = {
            'session': user,
            'context': 'no_accounts',
            'account_created': False
        }

        account = Mock(spec=Account)
        account.id = 1
        account.balance = 0
        user = Mock(spec=User)

        renderer = AccountsRenderer()
        result = renderer.render(state)

        self.assertEqual("You have 0 accounts\n", result)

        user.accounts = [account]

        state = {
            'session': user,
            'context': 'single_account',
            'account_created': False
        }

        result = renderer.render(state)

        self.assertEqual(f"\n| Acct No. | Balance |\n| {account.id} | "
                         f"{account.balance} |\n\n", result)

        account2 = Mock(spec=Account)
        account2.id = 2
        account2.balance = 0
        user.accounts = [account, account2]

        state = {
            'session': user,
            'context': 'multiple_account',
            'account_created': False
        }

        result = renderer.render(state)

        self.assertEqual(f"\n| Acct No. | Balance |\n| 1 | 0 |\n| 2 | 0 |\n\n", result)

    def test_render_by_id(self):
        user = Mock(spec=User)
        user.accounts = [Account(1, 100), Account(2, 200)]

        state = {
            'session': user
        }

        renderer = AccountsRenderer()
        result = renderer.render_by_id(state, account_id=2)

        account2 = user.accounts[1]
        self.assertEqual(f"\n| Acct No. | Balance |\n| {account2.id} | {account2.balance} |\n", result)

    def test_render_table(self):
        accounts = [Account(1, 100), Account(2, 200)]

        renderer = AccountsRenderer()
        result = renderer.render_table(accounts)

        self.assertEqual(f"\n| Acct No. | Balance |\n| 1 | 100 |\n| 2 | 200 |\n", result)

    def test_render_table_from_state(self):
        user = Mock(spec=User)
        accounts = [Account(1, 100), Account(2, 200)]
        user.accounts = accounts

        renderer = AccountsRenderer()
        result = renderer.render_table_from_state({'session': user})

        self.assertEqual(f"\n| Acct No. | Balance |\n| 1 | 100 |\n| 2 | 200 |\n", result)

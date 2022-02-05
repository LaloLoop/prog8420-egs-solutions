from unittest import TestCase
from unittest.mock import Mock

from entities import User, Account
from render import Renderer, WelcomeRenderer, MenuRenderer, MainRenderer, AccountCreatedRenderer


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
        state = {'session': None}

        menu_renderer = MenuRenderer()
        result = menu_renderer.render(state)

        self.assertEqual("\nPlease create a user to begin.\n", result)

    def test_render_non_account_menu(self):
        u = User()

        state = {'session': u}

        menu_renderer = MenuRenderer()
        result = menu_renderer.render(state)

        self.assertEqual(
            "Your user is setup and you can now create a Bank account!\n1. Create account\n2. Exit\n",
            result
        )

    def test_render_account_available(self):
        u = Mock(spec=User)
        account = Mock(spec=Account)
        u.accounts = [account]

        state = {'session': u}

        renderer = MenuRenderer()
        result = renderer.render(state)

        self.assertEqual(
            "\nHow may I help you?\n1. Deposit\n2. Withdraw\n3. Transfer\n4. Create account\n5. Exit\nPlease select an "
            "option ",
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


class TestAccountCreatedRenderer(TestCase):
    def test_render(self):
        account = Mock(speck=Account)
        account.id = 1
        account.balance = 0
        user = Mock(spec=User)
        user.accounts = [account]

        state = {
            'session': user,
            'account_created': False
        }

        renderer = AccountCreatedRenderer()
        result = renderer.render(state)

        self.assertEqual("", result)

        state['account_created'] = True

        result = renderer.render(state)

        self.assertEqual(f"Nice, here's your virtual account\n| Acct No. | Balance |\n| {account.id} | "
                         f"{account.balance} |", result)


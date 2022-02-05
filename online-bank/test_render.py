from unittest import TestCase

from entities import User, Account
from render import Renderer, WelcomeRenderer, MenuRenderer, MainRenderer


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

        menu_rendered = MenuRenderer()
        result = menu_rendered.render(state)

        self.assertEqual("Your user is setup and you can now create a Bank account!\n1. Create account\n2. Exit\n", result)


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

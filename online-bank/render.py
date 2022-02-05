import functools


class Renderer:
    def render(self, state):
        return f"\nRender called from root class " \
               f"{self.__class__.__name__}\nState keys: {list(state.keys())}\n"


class WelcomeRenderer(Renderer):
    def render(self, state):
        return "\nWelcome to online banking!\n"


class MenuRenderer(Renderer):
    def render(self, state):
        session = state['session']
        if session is None:
            return "\nPlease create a user to begin.\n"
        elif len(session.accounts) == 0:
            return "Your user is setup and you can now create a Bank account!\n1. Create account\n2. Exit\n"

        return ""


class AccountsRenderer(Renderer):
    def render(self, state):
        super().render(state)


class MainRenderer(Renderer):
    def __init__(self, renderers=None):
        if renderers is None:
            renderers = [WelcomeRenderer(), MenuRenderer()]

        self.renderers = renderers

    def render(self, state):
        return functools.reduce(
            lambda s, r: s + r.render(state),
            self.renderers,
            ""
        )

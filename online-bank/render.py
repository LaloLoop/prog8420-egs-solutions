import functools


class Renderer:
    def render(self, state):
        return f"\nRender called from root class " \
               f"{self.__class__.__name__}\nState keys: {list(state.keys())}\n"


class WelcomeRenderer(Renderer):
    def render(self, state):
        return "\nWelcome to online banking!\n"


class MenuRenderer(Renderer):
    menu_headers = {
        'missing_user_account': "\nPlease create a user to begin.\n",
        'no_accounts': "Your user is setup and you can now create a Bank account!\n",
        'single_account': "\nHow may I help you?\n"
    }

    menu_titles = {
        'exit': 'Exit',
        'prompt_user_info': 'Create my user',
        'create_account': 'Create account',
        'deposit': 'Deposit',
        'withdraw': 'Withdraw',
        'transfer': 'Transfer',
    }

    def render(self, state):
        context = state['context']
        menu = state['menu']
        result = ""

        if context in self.menu_headers:
            result += self.menu_headers[context]

        for i, option in enumerate(menu.keys(), start=1):
            result += f"{i}. {self.menu_titles[option]}\n"

        return result


class AccountsRenderer(Renderer):
    def render(self, state):
        if state['account_created']:
            account = state['session'].accounts[-1]
            return self.render_table([account])

        return ""

    def render_by_id(self, state, account_id):
        found = None
        for account in state['session'].accounts:
            if account.id == account_id:
                found = account
                break

        return self.render_table([found])

    def render_table_from_state(self, state):
        accounts = state['session'].accounts

        return self.render_table(accounts)

    def render_table(self, accounts):
        result = f"\n| Acct No. | Balance |"
        for account in accounts:
            result += f"\n| {account.id} | {account.balance} |"

        return result


class MainRenderer(Renderer):
    def __init__(self, renderers=None):
        if renderers is None:
            renderers = [
                AccountsRenderer(),
                WelcomeRenderer(),
                MenuRenderer(),
            ]

        self.renderers = renderers

    def render(self, state):
        return functools.reduce(
            lambda s, r: s + r.render(state),
            self.renderers,
            ""
        )

import re
from time import sleep

from render import AccountsRenderer
from res_selectors import get_user_account_by_id


class Prompter:
    def prompt(self, state):
        result = input("What's on your mind?")

        return result != ""


class UserInfoPrompter(Prompter):
    def __init__(self, store):
        self.store = store

    def prompt(self, state):

        if 'context' in state and state['context'] != 'prompt_user_info':
            return False

        name = ''
        last_name = ''

        while name == '' or last_name == '':
            if name == '':
                name = input("What's your first name? ")

            if name == '':
                print("You should enter your name, otherwise, how will I know how to call you?")
                continue
            elif not re.match("[a-zA-Z]{4,}", name):
                print("Your name should only contain at least 4 English character letters")
                name = ""
                continue

            last_name = input('And, your last name? ')

            if last_name == '':
                print(f"There's more than one \"{name}\" in this world, please tell us your last name.")

            elif not re.match("[a-zA-Z]{4,}", last_name):
                print("Your Last name should only contain at least 4 English character letters")
                last_name = ""

        self.store.dispatch({
            'type': 'user/create',
            'payload': {
                'name': name,
                'last_name': last_name
            }
        })

        return True


class MenuPrompter(Prompter):
    def __init__(self, store):
        self.store = store

    def prompt(self, state):

        menu = state['menu']
        menu_keys = menu.keys()

        if len(menu_keys) == 0:
            return False

        menu_actions = {}
        for i, key in enumerate(menu_keys, start=1):
            menu_actions[str(i)] = key

        while True:
            value = input("> ")

            if value not in menu_actions:
                print("Sorry, I cannot help you with that at the moment, please choose another option")
                continue

            selection = menu_actions[value]

            if selection == 'exit':
                print("This is an in memory Bank, your data will be lost, are you sure?")
                if input("(y/N)> ") == "y":
                    self.store.dispatch(menu[selection])
                    print("Ok, hope you enjoyed your virtual 💸. Bye! 👋🏼")
                else:
                    self.store.dispatch({'type': 'program/terminate_cancel'})
                    print("Thanks for keeping us in business!")

                break

            elif selection == 'create_account':
                self.store.dispatch(menu[selection])
                print("Creating account...")
                sleep(1)
                break

            else:
                self.store.dispatch(menu[selection])
                break

        return True


class DepositPrompter(Prompter):
    def __init__(self, store, accounts_renderer=AccountsRenderer(), account_selector=get_user_account_by_id):
        self.store = store
        self.accounts_renderer = accounts_renderer
        self.account_selector = account_selector

    def prompt(self, state):
        if state['context'] != 'prompt_deposit_info':
            return False

        account_id = 0
        amount = 0

        input_error = True
        while input_error:
            if account_id == 0:
                print('Which account would you like to deposit to?')
                print(self.accounts_renderer.render_table_from_state(state))

                try:
                    account_id = int(input("> "))

                    account = self.account_selector(state, account_id=account_id)

                    if account is None:
                        print("That account does not exist, please pick a valid one")
                        account_id = 0
                        continue

                except ValueError:
                    print('That\'s not a valid ID, have a look again')
                    input_error = True
                    continue

            print("Great! How much money do you want to deposit?")

            try:
                amount = float(input("> "))

                if amount <= 0:
                    print("The amount has to be greater than 0")
                    amount = 0
                    continue

            except ValueError:
                print("Wait a minute, that does not look like a number.")
                input_error = True
                continue

            input_error = False

        print("Making deposit...")
        self.store.dispatch({
            'type': 'account/deposit',
            'payload': {
                'id': account_id,
                'amount': amount
            }
        })

        sleep(1)

        print("Here's your account detail")
        print(self.accounts_renderer.render_by_id(state, account_id=account_id))

        return True


class WithdrawPrompter(Prompter):
    def __init__(self, store, accounts_renderer=AccountsRenderer(), account_selector=get_user_account_by_id):
        self.store = store
        self.accounts_renderer = accounts_renderer
        self.account_selector = account_selector

    def prompt(self, state):
        if 'context' in state and state['context'] != 'prompt_withdraw_info':
            return False

        account_id = 0
        amount = 0

        input_error = True

        while input_error:
            if account_id == 0:

                print("Which account would you like to withdraw from?")
                print(self.accounts_renderer.render_table_from_state(state))

                try:
                    account_id = int(input("> "))

                    account = self.account_selector(state, account_id=account_id)
                    if account is None:
                        print("That account does not exist, please pick a valid one")
                        account_id = 0
                        continue

                except ValueError:
                    print('That\'s not a numeric ID, have a look again')
                    input_error = True
                    continue

            print("How much money would you like to withdraw?")

            try:

                amount = float(input("> "))

                if amount <= 0:
                    print("Your amount has to be greater than 0")
                    continue

            except ValueError:
                print("Hold your horses, please give a number.")
                input_error = True
                continue

            input_error = False

        print("Getting your money...")
        self.store.dispatch({'type': 'account/withdraw', 'payload': {'id': account_id, 'amount': amount}})

        sleep(1)

        if 'error' not in self.store.state or not self.store.state['error']:
            print(f"You've withdrawn ${amount}")
        else:
            print(f"I could not get your money. {self.store.state['error']}")

        return True


class TransferPrompter(Prompter):
    def __init__(self, store, accounts_renderer=AccountsRenderer(), selector=get_user_account_by_id):
        self.store = store
        self.accounts_renderer = accounts_renderer
        self.account_selector = selector

    def prompt(self, state):
        if state['context'] != 'prompt_transfer_info':
            return False

        input_error = True

        source_acct_id = 0
        amount = 0
        dest_acct_id = 0

        while input_error:
            if source_acct_id == 0:
                print("Please provide the source account")
                print(self.accounts_renderer.render_table_from_state(state))

                try:
                    source_acct_id = int(input("> "))
                    account = self.account_selector(state, source_acct_id)
                    if account is None:
                        print("Sorry, that account does not exist, please choose a valid ID")
                        source_acct_id = 0
                        continue

                except ValueError:
                    print("Please provide a numeric ID")
                    continue

            if amount == 0:
                print("How much money do you want to transfer?")
                try:
                    amount = float(input("> "))

                    if amount < 0:
                        print("I see what you did there. The amount cannot be negative")
                        amount = 0
                        continue
                    elif amount == 0:
                        print("Your amount has to be greater than 0")
                        amount = 0
                        continue

                except ValueError:
                    print("Please provide a numeric amount")
                    continue

            if dest_acct_id == 0:
                print("What\'s the destination account?")
                print(self.accounts_renderer.render_table_from_state(state))
                try:
                    dest_acct_id = int(input("> "))

                    account = self.account_selector(state, dest_acct_id)
                    if account is None:
                        print("Sorry, that account does not exist, please choose a valid ID")
                        dest_acct_id = 0
                        continue

                except ValueError:
                    print("Please provide a numeric ID")
                    continue

            input_error = False

        print("Working on it...")

        self.store.dispatch({
            'type': 'account/transfer',
            'payload': {
                'source_acct_id': source_acct_id,
                'dest_acct_id': dest_acct_id,
                'amount': amount
            }
        })

        sleep(1)

        if 'error' not in self.store.state or not self.store.state['error']:
            print("Done! the money has been transferred")
        else:
            print(f"I could not complete your transfer. {self.store.state['error']}")

        return True


class MainPrompter(Prompter):
    def __init__(self, store, prompters=None):
        if prompters is None:
            prompters = [
                UserInfoPrompter(store),
                DepositPrompter(store),
                WithdrawPrompter(store),
                TransferPrompter(store),
                MenuPrompter(store),
                Prompter()
            ]
        self.prompters = prompters

    def prompt(self, state):
        for prompt in self.prompters:
            if prompt.prompt(state):
                break

        return True

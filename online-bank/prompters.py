from time import sleep


class Prompter:
    def prompt(self, state):
        result = input("What's on your mind?")

        return result != ""


class UserInfoPrompter(Prompter):
    def __init__(self, store):
        self.store = store

    def prompt(self, state):

        if 'session' in state and state['session'] is not None:
            return False

        name = ''
        last_name = ''

        while name == '' or last_name == '':
            if name == '':
                name = input("What's your first name? ")

            if name == '':
                print("You should enter your name, otherwise, how will I know how to call you?")
                continue

            last_name = input('And, your last name? ')

            if last_name == '':
                print(f"There's more than one \"{name}\" in this world, please tell us your last name.")

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

        user = state['session']

        while True:
            value = input("> ")

            if user is not None and len(user.accounts) == 0:
                if value == "2":
                    print("This is an in memory Bank, your data will be lost, are you sure?")
                    if input("(y/N)> ") == "y":
                        self.store.dispatch({'type': 'program/terminate'})
                        print("Ok, hope you enjoyed your virtual 💸. Bye! 👋🏼")
                    break
                elif value == "1":
                    self.store.dispatch({'type': 'account/create'})
                    print("Creating account...")
                    sleep(1)
                    break

            print("Sorry, I cannot help you with that at the moment, please choose another option")

        return True


class MainPrompter(Prompter):
    def __init__(self, store, prompters=None):
        if prompters is None:
            prompters = [UserInfoPrompter(store), MenuPrompter(store), Prompter()]
        self.prompters = prompters

    def prompt(self, state):
        for prompt in self.prompters:
            if prompt.prompt(state):
                break

        return True


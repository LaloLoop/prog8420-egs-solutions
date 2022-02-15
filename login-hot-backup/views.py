class MenuView:

    def __init__(self, controller):
        self._controller = controller

    def display(self, state):
        selection = input("New user?").upper()

        if selection == "Y":
            self._controller.prompt_user_info()
        elif selection == "N":
            self._controller.prompt_login_info()
        elif selection == "EXIT":
            self._controller.exit()


class CreateUserView:

    def __init__(self, controller):
        self._controller = controller

    def display(self, state):
        email = input("email: ")

        password = input("password: ")

        self._controller.create_user(email, password)


class LoginView:
    def __init__(self, controller):
        self._controller = controller
        self._subview = CreateUserView(self)

    def display(self, state):
        self._subview.display(state)

    def create_user(self, email, password):
        user_record = self._controller.login(email, password)

        print(f"{user_record.email} has logged in {user_record.access_count} time(s)")


class MainView:
    def __init__(self, controller):
        self._factory = ViewFactory(controller)

    def display(self, state):
        product_view = self._factory.get_view(state['context'])
        product_view.display(state)


class ViewFactory:
    def __init__(self, controller):
        self._views = {
            'init': MenuView(controller),
            'prompt_user_info': CreateUserView(controller),
            'prompt_login_info': LoginView(controller)
        }

    def get_view(self, context):
        return self._views[context]

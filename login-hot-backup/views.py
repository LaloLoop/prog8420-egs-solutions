import re


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


class CreateValidatedUserView:
    email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    password_regex = r'\b[A-Z0-9]{4,}'

    def __init__(self, controller):
        self._controller = controller
        self.validators = {
            'email': self._validate_non_empty(self._validate_email(self._confirm_input())),
            'password': self._validate_non_empty(self._validate_password(self._confirm_input()))
        }

    def _validate_non_empty(self, next_validator=None):
        def validator(value, input_name):
            if not value:
                print(f"Please provide your {input_name}")
                return False

            elif next_validator:
                return next_validator(value, input_name)

            return True

        return validator

    def _validate_email(self, next_validator=None):
        def validator(value, input_name):
            if not re.fullmatch(self.email_regex, value):
                print("Please input a valid email, e.g. user@domain.com")
                return False
            elif next_validator:
                return next_validator(value, input_name)

            return True

        return validator

    def _validate_password(self, next_validator=None):
        def validator(value, input_name):
            if not re.fullmatch(self.password_regex, value):
                print("Provide a 4 or more uppercase letters password, no special characters are allowed")
                return False

            elif next_validator:
                return next_validator(value, input_name)

            return True

        return validator

    def _confirm_input(self, next_validator=None):
        def validator(value, input_name):

            while True:
                confirmed_input = input(f"Please confirm your {input_name}: ")
                if confirmed_input == value:
                    break

            if next_validator:
                return next_validator(value, input_name)

            return True

        return validator

    def validators_mapping(self):
        return

    def display(self, state):

        email_field = "email"
        email = ""

        valid_email = False
        password = ""

        while not valid_email:
            email = input(f"{email_field}: ")
            valid_email = self.validators[email_field](email, email_field)

        password_field = "password"
        valid_password = False
        while not valid_password:
            password = input(f"{password_field}: ")
            valid_password = self.validators[password_field](password, password_field)

        self._controller.create_user(email, password)


class LoginValidatedInputView(CreateValidatedUserView):
    def __init__(self, controller):
        super().__init__(controller)
        self.validators = {
            'email': self._validate_non_empty(self._validate_email()),
            'password': self._validate_non_empty(self._validate_password())
        }


class LoginView:
    def __init__(self, controller):
        self._controller = controller
        self._subview = LoginValidatedInputView(self)

    def display(self, state):
        self._subview.display(state)

    def create_user(self, email, password):
        user_record = self._controller.login(email, password)

        if user_record:
            print(f"{user_record.email} has logged in {user_record.access_count} time(s)")
        else:
            print("User does not exist")


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
            'prompt_user_info': CreateValidatedUserView(controller),
            'prompt_login_info': LoginView(controller)
        }

    def get_view(self, context):
        return self._views[context]

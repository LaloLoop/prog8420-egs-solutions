class MenuView:

    def __init__(self, controller):
        self._controller = controller

    def display(self, state):
        selection = input("New user?").upper()

        if selection == "Y":
            self._controller.create_user()
        elif selection == "N":
            self._controller.login()
        elif selection == "EXIT":
            self._controller.exit()

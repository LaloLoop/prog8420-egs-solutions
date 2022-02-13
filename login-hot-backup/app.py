from controller import Controller
from views import MenuView


class App:

    def __init__(self, view=None, controller=Controller()):
        if view is None:
            view = MenuView(controller)

        self._view = view
        self._controller = controller

    def run(self):
        while self._controller.is_running():
            state = self._controller.get_state()
            self._view.display(state)

        return 0

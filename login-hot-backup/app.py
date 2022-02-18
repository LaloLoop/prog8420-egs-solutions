from controller import Controller
from views import MainView


class App:

    def __init__(self):
        self._controller = Controller()
        self._view = MainView(self._controller)

    def run(self):
        self._controller.init_db()

        while self._controller.is_running():
            state = self._controller.get_state()
            self._view.display(state)

        return 0

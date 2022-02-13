class Controller:

    def __init__(self):
        self._running = True
        self._state = {}

    def is_running(self):
        return self._running

    def exit(self):
        self._running = False

    def get_state(self):
        return self._state

    def create_user(self):
        pass

    def login(self):
        pass

class Controller:

    def __init__(self):
        self._running = True
        self._state = {
            'context': 'init'
        }

    def is_running(self):
        return self._running

    def exit(self):
        self._running = False

    def get_state(self):
        return self._state

    def prompt_user_info(self):
        self._state = {
            **self._state,
            'context': 'prompt_user_info'
        }

    def create_user(self, email, password):
        pass

    def login(self):
        pass

from cipher import PasswordCipher
from repository import DBRepository


class Controller:

    def __init__(self):
        self._running = True
        self._state = {
            'context': 'init'
        }
        self._cipher = PasswordCipher()
        self._repo = DBRepository()

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
        ciphered_password = self._cipher.cipher(password)
        created = self._repo.create_user(email, ciphered_password)

        self._state = {**self._state, 'context': 'init'}

        return created

    def login(self):
        pass

    def init_db(self):
        self._repo.create_tb_user()

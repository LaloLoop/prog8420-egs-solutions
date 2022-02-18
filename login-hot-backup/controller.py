from cipher import XLSXCipher
from exporter import DBExporter
from repository import DBRepository


class Controller:

    def __init__(self):
        self._running = True
        self._state = {
            'context': 'init'
        }
        self._cipher = XLSXCipher()
        self._repo = DBRepository()
        self._exporter = DBExporter()

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

    def prompt_login_info(self):
        self._state = {
            **self._state,
            'context': 'prompt_login_info'
        }

    def create_user(self, email, password):
        ciphered_password = self._cipher.cipher(password)
        created = self._repo.create_user(email, ciphered_password)

        if created:
            self._exporter.export()

        self._state = {**self._state, 'context': 'init'}

        return created

    def login(self, email, password):
        self._state = {**self._state, 'context': 'init'}

        ciphered_password = self._cipher.cipher(password)

        updated = self._repo.update_access_count(email, ciphered_password)

        if updated:
            self._exporter.export()
            return self._repo.find_user_with_credentials(email, ciphered_password)

        return None

    def init_db(self):
        self._repo.create_tb_user()


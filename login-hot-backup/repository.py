import sqlite3


class DBRepository:

    def __init__(self, db_path="user.db"):
        self._db_path = db_path

    def create_tb_user(self):
        con = sqlite3.connect(self._db_path)
        cur = con.cursor()

        cur.execute('''CREATE TABLE IF NOT EXISTS TB_USER (
                       USER_ID INTEGER PRIMARY KEY,
                       LOGIN TEXT,
                       "CRYPTOGRAPHIC PASSWORD" TEXT,
                       ACCESS_COUNT INTEGER DEFAULT 0 NOT NULL
                       )''')

        con.commit()

        con.close()

        return True

    def create_user(self, email, password):
        con = sqlite3.connect(self._db_path)
        cur = con.cursor()

        cur.execute('INSERT INTO TB_USER("LOGIN", "CRYPTOGRAPHIC PASSWORD") VALUES (?, ?)', (email, password, ))

        con.commit()
        con.close()

        return True

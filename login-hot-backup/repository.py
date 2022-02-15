import sqlite3


class UserRecord:
    def __init__(self, email, access_count):
        self.email = email
        self.access_count = access_count


class DBRepository:

    def __init__(self, db_path="user.db"):
        self._db_path = db_path

    def _get_connection(self):
        return sqlite3.connect(self._db_path)

    def create_tb_user(self):
        con = self._get_connection()
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
        con = self._get_connection()
        cur = con.cursor()

        cur.execute('INSERT INTO TB_USER("LOGIN", "CRYPTOGRAPHIC PASSWORD") VALUES (?, ?)', (email, password,))

        inserted = cur.rowcount

        con.commit()
        con.close()

        return inserted

    def find_user_with_credentials(self, email, password):
        con = self._get_connection()
        con.row_factory = sqlite3.Row
        cur = con.cursor()

        cur.execute(
            'SELECT LOGIN, ACCESS_COUNT FROM TB_USER WHERE LOGIN=? AND "CRYPTOGRAPHIC PASSWORD"=?',
            (email, password)
        )

        r = cur.fetchone()

        return UserRecord(r['LOGIN'], r["ACCESS_COUNT"])

    def update_access_count(self, email, password):
        con = self._get_connection()

        cur = con.cursor()

        cur.execute(
            '''UPDATE TB_USER SET ACCESS_COUNT = ACCESS_COUNT + 1
               WHERE LOGIN = ? AND "CRYPTOGRAPHIC PASSWORD" = ?''',
            (email, password)
        )

        con.commit()

        updated = cur.rowcount > 0

        con.close()

        return updated

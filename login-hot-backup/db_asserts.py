import os
import sqlite3


def _get_users_cursor(db_path, con=None):
    if con is None:
        con = sqlite3.connect(db_path)

    con.row_factory = sqlite3.Row
    cur = con.cursor()

    return cur.execute('SELECT USER_ID, LOGIN, "CRYPTOGRAPHIC PASSWORD", ACCESS_COUNT FROM TB_USER ORDER BY USER_ID')


def _assert_row(row, id, email, ciphered_pass, access_count):
    assert id == row['USER_ID']
    assert email == row['LOGIN']
    assert ciphered_pass == row["CRYPTOGRAPHIC PASSWORD"]
    assert access_count == row['ACCESS_COUNT']


def assert_user_record(email, ciphered_pass, id=1, access_count=0, db_path='./user.db', con=None):
    cur = _get_users_cursor(db_path, con)

    r = cur.fetchone()

    _assert_row(r, id, email, ciphered_pass, access_count)


def assert_db_backup(db_path='./user.db', file_path='./userdb-backup.csv'):
    assert os.path.exists(file_path)

    cur = _get_users_cursor(db_path)

    with open(file_path, "r") as backup_file:
        # Assuming there's no header in the file

        for line in backup_file:
            row = cur.fetchone()

            assert row is not None

            cols = line.replace("\n", "").split(",")
            for i, col in enumerate(cols):
                assert str(row[i]) == col


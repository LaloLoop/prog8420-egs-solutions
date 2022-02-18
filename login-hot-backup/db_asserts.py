import os
import sqlite3

TEST_FILES_FOLDER = "./"
TEST_DB = "user.db"
BACKUP_FILE = "userdb-backup.csv"


def _test_file_path(fpath):
    return "/".join([TEST_FILES_FOLDER, fpath])


TEST_DB_PATH = _test_file_path(TEST_DB)
TEST_BACKUP_PATH = _test_file_path(BACKUP_FILE)


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


def assert_user_record(email, ciphered_pass, id=1, access_count=0, db_path=TEST_DB_PATH, con=None):
    cur = _get_users_cursor(db_path, con)

    r = cur.fetchone()

    _assert_row(r, id, email, ciphered_pass, access_count)


def assert_empty_db(db_path=TEST_DB_PATH):
    cur = _get_users_cursor(db_path)
    assert cur.fetchone() is None

    cur.close()


def assert_no_backup(file_path=TEST_BACKUP_PATH):
    assert not os.path.exists(file_path)


def assert_db_backup(db_path=TEST_DB_PATH, file_path=TEST_BACKUP_PATH):
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

    cur.close()

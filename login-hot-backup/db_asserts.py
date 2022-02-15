import sqlite3


def assert_user_record(email, ciphered_pass, id=1, access_count=0, db_path='./user.db', con=None):
    if con is None:
        con = sqlite3.connect(db_path)

    con.row_factory = sqlite3.Row
    cur = con.cursor()

    cur.execute('SELECT USER_ID, LOGIN, "CRYPTOGRAPHIC PASSWORD", ACCESS_COUNT FROM TB_USER')

    r = cur.fetchone()

    assert id == r['USER_ID']
    assert email == r['LOGIN']
    assert ciphered_pass == r["CRYPTOGRAPHIC PASSWORD"]
    assert access_count == r['ACCESS_COUNT']

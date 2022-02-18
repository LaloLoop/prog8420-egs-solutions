import random
from string import ascii_letters

import pexpect

email_domains = [
    "hotmail.com", "yahoo.com", "faceboook.com", "gmail.com", "live.com", "icloud.com", "todito.com", "vk.ru",
    "youtube.tv", "conestoga.ca", "gob.mx", "gob.co"
]


def random_email():
    username = "".join([random.choice(ascii_letters) for _ in range(7)]).lower()
    domain = random.choice(email_domains)

    return f"{username}@{domain}"


def random_password():
    return "".join([random.choice(ascii_letters + "0123456789") for _ in range(12)]).upper()


def generate_users(num):
    users = []
    for _ in range(num):
        users.append((random_email(), random_password()))

    return users


if __name__ == "__main__":
    total_users = 100

    users = generate_users(total_users)

    child = pexpect.spawn('python main.py', timeout=3)

    print(f"Inserting: {total_users} users...")

    for i, u in enumerate(users):

        child.sendline("y")
        child.expect("email")
        child.sendline(u[0])
        child.expect("email")
        child.sendline(u[0])
        child.expect("password")
        child.sendline(u[1])
        child.expect("password")
        child.sendline(u[1])

    print(f"Finished: {total_users} users inserted")

    print(f"Doing {total_users} random logins...")
    # Doing random logins
    for i in range(total_users):
        random_user = random.choice(users)

        child.sendline("n")
        child.expect("email")
        child.sendline(random_user[0])
        child.expect("password")
        child.sendline(random_user[1])
        child.expect("has logged in")

    print(f"Finished: {total_users} random logins done")

    child.sendline("exit")
    child.wait()

    assert child.exitstatus == 0

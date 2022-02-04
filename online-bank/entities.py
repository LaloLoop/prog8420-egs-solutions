# Business rules
class Bank:
    accounts_by_user = {}
    users_by_id = {}
    accounts_by_id = {}

    # 1. Create bank accounts
    def create_account(self, user):
        account = Account(account_id=self.__next_id(self.accounts_by_id))

        if user.id not in self.accounts_by_user:
            self.accounts_by_user[user.id] = {}

        self.accounts_by_user[user.id][account.id] = account

        self.accounts_by_id[account.id] = account

        return account

    def create_user(self):
        user = User()

        self.users_by_id[user.id] = user
        return user

    @staticmethod
    def __next_id(table):
        return len(table.keys()) + 1


# 2. Perform account deposits
class Account:
    def __init__(self, account_id=1, balance=0):
        self.balance = balance
        self.id = account_id

    def deposit(self, amount):
        self.balance += amount

    # 3. Perform Account Withdraws
    # Note 2. Balance negative is unacceptable
    def withdraw(self, amount):
        if self.balance - amount >= 0:
            self.balance -= amount
            return amount

        return 0

    # 4. Perform Account(s) transfer
    def transfer(self, destination, amount):
        destination.deposit(self.withdraw(amount))


class User:
    accounts = []

    def __init__(self, user_id=1):
        self.id = user_id

    # Note 3. As a User I can create multiple accounts
    def create_account(self, bank):
        return bank.create_account(self)

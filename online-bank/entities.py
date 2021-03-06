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

    def create_user(self, name='Eduardo', lastname='Gutierrez'):
        user = User(name=name, last_name=lastname)

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
        if amount < 0:
            return 0

        self.balance += amount

        return amount

    # 3. Perform Account Withdraws
    # Note 2. Balance negative is unacceptable
    def withdraw(self, amount):

        if amount > 0 and self.balance - amount >= 0:
            self.balance -= amount
            return amount

        return 0

    # 4. Perform Account(s) transfer
    def transfer(self, destination, amount):
        return destination.deposit(self.withdraw(amount))


class User:

    def __init__(self, user_id=1, name='John', last_name='Doe'):
        self.id = user_id
        self.name = name
        self.last_name = last_name
        self.accounts = []

    # Note 3. As a User I can create multiple accounts
    def create_account(self, bank):
        new_account = bank.create_account(self)
        self.accounts.append(new_account)

        return new_account

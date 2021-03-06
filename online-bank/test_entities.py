from unittest import TestCase
from unittest.mock import Mock
from entities import Bank, Account, User


class TestBank(TestCase):
    def test_create_account(self):
        bank = Bank()
        user = User()

        account = bank.create_account(user)

        self.assertTrue(account.id in bank.accounts_by_user[user.id])
        self.assertEqual(bank.accounts_by_user[user.id][account.id], account)
        self.assertEqual(bank.accounts_by_id[account.id], account)

    def test_create_user(self):
        bank = Bank()

        created_user = bank.create_user()

        self.assertTrue(created_user.id in bank.users_by_id)
        self.assertEqual(bank.users_by_id[created_user.id], created_user)

    def test_create_user_with_fullname(self):
        b = Bank()
        created_user = b.create_user('Samuel', 'Jackson')

        self.assertEqual(created_user.name, 'Samuel')
        self.assertEqual(created_user.last_name, 'Jackson')

    def test_next_id(self):
        bank = Bank()

        table = {}

        next_id = bank._Bank__next_id(table)

        self.assertEqual(next_id, 1)

        table = {1: 'some'}

        next_id = bank._Bank__next_id(table)

        self.assertEqual(next_id, 2)

    def test_create_multiple_accounts(self):
        bank = Bank()
        user = User()

        account1 = bank.create_account(user)
        account2 = bank.create_account(user)

        self.assertNotEqual(account1, account2)
        self.assertIsNot(account1, account2)
        self.assertNotEqual(account1.id, account2.id)


class TestAccount(TestCase):
    def test_deposit(self):
        account = Account()
        deposited = account.deposit(230)

        self.assertEqual(account.balance, 230)
        self.assertEqual(deposited, 230)

    def test_deposit_cannot_be_negative(self):
        account = Account()
        account.balance = 200
        deposited = account.deposit(-200)

        self.assertEqual(account.balance, 200)
        self.assertEqual(deposited, 0)

    def test_deposit_accumulates(self):
        account = Account()

        account.deposit(100)
        account.deposit(300)

        self.assertEqual(account.balance, 400)

    def test_withdraw(self):
        account = Account(balance=100)

        account.withdraw(50)

        self.assertEqual(account.balance, 50)

    def test_withdraw_cannot_be_negative(self):
        account = Account(balance=100)

        withdrawn = account.withdraw(-100)

        self.assertEqual(account.balance, 100)
        self.assertEqual(withdrawn, 0)

    def test_withdraw_cannot_leave_negative_balance(self):
        account = Account(balance=200)

        account.withdraw(300)

        self.assertEqual(account.balance, 200)

    def test_transfer(self):
        acct_origin = Account(balance=200)
        acct_destination = Account(balance=100)

        transferred = acct_origin.transfer(acct_destination, 200)

        self.assertEqual(acct_destination.balance, 300)
        self.assertEqual(acct_origin.balance, 0)
        self.assertEqual(transferred, 200)

    def test_transfer_greater_amount_returns_zero(self):
        acct_origin = Account(balance=0)
        acct_destination = Account(balance=0)

        transferred = acct_origin.transfer(acct_destination, 100)

        self.assertEqual(acct_destination.balance, 0)
        self.assertEqual(acct_origin.balance, 0)
        self.assertEqual(transferred, 0)


class TestUser(TestCase):

    def test_create_multiple_account(self):
        user = User()
        bank = Mock(spec=Bank)

        account1 = Account(account_id=1)
        account2 = Account(account_id=2)

        user_accounts = [account1, account2]
        bank.create_account.side_effect = user_accounts

        account1 = user.create_account(bank)
        account2 = user.create_account(bank)

        self.assertEqual(bank.create_account.call_count, 2)

        self.assertNotEqual(account1, account2)
        self.assertIsNot(account1, account2)
        self.assertNotEqual(account1.id, account2.id)
        self.assertEqual(user_accounts, user.accounts)

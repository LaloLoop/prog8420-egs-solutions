from unittest import TestCase
from unittest.mock import Mock

from entities import User, Account
from res_selectors import get_user_account_by_id


class TestAccountSelector(TestCase):

    def test_get_user_account_by_id(self):
        user = Mock(spec=User)

        account1 = Mock(spec=Account)
        account1.id = 1
        account1.balance = 200

        account2 = Mock(spec=Account)
        account2.id = 2
        account2.balance = 300

        user.accounts = [account1, account2]

        state = {
            'session': user
        }

        account = get_user_account_by_id(state, account_id=2)

        self.assertIs(account, account2)

        account = get_user_account_by_id(state, account_id=3)

        self.assertIsNone(account)
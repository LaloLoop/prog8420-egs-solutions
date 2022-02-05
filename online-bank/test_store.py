from unittest import TestCase
from unittest.mock import Mock

from store import Store
from entities import Bank, User


def reducer(state, action):
    if action['type'] == 'test':
        payload = action['payload']
        return {**state, 'test_prop': f"Hi {payload}!"}

    return state


class TestStore(TestCase):
    def test_init(self):
        s = Store()

        self.assertEqual(s.state, {})

    def test_dispatch(self):
        s = Store(initial_state={}, reducer=reducer)

        s.dispatch({'type': 'test', 'payload': 'Lalo'})

        self.assertEqual({'test_prop': 'Hi Lalo!'}, s.state)


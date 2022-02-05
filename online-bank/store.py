from entities import Bank


class Store:
    def __init__(self, initial_state=None, reducer=lambda s, a: s):
        if initial_state is None:
            initial_state = {}
        self.state = reducer(initial_state, {'type': 'init'})
        self.reducer = reducer

    def dispatch(self, action):
        self.state = self.reducer(self.state, action)

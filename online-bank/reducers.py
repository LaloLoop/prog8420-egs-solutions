import functools

from entities import Bank


def main_reducer(state, action):
    return functools.reduce(
        lambda st, red_key: STATE_MAPPING[red_key](st, action),
        STATE_MAPPING.keys(),
        state
    )


def user_reducer(state, action):
    act_type = action['type']

    if act_type == 'init':
        return {**state, 'session': None}
    elif act_type == 'user/create':
        payload = action['payload']
        name = payload['name']
        last_name = payload['last_name']

        bank = state['bank']

        return {
            **state,
            'session': bank.create_user(name, last_name)
        }

    return state


def bank_reducer(state, action):
    act_type = action['type']

    if act_type == 'init':
        return {**state, 'bank': Bank()}
    elif act_type == 'account/create':
        state['session'].create_account(state['bank'])
        return {**state, 'account_created': True}

    return state


def exit_reducer(state, action):
    act_type = action['type']

    if act_type == 'init':
        return {**state, 'exit': False}
    elif act_type == 'program/terminate':
        return {**state, 'exit': True}

    return state


def account_created(state, action):
    act_type = action['type']

    if act_type == 'account/create':
        return state

    return {**state, 'account_created': False}


STATE_MAPPING = {
    'bank': bank_reducer,
    'session': user_reducer,
    'exit': exit_reducer,
    'account_created': account_created
}

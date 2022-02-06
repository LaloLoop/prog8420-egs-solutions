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


def __find_account(state, action):
    account_id = action['payload']['id']
    account_found = None
    for account in state['session'].accounts:
        if account.id == account_id:
            account_found = account
            break
    return account_found


def bank_reducer(state, action):
    act_type = action['type']

    if act_type == 'init':
        return {**state, 'bank': Bank()}

    elif act_type == 'account/create':
        state['session'].create_account(state['bank'])
        return {**state, 'account_created': True}

    elif act_type == 'account/deposit':
        amount = action['payload']['amount']
        account_found = __find_account(state, action)
        if account_found is not None:
            account_found.deposit(amount)

    elif act_type == 'account/withdraw':
        amount = action['payload']['amount']
        account_found = __find_account(state, action)

        if account_found is not None:
            balance = account_found.balance
            if balance == 0:
                return {**state, 'error': f"Not enough funds to withdraw ${amount}"}
            elif 0 < balance < amount:
                return {**state, 'error': f"Uh oh, you can withdraw at most ${balance}"}
            else:
                account_found.withdraw(amount)

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


def menu_reducer(state, action):
    act_type = action['type']

    if act_type == 'init':
        return {
            **state,
            'context': 'missing_user_account',
            'menu': {
                'prompt_user_info': {
                    'type': 'user/prompt_info'
                },
                'exit': {
                    'type': 'program/terminate'
                }
            }
        }
    elif act_type == 'user/prompt_info':
        return {
            **state,
            'context': 'prompt_user_info',
            'menu': {}
        }

    elif act_type == 'account/prompt_deposit_info':
        return {
            **state,
            'context': 'prompt_deposit_info',
            'menu': {}
        }

    elif act_type == 'account/prompt_withdraw_info':
        return {
            **state,
            'context': 'prompt_withdraw_info',
            'menu': {}
        }

    elif act_type == 'user/create':
        return {
            **state,
            'context': 'no_accounts',
            'menu': {
                'create_account': {
                    'type': 'account/create'
                },
                'exit': {
                    'type': 'program/terminate'
                }
            }
        }

    elif act_type in ['account/create', 'account/deposit']:
        return {
            **state,
            'context': 'single_account',
            'menu': {
                'deposit': {
                    'type': 'account/prompt_deposit_info'
                },
                'withdraw': {
                    'type': 'account/prompt_withdraw_info'
                },
                'create_account': {
                    'type': 'account/create'
                },
                'exit': {
                    'type': 'program/terminate'
                }
            }
        }

    return state


STATE_MAPPING = {
    'bank': bank_reducer,
    'session': user_reducer,
    'exit': exit_reducer,
    'account_created': account_created,
    'menu': menu_reducer
}

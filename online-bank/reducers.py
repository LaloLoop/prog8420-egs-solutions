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


def __find_account(state, account_id):
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
        account_found = __find_account(state, action['payload']['id'])
        if account_found is not None:
            account_found.deposit(amount)

    elif act_type == 'account/withdraw':
        amount = action['payload']['amount']
        account_found = __find_account(state, action['payload']['id'])

        if account_found is not None:
            balance = account_found.balance
            if balance == 0:
                return {**state, 'error': f"Not enough funds to withdraw ${amount}"}
            elif 0 < balance < amount:
                return {**state, 'error': f"Uh oh, you can withdraw at most ${balance}"}
            else:
                account_found.withdraw(amount)
                return {**state, 'error': ''}

    elif act_type == 'account/transfer':
        payload = action['payload']
        source_acct_id = payload['source_acct_id']
        dest_acct_id = payload['dest_acct_id']
        amount = payload['amount']

        source_found = __find_account(state, source_acct_id)
        dest_found = __find_account(state, dest_acct_id)

        if source_found is not None and dest_found is not None:
            transferred = source_found.transfer(dest_found, amount)

            if transferred == 0:
                return {**state, 'error': 'Could not perform transfer, insufficient funds'}

            return {**state, 'error': ''}
        elif source_found is None:
            return {**state, 'error': f'Could not find source account with id: {source_acct_id}'}
        elif dest_found is None:
            return {**state, 'error': f'Could not find destination account with id: {dest_acct_id}'}

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


def error_reducer(state, action):
    act_type = action['type']

    if act_type == 'account/withdraw':
        return state

    return {**state, 'error': ''}


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

    elif act_type in ['account/create', 'account/deposit', 'account/withdraw']:
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
    'menu': menu_reducer,
    'error': error_reducer,
}

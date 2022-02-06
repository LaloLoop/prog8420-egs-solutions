def get_user_account_by_id(state, account_id):
    for account in state['session'].accounts:
        if account.id == account_id:
            return account

    return None

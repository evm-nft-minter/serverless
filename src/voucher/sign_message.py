from eth_account import Account


def sign_message(private_key, msg):
    account = Account.privateKeyToAccount(private_key)
    signed_msg = Account.sign_message(msg, account.key)

    return signed_msg.signature.hex()

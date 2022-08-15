import json
import os
from arweave import Wallet, Transaction

ARWEAVE_JWK_KEY = json.loads(os.environ.get("ARWEAVE_JWK_KEY"))


def upload(data, content_type):
    wallet = Wallet.from_data(ARWEAVE_JWK_KEY)

    tx = Transaction(wallet, data=bytes(data))
    tx.add_tag("Content-Type", content_type)
    tx.sign()
    tx.send()

    return tx

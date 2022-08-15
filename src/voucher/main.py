import os
import time
from math import floor
from src.common.Response import Response
from src.common.to_wei import to_wei
from src.common.get_token_price import get_token_price
from src.voucher.sign_message import sign_message
from src.voucher.Voucher import Voucher
from src.common.network_enum import NetworkEnum
from src.common.netwrok_to_chain_id import NETWORK_TO_CHAIN_ID
from src.common.network_to_contract import NETWORK_TO_CONTRACT
from src.common.network_to_currency import NETWORK_TO_CURRENCY

VOUCHER_SIGNER_PRIVATE_KEY = os.environ.get("VOUCHER_SIGNER_PRIVATE_KEY")
MAKER_FEE_USD = int(os.environ.get("MAKER_FEE_USD"))


def main(event, context):
    network = event["pathParameters"]["network"]

    if network not in list(NetworkEnum):
        return Response(404, msg="Network not supported")

    chainId = NETWORK_TO_CHAIN_ID[network]
    currency = NETWORK_TO_CURRENCY[network]
    contract = NETWORK_TO_CONTRACT[network]

    currency_price_usd, = get_token_price(currency)
    fee_wei = to_wei(MAKER_FEE_USD / currency_price_usd)
    timestamp = floor(time.time())

    voucher = Voucher(
        _chainId_=chainId,
        _verifyingContract_=contract,
        fee=fee_wei,
        timestamp=timestamp,
    )

    signature = sign_message(VOUCHER_SIGNER_PRIVATE_KEY, voucher.signable_message)

    body = {
        "fee": fee_wei,
        "timestamp": timestamp,
        "signature": signature,
    }

    return Response(200, body)

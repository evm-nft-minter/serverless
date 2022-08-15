from functools import reduce
from src.common.get_token_price import get_token_price
from src.common.network_enum import NetworkEnum
from src.common.network_to_currency import NETWORK_TO_CURRENCY
from src.upload.arweave.get_upload_price import get_upload_price
from src.upload.arweave.winston_to_ar import winston_to_ar


def calc_network_upload_price(network, data_sizes):
    winston_upload_price = reduce(
        lambda acc, s: acc + int(get_upload_price(s)),
        data_sizes,
        0,
    )

    ar_upload_price = winston_to_ar(winston_upload_price)

    ar_price_usd, network_currency_price_usd = get_token_price(
        NETWORK_TO_CURRENCY[NetworkEnum.ARWEAVE],
        NETWORK_TO_CURRENCY[network],
    )

    network_upload_price = ar_price_usd / network_currency_price_usd * ar_upload_price

    return network_upload_price

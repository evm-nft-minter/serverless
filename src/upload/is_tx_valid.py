import os
import time
from web3 import Web3
from web3.middleware import geth_poa_middleware
from src.common.to_wei import to_wei
from src.upload.calc_network_upload_price import calc_network_upload_price
from src.common.network_to_rpc import NETWORK_TO_RPC

UPLOAD_FEE_RECEIVER = os.environ.get("UPLOAD_FEE_RECEIVER")
TX_EXPIRATION_TIME = 1800000000000000


def is_tx_valid(network, txHash, data, metadata):
    web3 = Web3(Web3.HTTPProvider(NETWORK_TO_RPC[network]))

    tx = web3.eth.get_transaction(txHash)

    validators = [
        is_receiver_valid,
        is_tx_time_valid,
        is_tx_value_valid,
    ]

    for fun in validators:
        if not fun(network=network, tx=tx, data=data, metadata=metadata):
            return False

    return True


def is_receiver_valid(**kwargs):
    return kwargs["tx"].to.lower() == UPLOAD_FEE_RECEIVER.lower()


def is_tx_time_valid(**kwargs):
    network = kwargs["network"]
    tx = kwargs["tx"]
    timestamp = time.time()

    web3 = Web3(Web3.HTTPProvider(NETWORK_TO_RPC[network]))
    web3.middleware_onion.inject(geth_poa_middleware, layer=0)

    block = web3.eth.get_block(tx.blockNumber)

    return timestamp - block.timestamp <= TX_EXPIRATION_TIME


def is_tx_value_valid(**kwargs):
    network = kwargs["network"]
    tx = kwargs["tx"]
    data = kwargs["data"]
    metadata = kwargs["metadata"]

    data_sizes = [len(data), len(metadata)]

    network_price = calc_network_upload_price(network, data_sizes)
    network_price_wei = to_wei(network_price)

    return tx.value >= network_price_wei

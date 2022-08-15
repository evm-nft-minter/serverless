from eip712.messages import EIP712Message

VOUCHER_DOMAIN_NAME = "Making Voucher"
VOUCHER_DOMAIN_VERSION = "1"


class Voucher(EIP712Message):
    _name_: "string" = VOUCHER_DOMAIN_NAME
    _version_: "string" = VOUCHER_DOMAIN_VERSION
    _chainId_: "uint256"
    _verifyingContract_: "address"
    fee: "uint256"
    timestamp: "uint256"

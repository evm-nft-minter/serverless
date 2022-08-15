from math import floor

WEI_DECIMALS = 18


def to_wei(num):
    return floor(num * 10**WEI_DECIMALS)

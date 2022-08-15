from pycoingecko import CoinGeckoAPI

cg = CoinGeckoAPI()

VS_CURRENCIES = "usd"


def get_token_price(*tokens):
    prices = cg.get_price(ids=",".join(tokens), vs_currencies=VS_CURRENCIES)

    return [prices[token][VS_CURRENCIES] for token in tokens]

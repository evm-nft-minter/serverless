import requests
from arweave.arweave_lib import API_URL as ARWEAVE_API_URL


def get_upload_price(data_size):
    url = f"{ARWEAVE_API_URL}/price/{data_size}"

    response = requests.get(url)

    return response.text

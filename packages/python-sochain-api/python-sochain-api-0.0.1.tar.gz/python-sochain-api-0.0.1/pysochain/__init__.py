"""Python API for using chain.so."""
import requests

BASE_URL = 'https://chain.so/api/v2/'

def get_balance(network, address):
    req_url = BASE_URL + 'get_address_balance/' + network + '/' + address
    response = requests.get(req_url).json()
    if response.get('status'):
        if response.get('status') == 'success':
            return response['data']['confirmed_balance']
    return False

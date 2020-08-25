import requests


API_URL = 'https://api.exchangeratesapi.io/latest'


def get_exchange_rates(currency_name='USD'):
    response = requests.get(API_URL + f'?base={currency_name}')
    return response.json()


def get_exchange_rates_for_chosen_currencies(to_convert, convert_to):
    data = get_exchange_rates(to_convert)
    return data['rates'][convert_to]

# example: convert('USD', 'RUB', 100) -> 7479.26
def convert(to_convert, convert_to, amount):
    rate = get_exchange_rates_for_chosen_currencies(to_convert, convert_to)
    return amount * rate


def list_currencies():
    data = get_exchange_rates()
    return [key for key in data['rates']]

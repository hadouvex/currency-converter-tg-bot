import requests
from datetime import datetime
from envparse import env

API_URL = 'https://api.exchangeratesapi.io/latest'

USE_CACHE = None

USE_CACHE = bool(int(env('CONVERT_CURRENCY_USE_CACHE', False)))

CURRENCIES_LIST_CACHED = []
ALL_CURRENCIES_EXCHANGE_RATES_CACHED = {}

CACHE_LAST_UPDATE_TIME = datetime(1, 1, 1, 0, 0)

def cache_currencies_list():
    global CURRENCIES_LIST_CACHED
    CURRENCIES_LIST_CACHED = get_currencies_list()

def get_exchange_rates_for_every_currency():
    data = {}
    for currency in CURRENCIES_LIST_CACHED:
        currency_rates = get_exchange_rates(currency)
        data[currency] = currency_rates
    return data

def cache_all_currencies_exchange_rates():
    global ALL_CURRENCIES_EXCHANGE_RATES_CACHED
    ALL_CURRENCIES_EXCHANGE_RATES_CACHED = get_exchange_rates_for_every_currency()

def get_exchange_rates(currency_name='USD'):
    response = requests.get(API_URL + f'?base={currency_name}')
    return response.json()

def get_exchange_rates_for_chosen_currencies_using_cache(to_convert, convert_to):
    return ALL_CURRENCIES_EXCHANGE_RATES_CACHED[to_convert]['rates'][convert_to]

def get_exchange_rates_for_chosen_currencies(to_convert, convert_to):
    data = get_exchange_rates(to_convert)
    return data['rates'][convert_to]

# example: convert('USD', 'RUB', 100) -> 7479.26
def convert(to_convert, convert_to, amount):
    rate = get_exchange_rates_for_chosen_currencies(to_convert, convert_to)
    return amount * rate

def check_time_and_update_cache(func):
    def wrapper(*args, **kwargs):
        dt_now = datetime.now()
        if dt_now.hour - CACHE_LAST_UPDATE_TIME.hour >= 1:
            update_cache()
            return_value = func(*args, **kwargs)
            return return_value
        else:
            return_value = func(*args, **kwargs)
            return return_value
    return wrapper

@check_time_and_update_cache
def convert_using_cache(to_convert, convert_to, amount):
    rate = get_exchange_rates_for_chosen_currencies_using_cache(to_convert, convert_to)
    return amount * rate

def get_currencies_list():
    data = get_exchange_rates()
    return [key for key in data['rates']]

def get_currencies_list_cached():
    return CURRENCIES_LIST_CACHED

def update_cache():
    global CACHE_LAST_UPDATE_TIME
    cache_currencies_list()
    cache_all_currencies_exchange_rates()

    CACHE_LAST_UPDATE_TIME = datetime.now()


if USE_CACHE:
    update_cache()

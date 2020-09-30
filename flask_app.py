import convert_currency


from flask import Flask
from flask import request
from flask import jsonify


from flask.logging import create_logger
from bot import send_message


app = Flask(__name__)
logger = create_logger(app)


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        process_request(request)
        return '<h2>Bot is currently working...</h2>'       
    return '<h2>Bot is currently working...</h2>'


def process_request(request):
    response = request.get_json()

    try:
        chat_id = response['message']['chat']['id']
    except KeyError:
        return '<h2>Bot is currently working...</h2>'
    
    try:
        text = response['message']['text']
    except KeyError:
        send_message(chat_id, text='Input is incorrect, try using "/help"')
        return '<h2>Bot is currently working...</h2>'
    
    available_currencies_string, available_currencies_list = generate_available_currencies_string_and_list()

    generate_response(text, chat_id, available_currencies_string, available_currencies_list)

def generate_response(text, chat_id, available_currencies_string, available_currencies_list):
    if text == '/start':
        send_message(chat_id, "Type '/help' to see how-to")
    elif text == '/help':
        send_message(chat_id, 'This bot can convert from one currency to another\nType "/convert" to start')
        send_message(chat_id, 'Available currencies:\n\n' + available_currencies_string)
    elif text == '/convert':
        send_message(chat_id, 'Reply using following format:\n"currency1 currency2 amount"')
    else:
        text = text.upper()
        if set(text.split()[0:2]) <= (set(available_currencies_list)):
            text_splitted = text.split()
            try:
                to_convert = text_splitted[0]
                convert_to = text_splitted[1]
                amount = int(text_splitted[2])
            except IndexError:
                send_message(chat_id, text='Input is incorrect, try using "/help"')
                return '<h2>Bot is currently working...</h2>'
            
            if convert_currency.USE_CACHE:
                calculated_value = round(convert_currency.convert_using_cache(to_convert, convert_to, amount), 2)
            else:
                calculated_value = round(convert_currency.convert(to_convert, convert_to, amount), 2)
            send_message(chat_id, text=f'{amount} {to_convert} = {calculated_value} {convert_to}')
        else:
            send_message(chat_id, text='Something is wrong, try using "/help"')

def generate_available_currencies_string_and_list():
    if convert_currency.USE_CACHE:
        available_currencies_list = convert_currency.get_currencies_list_cached()
    else:
        available_currencies_list = convert_currency.get_currencies_list()
    available_currencies_string = ''
    for currency in available_currencies_list:
        available_currencies_string += currency + '\n'
    return available_currencies_string, available_currencies_list
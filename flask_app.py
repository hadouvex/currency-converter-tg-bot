import convert_currency


from flask import Flask
from flask import request
from flask import jsonify
from bot import send_message


app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        response = request.get_json()
        chat_id = response['message']['chat']['id']

        try:
            text = response['message']['text']
        except KeyError:
            send_message(chat_id, text='Input is incorrect, try using "/help"')
            return '<h2>Bot is currently working...</h2>'
        
        available_currencies_list = convert_currency.list_currencies()
        available_currencies_string = ''
        for currency in available_currencies_list:
            available_currencies_string += currency + '\n'
        if text == '/start':
            send_message(chat_id, text="Type '/help' to see how-to")
        elif text == '/help':
            send_message(chat_id, text='This bot can convert from one currency to another\nType "/convert" to start')
            send_message(chat_id, text='Available currencies:\n\n' + available_currencies_string)
        elif text == '/convert':
            send_message(chat_id, 'Reply using following format:\n"currency1 currency2 amount"')
        else:
            text = text.upper()
            if set(text.split()[0:2]) <= (set(available_currencies_list)):
                text_splitted = text.split()

                to_convert = text_splitted[0]
                convert_to = text_splitted[1]
                amount = int(text_splitted[2])
                    
                calculated_value = round(convert_currency.convert(to_convert, convert_to, amount), 2)
                send_message(chat_id, text=f'{amount} {to_convert} = {calculated_value} {convert_to}')
            else:
                send_message(chat_id, text='Something is wrong, try using "/help"')
                # return jsonify(response)

        # return jsonify(response)
    return '<h2>Bot is currently working...</h2>'
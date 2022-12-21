import telebot
from telebot import types
from extensions import APIException, CryptoConverter
from config import TOKEN, keys

conv_markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
button = []
for val in keys.keys():
    button.append(types.KeyboardButton(val.capitalize()))

conv_markup.add(*button)

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    text = 'ЭТОТ БОТ КОНВЕРТИРУЕТ ВАЛЮТУ' \
           '\nЧтобы начать работу введите команду боту в следующем формате:\n<имя валюты, цену которой он хочет узнать> ' \
           '<имя валюты, в которой надо узнать цену первой валюты> ' \
           '<количество первой валюты>' \
           '\nУвидеть список валют можно по команде: /values'
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты: '
    for i in keys.keys():
        text = '\n'.join((text, i, ))
    bot.send_message(message.chat.id, text)\

@bot.message_handler(commands=['convert'])
def values(message: telebot.types.Message):
    text = 'Выберити валюту, из которой конвертировать:'
    bot.send_message(message.chat.id, text, reply_markup=conv_markup)
    bot.register_next_step_handler(message, quote_handler)

def quote_handler(message: telebot.types.Message):
    quote = message.text.strip()
    text = 'Выберити валюту, в которую конвертировать:'
    bot.send_message(message.chat.id, text, reply_markup=conv_markup)
    bot.register_next_step_handler(message, base_handler, quote)

def base_handler(message: telebot.types.Message, quote):
    base = message.text.strip()
    text = 'Выберити количество конвертируемой валюты:'
    bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(message, amount_handler, quote, base)

def amount_handler(message: telebot.types.Message, quote, base):
    amount = message.text.strip()
    try:
        total_base = CryptoConverter.get_price(quote.lower(), base.lower(), amount)
    except APIException as e:
        bot.send_message(message.chat.id, f'Ошибка конвертации\n{e}')
    else:
        text = f'Цена {amount} {keys[quote.lower()]} в {keys[base.lower()]} - {float(amount.replace(",", ".")) * total_base}'
        bot.send_message(message.chat.id, text)




bot.polling(non_stop=True)
input('enter')

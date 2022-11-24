import telebot
import traceback

from config import keys, TOKEN

from extensions import APIException, Convert




bot = telebot.TeleBot(TOKEN)


@bot.message_handler(comands=['start','help'])
def help(message: telebot.types.Message):
    text = 'привет'
    bot.send_message(message.chat.id, text)


@bot.message_handler(comands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступны валюты:'
    for i in keys.keys():
       text = '\n'.join((text, i))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    values = message.text.split()
    try:
        if len(values) != 3:
            raise APIException('Неверное количество параметров!')

        answer = Convert.get_price(values)
    except APIException as e:
        bot.reply_to(message, f"Ошибка в команде:\n{e}")

    except Exception as e:
        traceback.print_tb(e.__traceback__)
        bot.reply_to(message, f"Неизвестная ошибка:\n{e}")

    else:
        bot.reply_to(message, answer)




bot.polling()
import telebot
from telebot import types

import re

from Database import Database



bot = telebot.TeleBot(token='1866964447:AAFcnVgIaD_EUhltwqY6uz99qv59yf7bJTw')

markup_with_help = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
help_command = types.KeyboardButton("/help")
markup_with_help.add(help_command)


@bot.message_handler(commands=['start'])
def start_message(msg):
    db = Database()
    db.add_user(user_id=msg.from_user.id)
    bot.send_message(msg.chat.id, f"Здравствуй, <em>{msg.from_user.first_name}</em>\n/help", parse_mode='html',
                     reply_markup=markup_with_help)

@bot.message_handler(commands=['help'])
def help_send(msg):
    bot.send_message(msg.chat.id,
"""/month - Показать расходы за месяц
/day - показать расходы за день
/help - помощь""")

@bot.message_handler(commands=['months', 'month'])
def months_send(msg):
    db = Database()
    us = db.get_data(user_id=msg.from_user.id)
    bot.send_message(msg.chat.id, f"Потраченные за месяц деньги: {us.month_spending}")

@bot.message_handler(content_types=['text'])
def text_handler(msg):
    db = Database()
    us = db.get_data(user_id=msg.from_user.id)
    if re.match(r'\d+\s\w+', msg.text):
        money = int(msg.text.split()[0])
        wtf = msg.text.split()[1]
        us.spend_money(money, wtf)
        db.update_data(msg.from_user.id, us)
    else:
        bot.reply_to(msg, "Я не понимаю")





if __name__ == '__main__':
    bot.infinity_polling()

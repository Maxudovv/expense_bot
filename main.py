import telebot
from telebot import types

import re

from Database import Database



bot = telebot.TeleBot(token='1866964447:AAGJbIOyXboreVZmkP0uYkWaS1FidUelKo0')

markup_with_help = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
help_command = types.KeyboardButton("/help")
markup_with_help.add(help_command)

def dick(dic: dict):
    result = ""
    for k,v in dic.items():
        result += f'   {k} : {v}\n'
    return result

@bot.message_handler(commands=['start'])
def start_message(msg):
    db = Database()
    db.add_user(user_id=msg.from_user.id)
    bot.send_message(msg.chat.id, f"Здравствуй, <em>{msg.from_user.first_name}</em>\n/help", parse_mode='html',
                     reply_markup=markup_with_help)

@bot.message_handler(commands=['help'])
def help_send(msg):
    bot.send_message(msg.chat.id,
"""Для добавления расхода пишите <b>1000 Такси</b>
Для удаления расхода пишите <b>del 1000 Такси</b>
/month - Показать расходы за месяц
/day - показать расходы за день
/help - помощь""",
                     parse_mode='html')

@bot.message_handler(commands=['day'])
def day_send(msg):
    db = Database()
    us = db.get_data(user_id=msg.from_user.id)
    result = dick(us.day_logs) + f'\n   <b>Сумма</b>: {us.day_spending}'
    bot.send_message(msg.chat.id,
                     f"""Потраченные за день деньги:      
{result}""",
                     parse_mode='html')

@bot.message_handler(commands=['months', 'month'])
def months_send(msg):
    db = Database()
    us = db.get_data(user_id=msg.from_user.id)
    result = dick(us.logs) + f'\n   <b>Сумма</b>: {us.month_spending}' # Делаем из словаря приемлимый вид
    bot.send_message(msg.chat.id,
                     f"""Потраченные за месяц деньги:      
{result}""",
                     parse_mode='html')

@bot.message_handler(content_types=['text'])
def text_handler(msg):
    db = Database()
    us = db.get_data(user_id=msg.from_user.id)
    if re.match(r'\d+\s\w+\s*\w*', msg.text): # Вытаскиваем только сообщения формата: 100 Такси
        money = int(msg.text.split()[0])
        wtf = msg.text.replace(str(money),''.title()).strip()
        us.spend_money(money, wtf)
        db.update_data(msg.from_user.id, us)
        bot.send_message(
            msg.chat.id, "Успешно добавлено\n"
        )
    elif re.match(r'del\s\d*\s*\w+\s*\w*', msg.text): # Вытаскиваем только сообщения формата: del 100 Такси
        msg.text = msg.text.replace('del ', '')
        print(msg.text)
        if len(msg.text.split()) >= 1:
            print('1')
            print(us.logs)
            if re.match(r'\w+\s*\w*', msg.text):
                wtf = msg.text.strip().title()
                print('2')
                if wtf in us.logs:
                    print('3')
                    us.month_spending -= us.logs[wtf]
                    del us.logs[wtf]
                    del us.day_logs[wtf]
                    db.update_data(msg.from_user.id, us)
                    bot.send_message(msg.chat.id, "Успешно удалено")
                else:
                    pass
            elif re.match(r'\d+\s\w+', msg.text):
                wtf = msg.text.split()[1].title()
                value = int(msg.text.split()[0])
                us.logs.update({wtf : us.logs[wtf] - value})
                db.update_data(msg.from_user.id, us)
                bot.send_message(msg.chat.id, "Успешно удалено")
    else:
        bot.reply_to(msg, f"Я не понимаю")





if __name__ == '__main__':
    bot.infinity_polling()

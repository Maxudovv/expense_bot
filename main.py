import telebot
import time
import schedule
from telebot import types


class User:
    def __init__(self, reg_time):
        schedule.every().day.do(self.new_day)
        schedule.every().week.do(self.new_week)
        self.register_time = reg_time
        self.month_salary = 0
        self.month_spending = 0
        self.day_salary = 0
        self.day_spending = 0
        self.logs = {}
        self.weeks = 0

    def new_week(self):
        self.weeks += 1
        if self.weeks % 4 == 0:
            self.new_month()

    def new_day(self):
        self.day_salary = 0
        self.day_spending = 0

    def new_month(self):
        self.month_salary = 0
        self.month_spending = 0

    def add_money(self, value: int):
        self.day_salary += value
        self.month_salary += value

    def spend_money(self, value: int, for_what: str):
        self.day_salary -= value
        self.month_salary -= value
        self.day_spending += value
        self.month_spending += value
        res = self.logs.setdefault(for_what, 0)
        self.logs.update({for_what: res + value})


bot = telebot.TeleBot(token='1866964447:AAFcnVgIaD_EUhltwqY6uz99qv59yf7bJTw')

markup_with_help = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
help_command = types.KeyboardButton("/help")
markup_with_help.add(help_command)


@bot.message_handler(commands=['start'])
def send_welcome(msg):
    bot.send_message(msg.chat.id, f"Здравствуй, <em>{msg.from_user.first_name}</em>\n/help", parse_mode='html',
                     reply_markup=markup_with_help)


@bot.message_handler(commands=['help'])
def help_send(msg):
    bot.send_message(msg.chat.id,
                     """/month - Показать расходы за месяц
	/day - показать расходы за день
	/help - помощь""")


if __name__ == '__main__':
    while True:
        bot.polling()


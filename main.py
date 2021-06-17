import telebot
from telebot import types

bot = telebot.TeleBot(token='1866964447:AAFcnVgIaD_EUhltwqY6uz99qv59yf7bJTw')

markup_with_help = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
help_command = types.KeyboardButton("/help")
markup_with_help.add(help_command)

@bot.message_handler(commands=['start'])
def send_welcome(msg):
	bot.send_message(msg.chat.id, f"Здравствуй, <em>{msg.from_user.first_name}</em>\n/help", parse_mode='html', reply_markup=markup_with_help)

@bot.message_handler(commands=['help'])
def help_send(msg):
	bot.send_message(msg.chat.id, 
	"""/month - Показать расходы за месяц
	/day - показать расходы за день
	/help - помощь"""
		)


if __name__ == '__main__':
	bot.infinity_polling()



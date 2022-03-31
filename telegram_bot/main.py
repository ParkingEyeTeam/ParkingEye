import telebot;
from telebot import types

bot = telebot.TeleBot('********');

# @bot.message_handler(commands=['start'])
# def start_message(message):
#     bot.send_message(message.chat.id,'Привет')
msg="Здраствуйте!!!\n" \
    "Добро пожаловать в систему поиска ближайших свободных парковочных мест ParkingEye"


@bot.message_handler(commands=['start'])
def button_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True,selective=False)
    item1 = types.KeyboardButton("Маршрут",request_location=True)
    item2 = types.KeyboardButton("Следующая")
    item3 = types.KeyboardButton("Предыдущая")
    item4 = types.KeyboardButton("Обновить")
    item5 = types.KeyboardButton("Справка")
    markup.add(item1)
    markup.row(item2, item3)
    markup.row(item4)
    markup.add(item5)
    bot.send_message(message.chat.id,msg,reply_markup=markup)

@bot.message_handler(content_types=['text','location'])
def message_reply(message):
    if message.text=="Маршрут":
        bot.send_photo(message.chat.id,)
    if message.text=="Следующая":
        bot.send_message(message.chat.id,"Следующая")
    if message.text=="Предыдущая":
        bot.send_message(message.chat.id,"Предыдущая")
    if message.text=="Обновить":
        bot.send_message(message.chat.id,"Обновить")
    if message.text=="Справка":
        bot.send_message(message.chat.id,"Справка")

bot.infinity_polling()

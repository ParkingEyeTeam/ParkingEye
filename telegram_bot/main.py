import requests
import telebot
import json
from telebot import types
import os
# from dotenv import load_dotenv

# load_dotenv()

bot = telebot.TeleBot('5093740119:AAFwhqB_TpBJNM0dE30KZI7Z4a22PREBESY')


global cam_id


# @bot.message_handler(commands=['start'])
# def start_message(message):
#     bot.send_message(message.chat.id,'Привет')
hello_msg = "Чтобы узнать как пользоваться системой нажмите кнопку 'Справка'"
help_msg = "Чтобы начать пользоваться чат ботом, отправьте геопозицию места назначения" \
           " с помощью кнопки 'Отправить геопозицию' или встроенной функцией Telegram. " \
           "В результате будет подобрана ближайшая к этой геопозиции парковка.*******"
route_msg = "Сформированы ссылки на маршрут в некоторых картографических сервирсах.\n" \
            "Нажмите кнопку, чтобы перейти в нужный сервис."
@bot.message_handler(content_types=['location'])
def get_loc(message):
    loc =message.location
    res = requests.get(url='http://localhost:8000/?longitude='+str(loc.longitude)+'&latitude='+str(loc.latitude))
    print(loc.longitude)
    print(loc.latitude)
    res_d = res.json()
    button_message_2(message, res_d)

@bot.message_handler(commands=['start'])
def button_message_1(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True,selective=False)
    item4 = types.KeyboardButton("Отправить геопозицию", request_location=True)
    item5 = types.KeyboardButton("Справка")
    markup.row(item4)
    markup.add(item5)
    sent = bot.send_message(message.chat.id, hello_msg, reply_markup=markup)
    # bot.register_next_step_handler(sent, get_loc)


#Разделить так как пересекается с маршрутом
# @bot.message_handler(content_types=['location'])
def button_message_2(message, res):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True,selective=False)
    item1 = types.KeyboardButton("Маршрут")
    item2 = types.KeyboardButton("Обновить текущую")
    item3 = types.KeyboardButton("Следующая")
    item4 = types.KeyboardButton("Отправить геопозицию заново", request_location=True)
    item5 = types.KeyboardButton("Справка")
    markup.add(item1)
    markup.row(item2, item3)
    markup.row(item4)
    markup.add(item5)
    r = requests.get(res.get("imgUrl"))
    cap = "Парковка по адресу " + "["+res.get("address")+"]("+res.get("mapServiceLink")+")"+"\n3,2 км\n"+\
          "Свободно \- *"+str(res.get("freeParkingPlaces"))+"*;"+\
          "Занято \- *"+str(res.get("allParkingPlaces")-res.get("freeParkingPlaces"))+"*;"+\
          "Всего \- *"+str(res.get("allParkingPlaces"))+"*;"
    # with open("image.png", 'rb') as f:
    bot.send_photo(message.chat.id, photo=r.content, caption=cap, reply_markup=markup, parse_mode='MarkdownV2')
    #bot.send_message(message.chat.id, msg, reply_markup=markup, disable_web_page_preview=True, parse_mode='MarkdownV2')


@bot.message_handler(content_types=['text'])
def next_message_reply(message):
    if message.text == "Следующая":
        cap="Парковка по адресу "+"[Ленина 22](https://www.youtube.com/) "+"\n3,2 км\n"+"Свободно \- *4*;"+"Занято \- *3*;"+"Всего \- *7*;"
        with open("./src/Logo.png", 'rb') as f:
            bot.send_photo(message.chat.id, photo=f, caption=cap, parse_mode='MarkdownV2')
    if message.text == "Обновить текущую":
        cap = "Парковка по адресу " + "[Ленина 23](https://www.youtube.com/) "+"\n3,2 км\n"+"Свободно \- *4*;"+"Занято \- *3*;"+"Всего \- *7*;"
        with open("./src/Logo.png", 'rb') as f:
            bot.send_photo(message.chat.id, photo=f, caption=cap, parse_mode='MarkdownV2')
    if message.text == "Маршрут":
        # links = get_file()
        inline_markup = types.InlineKeyboardMarkup()
        item1 = types.InlineKeyboardButton(text="2GIS",url="https://2gis.ru/petrozavodsk")
        item2 = types.InlineKeyboardButton(text="Яндекс Карты", url="https://yandex.ru/maps/18/petrozavodsk/?from=tabbar&ll=34.356647%2C61.785675&source=serp_navig&z=14")
        inline_markup.add(item1)
        inline_markup.add(item2)
        bot.send_message(message.chat.id, route_msg, reply_markup=inline_markup)
    if message.text == "Справка":
        bot.send_message(message.chat.id, help_msg)

bot.infinity_polling()

def get_file():
    file = requests.get(url="")
    data = file.read()
    return data

def get_image():
    img = requests.get(url="")
import requests
import telebot
import json
from telebot import types
import os
from dotenv import load_dotenv

load_dotenv()

bot = telebot.TeleBot(os.getenv('TELEGRAM_TOKEN'))

with open("./src/log.json", 'rb') as f:
    data = json.load(f)

hello_msg = "Чтобы узнать как пользоваться системой нажмите кнопку 'Справка'"
help_msg = "Чтобы начать пользоваться чат ботом, отправьте геопозицию места назначения" \
           " с помощью кнопки 'Отправить геопозицию' или встроенной функцией Telegram. " \
           "В результате будет подобрана ближайшая к этой геопозиции парковка."
route_msg = "Сформированы ссылки на маршрут в некоторых картографических сервирсах.\n" \
            "Нажмите кнопку, чтобы перейти в нужный сервис."
no_parking_place_msg ="Извините, но все остальные известные сервису парковки заняты!"

@bot.message_handler(commands=['start'])
def button_message_1(message):
    print('Пользователь '+str(message.chat.id)+' запустил бота')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True,selective=False)
    item4 = types.KeyboardButton("Отправить геопозицию", request_location=True)
    item5 = types.KeyboardButton("Справка")
    markup.row(item4)
    markup.add(item5)
    bot.send_message(message.chat.id, hello_msg, reply_markup=markup)


@bot.message_handler(content_types=['location'])
def get_loc(message):
    print('Пользователь ' + str(message.chat.id) + ' отправил геопозицию')
    loc =message.location
    res = requests.get(url='http://localhost:8000/?longitude='+str(loc.longitude)+'&latitude='+str(loc.latitude))
    data[message.chat.id] = res.json()
    print(data[message.chat.id])
    button_message_2(message)

def button_message_2(message):
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
    r = requests.get(url=data[message.chat.id]["imgUrl"])
    cap = "Парковка по адресу " + "["+data[message.chat.id]["address"]+"]("+data[message.chat.id]["mapServiceLink"]+")"+"\n"+\
          "Свободно \- *"+str(data[message.chat.id]["freeParkingPlaces"])+"*;"+\
          "Занято \- *"+str(data[message.chat.id]["allParkingPlaces"]-data[message.chat.id]["freeParkingPlaces"])+"*;"+\
          "Всего \- *"+str(data[message.chat.id]["allParkingPlaces"])+"*;"
    bot.send_photo(message.chat.id, photo=r.content, caption=cap, reply_markup=markup, parse_mode='MarkdownV2')



@bot.message_handler(content_types=['text'])
def next_message_reply(message):
    if message.text == "Следующая":
        print('Пользователь ' + str(message.chat.id) + ' нажал кнопку "Следующая"')
        res = requests.get(url='http://localhost:8000/?last_camera_id='+str(data[message.chat.id]['cameraId'])+'&longitude='+str(data[message.chat.id]['coords'][0]) + '&latitude='+str(data[message.chat.id]['coords'][1]))
        if res.status_code == 200:
            print('Success!')
            data[message.chat.id] = res.json()
            print(data[message.chat.id])
            r = requests.get(url=data[message.chat.id]["imgUrl"])
            cap = "Парковка по адресу " + "[" + data[message.chat.id]["address"] + "](" + data[message.chat.id]["mapServiceLink"] + ")" + "\n" + \
                  "Свободно \- *" + str(data[message.chat.id]["freeParkingPlaces"]) + "*;" + \
                  "Занято \- *" + str(data[message.chat.id]["allParkingPlaces"] - data[message.chat.id]["freeParkingPlaces"]) + "*;" + \
                  "Всего \- *" + str(data[message.chat.id]["allParkingPlaces"]) + "*;"
            bot.send_photo(message.chat.id, photo=r.content, caption=cap, parse_mode='MarkdownV2')
        elif res.status_code == 404:
            bot.send_message(message.chat.id, no_parking_place_msg)

    if message.text == "Обновить текущую":
        print('Пользователь ' + str(message.chat.id) + ' нажал кнопку "Обновить текущую"')
        if data[message.chat.id]['prevCameraId'] != None:
            res = requests.get(url='http://localhost:8000/?last_camera_id='+str(data[message.chat.id]['prevCameraId'])+'&longitude='+str(data[message.chat.id]['coords'][0]) + '&latitude='+str(data[message.chat.id]['coords'][1]))
        else:
            res = requests.get(url='http://localhost:8000/?longitude='+str(data[message.chat.id]['coords'][0])+'&latitude='+str(data[message.chat.id]['coords'][1]))
        data[message.chat.id] = res.json()
        print(data[message.chat.id])
        r = requests.get(url=data[message.chat.id]["imgUrl"])
        cap = "Парковка по адресу " + "[" + data[message.chat.id]["address"] + "](" + data[message.chat.id]["mapServiceLink"] + ")" + "\n" + \
              "Свободно \- *" + str(data[message.chat.id]["freeParkingPlaces"]) + "*;" + \
              "Занято \- *" + str(data[message.chat.id]["allParkingPlaces"] - data[message.chat.id]["freeParkingPlaces"]) + "*;" + \
              "Всего \- *" + str(data[message.chat.id]["allParkingPlaces"]) + "*;"
        bot.send_photo(message.chat.id, photo=r.content, caption=cap, parse_mode='MarkdownV2')

    if message.text == "Маршрут":
        print('Пользователь ' + str(message.chat.id) + ' нажал кнопку "Маршрут"')
        inline_markup = types.InlineKeyboardMarkup()
        item1 = types.InlineKeyboardButton(text="2GIS",url=data[message.chat.id]["mapServiceLink"])
        inline_markup.add(item1)
        bot.send_message(message.chat.id, route_msg, reply_markup=inline_markup)
    if message.text == "Справка":
        print('Пользователь ' + str(message.chat.id) + ' нажал кнопку "Справка"')
        bot.send_message(message.chat.id, help_msg)

bot.infinity_polling()
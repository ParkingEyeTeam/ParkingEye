import telebot;
import json
import pprint
import numpy as np

bot = telebot.TeleBot('5093740119:AAGiXZ4W5UIxWCA5_PociTPfh7FU7gepCUc');


@bot.message_handler(content_types=['text'])
def get_start_messages(message):
    if message.text == "/start":
        bot.send_message(message.from_user.id,
                         "Добро пожаловать!!!\nОтправь свою геолокацию боту, чтобы получить изображения ближайщих парковочных мест и их адрес")
    elif message.text == "/help":
        bot.send_message(message.from_user.id,
                         "Отправь свою геолокацию боту, чтобы получить изображения ближайщих парковочных мест и их адрес")
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")


@bot.message_handler(content_types=['location'])
def get_location_message(message):
    with open('src/info.json', 'r', encoding='utf-8') as f:
        d = json.load(f)
        x = message.location.latitude
        # print(message.location.latitude)
        y = message.location.longitude
        # print(message.location.longitude)
        point_1 = np.array((x, y))
        min = 1000
        id = 0

        for i in range(12):
            x1 = (d['coord'][i]['position'][0])
            y1 = (d['coord'][i]['position'][1])
            point_2 = ((x1, y1))
            distance = np.linalg.norm(point_1 - point_2)
            # print(distance)
            if distance < min and d['coord'][i]['cnt_empty'] >= 1:
                min = distance
                id = i
        # print(id)
    adress = d['coord'][id]['address']
    img = open('src/' + (str)(d['coord'][id]['id']) + '.png', 'rb')
    bot.send_photo(message.from_user.id, img)
    bot.send_message(message.from_user.id, adress)


bot.polling(none_stop=True, interval=0)
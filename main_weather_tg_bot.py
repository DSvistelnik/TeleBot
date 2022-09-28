import datetime
from config import tg_bot_token, open_weather_token
import requests
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram import Bot, types


bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply(f"Привет{message.from_user.first_name}! Пришли мне название города и я пришлю тебе сводку погоды.")

@dp.message_handler()
async def get_weather(message: types.Message):
    try:
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric"
        )
        data = r.json()
        # pprint(data)

        city = data['name']
        cur_weather = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])

        await message.reply(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
              f"Погода в городе {city}:\nТемпература: {cur_weather}C°\n"
              f"Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст.\nВетер: {wind} м.с.\n"
              f"Восход: {sunrise_timestamp}\nЗакат: {sunset_timestamp}\n"
              f"***Всего хорошего. Обнимаю***")


    except:
        await message.reply("\U00002620  Проверьте название города \U00002620 ")

if __name__ =='__main__':
    executor.start_polling(dp)


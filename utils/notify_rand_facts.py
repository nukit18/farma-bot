import asyncio
import datetime
import os
from random import randint

import aioschedule

from loader import bot
from utils.db_api import quick_cmd_users


async def notify_scheduler_day_rnd():
    aioschedule.every().day.at("09:00").do(notify_scheduler_rnd)  #
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(60)


async def notify_scheduler_rnd():
    times = ["10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00"]
    time = times[randint(0, len(times)-1)]
    counter = 0
    print(time)
    while datetime.datetime.now().time().strftime("%H:%M") != time and counter < 900:
        counter += 1
        await asyncio.sleep(60)
    await notify_rand_facts()


async def notify_rand_facts():
    path = os.path.abspath(os.path.join(os.getcwd(), "")) + "/facts.txt"
    file = open(path, 'r', encoding="utf-8")
    text = file.read().split("•")
    file.close()
    all_users = await quick_cmd_users.select_all_users()
    phrases = ["Наша постоянная рубрика #Фактздоровья", "О! Что-то новенькое! #Фактздоровья",
               "Пора задуматься... #Фактздоровья", "Очередной факт от Анатолия #Фактздоровья"]
    for user in all_users:
        fact_id = randint(0, len(text)-1)
        phrase_id = randint(0, 3)
        try:
            await bot.send_message(user.user_id, phrases[phrase_id])
            await bot.send_message(user.user_id, text[fact_id])
        except:
            continue
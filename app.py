import logging

from aiogram import executor

from loader import dp, db
import middlewares, filters, handlers
from utils.db_api import db_gino
from utils.notification import notification_schedule
from utils.notify_admins import on_startup_notify
from utils.notify_rand_facts import notify_rand_facts, notify_scheduler_day_rnd
from utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher):
    logging.getLogger("gino").setLevel(logging.ERROR)

    # Устанавливаем дефолтные команды
    await set_default_commands(dispatcher)

    # Уведомляет про запуск
    await on_startup_notify(dispatcher)

    print("Подключаем БД")
    await db_gino.on_startup(dispatcher)
    print("Готово")
    print("------------")

    print("Чистим БД")
    await db.gino.drop_all()
    print("Готово")
    print("------------")

    print("Создаем таблицу")
    await db.gino.create_all()
    print("Готово")
    print("------------")

    dp.loop.create_task(notify_scheduler_day_rnd())
    dp.loop.create_task(notification_schedule())


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)

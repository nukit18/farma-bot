import asyncio
import datetime

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import bot, dp
from utils.db_api import quick_cmd_users, quick_cmd_courses, quick_cmd_confirm_courses


async def notification_schedule():
    await asyncio.sleep(0)
    print("Запускаем скрипт отправки уведомлений")
    while True:
        await notify_send()
        await asyncio.sleep(30)
        await notify_late()
        await asyncio.sleep(30)


async def notify_send():
    courses = await quick_cmd_courses.select_all_courses()
    date = datetime.datetime.today()
    for course in courses:
        user = await quick_cmd_users.select_user(course.user_id)
        confirm_implement_keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="Я принял лекарство",
                                         callback_data=f"confirm_implement:{course.id_course}")
                ],
            ]
        )
        if date.date() == course.duration and date.strftime('%H:%M') == course.times[len(course.times) - 1].strftime(
                '%H:%M'):
            await bot.send_message(user.user_id, f"Вам нужно принять {course.name_medicine} в количестве {course.dose}",
                                   reply_markup=confirm_implement_keyboard)
            await quick_cmd_confirm_courses.add_confirm_course(course.id_course, course.user_id, 2, True)# через 10 минут уведомление
            await quick_cmd_courses.delete_course(course.id_course)
            continue
        for time in course.times:
            if date.strftime('%H:%M') == time.strftime('%H:%M'):
                if user.active:
                    await bot.send_message(user.user_id,
                                           f"Вам нужно принять {course.name_medicine} в количестве {course.dose}",
                                           reply_markup=confirm_implement_keyboard)
                    await quick_cmd_confirm_courses.add_confirm_course(course.id_course, course.user_id,
                                                                       2)  # через 10 минут уведомление


async def notify_late():
    courses = await quick_cmd_confirm_courses.select_all_confirm_courses()
    date = datetime.datetime.today()
    for course in courses:
        if date.strftime('%H:%M') == course.time_notify.strftime('%H:%M'):
            await bot.send_message(course.user_id,
                                   "Не забывайте принять лекарство!")
            await quick_cmd_confirm_courses.update_time(course.id_course, 2)# через 10 минут уведомление

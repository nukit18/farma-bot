import os

from aiogram import types

from keyboards.default.enable_bot import enable_keyboard
from keyboards.default.menu_keyboard import menu_keyboard
from loader import dp, bot
from utils.db_api import quick_cmd_users, quick_cmd_courses, quick_cmd_confirm_courses


@dp.message_handler(text="Отключить Анатолия")
async def disable_bot(message: types.Message):
    user = await quick_cmd_users.select_user(int(message.from_user.id))
    if not user or not user.active:
        await message.answer("Для начала нужно зарегистрироваться.\nПропишите /start")
        return
    await quick_cmd_users.off_user(int(message.from_user.id))
    await quick_cmd_courses.delete_all_courses_user(int(message.from_user.id))
    await quick_cmd_confirm_courses.delete_all_courses_user(int(message.from_user.id))
    await message.answer("Очень жаль, ждем тебя в гости!", reply_markup=enable_keyboard)
    path = os.path.abspath(os.path.join(os.getcwd(), "")) + "/photo-data/Еще увидимся.png"
    await bot.send_photo(message.from_user.id, open(path, 'rb'))


@dp.message_handler(text="Включить Анатолия")
async def enable_bot(message: types.Message):
    user = await quick_cmd_users.select_user(int(message.from_user.id))
    if not user:
        await message.answer("Для начала нужно зарегистрироваться.\nПропишите /start")
        return
    if user and user.active:
        await message.answer("Анатолий уже включен", reply_markup=menu_keyboard)
        return
    await quick_cmd_users.on_user(int(message.from_user.id))
    await message.answer("С возвращением!", reply_markup=menu_keyboard)
    path = os.path.abspath(os.path.join(os.getcwd(), "")) + "/photo-data/Приветствие.png"
    await bot.send_photo(message.from_user.id, open(path, 'rb'))
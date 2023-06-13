import os

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart

from keyboards.default.menu_keyboard import menu_keyboard
from keyboards.default.startmenu_keyboard import startmenu_keyboard
from keyboards.inline.sex_keyboard import sex_keyboard
from loader import dp, bot
from utils.db_api import quick_cmd_users


@dp.message_handler(CommandStart())
async def start(message: types.Message):
    await message.answer(f"Привет, {message.from_user.full_name}!\n", reply_markup=startmenu_keyboard)
    path = os.path.abspath(os.path.join(os.getcwd(), "")) + "/photo-data/Приветствие.png"
    await bot.send_photo(message.from_user.id, open(path, 'rb'))


@dp.message_handler(text="Зарегистрироваться")
async def registration(message: types.Message, state: FSMContext):
    user = await quick_cmd_users.select_user(int(message.from_user.id))
    if user:
        if not user.active:
            await quick_cmd_users.on_user(int(message.from_user.id))
            await message.answer("С возвращением!", reply_markup=menu_keyboard)
            return
        await message.answer("Вы уже зарегистрированы!", reply_markup=menu_keyboard)
        return
    path = os.path.abspath(os.path.join(os.getcwd(), "")) + "/photo-data/Ввести данные.png"
    await bot.send_photo(message.from_user.id, open(path, 'rb'))
    await message.answer("Давай начнём знакомство, про меня ты уже узнал, твоя очередь 😎 Введи своё имя и фамилию 👇🏻")
    await state.set_state("input_fullname")


@dp.message_handler(state="input_fullname")
async def input_fullname(message: types.Message, state: FSMContext):
    await state.update_data(fullname=message.text)
    await message.answer("Я рад помогать всем! Но каждый индивидуален ☺️ С кем мы имеем дело?", reply_markup=sex_keyboard)
    await state.set_state("input_sex")


@dp.callback_query_handler(state="input_sex")
async def input_sex(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()
    await state.update_data(sex=call.data)
    await call.message.answer("Введите свой возраст:")
    await state.set_state("input_age")


@dp.message_handler(state="input_age")
async def input_age(message: types.Message, state: FSMContext):
    try:
        a = int(message.text)
    except:
        await message.answer("Ой-ой, возраст нужно ввести числом, попробуй ещё раз! ")
        return
    await state.update_data(age=message.text)
    await message.answer("Не буду долго мучить, последний вопрос! 😱 Напиши мне свой вес 👇🏻")
    await state.set_state("input_weight")


@dp.message_handler(state="input_weight")
async def input_weight(message: types.Message, state: FSMContext):
    try:
        a = int(message.text)
    except:
        await message.answer("Ой-ой, вес нужно ввести в кг, попробуй ещё раз! ")
        return
    data = await state.get_data()
    await quick_cmd_users.add_user(user_id=int(message.from_user.id), fullname=data.get("fullname"),
                                   sex=data.get("sex"), age=int(data.get("age")), weight=int(message.text))
    await state.reset_data()
    await state.finish()
    await message.answer("Вот и все! Твоя медицинская анкета заполнена, теперь мы — друзья ❤️")
    await message.answer("Можешь воспользоваться моим меню ниже 👇🏻",
                         reply_markup=menu_keyboard)
    path = os.path.abspath(os.path.join(os.getcwd(), "")) + "/photo-data/Регистрация завершена.png"
    await bot.send_photo(message.from_user.id, open(path, 'rb'))

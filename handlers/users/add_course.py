import datetime
import os

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from keyboards.inline.all_confirm_keyboard import confirm_all_keyboard
from keyboards.inline.confirm_keyboard import confirm_keyboard
from loader import dp, bot
from utils.db_api import quick_cmd_courses, quick_cmd_users


@dp.message_handler(text="Добавить курс")
async def add_course(message: types.Message, state: FSMContext):
    user = await quick_cmd_users.select_user(int(message.from_user.id))
    if not user or not user.active:
        await message.answer("Для начала нужно зарегистрироваться.\nПропишите /start")
        return
    await message.answer("Пора начать лечение! ✅ Давай узнаём, что прописал тебе врач, какое лекарство и в какой дозировке. Скажи мне название? 👇🏻")
    path = os.path.abspath(os.path.join(os.getcwd(), "")) + "/photo-data/Начать курс.png"
    await bot.send_photo(message.from_user.id, open(path, 'rb'))
    await state.set_state("input_name")


@dp.message_handler(state="input_name")
async def input_name(message: types.Message, state: FSMContext):
    await state.update_data(name_medicine=message.text)
    await message.answer("Хорошо, введите в каком количестве нужно принимать лекраство:")
    await state.set_state("input_dose")


@dp.message_handler(state="input_dose")
async def input_dose(message: types.Message, state: FSMContext):
    await state.update_data(dose=message.text)
    await message.answer("Теперь введите время, в которое нужно присылать уведомления:\n"
                         "Формат: ЧЧ:ММ")
    await state.set_state("input_times")


@dp.callback_query_handler(state="input_times")
async def confirm_input_times(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()
    await call.message.answer("Окей, введите количество дней прохождения курса:")
    await state.set_state("input_duration")


@dp.message_handler(state="input_times")
async def input_times_ms(message: types.Message, state: FSMContext):
    data = await state.get_data()
    try:
        time_str = str(message.text).split(":")
        int(time_str[0])
        int(time_str[1])
        time = datetime.time(hour=int(time_str[0]), minute=int(time_str[1]))
    except:
        await message.answer("Упс, кажется ты не так ввёл время, проверь правильность написания.")
        return
    if data.get("times"):
        array = data.get("times")
        array.append(time)
        await state.update_data(times=array)
    else:
        array = [time]
        await state.update_data(times=array)
        await message.answer("Продолжайте писать время, если ввод закончен, то нажмите \"Подтвердить\"",
                             reply_markup=confirm_keyboard)


@dp.message_handler(state="input_duration")
async def input_duration(message: types.Message, state: FSMContext):
    try:
        a = int(message.text)
    except:
        await message.answer("Ой-ой, введи количество дней числом и попробуй ещё раз! ")
        return
    await state.update_data(duration=message.text)
    data = await state.get_data()
    name_medicine = data.get("name_medicine")
    dose = data.get("dose")
    times = data.get("times")
    new_times = ""
    for time in times:
        new_times += str(time)[:5] + ", "
    duration = data.get("duration")

    await message.answer(f"Проверьте, правильность введенных данных:\n"
                         f"Название: {name_medicine}\n"
                         f"Доза: {dose}\n"
                         f"Время: {new_times}\n"
                         f"Продолжительность: {duration}", reply_markup=confirm_all_keyboard)
    await state.set_state("confirm")


@dp.callback_query_handler(state="confirm")
async def finish(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()
    data = await state.get_data()
    cb_data = call.data
    if cb_data == "confirm_all":
        user_id = call.from_user.id
        name_medicine = data.get("name_medicine")
        dose = data.get("dose")
        times = data.get("times")
        duration = data.get("duration")
        await quick_cmd_courses.add_course(user_id=int(user_id), name_medicine=name_medicine, dose=dose, times=times,
                                           duration=int(duration))
        await call.message.answer("Поздравляю! Мы поможем тебе не забыть о лечении и скорее выздороветь ❤️🙏🏻")
    else:
        await call.message.answer("Вы отменили ввод!")
    await state.reset_data()
    await state.finish()

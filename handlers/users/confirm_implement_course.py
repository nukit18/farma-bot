from aiogram import types

from loader import dp
from utils.db_api import quick_cmd_confirm_courses


@dp.callback_query_handler(lambda c: c.data.startswith('confirm_implement'))
async def confirm_implement_keyboard(call: types.CallbackQuery):
    try:
        await call.message.edit_reply_markup()
    except:
        pass
    data = str(call.data).split(":")
    course = await quick_cmd_confirm_courses.select_confirm_course(int(data[1]))
    if course.last:
        await call.message.answer("Вы молодцы! Продолжайте в таком же духе!\nПоздравляю с окончанием курса!")
    else:
        await call.message.answer("Вы молодцы! Продолжайте в таком же духе!")
    await quick_cmd_confirm_courses.delete_confirm_course(int(data[1]))

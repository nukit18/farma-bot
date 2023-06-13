import os

from aiogram import types

from data.config import PATH_TO_PHOTO
from loader import dp, bot
from utils.db_api import quick_cmd_users


@dp.message_handler(text="Узнать подробнее о боте")
async def disable_bot(message: types.Message):
    await message.answer(f"Я - Бот Анатолий, меня создали люди, чтобы я мог помогать им следить за здоровьем! "
                         f"Я не врач и не доктор, но стараюсь быть их помощником! "
                         f"Надоедать Вам - не мое желание, я лишь буду напоминать о приеме тех или иных лекарств и давать советы.")
    path = os.path.abspath(os.path.join(os.getcwd(),"")) + "/photo-data/Подробнее о боте.png"
    await bot.send_photo(message.from_user.id, open(path, 'rb'))
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Узнать подробнее о боте")
        ],
        [
            KeyboardButton(text="Добавить курс")
        ],
        [
            KeyboardButton(text="Отключить Анатолия")
        ],

    ],
    resize_keyboard=True
)
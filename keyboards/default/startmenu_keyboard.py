from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

startmenu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Узнать подробнее о боте")
        ],
        [
            KeyboardButton(text="Зарегистрироваться")
        ],
    ],
    resize_keyboard=True
)
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

enable_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Включить Анатолия")
        ],
    ],
    resize_keyboard=True
)
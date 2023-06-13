from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

sex_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Я мужчина", callback_data="male")
        ],
        [
            InlineKeyboardButton(text="Я женщина", callback_data="female")
        ],
    ]
)
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

confirm_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Подтвердить", callback_data="confirm")
        ],
    ]
)
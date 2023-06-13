from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

confirm_all_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Все верно!", callback_data="confirm_all")
        ],
        [
            InlineKeyboardButton(text="Отменить", callback_data="cancel")
        ]
    ]
)
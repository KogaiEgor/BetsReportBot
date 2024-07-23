from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton
)



main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Отчет по работе"),
            KeyboardButton(text="Аккаунты"),
            KeyboardButton(text='Последение ставки')
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Выберит действие из меню"
)

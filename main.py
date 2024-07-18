import os
import asyncio

from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message

from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton
)

from db.db_service import get_rev_and_count, get_accs, get_last_balance


load_dotenv()
bot = Bot(token=os.getenv("API_TOKEN"))
dp = Dispatcher()

main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Отчет по работе"),
            KeyboardButton(text="Аккаунты")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Выберит действие из меню"
)


@dp.message(Command("start"))
async def start(message: Message):
    await message.answer("Hello!", reply_markup=main_kb)


@dp.message(F.text.lower() == "отчет по работе")
async def get_data(message:Message):
    accs = await get_accs(3)
    msg = 'Отчет:\n'
    for acc in accs:
        balance = await get_last_balance(acc[0])
        count, rev = await get_rev_and_count(acc[0])

        msg = msg + f'{acc[1]}\nПоследний баланс - {balance}\nКоличество ставок - {count}\nОборот - {rev}\n\n'

    await message.answer(msg)


@dp.message(F.text.lower() == "аккаунты")
async def get_acc(message:Message):
    accs = await get_accs(3)
    await message.answer(f"Последние 3 аккаунта:\n1. {accs[0][1]}\n2. {accs[1][1]}\n3. {accs[2][1]}")


@dp.message()
async def echo(message: Message):
    await message.answer("Я вас не понял")



async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())


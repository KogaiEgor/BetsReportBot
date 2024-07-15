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

from db.db_service import get_rev_and_count, get_username


load_dotenv()
bot = Bot(token=os.getenv("API_TOKEN"))
dp = Dispatcher()

main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Данные"),
            KeyboardButton(text="Акки")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Выберит действие из меню"
)


@dp.message(Command("start"))
async def start(message: Message):
    await message.answer("Hello!", reply_markup=main_kb)


@dp.message(F.text.lower() == "данные")
async def get_data(message:Message):
    acc_id = 44
    total_amount = await get_rev_and_count(acc_id)
    username = await get_username(acc_id)
    await message.answer(f"Отчет:\n{username}\nКоличество ставок - {total_amount[0][0]}\nОборот - {total_amount[0][1]}")


@dp.message(F.text.lower() == "акки")
async def get_acc(message:Message):
    await message.answer("Акки получены")


@dp.message()
async def echo(message: Message):
    await message.answer("Я вас не понял")



async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())


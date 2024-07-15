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

from db.db_service import get_rev_and_count, get_username, get_last_two_accs


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
    accs = await get_last_two_accs()

    acc_id_1 = accs[0][0]
    total_amount_1 = await get_rev_and_count(acc_id_1)
    username_1 = await get_username(acc_id_1)

    acc_id_2 = accs[1][0]
    total_amount_2 = await get_rev_and_count(acc_id_2)
    username_2 = await get_username(acc_id_2)

    await message.answer(f"Отчет:\n{username_1}\nКоличество ставок - {total_amount_1[0][0]}\nОборот - {total_amount_1[0][1]}"
                         f"\n\n{username_2}\nКоличество ставок - {total_amount_2[0][0]}\nОборот - {total_amount_2[0][1]}")


@dp.message(F.text.lower() == "аккаунты")
async def get_acc(message:Message):
    accs = await get_last_two_accs()
    await message.answer(f"Активные аккаунты:\n1. {accs[0][1]}\n2. {accs[1][1]}")


@dp.message()
async def echo(message: Message):
    await message.answer("Я вас не понял")



async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())


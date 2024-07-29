import os
from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from db import queries
from utils.create_xlsx import create_excel


router = Router()
@router.message(F.text.lower() == "вся история")
async def get_all_data_excel(message: Message):
    await message.answer("Идет загрузка файла")
    stat = await queries.get_daily_stat_for_all()
    balance = await queries.get_daily_balance_for_all()
    await create_excel(stat, balance)

    filename = os.path.join(os.getcwd(), 'Report.xlsx')
    if os.path.exists(filename):
        file = FSInputFile(filename)
        await message.reply_document(file)
        os.remove(filename)
    else:
        await message.reply("Ошибка при создании файла отчета")


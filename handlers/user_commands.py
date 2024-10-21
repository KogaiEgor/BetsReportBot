from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from db.queries.stat_queries import (
    get_rev_and_count,
    get_last_balance,
    get_start_balance,
    get_last_bets,
    get_working_time
)
from db.queries.accs_queries import get_active_accs, get_accs
from keyboards.keyboard import main_kb


router = Router()

@router.message(CommandStart())
async def start(message: Message):
    await message.answer("Hello!")


@router.message(Command("work_report"))
async def get_data(message:Message):
    accs = await get_active_accs()
    msg = 'Отчет:\n'
    for acc in accs:
        balance = await get_last_balance(acc[0])
        start_balance = await get_start_balance(acc[0])
        count, rev = await get_rev_and_count(acc[0])

        msg = msg + f'{acc[1]}\nCтартовый баланс - {start_balance}\nПоследний баланс - {balance}\nКоличество ставок - {count}\nОборот - {rev}\n\n'

    await message.answer(msg)


@router.message(Command("accs_report"))
async def get_repor_by_acc(message: Message):
    accs = await get_accs(65)
    msg = ''

    for acc in accs:
        acc_id = acc[0]
        username = acc[1]

        balance = await get_last_balance(acc_id)
        start_balance = await get_start_balance(acc_id)
        count, rev = await get_rev_and_count(acc_id)
        working_time = await get_working_time(acc_id)

        msg = msg + f'{username}\n' \
                    f'Время работы - {working_time}\n' \
                    f'Cтартовый баланс - {start_balance}\n' \
                    f'Последний баланс - {balance}\n' \
                    f'Количество ставок - {count}\n' \
                    f'Оборот - {rev}\n' \
                    f'РОИ: {round(((balance - start_balance) / rev) * 100, 2)}%\n\n'

    await message.answer(msg)

@router.message(Command("last_bets"))
async def get_last_bets_handler(message: Message):
    data = await get_last_bets(10)

    msg = 'Последние 10 ставок:\n'
    for record in data:
        acc_id, balance, bet, bet_type, timestamp = record
        formatted_timestamp = timestamp.strftime('%Y-%m-%d %H:%M:%S')

        msg = msg + f'{acc_id}\nБаланс - {balance}\nСтавка - {bet}\nТип - {bet_type}\nВремя - {formatted_timestamp}\n\n'

    await message.answer(msg)

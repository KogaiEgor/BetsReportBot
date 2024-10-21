from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from utils.states import StatByDay
from db.queries.accs_queries import get_accs
from db.queries.daily_balance import get_balance_by_day
from db.queries.daily_stat import get_statistic_by_day



router = Router()

@router.message(Command("daily_report"))
async def ask_acc_id(message: Message, state: FSMContext):
    await state.set_state(StatByDay.acc_id)
    accs = await get_accs(42)
    msg = "Введите id аккаунта:\n"
    for i in range(1, len(accs) + 1):
        login = accs[i - 1][1]
        msg = msg + f'{accs[i - 1][0]}. {login}\n'

    await message.answer(msg)


@router.message(StatByDay.acc_id)
async def get_stat_by_day(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Некоректный id аккаунта")
        return

    acc_id = int(message.text)
    await state.update_data(acc_id=acc_id)

    balances = await get_balance_by_day(acc_id)
    stats = await get_statistic_by_day(acc_id)

    msg = 'Отчет:\n'

    for i in range(len(stats)):
        start_balance, end_balance = balances[i][1], balances[i][2]
        count, rev = stats[i][1], stats[i][2]
        profit = end_balance-start_balance

        msg = msg + f"{i + 1}-й день:\nНАЧАЛЬНЫЙ БАЛАНС: {start_balance}\nКол-во ставок: {count}\nСумма оборота: {rev}\n" \
                    f"Профит: {round(profit, 3)}\nROI: {round((profit / rev) * 100, 3)}\nКОНЕЧНЫЙ БАЛАНС: {end_balance}\n\n"

    await message.answer(msg)






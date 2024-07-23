import asyncio

from sqlalchemy import select, desc
from sqlalchemy.sql import func

from db.database import async_session
from db.models import BetModel, AccountModel


async def get_rev_and_count(acc_id: int):
    async with async_session() as session:
        result = await session.execute(
            select(func.count(BetModel.amount), func.sum(BetModel.amount)).where(BetModel.acc_id == acc_id)
        )
        # rows = []
        # for row in result:
        #     count, total_sum = row
        #     rows.append((count, total_sum))

        return result.all()[0]


async def get_active_accs():
    async with async_session() as session:
        result = await session.execute(
            select(BetModel.acc_id).order_by(desc(BetModel.id)).limit(6)
        )
        accs = set()
        for acc_id in result:
            accs.add(acc_id[0])

        active_accs = await session.execute(
            select(AccountModel.id, AccountModel.login).where(AccountModel.id.in_(accs))
        )
        rows = []
        for row in active_accs.all():
            rows.append((row.id, row.login))

        return rows


async def get_accs(amount: int):
    async with async_session() as session:
        result = await session.execute(
            select(AccountModel.id, AccountModel.login).order_by(desc(AccountModel.id)).limit(amount)
        )
        rows = []
        for row in result.all():
            rows.append((row.id, row.login))

        return rows


async def get_last_balance(acc_id: int):
    async with async_session() as session:
        result = await session.execute(
            select(BetModel.balance).where(BetModel.acc_id == acc_id).order_by(desc(BetModel.id)).limit(1)
        )

        return result.scalar()


async def get_start_balance(acc_id: int):
    async with async_session() as session:
        result = await session.execute(
            select(BetModel.balance).where(BetModel.acc_id == acc_id).limit(1)
        )

        return result.scalar()


async def get_last_bets(bets_limit: int, accs_ids=None):
    async with async_session() as session:
        stmt = (
            select(AccountModel.login, BetModel.balance, BetModel.amount, BetModel.bet_datetime)
            .join(AccountModel, BetModel.acc_id == AccountModel.id)
            .order_by(desc(BetModel.id))
            .limit(bets_limit)
        )

        if accs_ids:
            stmt = stmt.where(BetModel.acc_id.in_(accs_ids))

        result = await session.execute(stmt)
        return result.all()

# async def main():
#     data = await get_last_ten_bets()
#
#     msg = 'Последние 10 ставок:\n'
#     for record in data:
#         acc_id, balance, bet, timestamp = record
#         formatted_timestamp = timestamp.strftime('%Y-%m-%d %H:%M:%S')
#
#         msg = msg + f'{acc_id}\nБаланс - {balance}\nСтавка - {bet}\nВремя - {formatted_timestamp}\n\n'
#
#     print(msg)
#
#
#
# if __name__ == "__main__":
#     asyncio.run(main())


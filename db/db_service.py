import asyncio

from sqlalchemy import select, desc
from sqlalchemy.sql import func
from sqlalchemy.orm import aliased

from db.database import async_session
from db.models import BetModel, AccountModel


async def get_rev_and_count(acc_id: int):
    async with async_session() as session:
        result = await session.execute(
            select(func.count(BetModel.amount), func.sum(BetModel.amount)).where(BetModel.acc_id == acc_id)
        )

        return result.all()[0]


async def get_statistic_by_day(acc_id: int):
    async with async_session() as session:
        day_trunc = func.date_trunc('day', BetModel.bet_datetime).label('day')
        stmt = (
            select(
                day_trunc,
                func.count(BetModel.amount),
                func.sum(BetModel.amount)
            )
            .where(
                BetModel.acc_id == acc_id,
            )
            .group_by(day_trunc)
            .order_by(day_trunc)
        )
        result = await session.execute(stmt)
        return result.all()


async def get_balance_by_day(acc_id: int):
    async with async_session() as session:
        day_trunc = func.date_trunc('day', BetModel.bet_datetime).label('day')

        subquery = (
            select(
                day_trunc,
                func.min(BetModel.bet_datetime).label('first_bet_datetime'),
                func.max(BetModel.bet_datetime).label('last_bet_datetime')
            )
            .where(
                BetModel.acc_id == acc_id,
            )
            .group_by(day_trunc)
            .subquery()
        )

        first_bets = aliased(BetModel)
        last_bets = aliased(BetModel)

        stmt = (
            select(
                subquery.c.day,
                first_bets.balance,
                last_bets.balance
            )
            .join(first_bets, first_bets.bet_datetime == subquery.c.first_bet_datetime)
            .join(last_bets, last_bets.bet_datetime == subquery.c.last_bet_datetime)
        )

        result = await session.execute(stmt)
        return result.all()


async def get_active_accs():
    async with async_session() as session:
        result = await session.execute(
            select(BetModel.acc_id).order_by(desc(BetModel.id)).limit(8)
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


async def get_spain_accs():
    async with async_session() as session:
        result = await session.execute(
            select(AccountModel.id, AccountModel.login).where(AccountModel.id >= 42)
        )

        rows = []
        for row in result.all():
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
#     data = await get_spain_accs()
#     print(data)
#
# if __name__ == "__main__":
#     asyncio.run(main())


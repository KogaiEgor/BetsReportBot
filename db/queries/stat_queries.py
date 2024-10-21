from sqlalchemy import select, desc
from sqlalchemy.sql import func
from sqlalchemy.orm import query

from db.database import async_session
from db.models import BetModel, AccountModel




async def get_rev_and_count(acc_id: int):
    async with async_session() as session:
        result = await session.execute(
            select(func.count(BetModel.amount), func.sum(BetModel.amount)).where(BetModel.acc_id == acc_id)
        )

        return result.all()[0]


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


async def get_working_time(acc_id: int):
    async with async_session() as session:
        first_row_subquery = select(BetModel.bet_datetime).filter(BetModel.acc_id == acc_id).order_by(
            BetModel.bet_datetime.asc()).limit(1).scalar_subquery()

        last_row_subquery = select(BetModel.bet_datetime).filter(BetModel.acc_id == acc_id).order_by(
            BetModel.bet_datetime.desc()).limit(1).scalar_subquery()

        time_difference_query = select(last_row_subquery - first_row_subquery)

        result = await session.execute(time_difference_query)
        time_difference = result.scalar()

        time_diff = str(time_difference).split('.')[0]
        return time_diff


async def get_last_bets(bets_limit: int, accs_ids=None):
    async with async_session() as session:
        stmt = (
            select(AccountModel.login, BetModel.balance, BetModel.amount, BetModel.arb_or_value, BetModel.bet_datetime)
            .join(AccountModel, BetModel.acc_id == AccountModel.id)
            .order_by(desc(BetModel.id))
            .limit(bets_limit)
        )

        if accs_ids:
            stmt = stmt.where(BetModel.acc_id.in_(accs_ids))

        result = await session.execute(stmt)
        return result.all()



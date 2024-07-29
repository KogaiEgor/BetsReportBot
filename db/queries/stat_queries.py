from sqlalchemy import select, desc
from sqlalchemy.sql import func

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



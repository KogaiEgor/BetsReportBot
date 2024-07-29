from sqlalchemy import select
from sqlalchemy.sql import func

from db.database import async_session
from db.models import BetModel



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


async def get_daily_stat_for_all():
    async with async_session() as session:
        day_trunc = func.date_trunc('day', BetModel.bet_datetime).label('day')
        stmt = (
            select(
                day_trunc,
                func.count(BetModel.amount),
                func.sum(BetModel.amount),
                BetModel.acc_id
            )
            .where(
                BetModel.acc_id >= 42,
            )
            .group_by(day_trunc, BetModel.acc_id)
            .order_by(BetModel.acc_id, day_trunc)
        )
        result = await session.execute(stmt)
        return result.all()


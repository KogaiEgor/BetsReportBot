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



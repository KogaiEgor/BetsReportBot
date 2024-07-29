from sqlalchemy import select
from sqlalchemy.sql import func
from sqlalchemy.orm import aliased

from db.database import async_session
from db.models import BetModel


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


async def get_daily_balance_for_all():
    async with async_session() as session:
        day_trunc = func.date_trunc('day', BetModel.bet_datetime).label('day')

        subquery = (
            select(
                day_trunc,
                func.min(BetModel.bet_datetime).label('first_bet_datetime'),
                func.max(BetModel.bet_datetime).label('last_bet_datetime'),
                BetModel.acc_id
            )
            .where(
                BetModel.acc_id >= 42,
            )
            .group_by(day_trunc, BetModel.acc_id)
            .subquery()
        )

        first_bets = aliased(BetModel)
        last_bets = aliased(BetModel)

        stmt = (
            select(
                subquery.c.day,
                first_bets.balance,
                last_bets.balance,
                subquery.c.acc_id
            )
            .join(first_bets, first_bets.bet_datetime == subquery.c.first_bet_datetime)
            .join(last_bets, last_bets.bet_datetime == subquery.c.last_bet_datetime)
            .order_by(subquery.c.acc_id, subquery.c.day)
        )

        result = await session.execute(stmt)
        return result.all()


from sqlalchemy import select, desc, distinct
from datetime import datetime, timedelta, timezone

import asyncio
from db.database import async_session
from db.models import BetModel, AccountModel



async def get_active_accs():
    async with async_session() as session:
        subquery = (
            select(BetModel.acc_id, BetModel.bet_datetime)
            .where(BetModel.bet_datetime >= (datetime.now() - timedelta(hours=12)))
            .order_by(BetModel.bet_datetime.desc())
            .subquery()
        )

        query = (
            select(distinct(subquery.c.acc_id))
            .limit(10)
        )

        result = await session.execute(query)

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


async def get_accs(n: int):
    """
    Get all accs from n to the last
    :param n: int
    :return:
    """
    async with async_session() as session:
        result = await session.execute(
            select(AccountModel.id, AccountModel.login).where(AccountModel.id >= n)
        )

        rows = []
        for row in result.all():
            rows.append((row.id, row.login))

        return rows

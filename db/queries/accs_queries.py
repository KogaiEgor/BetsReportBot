from sqlalchemy import select, desc

from db.database import async_session
from db.models import BetModel, AccountModel



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



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
        rows = []
        for row in result:
            count, total_sum = row
            rows.append((count, total_sum))

        return rows


async def get_username(acc_id: int):
    async with async_session() as session:
        result = await session.execute(
            select(AccountModel).where(AccountModel.id == acc_id)
        )
        username = result.scalar()
        return username.login

async def get_last_two_accs():
    async with async_session() as session:
        result = await session.execute(
            select(AccountModel.id, AccountModel.login).order_by(desc(AccountModel.id)).limit(2)
        )
        rows = []
        for row in result.all():
            rows.append((row.id, row.login))

        return rows

# async def main():
#     # acc_id = 44
#     # count = await get_rev_and_count(acc_id)
#     # username = await get_username(acc_id)
#     # print(f"{username} = {count}")
#     data = await get_last_two_accs()
#     print(data)
#
#
#
# if __name__ == "__main__":
#     asyncio.run(main())


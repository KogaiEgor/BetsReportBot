import asyncio
import queries

async def main():
    data = await queries.get_daily_stat_for_all()
    print(data)

if __name__ == "__main__":
    asyncio.run(main())


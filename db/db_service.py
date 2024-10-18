import asyncio
import queries

async def main():
    data = await queries.get_last_bets(10, [70])
    print(data)

if __name__ == "__main__":
    asyncio.run(main())


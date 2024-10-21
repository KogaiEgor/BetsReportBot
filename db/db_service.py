import asyncio
import queries

async def main():
    data = await queries.delete_acc(74)
    print(data)

if __name__ == "__main__":
    asyncio.run(main())


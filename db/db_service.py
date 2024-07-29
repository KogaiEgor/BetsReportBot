import asyncio
import queries

async def main():
    data = await queries.get_spain_accs()
    print(data)

if __name__ == "__main__":
    asyncio.run(main())

